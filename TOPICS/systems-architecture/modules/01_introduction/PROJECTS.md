# Projects: Module 01 — Introduction to Distributed Systems

> These projects apply the concepts from Module 01 in a hands-on way.
> See the topic-level [PROJECTS.md](../../PROJECTS.md) for larger projects spanning multiple modules.

---

## Project A: Architecture Audit Report

**Difficulty:** Beginner
**Time estimate:** 2–3 hours

**Brief:**
Choose a real open-source project (suggestions: Mastodon, Discourse, Redmine, or any project you've used) and research its architecture. Produce a 1-page architecture audit report covering:

1. What is the deployment model — monolith, modular monolith, or microservices?
2. Which of the 8 Fallacies does the system's documentation acknowledge (explicitly or implicitly)?
3. Where in CAP space does the system's primary data store sit, and why?
4. One specific design decision in the project that you would characterize as either good (well-considered trade-off) or bad (ignores a fallacy or CAP concern), with your reasoning.

**Deliverable:** A 300–500 word Markdown document in this directory.

---

## Project B: Latency Budget Calculator

**Difficulty:** Intermediate
**Time estimate:** 2–3 hours

**Brief:**
Write a Python script that models the latency of a synchronous service call chain and computes the p50, p95, p99, and p999 combined latency given per-service latency distributions.

Your script should:
- Accept a list of services, each with: mean latency (ms), standard deviation, and p99 (ms)
- Simulate 100,000 requests by sampling from each service's distribution
- Compute the combined tail latencies for the sequential chain
- Output a comparison: "Sync chain p99: X ms. If services were called in parallel, p99 would be: Y ms."
- Show the "worst case" latency (max of all services at p99)

This demonstrates why synchronous chains amplify tail latency, and why parallelism helps.

**Deliverable:** A Python script `latency_budget.py` with a brief README explaining the output.
