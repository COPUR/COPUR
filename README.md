# Ali Çopur (`@COPUR`)

**Enterprise Software Architect & Product Engineering Leader · 

Building **enterprise-grade software products and platforms** across **Regulated Banking & Open Finance**, **Business Process Orchestration**, **EV Roaming & Mobility**, and **On-Premise AI Governance**. Every system is engineered with contract-first governance, zero-trust security boundaries, and production-ready operability.

---

## Enterprise Product Suites

### 1. FinTechBankX — Core Banking, Open Finance & Payment Orchestration Suite
*Target: Tier-1 Banks, Payment Service Providers (PSPs), Digital & Islamic Banks*

An end-to-end, domain-driven banking and process orchestration product family designed for regulated financial institutions requiring strict auditability, multi-jurisdiction isolation, and zero-trust service boundaries.

- **Instant Payment Exception & BPO Orchestrator**
  - **Product Value:** Automates mission-critical payment exception lifecycles (e.g., TR BKM FAST `pay-instant-exception`) with deterministic state transitions, human-in-the-loop escalation (Operate/Tasklist), and zero PII leakage into workflow state.
  - **Enterprise Controls:** Runtime output guardrails (`OutputVariables`) blocking monetary/PII fields from process engines, idempotent ledger capture (`x-idempotency-key`), per-provider OIDC audience isolation via Keycloak, and one-command Kubernetes/Helm deployment.
  - **Public Repositories:** [`demo-camunda-k8s`](https://github.com/COPUR/demo-camunda-k8s) · [`neo-fintechbankx-bpo-process-orchestration`](https://github.com/COPUR/neo-fintechbankx-bpo-process-orchestration) · [`camunda8-banking-poc`](https://github.com/COPUR/camunda8-banking-poc)

- **Enterprise Lending, Payments & Open Finance Platform**
  - **Product Value:** Modular banking core covering loan lifecycle management, payment orchestration, KYC/customer profile, and Open Finance APIs.
  - **Enterprise Controls:** Multi-wave microservices governance backed by IAM (Keycloak/LDAP), Terraform IaC modules, CI/CD templates, Service Mesh security, Kafka event streaming, and centralized OpenAPI/AsyncAPI/JSON Schema catalogs.
  - **Public Platform Modules:** [`OPF-Agentive-Platform`](https://github.com/COPUR/OPF-Agentive-Platform) · [`fintechbankx-customer-profile-kyc-core`](https://github.com/COPUR/fintechbankx-customer-profile-kyc-core) · [`fintechbankx-platform-identity-iam-keycloak-ldap`](https://github.com/COPUR/fintechbankx-platform-identity-iam-keycloak-ldap) · [`fintechbankx-platform-mesh-security-service-mesh`](https://github.com/COPUR/fintechbankx-platform-mesh-security-service-mesh) · [`fintechbankx-platform-event-streaming-kafka`](https://github.com/COPUR/fintechbankx-platform-event-streaming-kafka) · [`fintechbankx-platform-delivery-iac-terraform-modules`](https://github.com/COPUR/fintechbankx-platform-delivery-iac-terraform-modules) *(Core lending authority & compliance modules maintained in private enterprise repositories)*

- **MasruFi — Sharia-Compliant Digital Finance Engine**
  - **Product Value:** Production-oriented domain engine implementing Islamic finance instruments (Istisna, Ijarah, Qard Hassan) alongside crypto-banking primitives using strict DDD and Hexagonal Architecture.

---

### 2. EV Mobility — Plug & Charge Consent & Telemetry Product Suite
*Target: Charge Point Operators (CPOs), eMSPs, Automotive & EV Ecosystem Platforms*

A contract-first mobility platform enabling compliant EV roaming consent management, OCPI integration, telemetry, and safe vehicle diagnostics engineering.

- **EV PnC Consent & Roaming Governance Platform**
  - **Product Value:** Neutral, centralized Plug & Charge (PnC) roaming consent registry managing consent catalogues, notices, grants, receipts, safeguards, data-subject rights, and multi-tenancy—paired with OCPI eMSP adapters, hub gateway, telemetry, simulator, and revocation propagation workers.
  - **Enterprise Controls:** Dedicated contracts repository as the single source of truth (OpenAPI, AsyncAPI, JSON Schema), automated SDK generation, and consumer-driven contract verification.
  - **Public Repositories:** [`EV_PnC_Consent_contracts`](https://github.com/COPUR/EV_PnC_Consent_contracts) · [`EV_PnC_Consent_registry`](https://github.com/COPUR/EV_PnC_Consent_registry) · [`EV_PnC_Consent_decision`](https://github.com/COPUR/EV_PnC_Consent_decision) · [`EV_PnC_Consent_testkit`](https://github.com/COPUR/EV_PnC_Consent_testkit) · [`EV_PNC_hub-gateway`](https://github.com/COPUR/EV_PNC_hub-gateway) · [`EV_PNC_ocpi-emsp`](https://github.com/COPUR/EV_PNC_ocpi-emsp) · [`EV_PNC_telemetry`](https://github.com/COPUR/EV_PNC_telemetry) · [`EV_PNC_simulator`](https://github.com/COPUR/EV_PNC_simulator)

- **Driver Experience & Automotive Verification Products**
  - **EV Telemetry & CAN Engineering:** CAN bus exploration, FSD/open CAN mods, and controlled offline bench simulation tooling.
  - **EV Geek Stats *(In Design)*:** Official Tesla Fleet Telemetry iPhone companion integrating Türkiye climate/weather data, 50 km / route-based CPO discovery, pricing/availability visibility, and navigation handoff.
  - **Public Repositories:** [`tesla-can-mod`](https://github.com/COPUR/tesla-can-mod) · [`tesla-fsd-can-mod`](https://github.com/COPUR/tesla-fsd-can-mod) · [`tesla-open-can-mod`](https://github.com/COPUR/tesla-open-can-mod)

---

### 3. On-Prem AI Governance & Agentic Engineering Platform
*Target: Security-Sensitive Engineering Teams, Regulated Enterprises Adopting AI Coding Agents*

A zero-egress AI control plane that brings deterministic policy enforcement and structured enterprise architecture governance to autonomous coding agents.

- **Jeff — Self-Hosted AI Tool-Call Firewall**
  - **Product Value:** On-premise decision layer implementing TypeSafe's `jev` System One API to inspect and gate AI coding-agent tool calls (`PreToolUse` hooks) without sending proprietary code or prompts to external paid APIs.
  - **Enterprise Controls:** Powered by `GLiFormer` (400M parameters) with local Qwen (LM Studio) escalation for uncertain classifications before human-in-the-loop fallback.
  - **Public Repositories:** [`jeff`](https://github.com/COPUR/jeff) · [`ai-governance-framework`](https://github.com/COPUR/ai-governance-framework) · [`architecture-as-code`](https://github.com/COPUR/architecture-as-code) · [`common-cloud-controls`](https://github.com/COPUR/common-cloud-controls)

- **TOGAF & Scrum Multi-Agent Delivery Framework**
  - **Product Value:** Structured agentic engineering squad modeled after enterprise architecture roles (Business, Data, Application, Technology Architects, Program Manager, Quality Engineer) with umbrella-to-vertical skill execution.

---

### 4. Serverless Content & Operational Intelligence Suite
*Target: Digital Media Platforms, Event-Driven SaaS Teams*

- **Multi-Tenant Serverless News & Observability Platform**
  - **Product Value:** High-reliability, multi-tenant EV news aggregation and workflow platform built on Go/AWS Serverless with ADR-governed architecture and idempotent workflow execution, paired with local-first Node.js 20+ agents and an independently deployable Prisma/Docker dashboard microservice *(maintained in private repositories)*.

---

## Enterprise Engineering Standards Across All Products

| Pillar | Implementation Standard |
|---|---|
| **Contract-First Governance** | Single-source OpenAPI, AsyncAPI, and JSON Schema registries with consumer-driven contract tests |
| **Zero-Trust Security** | Per-provider OIDC audience scoping, restricted Kubernetes Pod Security, default-deny `NetworkPolicy`, HTTPS/JWT |
| **Resilience & Correctness** | Hexagonal ports/adapters, idempotent pivot steps, runtime PII/payload guardrails, deterministic error mapping |
| **Air-Gapped / On-Prem AI** | Local SLM/LLM policy gating (`GLiFormer` + local Qwen) with zero external data egress |

---

For detailed product specifications, deployment topologies, and technical stacks, see the [Enterprise Product Catalog](./PROJECTS.md) or visit the [Interactive Portfolio](https://copur.github.io/COPUR/).
