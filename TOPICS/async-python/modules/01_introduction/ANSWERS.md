# Answers: Module 01 — Introduction to Async Python

## Answer Key

### Easy Questions (1 pt each)

**Q1:** `async` — specifically, the function is defined with `async def function_name(...)`

**Q2:** B — Creates an event loop, runs `main()` to completion, then closes the loop.

**Q3:** The Global Interpreter Lock — a mutex in CPython that allows only one thread to
execute Python bytecode at a time. It exists to protect CPython's reference-counting memory
management from concurrent corruption.

**Q4:** Effective: I/O-bound workloads (network requests, database queries, file reads)
where the bottleneck is waiting for external operations. NOT effective: CPU-bound workloads
(image processing, mathematical computation, ML inference) where the bottleneck is
computation speed.

**Q5:** A coroutine object — an object of type `coroutine` that represents the paused
function body. The logic inside the function has NOT run yet. It will only run when the
coroutine object is awaited or scheduled by the event loop.

---

### Medium Questions (2 pts each)

**Q6:** Concurrency is handling multiple tasks by interleaving their progress over time on
one processor — tasks take turns. Parallelism is executing multiple tasks at the exact same
moment on multiple processors simultaneously.

Python examples:
- Concurrency: `asyncio.gather()` runs multiple coroutines concurrently on one thread —
  each suspends at `await` points and lets the others run
- Parallelism: `multiprocessing.Pool()` creates multiple processes, each on a separate CPU
  core, computing at the same instant

**Q7:** This takes approximately 3 seconds. The three `fetch` calls are awaited sequentially:
`r1` must complete before `r2` starts. To run concurrently, use `asyncio.gather()`:

```python
async def main():
    r1, r2, r3 = await asyncio.gather(
        fetch("https://api.example.com/a"),
        fetch("https://api.example.com/b"),
        fetch("https://api.example.com/c"),
    )
    print(r1, r2, r3)
```

This takes approximately 1 second because all three requests are in-flight simultaneously.

**Q8:** Asyncio runs all coroutines on a single thread. There is only ever one thread to
lock, so the GIL is irrelevant — there is never any thread contention. The event loop switches
between coroutines cooperatively at `await` points, but this switching happens within a single
thread's execution, not across threads. The GIL only matters when multiple threads compete to
run Python bytecode simultaneously, which asyncio never does.

**Q9:** `time.sleep(2)` is a blocking system call. When it executes inside an `async def`
function, it blocks the entire thread (and thus the entire event loop) for 2 seconds. No
other coroutine can run during that time — they are all frozen. The correct fix is to use
`await asyncio.sleep(2)`, which suspends only the current coroutine and returns control to
the event loop so other coroutines can run. For truly unavoidable blocking calls (e.g., legacy
library functions), use `await asyncio.to_thread(blocking_function, args)`.

**Q10:** `time.sleep(1)` blocks the entire event loop thread for 1 second — no other
coroutine runs during this time. `asyncio.sleep(1)` suspends only the current coroutine and
gives control back to the event loop, which can run other coroutines during that 1 second.
Always use `asyncio.sleep()` inside async code.

---

### Hard Questions (3 pts each)

**Q11:** Complete solution:

```python
import asyncio
import time

async def ping(host: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{host} responded in {delay}s"

async def main():
    start = time.perf_counter()

    results = await asyncio.gather(
        ping("a.com", 1.0),
        ping("b.com", 2.0),
        ping("c.com", 0.5),
        ping("d.com", 1.5),
    )

    elapsed = time.perf_counter() - start
    for r in results:
        print(r)
    print(f"Total time: {elapsed:.2f}s")  # ~2.00s

asyncio.run(main())
```

**Q12:** The bug is `config = load_config()` — missing `await`. `load_config()` is an
`async def` function; calling it without `await` returns a coroutine object, not a dict.
The print statement will show `Starting server with config: <coroutine object load_config ...>`.
Python will also emit a `RuntimeWarning: coroutine 'load_config' was never awaited`.

Corrected version:
```python
async def start_server():
    config = await load_config()  # fixed: added await
    print(f"Starting server with config: {config}")
```

**Q13:** Three-step strategy:

```python
import asyncio
import concurrent.futures

# Step 1: Fetch records — I/O-bound → asyncio (async def)
async def fetch_product(session, product_id: int) -> dict:
    async with session.get(f"/api/products/{product_id}") as resp:
        return await resp.json()

# Step 2: Resize image — CPU-bound → run in ProcessPoolExecutor
def resize_image_sync(image_bytes: bytes) -> bytes:
    # PIL operations — runs in a subprocess worker
    ...

async def resize_image(image_bytes: bytes) -> bytes:
    # Offload CPU work to process pool, freeing the event loop
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        return await loop.run_in_executor(pool, resize_image_sync, image_bytes)

# Step 3: Save to disk — I/O-bound → asyncio with aiofiles
async def save_image(path: str, data: bytes) -> None:
    import aiofiles
    async with aiofiles.open(path, "wb") as f:
        await f.write(data)
```

Rationale: Fetching and saving are I/O-bound — async is ideal. Resizing is CPU-bound — it
would block the event loop if run directly, so it must be offloaded to a process pool.

**Q14:** Cooperative multitasking means coroutines voluntarily yield control to the scheduler
at defined points. The contract is: every coroutine must include `await` expressions at
reasonable intervals, allowing the event loop to run other coroutines.

If a coroutine violates this contract — e.g., runs a tight CPU loop or calls a blocking
function without `await` — it monopolizes the thread. All other coroutines are starved:
they cannot make progress until the violating coroutine finally reaches an `await` or
returns. In extreme cases, this can cause request timeouts, missed heartbeats, and
unresponsive services. There is no preemption mechanism to force a coroutine to yield.

---

### Expert Questions (5 pts each)

**Q15:** Race conditions in asyncio:

Impossible (from threading): Data corruption from simultaneous read-modify-write on
shared state is impossible because coroutines never run simultaneously. For example,
`counter += 1` is safe between `await` points because nothing else can run mid-statement.

Still possible: Any operation that spans multiple `await` points where shared state is
read and then written can have a race condition if another coroutine modifies the same
state between those awaits.

Example:

```python
import asyncio

balance = 100  # shared state

async def transfer(amount: int):
    global balance
    current = balance          # read
    await asyncio.sleep(0)     # <-- another coroutine can run HERE
    balance = current - amount  # write: current is now stale!

async def main():
    # Two coroutines both read balance=100, both subtract 50
    # Expected result: 0. Actual result: 50 (one write overwrites the other)
    await asyncio.gather(transfer(50), transfer(50))
    print(balance)  # may print 50, not 0!

asyncio.run(main())
```

The race window is between any `await` where state was read before and written after.
Solution: Use `asyncio.Lock` to protect the read-modify-write sequence.

**Q16:** The reasoning is flawed on multiple levels:

1. **asyncio does not use multiple cores.** All asyncio coroutines run on a single thread
   in a single process. On a 4-core CPU, asyncio still uses exactly 1 core.

2. **asyncio does not help CPU-bound work at all.** The event loop switches between
   coroutines at `await` points. A tight matrix multiplication loop has no `await` — it
   would run to completion without yielding, completely blocking all other coroutines.

3. **The GIL prevents Python threads from achieving true parallelism** for Python code.
   Even `ThreadPoolExecutor` with 4 threads won't parallelize Python computation.

Correct alternative: `multiprocessing.Pool` or `concurrent.futures.ProcessPoolExecutor`.
Each worker is a separate Python process with its own GIL and interpreter, enabling true
parallel CPU usage:

```python
import concurrent.futures
import numpy as np

def matrix_multiply(args):
    a, b = args
    return np.matmul(a, b)  # runs in a subprocess — real parallelism

with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
    # Each of the 4 workers runs on a separate CPU core
    results = list(pool.map(matrix_multiply, batch_of_pairs))
```

Asyncio could wrap this with `run_in_executor()` to integrate it with an async service,
but the actual computation would happen in processes, not coroutines.

---

### Bonus Question Answer

**Bonus 1:** The old pre-3.5 syntax used generator-based coroutines:

```python
# Python 3.4 style (deprecated, removed in 3.11)
@asyncio.coroutine
def old_fetch(url):
    response = yield from aiohttp.get(url)  # yield from suspends, like await
    return response

# Python 3.5+ style
async def new_fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response
```

`yield from` delegated to another generator, and asyncio built coroutines on top of
Python's generator protocol. This worked but had serious problems:

1. **Ambiguity:** A `yield from` could be a coroutine delegation or a generator delegation
   — the same syntax served two different purposes. Code was hard to read.
2. **No type safety:** A regular function decorated with `@asyncio.coroutine` looked like
   a coroutine but was actually a generator. Typos (forgetting the decorator) caused
   silent failures — the function ran synchronously without warning.
3. **Performance:** Every yield-from traversal had overhead proportional to the depth of
   delegation.

`async def` / `await` introduced dedicated syntax, making coroutines a distinct language
concept from generators. The interpreter enforces that `await` is only valid inside
`async def`, and calling an `async def` function always returns a coroutine object — never
runs immediately. This eliminated the ambiguity and made code intent clear.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
