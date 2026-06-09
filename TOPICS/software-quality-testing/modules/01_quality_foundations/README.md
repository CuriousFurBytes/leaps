# Module 01: Quality Foundations

> Learn quality vocabulary, risk thinking, and the test pyramid.

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

This module focuses on quality vocabulary, risk thinking, and the test pyramid. It is written for learners who need practical quality judgment, not merely terminology. Every section connects concepts to observable behavior so that testing becomes a disciplined way to reduce uncertainty.

You will use small runnable examples to reason about test intent, maintenance cost, and confidence. The same principles apply whether your team uses Python, JavaScript, Java, C#, or another stack.

## Prerequisites

- None; this is the first module.
- Basic programming syntax in at least one language.
- Comfort reading command examples and simple assertions.

## Objectives

By the end of this module, you will be able to:

- Explain the role of quality foundations in a layered quality strategy.
- Design checks that connect directly to product risk.
- Implement small runnable examples with clear assertions.
- Debug common mistakes that make tests brittle or misleading.
- Communicate test confidence and remaining uncertainty.

## Theory

### Why This Module Exists

Quality Foundations is the part of software quality testing that teaches quality vocabulary, risk thinking, and the test pyramid. The central idea is that tests are evidence, not decoration. A test is useful only when it answers a meaningful question about behavior, risk, or maintainability. Historically, software teams moved from late manual inspection toward automated checks because software changes quickly and repeated verification by hand becomes slow, inconsistent, and expensive.

A beginner often asks, "Did I write enough tests?" A stronger question is, "What risks remain invisible?" For example, a payment calculation may have excellent unit coverage but still fail when the database stores cents as strings, or a login flow may work in an API client but fail in the browser because a cookie flag is wrong. This module builds the mental model for choosing test types intentionally.

### A Small Example System

The following example is intentionally tiny. It gives us a concrete behavior to discuss: an order total should include item prices and tax. In real work, this behavior might sit behind a UI, API, database, and deployment pipeline, but the core quality question starts with expected behavior.

```python
# Calculate an order total from item prices and a tax rate.
def order_total(prices, tax_rate):
    subtotal = sum(prices)              # Add every item price.
    tax = subtotal * tax_rate           # Calculate proportional tax.
    return round(subtotal + tax, 2)     # Round to currency-style precision.

print(order_total([10.00, 5.00], 0.10))  # Expected output: 16.5
```

### Turning Behavior Into Checks

A check needs an input, an observed result, and an expected result. The important habit is to test behavior that would matter if it broke. In quality work, this is connected to [[shared/glossary#risk]]: a low-risk formatting detail may not deserve the same attention as a checkout failure.

```python
# A minimal assertion-based check for the behavior above.
def test_order_total_includes_tax():
    actual = order_total([10.00, 5.00], 0.10)  # Exercise the behavior.
    assert actual == 16.50                     # Compare with expected behavior.
```

### Communicating Test Intent

Good tests are also documentation. The test name should say what behavior matters, the setup should reveal the scenario, and the assertion should make the expected outcome unambiguous. This is why QA connects technical work with product communication: a failing test should help the team understand a user-facing risk.

```javascript
// The same behavior expressed in JavaScript-style pseudocode for web teams.
function orderTotal(prices, taxRate) {
  const subtotal = prices.reduce((sum, price) => sum + price, 0); // Add prices.
  const tax = subtotal * taxRate;                                // Compute tax.
  return Math.round((subtotal + tax) * 100) / 100;                // Round cents.
}

console.log(orderTotal([10, 5], 0.10)); // Expected output: 16.5
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

- Quality Foundations helps teams gather credible evidence about software behavior.
- Useful tests are selected by risk, not by raw count.
- Fast checks and realistic checks both matter, but they answer different questions.
- Clear assertions make failures easier to diagnose.
- Regression coverage should preserve lessons learned from real defects.
