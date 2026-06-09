# Module 02: Awaitables, Tasks, and Cancellation

> Learn how awaitables become tasks, how cancellation travels, and how to write cleanup-safe async code.

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

## Overview
This module covers awaitable types, task lifecycles, structured waiting, timeouts, and cancellation. It emphasizes the mental model first, then applies that model in short runnable programs.

Async Python is easiest to learn when every suspension point is visible. Read each example by asking: which coroutine owns the work, where can it pause, and what other task could run while it is paused?

## Prerequisites
- Module 01: Event Loop Foundations.
- Comfortable reading small Python functions and exceptions from [[python]].

## Objectives
By the end of this module, you will be able to:
- Explain the core async concepts introduced in this module.
- Implement small runnable examples using `asyncio`.
- Debug common mistakes by identifying blocking calls, missing awaits, or unsafe cleanup.
- Connect this module to later production patterns in [[async-python]].

## Theory
### Mental Model
An awaitable is anything Python can pause on with `await`: native coroutine objects, tasks, futures, and custom objects implementing the await protocol. A task wraps a coroutine and registers it with the event loop so it can make progress independently while the current coroutine does something else.

### Mechanics
Cancellation is cooperative. Calling `task.cancel()` requests that a `CancelledError` be injected at the task's next suspension point. The task may run cleanup code before the cancellation is complete, which is why robust async code uses `try`/`finally` around acquired resources.

### Professional Use
Modern async Python encourages structured concurrency: tasks should have an owning scope, and that scope should decide what happens when one child fails. `asyncio.TaskGroup` makes this relationship explicit, preventing orphaned background tasks that keep running after the caller has moved on.


### Why This Matters
Awaitables and cancellation are where toy examples become real systems. A service that cannot cancel obsolete work wastes capacity, delays shutdown, and may write stale results after callers have gone away. A service that cancels aggressively but forgets cleanup can leak sockets, locks, or database transactions. The practical goal is to make each task's lifetime obvious: who created it, who waits for it, what happens if it fails, and what happens if the parent no longer needs it. This is also why timeouts are not just error handling. They are a resource policy that prevents one slow dependency from consuming all attention in the event loop.

## Key Concepts
- **Coroutine:** A suspended computation created by calling an `async def` function. It does not run to completion until awaited or scheduled.
- **Event loop:** The coordinator that resumes ready coroutines and waits for I/O readiness or timers.
- **Task:** A scheduled coroutine with lifecycle state, cancellation behavior, and a result or exception.
- **Suspension point:** An `await` expression where control may return to the event loop.
- **Backpressure:** Feedback that tells producers to slow down because a consumer, socket, or queue is saturated.

## Examples
### Example 1: Create and await a task
```python
import asyncio

async def compute():
    # Simulate async I/O before returning a value.
    await asyncio.sleep(0.1)
    return 42

async def main():
    task = asyncio.create_task(compute())
    result = await task
    print(result)

asyncio.run(main())
```
This example is intentionally small so you can run it directly and observe the async behavior.

### Example 2: Use a timeout
```python
import asyncio

async def slow_call():
    # This operation is slower than the caller allows.
    await asyncio.sleep(10)

async def main():
    try:
        async with asyncio.timeout(0.2):
            await slow_call()
    except TimeoutError:
        print("timed out safely")

asyncio.run(main())
```
This example is intentionally small so you can run it directly and observe the async behavior.

### Example 3: Clean up during cancellation
```python
import asyncio

async def worker():
    try:
        while True:
            # Every await is a possible cancellation point.
            await asyncio.sleep(1)
    finally:
        print("release resources here")

async def main():
    task = asyncio.create_task(worker())
    await asyncio.sleep(0.1)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("worker cancelled")

asyncio.run(main())
```
This example is intentionally small so you can run it directly and observe the async behavior.

## Common Pitfalls
### Pitfall 1: Swallowing cancellation accidentally
Wrong approach:
```python
async def load():
    return "data"

value = load()
print(value)  # Prints a coroutine object, not "data".
```
Correct approach:
```python
import asyncio

async def load():
    return "data"

async def main():
    value = await load()
    print(value)

asyncio.run(main())
```
This mistake happens because `async def` looks like normal `def`, but calling it creates a coroutine object.

### Pitfall 2: Blocking the event loop
Wrong approach:
```python
import time

async def pause_badly():
    time.sleep(1)  # Blocks the whole event loop thread.
```
Correct approach:
```python
import asyncio

async def pause_cooperatively():
    await asyncio.sleep(1)  # Lets other tasks run while waiting.
```
Use async-friendly libraries or move unavoidable blocking calls to a thread.

### Pitfall 3: Losing task ownership
Wrong approach:
```python
import asyncio

async def main():
    asyncio.create_task(asyncio.sleep(10))  # No owner awaits or cancels it.
```
Correct approach:
```python
import asyncio

async def main():
    task = asyncio.create_task(asyncio.sleep(10))
    await task
```
Every task should have an owner that awaits it, cancels it, or supervises it in a structured scope.

## Cross-Links
- [[async-python]]
- [[python]]
- [[networking]]
- [[operating-systems]]

## Summary
- Async Python uses explicit suspension points to coordinate I/O-bound work.
- Coroutines are not threads; they run cooperatively on an event loop.
- Tasks give coroutines independent lifecycle state and must be owned.
- Cancellation, cleanup, and backpressure are design concerns, not afterthoughts.
- Small runnable examples are the best way to build intuition before production use.
