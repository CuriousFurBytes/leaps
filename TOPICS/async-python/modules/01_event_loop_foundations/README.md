# Module 01: Event Loop Foundations

> Build the mental model for async Python by running coroutines on an event loop and observing cooperative scheduling.

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
This module covers orientation, setup, coroutines, tasks, and cooperative scheduling. It emphasizes the mental model first, then applies that model in short runnable programs.

Async Python is easiest to learn when every suspension point is visible. Read each example by asking: which coroutine owns the work, where can it pause, and what other task could run while it is paused?

## Prerequisites
- None; this is the first module.
- Comfortable reading small Python functions and exceptions from [[python]].

## Objectives
By the end of this module, you will be able to:
- Explain the core async concepts introduced in this module.
- Implement small runnable examples using `asyncio`.
- Debug common mistakes by identifying blocking calls, missing awaits, or unsafe cleanup.
- Connect this module to later production patterns in [[async-python]].

## Theory
### Mental Model
Event loops are schedulers for cooperative work. Unlike preemptive operating-system threads, a Python coroutine keeps running until it reaches an `await` that cannot complete immediately. At that point, the coroutine yields control so the loop can resume another ready task. This design grew out of earlier callback and generator-coroutine approaches: programmers wanted high-concurrency I/O without unreadable callback pyramids. Native `async def` made suspension points explicit and local, so the reader can see where control may leave the function.

### Mechanics
A coroutine object is a promise of future work, not work that is already running. Calling an `async def` function creates the coroutine; awaiting it or scheduling it as a task gives the event loop permission to drive it forward. This distinction prevents accidental background work but surprises beginners who expect normal function-call behavior.

### Professional Use
The event loop is most useful when operations wait on external systems. `asyncio.sleep()` is a teaching stand-in for socket, database, or subprocess waiting. It lets us demonstrate that two tasks can overlap their idle time while still using one thread.


### Why This Matters
The event-loop model gives async Python its strengths and its limits. When code reaches an operation that can be represented as waiting, the loop can park that coroutine and resume another one. When code performs CPU-heavy work or calls a blocking function, the loop cannot preempt it in the same way an operating system scheduler can preempt a thread. That is why professional async code reviews focus on suspension points, ownership, and blocking boundaries. A program may look concurrent because it contains many coroutines, yet still behave serially if the coroutines are awaited one at a time or if they block the loop. Conversely, a small number of well-owned tasks can deliver excellent latency because the loop spends most of its time waiting efficiently on external events.

## Key Concepts
- **Coroutine:** A suspended computation created by calling an `async def` function. It does not run to completion until awaited or scheduled.
- **Event loop:** The coordinator that resumes ready coroutines and waits for I/O readiness or timers.
- **Task:** A scheduled coroutine with lifecycle state, cancellation behavior, and a result or exception.
- **Suspension point:** An `await` expression where control may return to the event loop.
- **Backpressure:** Feedback that tells producers to slow down because a consumer, socket, or queue is saturated.

## Examples
### Example 1: Run the smallest async program
```python
import asyncio

async def main():
    # This line runs inside the event loop created by asyncio.run().
    print("hello from a coroutine")

# asyncio.run() creates, runs, and closes the event loop for this program.
asyncio.run(main())
```
This example is intentionally small so you can run it directly and observe the async behavior.

### Example 2: Overlap waiting time
```python
import asyncio

async def fetch_label(label, delay):
    # Sleeping simulates waiting for a network response.
    await asyncio.sleep(delay)
    return f"{label} finished"

async def main():
    # gather waits for both awaitables and preserves result order.
    results = await asyncio.gather(fetch_label("a", 1), fetch_label("b", 1))
    print(results)

asyncio.run(main())
```
This example is intentionally small so you can run it directly and observe the async behavior.

### Example 3: Show explicit suspension
```python
import asyncio

async def worker(name):
    print(f"{name}: before await")
    # This await gives the loop a chance to run another ready task.
    await asyncio.sleep(0)
    print(f"{name}: after await")

async def main():
    await asyncio.gather(worker("first"), worker("second"))

asyncio.run(main())
```
This example is intentionally small so you can run it directly and observe the async behavior.

## Common Pitfalls
### Pitfall 1: Forgetting to await a coroutine
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
