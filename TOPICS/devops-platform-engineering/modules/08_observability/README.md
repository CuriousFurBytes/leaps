# Module 08: Observability

[← Module 07: Infrastructure as Code](../07_infrastructure-as-code/) | [Topic Home](../../README.md) | [Next → Module 09: GitOps and Delivery](../09_gitops-and-delivery/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-orange)
![Time](https://img.shields.io/badge/time-10--14h-orange)

> You cannot improve what you cannot measure. This module covers Prometheus metrics, Grafana dashboards, OpenTelemetry distributed tracing, SLO/SLI/SLA definition and monitoring, and effective alerting strategies.

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

> [!NOTE]
> **This module is a stub.** Full content will be added in a future update.

Observability is the practice of understanding the internal state of a system from its external outputs. In production systems, this means being able to answer: "Why is this slow?", "What just changed?", "Is the SLO being met?", and "When did this start failing?" without needing SSH access to production servers. The three pillars of observability — metrics, logs, and traces — provide complementary views of system behavior.

---

## Prerequisites

- Module 04: Kubernetes Fundamentals — Prometheus typically runs in Kubernetes; this module deploys the observability stack there
- Module 05: Kubernetes Advanced — Prometheus Operator uses CRDs; ServiceMonitor and PrometheusRule are custom resources

---

## Objectives

By the end of this module, you will be able to:

1. Deploy and configure Prometheus to scrape metrics from applications and Kubernetes infrastructure
2. Write PromQL queries to compute rates, percentiles, ratios, and error budgets
3. Build Grafana dashboards that provide meaningful insight into system health and SLOs
4. Instrument applications with OpenTelemetry to emit metrics, logs, and traces
5. Configure distributed tracing (Jaeger or Tempo) to visualize request flows across microservices
6. Define SLIs and SLOs for a real service and configure alerting based on error budget burn rates
7. Design an alerting strategy that pages on symptoms, not causes, and minimizes alert fatigue

---

## Theory

> [!NOTE]
> Full theory content coming soon.

### The Three Pillars of Observability

```
Metrics          Logs             Traces
─────────        ──────────       ────────────────
Numerical        Text events      Request journeys
aggregations     per occurrence   across services
│                │                │
▼                ▼                ▼
"Error rate      "404 /api/v2/    Span: api-gateway
is 2.3%"         users at         → user-service
                 14:32:01"        → db (12ms)
```

**Metrics** tell you *what* is happening (rates, percentiles, counts). They are efficient to store and query but lose individual event detail.

**Logs** tell you *what happened* at a specific moment. They contain full event detail but are expensive to store at high volume.

**Traces** tell you *where* a request spent its time across multiple services. Essential for debugging latency in distributed systems.

### Prometheus Architecture

```bash
# Prometheus uses a pull model: it scrapes targets at regular intervals
# Targets expose metrics at /metrics in the Prometheus text format

# Example: a Go application exposing metrics
# GET /metrics returns:
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",path="/api/users",status="200"} 12453
http_requests_total{method="GET",path="/api/users",status="500"} 42

# Prometheus scrapes this every 15 seconds and stores time-series data
# The ServiceMonitor CRD tells Prometheus which services to scrape
```

```yaml
# ServiceMonitor: tells Prometheus Operator to scrape this service
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: my-app
  namespace: production
spec:
  selector:
    matchLabels:
      app: my-app
  endpoints:
  - port: metrics
    interval: 15s
    path: /metrics
```

### PromQL: Querying Prometheus

```promql
# Request rate over 5-minute window
rate(http_requests_total[5m])

# Error ratio (percentage of 5xx responses)
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
* 100

# 99th percentile latency using histogram
histogram_quantile(
  0.99,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
)

# SLO: fraction of requests meeting latency target (< 200ms)
sum(rate(http_request_duration_seconds_bucket{le="0.2"}[28d]))
/
sum(rate(http_request_duration_seconds_count[28d]))
```

### SLO / SLI Definition

```yaml
# SLO definition (can be stored as YAML for GitOps-managed SLOs)
# Using sloth (SLO generation tool) format
version: "prometheus/v1"
service: "payment-api"
labels:
  team: payments
  env: production

slos:
  - name: "availability"
    description: "99.9% of payment requests succeed"
    objective: 99.9                # 0.1% error budget = 43.8 minutes/month
    sli:
      events:
        error_query: |
          sum(rate(http_requests_total{job="payment-api",status=~"5.."}[{{.window}}]))
        total_query: |
          sum(rate(http_requests_total{job="payment-api"}[{{.window}}]))
    alerting:
      page_alert:
        labels:
          severity: critical
      ticket_alert:
        labels:
          severity: warning
```

### OpenTelemetry Instrumentation

```python
# Auto-instrumentation with OpenTelemetry Python SDK
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Configure tracer to export to OTel Collector
provider = TracerProvider()
provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4317"))
)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

# Create spans around operations
def process_payment(payment_id: str, amount: float) -> dict:
    with tracer.start_as_current_span("process_payment") as span:
        span.set_attribute("payment.id", payment_id)
        span.set_attribute("payment.amount", amount)

        # Child span for database call
        with tracer.start_as_current_span("db.charge_record"):
            result = db.insert_charge(payment_id, amount)
            span.set_attribute("db.rows_affected", result.rowcount)

        return {"status": "success", "id": payment_id}
```

---

## Key Concepts

**Prometheus Data Model** — metrics are time series identified by a metric name and a set of key-value labels. Labels enable powerful aggregation: query all services, or filter to a specific service and endpoint.

**Histogram vs. Summary** — both compute latency percentiles, but histograms allow aggregation across multiple instances (use `histogram_quantile`); summaries compute percentiles on the client and cannot be aggregated. Prefer histograms in Prometheus.

**Error Budget** — the complement of the SLO target. A 99.9% availability SLO has a 0.1% error budget — about 43 minutes per month. Tracking the burn rate (how fast you're consuming the error budget) enables proactive alerting before the SLO is violated.

**Multi-Window, Multi-Burn-Rate Alerting** — the Google SRE approach to SLO alerting. Alert on fast burn (consuming a lot of error budget quickly) on a short window, and on slow burn (steady degradation) on a longer window. This balances alert speed against false positives.

---

## Examples

> Full examples coming soon. Will include: deploying the kube-prometheus-stack, building a RED (Rate/Errors/Duration) dashboard in Grafana, implementing multi-window burn rate alerts, and correlating traces with logs in Grafana Loki.

---

## Common Pitfalls

> Full pitfalls section coming soon. Key pitfalls: alerting on causes (CPU high) instead of symptoms (error rate high), too many alerts creating fatigue, using `rate()` on a summary metric (wrong), not having runbooks linked from alerts, ignoring cardinality (too many label values causing memory exhaustion), and not testing that alerts actually fire.

---

## Cross-Links

- [[devops-platform-engineering/modules/05_kubernetes-advanced]] — Prometheus Operator uses CRDs; ServiceMonitor and PrometheusRule are custom resources from Module 05
- [[devops-platform-engineering/modules/09_gitops-and-delivery]] — SLO definitions and alerting rules can be managed via GitOps
- [[feature-flags-monitoring]] — feature flags and monitoring integrate in progressive delivery: metrics validate canary deployments automatically

---

## Summary

- Observability has three pillars: metrics (what is happening), logs (what happened), traces (where time was spent)
- Prometheus scrapes metrics at regular intervals; PromQL queries time-series data for rates, percentiles, and ratios
- SLIs measure service behavior; SLOs set targets; error budgets quantify acceptable unreliability
- Multi-window, multi-burn-rate alerting detects both fast and slow SLO violations with low false positive rates
- OpenTelemetry provides a vendor-neutral SDK for instrumenting applications with metrics, logs, and traces
- Grafana dashboards should show the RED method (Rate, Errors, Duration) as the primary health view
