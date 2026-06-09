# Module 12: Capstone Project — Build a Complete Internal Developer Platform

[← Module 11: Security and Compliance](../11_security-and-compliance/) | [Topic Home](../../README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Expert-red)
![Time](https://img.shields.io/badge/time-30--50h-orange)

> Design and implement a complete Internal Developer Platform for an engineering team of 20–50 engineers. This capstone synthesizes every module in the topic into a real, working artifact.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Brief](#project-brief)
4. [Milestones](#milestones)
5. [Acceptance Criteria](#acceptance-criteria)
6. [Getting Unstuck](#getting-unstuck)
7. [Evaluation Rubric](#evaluation-rubric)
8. [Cross-Links](#cross-links)

---

## Overview

This is the capstone project for the DevOps and Platform Engineering topic. You will design, build, and document a complete **Internal Developer Platform (IDP)** that a real team could use to develop, deploy, and operate software.

This is not a tutorial. There is no single correct solution. You are acting as a Platform Engineer building a product for real developer customers. Your decisions will have tradeoffs, and you must justify them.

> [!IMPORTANT]
> The goal of this capstone is for **you to build it.** The help sections below exist so you can unblock yourself when stuck, not so you can copy-paste a solution. The platform you build should reflect your understanding of the problem, your design decisions, and your ability to integrate what you have learned. Reviewers will ask you to explain every component.

---

## Prerequisites

Completion of all preceding modules in this topic (01–11), or equivalent professional experience with each topic area.

---

## Project Brief

### Context

You are joining "NovaCorp" as the founding Platform Engineer. NovaCorp is a B2B SaaS company with:
- 20 engineers across 5 teams (3–5 engineers each)
- Teams own services independently but deploy to shared Kubernetes clusters
- Current state: each team has its own CI/CD setup (inconsistent), no service catalog, no centralized observability, secrets stored in Kubernetes Secrets (base64-encoded in Git), no standardized deployment process
- Current pain points: "How do I deploy a new service?" takes 2 days of copying from other repos; nobody knows who owns what; incident MTTR is high because monitoring is inconsistent

### Your Mission

Design and implement a Platform that addresses NovaCorp's pain points. At minimum, the platform must provide:

1. **Service scaffolding** — one command creates a new service with CI/CD, Kubernetes manifests, observability, and catalog registration
2. **GitOps-based deployment** — all deployments flow through Git; no manual `kubectl apply` in production
3. **Centralized observability** — Prometheus + Grafana stack; every scaffolded service gets a default dashboard and alerts
4. **Secrets management** — no secrets in Git; engineers request secrets via self-service
5. **Service catalog** — every service is registered; engineers can find owners, docs, and runbooks
6. **Security baseline** — every deployed service passes a minimum security bar (no critical CVEs, signed images, resource limits set)

---

## Milestones

Work through these milestones in order. Each one produces a working artifact.

### Milestone 1: Foundation Infrastructure

Set up the core infrastructure that everything else will run on.

- [ ] Deploy a Kubernetes cluster (local: kind/minikube, or cloud: EKS/GKE/AKS free tier)
- [ ] Configure namespace structure and RBAC: `platform-system`, `monitoring`, `production`, `staging`, per-team namespaces
- [ ] Deploy cert-manager for TLS certificate management
- [ ] Deploy an Ingress controller (nginx-ingress or Traefik)
- [ ] Set up a container registry (GitHub Container Registry or self-hosted Harbor)
- [ ] Document the cluster architecture in an Architecture Decision Record (ADR)

**Checkpoint:** A new namespace can be created with correct RBAC in under 5 minutes. All platform components have TLS certificates.

---

### Milestone 2: CI/CD Foundation

Build the standardized CI/CD pipeline that all teams will use.

- [ ] Create a GitHub Actions reusable workflow (or GitLab CI template) for the standard build-test-scan-push pipeline
- [ ] The pipeline must: run tests, build a multi-stage Docker image, scan with Trivy (fail on CRITICAL), push to registry tagged with commit SHA, sign the image with Cosign
- [ ] Generate an SBOM and attach it to the image in the registry
- [ ] Write documentation: "How do I set up CI/CD for my service?" (2 pages, max)

**Checkpoint:** A new repository can be connected to the pipeline in 15 minutes. The pipeline fails if a critical CVE is introduced.

---

### Milestone 3: GitOps Deployment

Connect CI to Kubernetes deployment via GitOps.

- [ ] Deploy ArgoCD or Flux in the cluster
- [ ] Create a `gitops-config` repository with the folder structure for multiple environments (dev, staging, production)
- [ ] Configure automated sync for dev/staging; manual approval required for production
- [ ] Deploy a sample application using the GitOps pipeline end-to-end: commit → CI builds image → updates image tag in gitops-config → ArgoCD deploys
- [ ] Test rollback: revert a commit in gitops-config and verify the old version is restored

**Checkpoint:** A code change deploys to staging automatically in under 5 minutes. Production deployment requires an explicit approval step.

---

### Milestone 4: Observability Stack

Deploy centralized monitoring and define service SLOs.

- [ ] Deploy kube-prometheus-stack (Prometheus Operator + Grafana + Alertmanager)
- [ ] Create a default Grafana dashboard template (RED method: Rate/Errors/Duration) that every scaffolded service gets automatically
- [ ] Define SLOs for the platform itself: availability > 99.5%, scaffolding template success rate > 95%
- [ ] Configure multi-window burn rate alerting for the platform SLOs
- [ ] Set up PagerDuty or equivalent on-call integration (or document the intended integration)
- [ ] Deploy the OpenTelemetry Collector for distributed tracing

**Checkpoint:** Every service in the cluster has a default Grafana dashboard. An error rate spike triggers an alert within 5 minutes.

---

### Milestone 5: Service Catalog and Scaffolding

Build the self-service layer — the heart of the IDP.

- [ ] Deploy Backstage with the Kubernetes, GitHub, and Catalog plugins
- [ ] Write a software template that scaffolds a new service: creates a repository, configures CI/CD, creates Kubernetes namespaces and RBAC, registers in catalog, creates a default Grafana dashboard
- [ ] Configure TechDocs so every service can publish documentation from its repository
- [ ] Set up the Tech Radar with at least 10 technology entries reflecting NovaCorp's actual choices
- [ ] Register all platform components themselves in the Backstage catalog (Backstage, ArgoCD, Prometheus, Grafana)

**Checkpoint:** A new engineer can scaffold a service, deploy it to staging, and see its dashboard in Grafana in under 30 minutes using only the IDP.

---

### Milestone 6: Secrets Management

Replace insecure secret handling with Vault.

- [ ] Deploy HashiCorp Vault in Kubernetes using the Vault Operator or Helm chart
- [ ] Configure Kubernetes authentication for Vault
- [ ] Deploy External Secrets Operator to sync Vault secrets to Kubernetes Secrets
- [ ] Write the self-service workflow: how an engineer requests a secret, how Vault is configured, and how the secret appears in the application
- [ ] Update the scaffolding template to configure Vault access for new services by default

**Checkpoint:** A service can access a database password from Vault without the password appearing in any Git repository.

---

### Milestone 7: Security Baseline

Enforce security policy across all workloads.

- [ ] Deploy OPA Gatekeeper with constraint templates for: required labels, resource limits required, container image must be signed (from your registry), no privileged containers, no host network
- [ ] Run Trivy on all existing cluster workloads and produce a report
- [ ] Remediate any critical findings in platform-owned workloads
- [ ] Add image signature verification to the admission pipeline

**Checkpoint:** A Pod without resource limits is rejected by Gatekeeper. An unsigned image from an external registry is blocked.

---

### Milestone 8: Documentation and Runbooks

A platform that is not documented is not a product.

- [ ] Write a "Getting Started" guide for new engineers: from zero to deployed in 30 minutes
- [ ] Write a runbook for each critical platform component: what to do when ArgoCD is down, Prometheus is OOMKilled, Backstage is unreachable
- [ ] Write Architecture Decision Records (ADRs) for your three most significant technical decisions
- [ ] Create a "Platform SLAs" document: what uptime does the platform guarantee, what is the response SLA for a Backstage issue, when is the on-call engineer paged

**Checkpoint:** Another engineer can use the Getting Started guide without asking any questions. All runbooks are in Backstage TechDocs.

---

## Acceptance Criteria

Your IDP is complete when all of the following are true:

| Criteria | How to verify |
|----------|--------------|
| New service scaffold works end-to-end | Run the Backstage template; service is deployed to staging |
| All deployments use GitOps | No `kubectl apply` commands in any pipeline; everything flows through ArgoCD/Flux |
| Every service has observability | Default Grafana dashboard and Prometheus alerts exist for every service |
| Secrets are managed by Vault | No secrets in Git; all secrets in Vault with audit logging |
| Security baseline enforced | Gatekeeper rejects unsigned images and pods without resource limits |
| Platform is self-documenting | Backstage catalog shows all services, owners, docs, and runbooks |
| Platform has its own SLOs | Prometheus monitors platform component availability |
| DORA metrics baseline established | You can measure deployment frequency and lead time for the platform itself |

---

## Getting Unstuck

> [!TIP]
> If you are stuck, try these in order: (1) read the relevant module in this topic, (2) check the official documentation for the specific tool, (3) search the CNCF Slack for your error message, (4) use the staged hints below.

<details>
<summary>Hint: Backstage scaffolding template is failing</summary>

Backstage template debugging tips:
- Check the Backstage backend logs: `kubectl logs -n backstage deployment/backstage`
- Test the GitHub token has the required permissions: `read:org`, `repo`, `write:packages`
- Validate your `template.yaml` against the Backstage schema using the built-in editor
- Start with a simpler template (just create a repo) and add steps incrementally
- Review: [Backstage Software Templates documentation](https://backstage.io/docs/features/software-templates/)

</details>

<details>
<summary>Hint: ArgoCD is not syncing</summary>

ArgoCD sync troubleshooting:
- Check the Application status: `argocd app get <name>` or the ArgoCD UI
- Common issues: SSH key not added to GitHub repo, Kustomize version mismatch, YAML syntax errors
- Enable debug logging: `kubectl -n argocd patch configmap argocd-cm -p '{"data":{"server.log.level":"debug"}}'`
- For webhook-based sync: verify the GitHub webhook is configured in the repo settings
- Review: Module 09, ArgoCD section; [ArgoCD Troubleshooting Guide](https://argo-cd.readthedocs.io/en/stable/operator-manual/troubleshooting/)

</details>

<details>
<summary>Hint: Vault authentication is failing from Kubernetes</summary>

Vault + Kubernetes auth troubleshooting:
- Verify the service account token reviewer JWT is correctly configured
- Check the role matches the service account name and namespace exactly (case-sensitive)
- Test auth manually: `vault write auth/kubernetes/login role=<role> jwt=<token>`
- Common issue: Vault is configured with an internal cluster address but the JWT contains an external issuer URL
- Review: Module 11, Vault section; [Vault Kubernetes Auth documentation](https://developer.hashicorp.com/vault/docs/auth/kubernetes)

</details>

<details>
<summary>Hint: Gatekeeper is blocking everything</summary>

OPA Gatekeeper troubleshooting:
- Start constraints in `dryrun` enforcement mode to see violations without blocking
- Check violations: `kubectl describe constraint <constraint-name>`
- Gatekeeper audit runs periodically — new resources are checked immediately but existing ones are audited on a schedule
- Exemption: add `admission.gatekeeper.sh/ignore: "true"` label to namespace to exclude it
- Review: Module 11, OPA section; [Gatekeeper documentation](https://open-policy-agent.github.io/gatekeeper/website/docs/)

</details>

---

## Evaluation Rubric

| Category | Weight | Criteria |
|----------|--------|---------|
| **Functionality** | 30% | Does the end-to-end flow work? New service → deployed to production |
| **Security** | 20% | Secrets in Vault, image signing enforced, Gatekeeper policies active |
| **Observability** | 15% | SLOs defined, dashboards exist, alerts fire correctly |
| **Design Decisions** | 20% | ADRs present, tradeoffs articulated, alternatives considered |
| **Documentation** | 15% | Getting Started guide works; runbooks are actionable; Backstage catalog is current |

A passing capstone achieves ≥70% across all categories. An outstanding capstone achieves ≥90% and includes something beyond the milestones (e.g., a custom Backstage plugin, a chaos engineering exercise, or a cost analysis of the infrastructure).

---

## Cross-Links

- [[devops-platform-engineering/modules/10_platform-apis-and-idp]] — Backstage architecture and configuration details
- [[devops-platform-engineering/modules/09_gitops-and-delivery]] — ArgoCD/Flux setup and GitOps repository structure
- [[devops-platform-engineering/modules/11_security-and-compliance]] — Vault, Cosign, Trivy, and OPA/Gatekeeper integration
- [[devops-platform-engineering/modules/08_observability]] — Prometheus, Grafana, SLO configuration
- [[networks]] — Ingress, TLS, and DNS configuration for platform services
