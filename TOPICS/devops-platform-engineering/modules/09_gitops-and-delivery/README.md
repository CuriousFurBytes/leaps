# Module 09: GitOps and Delivery

[← Module 08: Observability](../08_observability/) | [Topic Home](../../README.md) | [Next → Module 10: Platform APIs and IDP](../10_platform-apis-and-idp/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-orange)
![Time](https://img.shields.io/badge/time-8--12h-orange)

> GitOps makes Git the single source of truth for both application code and infrastructure state. This module covers ArgoCD, Flux, progressive delivery with Argo Rollouts, canary and blue-green deployments, and feature flags integration.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Key Concepts](#key-concepts)
6. [Examples](#examples)
7. [Common Pitfalls](#common-pitfalls)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

---

## Overview

> [!NOTE]
> **This module is a stub.** Full content will be added in a future update.

GitOps is not just "use Git for infrastructure." It is a specific operational model: the desired state of the entire system is declared in Git, and an operator continuously reconciles the live system toward that state. The consequence is that `kubectl apply` by hand becomes an anti-pattern — all changes flow through Git, making every change auditable, reversible, and consistent.

Progressive delivery extends continuous deployment: instead of deploying to all users simultaneously, you route a small percentage of traffic to the new version, observe its behavior, and gradually increase traffic or roll back automatically based on metrics.

---

## Prerequisites

- Module 04: Kubernetes Fundamentals — all K8s objects, `kubectl`, RBAC
- Module 06: CI/CD Pipelines — understanding what CI produces (container images tagged with commit SHA)
- Module 08: Observability — Prometheus metrics are required for automated canary analysis

---

## Objectives

By the end of this module, you will be able to:

1. Explain the GitOps model and how it differs from push-based continuous deployment
2. Install and configure ArgoCD to manage Kubernetes deployments from a Git repository
3. Configure automated sync, self-healing, and pruning in ArgoCD
4. Implement a multi-environment GitOps structure (dev → staging → production promotion)
5. Implement canary deployments using Argo Rollouts with automated Prometheus-based analysis
6. Configure blue-green deployments and understand the tradeoffs vs. canary
7. Integrate feature flags with progressive delivery for production experimentation

---

## Theory

> [!NOTE]
> Full theory content coming soon.

### GitOps Principles

The four principles of GitOps (from OpenGitOps):

1. **Declarative** — the desired state is expressed declaratively
2. **Versioned and immutable** — desired state is stored in a version control system
3. **Pulled automatically** — software agents automatically pull the desired state
4. **Continuously reconciled** — agents continuously observe actual system state and attempt to apply the desired state

```bash
# Traditional push-based CD (anti-pattern with GitOps)
# CI pipeline runs kubectl apply directly:
git push → CI runs → kubectl apply -f k8s/ → deployed

# GitOps pull-based model:
git push → CI builds image, updates image tag in gitops-config repo
         → ArgoCD detects change in gitops-config repo
         → ArgoCD reconciles cluster toward new desired state
```

### ArgoCD Application

```yaml
# ArgoCD Application: declares what to deploy from where
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payment-api
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io  # delete K8s resources when app is deleted
spec:
  project: production-apps

  source:
    repoURL: https://github.com/myorg/gitops-config
    targetRevision: HEAD
    path: apps/payment-api/production
    # For Helm charts:
    # helm:
    #   valueFiles:
    #     - values-production.yaml

  destination:
    server: https://kubernetes.default.svc
    namespace: production

  syncPolicy:
    automated:
      prune: true      # delete resources removed from Git
      selfHeal: true   # revert manual kubectl changes
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### Multi-Environment GitOps Structure

```
gitops-config/
├── apps/
│   ├── payment-api/
│   │   ├── base/          # shared Kubernetes manifests
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   ├── dev/
│   │   │   └── kustomization.yaml   # patch: 1 replica, dev image tag
│   │   ├── staging/
│   │   │   └── kustomization.yaml   # patch: 2 replicas, staging image tag
│   │   └── production/
│   │       └── kustomization.yaml   # patch: 5 replicas, production image tag
```

```yaml
# apps/payment-api/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../base
patches:
  - patch: |-
      - op: replace
        path: /spec/replicas
        value: 5
    target:
      kind: Deployment
      name: payment-api
images:
  - name: myregistry/payment-api
    newTag: "abc1234"     # CI updates this field via `kustomize edit set image`
```

### Argo Rollouts: Progressive Delivery

```yaml
# Rollout: replaces Deployment for progressive delivery
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: payment-api
spec:
  replicas: 10
  strategy:
    canary:
      # Traffic routing: send 10% to canary, rest to stable
      canaryService: payment-api-canary
      stableService: payment-api-stable
      trafficRouting:
        nginx:
          stableIngress: payment-api-ingress

      steps:
        - setWeight: 10         # 10% traffic to canary
        - pause: {duration: 5m} # wait and observe
        - analysis:             # automated canary analysis
            templates:
              - templateName: error-rate-check
        - setWeight: 50
        - pause: {duration: 10m}
        - setWeight: 100

  selector:
    matchLabels:
      app: payment-api
  template:
    metadata:
      labels:
        app: payment-api
    spec:
      containers:
      - name: payment-api
        image: myregistry/payment-api:abc1234
```

```yaml
# AnalysisTemplate: automated pass/fail based on Prometheus metrics
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: error-rate-check
spec:
  metrics:
  - name: error-rate
    interval: 1m
    successCondition: result[0] < 0.01    # fail if error rate > 1%
    failureLimit: 3
    provider:
      prometheus:
        address: http://prometheus:9090
        query: |
          sum(rate(http_requests_total{app="payment-api",status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total{app="payment-api"}[5m]))
```

---

## Key Concepts

**Reconciliation Loop** — ArgoCD and Flux continuously compare the desired state (Git) to the actual state (cluster). When they differ, the operator takes action to bring the cluster in sync. This loop makes GitOps self-healing.

**Kustomize** — a Kubernetes native configuration management tool that allows you to customize YAML manifests without templating. It uses patches, overlays, and generators. Ideal for the base/overlay pattern in multi-environment GitOps.

**Canary Deployment** — a progressive delivery strategy where a small percentage of traffic is routed to the new version. If metrics remain healthy, traffic shifts gradually toward 100%. If metrics degrade, the rollout is aborted and traffic shifts back to the stable version.

**Blue-Green Deployment** — maintaining two identical environments (blue = current, green = new). Traffic switches instantly from blue to green. Rollback is instant (switch back to blue), but resource costs are doubled during the switch.

---

## Examples

> Full examples coming soon. Will include: setting up ArgoCD with ApplicationSets for multiple environments, a Flux multi-tenant setup, automated canary analysis with Argo Rollouts and Prometheus, and integrating LaunchDarkly feature flags with Argo Rollouts.

---

## Common Pitfalls

> Full pitfalls section coming soon. Key pitfalls: mixing push and pull deployment models (breaks audit trail), using the same repository for application code and GitOps config (permission separation concerns), `selfHeal: true` reverting legitimate manual fixes during incidents, canary analysis period too short to detect latent failures, and blue-green with stateful services (database migrations during the switch).

---

## Cross-Links

- [[devops-platform-engineering/modules/06_cicd-pipelines]] — CI pipeline produces the image tag that triggers the GitOps deploy
- [[devops-platform-engineering/modules/08_observability]] — Prometheus metrics power automated canary analysis in Argo Rollouts
- [[feature-flags-monitoring]] — feature flags are complementary to GitOps; flags control feature visibility without requiring a new deployment

---

## Summary

- GitOps declares desired state in Git; operators (ArgoCD, Flux) continuously reconcile the live system toward that state
- All cluster changes flow through Git: auditable, reversible, consistent across environments
- ArgoCD Application resources declare what to deploy from which Git path; automated sync handles updates
- Multi-environment GitOps uses Kustomize overlays or Helm value files to customize per environment
- Argo Rollouts enables canary deployments with automated metric-based analysis and automatic rollback
- Blue-green deployments trade resource cost for instant rollback capability
