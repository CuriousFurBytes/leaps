# Module 12: Capstone Project

> Design and validate a realistic network architecture that synthesizes the whole Networks topic.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Project Brief](#project-brief)
5. [Architecture Requirements](#architecture-requirements)
6. [Milestones](#milestones)
7. [Help and Getting Unstuck](#help-and-getting-unstuck)
8. [Acceptance Criteria](#acceptance-criteria)
9. [Cross-Links](#cross-links)
10. [Summary](#summary)

## Overview
The capstone is build-oriented: you produce a design package for a small organization with a headquarters, a cloud environment, remote users, public services, and monitoring. The goal is not to copy a provided solution. The goal is to make defensible engineering decisions, explain tradeoffs, and prove that the design can be operated and troubleshot.

A strong submission reads like something a network or platform engineer could hand to teammates before implementation. It includes an address plan, segmentation model, routing plan, security controls, service exposure strategy, observability plan, failure scenarios, and runbooks.

## Prerequisites
- Modules 01–11 of this topic.
- Comfort reading packet captures, route tables, firewall policies, and service diagrams.
- Ability to explain how [[networks#module-map]] connects to security, distributed systems, and [[devops-platform-engineering]].

## Objectives
By the end of this module, you will be able to:
- Design a multi-zone network from requirements and constraints.
- Allocate IPv4 and IPv6 space using clear CIDR reasoning.
- Choose routing, firewall, DNS, TLS, VPN, and load-balancing patterns.
- Define observability and troubleshooting procedures before incidents occur.
- Justify tradeoffs around cost, resilience, complexity, and security.

## Project Brief
Design the network for **Northwind Learning Labs**, a fictional training company with 120 employees, one office, remote instructors, a small cloud-hosted application, and partner access requirements. Your artifact may be a Markdown design document with diagrams, tables, command examples, and test plans.

```yaml
organization:
  users: 120
  office: headquarters
  remote_users: true
  public_services:
    - learning-portal
    - api
  private_services:
    - database
    - monitoring
    - internal-admin
```

## Architecture Requirements
- Provide an address plan with at least four subnets and room for growth.
- Separate user, server, management, guest, and cloud workloads.
- Define ingress and egress paths for public and private services.
- Include DNS naming, certificate, and TLS assumptions.
- Include firewall rules in plain language and a compact table.
- Include monitoring signals for latency, loss, DNS failures, saturation, and denied traffic.

```bash
# Example validation commands to include in your runbook, adjusted for your design.
dig portal.example.test
traceroute portal.example.test
curl -Iv https://portal.example.test
```

## Milestones
1. Requirements and assumptions.
2. Addressing and segmentation plan.
3. Routing and connectivity plan.
4. Security controls and trust boundaries.
5. Observability, troubleshooting, and incident runbooks.
6. Final review with explicit tradeoffs and known risks.

## Help and Getting Unstuck
Use these hints only when blocked; they are scaffolding, not a complete solution.

### Hint 1: Start with traffic flows
List who talks to what before drawing boxes. A user-to-portal flow, admin-to-management flow, and application-to-database flow reveal most required segments.

### Hint 2: Allocate by purpose
Avoid assigning addresses one host at a time. Reserve blocks for user devices, servers, management, guest access, cloud workloads, and point-to-point links.

### Hint 3: Security follows boundaries
A firewall rule should express a business need. If you cannot explain why a source needs a destination and port, deny it until a requirement proves otherwise.

### Hint 4: Make failure observable
For every critical dependency, define how you would notice failure and which command or dashboard would narrow the cause.

## Acceptance Criteria
- The design is internally consistent and can be reviewed without extra tools.
- Every subnet, route, trust boundary, and public exposure has a stated purpose.
- The runbook can distinguish DNS, routing, firewall, TLS, and application failures.
- The design includes at least three realistic failure scenarios and responses.
- The final reflection explains what you would change at 10x scale.

## Cross-Links
- [[networks#module-map]]
- [[devops-platform-engineering]]
- [[postgresql]]
- [[javascript-typescript-react]]

## Summary
- The capstone turns network knowledge into a realistic engineering artifact.
- Strong designs begin with requirements and traffic flows, not devices.
- Addressing, routing, security, DNS, TLS, and observability must agree with each other.
- Runbooks prove that the network can be operated after it is designed.
- The best submissions justify tradeoffs rather than pretending one design is universally correct.
