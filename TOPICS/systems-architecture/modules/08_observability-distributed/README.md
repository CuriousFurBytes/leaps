# Module 08: Observability in Distributed Systems

[← Module 07: API Design for Services](../07_api-design-for-services/README.md) | [Topic Home](../../README.md) | [Next → Module 09: Resilience and Chaos Engineering](../09_resilience-and-chaos/README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-blue)
![Time](https://img.shields.io/badge/time-8h-orange)

> Distributed tracing with OpenTelemetry and Jaeger, correlation IDs, structured logging, metrics aggregation across services — the practices that make debugging a distributed system survivable.

---

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

---

## Overview

When a single-machine application has a bug, you read the stack trace. When a distributed system has a bug, you ask: which of the 47 services involved in this request produced the error? Which service was slow? Was the database slow, or was the application slow? Did the failure originate in Service A or was Service A just propagating a failure from Service B?

Without observability, these questions are answered by guessing, SSH-ing to individual hosts, and grepping logs manually — a process that takes hours and often finds the wrong answer. With good observability, these questions are answered in minutes by a single correlation ID search.

This module covers the three pillars of observability — metrics, logs, and traces — and how to implement them coherently in a distributed system. The focus is on **distributed tracing** (the pillar that is unique to distributed systems) using **OpenTelemetry** (the emerging standard) and **Jaeger** (a popular open-source trace backend). Correlation IDs, structured logging schemas, and metrics aggregation patterns complete the module.

---

## Prerequisites

- Module 04: Microservices Fundamentals — the service topology being observed
- Module 05: Microservices Patterns — circuit breaker and other patterns that need observability
- Basic Python; familiarity with HTTP headers

---

## Objectives

By the end of this module, you will be able to:

1. Explain the three pillars of observability (metrics, logs, traces) and what each is good for
2. Instrument a Python service with OpenTelemetry to generate distributed traces
3. Implement correlation ID propagation across multiple services via HTTP headers
4. Design a structured log schema with the fields required for effective distributed debugging
5. Describe how Jaeger ingests and visualizes traces and how to query for specific traces
6. Build a debugging runbook for diagnosing a slow request in a 3-service chain using only your observability setup

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be written in a subsequent pass.

### Core Concepts to Cover

**The Three Pillars of Observability:**

| Pillar | Question Answered | Granularity | Storage |
|--------|------------------|------------|---------|
| Metrics | "Is anything broken right now?" | Aggregate (counters, gauges, histograms) | Time-series DB (Prometheus, InfluxDB) |
| Logs | "What happened in detail?" | Per-event (discrete records with context) | Log aggregator (Elasticsearch, Loki) |
| Traces | "Where did this specific request spend its time?" | Per-request, cross-service | Trace backend (Jaeger, Zipkin, Tempo) |

**Distributed Tracing Concepts:**
- **Trace:** A tree of spans representing a single request's journey through multiple services
- **Span:** A unit of work within a trace — one database query, one service call, one message processing
- **TraceID:** A unique identifier for the entire request, propagated in HTTP headers across all services
- **SpanID:** Unique identifier for one span
- **Parent SpanID:** Links a child span to its parent, creating the trace tree

```python
# OpenTelemetry instrumentation in Python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup — typically done once at application startup
provider = TracerProvider()
provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://jaeger:4317"))
)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("order-service")

def process_order(order_id: str) -> dict:
    with tracer.start_as_current_span("process-order") as span:
        # Add attributes to the span for debugging
        span.set_attribute("order.id", order_id)
        span.set_attribute("service.name", "order-service")
        
        # Child span for database query
        with tracer.start_as_current_span("db-query"):
            order = db.get_order(order_id)
        
        # Child span for downstream call (trace propagates automatically via OTel)
        with tracer.start_as_current_span("payment-service-call"):
            payment = payment_client.charge(order)
        
        span.set_attribute("order.status", "completed")
        return {"order": order, "payment": payment}
```

**Correlation IDs:**
A simpler alternative to (or complement of) full distributed tracing. A unique ID generated at the entry point (API gateway or first service) and propagated in HTTP headers across all services. Every log line includes the correlation ID, enabling log aggregation across services for a single request.

```python
import uuid
from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    """Propagate or generate a correlation ID for every request."""
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    
    # Make correlation ID available to all code in this request context
    request.state.correlation_id = correlation_id
    
    response = await call_next(request)
    
    # Echo back the correlation ID so clients can reference it
    response.headers["X-Correlation-ID"] = correlation_id
    return response
```

**Structured Logging:**
Instead of free-text log lines, emit JSON objects with consistent fields. This enables log aggregation, filtering, and correlation across services.

```python
import structlog
import logging

# Configure structlog for JSON output
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)

log = structlog.get_logger()

def process_order(order_id: str, correlation_id: str) -> None:
    log.info(
        "order_processing_started",
        order_id=order_id,
        correlation_id=correlation_id,  # KEY: enables cross-service log correlation
        service="order-service",
        environment="production"
    )
    # Output: {"event": "order_processing_started", "order_id": "abc123",
    #          "correlation_id": "req-xyz", "timestamp": "2026-06-09T10:00:00Z",
    #          "level": "info", "service": "order-service"}
```

---

## Key Concepts

**Observability:** The ability to infer internal system state from external outputs (logs, metrics, traces). A system is observable if you can ask "why is this happening?" and answer it from telemetry data alone.

**Distributed trace:** A record of a request's complete path through multiple services, composed of spans. Enables latency breakdown and error attribution.

**TraceID / Correlation ID:** A unique identifier that spans all services involved in a single request. The glue that ties together logs, metrics, and spans from different services.

**Span:** The fundamental unit of a trace — one named unit of work with a start time, duration, and metadata (attributes, events, status).

**OpenTelemetry (OTel):** The CNCF standard for telemetry instrumentation and data collection. Provides SDKs in all major languages for generating traces, metrics, and logs in a vendor-neutral format.

**Jaeger:** An open-source distributed tracing backend that ingests OTel traces, stores them, and provides a UI for querying and visualizing trace trees.

**Structured logging:** Emitting log records as structured data (JSON) with consistent fields rather than free-text strings. Enables programmatic aggregation and filtering.

**RED metrics:** Rate (requests per second), Errors (error rate), Duration (latency percentiles) — the three metrics that should be tracked for every service endpoint.

---

## Examples

> Full worked examples to be written. Planned examples:
> 1. Full OTel setup for a 3-service Python system with Jaeger backend (Docker Compose)
> 2. Correlation ID propagation: middleware → service → downstream service
> 3. Structured log schema with all required fields and a Kibana/Loki query example
> 4. Debugging runbook: "trace a slow request end-to-end using Jaeger"

---

## Common Pitfalls

**Pitfall 1: Logging without correlation IDs.**
Log lines without a correlation ID cannot be grouped by request. A 503 error log from Service C and the corresponding timeout log from Service A look completely unrelated — you must search by time range and hope you find the right entries. Always propagate correlation IDs.

**Pitfall 2: Using unstructured logs in a distributed system.**
`print(f"Processing order {order_id} for user {user_id}")` cannot be reliably parsed by a log aggregation system. JSON structured logs with consistent field names are the requirement for any system with more than one service.

**Pitfall 3: Sampling traces at the wrong level.**
In high-throughput systems, tracing 100% of requests is too expensive. Sampling at 1% means most errors are never traced. Use head-based sampling (decide at ingress) or tail-based sampling (decide after the request completes, keeping traces that had errors or high latency).

---

## Cross-Links

- [[systems-architecture/modules/05_microservices-patterns]] — Circuit breaker state changes must emit metrics; resilience patterns need observability to be operational
- [[systems-architecture/modules/09_resilience-and-chaos]] — Chaos experiments are validated by observability — you need tracing and metrics to confirm your resilience patterns work
- [[devops-platform-engineering]] — Prometheus, Grafana, and log aggregation stacks are deployed and operated as platform infrastructure
- [[feature-flags-monitoring]] — Monitoring and alerting are the operational side of the observability discipline

---

## Summary

- Observability has three pillars: metrics (aggregate health), logs (discrete events), traces (request path). Each answers different questions.
- Distributed traces show a request's complete path across services; TraceID ties all spans together.
- OpenTelemetry is the standard for instrumenting services; Jaeger, Zipkin, and Tempo are common backends.
- Correlation IDs are a lighter-weight alternative to full tracing — propagate in HTTP headers; include in every log line.
- Structured logging (JSON with consistent fields) is required for effective log aggregation across services.
- RED metrics (Rate, Errors, Duration) should be tracked for every service endpoint.
- Sampling strategy matters: 100% sampling is expensive; tail-based sampling (keep errors and slow requests) is the best compromise.
