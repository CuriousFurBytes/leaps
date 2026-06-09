# Software Quality Testing

> A zero-to-expert path for QA practice, unit tests, integration tests, E2E tests, and regression tests.

## Table of Contents
1. [Why Learn Software Quality Testing?](#why-learn-software-quality-testing)
2. [Prerequisites](#prerequisites)
3. [Module Map](#module-map)
4. [Cross-Links](#cross-links)
5. [Quick Reference](#quick-reference)

## Why Learn Software Quality Testing?

Software quality testing is the discipline of discovering whether a system behaves as expected, keeps behaving that way as it changes, and gives teams trustworthy information about release risk. It includes human judgment, automation, test design, tooling, and communication with product and engineering partners.

Modern QA grew from manufacturing quality control, formal software verification, and agile engineering practices. Early software teams often treated testing as a final inspection step; contemporary teams increasingly shift quality earlier by designing testable systems, writing automated checks alongside code, and using production feedback to improve test strategy.

This topic matters because defects are not only coding mistakes. They can be misunderstood requirements, weak observability, risky deployments, environmental drift, inaccessible workflows, brittle dependencies, or regressions in behavior that used to work. A skilled quality practitioner learns to ask where failure is likely, which evidence is credible, and how much confidence is enough for a given release.

By the end of this path, you should be able to design a layered test strategy, write maintainable automated checks, choose between unit, integration, E2E, exploratory, and regression approaches, and explain the tradeoffs to stakeholders in business language.

## Prerequisites

- Basic programming in one language such as JavaScript, Python, Java, C#, or Go.
- Familiarity with command-line workflows and version control; see [[git]] if available.
- Basic web concepts such as HTTP requests, APIs, browsers, and databases; see [[web-development]] and [[databases]] if available.
- No prior QA experience is assumed.

## Module Map

| # | Module | Difficulty | Status |
|---|--------|------------|--------|
| 01 | [Quality Foundations](./modules/01_quality_foundations/README.md) | Beginner | [ ] |
| 02 | [Unit Testing](./modules/02_unit_testing/README.md) | Beginner | [ ] |
| 03 | [Integration Testing](./modules/03_integration_testing/README.md) | Intermediate | [ ] |
| 04 | E2E Testing | Intermediate | [ ] |
| 05 | Regression Testing | Intermediate | [ ] |
| 06 | Test Data and Environments | Advanced | [ ] |
| 07 | CI Quality Gates and Flake Management | Advanced | [ ] |
| 08 | Exploratory Testing and Bug Advocacy | Advanced | [ ] |
| 09 | Performance, Security, and Accessibility Quality | Advanced | [ ] |
| 10 | Quality Metrics, Risk, and Release Strategy | Expert | [ ] |
| 11 | Test Architecture and Organizational Quality | Expert | [ ] |
| 12 | [Capstone Project](./modules/12_capstone_project/README.md) | Expert | [ ] |

## Cross-Links

- [[software-engineering]]
- [[web-development]]
- [[databases]]
- [[devops]]
- [[shared/glossary#regression]]

## Quick Reference

| Concept | Use it when | Watch out for |
|---|---|---|
| QA | You need a complete quality practice, not just scripts | Treating QA as only post-development inspection |
| Unit test | You need fast feedback on isolated logic | Over-mocking until tests no longer represent useful behavior |
| Integration test | You need confidence that components collaborate correctly | Environments that are slower or less deterministic than expected |
| E2E test | You need proof that a user-critical journey works through the whole stack | Brittle selectors, excessive coverage, and hard debugging |
| Regression test | A bug must stay fixed forever | Adding tests without understanding the failure mode |
| Test pyramid | You need a portfolio model for fast and slow checks | Interpreting it as a rigid quota instead of a risk heuristic |
