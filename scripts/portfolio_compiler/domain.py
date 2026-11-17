"""Domain models, canonical enums, and gateway protocols for the COPUR SSOT portfolio."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol, Tuple

ALLOWED_DOMAINS = (
    "D1_AGENTIC_AI",
    "D2_OPEN_FINANCE_CORE",
    "D3_EV_MOBILITY",
    "D4_SERVERLESS_INTELLIGENCE",
)

ALLOWED_MATURITY_TIERS = (
    "RUNNABLE_K8S_CLI_DEMO",
    "PUBLIC_REFERENCE_BASELINE",
    "CONTRACT_FIRST_ECOSYSTEM",
    "GOVERNED_PRIVATE_ENTERPRISE_BASELINE",
)

MATURITY_LABELS: Mapping[str, str] = {
    "RUNNABLE_K8S_CLI_DEMO": "Runnable K8s / CLI Demo",
    "PUBLIC_REFERENCE_BASELINE": "Public Reference Baseline",
    "CONTRACT_FIRST_ECOSYSTEM": "Contract-First Ecosystem",
    "GOVERNED_PRIVATE_ENTERPRISE_BASELINE": "Governed Private Enterprise Baseline",
}

ALLOWED_VISIBILITIES = (
    "PUBLIC",
    "PRIVATE",
    "IN_DESIGN",
    "PENDING_REPO_VERIFICATION",
)

ALLOWED_ENTRY_KINDS = ("GITHUB_REPO", "SUB_PRODUCT", "CONCEPT_PRODUCT")

ALLOWED_EVIDENCE_TYPES = (
    "QUICKSTART_DEEP_LINK",
    "CONTRACT_SPEC",
    "TESTKIT_OR_SIMULATOR",
    "C4_ARCHITECTURE_BRIEF",
    "ADR_OR_BENCHMARK",
)

EVIDENCE_LABELS: Mapping[str, str] = {
    "QUICKSTART_DEEP_LINK": "Quickstart",
    "CONTRACT_SPEC": "Contracts & Spec",
    "TESTKIT_OR_SIMULATOR": "Testkit / Simulator",
    "C4_ARCHITECTURE_BRIEF": "C4 Architecture Brief",
    "ADR_OR_BENCHMARK": "ADR / Benchmark",
}

ALLOWED_SPONSOR_TYPES = (
    "ENTERPRISE_PLATFORM_GOVERNANCE",
    "OPEN_FINANCE_CORE_BANKING",
    "CENTRALIZED_REGULATOR",
    "ECOSYSTEM_STAKEHOLDERS_FINTECH_CPO",
    "AUTOMOTIVE_RD_DRIVER_EXPERIENCE",
    "SERVERLESS_SAAS_RD",
)

ALLOWED_STANDARD_NAMES = (
    "Deterministic Sandwich",
    "Contract-First Governance",
    "Zero-Trust & Residency",
    "Air-Gapped / On-Prem AI",
)


@dataclass(frozen=True, slots=True)
class OwnerMetadata:
    name: str
    github_handle: str
    role_title: str
    portfolio_url: str
    github_profile_url: str
    discussions_url: str
    catalog_url: str


@dataclass(frozen=True, slots=True)
class CatalogMetadata:
    schema_version: str
    catalog_revision: str
    last_verified_at: str
    owner: OwnerMetadata


@dataclass(frozen=True, slots=True)
class EngineeringStandard:
    standard_id: str
    order: int
    name: str
    implementation_standard: str


@dataclass(frozen=True, slots=True)
class DomainEntry:
    domain_id: str
    domain_number: int
    title: str
    short_title: str
    target_audience: str
    executive_summary: str
    domain_boundary_note: str | None


@dataclass(frozen=True, slots=True)
class EnterpriseControl:
    title: str
    description: str


@dataclass(frozen=True, slots=True)
class SuiteEntry:
    suite_id: str
    suite_number: int
    domain_id: str
    render_order_in_domain: int
    title: str
    short_title: str
    target_audience: str
    sponsor_type: str
    sponsor_label: str
    sponsor_boundary_note: str | None
    maturity_tier: str
    value_proposition: str
    business_problem: str
    enterprise_controls: Tuple[EnterpriseControl, ...]
    tech_stack: Tuple[str, ...]
    tags: Tuple[str, ...]
    standard_ids: Tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RepositoryEntry:
    repo_id: str
    entry_kind: str
    github_repo_name: str | None
    display_name: str
    short_label: str | None
    canonical_suite_id: str
    referenced_by_suites: Tuple[str, ...]
    visibility: str
    maturity_tier: str
    role_in_suite: str
    summary: str
    verification_note: str | None
    display_order: int


@dataclass(frozen=True, slots=True)
class BriefEntry:
    asset_id: str
    slug: str
    suite_id: str
    title: str
    subtitle: str
    context_summary: str
    architecture_highlights: Tuple[str, ...]
    guardrails_and_compliance: Tuple[str, ...]
    diagram_mermaid: str


@dataclass(frozen=True, slots=True)
class ProofLinkEntry:
    proof_id: str
    suite_id: str
    evidence_type: str
    target_kind: str
    repo_id: str | None
    path_or_fragment: str | None
    asset_id: str | None
    title: str
    summary: str
    display_order: int


@dataclass(frozen=True, slots=True)
class Catalog:
    metadata: CatalogMetadata
    engineering_standards: Tuple[EngineeringStandard, ...]
    domains: Tuple[DomainEntry, ...]
    suites: Tuple[SuiteEntry, ...]
    repositories: Tuple[RepositoryEntry, ...]
    briefs: Tuple[BriefEntry, ...]
    proof_links: Tuple[ProofLinkEntry, ...]


@dataclass(frozen=True, slots=True)
class HygieneFinding:
    severity: str  # CRITICAL | WARNING
    rule_id: str
    location: str
    detail: str


@dataclass(frozen=True, slots=True)
class VerificationResult:
    ok: bool
    warnings: Tuple[str, ...]
    errors: Tuple[str, ...]
    checked_repos: int


class VisibilityGateway(Protocol):
    """Port abstracting GitHub repository visibility retrieval."""

    def fetch_visibilities(self, owner: str) -> Tuple[Mapping[str, str], bool]:
        """Return ({repo_name: 'PUBLIC'|'PRIVATE'}, includes_private_scope)."""
