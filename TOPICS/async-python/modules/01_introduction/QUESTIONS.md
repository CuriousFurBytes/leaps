# Questions: Module 01 — Introduction to Async Python

> Ask any question about this module here. AI agents will answer below your question.
> Never delete questions or answers — this is your learning record.

---

## Question Log

<!-- Questions and answers are appended below in chronological order. -->

### Q1 — If asyncio uses one thread, how is it faster than synchronous code?
**Asked:** 2026-06-09
**Status:** answered

The module says asyncio uses one thread. How can one thread be faster than one thread
(sequential)?

> **Answer** — *2026-06-09T00:00:00Z — claude-sonnet-4-6*
>
> This is exactly the right question to ask — it's the conceptual key to asyncio.
>
> Asyncio with one thread is NOT faster than sequential code for any single operation.
> A single HTTP request takes the same amount of time whether you use asyncio or not.
>
> The difference is what happens while you are waiting. In sequential code, while
> request A is in-flight, the thread is blocked — it cannot start request B. In asyncio,
> while request A is in-flight, the thread is free — the event loop uses that idle time
> to start request B, and C, and D, and E...
>
> The time savings come from overlapping the wait times:
> - Sequential: 3 requests × 1 second each = 3 seconds total
> - Async: 3 requests, all in-flight simultaneously = ~1 second total
>
> Asyncio doesn't make individual operations faster. It prevents the CPU from being
> idle while waiting, by filling that idle time with other work.
>
> *Further reading: [[async-python/modules/01_introduction#the-problem-blocking-io]]*

### Q2 — Why does Python have the GIL but other languages don't?
**Asked:** 2026-06-09
**Status:** answered

Java and C# don't have a GIL but Python does. Why?

> **Answer** — *2026-06-09T00:00:00Z — claude-sonnet-4-6*
>
> The GIL is a consequence of CPython's implementation choice for memory management:
> reference counting. Every Python object has a counter that tracks how many references
> point to it. When the counter reaches zero, the object is freed.
>
> If two threads could modify reference counts simultaneously, they could corrupt those
> counts — leading to premature frees (crashes) or memory leaks. The GIL prevents this
> by ensuring only one thread touches Python objects at a time.
>
> Java and C# use garbage collectors with a tracing/mark-and-sweep approach rather than
> reference counting. Tracing GCs are designed from the ground up to be thread-safe in
> a different way (they have their own pause-the-world mechanisms, but they don't need
> a global lock for every object access).
>
> CPython's designers could have replaced reference counting with a tracing GC early on,
> but the GIL was simpler and safer for the C extension ecosystem. Removing the GIL is
> now being actively worked on (PEP 703 — Python 3.13+), but it's extraordinarily complex
> because thousands of C extensions depend on the GIL's protections.
>
> *Further reading: [[async-python/modules/01_introduction#the-gil-what-it-is-and-why-it-exists]]*

### Q3 — What is the difference between await and yield?
**Asked:** 2026-06-09
**Status:** answered

I know about Python generators with yield. How does await relate to yield?

> **Answer** — *2026-06-09T00:00:00Z — claude-sonnet-4-6*
>
> Great question — they are deeply related, which is why understanding generators helps
> with coroutines.
>
> **`yield`** suspends a generator and returns a value to whoever called `next()` on it.
> The generator can be resumed later by calling `next()` again.
>
> **`await`** suspends a coroutine and returns control to the event loop. When the
> awaited thing (e.g., a timer, I/O completion) finishes, the event loop resumes the
> coroutine automatically.
>
> In fact, before Python 3.5 introduced `async def` and `await`, coroutines were built
> using `@asyncio.coroutine` and `yield from` — the generator protocol was the
> implementation mechanism for coroutines. `async def` / `await` is cleaner syntax
> over the same underlying idea.
>
> The key difference: `yield` gives control to the caller and can pass a value out.
> `await` gives control to the event loop and waits for a specific thing to be ready.
> The event loop is invisible — it's automatic.
>
> You can still see this connection: `asyncio.Future.__await__` is implemented using
> `yield`. Coroutines and generators share the same underlying suspension mechanism.
>
> *Further reading: [[async-python/modules/02_coroutines-and-event-loop]]*
