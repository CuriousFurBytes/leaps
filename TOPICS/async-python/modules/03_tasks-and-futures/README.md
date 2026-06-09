# Module 03: Tasks and Futures

[← Module 02](../02_coroutines-and-event-loop/) | [Topic Home](../../README.md) | [Next → Module 04](../04_async-io/)

---

![Status](https://img.shields.io/badge/status-stub-orange)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate-yellow)
![Time](https://img.shields.io/badge/time-5h-orange)

> **Stub module** — Full content to be generated. This file defines the scope and
> prerequisites so the topic roadmap is complete.

---

## Overview

Module 02 covered how the event loop runs coroutines. This module covers **Tasks** —
the higher-level object that wraps a running coroutine and gives you handles to inspect,
cancel, and wait for it. It also covers **Futures** — the low-level awaitable object that
Tasks are built on — and the suite of concurrent execution utilities: `asyncio.gather()`,
`asyncio.wait()`, and `asyncio.wait_for()`.

By the end of this module, you will be able to write programs that orchestrate many
concurrent operations with fine-grained control: start tasks, cancel specific ones,
wait for the first to finish, and handle partial failures gracefully.

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

- Module 02: Coroutines and the Event Loop
- Module 01: Introduction to Async Python

---

## Objectives

By the end of this module, you will be able to:

1. Create and manage Tasks with `asyncio.create_task()`
2. Use `asyncio.gather()` for fan-out concurrency with result collection
3. Use `asyncio.wait()` for fine-grained wait control (FIRST_COMPLETED, ALL_COMPLETED)
4. Apply `asyncio.wait_for()` and `asyncio.timeout()` for timeout handling
5. Cancel tasks and handle `asyncio.CancelledError` correctly
6. Understand the `asyncio.Future` API and when it is used directly

---

## Theory

> **Full content to be generated.** Topics to cover:
>
> - `asyncio.create_task()` vs. directly awaiting a coroutine
> - Task lifecycle: pending → running → cancelled / done (with result or exception)
> - `asyncio.gather()` — concurrent execution, return_exceptions, ordering guarantees
> - `asyncio.wait()` — FIRST_COMPLETED, FIRST_EXCEPTION, ALL_COMPLETED strategies
> - `asyncio.wait_for()` — timeout wrapping, cancellation behavior
> - `asyncio.timeout()` — context manager API (Python 3.11+)
> - Task cancellation: `task.cancel()`, `CancelledError`, cleanup patterns
> - `asyncio.Future` — the low-level awaitable; `set_result()`, `set_exception()`
> - `asyncio.shield()` — protecting a coroutine from cancellation

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

- [[async-python/modules/02_coroutines-and-event-loop]] — prerequisite
- [[async-python/modules/05_synchronization]] — synchronization primitives complement task management
- [[async-python/modules/06_structured-concurrency]] — TaskGroup builds on task/future concepts

---

## Summary

> To be filled in when this module is fully generated.
