# Answers: Module 03 — Async I/O Streams and Clients

## Answer Key

### Easy Questions
**Q1:** A coroutine is a paused async computation produced by calling an `async def` function.
**Q2:** It coordinates ready tasks, timers, and I/O readiness.
**Q3:** `await`.
**Q4:** It blocks the event-loop thread and prevents other tasks from running.
**Q5:** A caller, task group, supervisor, or other explicit lifecycle scope.

### Medium Questions
**Q6:** It overlaps waiting time for sockets, databases, APIs, and timers without one thread per operation.
**Q7:** Direct awaiting runs as part of the current flow; task scheduling lets it progress independently until awaited or cancelled.
**Q8:** Cancellation is requested and delivered at suspension points, allowing cleanup before completion.
**Q9:** Backpressure slows producers when consumers, buffers, or sockets cannot keep up.
**Q10:** CPU-bound work, simple scripts, or code dominated by blocking-only libraries may be better served by other approaches.

### Hard Questions
**Q11:** A correct answer uses `asyncio.run()`, two async functions, and `asyncio.gather()` or tasks.
**Q12:** The coroutine must be awaited inside an async main run by `asyncio.run()`.
**Q13:** A correct answer uses `asyncio.timeout()` or `asyncio.wait_for()` and handles timeout.
**Q14:** A correct answer uses `try`/`finally` and awaits the cancelled task while handling `CancelledError` where appropriate.

### Expert Questions
**Q15:** Strong answers include bounded concurrency, explicit task ownership, timeout/cancellation policy, and queue or drain-based backpressure.
**Q16:** Strong answers mention logs, slow callback warnings, task dumps, profiling, blocking-call audit, and latency metrics.

### Bonus Questions
**Bonus 1:** Async concurrency interleaves waiting tasks on an event loop; parallel CPU execution runs computations simultaneously on multiple cores or processes.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
