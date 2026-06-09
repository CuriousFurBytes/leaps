# Module 01: Foundations of Distributed Systems

> This module introduces the mental models behind distributed systems: boundaries, latency, partial failure, coordination, and tradeoffs.

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
This module introduces the mental models behind distributed systems: boundaries, latency, partial failure, coordination, and tradeoffs. It focuses on practical engineering judgment: how to choose patterns, identify risk, and explain tradeoffs to other engineers.

The examples are intentionally small so the mechanics are visible. In production, the same ideas appear inside frameworks, brokers, platforms, incident reviews, and architecture documents.

## Prerequisites
- None; this is the entry point.
- Basic programming and command-line fluency.
- Comfort reading short `python`, `yaml`, and `json` examples.

## Objectives
By the end of this module, you will be able to:
- Explain the core architectural tradeoffs in this module.
- Implement or sketch a runnable example of the main mechanism.
- Debug one realistic failure mode related to the module.
- Justify a design choice using latency, reliability, ownership, and operability.

## Theory

### Why Distribution Changes Everything
A single-process program can often pretend that function calls are immediate, failures are local, and state has one obvious owner. Distributed systems remove those assumptions. A call across a network may be slow, duplicated, reordered, or lost, and the remote service may be healthy, overloaded, deploying, partitioned from its dependencies, or returning stale data.

Historically, distributed systems grew from time-sharing computers, early packet networks, client-server systems, and later web-scale services. Each era discovered the same lesson in a new form: adding machines increases capacity and organizational flexibility, but it also creates coordination cost.

```python
# Simulate why remote calls need explicit timeouts.
import random
import time

for attempt in range(3):
    simulated_latency = random.uniform(0.01, 0.20)
    time.sleep(simulated_latency)
    print(f"attempt={attempt} latency={simulated_latency:.3f}s")
```

### Boundaries, Ownership, and Coupling
A service boundary is not just a URL. It is a promise about ownership, data, deployment, failure handling, and change. Good boundaries reduce coordination between teams and isolate failures. Bad boundaries turn simple product changes into multi-team migrations.

```yaml
# A minimal service contract sketch.
service: payments
owns:
  - payment_attempts
  - refund_requests
exposes:
  - POST /payments
  - GET /payments/{id}
does_not_own:
  - shopping_carts
  - product_catalog
```

### Tradeoffs Instead of Universal Rules
Distributed architecture is mostly tradeoff management. Synchronous calls are simple but amplify tail latency. Queues smooth bursts but add delay and operational complexity. Replication improves availability but raises consistency questions.

```python
# A simple decision table encoded as data, not as dogma.
patterns = {
    "sync_call": "use when caller needs the answer now",
    "queue": "use when work can happen later and must survive bursts",
    "cache": "use when repeated reads tolerate controlled staleness",
}
for pattern, rule in patterns.items():
    print(pattern, "->", rule)
```


## Key Concepts
- **Partial failure:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.
- **Latency:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.
- **Service boundary:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.
- **Coupling:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.
- **Tradeoff:** A core idea for this module. Define it precisely, connect it to operational behavior, and practice recognizing it in real systems.

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
### Mistake: Treating a remote call like a local function call
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
