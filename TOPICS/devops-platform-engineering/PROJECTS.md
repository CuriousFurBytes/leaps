# Projects: DevOps and Platform Engineering

> Project ideas organized by difficulty. Each project is a real artifact a practitioner would build.
> Work through them after completing the corresponding modules.

---

## Table of Contents

- [Beginner Projects](#beginner-projects)
- [Intermediate Projects](#intermediate-projects)
- [Advanced Projects](#advanced-projects)
- [Expert Projects](#expert-projects)

---

## Beginner Projects

### Project 1: Automated System Health Reporter

**After:** Module 02 (Linux and Shell)
**Estimated time:** 3–5 hours

Write a bash script that collects system health information and generates a human-readable report. The script should gather: CPU usage, memory usage, disk usage per partition, top 5 processes by CPU, top 5 by memory, recent system log errors, and failed systemd services. Schedule it with cron to run every hour and append to a log file.

**Acceptance criteria:**
- Script runs without root on a standard Linux system
- Output is clearly formatted and readable
- Cron job confirmed working via log entries
- Script handles errors gracefully (e.g., missing commands, insufficient permissions)

---

### Project 2: Containerized Web Application

**After:** Module 03 (Containers)
**Estimated time:** 4–6 hours

Take an existing open-source web application (or write a minimal one in any language) and containerize it from scratch. Write a production-quality `Dockerfile` (multi-stage build, non-root user, health check, minimal base image). Write a `docker-compose.yml` that runs the application with a database backend. Document the build and run process.

**Acceptance criteria:**
- Dockerfile uses multi-stage build to keep the final image small
- Container runs as a non-root user
- `docker compose up` starts the full stack
- Application is accessible and functional
- `docker scan` or `trivy image` shows no critical vulnerabilities in the final image

---

## Intermediate Projects

### Project 3: Kubernetes Deployment Pipeline

**After:** Module 04 (Kubernetes Fundamentals)
**Estimated time:** 6–8 hours

Deploy the containerized application from Project 2 to a local Kubernetes cluster (minikube or kind). Create all required manifests: Deployment (with resource limits and health probes), Service, ConfigMap for configuration, a Secret for sensitive data, and an Ingress for external access. Set up proper namespace isolation.

**Acceptance criteria:**
- Application deployed to a dedicated namespace
- Deployment has readiness and liveness probes
- All configuration in ConfigMaps; sensitive data in Secrets (base64-encoded, not plain text)
- Ingress routes external traffic to the service
- `kubectl rollout` works for zero-downtime updates

---

### Project 4: GitHub Actions CI Pipeline

**After:** Module 06 (CI/CD Pipelines)
**Estimated time:** 5–7 hours

Build a complete CI pipeline for your containerized application using GitHub Actions. The pipeline should: run unit tests on every push, build and push a Docker image to GitHub Container Registry (ghcr.io), run a security scan on the image, and deploy to a staging Kubernetes cluster on merge to `main`.

**Acceptance criteria:**
- Pipeline triggers on push and pull request
- Tests must pass before image is built
- Image tagged with commit SHA and pushed to ghcr.io
- Security scan results visible in the workflow summary
- Deployment step only runs on merge to `main`
- Secrets stored in GitHub repository secrets, not hardcoded

---

## Advanced Projects

### Project 5: Terraform Infrastructure

**After:** Module 07 (Infrastructure as Code)
**Estimated time:** 8–12 hours

Write Terraform code that provisions the infrastructure for your application on a cloud provider (AWS free tier, GCP free tier, or equivalent). Create: a VPC with public and private subnets, a managed Kubernetes cluster (EKS/GKE/AKS), a container registry, and an IAM role with least-privilege permissions for the CI/CD pipeline. Organize the code into reusable modules.

**Acceptance criteria:**
- `terraform plan` produces no errors
- All resources tagged/labeled with environment, owner, and project
- State stored remotely (S3, GCS, or Terraform Cloud)
- Code organized into at least two reusable modules
- `terraform destroy` cleanly removes all resources
- No hard-coded credentials or secrets in `.tf` files

---

### Project 6: Observability Stack

**After:** Module 08 (Observability)
**Estimated time:** 8–10 hours

Deploy a full observability stack into your Kubernetes cluster: Prometheus (with Prometheus Operator), Grafana, and an OpenTelemetry Collector. Instrument your application to emit metrics and traces. Define an SLO for your application's availability and request latency. Create a Grafana dashboard that shows the SLO burn rate.

**Acceptance criteria:**
- Prometheus scraping application metrics
- Application emits traces to OTel Collector
- Grafana dashboard shows request rate, error rate, and latency percentiles
- SLO defined with clear SLI and target (e.g., 99.9% of requests < 500ms over 28 days)
- Alert rule fires when error budget is being consumed faster than baseline

---

### Project 7: GitOps Delivery

**After:** Module 09 (GitOps and Delivery)
**Estimated time:** 6–8 hours

Set up ArgoCD in your cluster and migrate your application deployments to be managed via GitOps. Create a separate `gitops-config` repository that contains all Kubernetes manifests. Configure ArgoCD to watch this repository and automatically sync changes. Implement a canary deployment using Argo Rollouts.

**Acceptance criteria:**
- ArgoCD installed and accessible via UI
- All application manifests live in the gitops-config repo
- ArgoCD auto-syncs on changes to the repo
- A `Rollout` resource implements a canary strategy (20% → 50% → 100%)
- Manual promotion through canary steps documented and tested
- Rollback demonstrated by reverting a commit in the gitops-config repo

---

## Expert Projects

### Project 8: Internal Developer Platform (Capstone)

**After:** Module 12 (Capstone Project) — See [Capstone Module](./modules/12_capstone-project/README.md) for the full specification.

**Estimated time:** 30–50 hours

Design and implement a complete Internal Developer Platform that a real engineering team could use. Full specification in the Capstone module. This project synthesizes everything from the entire topic.
