# Projects — Module 01: Introduction to Observability

> These project ideas are specific to the concepts introduced in Module 01.
> For the full project list (beginner through capstone), see [../../PROJECTS.md](../../PROJECTS.md).

---

## Module 01 Project Ideas

### P01-A: Instrument a Personal Flask or FastAPI App

**Description:**
Take any Python web application you've built before (or build a minimal 3-endpoint API) and add the complete observability foundation from this module:
1. Prometheus metrics (counter for request count, histogram for latency) using `prometheus_client`
2. Structured JSON logging with `structlog` or Python's `logging` with a JSON formatter
3. Sentry error tracking (free tier is fine)

**Success Criteria:**
- [ ] Running the app and making requests produces Prometheus-format metrics at `/metrics`
- [ ] Log output is structured JSON with consistent fields (timestamp, level, event, request_id)
- [ ] Deliberately triggering an exception causes it to appear in Sentry

**Estimated Time:** 3–5 hours
**Concepts from this module:** Metrics pillar, logs pillar, toolchain landscape

---

### P01-B: SLO Design Document

**Description:**
Choose a real (or hypothetical) web service and write an SLO design document. This is a written exercise, not a coding exercise.

Your document should include:
1. Service description (2–3 sentences on what it does and who uses it)
2. Three candidate SLIs with justification for why each reflects user experience
3. Proposed SLO targets for each SLI with rationale (why 99.9% and not 99.5% or 99.99%?)
4. Monthly error budget calculations for each SLO
5. Error budget policy: what happens when 50% is consumed? When 90% is consumed? When 100% is consumed?

**Success Criteria:**
- [ ] At least 3 SLIs chosen, each clearly tied to user experience (not infrastructure)
- [ ] Error budget calculations are correct
- [ ] Error budget policy has specific, actionable consequences (not just "we'll be careful")

**Estimated Time:** 2–3 hours
**Concepts from this module:** SLI, SLO, SLA, error budget

---

### P01-C: Feature Flag Implementation Comparison

**Description:**
Implement the same feature flag (a simple "show new homepage" flag) in three different ways:
1. Environment variable flag (simplest possible)
2. Database-backed flag (read flag state from SQLite or any database on each request)
3. PostHog SDK flag (uses PostHog's free tier)

Compare the three implementations in a written analysis covering: implementation complexity, latency overhead, ability to do per-user targeting, and operational cost of changing flag state.

**Success Criteria:**
- [ ] All 3 implementations work and can be toggled without code changes
- [ ] Written comparison addresses all 4 comparison dimensions
- [ ] Analysis correctly identifies which approach is best for which scenario

**Estimated Time:** 4–6 hours
**Concepts from this module:** Feature flags, kill switches, progressive rollout concepts

---

## Recording Your Attempt

When you attempt a project, fill in the template below and add it to this file (append below, don't overwrite):

```markdown
### My Attempt: [P01-X: Project Name]

**Started:** {{YYYY-MM-DD}}
**Completed:** {{YYYY-MM-DD}} (or "In progress")
**Time Spent:** {{HOURS}} hours
**Result link:** {{LINK_OR_"local only"}}

**What went well:**
- ...

**What was harder than expected:**
- ...

**What I'd do differently:**
- ...

**Score (1–5):** /5
```
