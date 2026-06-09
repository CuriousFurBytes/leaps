# Feature Flags, System Monitoring, and Developer Experience — Cheat Sheet

> [!TIP]
> This cheat sheet is a reference for **after you've learned the material** — not a shortcut
> to avoid learning it. If you're looking something up here before truly understanding it,
> go back to the relevant module first. A cheat sheet only helps people who already know
> what they're looking for.

---

## Quick Navigation

- [PromQL Quick Reference](#promql-quick-reference)
- [OpenTelemetry SDK Setup Patterns](#opentelemetry-sdk-setup-patterns)
- [Prometheus Metric Types](#prometheus-metric-types)
- [SLO / Error Budget Formulas](#slo--error-budget-formulas)
- [Feature Flag Patterns](#feature-flag-patterns)
- [Sentry SDK Quick Setup](#sentry-sdk-quick-setup)
- [PostHog SDK Quick Setup](#posthog-sdk-quick-setup)
- [Decision Guide: Which Tool?](#decision-guide-which-tool)
- [Gotchas and Pitfalls](#gotchas-and-pitfalls)
- [DORA Metrics Reference](#dora-metrics-reference)

---

## PromQL Quick Reference

_The most commonly used PromQL operators and functions._

### Instant Vector Selectors

```promql
# Select all time series for a metric
http_requests_total

# Filter by label (equality)
http_requests_total{status="200", job="api"}

# Filter by label (regex match)
http_requests_total{status=~"2.."}

# Filter by label (not equal)
http_requests_total{status!="500"}

# Filter by label (regex not match)
http_requests_total{status!~"5.."}
```

### Rate and Increase Functions

```promql
# Per-second rate over a 5-minute window (use for counters)
rate(http_requests_total[5m])

# Total increase over a 1-hour window
increase(http_requests_total[1h])

# Derivative for gauges (not counters)
deriv(memory_usage_bytes[5m])
```

### Aggregation Operators

```promql
# Sum across all label dimensions
sum(rate(http_requests_total[5m]))

# Sum grouped by a label
sum by (status) (rate(http_requests_total[5m]))

# Sum grouped by all labels except some
sum without (instance) (rate(http_requests_total[5m]))

# Average
avg(memory_usage_bytes)

# Maximum
max(memory_usage_bytes)

# Count the number of time series
count(http_requests_total)
```

### Histogram Functions

```promql
# Calculate p99 latency from a histogram
histogram_quantile(0.99, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))

# Calculate p50 latency
histogram_quantile(0.50, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))

# Average latency from histogram
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])
```

### SLO-Specific Queries

```promql
# Error rate (fraction of requests returning 5xx)
sum(rate(http_requests_total{status=~"5.."}[5m]))
  /
sum(rate(http_requests_total[5m]))

# Availability SLI (fraction of successful requests)
sum(rate(http_requests_total{status!~"5.."}[5m]))
  /
sum(rate(http_requests_total[5m]))

# Burn rate over 1 hour (how fast error budget is being consumed)
# Assumes 99.9% SLO (error rate budget = 0.001)
(
  sum(rate(http_requests_total{status=~"5.."}[1h]))
  /
  sum(rate(http_requests_total[1h]))
) / 0.001
```

---

## OpenTelemetry SDK Setup Patterns

### Python: Basic Tracing Setup

```python
# pip install opentelemetry-sdk opentelemetry-exporter-otlp

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# Configure the tracer provider with service metadata
resource = Resource.create({"service.name": "my-service", "service.version": "1.0.0"})
provider = TracerProvider(resource=resource)

# Configure OTLP exporter (sends to OTel Collector or Jaeger)
exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
provider.add_span_processor(BatchSpanProcessor(exporter))

# Set the global tracer provider
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# Create spans in your code
with tracer.start_as_current_span("operation-name") as span:
    span.set_attribute("user.id", "123")    # Add custom attributes
    span.set_attribute("http.method", "GET")
    # ... do work here
```

### Python: Auto-Instrumentation for Flask

```python
# pip install opentelemetry-instrumentation-flask

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from flask import Flask

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)  # Automatically traces all Flask routes
```

### JavaScript/Node: Basic Tracing Setup

```javascript
// npm install @opentelemetry/sdk-node @opentelemetry/exporter-trace-otlp-http

const { NodeSDK } = require('@opentelemetry/sdk-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');
const { Resource } = require('@opentelemetry/resources');
const { SemanticResourceAttributes } = require('@opentelemetry/semantic-conventions');

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'my-node-service',
  }),
  traceExporter: new OTLPTraceExporter({
    url: 'http://localhost:4318/v1/traces',
  }),
});

sdk.start();  // Must call before importing other modules
```

---

## Prometheus Metric Types

| Type | Use Case | Example |
|------|----------|---------|
| **Counter** | Monotonically increasing value (never decreases) | `http_requests_total`, `errors_total` |
| **Gauge** | Value that can go up and down | `memory_usage_bytes`, `active_connections` |
| **Histogram** | Distribution of observations; calculates percentiles | `http_request_duration_seconds` |
| **Summary** | Pre-calculated quantiles client-side | `rpc_duration_seconds` (use histogram instead in most cases) |

### Python: Defining and Using Each Type

```python
from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Counter — use .inc() or .inc(amount)
REQUESTS = Counter('http_requests_total', 'Total HTTP requests',
                   ['method', 'endpoint', 'status'])
REQUESTS.labels(method='GET', endpoint='/api/users', status='200').inc()

# Gauge — use .set(), .inc(), .dec()
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Number of active connections')
ACTIVE_CONNECTIONS.set(42)
ACTIVE_CONNECTIONS.inc()
ACTIVE_CONNECTIONS.dec()

# Histogram — use .observe(value)
REQUEST_LATENCY = Histogram('http_request_duration_seconds',
                            'HTTP request latency',
                            ['endpoint'],
                            buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0])
REQUEST_LATENCY.labels(endpoint='/api/users').observe(0.042)

# Start the metrics server (exposes /metrics endpoint)
start_http_server(8000)
```

---

## SLO / Error Budget Formulas

| Formula | Description |
|---------|-------------|
| `Error Budget = 1 - SLO Target` | Monthly error budget as a fraction |
| `Error Budget (minutes) = (1 - SLO%) × 30 days × 24h × 60min` | Monthly error budget in minutes |
| `Burn Rate = Actual Error Rate / Error Budget Rate` | How fast the budget is being consumed (1.0 = exactly on pace) |
| `Time to Exhaustion = Error Budget Remaining / Burn Rate` | When the budget will run out at current pace |

### Error Budget Examples

| SLO Target | Monthly Error Budget (minutes) | Weekly Error Budget (minutes) |
|-----------|-------------------------------|------------------------------|
| 99.9% | 43.2 min | 10.1 min |
| 99.5% | 216 min (3.6 hr) | 50.4 min |
| 99.0% | 432 min (7.2 hr) | 100.8 min |
| 99.95% | 21.6 min | 5.0 min |

---

## Feature Flag Patterns

### PostHog Python: Basic Flag Check

```python
import posthog

posthog.api_key = 'your-api-key'
posthog.host = 'https://app.posthog.com'  # or your self-hosted URL

# Boolean flag
if posthog.feature_enabled('new-checkout-flow', 'user-123'):
    show_new_checkout()
else:
    show_old_checkout()

# Multivariate flag (returns string variant or None)
variant = posthog.get_feature_flag('checkout-experiment', 'user-123')
if variant == 'variant-a':
    show_variant_a()
elif variant == 'variant-b':
    show_variant_b()
else:
    show_control()
```

### Homegrown Kill Switch (Simple Pattern)

```python
import os
import json
from functools import wraps

# Read flags from environment variable or file
def get_flags():
    flags_json = os.getenv('FEATURE_FLAGS', '{}')
    return json.loads(flags_json)

def feature_flag(flag_name, default=False):
    """Decorator that wraps a function with a feature flag check."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if get_flags().get(flag_name, default):
                return func(*args, **kwargs)
            # Return None or a fallback when flag is off
        return wrapper
    return decorator

# Usage: FEATURE_FLAGS='{"new_algo": true}' python app.py
@feature_flag('new_algo')
def run_new_algorithm(data):
    return process_with_new_algo(data)
```

---

## Sentry SDK Quick Setup

```python
# pip install sentry-sdk

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://your-dsn@o123456.ingest.sentry.io/7890",
    integrations=[FlaskIntegration()],  # Auto-capture Flask errors
    traces_sample_rate=0.1,             # 10% of transactions for performance
    environment="production",
    release="my-app@1.2.3",            # Link errors to releases
)

# Manual error capture
try:
    risky_operation()
except ValueError as e:
    sentry_sdk.capture_exception(e)

# Add context to errors
with sentry_sdk.push_scope() as scope:
    scope.set_tag("payment.provider", "stripe")
    scope.set_user({"id": "user-123", "email": "user@example.com"})
    sentry_sdk.capture_message("Payment failed", level="error")
```

---

## PostHog SDK Quick Setup

```python
# pip install posthog

import posthog

posthog.api_key = 'phc_your_api_key'
posthog.host = 'https://app.posthog.com'

# Track an event
posthog.capture(
    distinct_id='user-123',
    event='checkout_completed',
    properties={
        'order_value': 49.99,
        'items_count': 3,
        'payment_method': 'card',
    }
)

# Identify a user (set person properties)
posthog.identify(
    distinct_id='user-123',
    properties={
        'email': 'user@example.com',
        'plan': 'pro',
        'created_at': '2025-01-15',
    }
)

# Feature flag check with automatic event tracking
if posthog.feature_enabled('new-dashboard', 'user-123'):
    render_new_dashboard()
```

---

## Decision Guide: Which Tool?

```
What are you trying to answer?
│
├── "Is my service up and how is it performing?"
│     └── Prometheus + Grafana (metrics + SLO dashboard)
│
├── "Why did this error happen and who was affected?"
│     └── Sentry (error tracking + context)
│
├── "Where in my distributed system is the slowness?"
│     └── OpenTelemetry + Jaeger/Tempo (distributed traces)
│
├── "Are users completing the checkout flow?"
│     └── PostHog (product analytics + funnels)
│
├── "Is this new feature working as expected in production?"
│     └── PostHog feature flags + PostHog analytics, or LaunchDarkly + DataDog
│
├── "Full APM for a team that wants one platform?"
│     └── DataDog (metrics + traces + logs + SLOs in one place)
│
└── "How fast is my team shipping and how stable is production?"
      └── DORA metrics dashboard (deploy frequency + lead time + MTTR + change failure rate)
```

---

## Gotchas and Pitfalls

> [!WARNING]
> **High-cardinality labels crash Prometheus**
> Never use `user_id`, `request_id`, or any unbounded identifier as a Prometheus label.
>
> Wrong: `http_requests_total{user_id="12345"}` — creates millions of time series
> Right: `http_requests_total{endpoint="/api/users", method="GET", status="200"}` — bounded set of values

> [!WARNING]
> **Counters always go up — never use them for values that can decrease**
> If a counter resets (e.g., process restart), Prometheus detects the reset automatically and handles it correctly via `rate()` — but using `increase()` on a gauge-like value will give wrong results.
>
> Wrong: Using a Counter for `active_connections` (which goes down when connections close)
> Right: Use a Gauge for values that decrease; Counter only for cumulative totals

> [!WARNING]
> **Feature flags without cleanup become permanent complexity**
> Every feature flag that is never removed adds a branch to your code that must be tested, understood, and maintained. Set a target removal date when creating every flag.
>
> Symptom: A codebase with 50+ flags, half of which are always `true` in production and no one knows what they control.

**Other things to watch out for:**

- **Sampling distributed traces** — tracing every request at high load is expensive; use head-based sampling for consistent traces or tail-based sampling for selective capture of errors
- **Alert noise kills on-call morale** — every alert should be actionable; if you can't write a runbook for it, it shouldn't fire
- **SLOs too strict or too loose** — 99.99% is probably too strict for most services; 95% is probably too loose; start with 99.5% and adjust based on error budget consumption
- **Sentry DSN in client-side code** — PostHog API keys should be treated carefully; Sentry DSNs for frontend SDKs are designed to be public, but backend DSNs are secret

---

## DORA Metrics Reference

| Metric | Definition | Elite Target | Poor Target |
|--------|-----------|-------------|-------------|
| **Deployment Frequency** | How often code is deployed to production | On-demand (multiple/day) | Less than once/month |
| **Lead Time for Changes** | Time from commit to production | Less than 1 hour | More than 6 months |
| **MTTR** | Time to restore service after an incident | Less than 1 hour | More than 1 week |
| **Change Failure Rate** | % of deployments causing a production failure | 0–15% | 46–60% |

_Source: DORA State of DevOps Report — [dora.dev](https://dora.dev/research/)_

---

## Module Cross-References

| If you need to recall... | See module |
|--------------------------|-----------|
| PromQL basics and metric types | [[modules/02_metrics-and-prometheus]] |
| Grafana dashboard design | [[modules/03_dashboards-and-grafana]] |
| Sentry SDK setup | [[modules/04_error-tracking-with-sentry]] |
| OpenTelemetry SDK patterns | [[modules/05_distributed-tracing]] |
| PostHog flag SDK | [[modules/06_posthog-product-analytics]] |
| DataDog APM configuration | [[modules/07_datadog-apm]] |
| Flag types and targeting | [[modules/08_feature-flags-deep-dive]] |
| Canary and blue-green | [[modules/09_progressive-delivery]] |
| Runbook and post-mortem format | [[modules/10_incident-response]] |
| DORA + SPACE in detail | [[modules/11_developer-experience]] |

---

_Last updated: 2026-06-09_
