# Module 03: Async I/O Streams and Clients

> Use async streams and client patterns to move bytes without blocking the event loop.

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Key Concepts](#key-concepts)
6. [Examples](#examples)
7. [Common Pitfalls](#common-pitfalls)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

## Overview
This module covers network streams, async context managers, backpressure, and practical clients. It emphasizes the mental model first, then applies that model in short runnable programs.

Async Python is easiest to learn when every suspension point is visible. Read each example by asking: which coroutine owns the work, where can it pause, and what other task could run while it is paused?

## Prerequisites
- Modules 01 and 02.
- Comfortable reading small Python functions and exceptions from [[python]].

## Objectives
By the end of this module, you will be able to:
- Explain the core async concepts introduced in this module.
- Implement small runnable examples using `asyncio`.
- Debug common mistakes by identifying blocking calls, missing awaits, or unsafe cleanup.
- Connect this module to later production patterns in [[async-python]].

## Theory
### Mental Model
Async I/O becomes concrete when a program waits for bytes. `asyncio` streams provide a high-level reader/writer interface over sockets, hiding low-level readiness notifications while preserving non-blocking behavior. The important habit is to await reads, writes, drains, and close operations instead of assuming data moves instantly.

### Mechanics
Backpressure is the system's way of saying downstream capacity is limited. If a writer produces faster than the network or peer can receive, `await writer.drain()` gives the loop a chance to pause the producer. Ignoring backpressure can turn temporary slowness into memory growth and outages.

### Professional Use
Async clients should own resources explicitly. An async context manager can open a connection on entry and close it on exit, even when an exception interrupts the request. This mirrors synchronous context managers but uses `async with` because setup and cleanup may themselves need I/O.


### Why This Matters
Streams and clients force you to think in terms of flow rather than isolated function calls. Bytes can arrive partially, remote peers can stop reading, and local buffers can grow if producers ignore downstream limits. In synchronous code, these problems still exist, but the operating system or thread pool may hide them until scale exposes the cost. In async code, the program structure makes the pressure visible: reads are awaited, writes are drained, and connection cleanup is part of the protocol. Experienced async Python developers design client code around these boundaries because most production incidents are not caused by a single failed request; they are caused by many slow or stuck requests accumulating without limits.

## Key Concepts
- **Coroutine:** A suspended computation created by calling an `async def` function. It does not run to completion until awaited or scheduled.
- **Event loop:** The coordinator that resumes ready coroutines and waits for I/O readiness or timers.
- **Task:** A scheduled coroutine with lifecycle state, cancellation behavior, and a result or exception.
- **Suspension point:** An `await` expression where control may return to the event loop.
- **Backpressure:** Feedback that tells producers to slow down because a consumer, socket, or queue is saturated.

## Examples
### Example 1: Tiny TCP echo client
```python
import asyncio

async def main():
    reader, writer = await asyncio.open_connection("example.com", 80)
    # Send a minimal HTTP request as bytes.
    writer.write(b"GET / HTTP/1.0\r\nHost: example.com\r\n\r\n")
    await writer.drain()
    data = await reader.read(80)
    print(data.decode("latin1", errors="replace"))
    writer.close()
    await writer.wait_closed()

asyncio.run(main())
```
This example is intentionally small so you can run it directly and observe the async behavior.

### Example 2: Async context manager client
```python
import asyncio

class TimerClient:
    async def __aenter__(self):
        # Real clients would open a connection here.
        self.started = asyncio.get_running_loop().time()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        # Real clients would close sockets or pools here.
        elapsed = asyncio.get_running_loop().time() - self.started
        print(f"client lived for {elapsed:.3f}s")

async def main():
    async with TimerClient():
        await asyncio.sleep(0.1)

asyncio.run(main())
```
This example is intentionally small so you can run it directly and observe the async behavior.

### Example 3: Bound concurrent clients
```python
import asyncio

async def request(i, limit):
    async with limit:
        # The semaphore prevents unlimited simultaneous requests.
        await asyncio.sleep(0.1)
        return f"response {i}"

async def main():
    limit = asyncio.Semaphore(3)
    results = await asyncio.gather(*(request(i, limit) for i in range(10)))
    print(results)

asyncio.run(main())
```
This example is intentionally small so you can run it directly and observe the async behavior.

## Common Pitfalls
### Pitfall 1: Writing without awaiting drain
Wrong approach:
```python
async def load():
    return "data"

value = load()
print(value)  # Prints a coroutine object, not "data".
```
Correct approach:
```python
import asyncio

async def load():
    return "data"

async def main():
    value = await load()
    print(value)

asyncio.run(main())
```
This mistake happens because `async def` looks like normal `def`, but calling it creates a coroutine object.

### Pitfall 2: Blocking the event loop
Wrong approach:
```python
import time

async def pause_badly():
    time.sleep(1)  # Blocks the whole event loop thread.
```
Correct approach:
```python
import asyncio

async def pause_cooperatively():
    await asyncio.sleep(1)  # Lets other tasks run while waiting.
```
Use async-friendly libraries or move unavoidable blocking calls to a thread.

### Pitfall 3: Losing task ownership
Wrong approach:
```python
import asyncio

async def main():
    asyncio.create_task(asyncio.sleep(10))  # No owner awaits or cancels it.
```
Correct approach:
```python
import asyncio

async def main():
    task = asyncio.create_task(asyncio.sleep(10))
    await task
```
Every task should have an owner that awaits it, cancels it, or supervises it in a structured scope.

## Cross-Links
- [[async-python]]
- [[python]]
- [[networking]]
- [[operating-systems]]

## Summary
- Async Python uses explicit suspension points to coordinate I/O-bound work.
- Coroutines are not threads; they run cooperatively on an event loop.
- Tasks give coroutines independent lifecycle state and must be owned.
- Cancellation, cleanup, and backpressure are design concerns, not afterthoughts.
- Small runnable examples are the best way to build intuition before production use.
