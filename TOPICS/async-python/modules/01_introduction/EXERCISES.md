# Exercises: Module 01 — Introduction to Async Python

## Instructions

Complete each exercise in order. Exercises increase in difficulty.
Submit your answers by editing this file or committing a solutions file.

---

## Easy Exercises (1–3)

### Exercise 1

**Difficulty:** Easy
**Objective:** Distinguish coroutine objects from coroutine results

Given the following code, answer these questions:
1. What is the type of `result_a`?
2. What is the type of `result_b`?
3. Which line actually executes the logic inside `add_async`?

```python
import asyncio

async def add_async(x: int, y: int) -> int:
    return x + y

result_a = add_async(3, 4)

async def main():
    result_b = await add_async(3, 4)

asyncio.run(main())
```

**Your answer:**

---

### Exercise 2

**Difficulty:** Easy
**Objective:** Write your first async function and run it with asyncio.run()

Write an `async def` function called `square(n: int) -> int` that:
1. Sleeps for `n * 0.01` seconds (to simulate I/O)
2. Returns `n * n`

Then write a `main()` coroutine that calls `square(5)` and prints the result.
Run it with `asyncio.run()`.

```python
import asyncio

# Write your solution here
```

**Expected output:** `25`

---

### Exercise 3

**Difficulty:** Easy
**Objective:** Identify which concurrency model is appropriate

For each scenario, write which model you would choose and one sentence why:
- asyncio
- threading
- multiprocessing

Scenarios:
1. Fetching weather data from 200 different city APIs simultaneously
2. Resizing 10,000 images using Pillow (CPU-intensive)
3. Querying a legacy MySQL database using PyMySQL (a blocking, non-async library)
4. Writing a real-time chat server that handles 5,000 WebSocket connections

**Your answer:**

---

## Medium Exercises (4–6)

### Exercise 4

**Difficulty:** Medium
**Objective:** Use asyncio.gather() to run multiple coroutines concurrently

Write an async program that simulates fetching three "reports" from a slow service:
- `fetch_report("sales")` — takes 1.5 seconds
- `fetch_report("inventory")` — takes 1.0 seconds
- `fetch_report("returns")` — takes 0.8 seconds

Implement `fetch_report(name: str) -> dict` as a coroutine that sleeps for the specified
time and returns `{"report": name, "rows": 42}`.

Requirements:
1. Use `asyncio.gather()` to fetch all three concurrently
2. Print each result
3. Print the total elapsed time
4. The total time must be less than 2 seconds (the max of the individual times, not the sum)

```python
import asyncio
import time

# Write your solution here
```

---

### Exercise 5

**Difficulty:** Medium
**Objective:** Understand the difference between creating and awaiting a coroutine

Explain in your own words what each of the following four lines does differently:

```python
import asyncio

async def work() -> str:
    await asyncio.sleep(1)
    return "done"

# Line 1: What does this do? Does it run anything?
coro = work()

# Line 2: What does this do? When does it complete?
async def approach_a():
    result = await work()

# Line 3: What does this do? When does it complete?
async def approach_b():
    task = asyncio.create_task(work())
    result = await task

# Line 4: What is wrong with this? What happens?
async def approach_c():
    asyncio.create_task(work())  # no await, no assignment
    # task is created but we never wait for it
```

**Your answer:**

---

### Exercise 6

**Difficulty:** Medium
**Objective:** Fix a blocking event loop bug

The following code is supposed to print "heartbeat" every 0.1 seconds while
`slow_operation()` runs. But it doesn't work as intended. Identify the bug and
fix it without changing what `slow_operation` actually does (it must still do
CPU-like work), but make the program respond correctly.

```python
import asyncio
import time

async def slow_operation() -> str:
    """Simulates CPU-intensive work by spinning."""
    # BUG: time.sleep() blocks the event loop!
    time.sleep(2)  # pretend this is heavy computation
    return "result"

async def heartbeat():
    for _ in range(20):
        print("heartbeat")
        await asyncio.sleep(0.1)

async def main():
    await asyncio.gather(
        slow_operation(),
        heartbeat(),
    )

asyncio.run(main())
```

Hint: How do you run a blocking function without blocking the event loop?

**Your solution:**

---

## Hard Exercises (7–8)

### Exercise 7

**Difficulty:** Hard
**Objective:** Build a concurrent task runner with timeout and error handling

Write an `async def run_with_timeout(coros, timeout_seconds)` function that:
1. Runs all coroutines in the list concurrently using `asyncio.gather()`
2. If the overall operation takes longer than `timeout_seconds`, cancels everything
   and raises `asyncio.TimeoutError`
3. If individual coroutines raise exceptions, captures them (do not let one failure
   kill the others) and returns them as exception objects in the results list
4. Returns a list of results (values for successes, Exception objects for failures)

Test it with:
```python
async def fast() -> str:
    await asyncio.sleep(0.1)
    return "fast result"

async def slow() -> str:
    await asyncio.sleep(5.0)
    return "slow result"

async def failing() -> str:
    await asyncio.sleep(0.2)
    raise ValueError("something went wrong")

async def main():
    # Should return within 1 second with a mix of result and exception
    results = await run_with_timeout(
        [fast(), failing(), slow()],
        timeout_seconds=1.0,
    )
    print(results)
```

**Your solution:**

---

### Exercise 8

**Difficulty:** Hard
**Objective:** Debug an async program that produces incorrect output

The following program is supposed to count from 1 to 5, with each number taking
progressively longer to compute. The expected output is `1, 2, 3, 4, 5` in order.
But the program has a bug. Find and fix it.

```python
import asyncio

async def compute(n: int) -> int:
    # Longer computation for larger numbers
    await asyncio.sleep(n * 0.1)
    return n

async def main():
    # Bug: the tasks are created but not run concurrently
    results = []
    for n in range(1, 6):
        result = await compute(n)  # <-- is this correct for concurrent execution?
        results.append(result)

    print(", ".join(str(r) for r in results))

asyncio.run(main())
```

The program currently produces correct output but runs sequentially (taking 1.5 seconds
total: 0.1 + 0.2 + 0.3 + 0.4 + 0.5). Fix it so all computations run concurrently and
the total time is ~0.5 seconds.

**Your solution:**

---

## Expert Exercise (9)

### Exercise 9

**Difficulty:** Expert
**Objective:** Implement a cooperative task scheduler from scratch

Implement a minimal `Scheduler` class that demonstrates how an event loop works
at the conceptual level. Your scheduler should:

1. Accept coroutines via `scheduler.schedule(coro)` 
2. When `scheduler.run()` is called, drive all scheduled coroutines to completion
   using `send(None)` / `throw()` on the underlying generator protocol
3. Support basic `asyncio.sleep`-like pausing via a `pause(seconds)` coroutine
   that you define
4. Not use `asyncio` at all — this is a from-scratch implementation

This exercise is intentionally open-ended. The goal is to understand that an event
loop is fundamentally a loop that calls `next()` on coroutines, handles `StopIteration`
when they finish, and tracks which coroutines are ready to run.

```python
import time
from collections import deque

# Hint: generators and coroutines share the same protocol
# send(None) starts a generator; send(value) resumes it with a value
# StopIteration.value contains the return value

class Scheduler:
    def __init__(self):
        self.ready = deque()
        # ... your implementation

    def schedule(self, coro):
        # ... add to ready queue
        pass

    def run(self):
        # ... main loop: drive coroutines to completion
        pass

async def pause(seconds: float):
    # Hint: you'll need to yield something the scheduler can inspect
    pass

# Test:
async def task_a():
    print("A: start")
    await pause(0.1)
    print("A: end")
    return "A done"

async def task_b():
    print("B: start")
    await pause(0.05)
    print("B: end")
    return "B done"

s = Scheduler()
s.schedule(task_a())
s.schedule(task_b())
s.run()
```

**Your solution:**
