# Exercises: Module 01 — Event Loop Foundations

## Instructions
Complete each exercise in order. Exercises increase in difficulty. Submit answers by editing this file or committing a solutions file.

---

## Easy Exercises (1–3)

### Exercise 1
**Difficulty:** Easy
**Objective:** Identify key vocabulary.

Write short definitions for coroutine, task, event loop, and cancellation.

### Exercise 2
**Difficulty:** Easy
**Objective:** Run a minimal async program.

```python
import asyncio

async def main():
    print("replace me")

asyncio.run(main())
```

Modify the message and run the file.

### Exercise 3
**Difficulty:** Easy
**Objective:** Locate suspension points.

Mark every line in a small async program where another task may run.

## Medium Exercises (4–6)

### Exercise 4
**Difficulty:** Medium
**Objective:** Compare sequential and concurrent waiting.

Write two versions of a program that waits on three `asyncio.sleep()` calls: one sequential and one concurrent.

### Exercise 5
**Difficulty:** Medium
**Objective:** Explain a tradeoff.

Explain when async Python is better than threads and when threads may be simpler.

### Exercise 6
**Difficulty:** Medium
**Objective:** Add a timeout.

Wrap a slow coroutine in a timeout and print a friendly message when it expires.

## Hard Exercises (7–8)

### Exercise 7
**Difficulty:** Hard
**Objective:** Debug broken async code.

Fix a program that creates a coroutine but never awaits it.

### Exercise 8
**Difficulty:** Hard
**Objective:** Design task ownership.

Start three tasks, collect their results, and ensure exceptions are visible to the caller.

## Expert Exercise (9)

### Exercise 9
**Difficulty:** Expert
**Objective:** Justify an architecture.

Write a one-page design note explaining how this module affects a production async service.
