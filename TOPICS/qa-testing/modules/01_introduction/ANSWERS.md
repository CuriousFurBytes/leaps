# Answers: Module 01 — Introduction to QA and Testing

## Answer Key

### Easy Questions (1 pt each)

**Q1:** Unit tests (the base of the pyramid). The pyramid model prescribes having the most tests at the unit level because they are the fastest and cheapest to write and maintain.

**Q2:** "I" stands for Isolated. An isolated unit test is completely independent from other tests — its outcome does not depend on any other test having run, and running it in any order produces the same result. Isolation is violated when tests share mutable global state.

**Q3:** Any three of: smoke tests, regression tests, performance/load tests, accessibility tests, contract tests, mutation tests, property-based tests, security tests, usability tests.

**Q4:** A smoke test is a minimal test suite that verifies the most critical functionality works. It is typically run immediately after a deployment to catch catastrophic failures before the full test suite runs. If smoke tests fail, the deployment is rolled back.

**Q5:** A regression test is a test added after a bug is discovered and fixed. Its purpose is to ensure the bug cannot silently reappear in future code changes. The creation of a regression test is triggered by finding and fixing a production (or staging) bug.

### Medium Questions (2 pts each)

**Q6:** The pyramid recommends many unit tests because they are fast (milliseconds), cheap to write, and precisely pinpoint failures. E2E tests are expensive because: (1) they are slow (minutes per test), (2) they are flaky (susceptible to timing issues, network problems, browser differences), (3) they are hard to maintain (any UI change can break many tests), and (4) when they fail, they don't pinpoint the cause — debugging requires investigating the entire stack.

**Q7:** The reasoning is wrong because coverage measures which lines were executed, not whether behavior was verified. Example: `def add(a, b): return a + b` with a test `def test_add(): add(2, 3)` (no assertion) achieves 100% line coverage but verifies nothing. Coverage is a floor (untested lines are definitely not tested) not a ceiling (tested lines are not necessarily well-tested).

**Q8:** Shift-left testing means moving testing activities earlier in the development lifecycle — "to the left" on a typical waterfall timeline. Instead of testing at the end, you test throughout. TDD is the most extreme form: you write tests before writing any implementation code. There is no earlier you can test than before the code exists.

**Q9:** AAA stands for Arrange, Act, Assert. Arrange: set up the test preconditions (create objects, configure mocks, prepare test data). Act: invoke the code under test (call the function, make the request). Assert: verify the outcome (check return values, verify side effects, inspect state). The pattern makes tests readable and reveals their purpose clearly.

**Q10:** Unit tests are faster (milliseconds vs. seconds), more isolated (no external dependencies), narrower in scope (one function/class), and easier to diagnose (failure points directly to the unit). Integration tests are slower, involve real or near-real dependencies, test cross-component behavior, and diagnose boundary failures. Choose unit tests for logic and behavior; choose integration tests when you need to verify that the database schema is correct, that HTTP serialization works, or that two services communicate as expected.

### Hard Questions (3 pts each)

**Q11:** Problems: (1) **Not Isolated / Not Fast** — `time.sleep(3)` makes the test slow; violates "Fast" and "Repeatable" (sleep duration is arbitrary). (2) **Not Isolated** — calls a real production API; the test outcome depends on external system availability. (3) **Not Self-Validating** — `print(f"Status: {response.status_code}")` with no assertion; a human must look at the output. (4) **Not Isolated** — `db_state["users"]` is shared mutable state; `test_user_count` depends on `test_register_user` running first. Correct rewrite: mock the HTTP call, use a local cart object per test, add an assertion.

**Q12:** Unit tests: mock the `EmailService` dependency; verify that `send_welcome_email` is called with the correct address. Integration tests: use a real email service stub (e.g., MailHog, a local SMTP server) and verify the email appears in the inbox. E2E test: register a user via the browser and verify a confirmation page appears (don't need to verify actual email delivery in E2E — that's the integration test's job). Pseudocode for unit level: `mock_email.assert_called_once_with(user.email, subject="Welcome")`.

**Q13:** Developer cost during coding: 0.5h × $100/hr = $50. Production bug cost: (8h dev × $100/hr) + (4h × $120/hr avg) = $800 + $480 = $1,280. Ratio: $1,280 / $50 ≈ 25.6x. This is before accounting for indirect costs (user churn, incident response, SLA penalties, reputation damage), which can multiply the production cost significantly. The calculation illustrates that even a modest estimate yields a 25x cost multiplier.

**Q14:** Four common causes of flakiness: (1) **Timing dependencies** — test asserts on state that hasn't propagated yet (async operations). Fix: use proper async waiting (`await expect(element).toBeVisible()`) rather than `sleep`. (2) **Shared mutable state** — test outcome depends on execution order. Fix: reset all shared state in `beforeEach`/`afterEach`. (3) **External service dependencies** — test calls a real API that may be slow or unavailable. Fix: mock external services in unit tests; use stable test environments in integration tests. (4) **Non-deterministic data** — test uses `random()` or `datetime.now()` without control. Fix: freeze time and seed random generators.

### Expert Questions (5 pts each)

**Q15:** A strong answer covers: Phase 1 — add a linter and enforce no-regression policy (any new code must have tests). Start with smoke tests for the most critical production flows. Identify the top 10 bugs that have occurred in production and write regression tests for them. Phase 2 — instrument coverage to find the uncovered hot paths (the code that is most frequently executed and most likely to have bugs). Write unit tests there. Phase 3 — add integration tests for the database and external service boundaries. Phase 4 — add E2E tests for the 3 most critical user journeys. Measurement: track coverage %, flaky test rate, time-to-detect bugs (does the test suite catch bugs before production?), and test suite execution time.

**Q16:** The testing trophy (Kent C. Dodds) argues that integration tests provide the most value and should form the bulk of the suite, with fewer unit tests and fewer E2E tests. The honeycomb (Spotify) emphasizes service-level integration tests in microservices. Answers that accurately describe a real model and synthesize its strengths and appropriate use cases deserve full credit. Accept any well-reasoned alternative including student-proposed models.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
