# Enterprise Product & Architecture Catalog

Detailed product breakdown of the `@COPUR` portfolio, structured by product suite, business problem, enterprise guarantees, and underlying technical components.

---

## Suite 1: FinTechBankX — Core Banking, Open Finance & Process Orchestration

### Product 1.1: Instant Payment Exception & BPO Orchestrator
- **Components:** [`demo-camunda-k8s`](https://github.com/COPUR/demo-camunda-k8s) · [`neo-fintechbankx-bpo-process-orchestration`](https://github.com/COPUR/neo-fintechbankx-bpo-process-orchestration)
- **Target Market:** Banks and PSPs operating instant payment rails (TR BKM FAST) and multi-jurisdiction payment operations.
- **Business Problem Solved:** Eliminates manual, error-prone handling of ambiguous/pending instant payment exceptions (`PDNG`) while guaranteeing that instructions are never re-submitted to the scheme.
- **Enterprise Capabilities:**
  - **Deterministic Orchestration:** Camunda 8.10 BPMN/DMN workflows with automated retry/wait timers (`PT30S`, `PT2M`, `PT10M`), message correlation (`Msg_SchemeStatusReported`), and tiered Tasklist escalation (`ops` → `supervisor`).
  - **Zero-PII Process State:** Runtime `OutputVariables` guardrail strictly rejects amounts, IBANs, and personal data from entering the workflow engine.
  - **Zero-Trust Service Security:** Keycloak 26.7 OIDC with per-provider scoped `client_credentials` tokens (e.g., `aud-svc-psg-tr`, `aud-svc-acc-accounts-ledger`, `aud-svc-pay-initiation-settlement`, `aud-svc-ntf`), restricted Pod Security, and default-deny Kubernetes `NetworkPolicy`.
  - **Turnkey Delivery:** Single-command (`./install.sh`) local Kubernetes deployment with PostgreSQL 17.6, Camunda Hub, Operate, Tasklist, and four HTTPS/JWT simulated providers.
- **Tech Stack:** Camunda 8.10, Java 23, Gradle, Spring Boot, Kubernetes, Helm, Keycloak, PostgreSQL, Docker.

### Product 1.2: Enterprise Lending, Payments & Open Finance Core
- **Components:** [`enterprise-loan-management-system`](https://github.com/COPUR/enterprise-loan-management-system) · [`enhanced-loan-management`](https://github.com/COPUR/enhanced-loan-management) · [`LoanPayment_POC`](https://github.com/COPUR/LoanPayment_POC) · [`orangeTeamPOC`](https://github.com/COPUR/orangeTeamPOC) · [`banking-transformation-report`](https://github.com/COPUR/banking-transformation-report)
- **Target Market:** Retail/corporate banks and fintechs modernizing legacy lending and launching Open Finance ecosystems.
- **Business Problem Solved:** Provides a modular, domain-aligned foundation replacing monolithic core banking modules with independently deployable, contract-governed capabilities.
- **Enterprise Capabilities:**
  - **Full Domain Coverage:** Loan lifecycle core, payment orchestration (initiation/settlement, request-to-pay, recurring mandates, bulk), customer KYC, risk decisioning, compliance evidence, and Open Finance (consent auth, retail/corporate financial data, open data product catalogs).
  - **Platform & Governance Backbone:** Multi-wave architecture (`wave0`–`phase5`) integrating Terraform IaC modules, CI/CD templates, Service Mesh security, Kafka event streaming, SRE observability, and centralized OpenAPI/AsyncAPI/Schema Registry catalogs.
- **Tech Stack:** Java, Spring Boot, Spring Cloud Gateway, Kafka, Redis, MongoDB, Keycloak/LDAP, Terraform, Kubernetes, Helm.

### Product 1.3: MasruFi — Sharia-Compliant Digital Finance Engine
- **Component:** [`MasruFi_Framework`](https://github.com/COPUR/MasruFi_Framework)
- **Target Market:** Islamic banks, participation finance institutions, and Sharia-compliant fintech platforms.
- **Business Problem Solved:** Encodes complex Sharia-compliant financing contracts into testable, auditable software models.
- **Enterprise Capabilities:**
  - Supports **Istisna**, **Ijarah**, and **Qard Hassan** financing models integrated with crypto-banking concepts.
  - Enforces clean Hexagonal & DDD boundaries between contract rules and external infrastructure.
- **Tech Stack:** Java, Gradle, JS test suites, DDD, Hexagonal Architecture.

---

## Suite 2: EV Mobility — Plug & Charge Consent & Telemetry

### Product 2.1: EV PnC Consent Governance Platform
- **Components:** [`EV_PnC_Consent_contracts`](https://github.com/COPUR/EV_PnC_Consent_contracts) · [`EV_PnC_Consent_registry`](https://github.com/COPUR/EV_PnC_Consent_registry)
- **Target Market:** EV roaming hubs, CPOs, eMSPs, and mobility service providers.
- **Business Problem Solved:** Establishes a neutral, verifiable consent source of truth for Plug & Charge roaming with rapid revocation propagation across ecosystem participants.
- **Enterprise Capabilities:**
  - **Contract-First Authority (`contracts`):** Single source of truth for OpenAPI, AsyncAPI, JSON Schema, generated SDKs, and consumer-driven contract tests.
  - **Modular Core + Async Workers (`registry`):** Modular monolith covering consent catalogue, notices, grants, receipts, safeguards, rights, and tenancy, paired with separately deployable revocation propagation workers.
- **Tech Stack:** OpenAPI, AsyncAPI, JSON Schema, Java, Gradle, Contract Testing.

### Product 2.2: PreFlight PDI — EV Delivery Companion
- **Component:** [`PreFlight_PDI`](https://github.com/COPUR/PreFlight_PDI)
- **Target Market:** EV owners and automotive delivery operations.
- **Business Problem Solved:** Standardizes vehicle Pre-Delivery Inspection (PDI) with guided mobile workflows and structured defect capture.
- **Tech Stack:** Cross-platform mobile (iOS & Android), Prisma backend, Docker/Infra.

### Product 2.3: Tesla CAN Explorer (Controlled Bench Simulator)
- **Component:** [`tesla-can-explorer-testing-only`](https://github.com/COPUR/tesla-can-explorer-testing-only)
- **Target Market:** Automotive R&D and diagnostic tooling teams.
- **Business Problem Solved:** Enables safe, offline CAN bus replay, simulation, and TDD rewrite verification strictly within controlled bench environments.
- **Tech Stack:** Python, `pytest`, Firmware tooling, Makefile.

### Product 2.4: EV Geek Stats *(In Design)*
- **Target Market:** EV drivers in Türkiye seeking climate-aware charging & route intelligence.
- **Product Capabilities:** Uses the official Tesla Fleet API / Telemetry stream combined with Türkiye weather/wind data to list charging stations within 50 km or along the active route, surface CPO pricing/availability, trigger weather-aware battery conditioning when needed, and hand off selected stations to vehicle navigation.

---

## Suite 3: On-Prem AI Governance & Agentic Engineering

### Product 3.1: Jeff — Self-Hosted AI Tool-Call Firewall
- **Component:** [`jeff`](https://github.com/COPUR/jeff)
- **Target Market:** Enterprises deploying AI coding assistants (e.g., Claude Code) under strict data-residency and cost-control mandates.
- **Business Problem Solved:** Prevents unauthorized or risky agent tool executions via `PreToolUse` hooks without relying on external paid classification APIs.
- **Enterprise Capabilities:**
  - Self-hosted implementation of TypeSafe's `jev` System One API powered by `GLiFormer` (400M parameters).
  - Tiered escalation to a local Qwen model (LM Studio) for ambiguous decisions before falling back to human approval.
- **Tech Stack:** Python, `uv`, GLiFormer (400M), LM Studio (local Qwen).

### Product 3.2: TOGAF & Scrum Multi-Agent Delivery Framework
- **Product Capabilities:** Organizes AI engineering skills into umbrella summaries and vertical implementation skills, backed by a six-role enterprise squad (Business, Data, Application, Technology Architects, Program Manager, Quality Engineer).

---

## Suite 4: Serverless Content & Operational Intelligence

### Product 4.1: Multi-Tenant Serverless News & Observability Platform
- **Components:** [`daily-ev-news-serverless-go`](https://github.com/COPUR/daily-ev-news-serverless-go) · [`daily-ev-news-agent`](https://github.com/COPUR/daily-ev-news-agent) · [`daily-news-agent`](https://github.com/COPUR/daily-news-agent) · [`dashboard-service`](https://github.com/COPUR/dashboard-service)
- **Target Market:** Digital publishing and event-driven SaaS teams.
- **Enterprise Capabilities:**
  - **Go/AWS Serverless Core:** Multi-tenant architecture governed by ADRs, automated contract checks, and idempotent workflow replay protection.
  - **Modular Ingestion & Dashboard:** Local-first Node.js 20+ API/agent runtime paired with an independently deployable Prisma/Docker dashboard microservice.
- **Tech Stack:** Go, AWS Serverless, Node.js 20+, Prisma, Docker.
