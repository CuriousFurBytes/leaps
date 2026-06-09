# Projects: Async Python

> Projects are the best way to cement async Python skills. They are ordered by difficulty
> from beginner to expert. Each project includes a clear goal, required modules, and
> acceptance criteria. Do not copy-paste solutions from the internet — the struggle is
> the learning.

---

## Beginner Projects

### Project 1: Async File Reader and Word Counter

**Difficulty:** Beginner
**Requires:** Module 01, Module 04
**Estimated Time:** 2–3 hours

**Goal:** Write a command-line tool that reads multiple text files concurrently using
`aiofiles`, counts word frequencies in each file, and prints a combined summary.

**Acceptance Criteria:**
- Reads 3+ files concurrently (not sequentially)
- Uses `asyncio.gather()` to parallelize file reads
- Counts word frequency and prints the top 10 words
- Handles the case where a file does not exist gracefully

**Stretch Goal:** Accept a directory path and process all `.txt` files in it.

---

### Project 2: Async URL Health Checker

**Difficulty:** Beginner
**Requires:** Module 01, Module 03, Module 04
**Estimated Time:** 3–4 hours

**Goal:** Build a tool that takes a list of URLs and checks whether each returns HTTP 200,
how long each takes to respond, and reports any that are slow or unreachable.

**Acceptance Criteria:**
- Checks all URLs concurrently using `aiohttp`
- Reports status code and response time for each URL
- Flags URLs that time out or return non-200 status
- Respects a configurable concurrency limit (e.g., max 10 requests at a time)
  using `asyncio.Semaphore`

**Stretch Goal:** Re-check failed URLs with exponential backoff retry.

---

## Intermediate Projects

### Project 3: Async News Aggregator

**Difficulty:** Intermediate
**Requires:** Modules 01–05
**Estimated Time:** 6–8 hours

**Goal:** Build an async program that fetches headlines from 3–5 public RSS/JSON news APIs
concurrently, deduplicates them by title, and writes the combined list to a file sorted by
publication date.

**Acceptance Criteria:**
- Fetches from at least 3 sources concurrently
- Deduplicates stories by normalized title
- Handles network errors on individual sources without failing the whole aggregation
- Writes output to a JSON file with timestamps
- Uses `asyncio.Lock` to protect shared data structures during concurrent writes

**Stretch Goal:** Run the aggregation on a schedule (every 15 minutes) without using
`time.sleep()`.

---

### Project 4: Async Rate-Limited API Client

**Difficulty:** Intermediate
**Requires:** Modules 03–05, Module 07
**Estimated Time:** 6–10 hours

**Goal:** Write an async client for a public API (e.g., GitHub API, a weather API) that
respects rate limits, retries on transient errors, and processes paginated results
concurrently across multiple resource types.

**Acceptance Criteria:**
- Implements a `RateLimiter` class using `asyncio.Semaphore`
- Handles HTTP 429 (Too Many Requests) with a proper delay
- Fetches multiple pages of results concurrently within rate limits
- Implements retry with exponential backoff for 5xx errors
- Has typed response models (dataclasses or Pydantic)

**Stretch Goal:** Add a circuit breaker that stops retrying after N consecutive failures.

---

## Advanced Projects

### Project 5: Async Job Queue System

**Difficulty:** Advanced
**Requires:** Modules 03–06, Module 08, Module 09
**Estimated Time:** 12–16 hours

**Goal:** Build a simple in-process async job queue with workers, priority levels, job
results, and error handling. Similar in spirit to Celery but entirely in-process using
asyncio primitives.

**Acceptance Criteria:**
- `JobQueue` class accepts submitted coroutine functions as jobs
- Configurable number of worker tasks consuming from the queue
- Jobs have priority levels (high/medium/low)
- Job results (success or exception) are stored and retrievable by job ID
- Workers handle exceptions in individual jobs without stopping
- Graceful shutdown: drains the queue before stopping workers
- Full test suite using pytest-asyncio

**Stretch Goal:** Add job timeouts using `asyncio.wait_for()`.

---

## Expert Projects

### Project 6: Async Data Ingestion Service

**Difficulty:** Expert
**Requires:** All modules (01–10)
**Estimated Time:** 20–30 hours

**Goal:** Build a production-grade async data ingestion service that: polls multiple external
APIs concurrently, validates and transforms incoming data, writes to a PostgreSQL database
using asyncpg, exposes a health check endpoint, and shuts down gracefully on SIGTERM.

**Acceptance Criteria:**
- At least 3 concurrent API pollers with configurable intervals
- Input validation with error logging (invalid records skipped, not crashed)
- Async writes to PostgreSQL using asyncpg connection pool
- `/health` endpoint that reports worker status and database connectivity
- Graceful shutdown: flushes pending writes and cancels pollers on SIGTERM
- Structured logging with per-request trace IDs
- Test suite covering: pollers (mocked HTTP), DB writer (mocked pool), and shutdown behavior

**Getting Unstuck:**
<details>
<summary>Hint: High-level architecture</summary>

Consider three layers:
1. **Pollers** — one coroutine per API, running in a loop, putting records into an
   `asyncio.Queue`
2. **Writers** — N worker coroutines consuming from the queue and batching inserts
3. **Coordinator** — a top-level `TaskGroup` that owns all pollers and writers, and handles
   cancellation on shutdown

The queue provides natural backpressure: if writers are slow, pollers will block on
`queue.put()`.
</details>

<details>
<summary>Hint: Graceful shutdown pattern</summary>

```python
import asyncio
import signal

async def main():
    loop = asyncio.get_running_loop()
    stop = asyncio.Event()

    def _on_sigterm():
        stop.set()

    loop.add_signal_handler(signal.SIGTERM, _on_sigterm)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(run_pollers(stop))
        tg.create_task(run_writers(stop))
        await stop.wait()
        # TaskGroup will wait for all tasks to finish before exiting
```
</details>
