# Module 03: Mocking and Test Doubles

[← Unit Testing](../02_unit-testing/) | [Topic Home](../../README.md) | [Next → Integration Testing](../04_integration-testing/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner%E2%80%93Intermediate-yellowgreen)
![Time](https://img.shields.io/badge/time-5--6h-orange)

---

> Mocks vs. stubs vs. fakes vs. spies vs. dummies — the five test double types; when to mock; the over-mocking trap; Python's unittest.mock and pytest-mock; Jest mocks.

## Overview

This module is a stub. Content will be added in a future iteration.

**Topics covered in this module:**

- Gerard Meszaros's five test double types: dummy, stub, fake, spy, mock — precise definitions and when to use each
- Python's `unittest.mock` in depth — `MagicMock`, `patch`, `patch.object`, `side_effect`, `return_value`
- pytest-mock — cleaner mock API via the `mocker` fixture
- Jest mocks — `jest.fn()`, `jest.mock()`, `jest.spyOn()`, `mockReturnValue`, `mockImplementation`
- The over-mocking trap — when mocking makes tests brittle and meaningless
- Designing for testability — dependency injection patterns that make mocking easy
- Testing with time — freezing time in Python (freezegun) and JavaScript (jest.useFakeTimers)
- Testing randomness — seeding random number generators in tests

## Prerequisites

- Module 02: Unit Testing in this topic
- Basic understanding of Python modules and JavaScript modules

## Objectives

By the end of this module, you will be able to:

1. Identify the correct test double type for any given scenario
2. Use Python's `unittest.mock.patch` to intercept and control dependencies
3. Use Jest's mock functions and module mocking to isolate JavaScript code
4. Recognize over-mocking and refactor tests that are too tightly coupled to implementation
5. Design code with dependency injection to make mocking natural
6. Mock time and randomness to make tests deterministic

## Cross-Links

- [[qa-testing/modules/02_unit-testing]] — Unit testing concepts that this module extends
- [[qa-testing/modules/04_integration-testing]] — Integration tests deliberately avoid mocking; understanding the contrast is important
- [[qa-testing/glossary#test-double]] — Formal definition of test doubles
