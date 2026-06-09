# Module 05: End-to-End Testing

[← Integration Testing](../04_integration-testing/) | [Topic Home](../../README.md) | [Next → API Testing](../06_api-testing/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate-yellow)
![Time](https://img.shields.io/badge/time-7--9h-orange)

---

> Playwright vs. Cypress — architecture comparison; page object model; locator strategies; visual regression testing; parallelization; CI/CD integration.

## Overview

This module is a stub. Content will be added in a future iteration.

**Topics covered in this module:**

- The E2E testing landscape: Playwright vs. Cypress — architectural differences, trade-offs, when to choose each
- Playwright setup and configuration — `playwright.config.ts`, browser selection, headless vs. headed
- Locator strategies — semantic locators (`getByRole`, `getByLabel`) vs. CSS selectors; why semantic locators are preferred
- The Page Object Model (POM) — encapsulating page interactions for maintainability
- Writing resilient E2E tests — avoiding timing issues, using `waitFor` correctly, retries
- Visual regression testing — capturing screenshots and comparing diffs with Playwright
- Parallelization — running E2E tests in parallel across multiple workers
- CI/CD integration — configuring Playwright in GitHub Actions, artifacts, and reporting
- Cypress comparison — Cypress's `cy.intercept()` for network stubbing, time travel debugging

## Prerequisites

- Module 04: Integration Testing in this topic
- Basic HTML and JavaScript knowledge — understanding the DOM, form elements, buttons

## Objectives

By the end of this module, you will be able to:

1. Install and configure Playwright for a web application test suite
2. Write E2E tests using semantic locators that are resilient to UI changes
3. Implement the page object model pattern to organize E2E tests
4. Configure E2E tests to run in parallel in a CI/CD pipeline
5. Distinguish between Playwright and Cypress and select the appropriate tool
6. Debug flaky E2E tests using Playwright's trace viewer and verbose output

## Cross-Links

- [[qa-testing/modules/04_integration-testing]] — Integration tests cover the backend; E2E tests add the browser layer
- [[javascript-typescript-react]] — React component testing with Testing Library is a complementary approach to full E2E
- [[devops-platform-engineering]] — CI/CD pipeline configuration for running E2E tests at scale
