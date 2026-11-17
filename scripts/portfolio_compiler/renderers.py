"""Deterministic projection renderers (README, PROJECTS, HTML showcase, and dual-artifact briefs)."""

from __future__ import annotations

import html
from dataclasses import dataclass
from typing import Dict, List, Mapping, Tuple

from .domain import (
    BriefEntry,
    Catalog,
    DomainEntry,
    EVIDENCE_LABELS,
    MATURITY_LABELS,
    ProofLinkEntry,
    RepositoryEntry,
    SuiteEntry,
)


@dataclass(frozen=True, slots=True)
class ResolvedProof:
    evidence_label: str
    title: str
    summary: str
    href: str
    is_external: bool


@dataclass(frozen=True, slots=True)
class SuiteBuckets:
    suite: SuiteEntry
    domain: DomainEntry
    maturity_label: str
    canonical_public: Tuple[RepositoryEntry, ...]
    cross_ref_public: Tuple[Tuple[RepositoryEntry, int], ...]
    canonical_private: Tuple[RepositoryEntry, ...]
    in_design_pending: Tuple[RepositoryEntry, ...]
    proofs: Tuple[ResolvedProof, ...]


class SurfaceLinkResolver:
    """Resolves GitHub repo URLs and PORTFOLIO_ASSET links cleanly per target surface."""

    def __init__(self, catalog: Catalog) -> None:
        self._handle = catalog.metadata.owner.github_handle
        self._repo_by_id = {r.repo_id: r for r in catalog.repositories}
        self._brief_by_id = {b.asset_id: b for b in catalog.briefs}

    def repo_url(self, repo: RepositoryEntry) -> str:
        if repo.visibility != "PUBLIC" or not repo.github_repo_name:
            raise ValueError(f"Cannot generate public URL for non-PUBLIC repo {repo.repo_id}")
        return f"https://github.com/{self._handle}/{repo.github_repo_name}"

    def resolve_proof(self, proof: ProofLinkEntry, surface: str) -> ResolvedProof:
        ev_label = EVIDENCE_LABELS[proof.evidence_type]
        if proof.target_kind == "PUBLIC_GITHUB_REPO":
            repo = self._repo_by_id[proof.repo_id or ""]
            frag = proof.path_or_fragment or ""
            return ResolvedProof(
                evidence_label=ev_label,
                title=proof.title,
                summary=proof.summary,
                href=f"{self.repo_url(repo)}{frag}",
                is_external=True,
            )
        brief = self._brief_by_id[proof.asset_id or ""]
        if surface == "HTML_SHOWCASE":
            href = f"briefs/{brief.slug}.html"
        elif surface == "MARKDOWN":
            href = f"./briefs/{brief.slug}.md"
        else:
            raise ValueError(f"Unsupported surface {surface!r}")
        return ResolvedProof(
            evidence_label=ev_label,
            title=proof.title,
            summary=proof.summary,
            href=href,
            is_external=False,
        )


class ProjectionViewModelBuilder:
    """Builds 4-bucket deterministic view models per suite."""

    def build_suites(self, catalog: Catalog, surface: str) -> Tuple[SuiteBuckets, ...]:
        resolver = SurfaceLinkResolver(catalog)
        domain_by_id = {d.domain_id: d for d in catalog.domains}
        suite_num_by_id = {s.suite_id: s.suite_number for s in catalog.suites}
        ordered_suites = sorted(catalog.suites, key=lambda s: s.suite_number)

        result: List[SuiteBuckets] = []
        for suite in ordered_suites:
            canon_pub = sorted(
                (r for r in catalog.repositories if r.canonical_suite_id == suite.suite_id and r.visibility == "PUBLIC"),
                key=lambda r: (r.display_order, r.repo_id),
            )
            xref_pub = sorted(
                (
                    (r, suite_num_by_id[r.canonical_suite_id])
                    for r in catalog.repositories
                    if suite.suite_id in r.referenced_by_suites and r.visibility == "PUBLIC"
                ),
                key=lambda item: item[0].repo_id,
            )
            canon_priv = sorted(
                (r for r in catalog.repositories if r.canonical_suite_id == suite.suite_id and r.visibility == "PRIVATE"),
                key=lambda r: (r.display_order, r.repo_id),
            )
            design_pend = sorted(
                (
                    r
                    for r in catalog.repositories
                    if r.canonical_suite_id == suite.suite_id
                    and r.visibility in ("IN_DESIGN", "PENDING_REPO_VERIFICATION")
                ),
                key=lambda r: (r.display_order, r.repo_id),
            )
            proofs = tuple(
                resolver.resolve_proof(p, surface)
                for p in sorted(
                    (pl for pl in catalog.proof_links if pl.suite_id == suite.suite_id),
                    key=lambda pl: (pl.display_order, pl.proof_id),
                )
            )
            result.append(
                SuiteBuckets(
                    suite=suite,
                    domain=domain_by_id[suite.domain_id],
                    maturity_label=MATURITY_LABELS[suite.maturity_tier],
                    canonical_public=tuple(canon_pub),
                    cross_ref_public=tuple(xref_pub),
                    canonical_private=tuple(canon_priv),
                    in_design_pending=tuple(design_pend),
                    proofs=proofs,
                )
            )
        return tuple(result)


def _public_md_links(items: Tuple[RepositoryEntry, ...], resolver: SurfaceLinkResolver) -> str:
    return " · ".join(f"[`{r.display_name}`]({resolver.repo_url(r)})" for r in items)


def render_readme(catalog: Catalog) -> str:
    vm_builder = ProjectionViewModelBuilder()
    resolver = SurfaceLinkResolver(catalog)
    suite_vms = vm_builder.build_suites(catalog, "MARKDOWN")
    by_domain: Dict[str, List[SuiteBuckets]] = {d.domain_id: [] for d in catalog.domains}
    for vm in suite_vms:
        by_domain[vm.domain.domain_id].append(vm)

    owner = catalog.metadata.owner
    lines: List[str] = [
        f"# {owner.name} (`@{owner.github_handle}`)",
        "",
        f"**{owner.role_title}**",
        "",
        (
            "Building **enterprise-grade software products and platforms** across "
            "**Agentic AI-Driven Enterprise Architecture**, **Agentic Open Finance (BaaS)**, "
            "**Regulated Core Banking & Process Orchestration**, **EV Roaming & Mobility**, and "
            "**Multi-Tenant Serverless Intelligence**. Every suite is governed by a Single Source of Truth (SSOT), "
            "deterministic harnesses, contract-first interfaces, and zero-trust security boundaries."
        ),
        "",
        (
            f"- **Interactive Showcase:** [{owner.portfolio_url}]({owner.portfolio_url})\n"
            f"- **Full Product & Architecture Catalog:** [PROJECTS.md](./PROJECTS.md)\n"
            f"- **TOGAF ADM BDAT Specification & Backlog:** [TOGAF_ADM_PLAN.md](./TOGAF_ADM_PLAN.md) · [BACKLOG.md](./BACKLOG.md)\n"
            f"- **Discussions & Contact:** [GitHub Discussions]({owner.discussions_url})"
        ),
        "",
        "---",
        "",
        "## Enterprise Product Suites (4 Executive Domains · 10 Canonical Suites)",
        "",
    ]

    for dom in sorted(catalog.domains, key=lambda d: d.domain_number):
        lines.append(f"### {dom.domain_number}. {dom.title}")
        lines.append(f"*Target: {dom.targetAudience if hasattr(dom, 'targetAudience') else dom.target_audience}*")
        if dom.domain_boundary_note:
            lines.append(f"> {dom.domain_boundary_note}")
        lines.append("")
        dom_suites = sorted(by_domain[dom.domain_id], key=lambda item: item.suite.render_order_in_domain)
        for svm in dom_suites:
            s = svm.suite
            lines.append(f"#### Suite {s.suite_number}: {s.title}")
            lines.append(f"- **Maturity Tier:** `{svm.maturity_label}` · **Sponsor / Scope:** {s.sponsor_label}")
            lines.append(f"- **Product Value:** {s.value_proposition}")
            for ctrl in s.enterprise_controls:
                lines.append(f"- **{ctrl.title}:** {ctrl.description}")
            if svm.canonical_public:
                lines.append(f"- **Public Repositories:** {_public_md_links(svm.canonical_public, resolver)}")
            if svm.cross_ref_public:
                xrefs = " · ".join(
                    f"[`{r.display_name}`]({resolver.repo_url(r)}) *(Cross-Ref: Suite {orig_num})*"
                    for r, orig_num in svm.cross_ref_public
                )
                lines.append(f"- **Cross-Referenced Public Modules:** {xrefs}")
            if svm.canonical_private:
                privs = ", ".join(f"`{r.display_name}`" for r in svm.canonical_private)
                lines.append(f"- **Private Enterprise Repositories (No Public Link):** {privs}")
            if svm.in_design_pending:
                pend = ", ".join(f"`{r.display_name}` ({r.visibility})" for r in svm.in_design_pending)
                lines.append(f"- **In Design / Roadmap:** {pend}")
            proof_str = " · ".join(f"[{p.evidence_label}: {p.title}]({p.href})" for p in svm.proofs)
            lines.append(f"- **Verifiable Proof & Briefs:** {proof_str}")
            lines.append("")
        lines.append("---")
        lines.append("")

    lines.extend(
        [
            "## Enterprise Engineering Standards Across All Products",
            "",
            "| Pillar | Implementation Standard |",
            "|---|---|",
        ]
    )
    for std in sorted(catalog.engineering_standards, key=lambda item: item.order):
        lines.append(f"| **{std.name}** | {std.implementation_standard} |")

    lines.extend(
        [
            "",
            "---",
            "",
            (
                f"Generated deterministically from [`catalog/portfolio-catalog.json`](./catalog/portfolio-catalog.json). "
                f"See [PROJECTS.md](./PROJECTS.md) or visit [{owner.portfolio_url}]({owner.portfolio_url})."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def render_projects_md(catalog: Catalog) -> str:
    vm_builder = ProjectionViewModelBuilder()
    resolver = SurfaceLinkResolver(catalog)
    suite_vms = vm_builder.build_suites(catalog, "MARKDOWN")
    std_by_id = {s.standard_id: s.name for s in catalog.engineering_standards}
    owner = catalog.metadata.owner

    lines: List[str] = [
        "# Enterprise Product & Architecture Catalog",
        "",
        (
            f"Canonical breakdown of `{owner.github_handle}`'s **4 Executive Domains and 10 Product Suites**, "
            f"generated deterministically from [`catalog/portfolio-catalog.json`](./catalog/portfolio-catalog.json)."
        ),
        "",
        "---",
        "",
    ]

    current_domain = None
    for svm in suite_vms:
        s = svm.suite
        if current_domain != svm.domain.domain_id:
            current_domain = svm.domain.domain_id
            lines.append(f"## Domain {svm.domain.domain_number}: {svm.domain.title}")
            lines.append("")
            lines.append(f"> {svm.domain.executive_summary}")
            if svm.domain.domain_boundary_note:
                lines.append(f"> **Boundary Rule:** {svm.domain.domain_boundary_note}")
            lines.append("")

        lines.append(f"### Suite {s.suite_number}: {s.title}")
        lines.append(f"- **Maturity Tier:** `{svm.maturity_label}`")
        lines.append(f"- **Sponsor / Governance Scope:** {s.sponsor_label}")
        if s.sponsor_boundary_note:
            lines.append(f"- **Governance Boundary:** {s.sponsor_boundary_note}")
        lines.append(f"- **Target Market:** {s.target_audience}")
        lines.append(f"- **Business Problem Solved:** {s.business_problem}")
        lines.append(f"- **Value Proposition:** {s.value_proposition}")
        lines.append("- **Enterprise Capabilities:**")
        for ctrl in s.enterprise_controls:
            lines.append(f"  - **{ctrl.title}:** {ctrl.description}")
        lines.append(f"- **Tech Stack:** {', '.join(s.tech_stack)}")
        lines.append(f"- **Applied Standards:** {', '.join(std_by_id[sid] for sid in s.standard_ids)}")
        if svm.canonical_public:
            lines.append(f"- **Canonical Public Repositories:** {_public_md_links(svm.canonical_public, resolver)}")
        if svm.cross_ref_public:
            xrefs = " · ".join(
                f"[`{r.display_name}`]({resolver.repo_url(r)}) *(via Suite {orig_num})*"
                for r, orig_num in svm.cross_ref_public
            )
            lines.append(f"- **Cross-Referenced Public Repositories:** {xrefs}")
        if svm.canonical_private:
            privs = ", ".join(f"`{r.display_name}` *(Private)*" for r in svm.canonical_private)
            lines.append(f"- **Private Enterprise Components:** {privs}")
        if svm.in_design_pending:
            pend = ", ".join(f"`{r.display_name}` *({r.visibility})*" for r in svm.in_design_pending)
            lines.append(f"- **In-Design / Roadmap Concepts:** {pend}")
        lines.append("- **Proof & Verification:**")
        for p in svm.proofs:
            lines.append(f"  - [{p.evidence_label} — {p.title}]({p.href}): {p.summary}")
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            "## Enterprise Engineering Standards Matrix",
            "",
            "| Order | Pillar | Implementation Standard |",
            "|---|---|---|",
        ]
    )
    for std in sorted(catalog.engineering_standards, key=lambda item: item.order):
        lines.append(f"| {std.order} | **{std.name}** | {std.implementation_standard} |")
    lines.append("")
    return "\n".join(lines)


def _esc(val: str) -> str:
    return html.escape(val, quote=True)


def render_html_showcase(catalog: Catalog) -> str:
    vm_builder = ProjectionViewModelBuilder()
    resolver = SurfaceLinkResolver(catalog)
    suite_vms = vm_builder.build_suites(catalog, "HTML_SHOWCASE")
    owner = catalog.metadata.owner

    domain_counts: Dict[str, int] = {d.domain_id: 0 for d in catalog.domains}
    for svm in suite_vms:
        domain_counts[svm.domain.domain_id] += 1

    filter_buttons: List[str] = [
        f'<button type="button" class="filter-btn is-active" data-domain-filter="ALL" aria-pressed="true">All ({len(suite_vms)})</button>'
    ]
    for dom in sorted(catalog.domains, key=lambda d: d.domain_number):
        cnt = domain_counts[dom.domain_id]
        filter_buttons.append(
            f'<button type="button" class="filter-btn" data-domain-filter="{_esc(dom.domain_id)}" aria-pressed="false">'
            f"{_esc(dom.short_title)} ({cnt})</button>"
        )

    maturity_options = ['<option value="ALL">All Maturity Tiers</option>']
    for tier_key, tier_label in MATURITY_LABELS.items():
        maturity_options.append(f'<option value="{_esc(tier_key)}">{_esc(tier_label)}</option>')

    cards_html: List[str] = []
    for svm in suite_vms:
        s = svm.suite
        all_names = [r.display_name for r in svm.canonical_public]
        all_names += [r.display_name for r, _ in svm.cross_ref_public]
        all_names += [r.display_name for r in svm.canonical_private]
        all_names += [r.display_name for r in svm.in_design_pending]
        search_blob = " ".join(
            [
                s.title,
                s.target_audience,
                s.sponsor_label,
                s.value_proposition,
                " ".join(s.tech_stack),
                " ".join(s.tags),
                " ".join(all_names),
            ]
        ).lower()

        sponsor_class = "sponsor-badge"
        if s.sponsor_type == "CENTRALIZED_REGULATOR":
            sponsor_class = "sponsor-badge sponsor-regulator"
        elif s.sponsor_type == "ECOSYSTEM_STAKEHOLDERS_FINTECH_CPO":
            sponsor_class = "sponsor-badge sponsor-stakeholder"

        tags_html = "".join(f'<span class="tag">{_esc(t)}</span>' for t in s.tags)
        proof_html = "".join(
            '<a class="proof-link" href="{href}"{ext}><span class="proof-type">{ev}</span> {title}</a>'.format(
                href=_esc(p.href),
                ext=' target="_blank" rel="noopener noreferrer"' if p.is_external else "",
                ev=_esc(p.evidence_label),
                title=_esc(p.title),
            )
            for p in svm.proofs
        )

        bucket_parts: List[str] = []
        if svm.canonical_public:
            pub_pills = "".join(
                f'<a class="pill pill-public" href="{_esc(resolver.repo_url(r))}" target="_blank" rel="noopener noreferrer">'
                f"{_esc(r.short_label or r.display_name)}</a>"
                for r in svm.canonical_public
            )
            bucket_parts.append(f'<div class="bucket">{pub_pills}</div>')
        if svm.cross_ref_public:
            xref_pills = "".join(
                f'<a class="pill pill-crossref" href="{_esc(resolver.repo_url(r))}" target="_blank" rel="noopener noreferrer">'
                f"{_esc(r.short_label or r.display_name)} <span class=\"xref\">via Suite {orig}</span></a>"
                for r, orig in svm.cross_ref_public
            )
            bucket_parts.append(f'<div class="bucket">{xref_pills}</div>')
        if svm.canonical_private:
            priv_pills = "".join(
                f'<span class="pill pill-private">{_esc(r.display_name)} · Private</span>'
                for r in svm.canonical_private
            )
            bucket_parts.append(f'<div class="bucket">{priv_pills}</div>')
        if svm.in_design_pending:
            ind_pills = "".join(
                f'<span class="pill pill-design">{_esc(r.display_name)} · {_esc(r.visibility)}</span>'
                for r in svm.in_design_pending
            )
            bucket_parts.append(f'<div class="bucket">{ind_pills}</div>')

        boundary_html = (
            f'<p class="boundary-note">{_esc(s.sponsor_boundary_note)}</p>'
            if s.sponsor_boundary_note
            else ""
        )

        cards_html.append(
            f"""      <article class="card"
        data-suite="suite-{s.suite_number:02d}"
        data-domain="{_esc(svm.domain.domain_id)}"
        data-maturity="{_esc(s.maturity_tier)}"
        data-sponsor="{_esc(s.sponsor_type)}"
        data-standards="{_esc(','.join(s.standard_ids))}"
        data-search-index="{_esc(search_blob)}">
        <div>
          <div class="card-meta">
            <span class="domain-chip">D{svm.domain.domain_number} · {_esc(svm.domain.short_title)}</span>
            <span class="maturity-badge">{_esc(svm.maturity_label)}</span>
          </div>
          <h3>{s.suite_number}. {_esc(s.title)}</h3>
          <div class="{sponsor_class}">{_esc(s.sponsor_label)}</div>
          {boundary_html}
          <p class="summary">{_esc(s.value_proposition)}</p>
          <div class="tags">{tags_html}</div>
          <div class="proof-box">
            <div class="proof-heading">Verifiable Proof &amp; Briefs</div>
            <div class="proof-links">{proof_html}</div>
          </div>
        </div>
        <div class="repos">
          {"".join(bucket_parts)}
        </div>
      </article>"""
        )

    applied_map: Dict[str, List[int]] = {std.standard_id: [] for std in catalog.engineering_standards}
    for svm in suite_vms:
        for sid in svm.suite.standard_ids:
            applied_map[sid].append(svm.suite.suite_number)

    standards_rows = "".join(
        "<tr>"
        f"<td><strong>{_esc(std.name)}</strong></td>"
        f"<td>{_esc(std.implementation_standard)}</td>"
        f"<td><code>{', '.join(f'Suite {n}' for n in applied_map[std.standard_id])}</code></td>"
        "</tr>"
        for std in sorted(catalog.engineering_standards, key=lambda item: item.order)
    )

    seo_desc = (
        "Enterprise software architecture and product portfolio across Agentic AI Governance, "
        "Agentic Open Finance (BaaS), Core Banking & Camunda BPO, EV Plug & Charge Roaming, and Serverless SaaS."
    )
    title_full = f"{owner.name} (@{owner.github_handle}) — Enterprise Product Suites"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{_esc(title_full)}</title>
  <link rel="canonical" href="{_esc(owner.portfolio_url)}" />
  <meta name="description" content="{_esc(seo_desc)}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{_esc(owner.portfolio_url)}" />
  <meta property="og:site_name" content="COPUR Enterprise Portfolio" />
  <meta property="og:title" content="{_esc(title_full)}" />
  <meta property="og:description" content="{_esc(seo_desc)}" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{_esc(title_full)}" />
  <meta name="twitter:description" content="{_esc(seo_desc)}" />
  <style>
    :root {{
      --bg: #0b1020;
      --surface: #121933;
      --surface-alt: #0f162d;
      --border: #232d54;
      --text: #e6ebf5;
      --muted: #9aa7c7;
      --accent: #5b8cff;
      --accent-soft: rgba(91, 140, 255, 0.14);
      --green: #3ddc97;
      --green-soft: rgba(61, 220, 151, 0.12);
      --amber: #f5b942;
      --amber-soft: rgba(245, 185, 66, 0.12);
      --cyan: #4cd4e8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.55;
      padding: 2.25rem 1.25rem 3rem;
    }}
    .container {{ max-width: 1200px; margin: 0 auto; }}
    header {{
      border-bottom: 1px solid var(--border);
      padding-bottom: 1.75rem;
      margin-bottom: 1.75rem;
    }}
    .badge {{
      display: inline-block;
      background: var(--accent-soft);
      color: var(--accent);
      border: 1px solid rgba(91, 140, 255, 0.35);
      padding: 0.25rem 0.75rem;
      border-radius: 999px;
      font-size: 0.8rem;
      font-weight: 600;
      margin-bottom: 0.85rem;
    }}
    h1 {{ font-size: 2.15rem; letter-spacing: -0.02em; margin-bottom: 0.5rem; }}
    .subtitle {{ color: var(--muted); font-size: 1.02rem; max-width: 860px; }}
    .links {{ margin-top: 1.15rem; display: flex; gap: 0.85rem; flex-wrap: wrap; }}
    .links a {{
      color: var(--text);
      text-decoration: none;
      background: var(--surface);
      border: 1px solid var(--border);
      padding: 0.45rem 0.9rem;
      border-radius: 8px;
      font-size: 0.88rem;
    }}
    .links a:hover {{ border-color: var(--accent); }}
    .controls {{
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1rem 1.1rem;
      margin-bottom: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
    }}
    .filter-bar {{ display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; }}
    .filter-btn {{
      background: var(--surface);
      color: var(--muted);
      border: 1px solid var(--border);
      padding: 0.4rem 0.8rem;
      border-radius: 8px;
      font-size: 0.84rem;
      cursor: pointer;
    }}
    .filter-btn.is-active {{
      background: var(--accent-soft);
      color: var(--text);
      border-color: var(--accent);
      font-weight: 600;
    }}
    .secondary-controls {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      align-items: center;
      justify-content: space-between;
    }}
    .inputs {{ display: flex; flex-wrap: wrap; gap: 0.65rem; flex: 1; }}
    select, input[type="search"] {{
      background: var(--surface);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.42rem 0.75rem;
      font-size: 0.86rem;
    }}
    input[type="search"] {{ min-width: 240px; flex: 1; max-width: 360px; }}
    #filter-status {{ color: var(--muted); font-size: 0.85rem; }}
    h2 {{ font-size: 1.4rem; margin: 1.5rem 0 1rem; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 1.25rem;
    }}
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.3rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 0.85rem;
    }}
    .card.is-hidden {{ display: none; }}
    .card-meta {{
      display: flex;
      justify-content: space-between;
      gap: 0.5rem;
      flex-wrap: wrap;
      margin-bottom: 0.55rem;
    }}
    .domain-chip {{
      font-size: 0.72rem;
      color: var(--muted);
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border);
      padding: 0.15rem 0.5rem;
      border-radius: 6px;
    }}
    .maturity-badge {{
      font-size: 0.72rem;
      color: var(--accent);
      background: var(--accent-soft);
      border: 1px solid rgba(91, 140, 255, 0.35);
      padding: 0.15rem 0.55rem;
      border-radius: 999px;
      font-weight: 600;
    }}
    .card h3 {{ font-size: 1.07rem; margin-bottom: 0.35rem; color: #fff; }}
    .sponsor-badge {{ font-size: 0.8rem; color: var(--green); margin-bottom: 0.5rem; font-weight: 600; }}
    .sponsor-regulator {{ color: var(--cyan); }}
    .sponsor-stakeholder {{ color: var(--amber); }}
    .boundary-note {{
      font-size: 0.78rem;
      color: var(--muted);
      border-left: 2px solid var(--border);
      padding-left: 0.6rem;
      margin-bottom: 0.65rem;
    }}
    .summary {{ color: var(--muted); font-size: 0.9rem; margin-bottom: 0.8rem; }}
    .tags {{ display: flex; flex-wrap: wrap; gap: 0.38rem; margin-bottom: 0.8rem; }}
    .tag {{
      font-size: 0.74rem;
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border);
      padding: 0.14rem 0.48rem;
      border-radius: 6px;
      color: var(--muted);
    }}
    .proof-box {{
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.6rem 0.75rem;
    }}
    .proof-heading {{ font-size: 0.73rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); margin-bottom: 0.35rem; }}
    .proof-links {{ display: flex; flex-direction: column; gap: 0.3rem; }}
    .proof-link {{ font-size: 0.82rem; color: var(--text); text-decoration: none; }}
    .proof-link:hover {{ color: var(--accent); text-decoration: underline; }}
    .proof-type {{
      display: inline-block;
      font-size: 0.7rem;
      background: var(--green-soft);
      color: var(--green);
      padding: 0.05rem 0.4rem;
      border-radius: 4px;
      margin-right: 0.35rem;
    }}
    .repos {{ border-top: 1px solid var(--border); padding-top: 0.75rem; display: flex; flex-direction: column; gap: 0.4rem; }}
    .bucket {{ display: flex; flex-wrap: wrap; gap: 0.38rem; }}
    .pill {{
      font-size: 0.76rem;
      padding: 0.16rem 0.5rem;
      border-radius: 6px;
      text-decoration: none;
      display: inline-block;
    }}
    .pill-public {{
      color: var(--accent);
      background: var(--accent-soft);
      border: 1px solid rgba(91, 140, 255, 0.25);
    }}
    .pill-public:hover {{ border-color: var(--accent); text-decoration: underline; }}
    .pill-crossref {{
      color: var(--cyan);
      background: rgba(76, 212, 232, 0.1);
      border: 1px solid rgba(76, 212, 232, 0.25);
    }}
    .xref {{ opacity: 0.85; font-size: 0.7rem; }}
    .pill-private {{
      color: var(--amber);
      background: var(--amber-soft);
      border: 1px solid rgba(245, 185, 66, 0.25);
    }}
    .pill-design {{
      color: var(--muted);
      background: rgba(255,255,255,0.04);
      border: 1px dashed var(--border);
    }}
    #empty-state {{
      background: var(--surface);
      border: 1px dashed var(--border);
      border-radius: 10px;
      padding: 1.5rem;
      text-align: center;
      color: var(--muted);
      margin-top: 1rem;
    }}
    .standards-section {{ margin-top: 2.5rem; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      overflow: hidden;
      font-size: 0.88rem;
    }}
    th, td {{
      text-align: left;
      padding: 0.75rem 0.9rem;
      border-bottom: 1px solid var(--border);
      vertical-align: top;
    }}
    th {{ background: var(--surface-alt); color: #fff; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.03em; }}
    td code {{ color: var(--accent); font-size: 0.8rem; }}
    footer {{
      margin-top: 2.5rem;
      padding-top: 1.25rem;
      border-top: 1px solid var(--border);
      color: var(--muted);
      font-size: 0.83rem;
      text-align: center;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <span class="badge">{_esc(owner.role_title)}</span>
      <h1>{_esc(owner.name)} (@{_esc(owner.github_handle)})</h1>
      <p class="subtitle">
        Enterprise-grade product suites across Agentic AI-Driven Enterprise Architecture,
        Agentic Open Finance (BaaS), Core Banking &amp; Process Orchestration (Camunda 8.10),
        Separately Sponsored EV PnC Consents &amp; Wallets, and Multi-Tenant Serverless SaaS.
      </p>
      <div class="links">
        <a href="{_esc(owner.github_profile_url)}">GitHub Profile</a>
        <a href="{_esc(owner.catalog_url)}">Full Product Catalog</a>
        <a href="{_esc(owner.discussions_url)}">Contact / Discussions</a>
      </div>
    </header>

    <section class="controls" aria-label="Filter product suites">
      <div class="filter-bar">
        {"".join(filter_buttons)}
      </div>
      <div class="secondary-controls">
        <div class="inputs">
          <select id="maturity-filter" aria-label="Filter by maturity tier">
            {"".join(maturity_options)}
          </select>
          <input id="suite-search" type="search" placeholder="Search suite, repo, technology, sponsor..." aria-label="Search product suites" />
        </div>
        <div id="filter-status" aria-live="polite">Showing {len(suite_vms)} of {len(suite_vms)} product suites</div>
      </div>
    </section>

    <h2>Enterprise Product Suites (10 Canonical Suites)</h2>
    <div class="grid" id="suites-grid">
{chr(10).join(cards_html)}
    </div>
    <div id="empty-state" hidden>No product suites match the selected domain, maturity tier, or search filter.</div>

    <section id="standards-matrix" class="standards-section">
      <h2>Enterprise Engineering Standards Across All Products</h2>
      <table>
        <thead>
          <tr>
            <th>Pillar</th>
            <th>Implementation Standard</th>
            <th>Applied Suites</th>
          </tr>
        </thead>
        <tbody>
          {standards_rows}
        </tbody>
      </table>
    </section>

    <footer>
      Generated deterministically from SSOT catalog · Revision {_esc(catalog.metadata.catalog_revision)} · @{_esc(owner.github_handle)}
    </footer>
  </div>

  <script>
    (function () {{
      var ALLOWED_DOMAINS = {{"ALL": true, "D1_AGENTIC_AI": true, "D2_OPEN_FINANCE_CORE": true, "D3_EV_MOBILITY": true, "D4_SERVERLESS_INTELLIGENCE": true}};
      var ALLOWED_MATURITIES = {{"ALL": true, "RUNNABLE_K8S_CLI_DEMO": true, "PUBLIC_REFERENCE_BASELINE": true, "CONTRACT_FIRST_ECOSYSTEM": true, "GOVERNED_PRIVATE_ENTERPRISE_BASELINE": true}};

      var activeDomain = "ALL";
      var activeMaturity = "ALL";
      var activeQuery = "";

      var cards = Array.prototype.slice.call(document.querySelectorAll("#suites-grid .card"));
      var buttons = Array.prototype.slice.call(document.querySelectorAll("[data-domain-filter]"));
      var maturitySelect = document.getElementById("maturity-filter");
      var searchInput = document.getElementById("suite-search");
      var statusEl = document.getElementById("filter-status");
      var emptyEl = document.getElementById("empty-state");

      function applyFilters() {{
        var visible = 0;
        var q = activeQuery.trim().toLowerCase();
        cards.forEach(function (card) {{
          var dOk = activeDomain === "ALL" || card.dataset.domain === activeDomain;
          var mOk = activeMaturity === "ALL" || card.dataset.maturity === activeMaturity;
          var sOk = q === "" || (card.dataset.searchIndex || "").indexOf(q) !== -1;
          var match = dOk && mOk && sOk;
          card.hidden = !match;
          card.classList.toggle("is-hidden", !match);
          if (match) visible += 1;
        }});
        statusEl.textContent = "Showing " + visible + " of " + cards.length + " product suites";
        emptyEl.hidden = visible > 0;
      }}

      function setActiveDomain(domainId) {{
        activeDomain = ALLOWED_DOMAINS[domainId] ? domainId : "ALL";
        buttons.forEach(function (btn) {{
          var selected = btn.dataset.domainFilter === activeDomain;
          btn.classList.toggle("is-active", selected);
          btn.setAttribute("aria-pressed", selected ? "true" : "false");
        }});
        applyFilters();
      }}

      buttons.forEach(function (btn) {{
        btn.addEventListener("click", function () {{
          setActiveDomain(btn.dataset.domainFilter || "ALL");
        }});
      }});

      if (maturitySelect) {{
        maturitySelect.addEventListener("change", function () {{
          var val = maturitySelect.value || "ALL";
          activeMaturity = ALLOWED_MATURITIES[val] ? val : "ALL";
          applyFilters();
        }});
      }}

      if (searchInput) {{
        searchInput.addEventListener("input", function () {{
          activeQuery = searchInput.value || "";
          applyFilters();
        }});
      }}

      try {{
        var params = new URLSearchParams(window.location.search);
        var qDom = params.get("domain");
        var qMat = params.get("maturity");
        if (qMat && ALLOWED_MATURITIES[qMat]) {{
          activeMaturity = qMat;
          if (maturitySelect) maturitySelect.value = qMat;
        }}
        if (qDom && ALLOWED_DOMAINS[qDom]) {{
          setActiveDomain(qDom);
        }} else {{
          applyFilters();
        }}
      }} catch (e) {{
        applyFilters();
      }}
    }})();
  </script>
</body>
</html>
"""


def render_brief_assets(catalog: Catalog) -> Dict[str, str]:
    suite_by_id = {s.suite_id: s for s in catalog.suites}
    outputs: Dict[str, str] = {"docs/.nojekyll": ""}
    for brief in sorted(catalog.briefs, key=lambda b: b.slug):
        suite = suite_by_id[brief.suite_id]
        md_lines = [
            f"# {brief.title}",
            "",
            f"> **Suite {suite.suite_number}:** {suite.title}  ",
            f"> **Maturity Tier:** `{MATURITY_LABELS[suite.maturity_tier]}` · **Sponsor / Scope:** {suite.sponsor_label}",
            "",
            f"*{brief.subtitle}*",
            "",
            "## Context & Architectural Intent",
            "",
            brief.context_summary,
            "",
            "## Architecture Highlights",
            "",
        ]
        for h in brief.architecture_highlights:
            md_lines.append(f"- {h}")
        md_lines.extend(["", "## Guardrails & Compliance", ""])
        for g in brief.guardrails_and_compliance:
            md_lines.append(f"- {g}")
        md_lines.extend(
            [
                "",
                "## Architecture Diagram",
                "",
                "```mermaid",
                brief.diagram_mermaid,
                "```",
                "",
                "---",
                "[← Back to Full Catalog](../PROJECTS.md) · [← Back to Profile README](../README.md)",
                "",
            ]
        )
        outputs[f"briefs/{brief.slug}.md"] = "\n".join(md_lines)

        highlights_html = "".join(f"<li>{_esc(h)}</li>" for h in brief.architecture_highlights)
        guardrails_html = "".join(f"<li>{_esc(g)}</li>" for g in brief.guardrails_and_compliance)
        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{_esc(brief.title)}</title>
  <style>
    :root {{ --bg:#0b1020; --surface:#121933; --border:#232d54; --text:#e6ebf5; --muted:#9aa7c7; --accent:#5b8cff; --green:#3ddc97; }}
    * {{ box-sizing:border-box; margin:0; padding:0; }}
    body {{ font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,sans-serif; background:var(--bg); color:var(--text); line-height:1.6; padding:2.25rem 1.25rem; }}
    .wrap {{ max-width:900px; margin:0 auto; }}
    .back {{ display:inline-block; color:var(--accent); text-decoration:none; margin-bottom:1.25rem; font-size:0.9rem; }}
    .back:hover {{ text-decoration:underline; }}
    .card {{ background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:1.6rem; margin-bottom:1.25rem; }}
    h1 {{ font-size:1.65rem; margin-bottom:0.4rem; }}
    .sub {{ color:var(--green); font-size:0.9rem; margin-bottom:1rem; }}
    h2 {{ font-size:1.1rem; margin:1.25rem 0 0.6rem; color:#fff; }}
    p, li {{ color:var(--muted); font-size:0.95rem; }}
    ul {{ padding-left:1.25rem; display:flex; flex-direction:column; gap:0.4rem; }}
    pre {{ background:#090d1a; border:1px solid var(--border); border-radius:8px; padding:1rem; overflow-x:auto; color:#cfe0ff; font-size:0.84rem; }}
  </style>
</head>
<body>
  <div class="wrap">
    <a class="back" href="../index.html">← Back to Enterprise Product Suites</a>
    <div class="card">
      <h1>{_esc(brief.title)}</h1>
      <div class="sub">Suite {suite.suite_number} · {_esc(MATURITY_LABELS[suite.maturity_tier])} · {_esc(suite.sponsor_label)}</div>
      <p>{_esc(brief.context_summary)}</p>
      <h2>Architecture Highlights</h2>
      <ul>{highlights_html}</ul>
      <h2>Guardrails &amp; Compliance</h2>
      <ul>{guardrails_html}</ul>
      <h2>Architecture Diagram (Mermaid Source)</h2>
      <pre>{_esc(brief.diagram_mermaid)}</pre>
    </div>
  </div>
</body>
</html>
"""
        outputs[f"docs/briefs/{brief.slug}.html"] = html_doc
    return outputs


def render_all(catalog: Catalog) -> Dict[str, str]:
    outputs: Dict[str, str] = {
        "README.md": render_readme(catalog),
        "PROJECTS.md": render_projects_md(catalog),
        "docs/index.html": render_html_showcase(catalog),
    }
    outputs.update(render_brief_assets(catalog))
    return outputs
