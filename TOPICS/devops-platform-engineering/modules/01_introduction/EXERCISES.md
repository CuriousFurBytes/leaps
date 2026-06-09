# Exercises: Module 01 — Introduction to DevOps and Platform Engineering

## Instructions

Complete each exercise in order. Exercises increase in difficulty.
Submit your answers by editing this file or committing a solutions file.

---

## Easy Exercises (1–3)

### Exercise 1

**Difficulty:** Easy
**Objective:** Recall the Three Ways and give a concrete example of each

Without referring back to the module, write a one-sentence description of each of the Three Ways of DevOps. Then give one concrete example of a practice or tool that embodies each Way.

| Way | Description | Example Practice |
|-----|-------------|-----------------|
| First Way (Flow) | | |
| Second Way (Feedback) | | |
| Third Way (Continuous Improvement) | | |

---

### Exercise 2

**Difficulty:** Easy
**Objective:** Identify DORA metric tiers for a given organization

A company has the following delivery characteristics:
- Deploys to production once per month
- Code changes take 3 weeks from commit to production
- About 25% of deployments cause production incidents
- When incidents occur, they take about 2 days to resolve

For each DORA metric, classify this organization as Elite, High, Medium, or Low performer (use the table in the module README).

| Metric | Value | DORA Tier |
|--------|-------|-----------|
| Deployment Frequency | Once/month | |
| Lead Time for Changes | 3 weeks | |
| Change Failure Rate | 25% | |
| MTTR | 2 days | |

What overall performance tier would you classify this organization in?

---

### Exercise 3

**Difficulty:** Easy
**Objective:** Match DevOps toolchain stages to tools

Draw a line (or fill in the table) matching each tool to its primary DevOps toolchain stage.

| Tool | Stage |
|------|-------|
| GitHub Issues | |
| Prometheus | |
| Docker | |
| ArgoCD | |
| pytest | |
| Terraform | |

Stages available: Plan, Code, Build, Test, Release, Deploy, Operate, Monitor

---

## Medium Exercises (4–6)

### Exercise 4

**Difficulty:** Medium
**Objective:** Analyze the organizational dysfunction of a wall of confusion scenario

Read the following scenario and answer the questions below.

> Acme Corp has separate Development (50 engineers) and Operations (15 engineers) departments. Development uses a 2-week sprint cycle and measures velocity (story points per sprint). Operations manages 200 production servers and measures uptime (99.9% SLA). Every two months, Development submits a "release request" to Operations, who schedule the deployment during a 4-hour maintenance window on Sunday at 2 AM. Post-deployment issues are handled by a dedicated "incident bridge" call involving both teams.

1. Identify three specific ways this organizational structure creates the "wall of confusion."
2. What are the incentive misalignments between the two teams?
3. Which DORA metrics would you expect to be worst for this organization, and why?
4. Propose two organizational changes (not tooling changes) that would begin to address the dysfunction.

---

### Exercise 5

**Difficulty:** Medium
**Objective:** Write a bash script that automates a manual operational task

Write a bash script called `health-check.sh` that:
1. Accepts a list of URLs as arguments (e.g., `./health-check.sh https://api.example.com/health https://web.example.com/`)
2. Makes an HTTP GET request to each URL using `curl`
3. Checks if the HTTP status code is 200
4. Prints a pass/fail result for each URL with color coding
5. Exits with a non-zero status code if any URL fails

```bash
#!/usr/bin/env bash
# health-check.sh — Verify that service endpoints are healthy
# TODO: Complete this script

set -euo pipefail

# Your implementation here
```

**Hint:** `curl -o /dev/null -s -w "%{http_code}"` returns just the HTTP status code.

---

### Exercise 6

**Difficulty:** Medium
**Objective:** Distinguish between DevOps, SRE, and Platform Engineering

For each of the following statements, identify whether it describes DevOps, SRE, Platform Engineering, or more than one. Explain your reasoning.

1. "We track error budgets for our services and pause feature work when we're over budget."
2. "Every engineer is on-call for the services they own."
3. "We built a CLI tool that scaffolds new services with CI/CD, monitoring, and Kubernetes manifests in one command."
4. "We have a 30% cap on time spent on toil; the rest must be engineering work."
5. "Teams can deviate from the golden path, but they must own the operational consequences."
6. "We measure Deployment Frequency, Lead Time, Change Failure Rate, and MTTR every sprint."

---

## Hard Exercises (7–8)

### Exercise 7

**Difficulty:** Hard
**Objective:** Apply value stream mapping to identify delivery bottlenecks

Sketch a value stream map for the following delivery process. Identify: (a) where work is waiting (queues), (b) which steps are manual vs. automated, and (c) what you would automate first to maximize impact on Lead Time.

> A feature request is created in Jira (1 day). A developer picks it up, codes it, and opens a PR (3 days). The PR sits waiting for code review (2 days average). After review, CI runs (45 minutes). The PR is merged. A manual deploy request is submitted to the operations team (1 day to process). Operations runs the deployment script in a 2-hour maintenance window. Monitoring confirms the deploy succeeded (30 minutes). Total lead time: ~8 days.

Your value stream map should show each step, its duration, and whether it is value-adding or waste.

---

### Exercise 8

**Difficulty:** Hard
**Objective:** Write a DORA metrics calculation script

Extend the `dora-metrics.sh` script from the Examples section. Add a function that:
1. Takes a git repository path as an argument
2. Calculates deployment frequency from git tags matching the pattern `deploy-*`
3. Calculates lead time by finding the time from the oldest commit in each deploy batch to the deploy tag timestamp
4. Outputs results in a human-readable table format

```bash
#!/usr/bin/env bash
# dora-metrics.sh — Calculate DORA metrics from git history
# Usage: ./dora-metrics.sh /path/to/repo

# Your implementation here
```

---

## Expert Exercise (9)

### Exercise 9

**Difficulty:** Expert
**Objective:** Design a DevOps transformation roadmap for a real organization

Choose an organization you know (your current or former employer, an open-source project, or a hypothetical organization you define). Write a structured DevOps transformation proposal addressing:

1. **Current State Assessment** — What are the approximate DORA metrics? What is the organizational structure? Where is the wall of confusion?

2. **Target State** — What DORA tier are you targeting? What organizational model (DevOps, SRE, Platform Engineering, or hybrid)?

3. **Phase 1 (0–3 months): Quick Wins** — Three specific changes you would implement first. For each: what you'd change, how you'd measure success, and what resistance to expect.

4. **Phase 2 (3–12 months): Foundation** — Three larger investments. For each: what it enables, estimated cost, and dependencies.

5. **Anti-patterns to avoid** — Name two specific failure modes most likely to occur in this organization's transformation, based on the pitfalls section of the module.

Length: 600–1000 words. Specificity is more valuable than generality.
