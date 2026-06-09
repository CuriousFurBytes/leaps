# Module 02: Queueing and Backpressure

> This module teaches queues as capacity tools, delay tools, and overload-control tools.

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
This module teaches queues as capacity tools, delay tools, and overload-control tools. It focuses on practical engineering judgment: how to choose patterns, identify risk, and explain tradeoffs to other engineers.

The examples are intentionally small so the mechanics are visible. In production, the same ideas appear inside frameworks, brokers, platforms, incident reviews, and architecture documents.

## Prerequisites
- Module 01: Foundations of Distributed Systems.
- Basic programming and command-line fluency.
- Comfort reading short `python`, `yaml`, and `json` examples.

## Objectives
By the end of this module, you will be able to:
- Explain the core architectural tradeoffs in this module.
- Implement or sketch a runnable example of the main mechanism.
- Debug one realistic failure mode related to the module.
- Justify a design choice using latency, reliability, ownership, and operability.

## Theory

### Queues as Shock Absorbers
A queue stores work until a consumer is ready. This lets producers and consumers run at different speeds for short periods. The danger is that queues can hide overload: if arrival rate stays above service rate, latency grows until users, disks, or memory fail.

Queueing theory emerged from early telephone traffic analysis. The same math applies to web requests, message brokers, background jobs, and task schedulers because all of them ask how arrivals, service time, and waiting interact.

```python
# Little's Law: L = lambda * W.
arrival_rate = 120      # jobs per second
wait_time = 0.5         # seconds in system
in_flight = arrival_rate * wait_time
print(f"Expected work in system: {in_flight} jobs")
```

### Backpressure and Load Shedding
Backpressure means the system tells producers to slow down before overload becomes collapse. Load shedding means rejecting some work intentionally to preserve the work that matters most. Both patterns are healthier than unbounded queues.

```python
# Bounded queue example using the standard library.
from queue import Queue, Full

queue = Queue(maxsize=2)
for item in ["a", "b", "c"]:
    try:
        queue.put_nowait(item)
        print("accepted", item)
    except Full:
        print("shed", item)
```

### Choosing Queue Semantics
Queue design involves delivery guarantees, ordering, retries, dead-letter handling, and idempotency. At-least-once delivery is common because it preserves work, but consumers must tolerate duplicates. Exactly-once claims usually depend on narrow assumptions and should be examined carefully.

```yaml
# Message handling policy sketch.
queue: invoice-jobs
max_retries: 5
dead_letter_queue: invoice-jobs-dlq
consumer_requirement: idempotent-by-invoice-id
ordering: per-customer
```


## Key Concepts
- **Little’s Law:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.
- **Arrival rate:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.
- **Service time:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.
- **Backpressure:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.
- **Dead-letter queue:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.

## Examples
### Scenario: Choosing the Right Interaction
Problem: a user action triggers work that may take longer than the user should wait.

```python
# If work is slow but retryable, acknowledge first and process later.
def submit_work(work_id, queue):
    queue.append({"work_id": work_id, "status": "queued"})
    return {"accepted": True, "work_id": work_id}

jobs = []
print(submit_work("job-1", jobs))
print(jobs)
```

This approach trades immediate completion for resilience and smoother capacity. The caller gets a quick acknowledgment, while workers process the job according to queue policy.

## Common Pitfalls
### Mistake: Using an unbounded queue as a substitute for capacity planning
Wrong approach:

```python
# Problem: this assumes every dependency is instant and always healthy.
def handle_request(remote_service):
    return remote_service.call_without_timeout()
```

Correct approach:

```python
# Better: make waiting, failure, and retry policy explicit.
def handle_request(remote_service, timeout_seconds=1.0):
    return remote_service.call(timeout=timeout_seconds)
```

This mistake happens because local tests hide network and load behavior. Avoid it by making limits, ownership, and failure handling part of the design from the start.

### Mistake: Optimizing for diagrams instead of operations
Wrong approach:

```yaml
services: many
reason: looks_modern
```

Correct approach:

```yaml
services: only_when_boundaries_are_clear
reason: independent_ownership_or_scaling_need
```

Architecture is successful when teams can build, operate, and evolve it safely.

### Mistake: Ignoring duplicate work
Wrong approach:

```python
def charge(order):
    return f"charged {order['id']}"
```

Correct approach:

```python
charged = set()

def charge(order):
    if order["id"] in charged:
        return "duplicate ignored"
    charged.add(order["id"])
    return f"charged {order['id']}"
```

Retries are normal, so side effects need idempotency or carefully controlled transactions.

## Cross-Links
- [[distributed-systems-architecture]]
- [[devops-platform-engineering]]
- [[postgresql]]
- [[devops-platform-engineering]]

## Summary
- Distributed architecture requires explicit reasoning about latency, failure, ownership, and operations.
- Small examples reveal mechanics that production platforms often hide.
- Queueing, async execution, service boundaries, and resilience patterns are connected choices.
- Correctness includes behavior under retries, overload, partial failure, and change.
- Engineering judgment means explaining tradeoffs, not memorizing pattern names.
