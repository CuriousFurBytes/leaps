# Projects: Module 01 — Introduction to QA and Testing

> Projects for this module focus on establishing testing fundamentals:
> setting up environments, writing first tests, and applying the testing pyramid.

---

## Project 1: Test Suite for a Utility Library (Beginner)

**Difficulty:** Beginner
**Time Estimate:** 3–4 hours
**Skills Practiced:** pytest setup, basic assertions, edge case thinking, test naming

**Description:**
Create a utility library with 3–5 simple functions (string manipulation, math operations, or date formatting), then write a complete test suite for it. Focus on coverage quality, not quantity — test the behavior thoroughly, including edge cases and error paths.

**Requirements:**
- At least 4 functions with meaningful behavior
- At least 4 tests per function (happy path, edge cases, error cases)
- Passing `pytest --cov` report showing ≥ 85% line coverage
- Test names that clearly describe the behavior being tested (not `test_function_1`)

**Starter functions to consider:**
- `count_vowels(text: str) -> int`
- `is_palindrome(text: str) -> bool`
- `clamp(value, min_val, max_val) -> float`
- `truncate_text(text: str, max_len: int, suffix: str = "...") -> str`

**Success Criteria:**
- All tests pass
- Coverage ≥ 85%
- At least one test uses `pytest.raises` for an error case
- Test file is organized with clear section comments or test classes

---

## Project 2: Testing Pyramid Analysis (Beginner–Intermediate)

**Difficulty:** Beginner–Intermediate
**Time Estimate:** 2–3 hours
**Skills Practiced:** Testing pyramid reasoning, test design, written communication

**Description:**
Choose a real-world feature from an application you use (or a fictional one you design). Write a testing strategy document that applies the testing pyramid: identify what unit tests, integration tests, and E2E tests you would write for this feature.

**Requirements:**
- Feature description (1–2 paragraphs)
- Unit tests: list at least 5 specific tests with test names and what they verify
- Integration tests: list at least 2 specific tests with what dependencies they involve
- E2E tests: list at most 2 user journey tests
- Brief rationale for why each test belongs in its pyramid tier

**Example feature:** A user authentication system (register, login, logout, forgot password)

**Success Criteria:**
- Unit tests test isolated functions/methods (no database, no HTTP)
- Integration tests involve at least one real dependency (database, HTTP, file)
- E2E tests describe a complete user journey
- Rationale is clearly argued, not just asserted

---

## Project 3: Refactor a Broken Test Suite (Intermediate)

**Difficulty:** Intermediate
**Time Estimate:** 3–5 hours
**Skills Practiced:** Identifying test quality issues, FIRST principles, test isolation

**Description:**
Take the broken test suite from Exercise 6 (or create your own set of 10+ poorly written tests) and refactor it to follow best practices. Document each problem you fixed and which FIRST principle it violated.

**Requirements:**
- Original test file with documented problems (in comments)
- Refactored test file with clean, isolated, descriptive tests
- A NOTES.md entry listing each problem, the principle violated, and how you fixed it

**Success Criteria:**
- No shared mutable state between tests
- No real network calls in unit tests (use mocks)
- No `time.sleep()` calls
- All tests have meaningful assertions
- All tests have descriptive names
