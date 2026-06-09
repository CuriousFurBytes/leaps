# Module 02: Coroutines and the Event Loop

[← Module 01](../01_introduction/) | [Topic Home](../../README.md) | [Next → Module 03](../03_tasks-and-futures/)

---

![Status](https://img.shields.io/badge/status-stub-orange)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate-yellow)
![Time](https://img.shields.io/badge/time-5h-orange)

> **Stub module** — Full content to be generated. This file defines the scope and
> prerequisites so the topic roadmap is complete.

---

## Overview

This module is a deep dive into the internals of coroutines and the asyncio event loop.
Module 01 introduced coroutines as "functions that can pause." This module explains the
*mechanism* behind that: how coroutines are implemented on top of Python's generator
protocol, how the event loop works as a scheduler, and how `asyncio.run()` relates to
the lower-level `loop.run_until_complete()`.

Understanding these internals makes you a better async programmer: you know what is
happening under the hood when a coroutine suspends, why certain patterns are safe or
unsafe, and how to diagnose problems that are invisible without this knowledge.

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

## Prerequisites

- Module 01: Introduction to Async Python — coroutines, `await`, `asyncio.run()`
- Python generators — `yield` and the generator protocol (send, throw, StopIteration)

---

## Objectives

By the end of this module, you will be able to:

1. Explain how coroutines are implemented using Python's generator protocol
2. Describe the lifecycle of a coroutine: created → scheduled → running → suspended → done
3. Use `asyncio.get_event_loop()`, `loop.run_until_complete()`, and explain when to use
   each vs. `asyncio.run()`
4. Implement a custom awaitable by defining `__await__`
5. Use `asyncio.to_thread()` to safely call blocking functions from async code
6. Inspect the event loop using `asyncio.current_task()` and `asyncio.all_tasks()`

---

## Theory

> **Full content to be generated.** Topics to cover:
>
> - How coroutines extend the generator protocol (`send()`, `throw()`, `close()`)
> - The coroutine object lifecycle: created, suspended, running, done
> - `asyncio.run()` vs `loop.run_until_complete()` vs `loop.run_forever()`
> - How the event loop uses `selectors` (epoll/kqueue/IOCP) to monitor I/O readiness
> - The `asyncio.AbstractEventLoop` interface and why there are multiple implementations
> - How `asyncio.sleep(0)` works as a yield-to-scheduler primitive
> - Custom awaitables: implementing `__await__`
> - Thread integration: `run_in_executor()` and `asyncio.to_thread()`

---

## Key Concepts

> To be filled in when this module is fully generated.

---

## Examples

> To be filled in when this module is fully generated.

---

## Common Pitfalls

> To be filled in when this module is fully generated.

---

## Cross-Links

- [[async-python/modules/01_introduction]] — prerequisite; coroutines and `asyncio.run()`
- [[async-python/modules/03_tasks-and-futures]] — next module; builds on event loop knowledge
- [[async-python/modules/06_structured-concurrency]] — TaskGroup requires understanding the
  event loop lifecycle covered here

---

## Summary

> To be filled in when this module is fully generated.
