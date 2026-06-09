# Feature Flags, System Monitoring, and Developer Experience — Resources

> [!WARNING]
> **Verified resources only.** Every entry in this file must be something you have
> personally confirmed exists, is accessible, and is genuinely useful.
> Do not add resources based on hearsay, AI suggestions, or titles that "sound right."
> A short list of excellent resources beats a long list of unverified ones.

---

## Official Documentation

- **[Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)** — The primary reference for Prometheus concepts, configuration, and PromQL. Start here for metric types and query syntax.
- **[Grafana Documentation](https://grafana.com/docs/grafana/latest/)** — Covers data sources, panel types, alerting, and dashboard-as-code (Grafonnet).
- **[Sentry Documentation](https://docs.sentry.io/)** — SDK integration guides for Python, JavaScript, and other languages; performance monitoring reference.
- **[PostHog Documentation](https://posthog.com/docs)** — Event schema, SDK setup, feature flags, A/B testing, and session recordings.
- **[DataDog Documentation](https://docs.datadoghq.com/)** — Agent installation, APM tracing, log management, and monitor/alert configuration.
- **[OpenTelemetry Documentation](https://opentelemetry.io/docs/)** — Vendor-neutral SDK reference for traces, metrics, and logs across all languages.

---

## Books

| Title | Author | Level | Format | Notes |
|-------|--------|-------|--------|-------|
| Site Reliability Engineering | Beyer, Jones, Petoff, Murphy (Google) | Intermediate | Print/eBook/Free online | The canonical SRE reference; Chapters 4–6 on SLOs and error budgets are essential — [sre.google/sre-book](https://sre.google/sre-book/table-of-contents/) |
| The Site Reliability Workbook | Beyer, Murphy, et al. (Google) | Intermediate | Print/eBook/Free online | Practical companion to the SRE Book with worked examples — [sre.google/workbook](https://sre.google/workbook/table-of-contents/) |
| Observability Engineering | Majors, Fong-Jones, Miranda | Advanced | Print/eBook | Covers the "observability-driven development" philosophy and OpenTelemetry in depth |
| Continuous Delivery | Humble, Farley | Intermediate | Print/eBook | The foundational text on deployment pipelines; Chapter 10 on feature flags is directly relevant |

---

## Online Courses

| Course | Platform | Level | Free? | Notes |
|--------|----------|-------|-------|-------|
| [Prometheus and Grafana for Beginners](https://www.udemy.com/course/prometheus-and-grafana-the-complete-guide/) | Udemy | Beginner | No (discounted frequently) | Hands-on lab-based; covers installation through alerting |
| [OpenTelemetry Bootcamp](https://www.aspecto.io/opentelemetry-bootcamp/) | Aspecto | Intermediate | Yes | Free video series covering OTel concepts and SDK usage |
| [Google SRE Learning Path](https://cloud.google.com/training/course-descriptions/sre-learning-path) | Google Cloud | Intermediate | No | Official Google content; covers SLOs, error budgets, and incident management |

---

## Video Resources

| Title / Channel | Creator | Type | Level | Notes |
|-----------------|---------|------|-------|-------|
| [Prometheus Tutorial for Beginners](https://www.youtube.com/watch?v=h4Sl21AKiDg) | TechWorld with Nana | Single video | Beginner | Clear introduction to the Prometheus architecture and PromQL basics |
| [Grafana Crash Course](https://www.youtube.com/watch?v=lILY8eSspEo) | Traversy Media | Single video | Beginner | Quick practical introduction to building Grafana dashboards |
| [OpenTelemetry explained](https://www.youtube.com/watch?v=r8UvWSX3GZc) | Honeycomb | Single video | Intermediate | Explains the OTel data model and SDK setup concisely |

---

## Blogs and Articles

- **[Cindy Sridharan's "Monitoring and Observability"](https://copyconstruct.medium.com/monitoring-and-observability-8417d1952e1c)** by Cindy Sridharan — The canonical blog post distinguishing monitoring from observability; read this before anything else
- **[The RED Method](https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/)** by Tom Wilkie (Grafana Labs) — Rate, Errors, Duration: the three metrics every service needs
- **[Google's SRE Error Budget Policy](https://sre.google/workbook/error-budget-policy/)** — How to operationalize error budgets in a real team
- **[Feature Flags Best Practices](https://launchdarkly.com/blog/feature-flag-best-practices/)** by LaunchDarkly — Covers flag taxonomy, naming conventions, lifecycle management, and technical debt

---

## Papers and Research

| Title | Authors | Year | Link | Why It Matters |
|-------|---------|------|------|---------------|
| Dapper, a Large-Scale Distributed Systems Tracing Infrastructure | Sigelman et al. (Google) | 2010 | [Research paper](https://research.google/pubs/pub36356/) | The foundational paper for all distributed tracing systems |
| Accelerate: The Science of Lean Software | Forsgren, Humble, Kim | 2018 | Book (not free) | Introduces DORA metrics with peer-reviewed statistical evidence |

---

## Tools and Libraries

| Tool / Library | Language | Purpose | Link |
|---------------|----------|---------|------|
| `prometheus_client` | Python | Expose Prometheus metrics from Python apps | [Docs](https://github.com/prometheus/client_python) |
| `prom-client` | JavaScript/Node | Expose Prometheus metrics from Node.js apps | [Docs](https://github.com/siimon/prom-client) |
| `opentelemetry-sdk` | Python | OpenTelemetry tracing, metrics, logs | [Docs](https://opentelemetry.io/docs/instrumentation/python/) |
| `@opentelemetry/sdk-node` | JavaScript | OpenTelemetry for Node.js | [Docs](https://opentelemetry.io/docs/instrumentation/js/) |
| `sentry-sdk` | Python | Sentry error tracking and performance | [Docs](https://docs.sentry.io/platforms/python/) |
| `posthog` | Python | PostHog analytics and feature flags | [Docs](https://posthog.com/docs/libraries/python) |
| Grafonnet | Jsonnet | Dashboard-as-code for Grafana | [Docs](https://grafana.github.io/grafonnet/API/dashboard/) |

---

## Communities

| Community | Platform | Focus | Link |
|-----------|----------|-------|------|
| r/devops | Reddit | General DevOps and observability discussion | [r/devops](https://www.reddit.com/r/devops/) |
| CNCF Slack | Slack | OpenTelemetry, Prometheus, Grafana channels | [Invite](https://slack.cncf.io/) |
| Stack Overflow | Stack Overflow | Technical Q&A | [Tag: prometheus](https://stackoverflow.com/questions/tagged/prometheus) |
| OpenTelemetry GitHub | GitHub | Issues, RFCs, SDK development | [github.com/open-telemetry](https://github.com/open-telemetry) |

---

## Cheat Sheets and Quick References

- **[PromQL Cheat Sheet](https://promlabs.com/promql-cheat-sheet/)** — Quick reference for PromQL operators and functions; maintained by PromLabs
- **[OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)** — Official reference for standard attribute names in OTel spans and metrics

See also the local [CHEATSHEET.md](./CHEATSHEET.md) which you'll build yourself as you study.

---

## My Recommendations

_Fill in as you progress — what actually helped you most?_

### Best for Absolute Beginners

> _To be filled in_

### Best for Building Mental Models

> _To be filled in_

### Best for Practical / Hands-On Learning

> _To be filled in_

### Best Deep Reference

> _To be filled in_

---

## Resources to Evaluate

_Drop links here when you find something but haven't verified it yet._

- [ ] Honeycomb's observability blog — needs evaluation
- [ ] DataDog's "Learning Center" free courses — needs evaluation
