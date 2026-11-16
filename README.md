# Ali Çopur (`@COPUR`)

**Enterprise Software Architect & Product Engineering Leader · 16+ Years Experience**

Building **enterprise-grade software products and platforms** across **Regulated Banking & Open Finance**, **Business Process Orchestration**, **EV Roaming & Mobility**, and **On-Premise AI Governance**. Every system is engineered with contract-first governance, zero-trust security boundaries, and production-ready operability.

---

## Enterprise Product Suites

### 1. FinTechBankX — Core Banking, Open Finance & Payment Orchestration Suite
*Target: Tier-1 Banks, Payment Service Providers (PSPs), Digital & Islamic Banks*

An end-to-end, domain-driven banking and process orchestration product family designed for regulated financial institutions requiring strict auditability, multi-jurisdiction isolation, and zero-trust service boundaries.

- **Instant Payment Exception & BPO Orchestrator**
  - **Product Value:** Automates mission-critical payment exception lifecycles (e.g., TR BKM FAST `pay-instant-exception`) with deterministic state transitions, human-in-the-loop escalation (Operate/Tasklist), and zero PII leakage into workflow state.
  - **Enterprise Controls:** Runtime output guardrails (`OutputVariables`) blocking monetary/PII fields from process engines, idempotent ledger capture (`x-idempotency-key`), per-provider OIDC audience isolation via Keycloak, and one-command Kubernetes/Helm deployment.
  - **Repositories:** [`demo-camunda-k8s`](https://github.com/COPUR/demo-camunda-k8s) · [`neo-fintechbankx-bpo-process-orchestration`](https://github.com/COPUR/neo-fintechbankx-bpo-process-orchestration)

- **Enterprise Lending, Payments & Open Finance Platform**
  - **Product Value:** Modular banking core covering loan lifecycle management, payment orchestration (initiation, settlement, request-to-pay, recurring mandates, bulk), KYC/risk decisioning, compliance evidence, and Open Finance consent/data APIs.
  - **Enterprise Controls:** Multi-wave microservices governance backed by centralized OpenAPI, AsyncAPI, and JSON Schema catalogs, Terraform IaC modules, Service Mesh security, Kafka event streaming, and SRE observability.
  - **Repositories:** [`enterprise-loan-management-system`](https://github.com/COPUR/enterprise-loan-management-system) · [`enhanced-loan-management`](https://github.com/COPUR/enhanced-loan-management) · [`LoanPayment_POC`](https://github.com/COPUR/LoanPayment_POC) · [`orangeTeamPOC`](https://github.com/COPUR/orangeTeamPOC) · [`banking-transformation-report`](https://github.com/COPUR/banking-transformation-report)

- **MasruFi — Sharia-Compliant Digital Finance Engine**
  - **Product Value:** Production-oriented domain engine implementing Islamic finance instruments (Istisna, Ijarah, Qard Hassan) alongside crypto-banking primitives.
  - **Enterprise Controls:** Strict Domain-Driven Design (DDD) and Hexagonal Architecture isolating financial rules from transport and persistence layers.
  - **Repository:** [`MasruFi_Framework`](https://github.com/COPUR/MasruFi_Framework)

---

### 2. EV Mobility — Plug & Charge Consent & Telemetry Product Suite
*Target: Charge Point Operators (CPOs), eMSPs, Automotive & EV Ecosystem Platforms*

A contract-first mobility platform enabling compliant EV roaming consent management, driver inspection workflows, and safe vehicle telemetry engineering.

- **EV PnC Consent Governance Platform**
  - **Product Value:** Neutral, centralized Plug & Charge (PnC) roaming consent registry managing consent catalogues, notices, grants, receipts, safeguards, data-subject rights, and multi-tenancy—paired with asynchronous revocation propagation workers.
  - **Enterprise Controls:** Dedicated contracts repository as the single source of truth (OpenAPI, AsyncAPI, JSON Schema), automated SDK generation, and consumer-driven contract verification.
  - **Repositories:** [`EV_PnC_Consent_contracts`](https://github.com/COPUR/EV_PnC_Consent_contracts) · [`EV_PnC_Consent_registry`](https://github.com/COPUR/EV_PnC_Consent_registry)

- **Driver Experience & Automotive Verification Products**
  - **PreFlight PDI:** Cross-platform (iOS & Android) delivery inspection product guiding EV owners through structured pre-delivery verification.
  - **Tesla CAN Explorer (Bench Edition):** Controlled, offline CAN bus simulator, replay tool, and TDD rewrite engine for safe automotive diagnostics engineering.
  - **EV Geek Stats *(In Design)*:** Official Tesla Fleet Telemetry iPhone companion integrating Türkiye climate/weather data, 50 km / route-based CPO discovery, pricing/availability visibility, and navigation handoff.
  - **Repositories:** [`PreFlight_PDI`](https://github.com/COPUR/PreFlight_PDI) · [`tesla-can-explorer-testing-only`](https://github.com/COPUR/tesla-can-explorer-testing-only)

---

### 3. On-Prem AI Governance & Agentic Engineering Platform
*Target: Security-Sensitive Engineering Teams, Regulated Enterprises Adopting AI Coding Agents*

A zero-egress AI control plane that brings deterministic policy enforcement and structured enterprise architecture governance to autonomous coding agents.

- **Jeff — Self-Hosted AI Tool-Call Firewall**
  - **Product Value:** On-premise decision layer implementing TypeSafe's `jev` System One API to inspect and gate AI coding-agent tool calls (`PreToolUse` hooks) without sending proprietary code or prompts to external paid APIs.
  - **Enterprise Controls:** Powered by `GLiFormer` (400M parameters) with local Qwen (LM Studio) escalation for uncertain classifications before human-in-the-loop fallback.
  - **Repository:** [`jeff`](https://github.com/COPUR/jeff)

- **TOGAF & Scrum Multi-Agent Delivery Framework**
  - **Product Value:** Structured agentic engineering squad modeled after enterprise architecture roles (Business, Data, Application, Technology Architects, Program Manager, Quality Engineer) with umbrella-to-vertical skill execution.

---

### 4. Serverless Content & Operational Intelligence Suite
*Target: Digital Media Platforms, Event-Driven SaaS Teams*

- **Multi-Tenant Serverless News & Observability Platform**
  - **Product Value:** High-reliability, multi-tenant EV news aggregation and workflow platform built on Go/AWS Serverless with ADR-governed architecture and idempotent workflow execution, paired with local-first Node.js 20+ agents and an independently deployable dashboard microservice.
  - **Repositories:** [`daily-ev-news-serverless-go`](https://github.com/COPUR/daily-ev-news-serverless-go) · [`daily-ev-news-agent`](https://github.com/COPUR/daily-ev-news-agent) · [`daily-news-agent`](https://github.com/COPUR/daily-news-agent) · [`dashboard-service`](https://github.com/COPUR/dashboard-service)

---

## Enterprise Engineering Standards Across All Products

| Pillar | Implementation Standard |
|---|---|
| **Contract-First Governance** | Single-source OpenAPI, AsyncAPI, and JSON Schema registries with consumer-driven contract tests |
| **Zero-Trust Security** | Per-provider OIDC audience scoping, restricted Kubernetes Pod Security, default-deny `NetworkPolicy`, HTTPS/JWT |
| **Resilience & Correctness** | Hexagonal ports/adapters, idempotent pivot steps, runtime PII/payload guardrails, deterministic error mapping |
| **Air-Gapped / On-Prem AI** | Local SLM/LLM policy gating (`GLiFormer` + local Qwen) with zero external data egress |

---

For detailed product specifications, deployment topologies, and technical stacks, see the [Enterprise Product Catalog](./PROJECTS.md).
