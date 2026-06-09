# QA and Testing — Glossary

> A living reference. Add terms as you encounter them — don't wait until you understand them perfectly.
> Writing a definition in your own words is itself a powerful learning tool.

---

## How to Add a Term

Copy this template and fill it in:

```markdown
### term-name

**Definition:** A clear, concise explanation of what this term means in the context of QA and Testing.

**Also known as:** Other names, abbreviations, or synonyms (if any).

**Related:** [[related-concept]], [[another-related-concept]]

**Example:**
A concrete, specific example of the term in use.
```

Keep definitions in your own words as much as possible. If you're copying from a source, add attribution.

---

## C

### contract test

**Definition:** A test that verifies the interface between two services matches an agreed-upon contract. In consumer-driven contract testing (e.g., with Pact), the consumer defines the contract and the provider verifies it independently. This allows services to be tested in isolation while still ensuring compatibility.

**Also known as:** consumer-driven contract test, CDC test

**Related:** [[integration-test]], [[qa-testing/modules/06_api-testing]]

**Example:**
A billing service (consumer) specifies that it expects the user service to return `{ "id": 123, "email": "user@example.com" }`. The user service runs a provider test to verify it can fulfill that contract without either service needing to be running simultaneously.

---

### coverage

**Definition:** A measure of how much of the source code is exercised by a test suite, typically expressed as a percentage. Line coverage measures which lines were executed; branch coverage measures which conditional branches were taken. 100% coverage does not mean the code is correct — it only means every line was executed at least once.

**Also known as:** code coverage, test coverage

**Related:** [[mutation-testing]], [[unit-test]]

**Example:**
```python
def divide(a, b):
    if b == 0:          # branch 1: b is zero
        return None
    return a / b        # branch 2: b is non-zero

# This test achieves 50% branch coverage (only one branch tested):
def test_divide():
    assert divide(10, 2) == 5.0
```

---

## E

### end-to-end test

**Definition:** A test that exercises a complete user journey through the application from the user interface down through all layers to the database and back, verifying that the entire system works together as intended.

**Also known as:** E2E test, UI test, browser test, acceptance test (in some contexts)

**Related:** [[test-pyramid]], [[integration-test]], [[qa-testing/modules/05_e2e-testing]]

**Example:**
A Playwright test that opens a browser, navigates to a login page, fills in credentials, clicks submit, and asserts the dashboard is shown — exercising the frontend, HTTP layer, authentication service, and database in sequence.

---

## F

### fixture

**Definition:** A fixed state of a system (data, objects, or configuration) that serves as the baseline for a test. Fixtures are set up before a test runs and torn down after. In pytest, fixtures are functions decorated with `@pytest.fixture`; in testing generally, the term encompasses any consistent test precondition.

**Also known as:** test fixture, test setup, baseline

**Related:** [[unit-test]], [[qa-testing/modules/02_unit-testing]]

**Example:**
```python
import pytest

@pytest.fixture
def sample_user():
    # Set up
    return {"id": 1, "name": "Alice", "email": "alice@example.com"}

def test_user_has_name(sample_user):
    assert sample_user["name"] == "Alice"
```

---

### flaky test

**Definition:** A test that produces inconsistent results (passing sometimes, failing sometimes) without any change to the code under test. Flaky tests are caused by factors such as timing dependencies, shared mutable state, network calls, or non-deterministic ordering. They erode trust in test suites because developers learn to re-run failing tests rather than investigate them.

**Also known as:** non-deterministic test, intermittent failure

**Related:** [[e2e-test]], [[integration-test]]

**Example:**
An E2E test that asserts an element is visible immediately after a click, but the click triggers an async operation. The test passes when the operation is fast and fails when it is slow — a timing dependency that makes the test flaky.

---

## I

### integration test

**Definition:** A test that verifies the interaction between two or more components of a system. Unlike unit tests, integration tests do not isolate components from their dependencies — they test the actual interaction. The dependencies may be real (a real database) or simulated (an in-memory database or test container).

**Also known as:** component test (sometimes), service test (sometimes)

**Related:** [[unit-test]], [[e2e-test]], [[test-pyramid]], [[qa-testing/modules/04_integration-testing]]

**Example:**
A test that calls a repository function and verifies it correctly writes to and reads from a real PostgreSQL test database, exercising the SQL queries and data mapping layer together.

---

## M

### mocking

**Definition:** The practice of replacing a real dependency with a controlled substitute (a mock object) in tests. A mock records interactions (calls, arguments) and can be configured to return specific values or raise specific errors. Mocking isolates the code under test from external dependencies like databases, APIs, or clocks.

**Also known as:** test mocking, object mocking

**Related:** [[stubbing]], [[test-double]], [[qa-testing/modules/03_mocking-and-test-doubles]]

**Example:**
```python
from unittest.mock import MagicMock

def send_welcome_email(user, email_service):
    email_service.send(user["email"], "Welcome!")

def test_welcome_email_is_sent():
    mock_email = MagicMock()
    send_welcome_email({"email": "a@b.com"}, mock_email)
    mock_email.send.assert_called_once_with("a@b.com", "Welcome!")
```

---

### mutation testing

**Definition:** A testing technique that evaluates the quality of a test suite by introducing small, deliberate code changes ("mutants") into the source code and checking whether the test suite detects those changes (i.e., at least one test fails). A high mutation score indicates that the tests are sensitive to real bugs. A low mutation score reveals gaps in test effectiveness even when code coverage appears high.

**Also known as:** mutation analysis

**Related:** [[coverage]], [[unit-test]]

**Example:**
A mutant might change `if balance >= amount` to `if balance > amount`. If no test catches this change (i.e., all tests still pass), the mutation survives — indicating a gap in test coverage for the boundary condition.

---

## R

### regression test

**Definition:** A test that verifies that previously working functionality still works after a code change. Regression tests are typically added when a bug is found and fixed; the test ensures the bug does not reappear. Over time, a regression test suite becomes the institutional memory of bugs that were once found in production.

**Also known as:** regression check

**Related:** [[unit-test]], [[integration-test]]

**Example:**
After finding that a discount calculation incorrectly applies negative discounts, a developer adds a test asserting `apply_discount(price=100, discount=-10) == 100`. This test prevents the bug from being reintroduced in future refactors.

---

## S

### smoke test

**Definition:** A minimal set of tests that verify the most critical functionality of a system is working, typically run as the first check after a deployment or build. Smoke tests are intentionally shallow and fast — their purpose is to catch catastrophic failures before running the full test suite.

**Also known as:** sanity test, build verification test (BVT)

**Related:** [[regression-test]], [[e2e-test]]

**Example:**
After deploying an API, a smoke test suite calls the `/health` endpoint, performs a login, and fetches one resource. If any of these fail, the deployment is rolled back immediately without running the full 30-minute test suite.

---

### stubbing

**Definition:** The practice of replacing a dependency with a simplified implementation (a stub) that returns hardcoded or pre-configured responses. Unlike mocks, stubs do not verify that they were called in a specific way — they just provide controlled return values. Stubs are used to isolate the code under test from unpredictable or slow dependencies.

**Also known as:** test stub, service stub

**Related:** [[mocking]], [[test-double]]

**Example:**
```python
class StubPaymentGateway:
    def charge(self, amount, card_token):
        return {"status": "success", "transaction_id": "fake-123"}

def test_order_creation_on_payment_success():
    gateway = StubPaymentGateway()
    order = create_order(amount=50.00, card="tok_test", gateway=gateway)
    assert order.status == "paid"
```

---

## T

### test double

**Definition:** The general term for any object that stands in for a real dependency in a test. The term was coined by Gerard Meszaros and encompasses five subtypes: dummies (objects passed but never used), stubs (provide canned responses), fakes (working implementations too simple for production), spies (record interactions), and mocks (pre-programmed with expectations).

**Also known as:** test substitute, stand-in

**Related:** [[mocking]], [[stubbing]], [[qa-testing/modules/03_mocking-and-test-doubles]]

**Example:**
The five subtypes in one list: a Dummy is an empty logger object passed to a function that doesn't call it; a Stub returns a fixed HTTP response; a Fake is an in-memory database; a Spy records how many times a method was called; a Mock verifies the exact sequence of calls and arguments.

---

### test-driven development

**Definition:** A software development practice in which tests are written before the implementation code. The cycle is: write a failing test (red) → write the minimum code to make it pass (green) → refactor the code while keeping tests green (refactor). TDD was formalized by Kent Beck in 1999 as part of Extreme Programming.

**Also known as:** TDD, red/green/refactor

**Related:** [[unit-test]], [[qa-testing/modules/07_test-driven-development]]

**Example:**
Before writing a `validate_email()` function, a developer writes `assert validate_email("bad") == False` and `assert validate_email("a@b.com") == True`. These tests fail (red). The developer then writes the minimal implementation. Tests pass (green). The developer refactors for clarity. Cycle repeats.

---

### test pyramid

**Definition:** A conceptual model for structuring test suites, typically depicted as a triangle with unit tests at the base (many, fast, cheap), integration tests in the middle, and E2E tests at the top (few, slow, expensive). The pyramid shape represents the recommended proportion of each type: many unit tests, some integration tests, and few E2E tests.

**Also known as:** testing pyramid, test automation pyramid

**Related:** [[unit-test]], [[integration-test]], [[e2e-test]], [[qa-testing/modules/01_introduction]]

**Example:**
A healthy test suite for a web application might have 500 unit tests (run in 10 seconds), 50 integration tests (run in 2 minutes), and 20 E2E tests (run in 10 minutes). The ratio reflects the pyramid: abundant fast tests, fewer slow ones.

---

### unit test

**Definition:** A test that verifies the behavior of a single, isolated unit of code — typically a function, method, or class — by controlling all its dependencies through test doubles or direct invocation. Unit tests are fast (milliseconds), independent of external systems, and form the base of the testing pyramid.

**Also known as:** unit test, isolated test

**Related:** [[test-pyramid]], [[integration-test]], [[qa-testing/modules/02_unit-testing]]

**Example:**
```python
def add(a: int, b: int) -> int:
    return a + b

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_with_zero():
    assert add(0, 5) == 5

def test_add_negative_numbers():
    assert add(-2, -3) == -5
```

---

## Glossary Stats

| Metric | Count |
|--------|-------|
| Total terms defined | 15 |
| Terms pending definition | 0 |
| Last updated | 2026-06-09 |
