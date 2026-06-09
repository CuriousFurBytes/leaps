# QA and Testing — Projects

> Project ideas ranging from beginner to expert. Each project is designed to build real-world testing skills.
> Start with Beginner projects and work your way up.

---

## Beginner Projects

### Project 1: Calculator Library Test Suite

**Difficulty:** Beginner
**Estimated Time:** 3–5 hours
**Modules:** 01, 02

**Description:**
Write a complete test suite for a simple calculator library that supports addition, subtraction, multiplication, division, and square root. Focus on achieving meaningful coverage, including edge cases (division by zero, negative square roots, very large numbers).

**Deliverables:**
- A `calculator.py` (or `calculator.js`) implementation
- A test file with at least 20 tests organized into logical groups
- Coverage report showing ≥ 90% line coverage

**Success Criteria:**
- All tests pass
- Edge cases are explicitly tested (not just happy paths)
- Tests have clear, descriptive names that explain what they verify

---

### Project 2: String Utility Test Suite

**Difficulty:** Beginner
**Estimated Time:** 4–6 hours
**Modules:** 01, 02, 03

**Description:**
Write tests for a string utility library with functions: `truncate(text, max_len)`, `slugify(text)`, `extract_emails(text)`, and `count_words(text)`. Practice writing parametrized tests and testing with edge cases.

**Deliverables:**
- Tests using pytest parametrize (or Jest test.each) for data-driven scenarios
- At least 5 tests per function
- One mutation test run showing the mutation score

---

## Intermediate Projects

### Project 3: REST API Integration Test Suite

**Difficulty:** Intermediate
**Estimated Time:** 6–10 hours
**Modules:** 04, 06

**Description:**
Write an integration test suite for a simple CRUD REST API (user management: create, read, update, delete). Use a real test database (SQLite or PostgreSQL via Docker). Test both the happy path and error conditions (404, 409 conflict, 400 validation error).

**Deliverables:**
- Integration tests using pytest with a real database fixture
- Tests for all CRUD operations and error cases
- A `conftest.py` with database setup and teardown

**Success Criteria:**
- Tests run against a real database (not mocked)
- All HTTP status codes tested (200, 201, 400, 404, 409)
- Tests are isolated (each test starts with a clean database state)

---

### Project 4: E2E Test Suite with Playwright

**Difficulty:** Intermediate
**Estimated Time:** 8–12 hours
**Modules:** 05

**Description:**
Write an end-to-end test suite for a publicly accessible web application of your choice (e.g., a to-do app, a simple e-commerce demo, or a publicly available test site like [https://the-internet.herokuapp.com](https://the-internet.herokuapp.com)). Implement the page object model pattern.

**Deliverables:**
- Page object classes for each page under test
- At least 3 critical user journey tests
- A `playwright.config.ts` configured for headless CI execution

**Success Criteria:**
- Tests use locators that are resilient to minor UI changes (prefer `getByRole`, `getByLabel`, `getByTestId`)
- Page objects encapsulate all element interactions
- Tests pass in headless mode (CI-ready)

---

## Advanced Projects

### Project 5: TDD Kata — Bank Account

**Difficulty:** Advanced
**Estimated Time:** 6–8 hours
**Modules:** 07

**Description:**
Implement a `BankAccount` class using strict TDD. The class must support: `deposit(amount)`, `withdraw(amount)`, `get_balance()`, `get_statement()` (a formatted history). Write every test before writing any implementation code. Commit after each red/green/refactor cycle.

**Deliverables:**
- Git history showing the TDD cycles (each commit is a red, green, or refactor step)
- A `BankAccount` class with full test coverage
- A write-up (in NOTES.md) explaining decisions made during TDD

**Success Criteria:**
- Git log shows alternating "test: [failing]" and "impl: [passing]" commits
- No implementation code written before a failing test existed
- All edge cases (overdraft, negative deposit, zero balance) tested

---

### Project 6: Contract Test Suite with Pact

**Difficulty:** Advanced
**Estimated Time:** 8–12 hours
**Modules:** 06, 07

**Description:**
Build a consumer-provider contract test setup between two services: a frontend (consumer) that fetches user data and an API (provider). Write Pact consumer tests on the frontend side and provider verification tests on the API side. Simulate what happens when the provider makes a breaking change.

**Deliverables:**
- Consumer-side Pact tests in JavaScript
- Provider-side verification tests
- A documented demonstration of a breaking change being caught

---

## Expert Projects

### Project 7: Complete QA Strategy Document

**Difficulty:** Expert
**Estimated Time:** 10–15 hours
**Modules:** 11

**Description:**
Choose a real (or realistic fictional) application — an e-commerce platform, a SaaS product, a mobile API — and write a complete QA strategy document. Include: risk assessment, test plan, tool selection rationale, coverage targets, CI/CD integration plan, quality metrics, and on-call response procedures for test failures.

**Deliverables:**
- A QA strategy document (in NOTES.md or a dedicated file) covering all sections above
- A sample test plan for one sprint's worth of features
- Defined quality metrics with thresholds

---

### Project 8: Full QA Infrastructure for a Web Application

**Difficulty:** Expert
**Estimated Time:** 20–30 hours
**Modules:** All (capstone preparation)

**Description:**
Build a complete QA infrastructure for a real (or realistic) web application. The application should have at least a backend API and a frontend. Implement all four test tiers: unit tests with ≥ 90% coverage on critical paths, integration tests with a real database, E2E tests with Playwright covering 3+ user journeys, and a GitHub Actions CI pipeline that runs all tiers.

**Deliverables:**
- Working application with all four test tiers
- GitHub Actions workflow that runs on every PR
- Coverage report, E2E test report, and a QA metrics dashboard
- A README explaining the testing strategy

**Success Criteria:**
- Unit tests run in < 30 seconds
- Integration tests run in < 2 minutes
- E2E tests run in < 10 minutes in parallel
- CI pipeline blocks merges on test failure
