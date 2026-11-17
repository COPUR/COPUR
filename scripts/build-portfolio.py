#!/usr/bin/env python3
"""CLI compiler and parity verifier for the COPUR SSOT portfolio catalog."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, Sequence

from portfolio_compiler.adapters import (
    AtomicWriter,
    CheckComparator,
    GhCliVisibilityGateway,
    GitHubVisibilityVerifier,
)
from portfolio_compiler.renderers import render_all
from portfolio_compiler.validator import CatalogLoader, HygieneScanner, InvariantValidator

EXIT_OK = 0
EXIT_VALIDATION_OR_HYGIENE = 1
EXIT_DRIFT = 2
EXIT_GITHUB_VISIBILITY = 3


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compile and verify COPUR SSOT portfolio outputs (Python 3 stdlib only)."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--build", action="store_true", help="Validate SSOT and write deterministic outputs")
    mode.add_argument("--check", action="store_true", help="Validate SSOT and verify byte-exact parity on disk")

    gh_mode = parser.add_mutually_exclusive_group()
    gh_mode.add_argument("--verify-github", action="store_true", help="Verify live GitHub repo visibilities")
    gh_mode.add_argument("--offline", action="store_true", help="Skip live GitHub visibility checks")

    parser.add_argument("--strict-verification", action="store_true", help="Fail if any repo is unverified or pending")
    parser.add_argument("--strict-hygiene", action="store_true", help="Treat hygiene warnings as errors")
    parser.add_argument(
        "--catalog",
        default="catalog/portfolio-catalog.json",
        help="Relative or absolute path to portfolio-catalog.json",
    )
    parser.add_argument(
        "--schema",
        default="catalog/portfolio-catalog.schema.json",
        help="Relative or absolute path to portfolio-catalog.schema.json",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    catalog_path = Path(args.catalog) if Path(args.catalog).is_absolute() else root / args.catalog
    schema_path = Path(args.schema) if Path(args.schema).is_absolute() else root / args.schema

    loader = CatalogLoader()
    try:
        raw = loader.load_raw(catalog_path)
    except Exception as exc:
        print(f"ERROR loading catalog: {exc}", file=sys.stderr)
        return EXIT_VALIDATION_OR_HYGIENE

    schema_errors = loader.validate_schema(raw, schema_path)
    catalog, parse_errors = loader.parse(raw)
    all_errors = schema_errors + parse_errors
    if catalog is None or all_errors:
        for err in all_errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return EXIT_VALIDATION_OR_HYGIENE

    val_errors = InvariantValidator().validate(catalog, strict_verification=args.strict_verification)
    if val_errors:
        for err in val_errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return EXIT_VALIDATION_OR_HYGIENE

    artifacts = render_all(catalog)
    scan_inputs: Dict[str, str] = {
        str(catalog_path.relative_to(root) if catalog_path.is_relative_to(root) else catalog_path): catalog_path.read_text(encoding="utf-8")
    }
    scan_inputs.update(artifacts)

    findings = HygieneScanner().scan_artifacts(catalog, scan_inputs, strict_hygiene=args.strict_hygiene)
    blocking = [
        f
        for f in findings
        if f.severity == "CRITICAL" or (args.strict_hygiene and f.severity == "WARNING")
    ]
    for f in findings:
        print(f"[{f.severity}] {f.rule_id} ({f.location}): {f.detail}", file=sys.stderr)
    if blocking:
        return EXIT_VALIDATION_OR_HYGIENE

    if args.verify_github:
        try:
            ver_result = GitHubVisibilityVerifier(GhCliVisibilityGateway()).verify(
                catalog, strict_verification=args.strict_verification
            )
        except Exception as exc:
            print(f"ERROR verifying GitHub visibilities: {exc}", file=sys.stderr)
            return EXIT_GITHUB_VISIBILITY
        for warn in ver_result.warnings:
            print(f"WARNING: {warn}", file=sys.stderr)
        if not ver_result.ok:
            for err in ver_result.errors:
                print(f"ERROR: {err}", file=sys.stderr)
            return EXIT_GITHUB_VISIBILITY
        print(f"GitHub visibility verified for {ver_result.checked_repos} repositories.")

    if args.build:
        written, unchanged = AtomicWriter().write_all(root, artifacts)
        print(f"Built SSOT outputs: written={written}, unchanged={unchanged}")
        return EXIT_OK

    diffs = CheckComparator().verify_all(root, artifacts)
    if diffs:
        for d in diffs:
            print(d, file=sys.stderr)
        return EXIT_DRIFT
    print(f"Check passed: all {len(artifacts)} deterministic files match SSOT byte-for-byte.")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
