# Module 03: Containers

[← Module 02: Linux and Shell](../02_linux-and-shell/) | [Topic Home](../../README.md) | [Next → Module 04: Kubernetes Fundamentals](../04_kubernetes-fundamentals/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate-yellow)
![Time](https://img.shields.io/badge/time-8--10h-orange)

> Containers package applications with their dependencies into portable, reproducible units using Linux namespaces and cgroups. This module covers Docker fundamentals, image layers, Dockerfile best practices, Docker Compose, and container security.

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
> **This module is a stub.** Full content will be added in a future update. The objectives, key topics, and cross-links below are complete.

Containers are the packaging format of modern software delivery. Every CI/CD pipeline ends with a container image. Every Kubernetes deployment runs containers. Understanding how containers work — not just how to use Docker commands, but what is happening at the Linux kernel level — is essential for debugging production issues, optimizing builds, and understanding security boundaries.

---

## Prerequisites

- Module 02: Linux and Shell — specifically: process management, namespaces/cgroups concepts, file permissions
- Basic familiarity with running command-line tools

---

## Objectives

By the end of this module, you will be able to:

1. Explain how Docker uses Linux namespaces, cgroups, and Union filesystems to create container isolation
2. Write production-quality multi-stage Dockerfiles that produce minimal, secure images
3. Understand image layer caching and design Dockerfiles that maximize cache efficiency
4. Push and pull images from container registries (Docker Hub, GitHub Container Registry)
5. Compose multi-service applications using Docker Compose
6. Apply container security best practices: non-root users, read-only filesystems, minimal base images, image scanning
7. Debug running containers using `docker exec`, `docker logs`, and `docker inspect`

---

## Theory

> [!NOTE]
> Full theory content coming soon. Subsections will cover:
> - How containers work: namespaces (pid, net, mnt, uts, ipc, user), cgroups, Union filesystem (OverlayFS)
> - The OCI image specification and container runtime (containerd, runc)
> - Docker image layers: how they are created, cached, and shared
> - Dockerfile instructions: FROM, RUN, COPY, ADD, ENV, ARG, EXPOSE, WORKDIR, USER, CMD, ENTRYPOINT
> - Multi-stage builds for smaller, more secure images
> - Docker Compose: defining multi-service applications
> - Container security: CVE scanning, non-root users, capabilities, seccomp profiles

### Container Isolation Model

```bash
# A container is a process with restricted visibility
# These Linux features create the isolation:
# 1. PID namespace — the container's processes have their own PID tree
# 2. Network namespace — the container has its own network interfaces
# 3. Mount namespace — the container has its own filesystem view
# 4. UTS namespace — the container has its own hostname
# 5. IPC namespace — isolated inter-process communication
# 6. User namespace — can map root in container to non-root on host

# Verify: a container's PID 1 is not the host's PID 1
docker run --rm alpine ps aux
# PID 1 inside the container is the container's process
```

### Image Layers and Caching

```dockerfile
# WRONG: dependency installation is re-run on every code change
FROM python:3.12-slim
WORKDIR /app
COPY . .                          # any file change invalidates this layer
RUN pip install -r requirements.txt  # and all subsequent layers

# RIGHT: copy dependency files first to maximize cache hits
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .           # only invalidates when requirements.txt changes
RUN pip install --no-cache-dir -r requirements.txt  # cached unless deps change
COPY . .                          # only this layer rebuilds on code changes
```

### Multi-Stage Build Pattern

```dockerfile
# Stage 1: Build environment (large, has build tools)
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /bin/server ./cmd/server

# Stage 2: Runtime environment (minimal, no build tools)
FROM scratch                      # empty image — absolute minimum
COPY --from=builder /bin/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
EXPOSE 8080
ENTRYPOINT ["/server"]
```

### Docker Compose for Local Development

```yaml
# docker-compose.yml
version: '3.9'
services:
  api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app                    # mount source for hot reloading in dev

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres-data:
```

---

## Key Concepts

**Union Filesystem (OverlayFS)** — Docker images are composed of stacked read-only layers with a writable layer on top. Each `RUN`, `COPY`, and `ADD` instruction creates a new layer. The Union filesystem merges these layers into a coherent view. Layers are shared across images — if two images share a base layer, it is stored once on disk.

**Container Registry** — A server for storing and distributing container images. Docker Hub is the public default; GitHub Container Registry (ghcr.io), AWS ECR, GCP Artifact Registry, and Azure ACR are common enterprise registries. Images are identified by `registry/repository:tag`.

**Docker Compose** — A tool for defining and running multi-container applications. The `docker-compose.yml` file declares services, their images or build contexts, environment variables, port mappings, volumes, and dependencies. `docker compose up` starts the entire stack.

**Container Security Scanning** — The process of checking a container image for known CVEs (Common Vulnerabilities and Exposures) in the installed packages and dependencies. Trivy, Grype, and Docker Scout are common scanners.

---

## Examples

> Full worked examples coming soon. Will include: building and scanning a Node.js application, creating a multi-stage Python application with secrets, a complete docker-compose stack with PostgreSQL and Redis, and debugging a container crash.

---

## Common Pitfalls

> Full pitfalls section coming soon. Key pitfalls include: running as root, not using multi-stage builds, installing development dependencies in production images, committing secrets in image layers, not pinning base image versions, and port conflict issues in docker-compose.

---

## Cross-Links

- [[devops-platform-engineering/modules/02_linux-and-shell]] — Linux namespaces and cgroups are the kernel foundation for container isolation
- [[devops-platform-engineering/modules/04_kubernetes-fundamentals]] — Kubernetes schedules and orchestrates containers; Docker builds the images Kubernetes runs
- [[devops-platform-engineering/modules/11_security-and-compliance]] — Container image scanning, signing (Cosign), and SBOM generation extend the security practices introduced here

---

## Summary

- Containers use Linux namespaces (process, network, filesystem isolation) and cgroups (resource limits) to provide lightweight process isolation
- Docker images are stacked read-only layers built by Dockerfile instructions; the final writable layer is the running container
- Multi-stage builds separate build tools from runtime, producing minimal images
- Layer ordering matters for cache efficiency: copy dependency files before source code
- Docker Compose defines multi-service local development environments declaratively
- Container security requires: non-root user, minimal base image, no secrets in layers, regular CVE scanning, and pinned image versions
