# Module 12: Capstone Project

> Plan and build a realistic asynchronous Python service without receiving a copy-paste solution.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Project Brief](#project-brief)
6. [Milestones](#milestones)
7. [Help / Getting Unstuck](#help--getting-unstuck)
8. [Key Concepts](#key-concepts)
9. [Examples](#examples)
10. [Common Pitfalls](#common-pitfalls)
11. [Cross-Links](#cross-links)
12. [Summary](#summary)

## Overview
This module covers a production-minded asynchronous service that synthesizes the whole topic. It emphasizes the mental model first, then applies that model in short runnable programs.

Async Python is easiest to learn when every suspension point is visible. Read each example by asking: which coroutine owns the work, where can it pause, and what other task could run while it is paused?

## Prerequisites
- Modules 01 through 11.
- Comfortable reading small Python functions and exceptions from [[python]].

## Objectives
By the end of this module, you will be able to:
- Explain the core async concepts introduced in this module.
- Implement small runnable examples using `asyncio`.
- Debug common mistakes by identifying blocking calls, missing awaits, or unsafe cleanup.
- Connect this module to later production patterns in [[async-python]].

## Theory
### Mental Model
The capstone is a build module: you will create an async service that monitors multiple HTTP endpoints, records observations, exposes a small API or report, and shuts down cleanly. The point is synthesis. You must combine event-loop reasoning, cancellation, backpressure, resource ownership, testing, and production tradeoffs.

### Mechanics
A strong capstone design treats concurrency as a budgeted resource. It limits outbound calls, gives each operation a timeout, sends results through queues, and makes shutdown a first-class path rather than an afterthought. The implementation should be small enough to understand and realistic enough to resemble work done on a professional service team.

### Professional Use
Do not paste a complete solution from this module. Use the milestones, acceptance criteria, and help sections to drive your own implementation. If you get stuck, reveal only the hint you need, then return to building.


### Why This Matters
A capstone is where judgment matters more than syntax. The same service can be built as a fragile pile of background tasks or as a supervised system with clear resource budgets and failure semantics. Your design should make it possible to answer operational questions: how many checks can run at once, how long can shutdown take, what happens when one target is slow, and where can an operator see recent failures? Those questions force you to connect language-level async mechanics with service-level architecture.

## Project Brief
Build an asynchronous endpoint monitor. It should read a small list of targets, check them repeatedly or on demand, limit concurrency, capture success and failure details, expose a human-readable report, and stop cleanly when cancelled.

The artifact may be a command-line tool, a small API service, or a library with a runnable demo. Choose the shape that best demonstrates your learning, but keep the operational requirements visible.

## Milestones
1. Define immutable target and result models.
2. Implement one fake checker and one real checker.
3. Add bounded concurrency with a queue, semaphore, or task group.
4. Add per-check timeouts and cancellation-safe cleanup.
5. Record recent results and expose a report.
6. Test success, timeout, cancellation, and partial failure paths.
7. Write an architecture review explaining tradeoffs and future improvements.

## Help / Getting Unstuck
Use these hints gradually. The goal is to help you keep building, not to hand you a complete copy-paste solution.

### Hint 1: Start Fake
Use `asyncio.sleep()` and deterministic fake results before introducing network I/O. This lets you verify scheduling and cancellation first.

### Hint 2: Bound Work Early
Add a semaphore or queue before adding many targets. If the service is unsafe with ten fake targets, it will be unsafe with real endpoints.

### Hint 3: Treat Shutdown as a Feature
Send cancellation while work is active and confirm that workers release resources, pending work is accounted for, and final output is understandable.

## Key Concepts
- **Coroutine:** A suspended computation created by calling an `async def` function. It does not run to completion until awaited or scheduled.
- **Event loop:** The coordinator that resumes ready coroutines and waits for I/O readiness or timers.
- **Task:** A scheduled coroutine with lifecycle state, cancellation behavior, and a result or exception.
- **Suspension point:** An `await` expression where control may return to the event loop.
- **Backpressure:** Feedback that tells producers to slow down because a consumer, socket, or queue is saturated.

## Examples
### Example 1: Sketch the service boundary
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class CheckTarget:
    # A target is input data for one recurring async check.
    name: str
    url: str
    timeout_seconds: float
```
This example is intentionally small so you can run it directly and observe the async behavior.

### Example 2: Sketch a result model
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class CheckResult:
    # A result is immutable evidence produced by the checker.
    name: str
    ok: bool
    latency_ms: float
    detail: str
```
This example is intentionally small so you can run it directly and observe the async behavior.

### Example 3: Sketch a cancellation-safe worker
```python
import asyncio

async def worker(queue):
    try:
        while True:
            item = await queue.get()
            try:
                print(f"handle {item}")
            finally:
                queue.task_done()
    finally:
        print("worker cleanup")
```
This example is intentionally small so you can run it directly and observe the async behavior.

## Common Pitfalls
### Pitfall 1: Building without shutdown design
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
