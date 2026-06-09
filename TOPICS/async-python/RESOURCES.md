# Resources: Async Python

> All resources listed here have been verified to exist. URLs are provided only where a stable,
> canonical URL is known. For books, check your preferred retailer.

---

## Official Documentation

1. **[asyncio — Asynchronous I/O (Python docs)](https://docs.python.org/3/library/asyncio.html)**
   — The official Python standard library documentation for asyncio. Authoritative and
   comprehensive; the API reference sections are essential reading once you understand the
   concepts from this topic's modules.

2. **[FastAPI Documentation](https://fastapi.tiangolo.com/)**
   — FastAPI's docs include excellent practical coverage of async Python in a web context.
   The "Concurrency and async / await" page is especially useful for Module 01.

3. **[aiohttp Documentation](https://docs.aiohttp.org/)**
   — Official docs for the aiohttp async HTTP client/server library, covering client usage,
   connection pooling, and timeouts in detail.

4. **[pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)**
   — Official docs for pytest-asyncio, covering fixture modes, event loop scoping, and
   integration with pytest.

---

## Books

5. **"Using asyncio in Python" by Caleb Hattingh (O'Reilly)**
   — [Verify URL before publishing: check O'Reilly catalog]
   — A focused, practical book on asyncio specifically. Covers the event loop, coroutines,
   tasks, and real-world patterns. Recommended for Modules 01–05.

6. **"Python Cookbook, 3rd Edition" by David Beazley and Brian K. Jones (O'Reilly)**
   — [Verify URL before publishing: check O'Reilly catalog]
   — Chapter 12 covers concurrency including asyncio patterns. Excellent for seeing how async
   fits into the broader Python ecosystem. The recipes format makes it useful as a reference.

7. **"Fluent Python, 2nd Edition" by Luciano Ramalho (O'Reilly)**
   — [Verify URL before publishing: check O'Reilly catalog]
   — Part V covers concurrency models including asyncio. Ramalho's explanations of coroutine
   internals (how they relate to generators) are among the clearest available in print.

---

## Articles and Deep Dives

8. **[Python Docs: Developing with asyncio](https://docs.python.org/3/library/asyncio-dev.html)**
   — Official guidance on debugging, common mistakes, and development best practices for
   asyncio applications.

9. **[PEP 492 — Coroutines with async and await syntax](https://peps.python.org/pep-0492/)**
   — The original Python Enhancement Proposal that introduced `async def` and `await`. Reading
   the motivation section gives deep insight into the design decisions.

10. **[PEP 654 — Exception Groups and except*](https://peps.python.org/pep-0654/)**
    — The PEP that introduced TaskGroup and exception groups. Essential reading before
    Module 06 (Structured Concurrency).

---

## Libraries and Tools

11. **[anyio](https://anyio.readthedocs.io/)** — A cross-runtime async compatibility library
    that works on asyncio, Trio, and Curio. Covered in Module 06. Useful for writing library
    code that is not tied to a specific event loop implementation.

12. **[aiofiles](https://github.com/Tinche/aiofiles)** — Async file I/O wrapper. Covered in
    Module 04. Simple API; wraps standard file operations to be non-blocking.

13. **[asyncpg](https://magicstack.github.io/asyncpg/)** — High-performance async PostgreSQL
    client. Covered in Module 08. Significantly faster than psycopg2 for async workloads.

14. **[SQLAlchemy async extension](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)**
    — Official SQLAlchemy docs for the async session API. Essential reading for Module 08.
