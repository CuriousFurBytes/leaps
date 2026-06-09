# Resources: Module 01 — Introduction to Async Python

> Verified resources relevant to this module's content on concurrency models, the GIL,
> and the foundational asyncio concepts.

---

## Primary Resources

1. **[asyncio — Asynchronous I/O (Python docs)](https://docs.python.org/3/library/asyncio.html)**
   — The official reference. Start with the "High-level API" section, which covers
   `asyncio.run()`, `gather()`, and task creation at the level this module introduces.

2. **[Coroutines and Tasks (Python docs)](https://docs.python.org/3/library/asyncio-task.html)**
   — The most relevant subsection of the asyncio docs for this module. Covers coroutines,
   `asyncio.run()`, `create_task()`, `gather()`, and `sleep()` with authoritative examples.

3. **[FastAPI: Concurrency and async / await](https://fastapi.tiangolo.com/async/)**
   — FastAPI's explanation of async Python for web developers. Exceptionally well-written,
   with a clear "race car pit crew" analogy for the event loop. Recommended as a companion
   read to this module.

---

## Deeper Reading

4. **[PEP 492 — Coroutines with async and await syntax](https://peps.python.org/pep-0492/)**
   — The original proposal that introduced `async def` and `await` in Python 3.5. The
   "Motivation" and "Rationale" sections explain exactly why the old `yield from` approach
   was replaced.

5. **[Python Docs: asyncio — Developing with asyncio](https://docs.python.org/3/library/asyncio-dev.html)**
   — Official guidance on common debugging patterns, including how to detect when you have
   accidentally blocked the event loop with synchronous code.

6. **[Python Wiki: The GIL](https://wiki.python.org/moin/GlobalInterpreterLock)**
   — The Python wiki's explanation of the GIL, including its history, purpose, and the
   ongoing effort to make it optional in Python 3.13+.

---

## Video Resources

7. **[David Beazley: Python Concurrency From the Ground Up (PyCon 2015)](https://www.youtube.com/watch?v=MCs5OvhV9S4)**
   — A famous live-coded talk where Beazley builds an async scheduler from scratch. Gives
   deep intuition for how `yield` and event loops work together. ~45 minutes; highly
   recommended after completing Exercise 9 (the from-scratch scheduler exercise).

8. **[Raymond Hettinger: Keynote on Concurrency (PyBay 2017)](https://www.youtube.com/watch?v=9zinZmE3Ogk)**
   — Hettinger's clear comparison of threading, asyncio, and multiprocessing with worked
   examples. Good for reinforcing the "when to use which model" intuition from this module.
