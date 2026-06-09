# Cheatsheet: DevOps and Platform Engineering

> Quick reference for the most-used commands, patterns, and concepts across the entire topic.

---

## Table of Contents

- [Linux and Shell](#linux-and-shell)
- [Docker](#docker)
- [Kubernetes (kubectl)](#kubernetes-kubectl)
- [Helm](#helm)
- [Terraform](#terraform)
- [GitHub Actions](#github-actions)
- [ArgoCD](#argocd)
- [Prometheus / Grafana](#prometheus--grafana)
- [DORA Metrics Reference](#dora-metrics-reference)

---

## Linux and Shell

```bash
# Process management
ps aux                          # list all processes
kill -9 <pid>                   # force kill process
systemctl status <service>      # check service status
systemctl restart <service>     # restart a service
journalctl -u <service> -f      # follow service logs

# Filesystem
df -h                           # disk usage by filesystem
du -sh <dir>                    # size of directory
lsof -i :<port>                 # what's listening on a port
find / -name "*.log" -mtime -1  # files modified in last day

# Bash scripting essentials
set -euo pipefail               # fail fast, catch errors, unset vars
"${VAR:-default}"               # use default if VAR unset
[[ -z "$VAR" ]]                 # true if VAR is empty
[[ -f "$FILE" ]]                # true if FILE exists and is regular file
trap 'cleanup' EXIT             # run cleanup on exit

# Useful one-liners
grep -r "error" /var/log/ | tail -50          # recent errors
awk '{print $1}' file.txt | sort | uniq -c    # count occurrences
curl -sI https://example.com | head -5         # check HTTP headers
```

---

## Docker

```bash
# Build and run
docker build -t myapp:v1.0 .
docker build -t myapp:v1.0 --no-cache .
docker run -d -p 8080:8080 --name myapp myapp:v1.0
docker run -it --rm myapp:v1.0 /bin/sh         # debug shell

# Registry
docker tag myapp:v1.0 registry.example.com/myapp:v1.0
docker push registry.example.com/myapp:v1.0
docker pull registry.example.com/myapp:v1.0

# Inspection and cleanup
docker ps                                       # running containers
docker ps -a                                    # all containers
docker logs myapp -f                            # follow logs
docker exec -it myapp /bin/sh                  # shell into running container
docker inspect myapp                            # full container metadata
docker image prune -f                           # remove dangling images
docker system prune --volumes -f               # nuclear cleanup

# Docker Compose
docker compose up -d                            # start detached
docker compose down                             # stop and remove
docker compose logs -f                          # follow all logs
docker compose ps                               # service status
```

### Minimal Production Dockerfile Pattern

```dockerfile
# Stage 1: build
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app/server ./cmd/server

# Stage 2: run
FROM gcr.io/distroless/static:nonroot
COPY --from=builder /app/server /server
EXPOSE 8080
USER nonroot:nonroot
ENTRYPOINT ["/server"]
```

---

## Kubernetes (kubectl)

```bash
# Context and namespace
kubectl config get-contexts
kubectl config use-context <name>
kubectl config set-context --current --namespace=<ns>

# Core operations
kubectl get pods -n <ns> -o wide
kubectl describe pod <pod> -n <ns>
kubectl logs <pod> -c <container> -f
kubectl exec -it <pod> -n <ns> -- /bin/sh
kubectl apply -f manifest.yaml
kubectl delete -f manifest.yaml
kubectl get events --sort-by='.lastTimestamp' -n <ns>

# Deployments
kubectl rollout status deployment/<name>
kubectl rollout history deployment/<name>
kubectl rollout undo deployment/<name>
kubectl set image deployment/<name> <container>=<image>:tag

# Debugging
kubectl port-forward svc/<name> 8080:80
kubectl run debug --rm -it --image=busybox -- /bin/sh
kubectl top pods -n <ns>
kubectl top nodes

# RBAC
kubectl auth can-i create pods --as=system:serviceaccount:<ns>:<sa>
kubectl get rolebindings -n <ns> -o wide
```

### Common Manifest Patterns

```yaml
# Deployment with probes and resource limits
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:v1.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
        readinessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 20
```

---

## Helm

```bash
helm repo add stable https://charts.helm.sh/stable
helm repo update
helm search repo <keyword>
helm install <release> <chart> -n <ns> --create-namespace
helm install <release> <chart> -f values.yaml
helm upgrade <release> <chart> -f values.yaml
helm rollback <release> <revision>
helm list -A
helm uninstall <release> -n <ns>
helm template <release> <chart> -f values.yaml > rendered.yaml
```

---

## Terraform

```bash
terraform init                       # download providers and modules
terraform fmt                        # format code
terraform validate                   # validate syntax
terraform plan -out=tfplan           # preview changes, save plan
terraform apply tfplan               # apply saved plan
terraform destroy                    # destroy all resources
terraform state list                 # list tracked resources
terraform state show <resource>      # inspect resource state
terraform import <resource> <id>     # import existing resource
terraform output                     # show output values
```

### Module Pattern

```hcl
# modules/vpc/main.tf
variable "cidr_block" {
  type        = string
  description = "CIDR block for the VPC"
}

resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true

  tags = {
    Name = "main-vpc"
  }
}

output "vpc_id" {
  value = aws_vpc.main.id
}

# Root main.tf calling the module
module "vpc" {
  source     = "./modules/vpc"
  cidr_block = "10.0.0.0/16"
}
```

---

## GitHub Actions

### Basic Workflow Pattern

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: make test

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: ${{ github.event_name == 'push' }}
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
```

---

## ArgoCD

```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# CLI login
argocd login <server> --username admin --password <pass>

# App management
argocd app create myapp \
  --repo https://github.com/org/gitops-config \
  --path apps/myapp \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace production
argocd app sync myapp
argocd app status myapp
argocd app rollback myapp <revision>
```

### Application Manifest

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/gitops-config
    targetRevision: HEAD
    path: apps/myapp
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

---

## Prometheus / Grafana

### PromQL Essentials

```promql
# Request rate (5m window)
rate(http_requests_total[5m])

# Error rate percentage
sum(rate(http_requests_total{status=~"5.."}[5m])) /
sum(rate(http_requests_total[5m])) * 100

# 99th percentile latency
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# SLO burn rate (fast burn, 1h window)
sum(rate(http_requests_total{status=~"5.."}[1h])) /
sum(rate(http_requests_total[1h])) > bool (14.4 * 0.001)
```

### PrometheusRule for Alerting

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: myapp-alerts
spec:
  groups:
  - name: myapp.rules
    rules:
    - alert: HighErrorRate
      expr: |
        sum(rate(http_requests_total{status=~"5.."}[5m])) /
        sum(rate(http_requests_total[5m])) > 0.01
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Error rate above 1% for 5 minutes"
```

---

## DORA Metrics Reference

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| **Deployment Frequency** | Multiple/day | 1/day–1/week | 1/week–1/month | < 1/month |
| **Lead Time for Changes** | < 1 hour | 1 day–1 week | 1 week–1 month | > 6 months |
| **Change Failure Rate** | 0–15% | 0–15% | 0–15% | 0–15% |
| **MTTR** | < 1 hour | < 1 day | 1 day–1 week | > 6 months |

> [!NOTE]
> The Change Failure Rate ranges appear identical across tiers in the original DORA research — the differentiating factor is the absolute CFR combined with the combination of all four metrics together.
