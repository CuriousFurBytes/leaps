# Module 11: QA Strategy and Metrics

[← Accessibility Testing](../10_accessibility-testing/) | [Topic Home](../../README.md) | [Next → Capstone Project](../12_capstone-project/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Expert-darkred)
![Time](https://img.shields.io/badge/time-8--10h-orange)

---

> Test plans; risk-based testing prioritization; test management concepts; quality metrics (defect escape rate, flaky test rate); QA in CI/CD pipelines.

## Overview

This module is a stub. Content will be added in a future iteration.

**Topics covered in this module:**

- The QA strategy document — what it contains, who reads it, how it changes across the project lifecycle
- Risk-based testing — identifying and prioritizing the highest-risk areas of a system; risk matrices
- Test planning — scope, entry/exit criteria, resource estimation, schedule
- Test management concepts — defect lifecycle, test case management (TestRail-style concepts), traceability
- Quality metrics that matter:
  - Defect escape rate (bugs found in production / bugs found total)
  - Flaky test rate (flaky tests / total tests — should be < 1%)
  - Mean time to detect (how long from bug introduction to detection)
  - Test suite execution time (should fit CI/CD pipeline budget)
  - Mutation score (quality of test coverage)
- QA in CI/CD pipelines — test tiers, parallelization, quality gates, merge blocking
- Building a QA culture — working with developers, product managers, and stakeholders
- QA in Agile — testing within sprints, Definition of Done with testing criteria
- Shift-left and DevOps testing — developer-owned quality, test-in-production strategies

## Prerequisites

- All previous modules in this topic (01–10)
- Understanding of software development processes (Agile, CI/CD)

## Objectives

By the end of this module, you will be able to:

1. Write a QA strategy document for a real or realistic application
2. Apply risk-based prioritization to a test suite, focusing effort on high-risk areas
3. Define and track quality metrics that are meaningful and actionable
4. Design a CI/CD pipeline test strategy with appropriate quality gates
5. Articulate the tradeoffs between testing thoroughness and development velocity
6. Build the case for QA investment using economic arguments and quality metrics

## Cross-Links

- [[devops-platform-engineering]] — CI/CD pipelines are the infrastructure for this module's quality gates
- [[feature-flags-monitoring]] — Monitoring provides the production-side quality signal that complements testing
- [[qa-testing/modules/12_capstone-project]] — This module provides the strategy framework for the capstone
