# Module 09: Performance Testing

[← Behavior-Driven Development](../08_behavior-driven-development/) | [Topic Home](../../README.md) | [Next → Accessibility Testing](../10_accessibility-testing/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-red)
![Time](https://img.shields.io/badge/time-7--9h-orange)

---

> Load testing with k6 and Locust; stress vs. soak testing; identifying bottlenecks; profiling; baseline and regression performance tests.

## Overview

This module is a stub. Content will be added in a future iteration.

**Topics covered in this module:**

- Performance testing taxonomy — load testing, stress testing, soak/endurance testing, spike testing
- k6 — writing k6 scripts in JavaScript, virtual users, ramp-up patterns, thresholds, CI integration
- Locust — writing Locust scenarios in Python, distributed load generation, real-time monitoring
- Baseline performance tests — establishing performance SLAs and regression thresholds
- Profiling Python applications — `cProfile`, `py-spy`, identifying CPU and memory bottlenecks
- Profiling Node.js applications — `--prof`, Chrome DevTools, identifying event loop blocking
- Database performance — slow query analysis, `EXPLAIN ANALYZE` in PostgreSQL
- Performance testing in CI — when to run, how to avoid false positives from environment variance
- Chaos engineering — introducing failures deliberately (Netflix's Chaos Monkey principles)

## Prerequisites

- Module 04: Integration Testing in this topic
- Basic understanding of HTTP and server architecture

## Objectives

By the end of this module, you will be able to:

1. Write k6 load test scripts that simulate realistic user traffic patterns
2. Design stress and soak test scenarios that identify system limits
3. Interpret k6 and Locust output to identify bottlenecks
4. Profile a Python or Node.js application to find CPU and memory inefficiencies
5. Define performance SLAs and write automated performance regression tests

## Cross-Links

- [[devops-platform-engineering]] — Performance testing is often integrated into CD pipelines; observability tools (Prometheus, Grafana) are the companion to performance tests
- [[qa-testing/modules/11_qa-strategy-and-metrics]] — Performance SLAs are part of QA strategy
- [[django-fastapi-flask]] — FastAPI's async architecture has specific performance characteristics worth testing
