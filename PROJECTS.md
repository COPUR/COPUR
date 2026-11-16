# Enterprise Product & Architecture Catalog

Detailed product breakdown of the `@COPUR` portfolio, structured by product suite, business problem, enterprise guarantees, and underlying technical components.

---

## Suite 1: FinTechBankX — Core Banking, Open Finance & Process Orchestration

### Product 1.1: Instant Payment Exception & BPO Orchestrator
- **Public Components:** [`demo-camunda-k8s`](https://github.com/COPUR/demo-camunda-k8s) · [`neo-fintechbankx-bpo-process-orchestration`](https://github.com/COPUR/neo-fintechbankx-bpo-process-orchestration) · [`camunda8-banking-poc`](https://github.com/COPUR/camunda8-banking-poc)
- **Target Market:** Banks and PSPs operating instant payment rails (TR BKM FAST) and multi-jurisdiction payment operations.
- **Business Problem Solved:** Eliminates manual, error-prone handling of ambiguous/pending instant payment exceptions (`PDNG`) while guaranteeing that instructions are never re-submitted to the scheme.
- **Enterprise Capabilities:**
  - **Deterministic Orchestration:** Camunda 8.10 BPMN/DMN workflows with automated retry/wait timers (`PT30S`, `PT2M`, `PT10M`), message correlation (`Msg_SchemeStatusReported`), and tiered Tasklist escalation (`ops` → `supervisor`).
  - **Zero-PII Process State:** Runtime `OutputVariables` guardrail strictly rejects amounts, IBANs, and personal data from entering the workflow engine.
  - **Zero-Trust Service Security:** Keycloak 26.7 OIDC with per-provider scoped `client_credentials` tokens (`aud-svc-psg-tr`, `aud-svc-acc-accounts-ledger`, `aud-svc-pay-initiation-settlement`, `aud-svc-ntf`), restricted Pod Security, and default-deny Kubernetes `NetworkPolicy`.
  - **Turnkey Delivery:** Single-command (`./install.sh`) local Kubernetes deployment with PostgreSQL 17.6, Camunda Hub, Operate, Tasklist, and four HTTPS/JWT simulated providers.
- **Tech Stack:** Camunda 8.10, Java 23, Gradle, Spring Boot, Kubernetes, Helm, Keycloak, PostgreSQL, Docker.

### Product 1.2: Enterprise Lending, Payments & Open Finance Core
- **Public Components:** [`OPF-Agentive-Platform`](https://github.com/COPUR/OPF-Agentive-Platform) · [`fintechbankx-customer-profile-kyc-core`](https://github.com/COPUR/fintechbankx-customer-profile-kyc-core) · [`fintechbankx-platform-identity-iam-keycloak-ldap`](https://github.com/COPUR/fintechbankx-platform-identity-iam-keycloak-ldap) · [`fintechbankx-platform-delivery-iac-cicd-templates`](https://github.com/COPUR/fintechbankx-platform-delivery-iac-cicd-templates) · [`fintechbankx-platform-delivery-iac-terraform-modules`](https://github.com/COPUR/fintechbankx-platform-delivery-iac-terraform-modules) · [`fintechbankx-platform-mesh-security-service-mesh`](https://github.com/COPUR/fintechbankx-platform-mesh-security-service-mesh) · [`fintechbankx-platform-event-streaming-kafka`](https://github.com/COPUR/fintechbankx-platform-event-streaming-kafka)
- **Private Enterprise Components:** `enterprise-loan-management-system`, `fintechbankx-platform-observability-sre-operations`
- **Target Market:** Retail/corporate banks and fintechs modernizing legacy lending and launching Open Finance ecosystems.
- **Business Problem Solved:** Provides a modular, domain-aligned foundation replacing monolithic core banking modules with independently deployable, contract-governed capabilities.
- **Tech Stack:** Java, Spring Boot, Spring Cloud Gateway, Kafka, Redis, MongoDB, Keycloak/LDAP, Terraform, Kubernetes, Helm.

### Product 1.3: MasruFi — Sharia-Compliant Digital Finance Engine
- **Target Market:** Islamic banks, participation finance institutions, and Sharia-compliant fintech platforms.
- **Business Problem Solved:** Encodes complex Sharia-compliant financing contracts (**Istisna**, **Ijarah**, **Qard Hassan**) into testable, auditable software models integrated with crypto-banking primitives.
- **Tech Stack:** Java, Gradle, JS test suites, DDD, Hexagonal Architecture.

---

## Suite 2: EV Mobility — Plug & Charge Consent & Telemetry

### Product 2.1: EV PnC Consent & Roaming Governance Platform
- **Public Components:** [`EV_PnC_Consent_contracts`](https://github.com/COPUR/EV_PnC_Consent_contracts) · [`EV_PnC_Consent_registry`](https://github.com/COPUR/EV_PnC_Consent_registry) · [`EV_PnC_Consent_decision`](https://github.com/COPUR/EV_PnC_Consent_decision) · [`EV_PnC_Consent_testkit`](https://github.com/COPUR/EV_PnC_Consent_testkit) · [`EV_PNC_hub-gateway`](https://github.com/COPUR/EV_PNC_hub-gateway) · [`EV_PNC_ocpi-emsp`](https://github.com/COPUR/EV_PNC_ocpi-emsp) · [`EV_PNC_telemetry`](https://github.com/COPUR/EV_PNC_telemetry) · [`EV_PNC_simulator`](https://github.com/COPUR/EV_PNC_simulator)
- **Target Market:** EV roaming hubs, CPOs, eMSPs, and mobility service providers.
- **Business Problem Solved:** Establishes a neutral, verifiable consent source of truth for Plug & Charge roaming with rapid revocation propagation across ecosystem participants.
- **Enterprise Capabilities:**
  - **Contract-First Authority (`contracts`):** Single source of truth for OpenAPI, AsyncAPI, JSON Schema, generated SDKs, and consumer-driven contract tests.
  - **Modular Core + Async Workers (`registry`):** Modular monolith covering consent catalogue, notices, grants, receipts, safeguards, rights, and tenancy, paired with separately deployable revocation propagation workers.
- **Tech Stack:** OpenAPI, AsyncAPI, JSON Schema, Java, Gradle, OCPI, Contract Testing.

### Product 2.2: Automotive Diagnostics & Driver Experience Products
- **Public Components:** [`tesla-can-mod`](https://github.com/COPUR/tesla-can-mod) · [`tesla-fsd-can-mod`](https://github.com/COPUR/tesla-fsd-can-mod) · [`tesla-open-can-mod`](https://github.com/COPUR/tesla-open-can-mod)
- **Private / In-Design Products:** `tesla-can-explorer-testing-only` *(offline CAN bench simulator & TDD rewrite engine)*, `PreFlight_PDI` *(iOS/Android delivery inspection app)*, and **EV Geek Stats** *(official Tesla Fleet Telemetry iPhone companion with Türkiye weather/wind integration and 50 km / route-based CPO discovery)*.

---

## Suite 3: On-Prem AI Governance & Agentic Engineering

### Product 3.1: Jeff — Self-Hosted AI Tool-Call Firewall
- **Public Components:** [`jeff`](https://github.com/COPUR/jeff) · [`ai-governance-framework`](https://github.com/COPUR/ai-governance-framework) · [`architecture-as-code`](https://github.com/COPUR/architecture-as-code) · [`common-cloud-controls`](https://github.com/COPUR/common-cloud-controls)
- **Target Market:** Enterprises deploying AI coding assistants under strict data-residency and cost-control mandates.
- **Business Problem Solved:** Prevents unauthorized or risky agent tool executions via `PreToolUse` hooks without relying on external paid classification APIs.
- **Enterprise Capabilities:** Self-hosted implementation of TypeSafe's `jev` System One API powered by `GLiFormer` (400M parameters), escalating uncertain classifications to a local Qwen model (LM Studio) before human-in-the-loop fallback.
- **Tech Stack:** Python, `uv`, GLiFormer (400M), LM Studio (local Qwen).

### Product 3.2: TOGAF & Scrum Multi-Agent Delivery Framework
- **Product Capabilities:** Organizes AI engineering skills into umbrella summaries and vertical implementation skills, backed by a six-role enterprise squad (Business, Data, Application, Technology Architects, Program Manager, Quality Engineer).

---

## Suite 4: Serverless Content & Operational Intelligence

### Product 4.1: Multi-Tenant Serverless News & Observability Platform
- **Private Components:** `daily-ev-news-serverless-go`, `daily-ev-news-agent`, `daily-news-agent`, `dashboard-service`
- **Target Market:** Digital publishing and event-driven SaaS teams.
- **Enterprise Capabilities:** ADR-governed Go/AWS Serverless multi-tenant architecture with idempotent workflow replay protection, paired with Node.js 20+ local-first agents and an independently deployable Prisma/Docker dashboard microservice.
- **Tech Stack:** Go, AWS Serverless, Node.js 20+, Prisma, Docker.
