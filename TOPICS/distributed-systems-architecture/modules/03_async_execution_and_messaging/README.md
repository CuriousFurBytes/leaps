# Module 03: Async Execution and Messaging

> This module explains event loops, futures, message brokers, and the difference between concurrency and distribution.

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
This module explains event loops, futures, message brokers, and the difference between concurrency and distribution. It focuses on practical engineering judgment: how to choose patterns, identify risk, and explain tradeoffs to other engineers.

The examples are intentionally small so the mechanics are visible. In production, the same ideas appear inside frameworks, brokers, platforms, incident reviews, and architecture documents.

## Prerequisites
- Modules 01 and 02.
- Basic programming and command-line fluency.
- Comfort reading short `python`, `yaml`, and `json` examples.

## Objectives
By the end of this module, you will be able to:
- Explain the core architectural tradeoffs in this module.
- Implement or sketch a runnable example of the main mechanism.
- Debug one realistic failure mode related to the module.
- Justify a design choice using latency, reliability, ownership, and operability.

## Theory

### Async Is About Waiting Efficiently
Asynchronous execution lets a program make progress while operations wait on I/O. It does not make slow work disappear; it changes how waiting is scheduled. Event loops became prominent in GUI systems, network servers, and later platforms such as Node.js and Python asyncio because many workloads wait more than they compute.

```python
# Runnable asyncio example: two waits overlap.
import asyncio

async def fetch(name, delay):
    await asyncio.sleep(delay)
    return f"{name} done"

async def main():
    results = await asyncio.gather(fetch("a", 0.1), fetch("b", 0.1))
    print(results)

asyncio.run(main())
```

### Messaging Decouples Time and Ownership
A message records intent or fact so another component can react later. Commands ask for work; events announce that something happened. This difference matters because commands usually target one handler, while events may interest many subscribers.

```json
{
  "type": "OrderPlaced",
  "event_id": "evt-123",
  "occurred_at": "2026-06-09T00:00:00Z",
  "order_id": "ord-456"
}
```

### Delivery Semantics Shape Consumer Design
Messaging systems force engineers to decide what happens on retries, duplicates, ordering gaps, and poison messages. Consumers should commit progress only after durable side effects are safe, and they should use idempotency keys when duplicate delivery is possible.

```python
# Idempotent consumer sketch.
processed = set()

def handle(message):
    if message["event_id"] in processed:
        return "duplicate ignored"
    processed.add(message["event_id"])
    return f"processed {message['order_id']}"

print(handle({"event_id": "1", "order_id": "A"}))
print(handle({"event_id": "1", "order_id": "A"}))
```


## Key Concepts
- **Event loop:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.
- **Future:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.
- **Command:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.
- **Event:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.
- **Idempotent consumer:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.

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
### Mistake: Assuming async code automatically improves throughput
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
