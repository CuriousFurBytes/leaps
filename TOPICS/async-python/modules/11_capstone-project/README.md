# Module 11: Capstone — Async Data Pipeline

[← Module 10](../10_production-patterns/) | [Topic Home](../../README.md)

---

![Status](https://img.shields.io/badge/status-stub-orange)
![Difficulty](https://img.shields.io/badge/difficulty-Expert-red)
![Time](https://img.shields.io/badge/time-20h-orange)

> This is the **Capstone Project** for the Async Python topic. It is build-oriented:
> you will produce a working, tested, production-quality artifact. There is no lecture
> content here — only a project brief, milestones, and help sections.
>
> Do not look for a copy-paste solution. The struggle is the learning. Use the help
> sections if you get stuck, then push forward on your own.

---

## Table of Contents

1. [Project Brief](#project-brief)
2. [Milestones](#milestones)
3. [Acceptance Criteria](#acceptance-criteria)
4. [Architecture Guidance](#architecture-guidance)
5. [Help: Getting Unstuck](#help-getting-unstuck)
6. [What to Submit](#what-to-submit)
7. [Cross-Links](#cross-links)

---

## Project Brief

**Build an async high-performance data pipeline** that:

1. Fetches records from **at least 3 external data sources** concurrently (simulated
   or real public APIs)
2. Validates and transforms each record in a processing stage
3. Writes valid records to a **PostgreSQL database** using an async connection pool
4. Runs gracefully — handles SIGTERM by draining the pipeline before exiting
5. Has a health check that reports pipeline status
6. Has a complete test suite using `pytest-asyncio`

The pipeline should demonstrate that you can apply everything from Modules 01–10:
coroutines, tasks, async I/O, synchronization, structured concurrency, performance
patterns, async databases, testing, and production patterns.

---

## Milestones

Work through these milestones in order. Each one is independently testable.

### Milestone 1: Fetchers

Implement at least 3 async fetchers, each fetching from a different source.
Sources can be real public APIs or `asyncio.sleep()`-based simulations (specify in your
README which you used).

**Done when:** Running the fetchers concurrently via `TaskGroup` fetches records from all
three sources and prints a count of records received from each.

### Milestone 2: Processor

Implement a validation and transformation step. Each record should be:
- Validated against a schema (use Pydantic or manual validation)
- Transformed into a canonical internal format
- Invalid records logged and discarded (not crashed on)

**Done when:** Sending a mix of valid and invalid records through the processor produces
only valid, transformed records in the output queue and logs discarded records.

### Milestone 3: Database Writer

Implement an async writer that batch-inserts records into PostgreSQL using `asyncpg`.
The writer should:
- Consume from the processing output queue
- Batch records (e.g., 100 at a time or every 5 seconds, whichever comes first)
- Use a connection pool (not a single connection)

**Done when:** Valid records from Milestone 2 appear in the database after running the
pipeline for 30 seconds.

### Milestone 4: Graceful Shutdown

Add SIGTERM handling. On SIGTERM:
1. Stop fetchers from starting new requests
2. Allow the processing queue to drain
3. Flush the writer's current batch to the database
4. Close the connection pool
5. Exit cleanly (exit code 0)

**Done when:** Sending SIGTERM to the running pipeline results in all in-flight records
being saved before the process exits.

### Milestone 5: Health Check

Add a simple HTTP health endpoint (use `aiohttp.web` or Python's built-in
`http.server` in a thread) that returns JSON with:
- Pipeline status (running / draining / stopped)
- Records processed in the last 60 seconds
- Database pool status (available connections)

**Done when:** The endpoint returns valid JSON while the pipeline is running.

### Milestone 6: Test Suite

Write a pytest-asyncio test suite that covers:
- Each fetcher (mock HTTP responses)
- The processor (valid records pass, invalid records are discarded)
- The writer (mock database pool, verify batch inserts are called correctly)
- Graceful shutdown (send cancellation, verify cleanup runs)

**Done when:** `pytest` passes with 80%+ coverage on your pipeline code.

---

## Acceptance Criteria

A completed capstone meets all of the following:

- [ ] At least 3 concurrent fetchers running via `TaskGroup` or `asyncio.gather()`
- [ ] Records validated and transformed in a processor stage
- [ ] Records written to PostgreSQL using `asyncpg` with a connection pool
- [ ] Graceful shutdown on SIGTERM that drains the pipeline before exit
- [ ] Health check endpoint returning valid JSON
- [ ] pytest test suite covering fetchers, processor, writer, and shutdown
- [ ] A `README.md` in your project directory explaining how to run it

---

## Architecture Guidance

A minimal architecture that satisfies all milestones:

```
[Fetcher A] ──┐
[Fetcher B] ──┤──→ [raw_queue] ──→ [Processor] ──→ [processed_queue] ──→ [DB Writer]
[Fetcher C] ──┘
```

- Each fetcher is a long-running coroutine inside a `TaskGroup`
- Queues provide buffering and backpressure between stages
- The processor is one or more worker tasks consuming from `raw_queue`
- The DB writer batches from `processed_queue`
- A coordinator owns all `TaskGroup`s and handles shutdown signals

---

## Help: Getting Unstuck

Work through the milestones before reading these hints. Use them when you are genuinely
stuck, not as a shortcut.

<details>
<summary>Hint: Milestone 1 — Fetcher structure</summary>

Each fetcher should be an `async def` that runs in an infinite loop until a stop event
is set:

```python
async def fetcher(source_url: str, queue: asyncio.Queue, stop: asyncio.Event):
    async with aiohttp.ClientSession() as session:
        while not stop.is_set():
            try:
                async with session.get(source_url) as resp:
                    records = await resp.json()
                    for record in records:
                        await queue.put(record)
            except Exception as e:
                logging.error(f"Fetch error: {e}")
            await asyncio.sleep(5)  # poll interval
```

Run multiple fetchers with `TaskGroup`:

```python
async with asyncio.TaskGroup() as tg:
    for url in source_urls:
        tg.create_task(fetcher(url, raw_queue, stop_event))
```
</details>

<details>
<summary>Hint: Milestone 3 — Async batch writer</summary>

A time-or-count batch writer collects records and flushes when either N records
accumulate or T seconds have passed, whichever comes first:

```python
async def db_writer(queue: asyncio.Queue, pool: asyncpg.Pool):
    batch = []
    BATCH_SIZE = 100
    FLUSH_INTERVAL = 5.0

    async def flush():
        if batch:
            await pool.executemany("INSERT INTO records ...", batch)
            batch.clear()

    last_flush = asyncio.get_event_loop().time()

    while True:
        try:
            record = await asyncio.wait_for(queue.get(), timeout=1.0)
            batch.append(record)
            queue.task_done()
        except asyncio.TimeoutError:
            pass

        now = asyncio.get_event_loop().time()
        if len(batch) >= BATCH_SIZE or (now - last_flush) >= FLUSH_INTERVAL:
            await flush()
            last_flush = now
```
</details>

<details>
<summary>Hint: Milestone 4 — Graceful shutdown pattern</summary>

```python
import asyncio, signal

async def main():
    loop = asyncio.get_running_loop()
    stop = asyncio.Event()
    loop.add_signal_handler(signal.SIGTERM, stop.set)
    loop.add_signal_handler(signal.SIGINT, stop.set)

    raw_queue = asyncio.Queue(maxsize=1000)
    processed_queue = asyncio.Queue(maxsize=1000)
    pool = await asyncpg.create_pool(dsn=DATABASE_URL)

    async with asyncio.TaskGroup() as tg:
        # Start pipeline components
        for url in SOURCE_URLS:
            tg.create_task(fetcher(url, raw_queue, stop))
        tg.create_task(processor(raw_queue, processed_queue, stop))
        tg.create_task(db_writer(processed_queue, pool))

        # Wait for shutdown signal
        await stop.wait()
        # TaskGroup waits for all tasks to complete before exiting

    await pool.close()
    print("Pipeline shut down cleanly")

asyncio.run(main())
```
</details>

<details>
<summary>Hint: Milestone 6 — Testing the writer with mocks</summary>

```python
import pytest
from unittest.mock import AsyncMock, MagicMock
import asyncio

@pytest.mark.asyncio
async def test_db_writer_flushes_on_batch_size():
    queue = asyncio.Queue()
    mock_pool = MagicMock()
    mock_pool.executemany = AsyncMock()

    # Put exactly BATCH_SIZE records
    for i in range(100):
        await queue.put({"id": i, "value": f"record_{i}"})

    # Run writer for just long enough to flush
    writer_task = asyncio.create_task(db_writer(queue, mock_pool))
    await asyncio.sleep(0.1)
    writer_task.cancel()
    try:
        await writer_task
    except asyncio.CancelledError:
        pass

    # Verify the batch insert was called
    mock_pool.executemany.assert_called_once()
    args = mock_pool.executemany.call_args[0]
    assert len(args[1]) == 100  # 100 records in the batch
```
</details>

---

## What to Submit

Create a `solution/` directory inside this module directory containing:

```
solution/
├── README.md          (how to run and test the pipeline)
├── pipeline.py        (main pipeline code)
├── fetchers.py        (data source fetchers)
├── processor.py       (validation and transformation)
├── writer.py          (async database writer)
├── tests/
│   ├── test_fetchers.py
│   ├── test_processor.py
│   └── test_writer.py
├── requirements.txt
└── schema.sql         (database schema)
```

Your `README.md` should include:
- Setup instructions (how to start a local PostgreSQL instance)
- How to run the pipeline
- How to run the test suite
- A brief description of any design decisions you made

---

## Cross-Links

- [[async-python/modules/01_introduction]] — concurrency fundamentals used throughout
- [[async-python/modules/06_structured-concurrency]] — TaskGroup used for pipeline lifecycle
- [[async-python/modules/07_performance-patterns]] — rate limiting and backpressure
- [[async-python/modules/08_async-databases]] — asyncpg connection pool
- [[async-python/modules/09_testing-async]] — pytest-asyncio test suite
- [[async-python/modules/10_production-patterns]] — graceful shutdown and health checks
- [[postgresql]] — SQL schema and PostgreSQL-specific features
