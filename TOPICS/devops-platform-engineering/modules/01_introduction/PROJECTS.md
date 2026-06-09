# Projects: Module 01 — Introduction to DevOps and Platform Engineering

> These projects apply the cultural and measurement concepts from Module 01.
> No advanced tooling required — this module is about understanding, measurement, and communication.

---

## Project 1: Team DORA Self-Assessment (Beginner)

**Estimated time:** 2–3 hours

Conduct a DORA metrics assessment for a real or hypothetical team.

If you work in software: gather data on your current team's four DORA metrics (deployment frequency, lead time, change failure rate, MTTR) from whatever data sources are available (git history, incident tickets, deployment logs). If you cannot access real data, use a hypothetical team you define.

**Deliverables:**
1. A written assessment identifying each metric value and DORA tier
2. A list of the top three bottlenecks contributing to the weakest metrics
3. Three concrete improvement suggestions (not tool purchases — process and organizational changes first)

---

## Project 2: Value Stream Map (Intermediate)

**Estimated time:** 3–4 hours

Map the current state value stream for a software delivery process you are familiar with. If you cannot use a real one, design a realistic hypothetical for a 10-person engineering team at a Series B startup.

**Deliverables:**
1. Current state value stream map (hand-drawn and photographed, or a diagram tool like draw.io) showing each step, its duration, and whether it is value-adding or waste
2. Identification of the top three waste sources
3. Future state value stream map showing what changes you would make
4. Estimated DORA metric improvements from your proposed changes

---

## Project 3: Service Health Monitor Script (Beginner)

**Estimated time:** 1–2 hours

Write and test the `health-check.sh` script from Exercise 5 (or extend it). Your script should check multiple services or URLs, produce a clear report, and be usable in a CI/CD pipeline.

**Deliverables:**
- A working `health-check.sh` script that you have tested on your machine
- A README section explaining how to use it and how to integrate it into a pipeline
