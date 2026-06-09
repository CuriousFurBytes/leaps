# Module 05: Synchronization Primitives

[← Module 04](../04_async-io/) | [Topic Home](../../README.md) | [Next → Module 06](../06_structured-concurrency/)

---

![Status](https://img.shields.io/badge/status-stub-orange)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate-yellow)
![Time](https://img.shields.io/badge/time-4h-orange)

> **Stub module** — Full content to be generated. This file defines the scope and
> prerequisites so the topic roadmap is complete.

---

## Overview

Asyncio runs on a single thread, so many classic threading race conditions cannot occur.
But concurrent coroutines *can* interleave at `await` points, and shared state is still
possible to corrupt if not protected. This module covers `asyncio`'s synchronization
primitives — the async equivalents of threading locks, events, semaphores, and queues —
and when to use each.

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

- Module 04: Async I/O Patterns
- Module 03: Tasks and Futures

---

## Objectives

By the end of this module, you will be able to:

1. Identify when shared state needs protection in async code
2. Use `asyncio.Lock` for mutual exclusion
3. Use `asyncio.Event` to signal between coroutines
4. Use `asyncio.Semaphore` to limit concurrency
5. Use `asyncio.Queue` for producer-consumer patterns
6. Implement a simple worker pool using `Queue` and `create_task()`

---

## Theory

> **Full content to be generated.** Topics to cover:
>
> - Why single-threaded asyncio still needs synchronization (the read-modify-await-write race)
> - `asyncio.Lock`: mutual exclusion, `async with lock:` pattern, deadlock risk
> - `asyncio.Event`: one-shot notifications, resetting, broadcasting to multiple waiters
> - `asyncio.Condition`: coordinating waiters with a condition predicate
> - `asyncio.Semaphore` and `asyncio.BoundedSemaphore`: limiting concurrency
> - `asyncio.Queue`, `asyncio.LifoQueue`, `asyncio.PriorityQueue`
> - Producer-consumer pattern with `queue.put()`, `queue.get()`, `queue.join()`
> - Worker pool pattern: fixed number of worker tasks draining a queue

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

- [[async-python/modules/04_async-io]] — prerequisite; async I/O patterns this module builds on
- [[async-python/modules/06_structured-concurrency]] — structured concurrency provides a
  better alternative to manual task coordination in many cases
- [[async-python/modules/07_performance-patterns]] — Semaphore-based rate limiting builds
  directly on this module

---

## Summary

> To be filled in when this module is fully generated.
