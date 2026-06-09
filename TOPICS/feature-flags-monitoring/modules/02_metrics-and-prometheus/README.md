# Module 02: Metrics and Prometheus

[← Module 01: Introduction](../01_introduction/) | [Topic Home](../../README.md) | [Next → Module 03: Dashboards and Grafana](../03_dashboards-and-grafana/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner--Intermediate-blue)
![Time](https://img.shields.io/badge/time-6h-orange)

> **Stub module** — Content to be generated. See the topic README for the full module map.

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

This module covers the Prometheus metrics ecosystem in depth: the four metric types (counter, gauge, histogram, summary), the Prometheus data model with labels, PromQL query language basics, the exporter ecosystem for instrumenting third-party systems, and recording rules for query performance optimization.

By the end of this module, you will be able to instrument any Python or Node.js application with Prometheus metrics, write PromQL queries to compute rates, percentiles, and error budgets, and configure a Prometheus server to scrape and store your metrics.

**Difficulty:** Beginner–Intermediate &nbsp;|&nbsp; **Estimated time:** 6 hours

---

## Prerequisites

- Module 01: Introduction to Observability — specifically: understanding what metrics are and why they're needed
- Basic Python or JavaScript programming
- Familiarity with HTTP (you should be able to explain what a GET request is)

---

## Objectives

By the end of this module, you will be able to:

1. Explain the four Prometheus metric types (counter, gauge, histogram, summary) and choose the correct type for a given measurement
2. Instrument a Python or JavaScript application using the `prometheus_client` or `prom-client` SDK
3. Write PromQL queries using `rate()`, `sum()`, `histogram_quantile()`, and label selectors
4. Configure a `prometheus.yml` scrape config to collect metrics from your application
5. Explain the Prometheus pull-based collection model and why it differs from push-based systems
6. Use recording rules to pre-compute expensive queries for dashboard performance

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be generated when this module is expanded.
> The following outline describes what the theory section will cover.

### Planned Sections

1. **The Prometheus Data Model** — time series, labels, the pull-based scrape model, metric naming conventions
2. **Counter** — monotonically increasing; `rate()` function; when to use; common mistakes (using counter for decreasing values)
3. **Gauge** — current state; `set()`, `inc()`, `dec()`; use cases (queue depth, memory usage, active connections)
4. **Histogram** — value distribution; buckets; `histogram_quantile()`; choosing bucket boundaries
5. **Summary** — pre-computed quantiles; when to use vs. histogram; limitations
6. **PromQL Language** — selectors, matchers, rate(), increase(), functions, aggregation operators
7. **The Exporter Ecosystem** — node_exporter, blackbox_exporter, postgres_exporter, redis_exporter
8. **Recording Rules** — pre-computing expensive queries; performance optimization

---

## Key Concepts

_To be filled in when module is fully generated._

---

## Examples

_To be filled in when module is fully generated._

---

## Common Pitfalls

_To be filled in when module is fully generated._

---

## Cross-Links

- [[feature-flags-monitoring/modules/01_introduction]] — Introduces the metrics pillar; this module expands on it in depth
- [[feature-flags-monitoring/modules/03_dashboards-and-grafana]] — Grafana queries Prometheus using the PromQL learned in this module
- [[devops-platform-engineering]] — Kubernetes environments typically use kube-state-metrics and node_exporter alongside application metrics

---

## Summary

_To be filled in when module is fully generated._

---

## Further Reading

- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/) — Complete reference
- [PromQL Cheat Sheet](https://promlabs.com/promql-cheat-sheet/) — Quick reference for PromQL operators
- [Prometheus: Up & Running](https://www.oreilly.com/library/view/prometheus-up/9781492034131/) — [Verify: O'Reilly book by Brian Brazil — confirm availability]
