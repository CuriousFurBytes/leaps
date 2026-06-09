# Projects: Module 01 — Introduction to Async Python

> Project ideas sized for the concepts covered in this module (async def, await,
> asyncio.run(), asyncio.gather(), concurrency model selection). All projects can be
> completed using only the standard library — no external dependencies required.

---

## Project 1: Async Countdown Clock

**Difficulty:** Beginner
**Estimated Time:** 1–2 hours
**Concepts:** `async def`, `await asyncio.sleep()`, `asyncio.gather()`, cooperative multitasking

**Goal:** Build a terminal program that runs multiple countdown timers simultaneously.
Each timer prints its name and remaining time every second. All timers run concurrently
on a single thread.

**Requirements:**
- Define `async def countdown(name: str, seconds: int)` that prints `"{name}: {n}s remaining"`
  every second and then prints `"{name}: done!"`
- Run at least 3 timers with different durations concurrently
- The program should finish when the longest timer completes

**Expected output (with timers of 3s, 5s, and 2s):**
```
alpha: 3s remaining
beta: 5s remaining
gamma: 2s remaining
alpha: 2s remaining
beta: 4s remaining
gamma: 1s remaining
gamma: done!
alpha: 1s remaining
beta: 3s remaining
...
```

---

## Project 2: Async Concurrency Benchmarker

**Difficulty:** Beginner–Intermediate
**Estimated Time:** 2–3 hours
**Concepts:** Concurrency model comparison, `asyncio.gather()`, `ThreadPoolExecutor`,
`ProcessPoolExecutor`, timing

**Goal:** Write a benchmarking program that tests the same workload using all three
Python concurrency models and prints a comparison table.

**Two workloads to implement:**
1. I/O-bound: sleep for 0.1 seconds × 50 operations
2. CPU-bound: compute `sum(i**2 for i in range(100_000))` × 8 operations

**For each workload, measure the time taken by:**
- Sequential execution
- `asyncio.gather()` (for I/O-bound)
- `ThreadPoolExecutor`
- `ProcessPoolExecutor`

**Print a comparison table** showing which approach is fastest for each workload type.

This project will concretely validate the theory from the module: async and threads win
for I/O; multiprocessing wins for CPU.

---

## Project 3: Simple Async Task Runner CLI

**Difficulty:** Intermediate
**Estimated Time:** 3–4 hours
**Concepts:** `asyncio.create_task()`, `asyncio.gather()`, error handling, task naming

**Goal:** Build a command-line tool that reads a list of "jobs" from a YAML or JSON
file, runs them as concurrent async tasks, and prints a status report when done.

Each "job" in the file describes a shell command to run as a subprocess.

**Requirements:**
- Parse a jobs file with this structure:
  ```json
  [
    {"name": "lint", "command": "python -m flake8 src/"},
    {"name": "test", "command": "python -m pytest tests/"},
    {"name": "type-check", "command": "python -m mypy src/"}
  ]
  ```
- Run each job using `asyncio.create_subprocess_exec()` (Python standard library)
- Run all jobs concurrently
- Print a summary: which jobs passed, which failed, and the total elapsed time
- If a job fails, do not cancel the others

**Why this is interesting:** `asyncio.create_subprocess_exec()` is the async-native way
to run subprocesses — it does not block the event loop while the subprocess runs. This
is a real-world use case for asyncio that does not require any third-party libraries.
