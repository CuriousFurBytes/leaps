# Exercises: Module 01 — Introduction to QA and Testing

## Instructions

Complete each exercise in order. Exercises increase in difficulty.
Submit your answers by editing this file or committing a solutions file.

---

## Easy Exercises (1–3)

### Exercise 1

**Difficulty:** Easy
**Objective:** Recall the testing pyramid and identify test types

For each scenario below, identify which layer of the testing pyramid is most appropriate (Unit, Integration, or E2E):

a) Verifying that a `calculate_tax(price, rate)` function returns `8.25` when called with `price=100, rate=0.0825`

b) Verifying that a user can register, log in, and see their profile on a web application by controlling a real browser

c) Verifying that a `UserRepository.save()` method correctly writes a user record to a PostgreSQL test database

d) Verifying that a `format_date(date, format_string)` utility function returns `"2024-01-15"` for the given inputs

e) Verifying that a REST API endpoint returns 404 when a user with the given ID does not exist, by making a real HTTP call to the application running against a test database

---

### Exercise 2

**Difficulty:** Easy
**Objective:** Apply the FIRST principles to identify test quality issues

Read each test description below. Identify which FIRST principle(s) it violates and explain why.

a) A test that calls `time.sleep(2)` before asserting that an email was sent

b) A test that passes when run in isolation but fails when run after `test_add_item_to_cart` because they share a global shopping cart object

c) A test that calls a live external payment API to verify charge processing

d) A test that runs a calculation and prints the result to stdout, expecting a developer to verify it manually

e) A test that was written 6 months after the feature shipped, and whose failure mode doesn't clearly identify which requirement was violated

---

### Exercise 3

**Difficulty:** Easy
**Objective:** Set up pytest and write first tests

Set up a Python project with pytest and write a test file for the following function:

```python
def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32
```

Write at least 5 tests covering:
- Freezing point of water (0°C → 32°F)
- Boiling point of water (100°C → 212°F)
- Body temperature (37°C → 98.6°F)
- Absolute zero (-273.15°C → -459.67°F)
- A negative temperature of your choice

---

## Medium Exercises (4–6)

### Exercise 4

**Difficulty:** Medium
**Objective:** Explain the economic case for testing and identify when testing is most valuable

Answer the following questions in 3–5 sentences each:

a) Explain the "1x/10x/100x" rule for bug fix costs. Give a concrete example (not the one from the module) that illustrates why production bugs cost so much more to fix.

b) What does "shift-left testing" mean? How does adopting TDD represent an extreme form of shift-left testing?

c) A startup founder argues: "We're moving fast; testing slows us down. We'll add tests later once the product is proven." What is the best counter-argument, grounded in economics rather than ideology?

---

### Exercise 5

**Difficulty:** Medium
**Objective:** Write parametrized tests and handle edge cases

Extend the `calculate_discount()` function from the module (you can copy the implementation) and write a parametrized test that covers at least 8 combinations of price and discount_percent, including:
- Standard discounts (10%, 25%, 50%)
- Boundary values (0% and 100%)
- One floating-point edge case (e.g., 33.33%)

Use `@pytest.mark.parametrize` in Python or `test.each` in Jest.

```python
# Starter code — pytest
import pytest
from discount import calculate_discount

@pytest.mark.parametrize("price,discount,expected", [
    # Add your test cases here
    (100.00, 10, 90.00),
    # ...
])
def test_calculate_discount(price, discount, expected):
    assert calculate_discount(price, discount) == expected
```

---

### Exercise 6

**Difficulty:** Medium
**Objective:** Identify and fix poorly written tests

The following test suite has several problems. Identify every issue and rewrite each test correctly.

```python
import time

# Problem test suite — find and fix all issues

cart = []  # shared state

def test_add_apple():
    cart.append("apple")
    assert "apple" in cart

def test_cart_has_one_item():
    assert len(cart) == 1  # this depends on test_add_apple running first

def test_expensive_shipping_calculation():
    time.sleep(5)  # waiting for "database"
    result = calculate_shipping(cart)
    print(f"Shipping cost: {result}")  # no assertion

def test_discount_applied():
    result = apply_discount(cart, 0.1)
    # just checking it doesn't throw an error
    assert result is not None
```

---

## Hard Exercises (7–8)

### Exercise 7

**Difficulty:** Hard
**Objective:** Write a complete test suite for a real function with AAA structure

Write a complete test suite for the following `ShoppingCart` class. Your tests must:
- Follow the AAA (Arrange/Act/Assert) pattern for each test
- Cover all methods: `add_item`, `remove_item`, `get_total`, `apply_discount`
- Include at least 3 edge case tests (empty cart operations, duplicate items, etc.)
- Include at least 2 error case tests
- Have descriptive test names that explain the behavior being tested

```python
class ShoppingCart:
    def __init__(self):
        self._items = {}  # {name: {"price": float, "quantity": int}}

    def add_item(self, name: str, price: float, quantity: int = 1):
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
        if name in self._items:
            self._items[name]["quantity"] += quantity
        else:
            self._items[name] = {"price": price, "quantity": quantity}

    def remove_item(self, name: str):
        if name not in self._items:
            raise KeyError(f"Item '{name}' not in cart")
        del self._items[name]

    def get_total(self) -> float:
        return sum(
            item["price"] * item["quantity"]
            for item in self._items.values()
        )

    def apply_discount(self, percent: float) -> float:
        if not 0 <= percent <= 100:
            raise ValueError("Discount must be 0–100%")
        total = self.get_total()
        return round(total * (1 - percent / 100), 2)
```

---

### Exercise 8

**Difficulty:** Hard
**Objective:** Design a test strategy for a real feature

You are working on a user authentication feature with the following requirements:
- Users can register with email and password
- Passwords must be at least 8 characters and contain at least one number
- Email must be a valid format and not already registered
- After registration, users receive a confirmation email
- Users can log in with email and password
- After 5 failed login attempts, the account is locked for 15 minutes

Design a test strategy for this feature:
1. List all the unit tests you would write (function-level behavior, including all error paths)
2. List all the integration tests you would write (interactions with the database and email service)
3. List any E2E tests you would write (only for the most critical user journeys)
4. Identify which tests would use mocks and explain what they would mock and why

You do not need to write the code — just design the strategy with clear descriptions of each test.

---

## Expert Exercise (9)

### Exercise 9

**Difficulty:** Expert
**Objective:** Evaluate testing strategy tradeoffs and synthesize the testing pyramid with real-world constraints

A colleague proposes the following testing strategy for a new microservices application:

> "Each of our 8 services will have E2E tests that test the full flow from UI to database. We'll write one E2E test per user story. Our current sprint has 20 user stories. E2E tests take about 2 minutes each. We'll have CI run these tests on every PR. We don't need unit tests because the E2E tests cover everything."

Write a detailed critique of this strategy (400–600 words) that covers:
1. The specific problems with this approach (using the pyramid model and FIRST principles)
2. What the developer time and CI cost implications would be at scale (calculate: if each E2E takes 2 minutes, 20 tests × 2 min = 40 minutes per CI run; estimate how this compounds as the team grows)
3. An alternative testing strategy that achieves the same confidence with lower cost and faster feedback
4. How you would make the argument for the alternative strategy to a stakeholder who is comfortable with the current approach
