# DevOps and Platform Engineering

![Status](https://img.shields.io/badge/status-in--progress-yellow)
![Modules Completed](https://img.shields.io/badge/modules-0%2F12-lightgrey)
![Last Updated](https://img.shields.io/badge/updated-2026--06--09-blue)

> A comprehensive curriculum covering the culture, tooling, and engineering practices that enable organizations to ship software reliably, at scale, and with high autonomy.

> [!NOTE]
> **Topic Overview**
> DevOps and Platform Engineering encompasses the cultural movements, engineering disciplines, and automation toolchains that close the gap between writing code and running it reliably in production. This topic spans from foundational philosophy and Linux fundamentals all the way to advanced Kubernetes internals, Infrastructure as Code, GitOps, and building Internal Developer Platforms.
>
> This topic is organized into progressive modules, each building on the last.
> Work through them in order unless you already have relevant prior experience —
> use the [Difficulty & Time Estimate](#difficulty--time-estimate) section and
> the [Prerequisites](#prerequisites) section to decide where to begin.

---

## Table of Contents

- [Overview](#overview)
- [Historical Context](#historical-context)
- [Real-World Applications](#real-world-applications)
- [Learning Objectives](#learning-objectives)
- [Difficulty & Time Estimate](#difficulty--time-estimate)
- [Prerequisites](#prerequisites)
- [Learning Modules](#learning-modules)
- [Progress](#progress)
- [Milestones](#milestones)
- [Test Scores](#test-scores)
- [Projects](#projects)
- [Resources](#resources)
- [Related Topics](#related-topics)
- [Quick Reference](#quick-reference)
- [Learning Journal](#learning-journal)
- [AI Metadata](#ai-metadata)

---

## Overview

DevOps emerged at the intersection of software development and IT operations, born from the frustration of the "wall of confusion" — the organizational barrier where development teams threw code over the fence to operations teams who were responsible for keeping systems stable. The result was adversarial dynamics, slow releases, and high failure rates. DevOps is the movement that dismantles this wall.

At its core, DevOps is a cultural and organizational philosophy, not a job title or a toolset. It draws heavily from Lean manufacturing principles (eliminate waste, optimize flow), Agile development (iterative delivery, fast feedback), and Systems Thinking (understand the whole, not just the parts). The practical outcome is a software delivery system capable of deploying multiple times per day with high confidence and fast recovery when things go wrong.

Site Reliability Engineering (SRE) is Google's concrete implementation of DevOps principles: engineering operations work the same way software is engineered, with SLOs (Service Level Objectives), error budgets, toil reduction, and automation. Platform Engineering is the 2020s evolution: rather than embedding SRE practices into every team, build a self-service Internal Developer Platform (IDP) that gives all engineers golden paths to production — standardized, paved roads that encode best practices into tooling so teams don't have to reinvent them.

### Why It Matters

The DORA (DevOps Research and Assessment) research program — run by Dr. Nicole Forsgren, Jez Humble, and Gene Kim — has produced the most rigorous empirical evidence for which engineering practices actually drive organizational performance. Elite performers deploy code hundreds of times more frequently than low performers, with dramatically shorter lead times and faster recovery from incidents. These are not marginal differences — they represent the gap between industry leaders and laggards.

Understanding DevOps and Platform Engineering matters because:

- It underpins **every production software system** — a skill used directly in cloud infrastructure, microservices, SaaS platforms, and any organization deploying software continuously
- It develops the mental model for **systems thinking and feedback loops** — transferable to incident management, architecture decisions, and organizational design
- Proficiency is expected in roles such as **DevOps Engineer, Platform Engineer, SRE, Infrastructure Engineer, Cloud Architect**, and increasingly in senior software engineers of all kinds

### Key Features of This Topic

- **Culture-first approach** — begins with the philosophy and organizational dynamics before introducing tools, because tools without culture change nothing
- **Full-stack toolchain coverage** — Linux, containers, Kubernetes, CI/CD, IaC, observability, GitOps, and Platform Engineering
- **DORA-aligned** — all practices traced back to empirical research on what actually improves delivery performance
- **Capstone project** — build a complete Internal Developer Platform demonstrating mastery of all major topics

---

## Historical Context

The conditions that produced DevOps were created by the convergence of Agile development, virtualization, and cloud computing in the mid-2000s.

In 2001, the **Agile Manifesto** was signed by 17 software practitioners. Agile introduced iterative development, working software over documentation, and responding to change — but it addressed only the development half of the delivery equation. Operations teams still ran rigid, change-averse processes measured in weeks or months.

By 2009, the tension was visible. John Allspaw and Paul Hammond's landmark Velocity Conference talk "10+ Deploys Per Day: Dev and Ops Cooperation at Flickr" demonstrated that high-frequency deployment and operational stability were not opposites — they were complementary when teams shared responsibility. That same year, Patrick Debois organized the first **DevOpsDays** in Ghent, Belgium, coining the "DevOps" portmanteau.

The theoretical framework crystallized with **The Phoenix Project** by Gene Kim, Kevin Behr, and George Spafford — a business novel that dramatized DevOps transformation. The "Three Ways" framework from this work — Flow, Feedback, and Continuous Improvement — remains the foundational model.

Google had been doing SRE since 2003, when Benjamin Treynor Sloss built the first SRE team. But the world learned about it when Google published the **Site Reliability Engineering** book in 2016, revealing how the company operationalized software reliability at planetary scale.

Containerization changed infrastructure in 2013 when Docker released its open-source container runtime, making Linux namespaces and cgroups accessible to ordinary developers. In 2014, Google open-sourced **Kubernetes**, the orchestration system it had built from its internal Borg system. Kubernetes became the de facto cloud-native compute substrate within years.

**GitOps** was coined by Alexis Richardson of Weaveworks in 2017, defining a model where Git is the single source of truth for both application code and infrastructure state. ArgoCD and Flux became its primary implementations.

The 2020s brought **Platform Engineering** as a formalization of the insight that self-service platforms reduce cognitive load on application teams. The concept of the **Internal Developer Platform (IDP)** moved from industry-leading practice to mainstream expectation.

### Timeline

| Year | Event |
|------|-------|
| 2001 | Agile Manifesto signed; iterative development enters mainstream |
| 2003 | Google founds first SRE team under Benjamin Treynor Sloss |
| 2009 | Allspaw & Hammond's "10+ Deploys Per Day" at Velocity; first DevOpsDays in Ghent |
| 2013 | Docker 0.1 released; The Phoenix Project published |
| 2014 | Google open-sources Kubernetes at DockerCon |
| 2016 | Google SRE book published; The DevOps Handbook published |
| 2017 | GitOps coined by Alexis Richardson; ArgoCD and Flux created |
| 2018 | DORA joins Google Cloud; Accelerate published by Forsgren, Humble & Kim |
| 2019 | Backstage open-sourced by Spotify as internal developer portal |
| 2020s | Platform Engineering emerges as dedicated discipline; IDPs go mainstream |

---

## Real-World Applications

DevOps and Platform Engineering practices are actively used across every major technology organization:

- **Google SRE** — the originator of the SRE model, running services at billions of QPS using error budgets, toil elimination, and progressive rollouts
- **Netflix Chaos Engineering** — the Simian Army (including Chaos Monkey) intentionally terminates production services to discover and fix reliability weaknesses before they cause real outages
- **Spotify Squad Model** — organized development around autonomous squads with clear domain ownership, demonstrating how Conway's Law applies to platform design
- **Shopify Deploys** — ships code to production hundreds of times per day during peak traffic periods using feature flags, canary deployments, and automated rollbacks
- **GitHub CI/CD** — GitHub Actions runs on the same Git-based infrastructure used by millions of teams, demonstrating dogfooding at scale
- **Amazon "You Build It, You Run It"** — Amazon's organizational model of small, autonomous teams owning their services end-to-end predates the term DevOps but embodies its principles

---

## Learning Objectives

By completing this topic in full, you will be able to:

1. Explain the cultural and organizational foundations of DevOps — the Three Ways, DORA metrics, and the evolution from waterfall to Platform Engineering
2. Work confidently in Linux — filesystem navigation, process management, bash scripting, systemd, and user/permission management
3. Build, run, and secure containerized applications using Docker, and compose multi-service applications with Docker Compose
4. Deploy and operate applications on Kubernetes — managing Pods, Deployments, Services, ConfigMaps, Ingress, RBAC, and namespaces
5. Design and implement CI/CD pipelines using GitHub Actions or GitLab CI/CD with proper secrets management, environments, and approval gates
6. Write, organize, and maintain Infrastructure as Code using Terraform and understand state management, drift detection, and module design
7. Instrument applications and infrastructure with Prometheus, Grafana, and OpenTelemetry; define and monitor SLOs and SLIs; design alerting strategies
8. Implement GitOps workflows with ArgoCD or Flux, and apply progressive delivery techniques including canary deployments and blue-green releases
9. Build self-service platform capabilities using Backstage, including service catalog, scaffolding templates, and tech radar
10. Secure the software supply chain using SBOM generation, image signing (Cosign), vulnerability scanning (Trivy), and policy enforcement (OPA/Gatekeeper)
11. Design a complete Internal Developer Platform that integrates CI/CD, IaC, observability, and self-service workflows for a real engineering organization

---

## Difficulty & Time Estimate

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Intermediate → Expert |
| **Estimated Total Hours** | 120–160 hours |
| **Prerequisites** | Linux basics, programming fundamentals |
| **Recommended Pace** | 6–8 hours/week |
| **Topic Type** | Computational (shell, YAML, HCL code examples throughout) |
| **Suitable For** | Software engineers, ops engineers, cloud practitioners, technical leads |

---

## Prerequisites

Before starting this topic, you should have a working understanding of:

- Basic Linux command-line usage — specifically: navigating the filesystem, running commands, understanding file permissions (Module 02 extends this significantly)
- At least one programming language — specifically: understanding functions, control flow, and basic data structures (needed for scripting and reading configuration DSLs)
- [[networks]] — specifically: TCP/IP basics, DNS, HTTP/HTTPS, ports, and what a load balancer does (Kubernetes networking and service meshes build directly on this)

> [!TIP]
> Not sure if you're ready? Attempt Module 01 (Introduction) — it is culture-heavy and requires no tooling. Module 02 is where the technical prerequisites matter. If Linux commands feel completely foreign, spend a few hours with a basic Linux tutorial first.

---

## Learning Modules

| # | Module | Topics Covered | Difficulty | Status |
|---|--------|---------------|------------|--------|
| 01 | [Introduction to DevOps and Platform Engineering](./modules/01_introduction/) | Culture, Three Ways, DORA metrics, DevOps toolchain, Platform Engineering | Beginner | [ ] |
| 02 | [Linux and Shell](./modules/02_linux-and-shell/) | Filesystem, processes, bash scripting, systemd, cron, user management | Beginner–Intermediate | [ ] |
| 03 | [Containers](./modules/03_containers/) | Docker fundamentals, image layers, Dockerfile best practices, docker-compose, container security | Intermediate | [ ] |
| 04 | [Kubernetes Fundamentals](./modules/04_kubernetes-fundamentals/) | Pods, Deployments, Services, ConfigMaps/Secrets, Ingress, namespaces, kubectl | Intermediate | [ ] |
| 05 | [Kubernetes Advanced](./modules/05_kubernetes-advanced/) | HPA/VPA, PodDisruptionBudgets, RBAC, NetworkPolicies, admission webhooks, Operators | Advanced | [ ] |
| 06 | [CI/CD Pipelines](./modules/06_cicd-pipelines/) | GitHub Actions, GitLab CI/CD, pipeline design, artifacts, environments, approvals, secrets management | Intermediate–Advanced | [ ] |
| 07 | [Infrastructure as Code](./modules/07_infrastructure-as-code/) | Terraform providers/state/modules, Pulumi, drift detection, IaC best practices | Advanced | [ ] |
| 08 | [Observability](./modules/08_observability/) | Prometheus, Grafana, OpenTelemetry, distributed tracing, SLO/SLI/SLA, alerting strategies | Advanced | [ ] |
| 09 | [GitOps and Delivery](./modules/09_gitops-and-delivery/) | ArgoCD, Flux, progressive delivery, Argo Rollouts, canary/blue-green, feature flags integration | Advanced | [ ] |
| 10 | [Platform APIs and Internal Developer Platforms](./modules/10_platform-apis-and-idp/) | Backstage service catalog, scaffolding, tech radar, self-service workflows, platform metrics | Expert | [ ] |
| 11 | [Security and Compliance](./modules/11_security-and-compliance/) | Supply chain security (SBOM, Cosign), Trivy, OPA/Gatekeeper, secrets management (Vault) | Expert | [ ] |
| 12 | [Capstone Project](./modules/12_capstone-project/) | Design and implement a complete Internal Developer Platform | Expert | [ ] |

**Status key:** ` ` Not started · `~` In progress · `x` Complete

---

## Progress

### Overall Progress

```
[░░░░░░░░░░░░░░░░░░░░] 0 / 12 modules complete (0%)
```

_Update this bar as you complete modules. Each block = 5% of total modules._

```
Legend:  ░ = not started   ▒ = in progress   █ = complete
Example: [███████▒░░░░░░░░░░░░] 7.5 / 20 modules (37%)
```

### Point Tracker

| Category | Earned | Possible | Percentage |
|----------|--------|----------|------------|
| Module Tests | 0 | 444 | 0% |
| Exercises | 0 | 120 | 0% |
| Projects | 0 | 60 | 0% |
| Bonus | 0 | — | — |
| **Total** | **0** | **624** | **0%** |

---

## Milestones

- [ ] **First Step** — Complete Module 01 (Introduction)
- [ ] **Shell Confident** — Complete Module 02 (Linux and Shell) with ≥70%
- [ ] **Container Ready** — Complete Module 03 (Containers) with ≥70%
- [ ] **Kubernetes Operator** — Complete Modules 04 and 05 with ≥70% each
- [ ] **Pipeline Builder** — Complete Module 06 (CI/CD Pipelines) with ≥70%
- [ ] **Infrastructure Coder** — Complete Module 07 (IaC) with ≥70%
- [ ] **Halfway There** — Complete 6 of 12 modules
- [ ] **Reliability Engineer** — Complete Module 08 (Observability) with ≥80%
- [ ] **GitOps Practitioner** — Complete Module 09 with ≥70%
- [ ] **Platform Builder** — Complete Modules 10 and 11
- [ ] **Topic Complete** — All 12 modules finished
- [ ] **Elite Performer** — Capstone project evaluated and approved

---

## Test Scores

_Append a row after each test attempt. Do not overwrite previous attempts._

| Module | Date | Score | Grade | Notes |
|--------|------|-------|-------|-------|
| — | — | —/— | — | Not started |

**Grade scale:** A ≥ 90% · B ≥ 80% · C ≥ 70% · D ≥ 60% · F < 60%

---

## Projects

See [PROJECTS.md](./PROJECTS.md) for project ideas ranging from beginner to expert.

**My Projects:**

| Project Name | Difficulty | Started | Status | Link |
|-------------|------------|---------|--------|------|
| — | — | — | — | — |

---

## Resources

See [RESOURCES.md](./RESOURCES.md) for a curated and verified list of books, courses, docs, and tools.

**Top picks:**

1. [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) — Google's SRE book, free online
2. The Phoenix Project — Gene Kim et al., the DevOps origin story in novel form
3. [Kubernetes Documentation](https://kubernetes.io/docs/home/) — official docs, the best reference for K8s

---

## Related Topics

Topics that complement, extend, or are required for DevOps and Platform Engineering:

- [[networks]] — TCP/IP, DNS, HTTP, and load balancing underpin all Kubernetes networking, service meshes, and ingress design
- [[qa-testing]] — testing pipelines integrate directly with CI/CD; shift-left testing is a core DevOps practice; contract testing is critical in microservices
- [[feature-flags-monitoring]] — feature flags enable progressive delivery and are central to canary releases and A/B testing in production

See also the [ROADMAP.md](./ROADMAP.md) for how this topic fits into broader learning paths.

---

## Quick Reference

### DORA Four Key Metrics

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| Deployment Frequency | Multiple/day | 1/day–1/week | 1/week–1/month | < 1/month |
| Lead Time for Changes | < 1 hour | 1 day–1 week | 1 week–1 month | > 6 months |
| Change Failure Rate | 0–15% | 16–30% | 16–30% | 16–30% |
| Time to Restore Service | < 1 hour | < 1 day | 1 day–1 week | > 6 months |

### Essential kubectl Commands

```bash
kubectl get pods -n <namespace>          # list pods
kubectl describe pod <name>              # detailed pod info
kubectl logs <pod> -c <container>        # view logs
kubectl exec -it <pod> -- /bin/sh        # shell into pod
kubectl apply -f manifest.yaml           # apply config
kubectl delete -f manifest.yaml          # delete resources
kubectl rollout status deployment/<name> # check rollout
kubectl rollout undo deployment/<name>   # roll back
```

### Docker Quick Reference

```bash
docker build -t myapp:v1.0 .             # build image
docker run -p 8080:8080 myapp:v1.0       # run container
docker push registry/myapp:v1.0          # push to registry
docker compose up -d                     # start all services
docker images                            # list images
docker ps                                # list running containers
```

### Terraform Quick Reference

```bash
terraform init         # initialize providers
terraform plan         # preview changes
terraform apply        # apply changes
terraform destroy      # destroy resources
terraform state list   # list tracked resources
terraform import       # import existing resource
```

---

## Learning Journal

_Date-stamp each entry. Write honestly — confusion documented now becomes insight later._
_Newest entries at the top._

---

### 2026-06-09 — Topic Created

**What I did today:**
- Read the topic overview and ROADMAP.md
- Reviewed the module map from beginner to expert
- Started Module 01: Introduction to DevOps and Platform Engineering

**What clicked:**
- _Write one thing that made sense immediately_

**What's still unclear:**
- _Write your first open question — then add it to QUESTIONS.md_

**How I feel about this topic:**
- _Honest assessment: excited / intimidated / curious / confused / etc._

---

_Add new journal entries above this line, newest first._

---

## AI Metadata

```yaml
# Maintained by LEAPS tooling — manual edits will be overwritten on next sync
last_ai_expansion: "2026-06-09"
topic_slug: "devops-platform-engineering"
topic_name: "DevOps and Platform Engineering"
module_count: 12
modules_complete: 0
total_points_earned: 0
total_points_possible: 624
completion_percentage: 0
difficulty: "Intermediate → Expert"
estimated_hours: 120
prerequisites:
  - "linux-basics"
  - "programming-fundamentals"
  - "networks"
related_topics:
  - "networks"
  - "qa-testing"
  - "feature-flags-monitoring"
tags:
  - "devops"
  - "platform-engineering"
  - "kubernetes"
  - "ci-cd"
  - "infrastructure-as-code"
  - "sre"
  - "observability"
creator: "Patrick Debois / Community"
year_created: "2009"
```
