# Cheatsheet: Async Python

> Quick reference for asyncio API, common patterns, and error handling.
> For in-depth explanations, see the relevant module README.

---

## Table of Contents

- [Core API](#core-api)
- [Running Coroutines](#running-coroutines)
- [Tasks and Concurrency](#tasks-and-concurrency)
- [Synchronization](#synchronization)
- [Async I/O Patterns](#async-io-patterns)
- [Error Handling](#error-handling)
- [Common Patterns](#common-patterns)
- [Quick Decision Guide](#quick-decision-guide)

---

## Core API

| Function / Class | What It Does | Module |
|-----------------|-------------|--------|
| `asyncio.run(coro)` | Create event loop, run coroutine to completion, close loop | 01 |
| `asyncio.create_task(coro)` | Schedule coroutine as a Task (starts immediately) | 03 |
| `asyncio.gather(*awaitables)` | Run multiple awaitables concurrently; return all results | 03 |
| `asyncio.wait(tasks, ...)` | Wait for tasks with fine-grained control over completion | 03 |
| `asyncio.sleep(seconds)` | Async sleep (yields control to event loop) | 02 |
| `asyncio.timeout(seconds)` | Context manager for timeouts (Python 3.11+) | 06 |
| `asyncio.wait_for(coro, timeout)` | Run coroutine with timeout | 03 |
| `asyncio.TaskGroup()` | Structured concurrency group (Python 3.11+) | 06 |
| `asyncio.get_event_loop()` | Get the running event loop | 02 |
| `asyncio.current_task()` | Get the currently running Task | 03 |
| `asyncio.all_tasks()` | Get all running Tasks | 03 |
| `asyncio.to_thread(func, *args)` | Run sync function in thread pool (Python 3.9+) | 02 |
| `asyncio.Queue(maxsize)` | Async producer/consumer queue | 05 |
| `asyncio.Lock()` | Mutual exclusion lock | 05 |
| `asyncio.Semaphore(n)` | Limit concurrent access to N | 05 |
| `asyncio.Event()` | Notify one or more waiters | 05 |

---

## Running Coroutines

```python
import asyncio

# Define a coroutine
async def greet(name: str) -> str:
    await asyncio.sleep(0.1)  # simulate I/O
    return f"Hello, {name}!"

# Run from synchronous code — the standard entry point
result = asyncio.run(greet("world"))
print(result)  # Hello, world!
```

---

## Tasks and Concurrency

```python
import asyncio

# Run multiple coroutines concurrently — gather() returns results in order
async def main():
    results = await asyncio.gather(
        fetch("https://example.com/a"),
        fetch("https://example.com/b"),
        fetch("https://example.com/c"),
    )
    # results is a list in the same order as the arguments

# Create a task explicitly (fires immediately, doesn't need to be awaited right away)
async def main():
    task = asyncio.create_task(long_operation())
    # Do other work here...
    result = await task  # wait for it now

# TaskGroup — structured concurrency (Python 3.11+)
async def main():
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(operation_one())
        t2 = tg.create_task(operation_two())
    # Both tasks are guaranteed complete here
    # If any task raises, the group cancels the others and re-raises

# Limit concurrency with a Semaphore
sem = asyncio.Semaphore(10)  # max 10 concurrent

async def bounded_fetch(url):
    async with sem:
        return await fetch(url)
```

---

## Synchronization

```python
import asyncio

# Lock — mutual exclusion
lock = asyncio.Lock()

async def safe_increment(counter: list):
    async with lock:
        counter[0] += 1  # only one coroutine runs this at a time

# Event — notify waiters
event = asyncio.Event()

async def waiter():
    await event.wait()
    print("Event fired!")

async def setter():
    await asyncio.sleep(1)
    event.set()

# Queue — producer/consumer
queue = asyncio.Queue(maxsize=100)

async def producer():
    for item in range(10):
        await queue.put(item)
    await queue.put(None)  # sentinel

async def consumer():
    while True:
        item = await queue.get()
        if item is None:
            break
        process(item)
        queue.task_done()
```

---

## Async I/O Patterns

```python
import aiohttp
import aiofiles
import asyncio

# Async HTTP GET with aiohttp
async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# Reuse a session across requests (preferred in production)
async def fetch_many(urls: list[str]) -> list[str]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_session(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Async file I/O with aiofiles
async def read_file(path: str) -> str:
    async with aiofiles.open(path, mode="r") as f:
        return await f.read()

# Async generator
async def paginated_results(api_url: str):
    page = 1
    while True:
        data = await fetch(f"{api_url}?page={page}")
        if not data:
            break
        yield data
        page += 1

# Consume an async generator
async def process_all():
    async for page in paginated_results("https://api.example.com/items"):
        process(page)
```

---

## Error Handling

```python
import asyncio

# Handle errors in gather() — return_exceptions=True prevents short-circuiting
async def main():
    results = await asyncio.gather(
        risky_operation_1(),
        risky_operation_2(),
        return_exceptions=True,  # exceptions returned as values, not raised
    )
    for r in results:
        if isinstance(r, Exception):
            print(f"Error: {r}")
        else:
            process(r)

# Timeout handling
async def with_timeout():
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=5.0)
    except asyncio.TimeoutError:
        print("Operation timed out")

# Python 3.11+: asyncio.timeout() context manager
async def with_timeout_311():
    async with asyncio.timeout(5.0):
        result = await slow_operation()
    # asyncio.TimeoutError raised if it exceeds 5s

# Task cancellation
async def cancellable_task():
    try:
        await long_running_operation()
    except asyncio.CancelledError:
        # Clean up resources before propagating
        await cleanup()
        raise  # always re-raise CancelledError

# ExceptionGroup handling (Python 3.11+ with TaskGroup)
async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(op_one())
            tg.create_task(op_two())
    except* ValueError as eg:
        for exc in eg.exceptions:
            print(f"ValueError: {exc}")
    except* IOError as eg:
        for exc in eg.exceptions:
            print(f"IOError: {exc}")
```

---

## Common Patterns

### Fan-out and Fan-in

```python
async def fan_out_fan_in(items: list) -> list:
    """Process many items concurrently, collect all results."""
    tasks = [asyncio.create_task(process(item)) for item in items]
    results = await asyncio.gather(*tasks)
    return list(results)
```

### Worker Pool

```python
async def worker_pool(jobs: list, n_workers: int = 5):
    """Process jobs with a fixed number of concurrent workers."""
    queue = asyncio.Queue()
    for job in jobs:
        await queue.put(job)

    async def worker():
        while not queue.empty():
            job = await queue.get()
            await process(job)
            queue.task_done()

    workers = [asyncio.create_task(worker()) for _ in range(n_workers)]
    await queue.join()
    for w in workers:
        w.cancel()
```

### Retry with Backoff

```python
import asyncio

async def with_retry(coro_func, *args, retries=3, base_delay=1.0):
    """Call an async function, retrying with exponential backoff on failure."""
    for attempt in range(retries):
        try:
            return await coro_func(*args)
        except Exception as e:
            if attempt == retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            await asyncio.sleep(delay)
```

---

## Quick Decision Guide

| Situation | Solution |
|-----------|----------|
| Run one coroutine from sync code | `asyncio.run(coro)` |
| Run N coroutines, need all results | `asyncio.gather(*coros)` |
| Run N coroutines, structured lifetime | `asyncio.TaskGroup()` |
| Limit to M concurrent operations | `asyncio.Semaphore(M)` |
| Protect shared data | `asyncio.Lock()` |
| Communicate between tasks | `asyncio.Queue()` |
| Add a timeout | `asyncio.wait_for(coro, timeout=N)` |
| Call a blocking function safely | `asyncio.to_thread(func, *args)` |
| Sleep without blocking | `await asyncio.sleep(seconds)` |
| Cancel a task | `task.cancel()` then `await task` |
