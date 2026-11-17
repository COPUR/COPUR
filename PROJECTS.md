# Enterprise Product & Architecture Catalog

Canonical breakdown of `COPUR`'s **4 Executive Domains and 10 Product Suites**, generated deterministically from [`catalog/portfolio-catalog.json`](./catalog/portfolio-catalog.json).

---

## Domain 1: Agentic AI-Driven Enterprise Architecture & Governance

> Turns non-deterministic LLMs/SLMs into governed, auditable enterprise architecture and engineering capacity via Agent = Model + Harness and local policy firewalls.

### Suite 1: Agentive Enterprise Architecture, Governance & Cloud Controls
- **Maturity Tier:** `Governed Private Enterprise Baseline`
- **Sponsor / Governance Scope:** Enterprise Architecture & AI Governance
- **Target Market:** Tier-1 Financial Institutions, Enterprise Architecture Boards (EAB)
- **Business Problem Solved:** Enables safe, auditable AI-assisted enterprise architecture and microservice scaffolding under CBUAE 3/2025 data residency and PCI-DSS v4 compliance constraints.
- **Value Proposition:** Autonomous TOGAF ADM & BDAT multi-agent architecture platforms where governance and domain developer agents emit schema/Zod-validated JSON inside deterministic Java/TypeScript harnesses.
- **Enterprise Capabilities:**
  - **The Deterministic Sandwich (Agent = Model + Harness):** LLMs produce only schema/Zod-validated JSON; deterministic Spring Boot or Node.js/TypeScript harnesses execute every side effect.
  - **Zero-Trust Agentic Gateway & Multi-Protocol Standards:** DPoP-authenticated agent gateway, streaming DLP via Security SLMs, W3C Trace Context, and public AI governance/protocol baselines (ADK, MCP, A2A).
- **Tech Stack:** Java / Spring Boot, TypeScript, TOGAF ADM / BDAT, DPoP, MCP / A2A / ADK, Architecture-as-Code
- **Applied Standards:** Deterministic Sandwich, Contract-First Governance, Zero-Trust & Residency
- **Canonical Public Repositories:** [`ai-governance-framework`](https://github.com/COPUR/ai-governance-framework) · [`architecture-as-code`](https://github.com/COPUR/architecture-as-code) · [`common-cloud-controls`](https://github.com/COPUR/common-cloud-controls) · [`ai-agent-protocols`](https://github.com/COPUR/ai-agent-protocols)
- **Cross-Referenced Public Repositories:** [`fintechbankx-governance-architecture-enablement-adr-runbooks`](https://github.com/COPUR/fintechbankx-governance-architecture-enablement-adr-runbooks) *(via Suite 6)*
- **Private Enterprise Components:** `EA-Agentive-Platform-v3` *(Private)*, `X_Bank-Agentive-Architecture-Framework` *(Private)*, `AgentiveArchitectureFW_v3` *(Private)*, `redbank-agentive-framework` *(Private)*, `redbank-agentive-enterprise-architecture` *(Private)*, `fintechbankx-governance-architecture-enablement-enterprise-architecture` *(Private)*
- **Proof & Verification:**
  - [Contracts & Spec — AI Governance Framework Baseline](https://github.com/COPUR/ai-governance-framework#readme): Public financial AI governance repository anchoring controls referenced by Suite 1.
  - [C4 Architecture Brief — Deterministic Sandwich C4 Brief](./briefs/suite-01-agentive-ea.md): Redacted C4 overview of Agent = Model + Harness across private EA frameworks.

### Suite 2: Jeff & Book-to-Skill — On-Prem AI Tool-Call Firewall & Knowledge Synthesis
- **Maturity Tier:** `Runnable K8s / CLI Demo`
- **Sponsor / Governance Scope:** On-Premise AI Control Plane & Knowledge Engineering
- **Target Market:** Security-Sensitive Engineering Teams, Air-Gapped AI Environments
- **Business Problem Solved:** Eliminates external data egress and third-party API dependency when enforcing deterministic tool-call policies and codifying engineering books into structured agent skills.
- **Value Proposition:** Self-hosted AI tool-call firewall (Jeff) gating coding-agent PreToolUse hooks on-prem via GLiFormer (400M) + local Qwen escalation, paired with automated book-to-skill synthesis.
- **Enterprise Capabilities:**
  - **Zero-Egress PreToolUse Classification:** Drop-in self-hosted replacement for TypeSafe's jev System One API backed by GLiFormer (400M) and local LM Studio Qwen escalation.
  - **TOGAF & Scrum Squad Skill Synthesis:** Transforms technical books into umbrella-and-vertical agent skills supporting a six-role enterprise engineering squad.
- **Tech Stack:** Python, uv, GLiFormer (400M), LM Studio (Qwen), PreToolUse Hooks
- **Applied Standards:** Deterministic Sandwich, Air-Gapped / On-Prem AI
- **Canonical Public Repositories:** [`jeff`](https://github.com/COPUR/jeff)
- **Private Enterprise Components:** `book-to-skill` *(Private)*, `book-skills` *(Private)*
- **Proof & Verification:**
  - [Quickstart — Jeff Self-Hosted GLiFormer Quickstart](https://github.com/COPUR/jeff#readme): Public repo README, bench suite, and PreToolUse guardrail setup.

## Domain 2: Agentic Open Finance (BaaS) & Regulated Core Banking

> Combines Temporal-orchestrated Open Finance agent layers, Camunda 8.10 instant payment orchestration, modular core banking/Islamic finance, and cloud API governance.

### Suite 3: OPF — Agentive Open Finance (BaaS) Platform
- **Maturity Tier:** `Public Reference Baseline`
- **Sponsor / Governance Scope:** Agentive Open Finance & BaaS Initiative
- **Target Market:** Open Finance / BaaS Platforms, Incumbent Core Banks
- **Business Problem Solved:** Replaces brittle static adapters and rigid state machines with durable stateful intent workflows, low-latency SLM routing, and semantic cache inference bypass.
- **Value Proposition:** Acts as an Agentive Translation Layer bridging Open Finance channels and legacy core-banking constraints via Temporal-orchestrated agents, Model Cascades, and pgvector semantic caching.
- **Enterprise Capabilities:**
  - **Temporal Durable AI Workflows:** Long-running, stateful intent orchestration across V2 public reference and V3/V4 regulated enterprise baselines.
  - **Model Cascades (MoE) & pgvector Semantic Caching:** Routes simple requests to fast SLMs and uses vector intent embeddings to bypass redundant foundation-model inference.
- **Tech Stack:** Temporal.io, pgvector, Model Cascades (MoE), Java, PostgreSQL
- **Applied Standards:** Deterministic Sandwich, Zero-Trust & Residency, Air-Gapped / On-Prem AI
- **Canonical Public Repositories:** [`OPF-Agentive-Platform`](https://github.com/COPUR/OPF-Agentive-Platform)
- **Cross-Referenced Public Repositories:** [`ai-agent-protocols`](https://github.com/COPUR/ai-agent-protocols) *(via Suite 1)*
- **Private Enterprise Components:** `OPF_Agentive_Platform_V4` *(Private)*, `OPF-Agentive-Platform-V3` *(Private)*
- **Proof & Verification:**
  - [Contracts & Spec — OPF V2 Master Codex & C4 Context](https://github.com/COPUR/OPF-Agentive-Platform#readme): Public OPF architecture walkthrough, Temporal orchestration, and Model Cascades.
  - [C4 Architecture Brief — OPF Architecture & Semantic Cache Brief](./briefs/suite-03-opf-architecture.md): Summary of V2 public vs V3/V4 private Open Finance capabilities.

### Suite 4: Instant Payment Exception & BPO Orchestrator
- **Maturity Tier:** `Runnable K8s / CLI Demo`
- **Sponsor / Governance Scope:** Regulated Payment Operations Orchestration
- **Target Market:** Tier-1 Banks, PSPs, TR BKM FAST Operations
- **Business Problem Solved:** Eliminates manual handling of ambiguous instant payment exceptions (PDNG) while guaranteeing instructions are never re-submitted to the scheme.
- **Value Proposition:** Turnkey Camunda 8.10 BPMN/DMN orchestration for instant payment exceptions featuring PII-free workflow state, idempotent ledger capture, and per-provider OIDC audience isolation.
- **Enterprise Capabilities:**
  - **Zero-PII OutputVariables Guardrail:** Runtime guardrail rejects monetary amounts, IBANs, and personal data from entering Camunda process variables.
  - **Per-Provider Keycloak OIDC & Pod Security:** Enforces dedicated audience tokens per downstream provider, restricted Pod Security, default-deny NetworkPolicy, and one-command K8s install.
- **Tech Stack:** Camunda 8.10, Java 23, Gradle, Keycloak 26.7, Kubernetes / Helm, PostgreSQL 17.6
- **Applied Standards:** Contract-First Governance, Zero-Trust & Residency
- **Canonical Public Repositories:** [`demo-camunda-k8s`](https://github.com/COPUR/demo-camunda-k8s) · [`neo-fintechbankx-bpo-process-orchestration`](https://github.com/COPUR/neo-fintechbankx-bpo-process-orchestration) · [`camunda8-banking-poc`](https://github.com/COPUR/camunda8-banking-poc)
- **Proof & Verification:**
  - [Quickstart — One-Command Kubernetes Install & UML](https://github.com/COPUR/demo-camunda-k8s#h%C4%B1zl%C4%B1-ba%C5%9Flang%C4%B1%C3%A7): Runnable Camunda 8.10 + Keycloak + Java 23 hexagonal worker demo via ./install.sh.

### Suite 5: FinTechBankX Core Lending, Ledger, KYC & MasruFi
- **Maturity Tier:** `Public Reference Baseline`
- **Sponsor / Governance Scope:** Core Banking, Lending & Islamic Finance
- **Target Market:** Retail, Corporate & Islamic Participation Banks
- **Business Problem Solved:** Replaces monolithic core banking modules with bounded-context microservices and auditable Islamic finance domain engines (Istisna, Ijarah, Qard Hassan).
- **Value Proposition:** Domain-driven banking core unifying loan lifecycle management, double-entry accounts/ledger, customer KYC profiles, and Sharia-compliant financing models (MasruFi).
- **Enterprise Capabilities:**
  - **Bounded-Context Core Isolation:** Separates Loan Lifecycle, Accounts/Ledger, and KYC Core into independent, contract-governed services.
  - **MasruFi Sharia Finance Engine (Private Baseline):** Encodes Istisna, Ijarah, and Qard Hassan contracts with crypto-banking primitives via DDD and Hexagonal Architecture.
- **Tech Stack:** Java, Spring Boot, MongoDB, PostgreSQL, DDD / Hexagonal
- **Applied Standards:** Contract-First Governance, Zero-Trust & Residency
- **Canonical Public Repositories:** [`fintechbankx-lendingpayments-loan-lifecycle-core`](https://github.com/COPUR/fintechbankx-lendingpayments-loan-lifecycle-core) · [`neo-fintechbankx-corebanking-accounts-ledger-service`](https://github.com/COPUR/neo-fintechbankx-corebanking-accounts-ledger-service) · [`fintechbankx-customer-profile-kyc-core`](https://github.com/COPUR/fintechbankx-customer-profile-kyc-core)
- **Private Enterprise Components:** `enterprise-loan-management-system` *(Private)*, `MasruFi_Framework` *(Private)*
- **Proof & Verification:**
  - [Contracts & Spec — Loan Lifecycle Core Repository](https://github.com/COPUR/fintechbankx-lendingpayments-loan-lifecycle-core): Public core lending bounded-context microservice.
  - [C4 Architecture Brief — FinTechBankX Core & MasruFi Brief](./briefs/suite-05-masrufi-domain-model.md): Redacted domain summary covering MasruFi_Framework (PRIVATE) Islamic finance models.

### Suite 6: FinTechBankX Cloud Platform, IaC & API Governance
- **Maturity Tier:** `Public Reference Baseline`
- **Sponsor / Governance Scope:** Enterprise Platform & API Governance Guild
- **Target Market:** Platform Engineering Teams, API Governance Guilds
- **Business Problem Solved:** Standardizes infrastructure provisioning, security posture, event schemas, and architectural decision runbooks across dozens of banking microservices.
- **Value Proposition:** Multi-wave cloud platform backbone delivering Keycloak/LDAP IAM, Terraform IaC modules, CI/CD templates, Service Mesh security, Kafka event streaming, ADR runbooks, and OpenAPI/AsyncAPI/Schema catalogs.
- **Enterprise Capabilities:**
  - **Centralized Contract & Schema Governance:** Dedicated OpenAPI, AsyncAPI, and Schema Registry catalogs paired with Architecture Board ADR runbooks.
  - **Zero-Trust Infrastructure & Event Backbone:** Reusable Terraform modules, CI/CD templates, Service Mesh policies, Keycloak/LDAP IAM, and Kafka streaming infrastructure.
- **Tech Stack:** Terraform, Kubernetes, Keycloak / LDAP, Service Mesh, Kafka, OpenAPI / AsyncAPI
- **Applied Standards:** Contract-First Governance, Zero-Trust & Residency
- **Canonical Public Repositories:** [`fintechbankx-platform-identity-iam-keycloak-ldap`](https://github.com/COPUR/fintechbankx-platform-identity-iam-keycloak-ldap) · [`fintechbankx-platform-delivery-iac-terraform-modules`](https://github.com/COPUR/fintechbankx-platform-delivery-iac-terraform-modules) · [`fintechbankx-platform-delivery-iac-cicd-templates`](https://github.com/COPUR/fintechbankx-platform-delivery-iac-cicd-templates) · [`fintechbankx-platform-mesh-security-service-mesh`](https://github.com/COPUR/fintechbankx-platform-mesh-security-service-mesh) · [`fintechbankx-platform-event-streaming-kafka`](https://github.com/COPUR/fintechbankx-platform-event-streaming-kafka) · [`fintechbankx-governance-api-contracts-openapi-catalog`](https://github.com/COPUR/fintechbankx-governance-api-contracts-openapi-catalog) · [`fintechbankx-governance-api-contracts-asyncapi-catalog`](https://github.com/COPUR/fintechbankx-governance-api-contracts-asyncapi-catalog) · [`fintechbankx-governance-api-contracts-schema-registry`](https://github.com/COPUR/fintechbankx-governance-api-contracts-schema-registry) · [`fintechbankx-governance-architecture-enablement-adr-runbooks`](https://github.com/COPUR/fintechbankx-governance-architecture-enablement-adr-runbooks)
- **Private Enterprise Components:** `fintechbankx-platform-observability-sre-operations` *(Private)*
- **Proof & Verification:**
  - [Contracts & Spec — OpenAPI Governance Catalog](https://github.com/COPUR/fintechbankx-governance-api-contracts-openapi-catalog): Centralized OpenAPI contracts paired with AsyncAPI, Schema Registry, and ADR runbooks.

## Domain 3: EV Mobility — Consent Authority, Wallet & Telemetry

> Separately sponsored Plug & Charge (PnC) regulator consent authority and stakeholder wallet/loyalty suites alongside automotive CAN/telemetry engineering.
> **Boundary Rule:** Suite 7 (Centralized Regulator) and Suite 8 (Fintech/CPO Stakeholders) are independent, separately sponsored initiatives.

### Suite 7: Consent EV PnC — Centralized Regulator Consent Authority
- **Maturity Tier:** `Contract-First Ecosystem`
- **Sponsor / Governance Scope:** Sponsor: Centralized Regulator (Government / Neutral Trust Anchor)
- **Governance Boundary:** Neutral regulator-sponsored consent authority; strictly independent from Stakeholder Wallet PnC EV (Suite 8).
- **Target Market:** Centralized Regulator, Government / Neutral Trust Anchor
- **Business Problem Solved:** Establishes a single, vendor-neutral consent trust anchor across EV roaming participants governed by verifiable contracts.
- **Value Proposition:** Regulator-sponsored neutral Plug & Charge consent authority managing consent catalogues, notices, grants, receipts, safeguards, data-subject rights, decisioning, and cross-ecosystem revocation propagation.
- **Enterprise Capabilities:**
  - **Single-Source Contracts & Consumer-Driven Testkit:** Dedicated contracts repository (OpenAPI, AsyncAPI, JSON Schema) enforced by automated EV_PnC_Consent_testkit verification.
  - **Modular Monolith Core + Revocation Workers:** Isolates consent registry state, real-time decision evaluation, and asynchronous cross-ecosystem revocation propagation.
- **Tech Stack:** OpenAPI, AsyncAPI, JSON Schema, Java / Gradle, Contract Testkit
- **Applied Standards:** Contract-First Governance, Zero-Trust & Residency
- **Canonical Public Repositories:** [`EV_PnC_Consent_contracts`](https://github.com/COPUR/EV_PnC_Consent_contracts) · [`EV_PnC_Consent_registry`](https://github.com/COPUR/EV_PnC_Consent_registry) · [`EV_PnC_Consent_decision`](https://github.com/COPUR/EV_PnC_Consent_decision) · [`EV_PnC_Consent_testkit`](https://github.com/COPUR/EV_PnC_Consent_testkit) · [`EV_PnC_Consent_docs`](https://github.com/COPUR/EV_PnC_Consent_docs)
- **Proof & Verification:**
  - [Contracts & Spec — Regulator Consent OpenAPI/AsyncAPI SSOT](https://github.com/COPUR/EV_PnC_Consent_contracts#readme): Authoritative interface contracts and SDK definitions for Consent EV PnC.
  - [Testkit / Simulator — Regulator Consent Conformance Testkit](https://github.com/COPUR/EV_PnC_Consent_testkit): Consumer-driven contract testkit verifying consent registry conformance.

### Suite 8: Wallet PnC EV — Fintech & CPO Wallet + Loyalty Platform
- **Maturity Tier:** `Contract-First Ecosystem`
- **Sponsor / Governance Scope:** Sponsor: Ecosystem Stakeholders (Fintechs, CPOs, eMSPs)
- **Governance Boundary:** Commercial stakeholder-sponsored wallet & loyalty platform; strictly separate from Centralized Regulator Consent Authority (Suite 7).
- **Target Market:** Fintechs, Charge Point Operators (CPOs), eMSPs
- **Business Problem Solved:** Accelerates Fintech and CPO onboarding into Plug & Charge roaming and driver loyalty ecosystems through modular gateway, OCPI, and simulator services.
- **Value Proposition:** Stakeholder-sponsored Plug & Charge wallet platform enabling any Fintech or CPO to launch branded EV wallets with loyalty solutions, OCPI eMSP adapters, hub gateway, telemetry, and pilot analytics.
- **Enterprise Capabilities:**
  - **Hub Contracts & OCPI Roaming Adapters:** Decouples EV_PNC_hub-contracts and EV_PNC_ocpi-model from gateway, eMSP adapter, and telemetry components.
  - **End-to-End Simulator & Pilot Analytics:** Includes EV_PNC_simulator, EV_PNC_pilot-analytics, EV_PNC_infra-modules, and EV_PNC_docs for full lifecycle validation.
- **Tech Stack:** OCPI, Hub Gateway, Python, Telemetry, Simulator, Infra Modules
- **Applied Standards:** Contract-First Governance, Zero-Trust & Residency
- **Canonical Public Repositories:** [`EV_PNC_hub-gateway`](https://github.com/COPUR/EV_PNC_hub-gateway) · [`EV_PNC_hub-contracts`](https://github.com/COPUR/EV_PNC_hub-contracts) · [`EV_PNC_ocpi-emsp`](https://github.com/COPUR/EV_PNC_ocpi-emsp) · [`EV_PNC_ocpi-model`](https://github.com/COPUR/EV_PNC_ocpi-model) · [`EV_PNC_telemetry`](https://github.com/COPUR/EV_PNC_telemetry) · [`EV_PNC_pilot-analytics`](https://github.com/COPUR/EV_PNC_pilot-analytics) · [`EV_PNC_simulator`](https://github.com/COPUR/EV_PNC_simulator) · [`EV_PNC_infra-modules`](https://github.com/COPUR/EV_PNC_infra-modules) · [`EV_PNC_docs`](https://github.com/COPUR/EV_PNC_docs)
- **Proof & Verification:**
  - [Contracts & Spec — Wallet PnC Hub Contracts](https://github.com/COPUR/EV_PNC_hub-contracts): Public Fintech/CPO wallet hub contracts paired with OCPI eMSP adapters.
  - [Testkit / Simulator — Wallet PnC EV Simulator](https://github.com/COPUR/EV_PNC_simulator): Executable simulator for Fintech/CPO charging and roaming workflows.

### Suite 9: EV Telemetry, CAN & Driver Companion
- **Maturity Tier:** `Public Reference Baseline`
- **Sponsor / Governance Scope:** Automotive R&D & Driver Experience
- **Governance Boundary:** Dedicated automotive CAN bus, bench testing, and driver companion suite; decoupled from D4 Serverless News & Observability.
- **Target Market:** Automotive R&D, Vehicle Diagnostics & EV Driver Companion Apps
- **Business Problem Solved:** Supports safe offline CAN frame testing, structured EV delivery inspection, and weather-aware Fleet Telemetry charging/route planning.
- **Value Proposition:** Combines public CAN bus exploration/FSD mod tooling, Pre-Delivery Inspection mobile workflows (PreFlight_PDI), offline bench CAN simulation, and Fleet Telemetry driver intelligence (EV Geek Stats).
- **Enterprise Capabilities:**
  - **Controlled Offline CAN Bench Simulation:** Separates public CAN mod tooling from private offline bench replay and TDD rewrite verification.
  - **Delivery Inspection & Official Fleet Telemetry:** Pairs PreFlight_PDI cross-platform mobile inspection with the EV Geek Stats official Tesla Fleet Telemetry design.
- **Tech Stack:** CAN Bus, Python / pytest, iOS & Android, Prisma, Tesla Fleet Telemetry
- **Applied Standards:** Deterministic Sandwich, Zero-Trust & Residency
- **Canonical Public Repositories:** [`tesla-can-mod`](https://github.com/COPUR/tesla-can-mod) · [`tesla-fsd-can-mod`](https://github.com/COPUR/tesla-fsd-can-mod) · [`tesla-open-can-mod`](https://github.com/COPUR/tesla-open-can-mod) · [`PreFlight_PDI`](https://github.com/COPUR/PreFlight_PDI)
- **Private Enterprise Components:** `tesla-can-explorer-testing-only` *(Private)*
- **In-Design / Roadmap Concepts:** `EV Geek Stats` *(IN_DESIGN)*
- **Proof & Verification:**
  - [Quickstart — PreFlight_PDI Mobile App README](https://github.com/COPUR/PreFlight_PDI#readme): Public Tesla Delivery Companion mobile app complementing CAN tools.

## Domain 4: Serverless Content & Operational Intelligence

> ADR-governed multi-tenant Go/AWS Serverless platform, local-first Node.js 20+ agents, and an independently deployable Prisma/Docker dashboard microservice.
> **Boundary Rule:** Separated from D3_EV_MOBILITY to keep clean domain boundaries between automotive R&D and multi-tenant serverless SaaS.

### Suite 10: Multi-Tenant Serverless News & Observability Platform
- **Maturity Tier:** `Governed Private Enterprise Baseline`
- **Sponsor / Governance Scope:** Multi-Tenant Serverless SaaS Platform
- **Target Market:** Digital Publishing Platforms, Event-Driven SaaS Engineering Teams
- **Business Problem Solved:** Guarantees multi-tenant isolation and idempotent workflow execution across serverless content pipelines while keeping the dashboard microservice independently deployable.
- **Value Proposition:** ADR-governed Go/AWS Serverless multi-tenant news workflow engine with idempotent replay guards, paired with Node.js 20+ local-first agents and a public standalone Prisma/Docker dashboard microservice.
- **Enterprise Capabilities:**
  - **ADR-Governed Idempotent Serverless Workflows:** Enforces tenant scope checks and idempotency-key replay validation in Go/AWS Serverless handlers.
  - **Decoupled Dashboard Microservice:** Exposes dashboard-service (Node.js, Prisma, Docker) as a public standalone repository decoupled from private ingestion agents.
- **Tech Stack:** Go, AWS Serverless, Node.js 20+, TypeScript, Prisma, Docker
- **Applied Standards:** Deterministic Sandwich, Contract-First Governance, Zero-Trust & Residency
- **Canonical Public Repositories:** [`dashboard-service`](https://github.com/COPUR/dashboard-service)
- **Private Enterprise Components:** `daily-ev-news-serverless-go` *(Private)*, `daily-ev-news-agent` *(Private)*, `daily-news-agent` *(Private)*
- **Proof & Verification:**
  - [Contracts & Spec — Dashboard Microservice Repository](https://github.com/COPUR/dashboard-service#readme): Public standalone Prisma/Docker dashboard microservice for the news platform.
  - [C4 Architecture Brief — Serverless Multi-Tenant C4 Brief](./briefs/suite-10-serverless-c4.md): Redacted architecture overview of Go/AWS Serverless workflows and idempotency guards.

---

## Enterprise Engineering Standards Matrix

| Order | Pillar | Implementation Standard |
|---|---|---|
| 1 | **Deterministic Sandwich** | Agent = Model + Harness — LLMs produce schema-validated JSON only; deterministic code executes all side effects |
| 2 | **Contract-First Governance** | Single-source OpenAPI, AsyncAPI, and JSON Schema registries with consumer-driven contract tests |
| 3 | **Zero-Trust & Residency** | Per-provider OIDC/DPoP scoping, restricted K8s Pod Security, default-deny NetworkPolicy, CBUAE/PCI-DSS v4 alignment |
| 4 | **Air-Gapped / On-Prem AI** | Local SLM/LLM inference and policy gating (GLiFormer, local Qwen, pgvector semantic caching) with zero external egress |
