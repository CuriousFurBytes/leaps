# Module 08: Behavior-Driven Development

[← Test-Driven Development](../07_test-driven-development/) | [Topic Home](../../README.md) | [Next → Performance Testing](../09_performance-testing/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate%E2%80%93Advanced-orange)
![Time](https://img.shields.io/badge/time-6--7h-orange)

---

> Gherkin syntax; Cucumber and Behave; writing scenarios with non-technical stakeholders; living documentation; BDD pitfalls.

## Overview

This module is a stub. Content will be added in a future iteration.

**Topics covered in this module:**

- What BDD is and why Dan North invented it — the gap between TDD tests and business requirements
- Gherkin syntax — Feature, Scenario, Given/When/Then, Background, Scenario Outline, Examples
- Behave (Python) — step definitions, context, hooks, table parameters
- Cucumber (JavaScript/Java) — `@Given`, `@When`, `@Then`, world objects
- Writing good scenarios — the "so that" format, one behavior per scenario, avoiding UI details in Gherkin
- Collaborating with non-technical stakeholders — the "three amigos" meeting (developer, tester, business analyst)
- Living documentation — keeping Gherkin scenarios as the authoritative specification
- BDD pitfalls — writing Gherkin for already-implemented code, too many scenarios, scenarios that test implementation

## Prerequisites

- Module 07: Test-Driven Development in this topic
- Some exposure to requirements gathering or user stories

## Objectives

By the end of this module, you will be able to:

1. Write Gherkin scenarios that express business behavior clearly, without implementation details
2. Implement step definitions in Behave (Python) that execute the Gherkin scenarios
3. Use Scenario Outlines to test multiple data combinations without duplicating scenarios
4. Distinguish good BDD scenarios from bad ones using established criteria
5. Run a Behave suite and interpret the output

## Cross-Links

- [[qa-testing/modules/07_test-driven-development]] — BDD extends TDD into the requirements layer
- [[django-fastapi-flask]] — Django BDD testing with Behave is a common combination
- [[qa-testing/modules/11_qa-strategy-and-metrics]] — BDD feeds into QA strategy as living documentation
