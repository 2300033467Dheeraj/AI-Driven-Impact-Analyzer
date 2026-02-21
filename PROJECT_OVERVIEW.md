# AI-Driven Impact Analyzer for Cloud-Native Systems

## Detailed Project Explanation

### What Is This Project?

This is an **AI-Driven Impact Analyzer** for **cloud-native systems**. It helps engineering and DevOps teams understand **deployment risk** and **blast radius** (which services are affected when something changes) before or after a release.

The system has three main parts:

1. **Frontend (Next.js)** – Dashboard to view risk scores, metrics, blast radius, and deployment history.
2. **Backend (FastAPI)** – APIs that compute risk, serve metrics, run ML predictions, and query the service graph.
3. **Neo4j (Graph Database)** – Stores **service dependencies** (which service calls which). Used to compute “blast radius” (downstream impact).

---

### How It Works (End-to-End)

1. **Risk score**  
   The backend combines **deployment signals** (files changed, critical service touched, dependency depth) with **live metrics** (CPU, latency, error rate). A **RandomForest ML model** (or a rule-based fallback) outputs a score 0–100 and a decision: **Approve**, **Canary**, or **Manual Approval**.

2. **Blast radius**  
   Service dependencies are stored in Neo4j (e.g. `User → Order → Payment → Notification`). When you ask “what is the blast radius of **Order**?”, the system does a **BFS traversal** from that service and returns all **downstream services** (e.g. Payment, Notification). So you see “if Order breaks, these services are impacted.”

3. **Metrics**  
   Simulated (or later real) Prometheus-style metrics (CPU, memory, latency, error rate) are used in the dashboard and as features for the risk model.

4. **GitHub webhook**  
   A push event can trigger automatic risk analysis (e.g. files changed, critical paths) so you get risk feedback in CI/CD or Slack.

---

### Core Concepts

| Concept | Meaning |
|--------|--------|
| **Risk score** | 0–100 score for a deployment. Higher = more risk. |
| **Decision** | **Approve** (low risk), **Canary** (medium), **Manual Approval** (high). |
| **Blast radius** | List of services that **depend on** or are **called by** a given service (downstream impact). |
| **Service graph** | Graph in Neo4j: nodes = services, edges = “CALLS” (e.g. Order CALLS Payment). |
| **Impact** | If service A is down or buggy, every service in A’s blast radius can be affected. |

---

## Real-Life Use Cases

### 1. **Safe Deployments (Pre-Deploy Risk Check)**

- **Problem:** Deploying to “order-service” might break checkout, payments, and notifications. Teams often discover impact only after an outage.
- **Use:** Before deploying, you run an **impact analysis** (or the system runs it via webhook). You see:
  - Risk score and decision (approve / canary / manual).
  - Blast radius: “Order service change will impact: Payment, Notification, Auth.”
- **Outcome:** You decide to do a canary, add feature flags, or schedule the deploy for low-traffic hours.

### 2. **Incident Response and On-Call**

- **Problem:** “Order service is slow.” On-call needs to know who else is affected and who might need to be paged.
- **Use:** Query blast radius for **Order**. Get: Payment, Notification, etc. Dashboards can show “Impacted services” so support and product know which user flows are at risk.
- **Outcome:** Faster, targeted communication and prioritization during incidents.

### 3. **Change Management and Compliance**

- **Problem:** Auditors or change boards ask: “What is the impact of this release?”
- **Use:** Every deployment (or major change) gets a **risk score** and **blast radius report**. You attach this to change tickets and audits.
- **Outcome:** Clear, repeatable impact documentation for compliance and change approval.

### 4. **CI/CD Gates (Pipeline Decisions)**

- **Problem:** Should this build go straight to prod, or to canary, or require manual approval?
- **Use:** In CI/CD, call **POST /analyze-deployment** (or **POST /webhook/github**) with:
  - `files_changed`, `critical_service_modified`, `dependency_depth`
- **Outcome:** Pipeline uses the returned **decision** to:
  - Auto-approve low risk.
  - Send to canary for medium risk.
  - Block and require approval for high risk.

### 5. **Architecture and Refactoring**

- **Problem:** “We want to split Order service. What depends on it?”
- **Use:** Blast radius for **Order** shows all downstream consumers. You see coupling and can plan APIs, contracts, and migration order.
- **Outcome:** Safer refactors and clearer ownership of dependent services.

### 6. **SLO and Capacity Planning**

- **Problem:** “Which services need to be resilient if Payment is under load?”
- **Use:** Blast radius of **Payment** (and others) shows the “critical path.” You prioritize SLOs and capacity for high-impact nodes.
- **Outcome:** Better placement of redundancy, caching, and scaling.

---

## Where Can It Be Used? (Industries & Scenarios)

| Industry / Scenario | How the system is used |
|--------------------|------------------------|
| **E‑commerce** | Deployments to order, payment, inventory; incident impact; canary for checkout. |
| **FinTech / Banking** | Risk gates for payment and account services; audit trail of impact for regulators. |
| **SaaS / B2B** | Safe rollout of API and backend changes; blast radius for multi-tenant core services. |
| **Media / Streaming** | Impact of changes to recommendation, playback, or billing services. |
| **Healthcare / EdTech** | Controlled releases for critical flows; documented impact for compliance. |
| **Platform / Internal tools** | Any org with many microservices and a need for “what breaks if we change X?” |

**Best fit:**  
Teams that already have (or are building) **microservices**, **service mesh**, or **API gateways**, and want **deployment risk** and **impact visibility** without building everything from scratch.

---

## What You Have in This Repo

- **Frontend:** Dashboard (risk card, gauge, metrics chart, blast radius list, deployment table), Deployments page, Services page (blast radius by service name).
- **Backend:** REST API for risk, metrics, blast radius, analyze-deployment, GitHub webhook; ML model (or heuristic); structured logging; CORS for local frontend.
- **Neo4j:** Service graph and BFS-based blast radius; optional Docker Compose service; seed script for default graph.
- **Docker:** Dockerfiles for frontend and backend; Docker Compose to run frontend + backend + Neo4j together.

---

## Summary

- **What it is:** A tool that combines **deployment context**, **live metrics**, and a **service dependency graph** to produce **risk scores**, **decisions**, and **blast radius** for cloud-native apps.
- **Real-life use:** Safer deployments, incident impact, change management, CI/CD gates, refactoring, and SLO/capacity planning.
- **Where it’s used:** Any environment with multiple services (e‑commerce, FinTech, SaaS, media, healthcare, internal platforms) that needs **impact visibility** and **deployment risk** in one place.

This project is a **working prototype** you can extend with real metrics (e.g. Prometheus), real CI/CD (e.g. GitHub Actions calling the API), and a Neo4j graph filled from your actual service mesh or API catalog.
