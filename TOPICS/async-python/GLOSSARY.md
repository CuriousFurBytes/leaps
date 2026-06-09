# Glossary: Async Python

> Definitions specific to the Async Python topic. General Python terms are in
> [[shared/glossary]]. Terms here are cross-referenced from module READMEs on first use.

---

## Terms

### async context manager

An object that implements `__aenter__` and `__aexit__` as coroutines, allowing it to be used
with `async with`. The `__aenter__` coroutine runs when entering the block; `__aexit__` runs
on exit (even if an exception occurs). Unlike a regular context manager, the enter and exit
steps can involve awaiting I/O — for example, opening a database connection asynchronously.
Used in Module 04.

### async generator

A function defined with `async def` that contains at least one `yield` expression. It produces
values asynchronously, allowing callers to iterate over it with `async for`. Each `yield` is
a suspension point where other coroutines can run. Async generators combine the iteration
protocol of generators with the suspension capability of coroutines. Used in Module 04.

### async iterator

An object that implements `__aiter__` (returning `self`) and `__anext__` (a coroutine that
returns the next value or raises `StopAsyncIteration`). Used with `async for` loops. The
primary difference from a sync iterator is that `__anext__` can do I/O before returning each
value. Used in Module 04.

### awaitable

Any object that can be used with the `await` keyword. The three built-in awaitable types in
asyncio are coroutines, Tasks, and Futures. A custom object can also be awaitable by
implementing `__await__`. When you `await` something, you suspend the current coroutine until
the awaitable completes. Used in Modules 01–03.

### concurrency

The ability to handle multiple tasks by interleaving their execution over time. Concurrent
tasks do not necessarily run at the same time — they may take turns on a single CPU. Asyncio
provides concurrency via cooperative multitasking: tasks voluntarily suspend at `await` points,
allowing other tasks to run. Contrast with [[async-python#parallelism]]. Used in Module 01.

### cooperative multitasking

A concurrency model in which tasks voluntarily yield control to a scheduler at defined points
(in Python, at every `await`). The scheduler then selects the next runnable task. This
contrasts with preemptive multitasking (used by OS threads), where the scheduler can interrupt
a task at any time. Cooperative multitasking requires all tasks to cooperate — a task that
never awaits will starve other tasks. Used in Modules 01–02.

### coroutine

A function defined with `async def` that can suspend its execution at `await` expressions and
resume later. Calling an `async def` function does not run it — it returns a coroutine
object. The coroutine runs only when it is scheduled by the event loop (e.g., via
`asyncio.run()` or `asyncio.create_task()`). Coroutines are the fundamental unit of work in
asyncio. Used throughout all modules.

### CPU-bound

A workload where the bottleneck is CPU computation — mathematical operations, data
transformation, image processing, etc. CPU-bound tasks cannot be effectively parallelized
within a single Python process using asyncio or threads (due to the GIL). For CPU-bound
work, use `multiprocessing` or `ProcessPoolExecutor`. Contrast with [[async-python#io-bound]].
Used in Module 01.

### event loop

The central scheduler in asyncio. The event loop maintains a queue of ready-to-run coroutines,
runs each one until it suspends at an `await`, then moves to the next. It also monitors I/O
file descriptors and timers to know when suspended coroutines become ready. There is typically
one event loop per thread; `asyncio.run()` creates, runs, and then closes an event loop.
Used in Modules 01–02.

### future

A low-level awaitable object that represents the eventual result of an asynchronous operation.
A Future can be in one of three states: pending, done (with a result), or done (with an
exception). Unlike a Task (which wraps a coroutine), a Future's result is set externally by
calling `future.set_result()`. Most user code works with Tasks, not raw Futures. Used in
Module 03.

### GIL

The **Global Interpreter Lock** — a mutex in CPython that allows only one thread to execute
Python bytecode at a time. It exists to protect CPython's memory management (reference
counting) from concurrent modifications. The GIL means that CPU-bound multithreaded Python
programs cannot achieve true parallelism. Asyncio sidesteps the GIL entirely by running all
coroutines on a single thread — there is nothing to lock. Used in Module 01.

### I/O-bound

A workload where the bottleneck is waiting for input/output operations — network requests,
database queries, file reads. During I/O waits, the CPU is idle. Asyncio is ideal for
I/O-bound work because one thread can service thousands of concurrent I/O operations by
suspending at each wait rather than blocking. Contrast with [[async-python#cpu-bound]].
Used in Module 01.

### parallelism

True simultaneous execution of multiple tasks on multiple CPU cores. In Python, parallelism
requires multiple processes (via `multiprocessing` or `ProcessPoolExecutor`). Asyncio provides
concurrency but not parallelism — all coroutines run on a single thread. Contrast with
[[async-python#concurrency]]. Used in Module 01.

### structured concurrency

A programming model in which the lifetime of concurrent tasks is bounded by the scope in which
they are created. No task can outlive its creating scope. This prevents "fire and forget" tasks
that become orphaned when errors occur. Python 3.11's `TaskGroup` implements structured
concurrency: all tasks in a group are guaranteed to complete (or be cancelled) before the
`async with TaskGroup()` block exits. Used in Module 06.

### task

An asyncio `Task` is a scheduled, running coroutine managed by the event loop. When you call
`asyncio.create_task(coroutine)`, the event loop wraps the coroutine in a Task and schedules
it to run. Tasks can be awaited, cancelled, and inspected for completion or exceptions. Unlike
a raw coroutine (which only runs when explicitly awaited), a Task runs concurrently with the
code that created it. Used in Modules 02–03.
