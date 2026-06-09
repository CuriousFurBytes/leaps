# Roadmap: Async Python

> This roadmap shows how the 11 modules are organized into learning phases and how this
> topic connects to the broader leaps knowledge graph.

---

## Learning Phases

```mermaid
flowchart TD
    subgraph P1["Phase 1: Foundations (Modules 01–02)"]
        M01["01: Introduction\nWhy async, GIL, concurrency models"]
        M02["02: Coroutines & Event Loop\nInternals, lifecycle, asyncio.run()"]
        M01 --> M02
    end

    subgraph P2["Phase 2: Core Patterns (Modules 03–05)"]
        M03["03: Tasks & Futures\ngather(), wait(), cancellation"]
        M04["04: Async I/O\naiohttp, aiofiles, async iterators"]
        M05["05: Synchronization\nLock, Event, Semaphore, Queue"]
        M02 --> M03
        M03 --> M04
        M04 --> M05
    end

    subgraph P3["Phase 3: Advanced Techniques (Modules 06–09)"]
        M06["06: Structured Concurrency\nTaskGroup, anyio, error propagation"]
        M07["07: Performance Patterns\nPools, rate limiting, circuit breakers"]
        M08["08: Async Databases\nSQLAlchemy async, asyncpg"]
        M09["09: Testing Async\npytest-asyncio, AsyncMock"]
        M05 --> M06
        M06 --> M07
        M06 --> M08
        M07 --> M09
        M08 --> M09
    end

    subgraph P4["Phase 4: Production & Capstone (Modules 10–11)"]
        M10["10: Production Patterns\nGraceful shutdown, observability"]
        M11["11: Capstone Project\nAsync data pipeline end-to-end"]
        M09 --> M10
        M10 --> M11
    end
```

_Four phases take you from first coroutine to a production-grade async data pipeline._

---

## Phase Descriptions

### Phase 1: Foundations

Build the mental model. Understand *why* async exists, how it differs from threading and
multiprocessing, and how the event loop and coroutines work at the language level. You will
write your first coroutines and run them, and understand the difference between a coroutine
object and a running task.

**Outcome:** You can explain the GIL, write a basic coroutine, and run it with `asyncio.run()`.

### Phase 2: Core Patterns

Learn the bread-and-butter patterns of daily async Python work: creating and managing multiple
tasks, doing real I/O with async HTTP and file clients, and preventing race conditions with
synchronization primitives.

**Outcome:** You can write async programs that fetch multiple URLs concurrently, read files
asynchronously, and safely share state between tasks.

### Phase 3: Advanced Techniques

Go deeper: structured concurrency for disciplined task lifecycle management, performance
patterns for production workloads, async database access, and comprehensive testing strategies
for async code.

**Outcome:** You can write production-quality async code with proper error handling,
cancellation support, database integration, and test coverage.

### Phase 4: Production and Capstone

Apply everything to real production concerns: graceful shutdown, health checks, worker pools,
distributed tracing. Then synthesize all of it into a complete capstone project — a
high-performance async data pipeline that fetches from multiple APIs, processes data
concurrently, and stores results to a database.

**Outcome:** You can design, build, test, and operate an async Python service in production.

---

## Prerequisites Map

```mermaid
flowchart LR
    PY["[[python]]\nBasic Python"]
    DJF["[[django-fastapi-flask]]\nWeb frameworks (recommended)"]
    PG["[[postgresql]]\nDatabase concepts (for Module 08)"]
    SA["[[systems-architecture]]\nDistributed systems (for Module 10)"]

    PY --> ASYNC["async-python"]
    DJF -.->|recommended| ASYNC
    PG -.->|Module 08| ASYNC
    SA -.->|Module 10| ASYNC
```

_Solid arrow = required; dashed arrow = recommended or relevant for specific modules._
