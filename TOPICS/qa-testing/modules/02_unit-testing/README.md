# Module 02: Unit Testing

[← Introduction](../01_introduction/) | [Topic Home](../../README.md) | [Next → Mocking and Test Doubles](../03_mocking-and-test-doubles/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner-green)
![Time](https://img.shields.io/badge/time-5--6h-orange)

---

> Writing effective unit tests, test isolation, the AAA pattern (Arrange/Act/Assert), code coverage — what it measures and what it doesn't — and mutation testing.

## Overview

This module is a stub. Content will be added in a future iteration.

**Topics covered in this module:**

- The AAA (Arrange/Act/Assert) pattern in depth — structuring tests for readability and maintainability
- Test isolation techniques — dependency injection, pure functions, and seam-based design
- pytest fixtures in depth — scope, parametrize, autouse, and sharing fixtures across files
- Jest configuration — TypeScript support, module resolution, coverage thresholds
- Code coverage — line, branch, function, and statement coverage; what each measures and what it misses
- Mutation testing with mutmut (Python) and Stryker (JavaScript) — measuring the quality of your test suite
- Property-based testing with Hypothesis (Python) — generating test cases automatically
- Test organization patterns — grouping by behavior vs. by module, naming conventions

## Prerequisites

- Module 01: Introduction to QA and Testing in this topic
- Basic Python or JavaScript programming

## Objectives

By the end of this module, you will be able to:

1. Apply the AAA pattern consistently to write readable, maintainable unit tests
2. Configure pytest and Jest for a real project with coverage reporting
3. Interpret coverage reports and identify meaningful gaps (not just line gaps)
4. Run mutation tests and interpret their output to improve test quality
5. Use pytest parametrize and Jest test.each to eliminate test duplication
6. Design functions and classes for testability (avoiding hidden dependencies)

## Cross-Links

- [[qa-testing/modules/01_introduction]] — The testing pyramid and FIRST principles established there are the foundation for this module
- [[qa-testing/modules/03_mocking-and-test-doubles]] — Mocking builds directly on unit testing concepts
- [[django-fastapi-flask]] — Django and FastAPI unit testing patterns use these same pytest foundations
