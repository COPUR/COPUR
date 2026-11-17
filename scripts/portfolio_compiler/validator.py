"""SSOT loading, stdlib schema/invariant validation (VAL-01..VAL-09), and HygieneScanner."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Set, Tuple

from .domain import (
    ALLOWED_DOMAINS,
    ALLOWED_ENTRY_KINDS,
    ALLOWED_EVIDENCE_TYPES,
    ALLOWED_MATURITY_TIERS,
    ALLOWED_SPONSOR_TYPES,
    ALLOWED_STANDARD_NAMES,
    ALLOWED_VISIBILITIES,
    BriefEntry,
    Catalog,
    CatalogMetadata,
    DomainEntry,
    EngineeringStandard,
    EnterpriseControl,
    HygieneFinding,
    OwnerMetadata,
    ProofLinkEntry,
    RepositoryEntry,
    SuiteEntry,
)

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SUITE_ID_RE = re.compile(r"^suite-(?:0[1-9]|10)-[a-z0-9-]+$")
GITHUB_REPO_NAME_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
EXPECTED_DOMAIN_SUITES: Mapping[str, Set[int]] = {
    "D1_AGENTIC_AI": {1, 2},
    "D2_OPEN_FINANCE_CORE": {3, 4, 5, 6},
    "D3_EV_MOBILITY": {7, 8, 9},
    "D4_SERVERLESS_INTELLIGENCE": {10},
}


def reject_duplicate_keys(pairs: Sequence[Tuple[str, Any]]) -> Dict[str, Any]:
    obj: Dict[str, Any] = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"Duplicate JSON object key: {key!r}")
        obj[key] = value
    return obj


class CatalogLoader:
    """Loads and validates catalog JSON structure using stdlib (+ optional jsonschema)."""

    def load_raw(self, catalog_path: Path) -> Dict[str, Any]:
        text = catalog_path.read_text(encoding="utf-8")
        data = json.loads(text, object_pairs_hook=reject_duplicate_keys)
        if not isinstance(data, dict):
            raise ValueError("Catalog root must be a JSON object")
        return data

    def validate_schema(self, raw: Mapping[str, Any], schema_path: Path) -> List[str]:
        errors: List[str] = []
        schema_raw = json.loads(
            schema_path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_keys,
        )
        required_top = set(schema_raw.get("required", []))
        actual_keys = set(raw.keys())
        missing = sorted(required_top - actual_keys)
        extra = sorted(actual_keys - set(schema_raw.get("properties", {}).keys()))
        if missing:
            errors.append(f"VAL-01: Missing required top-level fields: {missing}")
        if extra:
            errors.append(f"VAL-01: Unexpected top-level fields: {extra}")

        if importlib.util.find_spec("jsonschema") is not None:
            import jsonschema  # type: ignore

            try:
                jsonschema.validate(instance=dict(raw), schema=schema_raw)
            except jsonschema.ValidationError as exc:
                errors.append(f"VAL-01 (jsonschema): {exc.message}")
        return errors

    def parse(self, raw: Mapping[str, Any]) -> Tuple[Catalog | None, List[str]]:
        errors: List[str] = []
        try:
            meta_raw = raw["metadata"]
            owner_raw = meta_raw["owner"]
            owner = OwnerMetadata(
                name=str(owner_raw["name"]),
                github_handle=str(owner_raw["githubHandle"]),
                role_title=str(owner_raw["roleTitle"]),
                portfolio_url=str(owner_raw["portfolioUrl"]),
                github_profile_url=str(owner_raw["githubProfileUrl"]),
                discussions_url=str(owner_raw["discussionsUrl"]),
                catalog_url=str(owner_raw["catalogUrl"]),
            )
            metadata = CatalogMetadata(
                schema_version=str(meta_raw["schemaVersion"]),
                catalog_revision=str(meta_raw["catalogRevision"]),
                last_verified_at=str(meta_raw["lastVerifiedAt"]),
                owner=owner,
            )
            standards = tuple(
                EngineeringStandard(
                    standard_id=str(item["standardId"]),
                    order=int(item["order"]),
                    name=str(item["name"]),
                    implementation_standard=str(item["implementationStandard"]),
                )
                for item in raw["engineeringStandards"]
            )
            domains = tuple(
                DomainEntry(
                    domain_id=str(item["domainId"]),
                    domain_number=int(item["domainNumber"]),
                    title=str(item["title"]),
                    short_title=str(item["shortTitle"]),
                    target_audience=str(item["targetAudience"]),
                    executive_summary=str(item["executiveSummary"]),
                    domain_boundary_note=item.get("domainBoundaryNote"),
                )
                for item in raw["domains"]
            )
            suites = tuple(
                SuiteEntry(
                    suite_id=str(item["suiteId"]),
                    suite_number=int(item["suiteNumber"]),
                    domain_id=str(item["domainId"]),
                    render_order_in_domain=int(item["renderOrderInDomain"]),
                    title=str(item["title"]),
                    short_title=str(item["shortTitle"]),
                    target_audience=str(item["targetAudience"]),
                    sponsor_type=str(item["sponsorType"]),
                    sponsor_label=str(item["sponsorLabel"]),
                    sponsor_boundary_note=item.get("sponsorBoundaryNote"),
                    maturity_tier=str(item["maturityTier"]),
                    value_proposition=str(item["valueProposition"]),
                    business_problem=str(item["businessProblem"]),
                    enterprise_controls=tuple(
                        EnterpriseControl(
                            title=str(c["title"]),
                            description=str(c["description"]),
                        )
                        for c in item["enterpriseControls"]
                    ),
                    tech_stack=tuple(str(t) for t in item["techStack"]),
                    tags=tuple(str(t) for t in item["tags"]),
                    standard_ids=tuple(str(s) for s in item["standardIds"]),
                )
                for item in raw["suites"]
            )
            repositories = tuple(
                RepositoryEntry(
                    repo_id=str(item["repoId"]),
                    entry_kind=str(item["entryKind"]),
                    github_repo_name=item.get("githubRepoName"),
                    display_name=str(item["displayName"]),
                    short_label=item.get("shortLabel"),
                    canonical_suite_id=str(item["canonicalSuiteId"]),
                    referenced_by_suites=tuple(str(s) for s in item["referencedBySuites"]),
                    visibility=str(item["visibility"]),
                    maturity_tier=str(item["maturityTier"]),
                    role_in_suite=str(item["roleInSuite"]),
                    summary=str(item["summary"]),
                    verification_note=item.get("verificationNote"),
                    display_order=int(item["displayOrder"]),
                )
                for item in raw["repositories"]
            )
            briefs = tuple(
                BriefEntry(
                    asset_id=str(item["assetId"]),
                    slug=str(item["slug"]),
                    suite_id=str(item["suiteId"]),
                    title=str(item["title"]),
                    subtitle=str(item["subtitle"]),
                    context_summary=str(item["contextSummary"]),
                    architecture_highlights=tuple(str(h) for h in item["architectureHighlights"]),
                    guardrails_and_compliance=tuple(str(g) for g in item["guardrailsAndCompliance"]),
                    diagram_mermaid=str(item["diagramMermaid"]),
                )
                for item in raw["briefs"]
            )
            proof_links = tuple(
                ProofLinkEntry(
                    proof_id=str(item["proofId"]),
                    suite_id=str(item["suiteId"]),
                    evidence_type=str(item["evidenceType"]),
                    target_kind=str(item["targetKind"]),
                    repo_id=item.get("repoId"),
                    path_or_fragment=item.get("pathOrFragment"),
                    asset_id=item.get("assetId"),
                    title=str(item["title"]),
                    summary=str(item["summary"]),
                    display_order=int(item["displayOrder"]),
                )
                for item in raw["proofLinks"]
            )
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"VAL-01: Malformed catalog structure: {exc}")
            return None, errors

        return (
            Catalog(
                metadata=metadata,
                engineering_standards=standards,
                domains=domains,
                suites=suites,
                repositories=repositories,
                briefs=briefs,
                proof_links=proof_links,
            ),
            errors,
        )


class InvariantValidator:
    """Enforces VAL-01..VAL-09 architectural and data integrity invariants."""

    def validate(self, catalog: Catalog, strict_verification: bool = False) -> List[str]:
        errors: List[str] = []

        # VAL-01 & VAL-02: Cardinality and taxonomy continuity
        if len(catalog.domains) != 4:
            errors.append(f"VAL-01: Expected 4 domains, got {len(catalog.domains)}")
        if len(catalog.suites) != 10:
            errors.append(f"VAL-01: Expected 10 suites, got {len(catalog.suites)}")
        if len(catalog.engineering_standards) != 4:
            errors.append(
                f"VAL-01: Expected 4 engineeringStandards, got {len(catalog.engineering_standards)}"
            )

        domain_ids = [d.domain_id for d in catalog.domains]
        domain_nums = [d.domain_number for d in catalog.domains]
        if set(domain_ids) != set(ALLOWED_DOMAINS):
            errors.append(f"VAL-02: Domain IDs mismatch allowed set: {domain_ids}")
        if sorted(domain_nums) != [1, 2, 3, 4]:
            errors.append(f"VAL-02: Domain numbers must be 1..4, got {domain_nums}")

        std_ids = {s.standard_id for s in catalog.engineering_standards}
        if len(std_ids) != len(catalog.engineering_standards):
            errors.append("VAL-02: Duplicate standardId in engineeringStandards")
        if sorted(s.order for s in catalog.engineering_standards) != [1, 2, 3, 4]:
            errors.append("VAL-02: engineeringStandards order must be 1..4")
        for s in catalog.engineering_standards:
            if s.name not in ALLOWED_STANDARD_NAMES:
                errors.append(f"VAL-02: Unknown standard name {s.name!r}")

        suite_ids: List[str] = []
        suite_nums: List[int] = []
        domain_suite_map: Dict[str, Set[int]] = {d: set() for d in ALLOWED_DOMAINS}
        domain_orders: Dict[str, List[int]] = {d: [] for d in ALLOWED_DOMAINS}

        for suite in catalog.suites:
            if not SUITE_ID_RE.match(suite.suite_id):
                errors.append(f"VAL-01: Invalid suiteId pattern {suite.suite_id!r}")
            suite_ids.append(suite.suite_id)
            suite_nums.append(suite.suite_number)
            if suite.domain_id not in domain_suite_map:
                errors.append(f"VAL-03: Suite {suite.suite_id} references unknown domain {suite.domain_id}")
            else:
                domain_suite_map[suite.domain_id].add(suite.suite_number)
                domain_orders[suite.domain_id].append(suite.render_order_in_domain)
            if suite.maturity_tier not in ALLOWED_MATURITY_TIERS:
                errors.append(f"VAL-08: Invalid maturityTier on {suite.suite_id}: {suite.maturity_tier}")
            if suite.sponsor_type not in ALLOWED_SPONSOR_TYPES:
                errors.append(f"VAL-01: Invalid sponsorType on {suite.suite_id}: {suite.sponsor_type}")
            if not suite.standard_ids:
                errors.append(f"VAL-08: Suite {suite.suite_id} must reference at least one standard")
            for sid in suite.standard_ids:
                if sid not in std_ids:
                    errors.append(f"VAL-03: Suite {suite.suite_id} references unknown standardId {sid!r}")

        if len(set(suite_ids)) != len(suite_ids):
            errors.append("VAL-02: Duplicate suiteId detected")
        if sorted(suite_nums) != list(range(1, 11)):
            errors.append(f"VAL-02: Suite numbers must be 1..10 without duplicates, got {suite_nums}")
        for dom_id, expected_nums in EXPECTED_DOMAIN_SUITES.items():
            if domain_suite_map.get(dom_id) != expected_nums:
                errors.append(
                    f"VAL-02: Domain {dom_id} expected suites {sorted(expected_nums)}, got {sorted(domain_suite_map.get(dom_id, set()))}"
                )
            orders = sorted(domain_orders.get(dom_id, []))
            if orders != list(range(1, len(expected_nums) + 1)):
                errors.append(f"VAL-02: Domain {dom_id} renderOrderInDomain not contiguous 1..k: {orders}")

        suite_by_id = {s.suite_id: s for s in catalog.suites}

        # VAL-03 & VAL-04: Repository uniqueness, single canonical owner, visibility constraints
        seen_repo_ids: Set[str] = set()
        seen_github_names: Set[str] = set()
        canonical_counts: Dict[str, int] = {s.suite_id: 0 for s in catalog.suites}

        for repo in catalog.repositories:
            if not SLUG_RE.match(repo.repo_id):
                errors.append(f"VAL-01: Invalid repoId {repo.repo_id!r}")
            if repo.repo_id in seen_repo_ids:
                errors.append(f"VAL-04: Duplicate repoId {repo.repo_id!r}")
            seen_repo_ids.add(repo.repo_id)

            if repo.entry_kind not in ALLOWED_ENTRY_KINDS:
                errors.append(f"VAL-01: Invalid entryKind {repo.entry_kind!r} on {repo.repo_id}")
            if repo.visibility not in ALLOWED_VISIBILITIES:
                errors.append(f"VAL-01: Invalid visibility {repo.visibility!r} on {repo.repo_id}")
            if repo.maturity_tier not in ALLOWED_MATURITY_TIERS:
                errors.append(f"VAL-08: Invalid maturityTier on repo {repo.repo_id}")

            if repo.visibility in ("PUBLIC", "PRIVATE"):
                if repo.entry_kind != "GITHUB_REPO" or not repo.github_repo_name:
                    errors.append(f"VAL-04: {repo.repo_id} ({repo.visibility}) must have GITHUB_REPO + githubRepoName")
            if repo.visibility == "IN_DESIGN" and repo.github_repo_name is not None:
                errors.append(f"VAL-04: IN_DESIGN item {repo.repo_id} must have githubRepoName=null")
            if strict_verification and repo.visibility == "PENDING_REPO_VERIFICATION":
                errors.append(f"VAL-05: Strict verification rejects PENDING_REPO_VERIFICATION on {repo.repo_id}")

            if repo.github_repo_name is not None:
                if not GITHUB_REPO_NAME_RE.match(repo.github_repo_name):
                    errors.append(f"VAL-01: Invalid githubRepoName {repo.github_repo_name!r}")
                lowered = repo.github_repo_name.lower()
                if lowered in seen_github_names:
                    errors.append(f"VAL-04: Duplicate githubRepoName across catalog: {repo.github_repo_name!r}")
                seen_github_names.add(lowered)

            if repo.canonical_suite_id not in suite_by_id:
                errors.append(f"VAL-03: Repo {repo.repo_id} unknown canonicalSuiteId {repo.canonical_suite_id!r}")
            else:
                canonical_counts[repo.canonical_suite_id] += 1

            if repo.canonical_suite_id in repo.referenced_by_suites:
                errors.append(f"VAL-04: Repo {repo.repo_id} has canonicalSuiteId inside referencedBySuites")
            for ref_suite in repo.referenced_by_suites:
                if ref_suite not in suite_by_id:
                    errors.append(f"VAL-03: Repo {repo.repo_id} references unknown suite {ref_suite!r}")
                if repo.visibility != "PUBLIC":
                    errors.append(f"VAL-04: Non-PUBLIC repo {repo.repo_id} cannot be cross-referenced by {ref_suite}")

        for sid, count in canonical_counts.items():
            if count < 1:
                errors.append(f"VAL-04: Suite {sid} must own at least 1 canonical repository entry")

        # VAL-05 & VAL-06: Suite 7 vs Suite 8 sponsor boundary and verified repo prefixes
        s7 = suite_by_id.get("suite-07-consent-ev-pnc")
        s8 = suite_by_id.get("suite-08-wallet-pnc-ev")
        s9 = suite_by_id.get("suite-09-ev-telemetry-can")
        if s7 and s8 and s9:
            if s7.sponsor_type != "CENTRALIZED_REGULATOR" or s8.sponsor_type != "ECOSYSTEM_STAKEHOLDERS_FINTECH_CPO":
                errors.append("VAL-06: Suite 7 must be CENTRALIZED_REGULATOR and Suite 8 ECOSYSTEM_STAKEHOLDERS_FINTECH_CPO")
            if not s7.sponsor_boundary_note or not s8.sponsor_boundary_note:
                errors.append("VAL-06: Suite 7 and Suite 8 require explicit sponsorBoundaryNote")
        for repo in catalog.repositories:
            if repo.github_repo_name:
                if repo.github_repo_name.startswith("EV_PnC_Consent_") and repo.canonical_suite_id != "suite-07-consent-ev-pnc":
                    errors.append(f"VAL-06: {repo.github_repo_name} must belong canonically to suite-07-consent-ev-pnc")
                if repo.github_repo_name.startswith("EV_PNC_") and repo.canonical_suite_id != "suite-08-wallet-pnc-ev":
                    errors.append(f"VAL-06: {repo.github_repo_name} must belong canonically to suite-08-wallet-pnc-ev")
            if repo.canonical_suite_id == "suite-07-consent-ev-pnc" and "suite-08-wallet-pnc-ev" in repo.referenced_by_suites:
                errors.append("VAL-06: Suite 7 and Suite 8 must remain isolated without direct cross-reference")
            if repo.canonical_suite_id == "suite-08-wallet-pnc-ev" and "suite-07-consent-ev-pnc" in repo.referenced_by_suites:
                errors.append("VAL-06: Suite 8 and Suite 7 must remain isolated without direct cross-reference")

        # VAL-07: Briefs & proofLinks integrity
        repo_by_id = {r.repo_id: r for r in catalog.repositories}
        brief_by_id: Dict[str, BriefEntry] = {}
        seen_brief_slugs: Set[str] = set()
        for brief in catalog.briefs:
            if brief.asset_id in brief_by_id:
                errors.append(f"VAL-02: Duplicate brief assetId {brief.asset_id!r}")
            if brief.slug in seen_brief_slugs:
                errors.append(f"VAL-02: Duplicate brief slug {brief.slug!r}")
            seen_brief_slugs.add(brief.slug)
            if brief.suite_id not in suite_by_id:
                errors.append(f"VAL-03: Brief {brief.asset_id} references unknown suite {brief.suite_id!r}")
            brief_by_id[brief.asset_id] = brief

        proof_counts: Dict[str, int] = {s.suite_id: 0 for s in catalog.suites}
        seen_proof_ids: Set[str] = set()
        for proof in catalog.proof_links:
            if proof.proof_id in seen_proof_ids:
                errors.append(f"VAL-02: Duplicate proofId {proof.proof_id!r}")
            seen_proof_ids.add(proof.proof_id)
            if proof.evidence_type not in ALLOWED_EVIDENCE_TYPES:
                errors.append(f"VAL-07: Invalid evidenceType {proof.evidence_type!r}")
            if proof.suite_id not in suite_by_id:
                errors.append(f"VAL-03: Proof {proof.proof_id} references unknown suite {proof.suite_id!r}")
            else:
                proof_counts[proof.suite_id] += 1

            if proof.target_kind == "PUBLIC_GITHUB_REPO":
                if not proof.repo_id or proof.repo_id not in repo_by_id:
                    errors.append(f"VAL-07: Proof {proof.proof_id} references unknown repoId {proof.repo_id!r}")
                else:
                    target_repo = repo_by_id[proof.repo_id]
                    if target_repo.visibility != "PUBLIC":
                        errors.append(f"VAL-04/VAL-07: Proof {proof.proof_id} cannot link to non-PUBLIC repo {target_repo.repo_id}")
                    if proof.suite_id != target_repo.canonical_suite_id and proof.suite_id not in target_repo.referenced_by_suites:
                        errors.append(f"VAL-07: Proof {proof.proof_id} repo {target_repo.repo_id} not associated with {proof.suite_id}")
            elif proof.target_kind == "PORTFOLIO_ASSET":
                if not proof.asset_id or proof.asset_id not in brief_by_id:
                    errors.append(f"VAL-07: Proof {proof.proof_id} references unknown brief assetId {proof.asset_id!r}")
            else:
                errors.append(f"VAL-07: Invalid targetKind {proof.target_kind!r}")

        for sid, count in proof_counts.items():
            if count < 1:
                errors.append(f"VAL-07: Suite {sid} must have at least 1 proofLink entry")

        return errors


class HygieneScanner:
    """Single-source hygiene policy enforcement across SSOT inputs and rendered outputs."""

    def __init__(self) -> None:
        # Patterns assembled dynamically so the scanner module does not trigger false positives on itself.
        self._credential_re = re.compile(
            r"(AIza[0-9A-Za-z_-]{20,}|ghp_[0-9A-Za-z]{20,}|gho_[0-9A-Za-z]{20,}|"
            r"sk-[0-9A-Za-z]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)"
        )
        excluded_terms = (
            "JFor" + "ce",
            "Üm" + "it",
            "Ay" + "şe",
            "steer" + "f[0o]cus",
        )
        self._excluded_re = re.compile(r"(" + "|".join(excluded_terms) + r")", re.IGNORECASE)
        self._tenure_re = re.compile(r"(16\+?\s*[Yy]ears?|16-year)", re.IGNORECASE)
        self._unsafe_dom_re = re.compile(
            r"(innerHTML|outerHTML|insertAdjacentHTML|document\.write\s*\(|\beval\s*\()"
        )

    def scan_artifacts(
        self,
        catalog: Catalog,
        files_text: Mapping[str, str],
        strict_hygiene: bool = False,
    ) -> List[HygieneFinding]:
        findings: List[HygieneFinding] = []
        non_public_names = {
            r.github_repo_name.lower(): r.github_repo_name
            for r in catalog.repositories
            if r.github_repo_name and r.visibility != "PUBLIC"
        }
        owner_prefix = f"https://github.com/{catalog.metadata.owner.github_handle.lower()}/"
        github_url_re = re.compile(r"https://github\.com/([A-Za-z0-9_-]+)/([A-Za-z0-9_.-]+)")

        for location, content in files_text.items():
            for line_no, line in enumerate(content.splitlines(), 1):
                if self._credential_re.search(line):
                    findings.append(
                        HygieneFinding("CRITICAL", "CREDENTIAL_SIGNATURE", f"{location}:{line_no}", "Credential pattern detected")
                    )
                if self._excluded_re.search(line):
                    findings.append(
                        HygieneFinding("CRITICAL", "EXCLUDED_METADATA", f"{location}:{line_no}", "Excluded metadata pattern detected")
                    )
                if self._tenure_re.search(line):
                    findings.append(
                        HygieneFinding("CRITICAL", "PROHIBITED_TENURE_CLAIMS", f"{location}:{line_no}", "Excluded tenure string detected")
                    )
                if location.endswith(".html") and self._unsafe_dom_re.search(line):
                    findings.append(
                        HygieneFinding("CRITICAL", "UNSAFE_DOM_PATTERN", f"{location}:{line_no}", "Unsafe DOM manipulation API detected")
                    )
                for m in github_url_re.finditer(line):
                    repo_name = m.group(2).rstrip(".,);")
                    if m.group(0).lower().startswith(owner_prefix) and repo_name.lower() in non_public_names:
                        findings.append(
                            HygieneFinding(
                                "CRITICAL",
                                "NON_PUBLIC_URL_LEAK",
                                f"{location}:{line_no}",
                                f"Clickable URL to non-PUBLIC repo: {repo_name}",
                            )
                        )
                if strict_hygiene and "http://" in line and "localhost" not in line and "127.0.0.1" not in line and "xmlns" not in line:
                    findings.append(
                        HygieneFinding("WARNING", "PLAIN_HTTP_LINK", f"{location}:{line_no}", "Plain HTTP link detected outside localhost")
                    )
        return findings
