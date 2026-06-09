# Module 12: Capstone Project

> This capstone asks you to design and build a production-shaped async microservice system with queues, observability, and resilience.

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
This capstone asks you to design and build a production-shaped async microservice system with queues, observability, and resilience. It focuses on practical engineering judgment: how to choose patterns, identify risk, and explain tradeoffs to other engineers.

The examples are intentionally small so the mechanics are visible. In production, the same ideas appear inside frameworks, brokers, platforms, incident reviews, and architecture documents.

## Prerequisites
- All prior modules in this topic.
- Basic programming and command-line fluency.
- Comfort reading short `python`, `yaml`, and `json` examples.

## Objectives
By the end of this module, you will be able to:
- Explain the core architectural tradeoffs in this module.
- Implement or sketch a runnable example of the main mechanism.
- Debug one realistic failure mode related to the module.
- Justify a design choice using latency, reliability, ownership, and operability.

## Theory

### Project Brief
Build an order-processing platform that accepts orders, validates them, enqueues fulfillment work, processes payment-like side effects, emits status events, and exposes operational insight. The goal is not a polished commercial product; the goal is a system whose architecture can be defended under load, failure, and change.

```yaml
# Suggested system shape.
services:
  - api-gateway
  - order-service
  - fulfillment-worker
  - notification-worker
queues:
  - fulfillment-jobs
  - notification-events
observability:
  - structured-logs
  - request-correlation-ids
  - latency-and-queue-depth-metrics
```

### Required Engineering Evidence
Your final artifact must include runnable code or a detailed executable prototype, architecture notes, failure-mode analysis, and a short operations guide. Demonstrate backpressure, idempotent message handling, retries, and at least one intentional failure drill.

```python
# Minimal acceptance-check sketch for idempotency.
seen = set()

def accept(order_id):
    if order_id in seen:
        return "already accepted"
    seen.add(order_id)
    return "accepted"

assert accept("ord-1") == "accepted"
assert accept("ord-1") == "already accepted"
```

### Getting Unstuck Without Spoiling the Build
Use staged help. First draw service boundaries and data ownership. Next add queue contracts and retry rules. Then add observability and failure drills. Do not copy a complete solution; the learning value comes from making and justifying design decisions.

```text
Checkpoint order:
1. Define service responsibilities.
2. Define messages and idempotency keys.
3. Implement a thin happy path.
4. Add bounded queues and retry behavior.
5. Prove behavior with tests, logs, and metrics.
```


## Key Concepts
- **Architecture brief:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.
- **Acceptance criteria:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.
- **Failure drill:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.
- **Operational readiness:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.
- **Design review:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.

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
### Mistake: Building features before defining system boundaries and failure modes
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
