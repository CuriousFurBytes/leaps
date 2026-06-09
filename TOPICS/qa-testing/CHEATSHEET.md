# QA and Testing — Cheat Sheet

> Quick reference for pytest patterns, Jest patterns, mock idioms, and Playwright locator strategies.

---

## Table of Contents

- [pytest Cheat Sheet](#pytest-cheat-sheet)
- [Jest Cheat Sheet](#jest-cheat-sheet)
- [Common Mock Patterns](#common-mock-patterns)
- [Playwright Locator Strategies](#playwright-locator-strategies)
- [Testing Pyramid Quick Reference](#testing-pyramid-quick-reference)
- [FIRST Principles Quick Reference](#first-principles-quick-reference)

---

## pytest Cheat Sheet

### Installation and Running

```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest

# Run tests in a specific file
pytest tests/test_calculator.py

# Run a specific test
pytest tests/test_calculator.py::test_add_positive_numbers

# Run tests matching a keyword
pytest -k "add"

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run with coverage HTML report
pytest --cov=src --cov-report=html

# Stop after first failure
pytest -x

# Show print output (don't capture stdout)
pytest -s
```

### Basic Test Structure

```python
# tests/test_calculator.py

def test_add_two_numbers():
    # Arrange
    a, b = 2, 3
    # Act
    result = add(a, b)
    # Assert
    assert result == 5

def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

### Fixtures

```python
import pytest

@pytest.fixture
def db_connection():
    """Set up a test database connection."""
    conn = create_test_db()
    yield conn          # test runs here
    conn.close()        # teardown after test

@pytest.fixture(scope="module")
def expensive_resource():
    """Created once per module, shared across all tests in the module."""
    return load_large_dataset()

def test_query(db_connection):
    result = db_connection.execute("SELECT 1")
    assert result == 1
```

### Parametrize

```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -50, 50),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### Marks

```python
import pytest

@pytest.mark.slow
def test_large_dataset():
    ...

@pytest.mark.skip(reason="not implemented yet")
def test_future_feature():
    ...

@pytest.mark.xfail(reason="known bug #123")
def test_known_broken():
    ...
```

### conftest.py

```python
# tests/conftest.py — fixtures available to all tests in the directory

import pytest
from myapp import create_app, db

@pytest.fixture(scope="session")
def app():
    app = create_app(testing=True)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def reset_db(app):
    """Automatically reset database before each test."""
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()
```

---

## Jest Cheat Sheet

### Installation and Running

```bash
# Install Jest
npm install --save-dev jest

# For TypeScript
npm install --save-dev ts-jest @types/jest

# Run all tests
npx jest

# Run in watch mode
npx jest --watch

# Run with coverage
npx jest --coverage

# Run a specific file
npx jest calculator.test.js

# Run tests matching a pattern
npx jest --testNamePattern="add"
```

### Basic Test Structure

```javascript
// calculator.test.js

describe('Calculator', () => {
  test('adds two numbers', () => {
    // Arrange
    const a = 2, b = 3;
    // Act
    const result = add(a, b);
    // Assert
    expect(result).toBe(5);
  });

  test('throws on division by zero', () => {
    expect(() => divide(10, 0)).toThrow('Division by zero');
  });
});
```

### Common Matchers

```javascript
expect(value).toBe(5);                    // strict equality (===)
expect(value).toEqual({ a: 1 });          // deep equality
expect(value).toBeTruthy();               // truthy value
expect(value).toBeFalsy();                // falsy value
expect(array).toContain('item');          // array contains item
expect(string).toMatch(/pattern/);        // regex match
expect(fn).toThrow();                     // function throws
expect(fn).toThrow('message');            // throws with message
expect(mockFn).toHaveBeenCalled();        // mock was called
expect(mockFn).toHaveBeenCalledWith(42);  // mock called with args
expect(mockFn).toHaveBeenCalledTimes(3);  // called N times
```

### test.each (Parametrize)

```javascript
test.each([
  [2, 3, 5],
  [0, 0, 0],
  [-1, 1, 0],
])('adds %i and %i to equal %i', (a, b, expected) => {
  expect(add(a, b)).toBe(expected);
});
```

### Setup and Teardown

```javascript
beforeAll(() => { /* runs once before all tests in the describe block */ });
afterAll(() => { /* runs once after all tests */ });
beforeEach(() => { /* runs before each test */ });
afterEach(() => { /* runs after each test */ });
```

---

## Common Mock Patterns

### Python: unittest.mock

```python
from unittest.mock import MagicMock, patch, call

# 1. Create a mock object
mock_service = MagicMock()
mock_service.get_user.return_value = {"id": 1, "name": "Alice"}

result = process_user(1, service=mock_service)

# Verify calls
mock_service.get_user.assert_called_once_with(1)
mock_service.get_user.assert_called_with(1)  # most recent call
mock_service.get_user.assert_any_call(1)      # any call with these args

# 2. Patch a module-level name
with patch('mymodule.send_email') as mock_email:
    register_user("alice@example.com")
    mock_email.assert_called_once()

# 3. Patch as a decorator
@patch('mymodule.requests.get')
def test_fetch_user(mock_get):
    mock_get.return_value.json.return_value = {"id": 1}
    result = fetch_user(1)
    assert result["id"] == 1

# 4. Mock raising an exception
mock_db = MagicMock()
mock_db.query.side_effect = ConnectionError("DB down")

# 5. Spy on a real object (wrap it)
from unittest.mock import wraps
real_calculator = Calculator()
spy = MagicMock(wraps=real_calculator)
spy.add(2, 3)  # calls the real method
spy.add.assert_called_once_with(2, 3)
```

### JavaScript: Jest Mocks

```javascript
// 1. Mock a function
const mockFn = jest.fn();
mockFn.mockReturnValue(42);
mockFn.mockReturnValueOnce(99);  // returns 99 the first time, then 42

// 2. Mock a module
jest.mock('./emailService', () => ({
  sendEmail: jest.fn().mockResolvedValue({ success: true }),
}));

// 3. Spy on an existing method
const spy = jest.spyOn(console, 'log').mockImplementation(() => {});
doSomeThing();
expect(spy).toHaveBeenCalledWith('expected message');
spy.mockRestore();  // restore original

// 4. Mock an async function
const mockFetch = jest.fn().mockResolvedValue({ data: [1, 2, 3] });

// 5. Clear mocks between tests
beforeEach(() => {
  jest.clearAllMocks();  // clears call counts and return values
});
```

---

## Playwright Locator Strategies

### Recommended Locators (most to least resilient)

```typescript
// 1. By role — most accessible, mirrors what users see
page.getByRole('button', { name: 'Submit' })
page.getByRole('textbox', { name: 'Email' })
page.getByRole('heading', { name: 'Welcome' })
page.getByRole('link', { name: 'Sign in' })

// 2. By label — for form inputs
page.getByLabel('Email address')
page.getByLabel('Password')

// 3. By placeholder
page.getByPlaceholder('Enter your email')

// 4. By text content
page.getByText('Welcome back')
page.getByText('Submit', { exact: true })

// 5. By test ID — when other selectors aren't suitable
// (requires data-testid="submit-button" in HTML)
page.getByTestId('submit-button')

// 6. By CSS or XPath — LAST RESORT (fragile)
page.locator('.submit-btn')      // CSS
page.locator('//button[@type="submit"]')  // XPath — avoid when possible
```

### Common Playwright Actions

```typescript
// Navigation
await page.goto('https://example.com');
await page.goBack();
await page.reload();

// Interactions
await page.getByLabel('Email').fill('user@example.com');
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('checkbox').check();
await page.getByRole('select').selectOption('value');
await page.keyboard.press('Enter');

// Assertions
await expect(page.getByRole('heading')).toHaveText('Welcome');
await expect(page.getByRole('button')).toBeVisible();
await expect(page.getByRole('button')).toBeEnabled();
await expect(page).toHaveURL(/dashboard/);
await expect(page).toHaveTitle('Dashboard');

// Waiting (Playwright auto-waits, but explicit waits are sometimes needed)
await page.waitForURL('**/dashboard');
await page.waitForSelector('[data-loaded="true"]');
await expect(page.locator('.spinner')).not.toBeVisible();
```

### Page Object Model Pattern

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.getByLabel('Email').fill(email);
    await this.page.getByLabel('Password').fill(password);
    await this.page.getByRole('button', { name: 'Sign in' }).click();
  }

  async getErrorMessage() {
    return this.page.getByRole('alert').textContent();
  }
}

// tests/login.spec.ts
test('successful login redirects to dashboard', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password123');
  await expect(page).toHaveURL('/dashboard');
});
```

---

## Testing Pyramid Quick Reference

```
           /\
          /  \
         / E2E \         Few, slow, expensive
        /--------\       Playwright / Cypress
       /Integration\     Some, medium speed
      /--------------\   TestContainers, httpx
     /   Unit Tests   \  Many, fast, cheap
    /------------------\ pytest / Jest
```

| Type | Speed | Cost | Confidence | Count |
|------|-------|------|------------|-------|
| Unit | Milliseconds | Very low | Component behavior | Many (hundreds) |
| Integration | Seconds | Medium | Cross-component behavior | Some (tens) |
| E2E | Minutes | High | Full user journey | Few (single digits–tens) |

---

## FIRST Principles Quick Reference

| Letter | Principle | What It Means |
|--------|-----------|---------------|
| **F** | Fast | Unit tests should run in milliseconds. A suite of 500 tests should complete in < 30 seconds. |
| **I** | Isolated | Each test must be independent. The outcome of one test must not affect another. |
| **R** | Repeatable | Tests must produce the same result every time, on any machine, in any order. |
| **S** | Self-validating | Tests must pass or fail automatically — no human interpretation required. |
| **T** | Timely | Write tests at the right time — ideally before the code (TDD), or alongside it. |
