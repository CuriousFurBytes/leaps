# Module 05: Kubernetes Advanced

[← Module 04: Kubernetes Fundamentals](../04_kubernetes-fundamentals/) | [Topic Home](../../README.md) | [Next → Module 06: CI/CD Pipelines](../06_cicd-pipelines/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-orange)
![Time](https://img.shields.io/badge/time-10--14h-orange)

> Production Kubernetes requires going beyond the basics. This module covers autoscaling (HPA/VPA), PodDisruptionBudgets, RBAC, NetworkPolicies, admission webhooks, and the Operator pattern.

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

Running a Kubernetes cluster in development is very different from running one that serves production traffic. Production Kubernetes demands autoscaling under load, protection against accidental disruptions, least-privilege access control, network segmentation, and the ability to extend the platform with custom controllers. This module covers all of these.

---

## Prerequisites

- Module 04: Kubernetes Fundamentals — all core objects, kubectl, and the reconciliation model

---

## Objectives

By the end of this module, you will be able to:

1. Configure Horizontal Pod Autoscaler (HPA) and Vertical Pod Autoscaler (VPA) for workload autoscaling
2. Protect workloads during node maintenance using PodDisruptionBudgets (PDBs)
3. Implement least-privilege RBAC with Roles, ClusterRoles, RoleBindings, and ServiceAccounts
4. Restrict Pod-to-Pod traffic using NetworkPolicies
5. Write and deploy admission webhooks to enforce custom policies or inject configuration
6. Understand the Operator pattern and CRDs — build or deploy an existing Operator

---

## Theory

> [!NOTE]
> Full theory content coming soon.

### Horizontal Pod Autoscaler

```yaml
# HPA scales the number of Pods based on observed metrics
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: webserver-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: webserver
  minReplicas: 3
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70   # scale up when CPU > 70% average
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300   # wait 5 minutes before scaling down
```

### PodDisruptionBudget

```yaml
# PDB ensures at least 2 replicas remain available during node drains
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: webserver-pdb
  namespace: production
spec:
  minAvailable: 2          # or use maxUnavailable: 1
  selector:
    matchLabels:
      app: webserver
```

### RBAC: Least-Privilege Access

```yaml
# Role: namespaced permissions
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch"]  # read-only access to pods and logs

---
# RoleBinding: assign the role to a service account
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods-binding
  namespace: production
subjects:
- kind: ServiceAccount
  name: monitoring-agent
  namespace: monitoring
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### NetworkPolicy

```yaml
# Default deny all ingress, then selectively allow
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}          # applies to all pods in namespace
  policyTypes:
  - Ingress                # deny all ingress by default
---
# Allow ingress to the api service only from the frontend
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-api
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - port: 8080
```

### Operator Pattern

```bash
# Example: using an Operator to manage a database
# Instead of this imperative approach:
kubectl create configmap postgres-config --from-literal=POSTGRES_DB=mydb
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml
kubectl apply -f postgres-pvc.yaml

# An Operator allows this declarative approach:
kubectl apply -f - <<EOF
apiVersion: postgres-operator.crunchydata.com/v1beta1
kind: PostgresCluster
metadata:
  name: my-database
spec:
  instances:
    - name: primary
      replicas: 3
  backups:
    pgbackrest:
      repos:
        - name: repo1
          s3:
            bucket: my-backups
EOF
# The Operator creates all required resources and manages ongoing lifecycle
```

---

## Key Concepts

**Vertical Pod Autoscaler (VPA)** — automatically adjusts the CPU and memory requests/limits of Pods based on historical usage. Unlike HPA (which adds/removes Pods), VPA resizes individual Pods. Useful for workloads that cannot be horizontally scaled.

**Admission Webhook** — an HTTP callback that the Kubernetes API server calls for every matching API request. Mutating webhooks modify requests (e.g., inject sidecars); validating webhooks can reject invalid requests (e.g., Pods without resource limits). Used by Istio (sidecar injection), OPA Gatekeeper (policy), and cert-manager (secret injection).

**Custom Resource Definition (CRD)** — extends the Kubernetes API with new resource types. Once installed, CRDs are managed identically to built-in resources via `kubectl`. CRDs are the foundation for building Operators.

**Controller** — a loop that watches Kubernetes resources and takes action to reconcile actual state toward desired state. The Deployment controller watches Deployment objects and manages ReplicaSets. Operators implement custom controllers for domain-specific resources.

---

## Examples

> Full examples coming soon. Will include: HPA configuration with custom metrics (KEDA), building a simple Operator with controller-runtime, and configuring OPA Gatekeeper admission policies.

---

## Common Pitfalls

> Full pitfalls section coming soon. Key pitfalls: HPA without proper resource requests (autoscaler cannot make decisions), PDB blocking node drain (minAvailable too high), overly broad ClusterRole bindings, NetworkPolicy not enforced without a CNI plugin that supports it, and forgetting to handle webhook TLS in admission webhook setup.

---

## Cross-Links

- [[devops-platform-engineering/modules/04_kubernetes-fundamentals]] — all core Kubernetes objects are prerequisites
- [[devops-platform-engineering/modules/08_observability]] — HPA can use custom metrics from Prometheus via the Custom Metrics API
- [[devops-platform-engineering/modules/11_security-and-compliance]] — admission webhooks are how OPA Gatekeeper enforces security policies

---

## Summary

- HPA scales Pod count based on CPU, memory, or custom metrics; PDB prevents all replicas from being removed during maintenance
- RBAC grants least-privilege access using Roles (namespaced) and ClusterRoles (cluster-wide) bound to ServiceAccounts
- NetworkPolicies restrict Pod-to-Pod traffic at the network level — require a CNI plugin that enforces them (Calico, Cilium)
- Admission webhooks intercept API requests: mutating webhooks modify resources, validating webhooks enforce policies
- The Operator pattern encodes operational knowledge into controllers that manage CRDs — the correct abstraction for stateful applications
