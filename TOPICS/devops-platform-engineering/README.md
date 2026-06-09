# DevOps/Platform Engineering

> A zero-to-expert learning path for building, operating, and improving reliable software delivery platforms.

## Table of Contents
1. [Why Learn DevOps/Platform Engineering?](#why-learn-devopsplatform-engineering)
2. [Prerequisites](#prerequisites)
3. [Module Map](#module-map)
4. [Cross-Links](#cross-links)
5. [Quick Reference](#quick-reference)
6. [How to Use This Topic](#how-to-use-this-topic)

## Why Learn DevOps/Platform Engineering?

DevOps began as a response to the old wall between software development and operations. Developers wanted to ship faster; operators needed stable, understandable systems. Platform engineering keeps the best parts of that movement while making the paved road explicit: teams build reusable platforms, golden paths, self-service workflows, and operational guardrails so product teams can move quickly without rediscovering infrastructure lessons the hard way.

This topic teaches both the cultural and technical sides. You will learn why feedback loops matter, how Linux and networks shape production behavior, how CI/CD pipelines encode delivery policy, how infrastructure as code changes risk management, and how observability turns unknown failures into diagnosable signals. The goal is not tool memorization; tools change, but the mental models of automation, reliability, ownership, and service design transfer across clouds and organizations.

A mature platform engineer thinks like a product builder and an operator at the same time. They ask who the platform serves, which repetitive tasks should become self-service, which failure modes need guardrails, and how to make the safest path the easiest path. By the end of this path, you should be able to design and defend a realistic internal developer platform with deployment, runtime, monitoring, incident response, and governance concerns connected into one coherent system.

## Prerequisites

- Comfort using a terminal: changing directories, editing text files, and running commands.
- Basic programming experience in any language; [[python]] or [[javascript]] knowledge is enough.
- Basic web concepts such as HTTP requests, ports, clients, and servers.
- Curiosity about [[linux]], [[networking]], [[software-engineering]], [[cloud-computing]], and [[security]].

## Module Map

| # | Module | Difficulty | Status |
|---|--------|------------|--------|
| 01 | [Foundations and Workstation](./modules/01_foundations_and_workstation/README.md) | Beginner | [ ] |
| 02 | [Linux, Networking, and Git](./modules/02_linux_networking_and_git/README.md) | Beginner | [ ] |
| 03 | [Automation and CI/CD](./modules/03_automation_and_ci_cd/README.md) | Intermediate | [ ] |
| 04 | Infrastructure as Code and Configuration | Intermediate | [ ] |
| 05 | Containers and Image Supply Chains | Intermediate | [ ] |
| 06 | Kubernetes and Workload Orchestration | Advanced | [ ] |
| 07 | Cloud Architecture and Networking | Advanced | [ ] |
| 08 | Observability, SLOs, and Incident Response | Advanced | [ ] |
| 09 | Security, Secrets, and Compliance Guardrails | Advanced | [ ] |
| 10 | Platform Product Management and Developer Experience | Expert | [ ] |
| 11 | Scaling, Cost, Governance, and Reliability Tradeoffs | Expert | [ ] |
| 12 | [Capstone Project](./modules/12_capstone_project/README.md) | Expert | [ ] |

## Cross-Links

- [[linux]] — process, filesystem, shell, and service fundamentals.
- [[networking]] — DNS, TCP, HTTP, TLS, routing, and load balancing.
- [[cloud-computing]] — managed infrastructure, identity, and regional architecture.
- [[security]] — secrets management, supply-chain controls, and least privilege.
- [[software-engineering]] — testing, release discipline, and architecture tradeoffs.

## Quick Reference

| Task | Command or Concept | Why It Matters |
|---|---|---|
| Inspect the current directory | `pwd` and `ls` | Confirm where commands will run before changing systems. |
| Track changes | `git status` | Delivery starts with knowing exactly what changed. |
| Run a local health check | `curl -fsS http://localhost:8080/health` | Automation needs simple, scriptable pass/fail signals. |
| Describe desired infrastructure | Infrastructure as code | Reviewable text beats undocumented manual clicks. |
| Release safely | CI/CD pipeline | Make build, test, scan, and deploy repeatable. |
| Operate production | SLO plus runbook | Define user-facing reliability and what to do when it degrades. |

## How to Use This Topic

Work through Modules 01–03 first, even if you have used some tools before, because the later modules assume the same vocabulary. After that, continue through the roadmap in order or use the module map to target gaps. The final capstone asks you to synthesize the whole path into a small but realistic platform product; do not attempt it as a copy-paste exercise.
