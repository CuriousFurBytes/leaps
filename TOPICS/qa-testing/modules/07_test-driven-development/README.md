# Module 07: Test-Driven Development

[← API Testing](../06_api-testing/) | [Topic Home](../../README.md) | [Next → Behavior-Driven Development](../08_behavior-driven-development/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate%E2%80%93Advanced-orange)
![Time](https://img.shields.io/badge/time-7--9h-orange)

---

> Red/green/refactor cycle; designing for testability; TDD katas; when TDD works best — and when it doesn't.

## Overview

This module is a stub. Content will be added in a future iteration.

**Topics covered in this module:**

- The red/green/refactor cycle — precise mechanics, what each phase requires, how long to stay in each
- Kent Beck's original TDD vision — what TDD is *actually* for (design feedback, not just coverage)
- "Fake it till you make it" and triangulation — TDD techniques for building up implementations incrementally
- Designing for testability — what makes code hard to test and how to fix it (DI, pure functions, seams)
- TDD katas — practice exercises for developing TDD fluency: FizzBuzz, Roman Numerals, Word Wrap, Bank Account
- TDD with databases and external services — outside-in TDD (London school) vs. inside-out (classicist)
- When TDD works best — greenfield code, well-understood requirements, refactoring
- When TDD struggles — exploratory code, UI, performance-critical code, unclear requirements
- The TDD controversy — critiques (David Heinemeier Hansson), defenses (Kent Beck), the middle ground

## Prerequisites

- Module 03: Mocking and Test Doubles in this topic
- Module 02: Unit Testing in this topic — TDD requires fluency with writing unit tests quickly

## Objectives

By the end of this module, you will be able to:

1. Apply the red/green/refactor cycle to develop a function from a blank file to a complete implementation
2. Complete at least two TDD katas (FizzBuzz + one other) with git history showing each cycle
3. Identify code that is hard to test and refactor it using dependency injection
4. Distinguish between the London School (outside-in, mocks-heavy) and Detroit School (inside-out, classicist) TDD styles
5. Articulate the legitimate criticisms of TDD and when it is and isn't the right approach

## Cross-Links

- [[qa-testing/modules/02_unit-testing]] — Unit testing fluency is a prerequisite for TDD
- [[qa-testing/modules/03_mocking-and-test-doubles]] — The London School of TDD relies heavily on mocks
- [[qa-testing/glossary#test-driven-development]] — Formal definition and history
