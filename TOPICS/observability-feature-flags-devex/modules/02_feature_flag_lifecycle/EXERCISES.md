# Exercises: Module 02 — Feature Flag Lifecycle and Progressive Delivery

## Instructions
Complete each exercise in order. Exercises increase in difficulty. Submit your answers by editing this file or committing a solutions file.

---

## Easy Exercises (1–3)

### Exercise 1
**Difficulty:** Easy
**Objective:** Define the module's core vocabulary.

Write one-sentence definitions for feature flag, telemetry, guardrail metric, and DevEx.

---

### Exercise 2
**Difficulty:** Easy
**Objective:** Identify safe-release signals.

List three signals you would watch during a checkout rollout and explain what each protects.

---

### Exercise 3
**Difficulty:** Easy
**Objective:** Read structured release data.

```yaml
flag: search_ranking_v2
owner: search-platform
exposure_percent: 5
rollback_when: "error_rate >= 2% for 10 minutes"
```

Explain what decision this data supports.

---

## Medium Exercises (4–6)

### Exercise 4
**Difficulty:** Medium
**Objective:** Design a rollout checklist.

Create a five-step checklist for enabling a risky feature for internal users first.

---

### Exercise 5
**Difficulty:** Medium
**Objective:** Connect product and system evidence.

Describe how you would compare conversion rate, error rate, and latency during a rollout.

---

### Exercise 6
**Difficulty:** Medium
**Objective:** Improve DevEx.

Propose two automation ideas that make safe rollout behavior easier for developers.

---

## Hard Exercises (7–8)

### Exercise 7
**Difficulty:** Hard
**Objective:** Write runnable flag logic.

```python
def enabled_for_percent(user_id, percent):
    # Implement stable percentage rollout logic.
    pass
```

Complete the function and show sample output for at least five user IDs.

---

### Exercise 8
**Difficulty:** Hard
**Objective:** Debug an unsafe rollout policy.

Rewrite this policy so it has a clear owner, guardrails, and rollback action.

```yaml
flag: beta
status: on
watch: dashboards
```

---

## Expert Exercise (9)

### Exercise 9
**Difficulty:** Expert
**Objective:** Synthesize control, evidence, and workflow.

Design a one-page release plan for a customer-visible change. Include flag strategy, observability plan, ownership, rollout stages, and rollback criteria.
