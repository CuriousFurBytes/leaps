# Module 11: Security and Compliance

[← Module 10: Platform APIs and IDP](../10_platform-apis-and-idp/) | [Topic Home](../../README.md) | [Next → Module 12: Capstone Project](../12_capstone-project/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Expert-red)
![Time](https://img.shields.io/badge/time-10--14h-orange)

> Security is not a checkbox at the end of the delivery pipeline — it is woven throughout. This module covers supply chain security (SBOM, Cosign), vulnerability scanning (Trivy), policy enforcement (OPA/Gatekeeper), and secrets management (HashiCorp Vault).

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

The SolarWinds supply chain attack (2020), the Log4Shell vulnerability (2021), and the XZ Utils backdoor (2024) demonstrated that software supply chain security is not theoretical. Modern DevOps security practice — often called DevSecOps — integrates security validation into every stage of the delivery pipeline: scanning dependencies, signing container images, generating SBOMs, enforcing admission policies, and managing secrets with proper rotation and auditing.

---

## Prerequisites

- Module 03: Containers — image building and registries
- Module 05: Kubernetes Advanced — admission webhooks are how OPA Gatekeeper enforces policies
- Module 06: CI/CD Pipelines — security scanning runs in CI pipelines

---

## Objectives

By the end of this module, you will be able to:

1. Generate and validate Software Bill of Materials (SBOM) for container images
2. Sign container images with Cosign and verify signatures in Kubernetes admission
3. Scan container images and filesystems for CVEs using Trivy
4. Enforce policy as code using Open Policy Agent (OPA) and Gatekeeper
5. Write Rego policies to enforce Kubernetes resource standards
6. Deploy and configure HashiCorp Vault for dynamic secrets management
7. Integrate Vault with Kubernetes using the Vault Agent Injector or External Secrets Operator

---

## Theory

> [!NOTE]
> Full theory content coming soon.

### Software Supply Chain Security

The software supply chain is the chain of components, tools, and processes involved in building software. Each link is a potential attack surface:

```
Developer workstation → Source code → Dependencies → Build system
    → Container registry → Kubernetes cluster → Production
```

**SBOM (Software Bill of Materials)** — a machine-readable inventory of all components in a software artifact. Required by US Executive Order 14028 (2021) for software sold to the US government. Tools: Syft (generates), Grype (scans SBOM for CVEs).

**Cosign** — signs container images using keyless signing (OIDC-based, no long-lived keys) or with traditional key pairs. Signatures are stored in OCI registries alongside the image.

```bash
# Generate SBOM for a container image
syft myapp:v1.0 -o spdx-json > myapp-sbom.spdx.json

# Sign the image with Cosign (keyless, using OIDC token from GitHub Actions)
cosign sign --yes myregistry/myapp@sha256:abc123

# Verify the signature
cosign verify \
    --certificate-identity-regexp "https://github.com/myorg/myapp" \
    --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
    myregistry/myapp:v1.0
```

### Trivy: Vulnerability Scanning

```bash
# Scan a container image
trivy image myapp:v1.0

# Output in SARIF format for GitHub Security tab
trivy image --format sarif --output trivy-results.sarif myapp:v1.0

# Scan a local filesystem (for IaC misconfiguration)
trivy fs --scanners config .

# Scan a Kubernetes cluster
trivy k8s --report summary cluster

# Fail CI on CRITICAL vulnerabilities only
trivy image --exit-code 1 --severity CRITICAL myapp:v1.0
```

### OPA/Gatekeeper: Policy as Code

```bash
# Install Gatekeeper in the cluster
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/master/deploy/gatekeeper.yaml

# Define a constraint template (Rego policy)
```

```yaml
# ConstraintTemplate: defines the policy logic
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("Missing required labels: %v", [missing])
        }
---
# Constraint: enforce the policy for Deployments in production
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: require-team-label
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
    namespaces: ["production"]
  parameters:
    labels: ["team", "env", "service"]
```

### HashiCorp Vault: Secrets Management

```bash
# Vault provides dynamic secrets, secret rotation, and fine-grained access control

# Enable Kubernetes authentication
vault auth enable kubernetes
vault write auth/kubernetes/config \
    kubernetes_host="https://kubernetes.default.svc:443" \
    token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"

# Create a policy for the payment-api service
vault policy write payment-api - <<EOF
path "secret/data/payment-api/*" {
  capabilities = ["read"]
}
path "database/creds/payment-api-role" {
  capabilities = ["read"]
}
EOF

# Bind the policy to a Kubernetes service account
vault write auth/kubernetes/role/payment-api \
    bound_service_account_names=payment-api \
    bound_service_account_namespaces=production \
    policies=payment-api \
    ttl=1h

# Dynamic database credentials (Vault creates a temporary DB user)
vault secrets enable database
vault write database/config/postgresql \
    plugin_name=postgresql-database-plugin \
    connection_url="postgresql://{{username}}:{{password}}@postgres:5432/mydb" \
    allowed_roles="payment-api-role" \
    username="vault-admin" \
    password="${DB_ADMIN_PASSWORD}"
```

```yaml
# Pod with Vault Agent sidecar for automatic secret injection
apiVersion: v1
kind: Pod
metadata:
  annotations:
    vault.hashicorp.com/agent-inject: "true"
    vault.hashicorp.com/role: "payment-api"
    vault.hashicorp.com/agent-inject-secret-config: "secret/data/payment-api/config"
    vault.hashicorp.com/agent-inject-template-config: |
      {{- with secret "secret/data/payment-api/config" -}}
      export API_KEY="{{ .Data.data.api_key }}"
      export STRIPE_SECRET="{{ .Data.data.stripe_secret }}"
      {{- end -}}
spec:
  serviceAccountName: payment-api
  containers:
  - name: payment-api
    image: myregistry/payment-api:v1.0
    command: ["/bin/sh", "-c"]
    args: ["source /vault/secrets/config && /app/server"]
```

---

## Key Concepts

**SBOM (Software Bill of Materials)** — a machine-readable list of all components (open source libraries, system packages, programming language packages) in a software artifact. Enables automated vulnerability tracking and license compliance.

**Supply Chain Attack** — an attack that targets the tools, dependencies, or build systems used to create software rather than the software itself. SolarWinds (2020), Log4Shell (2021), and XZ Utils (2024) are major examples.

**Dynamic Secrets** — Vault generates secrets on-demand with a short TTL (time-to-live) instead of storing long-lived credentials. A database dynamic secret creates a real database user that expires after 1 hour — far more secure than a shared password.

**OPA Rego** — the policy language used by Open Policy Agent. Rego is a declarative language for expressing rules over JSON/YAML data structures. Gatekeeper uses Rego policies enforced via Kubernetes admission webhooks.

---

## Examples

> Full examples coming soon. Will include: a complete supply chain security pipeline (SBOM → Cosign signing → Trivy scanning → policy enforcement), Vault Agent with External Secrets Operator, Gatekeeper policies for CIS Kubernetes benchmark, and SLSA (Supply Chain Levels for Software Artifacts) framework implementation.

---

## Common Pitfalls

> Full pitfalls section coming soon. Key pitfalls: treating security scanning as informational rather than a pipeline gate, using long-lived credentials instead of dynamic secrets, storing secrets in ConfigMaps (not encrypted at rest by default), not rotating Vault root tokens, OPA policies in dry-run mode forever (never enforcing), and ignoring CVEs in base OS packages.

---

## Cross-Links

- [[devops-platform-engineering/modules/05_kubernetes-advanced]] — admission webhooks are the mechanism by which OPA Gatekeeper enforces policies
- [[devops-platform-engineering/modules/06_cicd-pipelines]] — security scanning runs in CI pipelines; Cosign signing happens in CD
- [[devops-platform-engineering/modules/10_platform-apis-and-idp]] — the IDP's scaffolding should configure Vault integration and security scanning by default in golden paths

---

## Summary

- Supply chain security means validating every link from source code to production: SBOM, image signing, vulnerability scanning, and policy enforcement
- SBOMs (generated by Syft) provide a machine-readable inventory of all components; Grype and Trivy scan SBOMs and images for CVEs
- Cosign signs container images using keyless (OIDC) or key-based signing; Gatekeeper can enforce that only signed images are admitted
- OPA Gatekeeper enforces Rego policies as Kubernetes admission webhooks: validate configuration, block non-compliant resources
- HashiCorp Vault provides dynamic secrets (created on-demand, expired automatically), fine-grained access control, and full audit logging
- Security must be integrated as pipeline gates, not optional warnings — fail on CRITICAL CVEs, require signed images
