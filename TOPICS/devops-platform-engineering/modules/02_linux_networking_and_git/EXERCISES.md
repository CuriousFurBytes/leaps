# Exercises: Module 02 — Linux, Networking, and Git

## Instructions

Complete each item in order. Exercises increase in difficulty. Submit your answers by editing this file or committing a separate solutions file.

---

## Easy Exercises (1–3)

### Exercise 1
**Difficulty:** Easy
**Objective:** Explain the module's main purpose.

Write a five-sentence summary of why this module matters to platform engineering.

### Exercise 2
**Difficulty:** Easy
**Objective:** Identify operational signals.

List three signals a team could use to know whether a change is safe.

### Exercise 3
**Difficulty:** Easy
**Objective:** Practice command literacy.

Write the command you would run to check repository status before making a change.

```bash
git status --short
```

---

## Medium Exercises (4–6)

### Exercise 4
**Difficulty:** Medium
**Objective:** Convert a manual process into documented steps.

Write a short deployment checklist with at least five ordered steps.

### Exercise 5
**Difficulty:** Medium
**Objective:** Reason about tradeoffs.

Compare a fully manual workflow with an automated workflow. Include one advantage and one risk for each.

### Exercise 6
**Difficulty:** Medium
**Objective:** Connect concepts.

Explain how feedback loops, guardrails, and runbooks support each other.

---

## Hard Exercises (7–8)

### Exercise 7
**Difficulty:** Hard
**Objective:** Design a small workflow.

Sketch a CI/CD workflow for a single HTTP service using a language-tagged YAML block.

```yaml
stages:
  - test
  - build
  - deploy
  - verify
```

### Exercise 8
**Difficulty:** Hard
**Objective:** Debug a platform process.

Given a failing health check, write the first five facts you would gather before changing the system.

---

## Expert Exercise (9)

### Exercise 9
**Difficulty:** Expert
**Objective:** Synthesize product and operations thinking.

Design a narrow golden path for one service type. Define the user, the supported workflow, the guardrails, and the evidence you would collect to decide whether the platform is working.
