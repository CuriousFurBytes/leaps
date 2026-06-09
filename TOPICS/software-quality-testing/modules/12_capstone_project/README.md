# Module 12: Capstone Project

> Learn a release-quality test strategy spanning unit, integration, E2E, and regression suites.

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

## Overview

This module focuses on a release-quality test strategy spanning unit, integration, E2E, and regression suites. It is written for learners who need practical quality judgment, not merely terminology. Every section connects concepts to observable behavior so that testing becomes a disciplined way to reduce uncertainty.

You will use small runnable examples to reason about test intent, maintenance cost, and confidence. The same principles apply whether your team uses Python, JavaScript, Java, C#, or another stack.

## Prerequisites

- Module 11 in this topic.
- Basic programming syntax in at least one language.
- Comfort reading command examples and simple assertions.

## Objectives

By the end of this module, you will be able to:

- Explain the role of capstone project in a layered quality strategy.
- Design checks that connect directly to product risk.
- Implement small runnable examples with clear assertions.
- Debug common mistakes that make tests brittle or misleading.
- Communicate test confidence and remaining uncertainty.

## Theory

### The Capstone Mindset

This module is build-oriented. You will not receive a complete copy-paste solution because the goal is to practice judgment: deciding what to test, where to test it, and how to explain residual risk. Real QA leadership is less about maximizing test count and more about choosing evidence that matches the release decision.

Historically, many organizations accumulated large manual regression checklists after painful production bugs. Automation later promised relief, but teams learned that automated suites can become their own maintenance burden. The mature approach is a balanced system: fast unit checks for logic, integration checks for boundaries, selective E2E checks for user-critical journeys, exploratory testing for unknown risks, and regression tests tied to real defects.

### Project Brief

Build a quality strategy for a small web API and browser workflow. The system may be fictional, but your artifacts must be concrete: a risk inventory, a unit test plan, integration test cases, E2E journeys, regression coverage for at least three historical bugs, CI gate recommendations, and a release note that explains confidence and remaining risk.

```bash
# Example capstone workspace layout you may create outside this module.
mkdir quality-capstone
cd quality-capstone
mkdir docs tests/unit tests/integration tests/e2e tests/regression
```

### Architecture Expectations

Your project should show why each test belongs at its layer. A price-calculation rule belongs in a unit test because it should be fast and deterministic. A checkout API plus database write belongs in an integration test because the contract crosses a boundary. A login-to-purchase journey belongs in E2E because it demonstrates user value through the system.

```python
# Example risk scoring helper: probability times impact gives a simple priority.
def risk_score(probability, impact):
    return probability * impact

print(risk_score(4, 5))  # 20 means test this early and explain the mitigation.
```

### Getting Unstuck

Use staged help instead of jumping to a solution. First, name the release decision. Second, list user journeys and failure modes. Third, map each failure mode to the cheapest credible test layer. Fourth, automate only what will remain valuable after the first run.

```pseudocode
for each risk in release_risks:
    choose the lowest test layer that can observe the failure honestly
    add manual exploration when automation would hide uncertainty
    record what confidence the test does and does not provide
```

## Key Concepts

- **Quality assurance:** The broad practice of preventing, detecting, and communicating quality risk across the delivery lifecycle.
- **Test case:** A specific scenario with setup, action, expected result, and purpose.
- **Assertion:** A precise statement of expected behavior that a check verifies.
- **Risk:** The combination of likelihood and impact if a failure reaches users; see [[shared/glossary#risk]].
- **Regression:** A behavior that used to work but breaks after change; see [[shared/glossary#regression]].

## Examples

### Example 1: Risk-Based Test Selection

**Scenario:** A password reset email sometimes arrives late.

```pseudocode
if risk affects account access:
    add integration coverage for email provider contract
    add E2E smoke coverage for the reset journey
    keep detailed delivery timing in monitoring
```

The tradeoff is speed versus realism. Unit tests can validate token generation, but they cannot prove the external email path works.

### Example 2: Regression Test From a Bug

**Scenario:** A coupon once applied twice when a user refreshed checkout.

```python
# Regression check: refreshing must not duplicate the coupon discount.
def apply_coupon(total, coupon_already_used):
    if coupon_already_used:
        return total
    return total - 10

assert apply_coupon(50, True) == 50
```

This test is valuable because it protects a known failure mode, not because every possible coupon scenario is equally likely.

## Common Pitfalls

### Pitfall 1: Testing Implementation Instead of Behavior

```python
# Wrong: this locks onto an internal variable name.
assert calculator._subtotal == 15
```

```python
# Correct: this checks the visible behavior.
assert order_total([10, 5], 0.10) == 16.50
```

Learners do this because internals are easy to inspect. Avoid it by asking what user-visible promise would break.

### Pitfall 2: Treating All Tests as Equally Valuable

```pseudocode
# Wrong: automate every low-risk visual variation first.
automate all button color combinations
```

```pseudocode
# Correct: prioritize checks by impact and probability.
automate checkout, login, data integrity, and known regressions first
```

Test effort is finite. Use risk to decide sequence.

### Pitfall 3: Ignoring Failure Diagnostics

```python
# Wrong: unclear failure message.
assert result
```

```python
# Correct: explicit expected behavior.
assert result == "paid", "order should be paid after successful capture"
```

A test that fails mysteriously slows the team. Make failures explain the broken promise.

## Cross-Links

- [[software-engineering]]
- [[web-development]]
- [[databases]]
- [[shared/glossary#regression]]

## Summary

- Capstone Project helps teams gather credible evidence about software behavior.
- Useful tests are selected by risk, not by raw count.
- Fast checks and realistic checks both matter, but they answer different questions.
- Clear assertions make failures easier to diagnose.
- Regression coverage should preserve lessons learned from real defects.
