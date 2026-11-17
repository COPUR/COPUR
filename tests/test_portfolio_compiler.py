"""Unit, invariant, hygiene, link-resolution, and architecture-boundary tests for portfolio_compiler."""

from __future__ import annotations

import ast
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from portfolio_compiler.adapters import AtomicWriter, CheckComparator, GitHubVisibilityVerifier  # noqa: E402
from portfolio_compiler.renderers import SurfaceLinkResolver, render_all  # noqa: E402
from portfolio_compiler.validator import CatalogLoader, HygieneScanner, InvariantValidator  # noqa: E402


class FakeVisibilityGateway:
    def __init__(self, vis_map: dict[str, str], includes_private: bool = True) -> None:
        self._vis = vis_map
        self._priv = includes_private

    def fetch_visibilities(self, owner: str):
        return self._vis, self._priv


class PortfolioCompilerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog_path = ROOT / "catalog" / "portfolio-catalog.json"
        self.schema_path = ROOT / "catalog" / "portfolio-catalog.schema.json"
        self.loader = CatalogLoader()
        self.raw = self.loader.load_raw(self.catalog_path)
        catalog, errors = self.loader.parse(self.raw)
        self.assertEqual(errors, [])
        assert catalog is not None
        self.catalog = catalog

    def test_live_catalog_passes_schema_and_all_invariants(self) -> None:
        schema_errors = self.loader.validate_schema(self.raw, self.schema_path)
        self.assertEqual(schema_errors, [])
        val_errors = InvariantValidator().validate(self.catalog, strict_verification=True)
        self.assertEqual(val_errors, [])

    def test_duplicate_repo_ownership_is_rejected(self) -> None:
        bad = copy.deepcopy(self.raw)
        bad["repositories"][1]["githubRepoName"] = bad["repositories"][0]["githubRepoName"]
        cat, _ = self.loader.parse(bad)
        assert cat is not None
        errs = InvariantValidator().validate(cat)
        self.assertTrue(any("VAL-04" in e for e in errs))

    def test_suite_7_and_8_cross_reference_is_rejected(self) -> None:
        bad = copy.deepcopy(self.raw)
        for repo in bad["repositories"]:
            if repo["canonicalSuiteId"] == "suite-07-consent-ev-pnc":
                repo["referencedBySuites"] = ["suite-08-wallet-pnc-ev"]
                break
        cat, _ = self.loader.parse(bad)
        assert cat is not None
        errs = InvariantValidator().validate(cat)
        self.assertTrue(any("VAL-06" in e for e in errs))

    def test_missing_proof_link_is_rejected(self) -> None:
        bad = copy.deepcopy(self.raw)
        bad["proofLinks"] = [p for p in bad["proofLinks"] if p["suiteId"] != "suite-10-serverless-news-observability"]
        cat, _ = self.loader.parse(bad)
        assert cat is not None
        errs = InvariantValidator().validate(cat)
        self.assertTrue(any("VAL-07" in e for e in errs))

    def test_hygiene_scanner_flags_private_url_leak_and_unsafe_dom(self) -> None:
        scanner = HygieneScanner()
        findings = scanner.scan_artifacts(
            self.catalog,
            {
                "docs/index.html": (
                    '<a href="https://github.com/COPUR/MasruFi_Framework">bad</a>\n'
                    '<script>el.innerHTML = x;</script>'
                )
            },
            strict_hygiene=True,
        )
        rules = {f.rule_id for f in findings}
        self.assertIn("NON_PUBLIC_URL_LEAK", rules)
        self.assertIn("UNSAFE_DOM_PATTERN", rules)

    def test_hygiene_scanner_flags_prohibited_tenure_and_excluded_terms(self) -> None:
        scanner = HygieneScanner()
        sample_tenure = " ".join(["16+", "Years", "Experience"])
        sample_excluded = "steer" + "f0cus"
        findings = scanner.scan_artifacts(
            self.catalog,
            {"README.md": f"{sample_tenure}\n{sample_excluded}"},
            strict_hygiene=True,
        )
        rules = {f.rule_id for f in findings}
        self.assertIn("PROHIBITED_TENURE_CLAIMS", rules)
        self.assertIn("EXCLUDED_METADATA", rules)

    def test_rendered_outputs_are_clean_and_surface_links_resolve(self) -> None:
        artifacts = render_all(self.catalog)
        self.assertIn("README.md", artifacts)
        self.assertIn("PROJECTS.md", artifacts)
        self.assertIn("docs/index.html", artifacts)
        self.assertIn("docs/.nojekyll", artifacts)
        self.assertIn("briefs/suite-10-serverless-c4.md", artifacts)
        self.assertIn("docs/briefs/suite-10-serverless-c4.html", artifacts)

        findings = HygieneScanner().scan_artifacts(self.catalog, artifacts, strict_hygiene=True)
        self.assertEqual(findings, [])

        html_out = artifacts["docs/index.html"]
        self.assertEqual(html_out.count('<article class="card"'), 10)
        self.assertIn("briefs/suite-10-serverless-c4.html", html_out)
        self.assertIn("Enterprise Engineering Standards", html_out)
        self.assertIn('property="og:url" content="https://copur.github.io/"', html_out)

        resolver = SurfaceLinkResolver(self.catalog)
        suite10_brief_proof = next(
            p for p in self.catalog.proof_links if p.proof_id == "proof-suite-10-brief"
        )
        self.assertEqual(resolver.resolve_proof(suite10_brief_proof, "MARKDOWN").href, "./briefs/suite-10-serverless-c4.md")
        self.assertEqual(resolver.resolve_proof(suite10_brief_proof, "HTML_SHOWCASE").href, "briefs/suite-10-serverless-c4.html")

    def test_atomic_writer_and_check_comparator_roundtrip(self) -> None:
        artifacts = render_all(self.catalog)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            written, unchanged = AtomicWriter().write_all(tmp_root, artifacts)
            self.assertEqual(written, len(artifacts))
            self.assertEqual(unchanged, 0)
            self.assertEqual(CheckComparator().verify_all(tmp_root, artifacts), [])

            # Mutate one byte on disk and verify CheckComparator catches drift
            readme = tmp_root / "README.md"
            readme.write_text(readme.read_text(encoding="utf-8") + "\nmanual-edit\n", encoding="utf-8")
            diffs = CheckComparator().verify_all(tmp_root, artifacts)
            self.assertEqual(len(diffs), 1)
            self.assertIn("README.md", diffs[0])

    def test_github_visibility_verifier_catches_unexpected_public_exposure(self) -> None:
        vis_map = {
            r.github_repo_name: r.visibility
            for r in self.catalog.repositories
            if r.github_repo_name
        }
        res_ok = GitHubVisibilityVerifier(FakeVisibilityGateway(vis_map)).verify(
            self.catalog, strict_verification=True
        )
        self.assertTrue(res_ok.ok)

        bad_map = dict(vis_map)
        bad_map["MasruFi_Framework"] = "PUBLIC"
        res_bad = GitHubVisibilityVerifier(FakeVisibilityGateway(bad_map)).verify(
            self.catalog, strict_verification=True
        )
        self.assertFalse(res_bad.ok)
        self.assertTrue(any("UNEXPECTED_PUBLIC_EXPOSURE" in e for e in res_bad.errors))

    def test_domain_module_has_zero_io_or_outer_layer_imports(self) -> None:
        domain_src = (ROOT / "scripts" / "portfolio_compiler" / "domain.py").read_text(encoding="utf-8")
        tree = ast.parse(domain_src)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        forbidden = {"os", "subprocess", "pathlib", "adapters", "renderers", "validator"}
        self.assertEqual(imported & forbidden, set())
