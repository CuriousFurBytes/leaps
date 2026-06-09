# Module 06: CI/CD Pipelines

[← Module 05: Kubernetes Advanced](../05_kubernetes-advanced/) | [Topic Home](../../README.md) | [Next → Module 07: Infrastructure as Code](../07_infrastructure-as-code/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate--Advanced-orange)
![Time](https://img.shields.io/badge/time-10--12h-orange)

> CI/CD pipelines are the automated assembly lines of software delivery. This module covers GitHub Actions, GitLab CI/CD, pipeline design principles, artifact management, environment promotion, approval gates, and secrets management.

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

A CI/CD pipeline is the automated path from a code commit to running software in production. It embodies the First Way (optimize flow) and Second Way (fast feedback) of DevOps. This module covers the two dominant CI/CD platforms — GitHub Actions and GitLab CI/CD — plus the principles that apply to any pipeline: fast feedback, shift-left testing, immutable artifacts, environment promotion, and secrets management.

---

## Prerequisites

- Module 03: Containers — building Docker images is a central pipeline step
- Module 04: Kubernetes Fundamentals — deploying to Kubernetes is the final pipeline stage
- Basic git knowledge: branches, pull requests, merges

---

## Objectives

By the end of this module, you will be able to:

1. Design a multi-stage CI/CD pipeline following best practices: fail fast, build once, promote artifacts
2. Write GitHub Actions workflows with jobs, steps, matrix builds, and reusable workflows
3. Write GitLab CI/CD pipelines with stages, rules, artifacts, and environments
4. Implement proper secrets management: use platform secrets, never hardcode credentials
5. Configure environment-based deployments with manual approval gates
6. Implement security scanning (SAST, container scanning) as pipeline gates
7. Optimize pipeline performance with caching, parallel jobs, and conditional execution

---

## Theory

> [!NOTE]
> Full theory content coming soon.

### Pipeline Design Principles

**Build once, deploy many.** Build and tag the artifact exactly once in CI. Promote the same artifact through staging → production. Never rebuild in CD — rebuilding can produce different output even from the same commit.

**Fail fast.** Order pipeline stages from fastest to slowest. Linting and unit tests (30 seconds) should run before integration tests (5 minutes) which should run before container builds (2 minutes). Developers get feedback from the cheapest checks first.

**Immutable artifacts.** Tag artifacts with the commit SHA. A tag like `myapp:abc1234` is immutable and auditable; `myapp:latest` is not. `latest` is an anti-pattern in production pipelines.

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Stage 1: Lint and test (fast feedback)
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'          # cache pip dependencies

      - name: Install dependencies
        run: pip install -r requirements.txt -r requirements-dev.txt

      - name: Run linting
        run: ruff check .

      - name: Run tests with coverage
        run: pytest --cov=. --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4

  # Stage 2: Build and scan (only on test pass)
  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      security-events: write
    outputs:
      image-digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@v4

      - name: Log in to registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=ref,event=branch

      - name: Build and push
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name == 'push' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Scan image for vulnerabilities
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'          # fail pipeline on critical/high CVEs

  # Stage 3: Deploy to production (only on main branch push, with approval)
  deploy-production:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    environment:
      name: production          # GitHub environment with required reviewers configured
      url: https://myapp.example.com
    steps:
      - uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/setup-kubectl@v3

      - name: Deploy to Kubernetes
        env:
          KUBECONFIG: ${{ secrets.KUBECONFIG_PRODUCTION }}
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          kubectl rollout status deployment/myapp --timeout=5m
```

### GitLab CI/CD

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - scan
  - deploy

variables:
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

test:
  stage: test
  image: python:3.12-slim
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .cache/pip
  script:
    - pip install -r requirements.txt
    - pytest --junitxml=report.xml
  artifacts:
    reports:
      junit: report.xml

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG

deploy-production:
  stage: deploy
  image: bitnami/kubectl:latest
  environment:
    name: production
    url: https://myapp.example.com
  when: manual                   # requires manual trigger
  only:
    - main
  script:
    - kubectl set image deployment/myapp myapp=$IMAGE_TAG
    - kubectl rollout status deployment/myapp
```

### Secrets Management

```yaml
# WRONG: hardcoded secret in pipeline
- name: Deploy
  run: |
    aws configure set aws_access_key_id AKIAIOSFODNN7EXAMPLE
    aws configure set aws_secret_access_key wJalrXUtnFEMI/K7MDENG

# WRONG: secret in environment variable visible in logs
env:
  DB_PASSWORD: mypassword123

# RIGHT: use platform secrets (never logged, encrypted at rest)
env:
  DB_PASSWORD: ${{ secrets.DB_PASSWORD }}   # GitHub Actions
  # or
  DB_PASSWORD: $DB_PASSWORD                 # GitLab CI, set in project secrets
```

---

## Key Concepts

**Continuous Integration (CI)** — the practice of merging developer changes to a shared branch frequently (at least daily), with automated build and test pipelines verifying each merge. CI eliminates integration hell by making integration a continuous, automated process.

**Continuous Delivery (CD)** — every passing CI build is in a deployable state. Deployment to production may require a manual approval, but it is always possible with one click.

**Artifact** — the immutable output of a build step: a container image, compiled binary, or deployment package. Artifacts are tagged with the commit SHA and stored in a registry or artifact store.

**Matrix Build** — running the same pipeline steps with multiple configurations in parallel (e.g., test against Python 3.10, 3.11, and 3.12 simultaneously).

**Reusable Workflow (GitHub Actions)** — a workflow that can be called by other workflows, enabling DRY pipeline code across multiple repositories.

---

## Examples

> Full examples coming soon. Will include: a complete monorepo pipeline with conditional job execution, a matrix test workflow, a GitLab CI pipeline with dynamic environments, and integrating SAST tools.

---

## Common Pitfalls

> Full pitfalls section coming soon. Key pitfalls: rebuilding the artifact in CD instead of promoting the CI-built artifact, storing secrets in environment variables (visible in logs), using `latest` as the image tag, not caching dependencies (slow pipelines), not setting pipeline timeouts (hung jobs consume quota), and running deployments without health checks.

---

## Cross-Links

- [[devops-platform-engineering/modules/03_containers]] — building and pushing container images is a core CI stage
- [[devops-platform-engineering/modules/07_infrastructure-as-code]] — Terraform can be run in CI/CD pipelines; `terraform plan` in CI, `terraform apply` with approval in CD
- [[devops-platform-engineering/modules/09_gitops-and-delivery]] — GitOps is a CD model where the pipeline updates a Git repository instead of directly deploying
- [[qa-testing]] — shift-left testing integrates unit, integration, and security tests into CI pipelines

---

## Summary

- CI/CD pipelines automate the path from commit to production; good pipelines fail fast, build once, and promote immutable artifacts
- GitHub Actions uses workflows with jobs and steps; GitLab CI uses `.gitlab-ci.yml` with stages
- Secrets must never be hardcoded or logged; use platform-provided secrets management
- Environment-based deployments with manual approval gates are the right model for production promotion
- Security scanning (SAST, container scanning, dependency scanning) should be pipeline gates that fail the build on critical issues
- Pipeline performance matters: caching, parallel jobs, and conditional execution keep pipelines under 10 minutes
