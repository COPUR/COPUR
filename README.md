# Ali Çopur (`@COPUR`)

**Enterprise Software Architect & Product Engineering Leader**

Building **enterprise-grade software products and platforms** across **Agentic AI-Driven Enterprise Architecture**, **Agentic Open Finance (BaaS)**, **Regulated Core Banking & Process Orchestration**, and **EV Roaming & Mobility**. Every system is engineered with deterministic safety harnesses, contract-first governance, and zero-trust security boundaries.

---

## Enterprise Product Suites

### 1. Agentic AI-Driven Enterprise Architecture & Governance Suite
*Target: Tier-1 Financial Institutions, Enterprise Architecture Boards, Regulated Engineering Organizations*

A production-oriented, zero-trust platform family that turns non-deterministic LLMs/SLMs into governed, auditable enterprise architecture and engineering capacity—built on the core paradigm **`Agent = Model + Harness` (*The Deterministic Sandwich*)**.

- **Agentive Enterprise Architecture & Governed Delivery Platforms**
  - **Product Value:** Autonomous, TOGAF ADM & BDAT-aligned multi-agent platforms (`EA-Agentive-Platform-v3`, `X_Bank-Agentive-Architecture-Framework`, `AgentiveArchitectureFW_v3`, `redbank-agentive-framework`) where five governance agents and seven domain developer agents design, validate, and scaffold core-banking microservices under regulatory policy.
  - **Enterprise Controls:** Models emit only schema/Zod-validated JSON while deterministic Java (Spring Boot) or Node.js/TypeScript harnesses execute every side effect; DPoP-authenticated agent gateways, streaming DLP via Security SLMs, compute-aware routing (SLMs → 70B local models), `pgvector` semantic caching, W3C Trace Context observability, and compliance targeting **CBUAE 3/2025** data residency & **PCI-DSS v4** *(maintained in private enterprise repositories)*.

- **Jeff — Self-Hosted AI Tool-Call Firewall**
  - **Product Value:** On-premise decision layer implementing TypeSafe's `jev` System One API to inspect and gate AI coding-agent tool calls (`PreToolUse` hooks) without sending proprietary code or prompts to external paid APIs.
  - **Enterprise Controls:** Powered by `GLiFormer` (400M parameters) with local Qwen (LM Studio) escalation for uncertain classifications before human-in-the-loop fallback.
  - **Public Repository:** [`jeff`](https://github.com/COPUR/jeff)

- **Architecture-as-Code, Cloud Controls & Agent Protocols**
  - **Product Value:** Machine-readable, version-controlled enterprise architecture (`architecture-as-code`), financial AI governance frameworks (`ai-governance-framework`, `common-cloud-controls`), multi-protocol agent interoperability (`ai-agent-protocols`: Google ADK, MCP, A2A, Quarkus, LangChain4j), and automated book-to-skill synthesis (`book-to-skill` in private repos).
  - **Public Repositories:** [`ai-governance-framework`](https://github.com/COPUR/ai-governance-framework) · [`architecture-as-code`](https://github.com/COPUR/architecture-as-code) · [`common-cloud-controls`](https://github.com/COPUR/common-cloud-controls) · [`ai-agent-protocols`](https://github.com/COPUR/ai-agent-protocols) · [`fintechbankx-governance-architecture-enablement-adr-runbooks`](https://github.com/COPUR/fintechbankx-governance-architecture-enablement-adr-runbooks)

---

### 2. Agentic Open Finance (BaaS) & Core Banking Orchestration Suite
*Target: Open Finance Ecosystems, Tier-1 Banks, Payment Service Providers (PSPs), Digital & Islamic Banks*

- **OPF — Agentive Open Finance (BaaS) Platform**
  - **Product Value:** Acts as an **Agentive Translation Layer** between Open Finance / BaaS ecosystems and incumbent core-banking constraints, replacing brittle static state machines with **Temporal-orchestrated autonomous agents** (V2–V4 architecture).
  - **Enterprise Controls:** **Model Cascades (MoE)** routing simple intents to ultra-fast SLMs before foundation models, **`pgvector` Semantic Caching** bypassing LLM inference for >80% of recurring intents, regulated architecture backlogs, and AI data controls.
  - **Public Platform:** [`OPF-Agentive-Platform`](https://github.com/COPUR/OPF-Agentive-Platform) *(V3 & V4 regulated baselines maintained in private enterprise repositories)*

- **Instant Payment Exception & BPO Orchestrator**
  - **Product Value:** Automates mission-critical payment exception lifecycles (e.g., TR BKM FAST `pay-instant-exception`) on Camunda 8.10 with deterministic state transitions, human-in-the-loop escalation (Operate/Tasklist), and zero PII leakage into workflow state.
  - **Enterprise Controls:** Runtime output guardrails (`OutputVariables`) blocking monetary/PII fields from process engines, idempotent ledger capture (`x-idempotency-key`), per-provider OIDC audience isolation via Keycloak, and one-command Kubernetes/Helm deployment.
  - **Public Repositories:** [`demo-camunda-k8s`](https://github.com/COPUR/demo-camunda-k8s) · [`neo-fintechbankx-bpo-process-orchestration`](https://github.com/COPUR/neo-fintechbankx-bpo-process-orchestration) · [`camunda8-banking-poc`](https://github.com/COPUR/camunda8-banking-poc)

- **FinTechBankX Core Lending, Payments & Open Finance Modules**
  - **Product Value:** Multi-wave, domain-driven banking core covering KYC/customer profile, IAM (Keycloak/LDAP), Terraform IaC modules, CI/CD templates, Service Mesh security, Kafka event streaming, and centralized OpenAPI/AsyncAPI/Schema Registry catalogs.
  - **Public Platform Modules:** [`fintechbankx-customer-profile-kyc-core`](https://github.com/COPUR/fintechbankx-customer-profile-kyc-core) · [`fintechbankx-platform-identity-iam-keycloak-ldap`](https://github.com/COPUR/fintechbankx-platform-identity-iam-keycloak-ldap) · [`fintechbankx-platform-mesh-security-service-mesh`](https://github.com/COPUR/fintechbankx-platform-mesh-security-service-mesh) · [`fintechbankx-platform-event-streaming-kafka`](https://github.com/COPUR/fintechbankx-platform-event-streaming-kafka) · [`fintechbankx-platform-delivery-iac-terraform-modules`](https://github.com/COPUR/fintechbankx-platform-delivery-iac-terraform-modules) · [`fintechbankx-governance-api-contracts-openapi-catalog`](https://github.com/COPUR/fintechbankx-governance-api-contracts-openapi-catalog) · [`fintechbankx-governance-api-contracts-asyncapi-catalog`](https://github.com/COPUR/fintechbankx-governance-api-contracts-asyncapi-catalog) · [`fintechbankx-governance-api-contracts-schema-registry`](https://github.com/COPUR/fintechbankx-governance-api-contracts-schema-registry)

- **MasruFi — Sharia-Compliant Digital Finance Engine**
  - **Product Value:** Production-oriented domain engine implementing Islamic finance instruments (Istisna, Ijarah, Qard Hassan) alongside crypto-banking primitives using strict DDD and Hexagonal Architecture.

---

### 3. EV Mobility — Consent Authority, Wallet & Telemetry Product Suites
*Two independent, separately sponsored EV Plug & Charge (PnC) initiatives plus automotive telemetry*

- **Consent EV PnC — Centralized Regulator Consent Authority** *(Sponsor: Government / Centralized Regulator)*
  - **Product Value:** Neutral, regulator-sponsored Plug & Charge consent registry managing consent catalogues, notices, grants, receipts, safeguards, data-subject rights, decisioning, and cross-ecosystem revocation propagation.
  - **Enterprise Controls:** Dedicated contracts repository as the single source of truth (OpenAPI, AsyncAPI, JSON Schema), automated SDK generation, and consumer-driven contract verification.
  - **Public Repositories:** [`EV_PnC_Consent_contracts`](https://github.com/COPUR/EV_PnC_Consent_contracts) · [`EV_PnC_Consent_registry`](https://github.com/COPUR/EV_PnC_Consent_registry) · [`EV_PnC_Consent_decision`](https://github.com/COPUR/EV_PnC_Consent_decision) · [`EV_PnC_Consent_testkit`](https://github.com/COPUR/EV_PnC_Consent_testkit) · [`EV_PnC_Consent_docs`](https://github.com/COPUR/EV_PnC_Consent_docs)

- **Wallet PnC EV — Fintech & CPO Wallet + Loyalty Platform** *(Sponsor: Fintechs / Charge Point Operators / eMSPs)*
  - **Product Value:** Stakeholder-sponsored Plug & Charge wallet platform enabling any Fintech or Charge Point Operator (CPO) to operate their own branded EV wallet with loyalty solutions, OCPI eMSP roaming adapters, hub gateway, telemetry, and pilot analytics.
  - **Public Repositories:** [`EV_PNC_hub-gateway`](https://github.com/COPUR/EV_PNC_hub-gateway) · [`EV_PNC_hub-contracts`](https://github.com/COPUR/EV_PNC_hub-contracts) · [`EV_PNC_ocpi-emsp`](https://github.com/COPUR/EV_PNC_ocpi-emsp) · [`EV_PNC_ocpi-model`](https://github.com/COPUR/EV_PNC_ocpi-model) · [`EV_PNC_telemetry`](https://github.com/COPUR/EV_PNC_telemetry) · [`EV_PNC_pilot-analytics`](https://github.com/COPUR/EV_PNC_pilot-analytics) · [`EV_PNC_simulator`](https://github.com/COPUR/EV_PNC_simulator) · [`EV_PNC_infra-modules`](https://github.com/COPUR/EV_PNC_infra-modules)

- **Driver Experience & Automotive Verification Products**
  - **EV Telemetry & CAN Engineering:** CAN bus exploration, FSD/open CAN mods, controlled offline bench simulation, Pre-Delivery Inspection (`PreFlight_PDI`), and Tesla Fleet Telemetry route/charging companion (*EV Geek Stats*).
  - **Public Repositories:** [`tesla-can-mod`](https://github.com/COPUR/tesla-can-mod) · [`tesla-fsd-can-mod`](https://github.com/COPUR/tesla-fsd-can-mod) · [`tesla-open-can-mod`](https://github.com/COPUR/tesla-open-can-mod)

---

### 4. Serverless Content & Operational Intelligence Suite
*Target: Digital Media Platforms, Event-Driven SaaS Teams*

- **Multi-Tenant Serverless News & Observability Platform**
  - **Product Value:** High-reliability, multi-tenant EV news aggregation and workflow platform built on Go/AWS Serverless with ADR-governed architecture and idempotent workflow execution, paired with local-first Node.js 20+ agents and an independently deployable Prisma/Docker dashboard microservice *(maintained in private repositories)*.

---

## Enterprise Engineering Standards Across All Products

| Pillar | Implementation Standard |
|---|---|
| **Deterministic Sandwich** | `Agent = Model + Harness` — LLMs produce schema-validated JSON only; deterministic code executes all side effects |
| **Contract-First Governance** | Single-source OpenAPI, AsyncAPI, and JSON Schema registries with consumer-driven contract tests |
| **Zero-Trust & Residency** | Per-provider OIDC/DPoP scoping, restricted K8s Pod Security, default-deny `NetworkPolicy`, CBUAE/PCI-DSS v4 alignment |
| **Air-Gapped / On-Prem AI** | Local SLM/LLM inference & policy gating (`GLiFormer`, local Qwen, `pgvector` semantic caching) with zero external egress |

---

For detailed product specifications, deployment topologies, and technical stacks, see the [Enterprise Product Catalog](./PROJECTS.md) or visit the [Interactive Portfolio](https://copur.github.io/).
