# Module 01: Introduction to Async Python

[← Topic Home](../../README.md) | [Next → Module 02](../02_coroutines-and-event-loop/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner-green)
![Time](https://img.shields.io/badge/time-4h-orange)

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Key Concepts](#key-concepts)
6. [Examples](#examples)
7. [Common Pitfalls](#common-pitfalls)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

---

## Overview

This module answers the foundational question: *why does Python have asyncio, and when
should you use it?*

Most Python programs you have written so far are synchronous — one statement runs, it
completes, then the next statement runs. That model is simple and correct for most programs.
But consider a program that needs to fetch data from 1,000 different URLs. A synchronous
approach would fetch URL 1, wait for the response, fetch URL 2, wait, and so on — spending
most of its time idle, waiting for the network. Asyncio allows that same program to have all
1,000 requests in-flight simultaneously on a single thread, processing responses as they
arrive.

Understanding *why* asyncio works this way — and the constraints it operates under — is
essential before writing a single line of async code. This module gives you that foundation:
the GIL, the difference between concurrency and parallelism, what a coroutine is, and how the
event loop ties it all together.

**Difficulty:** Beginner | **Estimated time:** 4 hours

---

## Prerequisites

### Required Concepts

- **Python functions** — you must be comfortable writing and calling regular Python functions
- **Context managers** — you should understand `with` statements and how `__enter__`/`__exit__`
  work, because `async with` is a direct extension of this pattern
- **Generators** — familiarity with `yield` helps, as coroutines share deep similarities with
  generators at the implementation level; not strictly required but very useful

> [!TIP]
> If `yield` is unfamiliar, don't block on it — you can follow this module without deep
> generator knowledge. Just know that coroutines and generators are related concepts in Python.
> Return to generators after completing Module 01.

---

## Objectives

By the end of this module, you will be able to:

1. Explain the difference between concurrency and parallelism in plain language
2. Describe what the GIL is and why it affects Python's threading performance
3. Compare threading, multiprocessing, and asyncio and choose the right model for a given
   problem
4. Explain what a coroutine is and how it differs from a regular function
5. Write a basic `async def` function and run it with `asyncio.run()`
6. Explain what the event loop does and how it schedules coroutines

---

## Theory

### The Problem: Blocking I/O

Most real-world programs spend the majority of their time waiting. A typical web API spends
perhaps 5% of its time running Python code and 95% waiting: for a database query to return,
for an upstream HTTP request to complete, for a cache lookup. During all that waiting, the
CPU is completely idle — sitting at a `recv()` system call, doing nothing.

In a traditional synchronous Python program, this idle time is wasted. Consider fetching
data from two separate services:

```python
import time
import urllib.request

def fetch_sync(url: str) -> str:
    """Synchronous HTTP fetch — blocks the entire thread until done."""
    with urllib.request.urlopen(url) as response:
        return response.read().decode()

def main_sync():
    start = time.perf_counter()

    # These run sequentially: fetch A, THEN fetch B
    # Total time = time(A) + time(B)
    result_a = fetch_sync("http://httpbin.org/delay/1")  # waits ~1 second
    result_b = fetch_sync("http://httpbin.org/delay/1")  # waits ~1 second

    elapsed = time.perf_counter() - start
    print(f"Sequential: {elapsed:.2f}s")  # ~2 seconds

main_sync()
```

The problem is obvious once you see it: while we are waiting for the response from service A,
we could have been waiting for service B at the same time. We wasted a full second of wall
clock time because the code was blocked on I/O.

### Python's Concurrency Models

Python offers three concurrency models, each suited to a different problem class:

| Model | When to Use | Bottleneck | GIL? | Parallelism? |
|-------|-------------|------------|------|-------------|
| **threading** | I/O-bound, moderate concurrency | Network/disk I/O, legacy blocking libs | Released during I/O | No (GIL prevents CPU parallelism) |
| **multiprocessing** | CPU-bound | Computation, number crunching | Each process has own GIL | Yes (multiple processes) |
| **asyncio** | I/O-bound, high concurrency | Network/disk I/O, async-aware libs | Sidesteps it entirely | No (single thread) |

Threads help with I/O because the GIL is released during I/O system calls — when a thread is
blocked on `recv()`, the GIL is free for other threads. But thread creation and context
switching carry real overhead, and OS threads consume memory (typically 1–8 MB per thread
for the stack). Scaling to thousands of concurrent I/O operations with threads is expensive.

Asyncio solves this by never blocking at all. A single thread services all operations by
switching between coroutines at `await` points — no OS context switches, no stack memory per
concurrent operation (coroutine stacks are heap-allocated and tiny).

The key constraint: **asyncio only helps for I/O-bound work**. If your bottleneck is CPU
computation, asyncio cannot help and you need multiprocessing.

### The GIL: What It Is and Why It Exists

The **Global Interpreter Lock (GIL)** is a mutex in CPython (the standard Python
interpreter) that allows only one thread to execute Python bytecode at any given moment.
Even on a multi-core CPU, Python threads take turns — they do not run in true parallel.

The GIL exists because CPython manages memory using **reference counting**. Every Python
object has an integer `ob_refcnt` field that tracks how many references point to it. When
a reference is added or removed, that counter is updated. If two threads incremented or
decremented `ob_refcnt` simultaneously, the counter could become corrupted — objects would
be freed too early (crash) or never freed (memory leak).

The GIL is a blunt but effective solution: only one thread touches reference counts at a time.
It also makes C extension modules easier to write safely.

The practical consequence:

```python
import threading

counter = 0

def increment():
    global counter
    for _ in range(1_000_000):
        counter += 1  # NOT thread-safe! Read-modify-write is not atomic.

# Two threads attempting to share counter will produce incorrect results
# despite the GIL — counter += 1 is multiple bytecode instructions
t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)
t1.start(); t2.start()
t1.join(); t2.join()
# counter will likely not be 2,000,000 — a classic race condition
print(counter)
```

Asyncio sidesteps the GIL entirely because there is only one thread. Two coroutines can
never truly run simultaneously — the event loop runs one at a time. This eliminates entire
classes of race conditions that affect multithreaded code, though async code has its own
subtler race conditions (covered in Module 05).

### Coroutines: The Building Block

A **coroutine** is a special kind of function that can suspend its execution at defined
points and later resume from exactly where it left off. In Python, coroutines are defined
with `async def` and suspended with `await`.

The critical difference from a regular function: calling a regular function runs it to
completion immediately. Calling an `async def` function does NOT run it — it returns a
**coroutine object**.

```python
# A regular function: calling it runs it immediately
def regular_greet(name: str) -> str:
    return f"Hello, {name}!"

result = regular_greet("Alice")  # runs immediately, result is "Hello, Alice!"
print(type(result))              # <class 'str'>

# A coroutine: calling it returns a coroutine OBJECT, not the result
async def async_greet(name: str) -> str:
    return f"Hello, {name}!"

coro = async_greet("Alice")  # does NOT run — returns a coroutine object
print(type(coro))            # <class 'coroutine'>
print(coro)                  # <coroutine object async_greet at 0x...>

# You'll see a warning: RuntimeWarning: coroutine 'async_greet' was never awaited
# The coroutine was created but never scheduled to run
coro.close()  # suppress the warning by closing it explicitly
```

This is the single most important thing to understand in all of asyncio: **a coroutine
object is not running until something schedules it**. The event loop is the scheduler.

The `await` keyword can be used inside an `async def` function to pause the current
coroutine and give control back to the event loop until the awaited thing completes:

```python
import asyncio

async def delayed_greeting(name: str, delay: float) -> str:
    """A coroutine that suspends for `delay` seconds, then returns a greeting."""
    # await asyncio.sleep() suspends THIS coroutine without blocking the thread
    # The event loop can run other coroutines during this pause
    await asyncio.sleep(delay)
    return f"Hello, {name}!"

async def main():
    # await runs the coroutine to completion from this context
    result = await delayed_greeting("Alice", 1.0)
    print(result)  # Hello, Alice!

# asyncio.run() is the standard entry point from synchronous code
# It creates an event loop, runs main() to completion, then cleans up
asyncio.run(main())
```

### The Event Loop: The Heart of asyncio

The **event loop** is a continuously running scheduler that:

1. Maintains a queue of coroutines ready to run
2. Runs each coroutine until it hits an `await` and suspends
3. While a coroutine is suspended (waiting for I/O, a timer, etc.), runs other ready
   coroutines
4. When an I/O operation completes or a timer fires, marks the waiting coroutine as
   ready again

Think of the event loop as a very efficient juggler: it keeps many balls in the air by
catching one, giving it a toss, and immediately turning to catch another — never waiting
idle for any single ball to fall back down.

```python
import asyncio

async def task(name: str, delay: float):
    """A coroutine that simulates I/O with a sleep."""
    print(f"{name}: starting, will pause for {delay}s")
    await asyncio.sleep(delay)  # event loop runs other tasks during this pause
    print(f"{name}: done after {delay}s")
    return name

async def main():
    import time
    start = time.perf_counter()

    # Without concurrent scheduling, this would take 1+2+3 = 6 seconds
    # With asyncio.gather(), all three run concurrently — total ~3 seconds
    results = await asyncio.gather(
        task("A", 1.0),
        task("B", 2.0),
        task("C", 3.0),
    )

    elapsed = time.perf_counter() - start
    print(f"All done in {elapsed:.2f}s: {results}")
    # Output: All done in ~3.00s: ['A', 'B', 'C']

asyncio.run(main())
```

The event loop runs `task("A", 1.0)`, `task("B", 2.0)`, and `task("C", 3.0)` by starting
all three, and as each hits `await asyncio.sleep(...)` it suspends. The event loop then
tracks which suspensions will expire soonest and wakes them up in order. All three complete
in approximately the time of the longest single task (3 seconds), not the sum (6 seconds).

This is the core value proposition of asyncio: **concurrent I/O without threads**.

---

## Key Concepts

### Coroutine

A function defined with `async def` that can pause at `await` expressions and resume later.
Calling a coroutine function returns a coroutine object; the object does not run until it
is scheduled by the event loop. Coroutines are the fundamental unit of async Python work.
See [[shared/glossary#coroutine]].

### Event Loop

The central asyncio scheduler. It runs coroutines in a cooperative fashion: each coroutine
runs until it awaits something, then the next ready coroutine runs. The event loop also
monitors I/O readiness and timers to know when to resume suspended coroutines.
`asyncio.run()` creates, runs, and closes an event loop automatically.
See [[shared/glossary#event-loop]].

### await

A keyword used inside `async def` functions to suspend the current coroutine until the
awaited expression completes. Only awaitables can be awaited: coroutines, Tasks, and Futures.
`await expr` is approximately "pause here, run the event loop until `expr` is done,
then resume with `expr`'s result."

### Concurrency vs. Parallelism

**Concurrency** is handling multiple tasks by interleaving their progress over time — tasks
take turns on one processor. **Parallelism** is executing multiple tasks at the same moment
on multiple processors. Asyncio provides concurrency; it does not provide parallelism. For
CPU-heavy work that needs parallelism, use `multiprocessing`.
See [[shared/glossary#concurrency]] and [[shared/glossary#parallelism]].

### I/O-Bound vs. CPU-Bound

**I/O-bound** work is limited by waiting for external operations (network, disk, database).
**CPU-bound** work is limited by computation speed. Asyncio is highly effective for I/O-bound
work and completely ineffective for CPU-bound work (which needs `multiprocessing`).
See [[shared/glossary#io-bound]] and [[shared/glossary#cpu-bound]].

### asyncio.run()

The standard entry point for async programs. Takes a coroutine, creates a new event loop,
runs the coroutine to completion, closes the loop, and returns the result. Always use
`asyncio.run()` to start an async program from synchronous code. Do not call it inside an
already-running event loop.

---

## Examples

### Example 1: Sequential vs. Async HTTP Fetching

**Scenario:** Fetch data from 3 slow endpoints. Measure the difference in time between
sequential and concurrent approaches.

**Goal:** Demonstrate concretely why asyncio matters for I/O-bound work.

> [!NOTE]
> This example uses `asyncio.sleep()` to simulate network latency rather than making
> real HTTP requests, so it runs offline. Real HTTP requests with `aiohttp` are covered
> in Module 04.

```python
import asyncio
import time

# Simulate a network request that takes `delay` seconds
async def fake_fetch(url: str, delay: float) -> dict:
    """Simulates a slow API call by sleeping for `delay` seconds."""
    await asyncio.sleep(delay)  # surrenders control to the event loop
    return {"url": url, "data": f"response from {url}"}

# --- Sequential approach (pretend we're calling them one by one) ---
async def sequential():
    """Fetch three URLs one after another — total time = sum of delays."""
    start = time.perf_counter()

    r1 = await fake_fetch("https://api.example.com/users", 1.0)
    r2 = await fake_fetch("https://api.example.com/posts", 1.0)
    r3 = await fake_fetch("https://api.example.com/comments", 1.0)

    elapsed = time.perf_counter() - start
    print(f"Sequential: {elapsed:.2f}s for 3 requests")
    # Output: Sequential: ~3.00s for 3 requests

# --- Concurrent approach using asyncio.gather() ---
async def concurrent():
    """Fetch three URLs at the same time — total time = max of delays."""
    start = time.perf_counter()

    # gather() starts all three coroutines immediately and waits for all to finish
    results = await asyncio.gather(
        fake_fetch("https://api.example.com/users", 1.0),
        fake_fetch("https://api.example.com/posts", 1.0),
        fake_fetch("https://api.example.com/comments", 1.0),
    )

    elapsed = time.perf_counter() - start
    print(f"Concurrent: {elapsed:.2f}s for 3 requests")
    print(f"Got {len(results)} results")
    # Output: Concurrent: ~1.00s for 3 requests

async def main():
    await sequential()
    await concurrent()

asyncio.run(main())
```

**What to notice:** The concurrent version takes approximately 1 second, not 3. The three
"requests" all run during the same second. This is the core benefit of asyncio for I/O-bound
work.

---

### Example 2: Your First Real Coroutine

**Scenario:** Write a simple coroutine that does something meaningful — greets multiple users
with a simulated database lookup delay for each.

**Goal:** Practice the `async def` / `await` / `asyncio.run()` pattern from scratch.

```python
import asyncio

# A simple "database lookup" — in real code this would use an async DB client
async def lookup_user(user_id: int) -> dict:
    """Simulate fetching a user record from a database."""
    # In production, this would be: user = await db.fetch_one("SELECT ...", user_id)
    await asyncio.sleep(0.05)  # simulate 50ms DB query
    return {"id": user_id, "name": f"User #{user_id}", "active": True}

async def greet_user(user_id: int) -> str:
    """Fetch a user and compose a greeting."""
    # await suspends this coroutine until lookup_user completes
    user = await lookup_user(user_id)
    if user["active"]:
        return f"Welcome back, {user['name']}!"
    else:
        return f"Account {user_id} is inactive."

async def main():
    # Greet 5 users concurrently
    user_ids = [101, 102, 103, 104, 105]

    greetings = await asyncio.gather(
        *[greet_user(uid) for uid in user_ids]
    )

    for greeting in greetings:
        print(greeting)

# Standard entry point
asyncio.run(main())

# Output (all 5 in ~50ms total, not 250ms):
# Welcome back, User #101!
# Welcome back, User #102!
# Welcome back, User #103!
# Welcome back, User #104!
# Welcome back, User #105!
```

**What to notice:** The list comprehension `[greet_user(uid) for uid in user_ids]` creates
5 coroutine objects without running them. `asyncio.gather(*...)` schedules all 5 and runs
them concurrently. The `*` unpacks the list into positional arguments.

---

### Example 3: Choosing the Right Tool — Concurrency Model Decision

**Scenario:** You need to build three different programs. For each, determine whether to use
asyncio, threading, or multiprocessing.

**Goal:** Develop practical intuition for which concurrency model to choose.

```python
import asyncio
import concurrent.futures
import multiprocessing

# ---- Program A: Download 500 files from the internet ----
# Decision: asyncio — pure I/O-bound, high concurrency needed

async def download_file(url: str, semaphore: asyncio.Semaphore) -> bytes:
    """Async download with concurrency limit."""
    async with semaphore:  # limit to 50 concurrent downloads
        # In real code: async with aiohttp.ClientSession() as session: ...
        await asyncio.sleep(0.1)  # simulate download time
        return b"file content"

async def download_all(urls: list) -> list:
    sem = asyncio.Semaphore(50)  # max 50 at a time
    tasks = [download_file(url, sem) for url in urls]
    return await asyncio.gather(*tasks)

# ---- Program B: Process a million images with PIL ----
# Decision: multiprocessing — CPU-bound, need multiple cores

def process_image(path: str) -> str:
    """CPU-intensive image processing — runs in a subprocess."""
    import hashlib
    # Simulate heavy computation
    result = hashlib.sha256(path.encode()).hexdigest()
    return result

def process_images_parallel(paths: list) -> list:
    with multiprocessing.Pool() as pool:
        # Each worker process gets its own GIL — true parallelism
        return pool.map(process_image, paths)

# ---- Program C: Call a legacy blocking database library ----
# Decision: threading — I/O-bound but can't use async; GIL released during I/O

def legacy_db_query(query: str) -> list:
    """Blocking database call using a legacy non-async library."""
    import time
    time.sleep(0.1)  # simulate blocking DB query
    return [{"result": query}]

async def query_with_threading(queries: list) -> list:
    """Run blocking queries in a thread pool to avoid blocking the event loop."""
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            loop.run_in_executor(executor, legacy_db_query, q)
            for q in queries
        ]
        return await asyncio.gather(*futures)

# asyncio.to_thread() (Python 3.9+) is a simpler alternative:
async def query_with_to_thread(queries: list) -> list:
    tasks = [asyncio.to_thread(legacy_db_query, q) for q in queries]
    return await asyncio.gather(*tasks)
```

**What to notice:** `asyncio.to_thread()` is the modern, clean way to call a blocking
function from async code. It runs the function in a thread pool so the event loop stays free.
This is the bridge between the sync and async worlds.

---

## Common Pitfalls

### Pitfall 1: Forgetting to await a coroutine

The most common mistake. A coroutine that is not awaited simply never runs.

**Wrong:**

```python
import asyncio

async def save_to_database(data: dict) -> None:
    await asyncio.sleep(0.01)  # simulate DB write
    print(f"Saved: {data}")

async def main():
    # BUG: save_to_database() returns a coroutine object; it is never actually called!
    save_to_database({"user": "alice"})  # no await!
    print("Done")
    # Output: Done (save never happened)
    # Python may print: RuntimeWarning: coroutine 'save_to_database' was never awaited

asyncio.run(main())
```

**Right:**

```python
async def main():
    # Correct: await the coroutine so it actually executes
    await save_to_database({"user": "alice"})
    print("Done")
    # Output: Saved: {'user': 'alice'}
    #         Done
```

**Why this happens:** `async def` functions return coroutine objects when called. Calling
them without `await` is like getting a to-do note instead of doing the task. Always `await`
coroutines unless you are intentionally scheduling them as a background task with
`asyncio.create_task()`.

---

### Pitfall 2: Blocking the event loop with synchronous I/O

Calling a blocking function directly in an async context freezes the entire program — every
other coroutine is stuck waiting.

**Wrong:**

```python
import asyncio
import time
import urllib.request

async def fetch_blocking(url: str) -> str:
    # BUG: urllib.request.urlopen() is SYNCHRONOUS — it blocks the entire event loop
    # for the duration of the request. No other coroutine can run while this is blocked.
    response = urllib.request.urlopen(url)
    return response.read().decode()

async def heartbeat():
    """Should print every 0.5s to show the event loop is alive."""
    while True:
        print("heartbeat")
        await asyncio.sleep(0.5)

async def main():
    # These two tasks should interleave, but they won't — fetch_blocking freezes everything
    await asyncio.gather(
        fetch_blocking("http://httpbin.org/delay/2"),  # blocks for 2 seconds
        heartbeat(),  # will not print anything during those 2 seconds
    )
```

**Right:**

```python
import aiohttp  # pip install aiohttp

async def fetch_async(url: str) -> str:
    # Correct: aiohttp is async-native — it yields control at every await point
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

**Why this happens:** The event loop only gets to run other coroutines at `await` points.
A blocking call contains no `await` points — the entire thread is stuck. Always use
async-native libraries for I/O in async code.

---

### Pitfall 3: Running asyncio.run() inside an already-running event loop

This is a common mistake when experimenting in Jupyter notebooks or calling async functions
from existing async code.

**Wrong:**

```python
import asyncio

async def main():
    asyncio.run(some_other_coro())  # ERROR: cannot run nested event loop!
```

**Right:**

```python
async def main():
    # Already inside an event loop — just await directly
    await some_other_coro()

    # Or create a task if you want it to run concurrently
    task = asyncio.create_task(some_other_coro())
    await task
```

**Why this happens:** `asyncio.run()` creates and runs a new event loop. Calling it when an
event loop is already running raises `RuntimeError: This event loop is already running.`
Inside an `async def` function, you are already in an event loop — use `await` or
`asyncio.create_task()` instead. (In Jupyter, use `await` directly in cells.)

---

## Cross-Links

- [[django-fastapi-flask]] — FastAPI is built on asyncio; understanding this module is a
  prerequisite for writing performant FastAPI route handlers with `async def`
- [[postgresql]] — async database access (covered in Module 08) depends on understanding
  the event loop model introduced here
- [[systems-architecture]] — the I/O-bound vs. CPU-bound distinction introduced here has
  direct implications for how distributed systems are architected; async services are a
  standard building block in microservice architectures

---

## Summary

- **Concurrency** is interleaving tasks over time on one processor; **parallelism** is
  executing tasks simultaneously on multiple processors. Asyncio provides concurrency, not
  parallelism.
- **I/O-bound** work (network, disk, database) benefits from asyncio because coroutines can
  suspend during I/O and let other coroutines run. **CPU-bound** work requires multiprocessing.
- The **GIL** prevents multiple threads from running Python bytecode simultaneously, making
  threading ineffective for CPU-bound work. Asyncio sidesteps the GIL by using a single thread.
- A **coroutine** is defined with `async def`. Calling it returns a coroutine object; it does
  not run until scheduled. Use `await` inside an async function to run a coroutine and get its
  result.
- The **event loop** is the scheduler: it runs one coroutine at a time, suspending at `await`
  points and resuming coroutines when their I/O completes.
- `asyncio.run(coro)` is the standard entry point: it creates an event loop, runs the
  coroutine to completion, and closes the loop.
- `asyncio.gather(*coros)` runs multiple coroutines concurrently and returns all results.
- **Never block the event loop** with synchronous I/O or CPU-heavy work inside an async
  function — use async-native libraries for I/O, and `asyncio.to_thread()` for blocking
  functions.
