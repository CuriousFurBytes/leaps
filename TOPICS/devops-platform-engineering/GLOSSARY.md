# Glossary: DevOps and Platform Engineering

> Key terms and definitions for this topic. Terms appear in order of when they are typically first encountered in the learning path.

---

## Terms

### Container

A lightweight, isolated unit of execution that packages an application with all its dependencies (libraries, runtime, configuration) into a single portable artifact. Containers use Linux kernel features — **namespaces** (for isolation) and **cgroups** (for resource limits) — to provide process-level isolation without the overhead of a full virtual machine. A container is not a virtual machine: it shares the host OS kernel rather than running its own. The key innovation is that the same container image runs identically on a developer's laptop and in a production cluster.

### Orchestration

The automated management of containerized workloads across a cluster of machines — scheduling containers onto nodes, restarting failed containers, scaling replicas up or down, managing network routing, and rolling out updates without downtime. Kubernetes is the dominant container orchestration platform; predecessors include Docker Swarm and Apache Mesos. The term comes from the analogy of an orchestra conductor: individual musicians (containers) follow their parts, while the conductor (orchestrator) ensures they start on time, stay in sync, and adapt when something goes wrong.

### CI/CD (Continuous Integration / Continuous Delivery)

**Continuous Integration (CI)** is the practice of merging developer changes into a shared main branch frequently (multiple times per day), with automated build and test pipelines verifying each change immediately. It eliminates the "integration hell" of infrequent merges. **Continuous Delivery (CD)** extends this by ensuring every passing build is deployable to production — the deployment may still require a manual approval, but it is always ready. **Continuous Deployment** goes one step further: every passing build is deployed to production automatically with no manual gate. The CI/CD pipeline is the automated assembly line that makes this possible.

### IaC (Infrastructure as Code)

The practice of managing and provisioning infrastructure — servers, networks, databases, DNS records — through machine-readable configuration files (code) rather than through manual processes or interactive tools. IaC enables version control, code review, automated testing, and repeatability for infrastructure changes. Terraform (by HashiCorp) is the dominant IaC tool for cloud infrastructure; Pulumi offers an alternative using real programming languages; Ansible focuses on configuration management. The key benefit: infrastructure changes go through the same review and testing workflows as application code.

### Immutable Infrastructure

A deployment philosophy where servers or containers are never modified after they are created. Instead of patching a running server, you build a new image, test it, and swap it in. This eliminates configuration drift (the slow divergence between intended and actual state), makes rollbacks trivial (swap back to the previous image), and ensures environments are truly identical. Docker containers and Kubernetes Pods naturally encourage immutability; "snowflake servers" (unique, hand-configured servers that nobody dares touch) are the anti-pattern this philosophy replaces.

### GitOps

An operational model where Git is the single source of truth for both application code and infrastructure/configuration state. A GitOps operator (ArgoCD, Flux) continuously observes the desired state declared in Git and reconciles the live system toward it. Changes are made by opening pull requests — not by running `kubectl apply` directly. Benefits: all changes are auditable via Git history, rollbacks are `git revert`, drift is automatically corrected, and cluster state is always reproducible from the repository. Coined by Alexis Richardson of Weaveworks in 2017.

### SLO / SLI / SLA

Three related reliability concepts from the SRE model:
- **SLI (Service Level Indicator)** — a quantitative measurement of service behavior, e.g. "99th-percentile latency of HTTP requests to /api/checkout"
- **SLO (Service Level Objective)** — the target value for an SLI, e.g. "99th-percentile latency < 200ms measured over a 28-day rolling window"
- **SLA (Service Level Agreement)** — the contractual commitment to users or customers, typically slightly looser than the SLO, with defined consequences for violation

SLOs are internal engineering targets; SLAs are external business commitments. The **error budget** (1 - SLO) is how much unreliability you can consume before violating the SLO — teams spend it on risky deployments or save it as a reliability reserve.

### MTTR (Mean Time to Restore)

The average time elapsed from when an incident begins (a service degrades or goes down) to when it is fully restored. MTTR is one of the four DORA key metrics and is considered more important than MTBF (Mean Time Between Failures) in modern DevOps thinking. A low MTTR indicates fast incident response, good observability (you can find the cause quickly), and reliable rollback mechanisms. The elite DORA benchmark for MTTR is under one hour.

### DORA Metrics

Four key metrics identified by the DevOps Research and Assessment (DORA) program as the strongest predictors of software delivery performance and organizational outcomes. Defined in the book *Accelerate* (2018) by Nicole Forsgren, Jez Humble, and Gene Kim:
1. **Deployment Frequency** — how often code is deployed to production
2. **Lead Time for Changes** — time from code commit to running in production
3. **Change Failure Rate** — percentage of deployments causing a production incident
4. **Time to Restore Service** (MTTR) — time to recover from a production incident

Elite performers have high deployment frequency, short lead times, low failure rates, and fast recovery.

### Service Mesh

A dedicated infrastructure layer for handling service-to-service communication in a microservices architecture. A service mesh provides: mutual TLS (mTLS) encryption between services, traffic management (retries, timeouts, circuit breaking, traffic splitting), observability (distributed tracing, metrics, access logs), and policy enforcement — all without requiring changes to application code. Implemented via **sidecar proxies** (typically Envoy) that are injected into each Pod. Istio and Linkerd are the dominant service mesh implementations. Service meshes solve the "cross-cutting concerns" problem in distributed systems.

### Operator (Kubernetes)

A method of packaging, deploying, and managing a Kubernetes application that extends the Kubernetes API with custom domain knowledge. An Operator is a combination of a **Custom Resource Definition (CRD)** — which adds new API types to Kubernetes — and a **controller** — which watches those resources and takes action to reconcile actual state toward desired state. Operators encode operational knowledge (how to deploy, scale, backup, upgrade a particular application) into software. The Prometheus Operator, for example, lets you declare `PrometheusRule` objects instead of writing PromQL in config files. The Operator pattern was introduced by CoreOS in 2016.

### CRD (Custom Resource Definition)

A Kubernetes extension mechanism that allows you to define your own API types (resources) in the Kubernetes API server. Once a CRD is installed, you can create, read, update, and delete custom objects using `kubectl` and the Kubernetes API just like built-in types (Pods, Deployments, Services). CRDs are the foundation of the Operator pattern and enable Kubernetes to be extended for domain-specific use cases — database clusters, certificate management, service meshes, and more. For example, the cert-manager project defines `Certificate` and `Issuer` CRDs.

### Admission Webhook

A Kubernetes extensibility mechanism that intercepts API requests before they are persisted to etcd. There are two types:
- **Validating Admission Webhooks** — can reject requests that violate policy (e.g., reject a Pod that doesn't specify resource limits)
- **Mutating Admission Webhooks** — can modify requests before they are saved (e.g., inject a sidecar proxy, add default labels)

Admission webhooks are how tools like OPA/Gatekeeper enforce policy, how Istio injects Envoy sidecars, and how many operators implement their defaulting logic. They run as HTTPS endpoints that the Kubernetes API server calls on every matching request.

### RBAC (Role-Based Access Control)

A method of regulating access to Kubernetes resources based on the roles assigned to users and service accounts. Kubernetes RBAC uses four core objects:
- **Role** / **ClusterRole** — defines a set of permissions (verbs: get, list, create, delete on specific resources)
- **RoleBinding** / **ClusterRoleBinding** — grants a Role to a user, group, or service account

RBAC is the primary security mechanism for controlling who can do what in a Kubernetes cluster. Least-privilege RBAC — granting only the minimum permissions required — is a key security practice. `ClusterRole` applies cluster-wide; `Role` is namespace-scoped.

### Observability

The ability to understand the internal state of a system from its external outputs. Observability is composed of three "pillars":
- **Metrics** — numeric measurements over time (e.g., request rate, error rate, latency percentiles, CPU usage)
- **Logs** — timestamped records of discrete events (e.g., an HTTP request log, an error stack trace)
- **Traces** — records of a request's journey through a distributed system (spans linked by a trace ID)

The term originates from control theory. In modern cloud-native systems, the OpenTelemetry project provides a vendor-neutral standard for generating all three signal types. High observability enables fast MTTR by making it possible to quickly determine what failed and why.
