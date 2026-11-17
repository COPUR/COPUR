"""Adapters for paginated GitHub visibility checks, atomic file writes, and byte-exact parity checks."""

from __future__ import annotations

import difflib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Mapping, Set, Tuple

from .domain import Catalog, VerificationResult, VisibilityGateway


class OfflineVisibilityGateway:
    """No-op gateway used with --offline."""

    def fetch_visibilities(self, owner: str) -> Tuple[Mapping[str, str], bool]:
        return {}, False


class GhCliVisibilityGateway:
    """Paginated GitHub visibility fetcher via gh CLI (never truncates at 200)."""

    def fetch_visibilities(self, owner: str) -> Tuple[Mapping[str, str], bool]:
        # 1. Authenticated owner endpoint returns both PUBLIC and PRIVATE repos.
        vis_map, ok_private = self._run_paginated_api("user/repos?affiliation=owner&per_page=100")
        if ok_private and vis_map:
            return vis_map, True

        # 2. Fallback to public user endpoint (e.g. repo-scoped GITHUB_TOKEN in CI).
        vis_map_pub, ok_pub = self._run_paginated_api(f"users/{owner}/repos?per_page=100&type=all")
        if ok_pub:
            return vis_map_pub, False

        # 3. Last fallback: gh repo list with high limit guard.
        proc = subprocess.run(
            ["gh", "repo", "list", owner, "--limit", "1000", "--json", "name,visibility"],
            shell=False,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"gh repo list failed: {proc.stderr.strip()}")
        data = json.loads(proc.stdout)
        if len(data) >= 950:
            raise RuntimeError("gh repo list approached 1000 limit; paginated API required")
        out = {item["name"]: str(item["visibility"]).upper() for item in data}
        has_priv = any(v == "PRIVATE" for v in out.values())
        return out, has_priv

    def _run_paginated_api(self, endpoint: str) -> Tuple[Dict[str, str], bool]:
        proc = subprocess.run(
            ["gh", "api", "--paginate", "--slurp", endpoint],
            shell=False,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if proc.returncode != 0 or not proc.stdout.strip():
            return {}, False
        try:
            pages = json.loads(proc.stdout)
        except json.JSONDecodeError:
            return {}, False
        vis: Dict[str, str] = {}
        items = []
        if isinstance(pages, list):
            for entry in pages:
                if isinstance(entry, list):
                    items.extend(entry)
                elif isinstance(entry, dict):
                    items.append(entry)
        for item in items:
            name = item.get("name")
            if not name:
                continue
            is_priv = bool(item.get("private", False))
            vis[str(name)] = "PRIVATE" if is_priv else "PUBLIC"
        return vis, True


class GitHubVisibilityVerifier:
    """Verifies catalog visibility assertions against live GitHub repository visibilities."""

    def __init__(self, gateway: VisibilityGateway) -> None:
        self._gateway = gateway

    def verify(self, catalog: Catalog, strict_verification: bool = False) -> VerificationResult:
        vis_map, includes_private = self._gateway.fetch_visibilities(catalog.metadata.owner.github_handle)
        errors: List[str] = []
        warnings: List[str] = []
        checked = 0

        for repo in catalog.repositories:
            if not repo.github_repo_name:
                continue
            checked += 1
            actual = vis_map.get(repo.github_repo_name)
            if repo.visibility == "PUBLIC":
                if actual != "PUBLIC":
                    errors.append(
                        f"Expected PUBLIC repo {repo.github_repo_name}, live GitHub returned {actual!r}"
                    )
            elif repo.visibility == "PRIVATE":
                if actual == "PUBLIC":
                    errors.append(
                        f"UNEXPECTED_PUBLIC_EXPOSURE: catalog marks {repo.github_repo_name} PRIVATE, live GitHub is PUBLIC"
                    )
                elif actual is None:
                    msg = f"Cannot verify PRIVATE repo {repo.github_repo_name} with current token scope"
                    if strict_verification:
                        errors.append(msg)
                    else:
                        warnings.append(msg)
            elif repo.visibility == "IN_DESIGN":
                if actual is not None:
                    errors.append(f"STALE_IN_DESIGN: {repo.github_repo_name} exists on GitHub as {actual}")
            elif repo.visibility == "PENDING_REPO_VERIFICATION":
                msg = f"Pending repository verification: {repo.github_repo_name}"
                if strict_verification:
                    errors.append(msg)
                else:
                    warnings.append(msg)

        return VerificationResult(
            ok=len(errors) == 0,
            warnings=tuple(warnings),
            errors=tuple(errors),
            checked_repos=checked,
        )


def _managed_brief_paths(root: Path) -> Set[Path]:
    paths: Set[Path] = set()
    for folder, suffix in ((root / "briefs", ".md"), (root / "docs" / "briefs", ".html")):
        if folder.is_dir():
            for child in folder.iterdir():
                if child.is_file() and child.name.endswith(suffix):
                    paths.add(child)
    return paths


class AtomicWriter:
    """Atomically writes deterministic UTF-8 LF outputs and prunes orphan briefs."""

    def write_all(self, root: Path, artifacts: Mapping[str, str]) -> Tuple[int, int]:
        written = 0
        unchanged = 0
        expected_paths: Set[Path] = set()

        for rel, content in sorted(artifacts.items()):
            target = root / rel
            expected_paths.add(target)
            target.parent.mkdir(parents=True, exist_ok=True)
            data = content.replace("\r\n", "\n").encode("utf-8")
            if target.is_file() and target.read_bytes() == data:
                unchanged += 1
                continue
            fd, tmp_name = tempfile.mkstemp(prefix=".tmp_", dir=str(target.parent))
            tmp_path = Path(tmp_name)
            try:
                with os.fdopen(fd, "wb") as fh:
                    fh.write(data)
                    fh.flush()
                    os.fsync(fh.fileno())
                os.chmod(tmp_path, 0o644)
                os.replace(tmp_path, target)
                written += 1
            except Exception:
                if tmp_path.exists():
                    tmp_path.unlink()
                raise

        for existing in _managed_brief_paths(root):
            if existing not in expected_paths:
                existing.unlink()
        return written, unchanged


class CheckComparator:
    """Byte-exact parity verifier for --check mode without mutating disk."""

    def verify_all(self, root: Path, artifacts: Mapping[str, str]) -> List[str]:
        diffs: List[str] = []
        expected_paths: Set[Path] = set()

        for rel, content in sorted(artifacts.items()):
            target = root / rel
            expected_paths.add(target)
            expected_bytes = content.replace("\r\n", "\n").encode("utf-8")
            if not target.is_file():
                diffs.append(f"MISSING generated file: {rel}")
                continue
            disk_bytes = target.read_bytes()
            if disk_bytes != expected_bytes:
                disk_lines = disk_bytes.decode("utf-8", errors="replace").splitlines(keepends=True)
                exp_lines = expected_bytes.decode("utf-8").splitlines(keepends=True)
                diff = "".join(
                    difflib.unified_diff(disk_lines, exp_lines, fromfile=f"disk/{rel}", tofile=f"ssot/{rel}", n=2)
                )
                diffs.append(f"DRIFT detected in {rel}:\n{diff[:1200]}")

        for existing in sorted(_managed_brief_paths(root)):
            if existing not in expected_paths:
                diffs.append(f"ORPHAN managed brief file: {existing.relative_to(root)}")
        return diffs
