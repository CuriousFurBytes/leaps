# Test: Module 01 — Introduction to Async Python

**Instructions:** Answer all questions. Write your answers directly below each question.
Bonus questions are optional and can raise your score above 100%.

**Total Points:** 25 pts (Easy: 5×1 + Medium: 5×2 + Hard: 4×3 + Expert: 2×5)
**Bonus Available:** 5 pts

---

## Section 1: Easy Questions (1 pt each)

**Q1.** What keyword is used to define an asynchronous function in Python?

> Answer:

**Q2.** What does `asyncio.run(main())` do? Choose the best description:
- A) Creates a coroutine object called `main`
- B) Creates an event loop, runs `main()` to completion, then closes the loop
- C) Adds `main()` to an existing event loop as a background task
- D) Imports the asyncio module and executes `main()`

> Answer:

**Q3.** What is the GIL?

> Answer:

**Q4.** Name one category of workload where asyncio is highly effective, and one where it
is NOT effective.

> Answer:

**Q5.** When you call an `async def` function without `await`, what is returned?

> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Explain the difference between *concurrency* and *parallelism*. Give one real-world
example of each using Python.

> Answer:

**Q7.** Consider this code:

```python
import asyncio

async def fetch(url: str) -> str:
    await asyncio.sleep(1)
    return f"data from {url}"

async def main():
    r1 = await fetch("https://api.example.com/a")
    r2 = await fetch("https://api.example.com/b")
    r3 = await fetch("https://api.example.com/c")
    print(r1, r2, r3)

asyncio.run(main())
```

How long does this take? How would you rewrite `main()` to make it take approximately
1 second instead of 3 seconds?

> Answer:

**Q8.** Why does asyncio sidestep the GIL, while regular Python threading does not?

> Answer:

**Q9.** What happens when you call a blocking function like `time.sleep(2)` directly inside
an `async def` function? Why is this a problem, and what is the correct fix?

> Answer:

**Q10.** What is the difference between `asyncio.sleep(1)` and `time.sleep(1)` when called
inside an `async def` function?

> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** Write a complete, runnable async program that:
1. Defines a coroutine `ping(host: str, delay: float) -> str` that sleeps for `delay`
   seconds and returns `f"{host} responded in {delay}s"`
2. Runs `ping` on four hosts concurrently: `"a.com"` (1s), `"b.com"` (2s), `"c.com"` (0.5s),
   `"d.com"` (1.5s)
3. Prints all four results when done
4. Prints the total elapsed time (should be ~2 seconds, not 5)

> Answer:

**Q12.** The following code has a bug. Identify the bug, explain what effect it has at
runtime, and write the corrected version.

```python
import asyncio

async def load_config() -> dict:
    await asyncio.sleep(0.1)
    return {"debug": True, "workers": 4}

async def start_server():
    config = load_config()  # bug is here
    print(f"Starting server with config: {config}")

asyncio.run(start_server())
```

> Answer:

**Q13.** You are building a program that must:
- Fetch 1,000 product records from an external REST API
- Resize each product's thumbnail image (CPU-heavy: takes ~50ms per image)
- Save each resized image to disk

Describe the concurrency strategy you would use. What model would you use for each
step, and why? You do not need to write full code, but write the key function signatures
showing which steps are `async def` and which are synchronous.

> Answer:

**Q14.** Explain what "cooperative multitasking" means in the context of asyncio. What is
the contract between a coroutine and the event loop? What happens if a coroutine
violates that contract?

> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** Explain how asyncio's single-threaded concurrency model affects the types of race
conditions that can occur. Specifically:
- What race conditions from threading are impossible in asyncio?
- What race conditions are still possible in asyncio (and why)?
- Give a concrete code example of a race condition that CAN occur in async Python
  (hint: the race happens between `await` points, not within a single statement)

> Answer:

**Q16.** A colleague proposes using asyncio to speed up a machine learning training loop
that does heavy matrix multiplications on CPU. They argue: "asyncio makes our code run
concurrently, so it will use both CPU cores."

Write a detailed technical response explaining why this reasoning is flawed, what the
actual behavior would be, and what the colleague should use instead to benefit from
multiple CPU cores. Include discussion of the GIL, asyncio's threading model, and
at least one alternative approach with a code sketch.

> Answer:

---

## Bonus Question (5 pts)

**Bonus 1.** Before `async def` / `await` were added in Python 3.5, asyncio coroutines
were written using `@asyncio.coroutine` and `yield from`. Explain how this worked and
why the `async def` / `await` syntax was introduced to replace it. What problems with
the old approach did the new syntax solve? (+5 pts)

> Answer:
