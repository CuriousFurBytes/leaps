# Test: Module 02 — Awaitables, Tasks, and Cancellation

**Instructions:** Answer all questions. Write your answers directly below each question. Bonus questions are optional and can raise your score above 100%.

**Total Points:** 37 pts (Easy: 5 + Medium: 10 + Hard: 12 + Expert: 10)
**Bonus Available:** 3 pts

---

## Section 1: Easy Questions (1 pt each)

**Q1.** Define a coroutine.
> Answer:

**Q2.** What does an event loop coordinate?
> Answer:

**Q3.** What keyword marks a suspension point?
> Answer:

**Q4.** Why is blocking sleep dangerous in async code?
> Answer:

**Q5.** What should own every created task?
> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Explain why async Python helps I/O-bound workloads.
> Answer:

**Q7.** Compare awaiting a coroutine directly with scheduling it as a task.
> Answer:

**Q8.** Explain cancellation as a cooperative process.
> Answer:

**Q9.** Describe one use of backpressure.
> Answer:

**Q10.** When might async Python be the wrong tool?
> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** Write a runnable program that runs two coroutines concurrently.
> Answer:

**Q12.** Find and fix the bug:
```python
async def get_value():
    return 1

print(get_value())
```
> Answer:

**Q13.** Add a timeout around a slow coroutine.
> Answer:

**Q14.** Design a cleanup path for a cancelled worker.
> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** Design a small async service and explain task ownership, cancellation, and backpressure.
> Answer:

**Q16.** Synthesize this module with production debugging: what evidence would you gather for a suspected event-loop stall?
> Answer:

---

## Bonus Questions (variable pts)

**Bonus 1.** Explain how async Python differs from parallel CPU execution. (+3 pts)
> Answer:
