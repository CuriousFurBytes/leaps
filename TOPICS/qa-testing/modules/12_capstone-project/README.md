# Module 12: Capstone Project

[← QA Strategy and Metrics](../11_qa-strategy-and-metrics/) | [Topic Home](../../README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Expert-darkred)
![Time](https://img.shields.io/badge/time-20--30h-orange)

---

> Build a complete QA infrastructure for a real application: unit tests (90%+ coverage on critical paths), integration tests with TestContainers, E2E tests with Playwright, a CI pipeline that runs all test tiers, and a QA strategy document.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Brief](#project-brief)
4. [Milestones](#milestones)
5. [Acceptance Criteria](#acceptance-criteria)
6. [Getting Unstuck](#getting-unstuck)
7. [Submission](#submission)

---

## Overview

This is the capstone project for the QA and Testing topic. You will build a complete, professional-grade QA infrastructure for a web application — everything from unit tests to CI pipeline configuration to a QA strategy document.

This module is intentionally build-oriented, not lecture-oriented. There is no new theory here — everything you need was covered in Modules 01–11. Your job is to synthesize those concepts into a coherent, working system.

> [!IMPORTANT]
> This module does not provide a complete solution. The learning happens in the building. Staged hints are available in the [Getting Unstuck](#getting-unstuck) section, but you should attempt each milestone independently before consulting them. A capstone solution you can point to on a resume requires that you built it yourself.

**Difficulty:** Expert &nbsp;|&nbsp; **Estimated time:** 20–30 hours

---

## Prerequisites

- All 11 preceding modules completed (or at minimum: 01, 02, 03, 04, 05, 07, 11)
- A working Python environment with pytest, httpx, and playwright installed
- Docker installed (for TestContainers)
- A GitHub account (for CI pipeline)

---

## Project Brief

You will implement a complete QA strategy for a **Task Management API** — a simple but realistic REST API that allows users to manage tasks (create, read, update, delete, assign, mark complete).

The application has these layers:
- A Python/FastAPI (or Django REST Framework) HTTP API
- A PostgreSQL database
- A frontend web interface (can be simple HTML or a React app)
- An email notification service (mocked)

You are responsible for all four test tiers and the supporting infrastructure.

---

## Milestones

### Milestone 1: Unit Test Suite

Write unit tests for the business logic layer of the application (task creation, validation rules, assignment rules, status transitions).

**Requirements:**
- ≥ 90% line coverage on the business logic module
- ≥ 80% branch coverage
- No database calls in unit tests (all dependencies mocked)
- Tests run in < 10 seconds total
- At least 5 parametrized tests for validation rules

**Deliverable:** `tests/unit/` directory with complete test suite and coverage report.

---

### Milestone 2: Integration Test Suite

Write integration tests for the API endpoints and the database layer.

**Requirements:**
- Tests use a real PostgreSQL database in a Docker container (via TestContainers or pytest-docker)
- All CRUD endpoints tested: create, read, update, delete
- All error cases tested: 400 validation errors, 404 not found, 409 conflict
- Each test runs against a clean database state (no test order dependencies)
- Tests run in < 2 minutes total

**Deliverable:** `tests/integration/` directory with test suite and a conftest.py managing the database fixture.

---

### Milestone 3: E2E Test Suite

Write end-to-end tests with Playwright for the three most critical user journeys.

**Requirements:**
- Page object model pattern used (at least 2 page classes)
- All locators use semantic selectors (`getByRole`, `getByLabel`, `getByTestId`)
- Tests cover: (1) user creates and completes a task, (2) user assigns a task to another user, (3) user searches and filters tasks
- Tests pass in headless mode
- Tests run in < 10 minutes with parallelization

**Deliverable:** `tests/e2e/` directory with test suite and `playwright.config.ts`.

---

### Milestone 4: CI Pipeline

Create a GitHub Actions workflow that runs all three test tiers automatically.

**Requirements:**
- Workflow triggers on: push to `main`, and on every pull request
- Unit tests run first (fastest feedback)
- Integration tests run second (require database)
- E2E tests run last (slowest)
- Pipeline fails the PR if any tier fails
- Coverage report is published as a PR comment
- E2E test artifacts (screenshots, traces) are uploaded on failure

**Deliverable:** `.github/workflows/test.yml` with working CI configuration.

---

### Milestone 5: QA Strategy Document

Write a QA strategy document for the Task Management application.

**Requirements:**
- Risk assessment: identify the 3 highest-risk areas and why
- Test plan: what each test tier covers and what it doesn't
- Quality metrics: define thresholds for coverage, flaky rate, and test execution time
- On-call runbook: what to do when the CI pipeline fails in each tier
- Retrospective section: what you would do differently if starting over

**Deliverable:** `QA_STRATEGY.md` in the project root.

---

## Acceptance Criteria

The capstone is complete when:

- [ ] `pytest tests/unit/ --cov=src/business_logic --cov-report=term-missing` shows ≥ 90% coverage
- [ ] `pytest tests/integration/` passes with all endpoints and error cases covered
- [ ] `npx playwright test` passes in headless mode with all three user journeys
- [ ] The GitHub Actions workflow runs successfully on a test PR
- [ ] `QA_STRATEGY.md` contains all five required sections with substantive content
- [ ] All test tiers are independent — each can be run without the others passing

---

## Getting Unstuck

Work through each milestone before consulting these hints. If you're genuinely blocked, expand the hint for the milestone you're working on.

<details>
<summary>Milestone 1 Hints — Unit Tests</summary>

- Start by identifying the business logic functions: `validate_task(data)`, `can_assign_task(user, task)`, `transition_status(task, new_status)`. These are the functions to unit test first.
- If you're not sure what to test, read the requirements and convert each rule into a test: "task title must be between 1 and 255 characters" → `test_validate_task_rejects_empty_title`, `test_validate_task_rejects_title_over_255_chars`.
- For mocking the database, use `unittest.mock.MagicMock()` for the repository object and configure `return_value` for each method your business logic calls.
- Coverage gaps often appear in error handling branches. Make sure you have tests that exercise every `if`, `elif`, `else`, and `raise` in your business logic.

See: [[qa-testing/modules/02_unit-testing]], [[qa-testing/modules/03_mocking-and-test-doubles]]
</details>

<details>
<summary>Milestone 2 Hints — Integration Tests</summary>

- The cleanest approach: use a pytest fixture with `scope="session"` to start the PostgreSQL container once, and a `scope="function"` fixture that wraps each test in a transaction and rolls it back at the end.
- For TestContainers: `from testcontainers.postgres import PostgresContainer`. Start the container in a session-scoped fixture, run migrations inside it, then yield the connection URL.
- Test the error cases by deliberately sending invalid data: missing required fields, duplicate records, referencing non-existent IDs.
- If tests are interdependent (one test's data affects another), your isolation is broken. Check that your rollback fixture is working.

See: [[qa-testing/modules/04_integration-testing]]
</details>

<details>
<summary>Milestone 3 Hints — E2E Tests</summary>

- Start by creating page objects for the Login page and the Task List page before writing any tests.
- If your tests are flaky, the most likely cause is an async operation that hasn't completed. Replace `time.sleep()` with `await expect(locator).toBeVisible()`.
- For the search/filter journey, test that filtering by "completed" status shows only completed tasks — this requires creating tasks with different states first.
- Playwright's trace viewer (`--trace on`) is invaluable for debugging failures: `npx playwright show-trace trace.zip`.

See: [[qa-testing/modules/05_e2e-testing]]
</details>

<details>
<summary>Milestone 4 Hints — CI Pipeline</summary>

- PostgreSQL in GitHub Actions: use the `services:` block in your workflow YAML to start a PostgreSQL service container. Set `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, and map port 5432.
- For E2E tests, install Playwright browsers with: `npx playwright install --with-deps chromium`.
- Upload artifacts with `actions/upload-artifact@v4` in an `if: failure()` step.
- For coverage comments on PRs, the `pytest-cov` plugin generates XML that can be posted as a PR comment using a GitHub Action like `MishaKav/pytest-coverage-comment`.

See: [[devops-platform-engineering]] (Module 06, CI/CD Pipelines)
</details>

<details>
<summary>Milestone 5 Hints — QA Strategy</summary>

- For the risk assessment, think about: Which parts of the application handle money or sensitive data? Which features have the most complex business logic? Which parts have the highest user traffic?
- A useful quality metric format: "Metric: defect escape rate. Target: < 5% of bugs found in production. Current: unknown. Measurement: track bugs reported via Sentry vs. bugs caught in CI."
- The retrospective is where the real learning is. Be honest: did you discover that E2E tests were harder to maintain than expected? Did coverage alone mislead you? Document what you would do differently.

See: [[qa-testing/modules/11_qa-strategy-and-metrics]]
</details>

---

## Submission

When complete:

1. Commit your code to a GitHub repository
2. Ensure the CI pipeline runs and all tests pass
3. Update `TOPICS/qa-testing/PROGRESS.md` to mark this module complete
4. Add a journal entry in `TOPICS/qa-testing/README.md` describing what you built and what you learned
5. Add your project link to the topic-level Projects table

Congratulations on completing the QA and Testing topic.
