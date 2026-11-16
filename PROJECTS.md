# Enterprise Product & Architecture Catalog

Detailed product breakdown of the `@COPUR` portfolio, structured by product suite, business problem, enterprise guarantees, and underlying technical components.

---

## Suite 1: Agentic AI-Driven Enterprise Architecture & Governance

### Product 1.1: RedBank / X_Bank / EA Agentive Architecture Frameworks
- **Private Enterprise Components:** `redbank-agentive-framework`, `redbank-agentive-enterprise-architecture`, `EA-Agentive-Platform-v3`, `X_Bank-Agentive-Architecture-Framework`, `AgentiveArchitectureFW_v3`, `redbank-agentive-framework`
- **Target Market:** Tier-1 banks and regulated enterprises adopting AI-native architecture engineering.
- **Business Problem Solved:** Enables autonomous multi-agent architecture design and microservice scaffolding without exposing core banking systems to unvalidated LLM outputs or external data egress.
- **Enterprise Capabilities:**
  - **The Deterministic Sandwich (`Agent = Model + Harness`):** Models output only schema/Zod-validated JSON; deterministic Java (Spring Boot / Java 26) or Node.js/TypeScript harnesses execute every side effect.
  - **Multi-Agent Fleet:** Five governance agents + seven domain developer agents (one per core-banking domain) operating under TOGAF ADM and BDAT enterprise layering.
  - **Zero-Trust & Regulatory Alignment:** DPoP-authenticated agent gateway, Temporal.io durable intent orchestration, streaming DLP via Security SLMs, compute-aware routing (SLMs → 70B local models), `pgvector` semantic caching, W3C Trace Context, and compliance targeting **CBUAE 3/2025** data residency & **PCI-DSS v4**.

### Product 1.2: Jeff — Self-Hosted AI Tool-Call Firewall
- **Public Component:** [`jeff`](https://github.com/COPUR/jeff)
- **Target Market:** Enterprises deploying AI coding assistants under strict data-residency and cost-control mandates.
- **Business Problem Solved:** Prevents unauthorized or risky agent tool executions via `PreToolUse` hooks without relying on external paid classification APIs.
- **Enterprise Capabilities:** Self-hosted implementation of TypeSafe's `jev` System One API powered by `GLiFormer` (400M parameters), escalating uncertain classifications to a local Qwen model (LM Studio) before human-in-the-loop fallback.
- **Tech Stack:** Python, `uv`, GLiFormer (400M), LM Studio (local Qwen).

### Product 1.3: Architecture-as-Code, Cloud Controls & Agent Protocols
- **Public Components:** [`ai-governance-framework`](https://github.com/COPUR/ai-governance-framework) · [`architecture-as-code`](https://github.com/COPUR/architecture-as-code) · [`common-cloud-controls`](https://github.com/COPUR/common-cloud-controls) · [`ai-agent-protocols`](https://github.com/COPUR/ai-agent-protocols) · [`fintechbankx-governance-architecture-enablement-adr-runbooks`](https://github.com/COPUR/fintechbankx-governance-architecture-enablement-adr-runbooks)
- **Private Components:** `book-to-skill`, `book-skills`, `fintechbankx-governance-architecture-enablement-enterprise-architecture`
- **Business Problem Solved:** Codifies enterprise architecture decisions, financial AI governance controls, multi-protocol agent interoperability (Google ADK, MCP, A2A, Quarkus, LangChain4j), and technical book knowledge into reusable, machine-readable agent skills and catalogs.

---

## Suite 2: Agentic Open Finance (BaaS) & Core Banking Orchestration

### Product 2.1: OPF — Agentive Open Finance (BaaS) Platform
- **Public Component:** [`OPF-Agentive-Platform`](https://github.com/COPUR/OPF-Agentive-Platform)
- **Private Enterprise Components:** `OPF_Agentive_Platform_V4`, `OPF-Agentive-Platform-V3`
- **Target Market:** Open Finance / Banking-as-a-Service (BaaS) platforms and incumbent banks modernizing legacy core interfaces.
- **Business Problem Solved:** Acts as an **Agentive Translation Layer** sitting between Open Finance channels and incumbent core-banking constraints, replacing static APIs and brittle state machines with durable autonomous workflows.
- **Enterprise Capabilities:**
  - **Temporal-Orchestrated AI Workflows:** Long-running, stateful intent orchestration across V2–V4 platform architectures.
  - **Model Cascades (MoE) & Semantic Caching:** Smart routing directs simple requests to ultra-fast SLMs before foundation models, while `pgvector` semantic caching bypasses LLM inference for >80% of recurring intents.
  - **Regulated Delivery:** Governed architecture backlogs and embedded AI data controls.

### Product 2.2: Instant Payment Exception & BPO Orchestrator
- **Public Components:** [`demo-camunda-k8s`](https://github.com/COPUR/demo-camunda-k8s) · [`neo-fintechbankx-bpo-process-orchestration`](https://github.com/COPUR/neo-fintechbankx-bpo-process-orchestration) · [`camunda8-banking-poc`](https://github.com/COPUR/camunda8-banking-poc)
- **Target Market:** Banks and PSPs operating instant payment rails (TR BKM FAST) and multi-jurisdiction payment operations.
- **Business Problem Solved:** Eliminates manual, error-prone handling of ambiguous/pending instant payment exceptions (`PDNG`) while guaranteeing that instructions are never re-submitted to the scheme.
- **Enterprise Capabilities:** Camunda 8.10 BPMN/DMN workflows, runtime `OutputVariables` guardrail blocking PII/monetary fields from workflow state, Keycloak 26.7 OIDC per-provider audience scoping, restricted Pod Security, and default-deny Kubernetes `NetworkPolicy`.
- **Tech Stack:** Camunda 8.10, Java 23, Gradle, Spring Boot, Kubernetes, Helm, Keycloak, PostgreSQL, Docker.

### Product 2.3: FinTechBankX Core Lending, Payments & Open Finance
- **Public Components:** [`fintechbankx-customer-profile-kyc-core`](https://github.com/COPUR/fintechbankx-customer-profile-kyc-core) · [`fintechbankx-platform-identity-iam-keycloak-ldap`](https://github.com/COPUR/fintechbankx-platform-identity-iam-keycloak-ldap) · [`fintechbankx-platform-delivery-iac-cicd-templates`](https://github.com/COPUR/fintechbankx-platform-delivery-iac-cicd-templates) · [`fintechbankx-platform-delivery-iac-terraform-modules`](https://github.com/COPUR/fintechbankx-platform-delivery-iac-terraform-modules) · [`fintechbankx-platform-mesh-security-service-mesh`](https://github.com/COPUR/fintechbankx-platform-mesh-security-service-mesh) · [`fintechbankx-platform-event-streaming-kafka`](https://github.com/COPUR/fintechbankx-platform-event-streaming-kafka) · [`fintechbankx-governance-api-contracts-openapi-catalog`](https://github.com/COPUR/fintechbankx-governance-api-contracts-openapi-catalog) · [`fintechbankx-governance-api-contracts-asyncapi-catalog`](https://github.com/COPUR/fintechbankx-governance-api-contracts-asyncapi-catalog) · [`fintechbankx-governance-api-contracts-schema-registry`](https://github.com/COPUR/fintechbankx-governance-api-contracts-schema-registry)
- **Private Enterprise Components:** `enterprise-loan-management-system`, `fintechbankx-platform-observability-sre-operations`
- **Tech Stack:** Java, Spring Boot, Spring Cloud Gateway, Kafka, Redis, MongoDB, Keycloak/LDAP, Terraform, Kubernetes, Helm.

### Product 2.4: MasruFi — Sharia-Compliant Digital Finance Engine
- **Target Market:** Islamic banks, participation finance institutions, and Sharia-compliant fintech platforms.
- **Business Problem Solved:** Encodes Sharia-compliant financing contracts (**Istisna**, **Ijarah**, **Qard Hassan**) into testable, auditable software models integrated with crypto-banking primitives using DDD and Hexagonal Architecture.

---

## Suite 3: EV Mobility — Plug & Charge Consent & Telemetry

### Product 3.1: EV PnC Consent & Roaming Governance Platform
- **Public Components:** [`EV_PnC_Consent_contracts`](https://github.com/COPUR/EV_PnC_Consent_contracts) · [`EV_PnC_Consent_registry`](https://github.com/COPUR/EV_PnC_Consent_registry) · [`EV_PnC_Consent_decision`](https://github.com/COPUR/EV_PnC_Consent_decision) · [`EV_PnC_Consent_testkit`](https://github.com/COPUR/EV_PnC_Consent_testkit) · [`EV_PNC_hub-gateway`](https://github.com/COPUR/EV_PNC_hub-gateway) · [`EV_PNC_ocpi-emsp`](https://github.com/COPUR/EV_PNC_ocpi-emsp) · [`EV_PNC_telemetry`](https://github.com/COPUR/EV_PNC_telemetry) · [`EV_PNC_simulator`](https://github.com/COPUR/EV_PNC_simulator)
- **Target Market:** EV roaming hubs, CPOs, eMSPs, and mobility service providers.
- **Business Problem Solved:** Neutral, contract-first Plug & Charge roaming consent registry with single-source OpenAPI/AsyncAPI/JSON Schema contracts, consumer-driven tests, OCPI adapters, and revocation propagation workers.

### Product 3.2: Automotive Diagnostics & Driver Experience Products
- **Public Components:** [`tesla-can-mod`](https://github.com/COPUR/tesla-can-mod) · [`tesla-fsd-can-mod`](https://github.com/COPUR/tesla-fsd-can-mod) · [`tesla-open-can-mod`](https://github.com/COPUR/tesla-open-can-mod)
- **Private / In-Design Products:** `tesla-can-explorer-testing-only` *(offline CAN bench simulator & TDD rewrite engine)*, `PreFlight_PDI` *(iOS/Android delivery inspection app)*, and **EV Geek Stats** *(official Tesla Fleet Telemetry iPhone companion with Türkiye weather/wind integration and 50 km / route-based CPO discovery)*.

---

## Suite 4: Serverless Content & Operational Intelligence

### Product 4.1: Multi-Tenant Serverless News & Observability Platform
- **Private Components:** `daily-ev-news-serverless-go`, `daily-ev-news-agent`, `daily-news-agent`, `dashboard-service`
- **Target Market:** Digital publishing and event-driven SaaS teams.
- **Enterprise Capabilities:** ADR-governed Go/AWS Serverless multi-tenant architecture with idempotent workflow replay protection, paired with Node.js 20+ local-first agents and an independently deployable Prisma/Docker dashboard microservice.
- **Tech Stack:** Go, AWS Serverless, Node.js 20+, Prisma, Docker.
