# Resources — Module 01: Introduction to Observability

> Resources listed here are specific to **this module's content**.
> For the full topic resource list (books, courses, communities), see [../RESOURCES.md](../../RESOURCES.md).

---

## Primary Resource

_The single best thing to read/watch if you only have time for one resource._

**[Monitoring and Observability](https://copyconstruct.medium.com/monitoring-and-observability-8417d1952e1c)** — Cindy Sridharan

This 2017 blog post is the canonical introduction to the monitoring-vs-observability distinction. It explains the conceptual shift in clear, practical terms with real-world examples. Read this before anything else in this module — it will make everything else click faster.

---

## Official Documentation

_The canonical reference for anything covered in this module._

- **[Google SRE Book — Chapter 4: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)** — The authoritative treatment of SLIs, SLOs, and error budgets. Free to read online. Chapters 4 and 5 are directly relevant to this module.
- **[OpenTelemetry — What is Observability?](https://opentelemetry.io/docs/concepts/observability-primer/)** — The CNCF's primer on observability concepts; concise and up-to-date.
- **[Prometheus Overview](https://prometheus.io/docs/introduction/overview/)** — Brief but authoritative description of the Prometheus data model and pull-based collection model.

---

## Relevant Book Chapters

_Specific chapters from the topic's main books that cover this module's material._

| Book | Chapter(s) | Notes |
|------|-----------|-------|
| Site Reliability Engineering (Google) | Ch. 4: SLOs, Ch. 5: Eliminating Toil | Free at sre.google; Chapter 4 is essential for SLI/SLO concepts |
| Observability Engineering (Majors, Fong-Jones, Miranda) | Ch. 1–3 | Covers the observability philosophy and why metrics+logs alone are insufficient |

---

## Videos

_Specific videos that explain this module's concepts well._

- **[What is Observability? (Grafana Labs)](https://www.youtube.com/watch?v=M0CaqSAggbk)** (~15 min) — Clear, concise explanation of the three pillars with good visual metaphors
- **[SLOs, SLIs, and Error Budgets Explained](https://www.youtube.com/watch?v=tEylFyxbDLE)** (~25 min) — Practical walkthrough of calculating error budgets and applying them to real service decisions

---

## Related Modules in This Topic

_Other modules that closely relate to this one._

| Module | Relationship |
|--------|-------------|
| [[modules/02_metrics-and-prometheus]] (Module 02) | Deep-dives into Prometheus metric types and PromQL; builds directly on the metrics pillar introduced here |
| [[modules/05_distributed-tracing]] (Module 05) | Implements the distributed tracing concepts introduced here using OpenTelemetry |
| [[modules/08_feature-flags-deep-dive]] (Module 08) | Expands on the feature flag concepts introduced here with production-grade patterns |

---

## Related Modules in Other Topics

_Modules from other topics that cover related concepts._

| Topic | Module | Relationship |
|-------|--------|-------------|
| [[devops-platform-engineering]] | Module 01: Introduction | CI/CD pipelines and deployment strategies are the context in which observability operates |
| [[systems-architecture]] | Distributed Systems modules | Microservice architectures create the distributed tracing challenges covered in this module |

---

## Resources to Evaluate

_Links found but not yet verified as genuinely useful. Check before relying on these._

- [ ] "The Art of SLOs" course by Google — described as a free online course; verify it's still available and accurate
- [ ] Charity Majors' talks at various conferences on observability — multiple recordings available; need to identify the best single starting point
