# Resources: DevOps and Platform Engineering

> A curated list of verified books, websites, courses, and tools for this topic.
> Resources are grouped by phase and type. All URLs have been verified.

---

## Table of Contents

- [Books](#books)
- [Official Documentation](#official-documentation)
- [Courses and Tutorials](#courses-and-tutorials)
- [Blogs and Articles](#blogs-and-articles)
- [Tools Reference](#tools-reference)
- [Communities](#communities)

---

## Books

### Essential Reading

| Title | Author(s) | Year | Notes |
|-------|-----------|------|-------|
| Site Reliability Engineering | Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy (Google) | 2016 | Free online at sre.google — foundational for understanding reliability engineering at scale |
| The Site Reliability Workbook | Betsy Beyer et al. (Google) | 2018 | Practical companion to the SRE book; free online |
| The Phoenix Project | Gene Kim, Kevin Behr, George Spafford | 2013 | Business novel dramatizing DevOps transformation; essential cultural grounding |
| Accelerate | Nicole Forsgren, Jez Humble, Gene Kim | 2018 | The research behind DORA metrics; scientific foundation for DevOps practices |
| The DevOps Handbook | Gene Kim, Jez Humble, Patrick Debois, John Willis | 2016 | Practitioner's guide to implementing the Three Ways |

### Advanced Reading

| Title | Author(s) | Year | Notes |
|-------|-----------|------|-------|
| Kubernetes in Action | Marko Luksa | 2018 | Deep dive into Kubernetes internals; still relevant despite age |
| Terraform: Up and Running | Yevgeniy Brikman | 2022 | Best practical Terraform book; covers modules, state, and testing |
| Continuous Delivery | Jez Humble, David Farley | 2010 | The original CD book; foundational theory still applies |
| Designing Distributed Systems | Brendan Burns | 2018 | Free from Microsoft; covers patterns relevant to Kubernetes and microservices |

---

## Official Documentation

### Cloud Native Foundation

| Resource | URL | Notes |
|----------|-----|-------|
| Kubernetes Documentation | https://kubernetes.io/docs/home/ | Start here for K8s; interactive tutorials available |
| CNCF Landscape | https://landscape.cncf.io/ | Map of all cloud-native tools organized by category |
| CNCF Trail Map | https://github.com/cncf/trailmap | Recommended learning path through cloud-native technologies |

### Tools Documentation

| Tool | Documentation URL | Notes |
|------|-------------------|-------|
| Docker | https://docs.docker.com/ | Full Docker documentation including Compose |
| Terraform | https://developer.hashicorp.com/terraform/docs | HashiCorp's official Terraform docs; includes tutorials |
| GitHub Actions | https://docs.github.com/en/actions | Complete reference for GitHub Actions workflows |
| GitLab CI/CD | https://docs.gitlab.com/ee/ci/ | GitLab's CI/CD documentation |
| ArgoCD | https://argo-cd.readthedocs.io/ | ArgoCD operator and user documentation |
| Flux | https://fluxcd.io/flux/ | Flux GitOps toolkit documentation |
| Prometheus | https://prometheus.io/docs/ | Prometheus monitoring documentation |
| Grafana | https://grafana.com/docs/ | Grafana observability platform docs |
| OpenTelemetry | https://opentelemetry.io/docs/ | OTel instrumentation and collector docs |
| Backstage | https://backstage.io/docs/ | Spotify's developer portal framework |
| Vault | https://developer.hashicorp.com/vault/docs | HashiCorp Vault secrets management |
| OPA | https://www.openpolicyagent.org/docs/ | Open Policy Agent documentation |

---

## Courses and Tutorials

### Free

| Resource | Provider | Focus |
|----------|----------|-------|
| [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/) | kubernetes.io | Interactive browser-based K8s tutorial |
| [Play with Kubernetes](https://labs.play-with-k8s.com/) | Docker | Free in-browser Kubernetes environment |
| [Learn Terraform](https://developer.hashicorp.com/terraform/tutorials) | HashiCorp | Official Terraform tutorials with free sandbox |
| [GitHub Actions Quickstart](https://docs.github.com/en/actions/quickstart) | GitHub | Get a workflow running in 5 minutes |
| [Google SRE Book](https://sre.google/sre-book/table-of-contents/) | Google | Full book free online |

### Paid (Widely Recommended)

| Resource | Provider | Notes |
|----------|----------|-------|
| Certified Kubernetes Administrator (CKA) prep courses | Linux Foundation / KodeKloud / A Cloud Guru | Multiple providers; CKA is the industry-standard K8s certification |
| HashiCorp Certified: Terraform Associate prep | HashiCorp / A Cloud Guru | Official certification path |

---

## Blogs and Articles

### Seminal Articles

| Title | Author | Notes |
|-------|--------|-------|
| "10+ Deploys Per Day: Dev and Ops Cooperation at Flickr" | John Allspaw & Paul Hammond | The 2009 Velocity talk that sparked DevOps; slides available online |
| "What is GitOps?" | Alexis Richardson (Weaveworks) | The original GitOps definition |
| "The SRE model of operations" | Ben Treynor Sloss (Google) | Google's description of how SRE works |

### Ongoing Blogs

| Blog | Focus |
|------|-------|
| https://engineering.atspotify.com/ | Spotify's engineering blog; Squad model, Backstage, reliability |
| https://netflixtechblog.com/ | Netflix Tech Blog; chaos engineering, deployment, scale |
| https://aws.amazon.com/blogs/devops/ | AWS DevOps blog |
| https://cloud.google.com/blog/products/devops-sre | Google Cloud DevOps and SRE blog |

---

## Tools Reference

### Core Toolchain

| Category | Tool | Purpose |
|----------|------|---------|
| Container runtime | Docker | Build and run containers |
| Container orchestration | Kubernetes | Deploy and manage containers at scale |
| CI/CD | GitHub Actions, GitLab CI | Pipeline automation |
| IaC | Terraform, Pulumi | Infrastructure provisioning |
| GitOps | ArgoCD, Flux | Continuous delivery via Git |
| Observability | Prometheus + Grafana + OTel | Metrics, dashboards, tracing |
| Developer portal | Backstage | Internal Developer Platform catalog |
| Secrets | HashiCorp Vault | Secrets management |
| Policy | OPA / Gatekeeper | Policy as code |
| Security scanning | Trivy, Cosign | Vulnerability scanning, image signing |

### Local Development Tools

| Tool | Purpose |
|------|---------|
| minikube | Local Kubernetes cluster |
| kind (Kubernetes in Docker) | Lightweight local K8s for CI/CD testing |
| k3s / k3d | Lightweight K8s distribution |
| kubectx / kubens | Quick context/namespace switching |
| k9s | Terminal UI for Kubernetes |
| helm | Kubernetes package manager |
| tilt | Local development loop for Kubernetes |

---

## Communities

| Community | Platform | Focus |
|-----------|----------|-------|
| CNCF Slack | Slack (cloud-native.slack.com) | All CNCF projects; find channels per tool |
| DevOps subreddit | Reddit (r/devops) | Practitioner discussions |
| Platform Engineering community | platformengineering.org | IDP-focused community |
| KubeCon talks | YouTube (CNCF channel) | Annual conference talks; free recordings |
| DevOpsDays | devopsdays.org | Local and virtual DevOps events worldwide |
