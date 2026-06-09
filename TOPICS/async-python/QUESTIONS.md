# Questions: Async Python

> Ask any question about the Async Python topic here — questions that span multiple modules,
> or questions that arise before you know which module they belong to.
> AI agents will answer below your question.
> Never delete questions or answers — this is your learning record.

---

## Question Log

<!-- Questions and answers are appended below in chronological order. -->

### Q1 — When should I use asyncio vs. threading vs. multiprocessing?
**Asked:** 2026-06-09
**Status:** answered

How do I decide which concurrency model to choose for a Python program?

> **Answer** — *2026-06-09T00:00:00Z — claude-sonnet-4-6*
>
> The choice depends entirely on what your bottleneck is:
>
> - **asyncio** — choose this for I/O-bound work where you need high concurrency
>   (thousands of simultaneous network connections, database queries, or file operations).
>   Asyncio uses a single thread, so it has very low overhead and no GIL contention.
>   FastAPI, web scrapers, and real-time dashboards are canonical use cases.
>
> - **threading** — choose this when you need concurrency and the tasks involve I/O but
>   you're working with libraries that are not async-aware (e.g., blocking SQL drivers,
>   legacy REST clients). The GIL is released during I/O, so threads help here. However,
>   the overhead of OS threads limits you to hundreds — not thousands — of concurrent
>   operations.
>
> - **multiprocessing** — choose this for CPU-bound work (number crunching, image
>   processing, ML inference). Each process has its own Python interpreter and GIL, so
>   multiple cores are used genuinely in parallel.
>
> Quick decision rule: Is your bottleneck CPU computation? Use multiprocessing.
> Is it I/O and you can use async libraries? Use asyncio.
> Is it I/O but you're stuck with blocking libraries? Use threading.
>
> *Further reading: [[async-python/modules/01_introduction]]*

### Q2 — Does asyncio use multiple CPU cores?
**Asked:** 2026-06-09
**Status:** answered

I see asyncio mentioned with "high performance" — does that mean it uses multiple cores?

> **Answer** — *2026-06-09T00:00:00Z — claude-sonnet-4-6*
>
> No — asyncio runs on a single thread and a single CPU core by default. Its "high
> performance" comes from I/O concurrency, not CPU parallelism. While one coroutine is
> waiting for a network response, hundreds of other coroutines can make progress on their
> own I/O — all on the same thread, with essentially no context-switch overhead.
>
> If you need to both handle many concurrent I/O operations *and* use multiple CPU cores,
> the standard pattern is to run multiple worker processes (each with their own asyncio
> event loop) behind a process manager like `gunicorn --worker-class uvicorn.workers.UvicornWorker`.
> Each process handles its own I/O concurrently; the OS distributes processes across cores.
>
> For occasional CPU-heavy work within an async program, use
> `asyncio.get_event_loop().run_in_executor()` to offload it to a thread pool or process
> pool without blocking the event loop.
>
> *Further reading: [[async-python/modules/01_introduction]], [[async-python/modules/07_performance-patterns]]*

### Q3 — What Python version do I need for asyncio?
**Asked:** 2026-06-09
**Status:** answered

This topic mentions features from Python 3.11 and 3.7. What is the minimum version?

> **Answer** — *2026-06-09T00:00:00Z — claude-sonnet-4-6*
>
> The minimum version for the modern asyncio API (with `async def`, `await`, and
> `asyncio.run()`) is **Python 3.7**. For this topic, Python 3.8+ is recommended as
> the baseline — it's the oldest version still in widespread use that has `asyncio.run()`,
> `asyncio.create_task()`, and the `async for` / `async with` protocol fully stabilized.
>
> Features covered in this topic that require specific versions:
> - `asyncio.run()` — Python 3.7+
> - `asyncio.TaskGroup` and `ExceptionGroup` — Python 3.11+
> - `asyncio.timeout()` context manager — Python 3.11+
>
> Module 06 (Structured Concurrency) specifically covers Python 3.11 features, and includes
> anyio as the alternative for codebases that must support Python 3.8–3.10.
>
> All code examples in this topic note their minimum Python version requirement.
>
> *Further reading: [[async-python/modules/06_structured-concurrency]]*

### Q4 — How does asyncio relate to Trio and Curio?
**Asked:** 2026-06-09
**Status:** answered

I've seen mentions of Trio as an alternative. How do they compare?

> **Answer** — *2026-06-09T00:00:00Z — claude-sonnet-4-6*
>
> **Trio** (by Nathaniel J. Smith) and **Curio** (by David Beazley) are alternative async
> libraries that inspired many of asyncio's later design decisions.
>
> Trio introduced *structured concurrency* (the "nursery" pattern) years before asyncio's
> TaskGroup was added — Python 3.11's TaskGroup is directly influenced by Trio nurseries.
> Trio also has a reputation for cleaner error handling and better cancellation semantics.
>
> Curio was Beazley's exploration of a simpler, lower-level async primitive set, primarily
> for education and research.
>
> In 2026, for production use, `asyncio` is almost always the right choice because:
> - It's in the standard library (no dependency to add)
> - The entire Python web ecosystem (FastAPI, aiohttp, SQLAlchemy async) is built on it
> - Python 3.11's TaskGroup closes most of Trio's ergonomic advantages
>
> **anyio** is a compatibility layer that lets you write code targeting both asyncio and
> Trio. It's worth knowing if you write library code that others will use in either runtime.
> This is covered in Module 06.
>
> *Further reading: [[async-python/modules/06_structured-concurrency]]*

### Q5 — Can I mix synchronous and asynchronous code?
**Asked:** 2026-06-09
**Status:** answered

What happens if I call a normal (blocking) function from inside an async function?

> **Answer** — *2026-06-09T00:00:00Z — claude-sonnet-4-6*
>
> You can call synchronous functions from async functions — but if the sync function blocks
> (e.g., makes a network request, reads a large file, does heavy computation), it will block
> the *entire event loop* for the duration. No other coroutines will run until that blocking
> call returns. This is one of the most common and dangerous mistakes in async Python.
>
> The fix is `loop.run_in_executor()` (or the equivalent `asyncio.to_thread()` in Python 3.9+),
> which runs a blocking function in a thread pool, freeing the event loop:
>
> ```python
> import asyncio
> import time
>
> def blocking_sleep(seconds):
>     time.sleep(seconds)  # blocks the thread — fine in an executor
>
> async def main():
>     # This runs blocking_sleep in a thread, not blocking the event loop
>     await asyncio.to_thread(blocking_sleep, 1)
>     print("Done — event loop was free during the sleep")
>
> asyncio.run(main())
> ```
>
> The rule of thumb: any call that might block for more than a millisecond should either
> be an async call (using `await`) or be run in an executor.
>
> *Further reading: [[async-python/modules/01_introduction]], [[async-python/modules/02_coroutines-and-event-loop]]*
