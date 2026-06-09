# Module 10: Platform APIs and Internal Developer Platforms

[← Module 09: GitOps and Delivery](../09_gitops-and-delivery/) | [Topic Home](../../README.md) | [Next → Module 11: Security and Compliance](../11_security-and-compliance/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Expert-red)
![Time](https://img.shields.io/badge/time-10--14h-orange)

> An Internal Developer Platform (IDP) is the product a Platform Engineering team builds to give application teams self-service access to everything they need to develop, deploy, and operate software. This module covers Backstage, service catalog, scaffolding, tech radar, self-service workflows, and measuring platform effectiveness.

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

An Internal Developer Platform is the product that emerges when a Platform Engineering team takes the "you are building a product for internal developers" model seriously. The IDP provides self-service access to environments, deployment pipelines, monitoring, documentation, service registration, and team tooling — all without requiring a ticket to the platform team.

Backstage, open-sourced by Spotify in 2019, is the dominant framework for building IDPs. It provides a plugin-based developer portal with a service catalog, software templates (scaffolding), tech radar, and TechDocs.

---

## Prerequisites

- Modules 04–09: All Kubernetes, CI/CD, IaC, Observability, and GitOps modules — the IDP surfaces and connects all of these
- Basic TypeScript/JavaScript knowledge is helpful for Backstage plugin development

---

## Objectives

By the end of this module, you will be able to:

1. Explain the value proposition of an IDP and how it reduces cognitive load on application teams
2. Deploy and configure Backstage with a service catalog, scaffolding templates, and TechDocs
3. Write a Backstage software template that scaffolds a new service with CI/CD, Kubernetes manifests, and monitoring
4. Register existing services in the catalog using `catalog-info.yaml`
5. Configure and maintain a tech radar to communicate platform standards and recommendations
6. Design self-service workflows that replace the most common platform team requests
7. Define and measure platform engineering metrics: DORA metrics, developer satisfaction (DevEx), platform adoption rate, and time-to-first-deploy

---

## Theory

> [!NOTE]
> Full theory content coming soon.

### What Makes an Internal Developer Platform

An IDP is not just a documentation portal or a collection of runbooks. A mature IDP provides:

| Capability | What It Replaces |
|-----------|-----------------|
| Service scaffolding | "Create a new repo and copy-paste from another service" |
| Self-service environments | "Open a ticket to request a dev/staging environment" |
| Automated pipeline setup | "Ask the DevOps team to configure CI/CD" |
| Service catalog | "Email the team to ask who owns that service" |
| Self-service observability | "Ask the SRE team to create a Grafana dashboard" |
| TechDocs | "Where is the documentation? Is it current?" |

### Backstage Service Catalog

```yaml
# catalog-info.yaml — every service registers itself in the catalog
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-api
  description: Payment processing API for the checkout flow
  annotations:
    github.com/project-slug: myorg/payment-api
    backstage.io/techdocs-ref: dir:.
    prometheus.io/alert-manager: "https://alertmanager.internal"
  tags:
    - payment
    - critical-path
    - go
  links:
    - url: https://grafana.internal/d/payment-api
      title: Grafana Dashboard
      icon: dashboard
spec:
  type: service
  lifecycle: production
  owner: group:payments-team
  system: checkout
  dependsOn:
    - component:database-service
    - resource:payments-kafka-topic
  providesApis:
    - payment-api-v2
```

### Backstage Software Template (Scaffolding)

```yaml
# template.yaml — creates a new Go microservice with everything pre-configured
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: go-microservice
  title: Go Microservice
  description: Create a new Go microservice with CI/CD, Kubernetes, and monitoring
  tags:
    - go
    - microservice
spec:
  owner: platform-team
  type: service

  parameters:
    - title: Service Information
      required: [name, description, owner]
      properties:
        name:
          title: Service Name
          type: string
          pattern: '^[a-z][a-z0-9-]*$'
        description:
          title: Description
          type: string
        owner:
          title: Owner Team
          type: string
          ui:field: OwnerPicker
        tier:
          title: Service Tier
          type: string
          enum: [critical, standard, internal]

  steps:
    - id: fetch-template
      name: Fetch Template
      action: fetch:template
      input:
        url: ./skeleton        # Git path with template files
        values:
          name: ${{ parameters.name }}
          owner: ${{ parameters.owner }}

    - id: publish
      name: Publish to GitHub
      action: publish:github
      input:
        allowedHosts: ['github.com']
        repoUrl: github.com?owner=myorg&repo=${{ parameters.name }}

    - id: register
      name: Register in Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
        catalogInfoPath: /catalog-info.yaml

    - id: create-namespace
      name: Create Kubernetes Namespace
      action: kubernetes:create-namespace
      input:
        namespace: ${{ parameters.name }}
        clusterRef: production

  output:
    links:
      - title: Repository
        url: ${{ steps.publish.output.remoteUrl }}
      - title: Catalog Entry
        url: ${{ steps.register.output.entityRef }}
```

### Platform Metrics

```bash
# Platform engineering teams should measure their own platform like a product:

# 1. DORA metrics (from the platform team's perspective)
#    - Time to create a new service (scaffolding → first deploy)
#    - Platform deployment frequency and stability

# 2. Developer Experience (DevEx) metrics
#    - Developer satisfaction score (quarterly survey)
#    - Time to first deploy for a new hire
#    - Percentage of deployments via self-service vs. ticket

# 3. Platform adoption
platform_adoption=$(
    kubectl get pods --all-namespaces -l managed-by=platform-team \
    | wc -l
)
echo "Services on platform: $platform_adoption"

# 4. Cognitive load proxy: how many runbooks are > 6 months old?
# Old runbooks signal that teams are not maintaining documentation →
# cognitive load is increasing
```

---

## Key Concepts

**Internal Developer Platform (IDP)** — a self-service layer built by a Platform Engineering team that provides application teams with the tools, workflows, and interfaces they need to develop, deploy, and operate software without requiring manual assistance from the platform team.

**Backstage** — an open-source developer portal framework created by Spotify and donated to the CNCF. Provides a plugin system, service catalog, software templates, and TechDocs integration. Deployed as a Node.js application.

**Golden Path** — the opinionated, supported, default path for common engineering tasks (creating a service, deploying to production, adding monitoring). Golden paths reduce decision fatigue and encode platform best practices.

**Tech Radar** — a visualization tool (popularized by ThoughtWorks) that categorizes technologies into rings: Adopt (recommended), Trial (promising), Assess (evaluate cautiously), Hold (avoid). Platform teams use it to communicate technology recommendations.

**Platform as a Product** — the mindset that the platform team's product is the IDP itself, with application teams as customers. This means applying product management practices: user research, feedback loops, SLOs for the platform, and measuring adoption.

---

## Examples

> Full examples coming soon. Will include: deploying Backstage with the Kubernetes plugin, writing a complete Go service template, configuring the GitHub integration, creating a Tech Radar configuration, and building a custom Backstage plugin.

---

## Common Pitfalls

> Full pitfalls section coming soon. Key pitfalls: building the IDP without talking to users (build what engineers actually need, not what the platform team thinks they need), making the golden path mandatory instead of preferred (developers will route around it), not measuring platform adoption (you cannot improve what you don't measure), and building a documentation portal instead of self-service tooling.

---

## Cross-Links

- [[devops-platform-engineering/modules/09_gitops-and-delivery]] — the IDP's scaffolding creates GitOps repositories and ArgoCD applications automatically
- [[devops-platform-engineering/modules/11_security-and-compliance]] — the IDP's golden paths should encode security best practices by default
- [[devops-platform-engineering/modules/12_capstone-project]] — the capstone project builds a complete IDP using the concepts from this module

---

## Summary

- An IDP provides self-service access to environments, CI/CD, monitoring, and documentation — replacing tickets with tooling
- Backstage is the dominant IDP framework: service catalog, software templates, TechDocs, and a plugin ecosystem
- Software templates (scaffolding) encode golden paths: one command creates a service with CI/CD, Kubernetes, monitoring, and catalog registration
- Platform teams should treat the IDP as a product: user research, feedback loops, SLOs, and adoption metrics
- Success metrics: time to first deploy, percentage of self-service deployments, developer satisfaction score, platform SLOs
