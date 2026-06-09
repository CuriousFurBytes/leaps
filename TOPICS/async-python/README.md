# Async Python

> Learn to design, debug, and ship Python programs that use `async` and `await` for high-concurrency I/O.

## Table of Contents
1. [Why Learn Async Python?](#why-learn-async-python)
2. [Prerequisites](#prerequisites)
3. [Module Map](#module-map)
4. [Cross-Links](#cross-links)
5. [Quick Reference](#quick-reference)

## Why Learn Async Python?
Async Python is Python's model for cooperative concurrency: many operations can make progress while each task waits for slow I/O such as sockets, databases, queues, subprocesses, or web APIs. It matters because modern services often spend more time waiting than computing, and one well-designed event loop can supervise thousands of in-flight operations without assigning a thread to each one.

Historically, Python grew from callback-based frameworks and generator coroutines toward native `async def` coroutines and `await`, giving programmers a readable way to express non-blocking workflows. The key mental shift is that async code is not automatically faster CPU code; it is a coordination tool for latency-heavy work.

This topic starts from zero: what an event loop is, why coroutines pause, and how to run the smallest program. It then moves through cancellation, streams, coordination primitives, web services, persistence, testing, profiling, and finally production architecture.

By the end, you should be able to reason like an experienced async Python practitioner: identify blocking hazards, design cancellation-safe workflows, use backpressure, test race-prone code, and explain when async is the wrong tool.

## Prerequisites
- [[python]] — functions, exceptions, context managers, iterators, and basic packaging.
- [[networking]] — helpful but not mandatory; the stream modules introduce the needed socket vocabulary.
- [[operating-systems]] — helpful for understanding threads, processes, file descriptors, and scheduling.

## Module Map
| # | Module | Difficulty | Status |
|---|--------|------------|--------|
| 01 | [Event Loop Foundations](./modules/01_event_loop_foundations/) | Beginner | [ ] |
| 02 | [Awaitables, Tasks, and Cancellation](./modules/02_awaitables_tasks_and_cancellation/) | Beginner | [ ] |
| 03 | [Async I/O Streams and Clients](./modules/03_async_io_streams_and_clients/) | Intermediate | [ ] |
| 04 | Coordination Primitives | Intermediate | [ ] |
| 05 | Error Handling and Resilience | Intermediate | [ ] |
| 06 | Async Web Services | Advanced | [ ] |
| 07 | Databases and Persistence | Advanced | [ ] |
| 08 | Testing and Debugging Async Code | Advanced | [ ] |
| 09 | Performance and Profiling | Advanced | [ ] |
| 10 | Interop with Threads and Processes | Expert | [ ] |
| 11 | Runtime Internals and Architecture | Expert | [ ] |
| 12 | [Capstone Project](./modules/12_capstone_project/) | Expert | [ ] |

## Cross-Links
- [[python]] for the language foundations behind `async def`, exceptions, and context managers.
- [[networking]] for sockets, protocols, and request/response thinking.
- [[operating-systems]] for scheduling, threads, processes, and blocking I/O.
- [[web-development]] for service boundaries, HTTP clients, and APIs.

## Quick Reference
| Task | Pattern |
|---|---|
| Run one coroutine | `asyncio.run(main())` |
| Pause until an awaitable finishes | `result = await awaitable` |
| Start concurrent work | `task = asyncio.create_task(coro())` |
| Wait for many tasks | `await asyncio.gather(*tasks)` or `asyncio.TaskGroup()` |
| Add a timeout | `async with asyncio.timeout(seconds): ...` |
| Avoid blocking the loop | Use async libraries or `asyncio.to_thread()` for blocking calls |
| Communicate between tasks | `asyncio.Queue` |
| Limit concurrency | `asyncio.Semaphore` |

> [!IMPORTANT]
> Async Python is primarily for I/O concurrency. CPU-bound work still needs vectorized code, native extensions, processes, or other parallel execution strategies.
