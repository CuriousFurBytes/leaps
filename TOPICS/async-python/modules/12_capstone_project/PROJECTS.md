# Projects: Module 12 — Capstone Project

## Project 1: Async Observation Notebook
Build a small script that demonstrates one concept from this module and records expected output, actual output, and a short explanation.

## Project 2: Failure Drill
Introduce one realistic failure, such as timeout or cancellation, and document how your code responds.

## Project 3: Production Note
Write a short engineering note explaining how this module changes the way you would design a real async service.


## Capstone Project Brief
Build an asynchronous endpoint monitor that checks multiple targets, limits concurrency, records recent outcomes, exposes a report, and shuts down cleanly.

## Help / Getting Unstuck
Use these hints progressively; do not reveal more than you need.

### Checkpoint 1
Start with data models and one fake checker before adding real network I/O.

### Checkpoint 2
Add bounded concurrency with a semaphore or queue before adding retries.

### Checkpoint 3
Test cancellation by stopping the service while work is in progress.

### Acceptance Criteria
- The program starts and stops cleanly.
- Concurrency is bounded.
- Every outbound operation has a timeout.
- Failures are visible in results rather than hidden.
- Tests cover success, timeout, and cancellation.
