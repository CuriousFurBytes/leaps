# Test: Module 01 — Introduction to QA and Testing

**Instructions:** Answer all questions. Write your answers directly below each question.
Bonus questions are optional and can raise your score above 100%.

**Total Points:** 37 pts (Easy: 5 × 1pt + Medium: 5 × 2pts + Hard: 4 × 3pts + Expert: 2 × 5pts)
**Bonus Available:** 5 pts

---

## Section 1: Easy Questions (1 pt each)

**Q1.** In the testing pyramid, which layer contains the most tests?
> Answer:

**Q2.** What does the "I" in the FIRST principles stand for, and what does it mean for a unit test?
> Answer:

**Q3.** Name three types of tests that exist outside the standard three layers of the testing pyramid (unit, integration, E2E).
> Answer:

**Q4.** What is a "smoke test" and when is it typically run?
> Answer:

**Q5.** What is a "regression test" and what triggers the creation of one?
> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Explain why the testing pyramid recommends having many unit tests and few E2E tests. What specific properties of E2E tests make them expensive to maintain?
> Answer:

**Q7.** A developer argues: "Our test suite has 95% line coverage, so our code is well-tested." What is wrong with this reasoning? Give a specific example of code that achieves 100% line coverage but is essentially untested.
> Answer:

**Q8.** Explain "shift-left testing" in your own words. How does test-driven development (TDD) represent the most extreme form of shift-left testing?
> Answer:

**Q9.** What is the AAA pattern? Write out the three components and explain the role of each in a well-structured test.
> Answer:

**Q10.** Compare unit tests and integration tests on the following dimensions: speed, isolation, scope, and typical failure diagnosis. When would you choose one over the other?
> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** The following Python test has multiple problems. Identify every problem (there are at least 4), explain what principle each problem violates, and rewrite the test correctly.

```python
import requests
import time

db_state = {"users": []}

def test_register_user():
    time.sleep(3)
    response = requests.post(
        "https://api.production.example.com/users",
        json={"email": "test@example.com"}
    )
    print(f"Status: {response.status_code}")
    db_state["users"].append("test@example.com")

def test_user_count():
    assert len(db_state["users"]) == 1
```

> Answer:

**Q12.** You are building a feature that sends a welcome email after a user registers. Describe how you would write tests for this feature at each level of the pyramid. For the unit test level, show pseudocode or real code demonstrating how you would avoid making a real email call.
> Answer:

**Q13.** Explain the economic argument for investing in automated testing. Use the "1x/10x/100x" rule to calculate the approximate cost difference between a bug found during coding vs. a bug found in production, assuming: a developer costs $100/hour, fixing a bug during coding takes 30 minutes, and fixing a production bug requires 8 hours of developer time plus 4 hours of DevOps, QA, and management time at an average rate of $120/hour.
> Answer:

**Q14.** A team is experiencing "flaky tests" — tests that pass sometimes and fail sometimes with no code changes. List four common causes of test flakiness and describe how to fix each one.
> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** You are the first QA engineer at a startup with no existing tests. The codebase is 50,000 lines of Python and has been running in production for 18 months. Where do you start? Design a phased approach to introducing automated testing that balances the need for immediate safety with the long-term goal of a healthy test pyramid. Your answer should cover: (1) how to prioritize what to test first, (2) the types of tests to introduce in each phase, (3) how to prevent the existing codebase from getting worse while the test suite is being built, and (4) how to measure progress.
> Answer:

**Q16.** The testing pyramid was described by Mike Cohn in 2009 and popularized by Martin Fowler. In the years since, several practitioners have proposed modifications: the "testing honeycomb" (Spotify), the "trophy" (Kent C. Dodds), and others. Research one alternative model (or propose your own based on what you've learned) and write a synthesis: What is the model? What problem with the original pyramid is it trying to solve? Under what circumstances would you favor this model over the traditional pyramid?
> Answer:

---

## Bonus Question (+5 pts)

**Bonus 1.** Edsger Dijkstra wrote in 1969 that "program testing can be used to show the presence of bugs, but never to show their absence." If testing cannot prove correctness, what value does it provide? Write a philosophical defense of software testing (200–300 words) that acknowledges Dijkstra's limitation while arguing that testing is still the best practical tool we have for managing software correctness at scale.
> Answer:
