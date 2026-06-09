# Product Management, Design and Discovery — Cheat Sheet

> [!TIP]
> This cheat sheet is a reference for **after you've learned the material** — not a shortcut
> to avoid learning it. If you're looking something up here before truly understanding it,
> go back to the relevant module first. A cheat sheet only helps people who already know
> what they're looking for.

---

## Quick Navigation

- [Prioritization Frameworks](#prioritization-frameworks)
- [OKR Template](#okr-template)
- [User Story Template](#user-story-template)
- [Problem Statement Template](#problem-statement-template)
- [Product Strategy One-Pager Template](#product-strategy-one-pager-template)
- [Decision Guide: Which Framework to Use](#decision-guide-which-framework-to-use)
- [Common PM Pitfalls](#common-pm-pitfalls)
- [Module Cross-References](#module-cross-references)

---

## Prioritization Frameworks

### RICE Scoring

**Formula:** `RICE Score = (Reach × Impact × Confidence) / Effort`

| Dimension | Definition | How to Estimate |
|-----------|-----------|----------------|
| **Reach** | How many users affected per time period? | Number of users who encounter this touchpoint per quarter |
| **Impact** | How much does it move the North Star metric? | 0.25 (minimal), 0.5 (low), 1 (medium), 2 (high), 3 (massive) |
| **Confidence** | How confident are you in your estimates? | 100% (high evidence), 80% (medium), 50% (low — gut feel) |
| **Effort** | How many person-months to build, including design and QA? | 1 = one person for one month |

**Example:**

```text
Feature: Email digest of weekly activity
Reach: 800 users/quarter
Impact: 0.5 (low — nice to have)
Confidence: 80%
Effort: 2 person-months

RICE = (800 × 0.5 × 0.8) / 2 = 160
```

---

### ICE Scoring

**Formula:** `ICE Score = Impact × Confidence × Ease`

Simpler than RICE — useful for early-stage teams or when Reach is hard to estimate.

| Dimension | Scale | Notes |
|-----------|-------|-------|
| **Impact** | 1–10 | How much will this move the metric? |
| **Confidence** | 1–10 | How confident are you? (1 = wild guess, 10 = proven data) |
| **Ease** | 1–10 | How easy is this to implement? (1 = very hard, 10 = trivial) |

---

### MoSCoW

| Category | Meaning | Use When |
|----------|---------|---------|
| **Must have** | Without this, the release fails or is unsafe | Non-negotiable for launch |
| **Should have** | Important but can survive a delay | Prioritize unless time-constrained |
| **Could have** | Nice to have; low impact if missing | Include only if time permits |
| **Won't have** | Explicitly out of scope for this release | Communicate clearly to manage expectations |

---

### Value vs. Effort Matrix

```text
                High Value
                    │
       Quick Wins   │   Major Projects
  ─────────────────┼─────────────────
       Fill-ins     │   Thankless Tasks
                    │
                Low Value
        Low Effort      High Effort
```

- **Quick Wins** (high value, low effort): Do these first
- **Major Projects** (high value, high effort): Plan carefully, build conviction before committing
- **Fill-ins** (low value, low effort): Do only if bandwidth exists
- **Thankless Tasks** (low value, high effort): Avoid or eliminate

---

### Kano Model

| Category | User Feeling | Examples |
|----------|-------------|---------|
| **Basic** (must-be) | Dissatisfied if absent; satisfied at best | App doesn't crash, data saves correctly |
| **Performance** (one-dimensional) | More = better, less = worse | Load time, search result accuracy |
| **Excitement** (delighter) | Not expected; delights when present | Spotify Discover Weekly, iPhone camera |
| **Indifferent** | Users don't care either way | Many "power user" features |
| **Reverse** | Some users dislike it | Forced onboarding, auto-play videos |

---

## OKR Template

```text
OBJECTIVE: [Qualitative, inspiring statement of what you want to achieve]
Time horizon: [Quarter/Year]
Owner: [Team or individual]

  KR1: [Metric] from [current baseline] → [target] by [date]
  KR2: [Metric] from [current baseline] → [target] by [date]
  KR3: [Metric] from [current baseline] → [target] by [date]

Initiatives supporting this OKR:
  • [Project or experiment 1]
  • [Project or experiment 2]
  • [Project or experiment 3]
```

**Example:**

```text
OBJECTIVE: Dramatically improve new user activation
Time horizon: Q3 2026
Owner: Growth team

  KR1: % users completing core action in first 7 days: 23% → 40%
  KR2: Median time-to-first-value: 4 days → 1 day
  KR3: D7 retention for new users: 31% → 45%

Initiatives:
  • Redesign onboarding checklist (in discovery)
  • Add contextual tooltips for first-time users (in development)
  • Email activation sequence experiment (planned)
```

---

## User Story Template

```text
As a [type of user],
I want [to do something / to have something happen],
so that [I can achieve a goal / get a benefit].

Acceptance criteria:
  • [Criterion 1 — specific and testable]
  • [Criterion 2 — specific and testable]
  • [Criterion 3 — edge case or error state]

Out of scope:
  • [What this story deliberately does NOT cover]

Open questions:
  • [Anything still to be decided before development]
```

**Good vs. Bad User Stories:**

| Bad | Good | Why |
|-----|------|-----|
| As a user, I want a dashboard. | As a manager, I want to see my team's task completion rate this week so I can identify blockers before they escalate. | Specific user, specific need, specific reason |
| As an admin, I want the system to be fast. | As a job seeker, I want search results to appear within 2 seconds so I don't lose my train of thought. | Measurable, user-centered |

---

## Problem Statement Template

A well-formed problem statement answers:

```text
[User type] struggles to [task/goal] when [context/situation]
because [root cause], which results in [negative outcome].

We believe that [proposed solution approach] will help [user type]
to [accomplish goal], as measured by [success metric].
```

**Example:**

```text
New users (< 7 days) struggle to find their first meaningful action in the product
when they log in for the first time, because the home screen shows all features equally
without guidance, which results in 60% of new users leaving without completing a
core action and not returning.

We believe that a contextual first-run experience that surfaces one core action will
help new users experience value faster, as measured by % completing core action in day 1.
```

---

## Product Strategy One-Pager Template

```text
PRODUCT: [Product name]
DATE: [Quarter/Year]
AUTHOR: [PM name]

VISION (5 years):
[One paragraph: What does the world look like if we succeed? What has changed for users?]

STRATEGY (1–2 years — how we win):
[2–3 sentences: What bets are we making? What are we explicitly NOT doing?]

TARGET USERS:
  Primary: [Most important user segment — who we optimize for]
  Secondary: [Other users we serve but don't sacrifice primary for]

NORTH STAR METRIC: [The one metric that best captures user value]
Current: [X] → Target in 12 months: [Y]

PRODUCT BETS (top 3 priorities):
  1. [Bet 1] — Hypothesis: [X] → Expected outcome: [Y]
  2. [Bet 2] — Hypothesis: [X] → Expected outcome: [Y]
  3. [Bet 3] — Hypothesis: [X] → Expected outcome: [Y]

EXPLICITLY NOT DOING (for now):
  • [Thing 1] — revisit in [time period] if [condition]
  • [Thing 2]
```

---

## Decision Guide: Which Framework to Use

```text
Need to prioritize a backlog?
│
├── If you have data on user reach → Use RICE
│
├── If you lack data (early stage) → Use ICE
│
├── If you have stakeholder pressure to "do everything" → Use MoSCoW to force tradeoffs
│
├── If you need to understand user satisfaction drivers → Use Kano model
│
└── If you have a binary keep/cut decision → Use value vs. effort matrix
```

---

## Common PM Pitfalls

> [!WARNING]
> **Building without discovery**
> Shipping features before validating the problem is real and the solution will work.
> Symptom: "We built it but users don't use it."
> Antidote: Run at least 5 user interviews before committing to a solution.

> [!WARNING]
> **Mistaking user requests for user needs**
> Users say "I want a filter" when they mean "I can't find what I'm looking for."
> Symptom: Building every feature users ask for but user satisfaction doesn't improve.
> Antidote: Always ask "why do you want that?" until you reach the underlying job.

> [!WARNING]
> **Roadmap as commitment**
> Treating a roadmap as a promise rather than a hypothesis, making it impossible to change when you learn something new.
> Symptom: Engineering feels blindsided by changes; stakeholders are angry when items move.
> Antidote: Communicate explicitly that roadmaps express current thinking, not contracts. Use outcome language.

**Other pitfalls:**

- **Confusing activity with outcomes** — "We shipped 12 features last quarter" is not a PM success metric
- **Solving for the loudest customer** — One enterprise customer's request is not a validated user need
- **Skipping acceptance criteria** — Leads to rework when PM and engineer had different mental models of "done"
- **Saying yes to everything** — Every yes is also a no to something else; most of the PM job is deciding what NOT to build

---

## Module Cross-References

| If you need to recall... | See module |
|--------------------------|-----------|
| What a PM actually does day-to-day | [[modules/01_introduction]] |
| How to run a user interview | [[modules/02_user-research-and-discovery]] |
| How to write a problem statement | [[modules/03_problem-framing]] |
| Vision, strategy, OKRs | [[modules/04_product-strategy]] |
| RICE, ICE, Kano, MoSCoW | [[modules/05_prioritization]] |
| Roadmap formats and communication | [[modules/06_product-roadmaps]] |
| User flows and wireframe literacy | [[modules/07_ux-design-fundamentals]] |
| User story writing and backlog management | [[modules/08_agile-and-delivery]] |
| Funnel analysis, A/B test design | [[modules/09_metrics-and-analytics]] |
| GTM plan and launch tiers | [[modules/10_go-to-market-and-launch]] |
| Saying no and stakeholder alignment | [[modules/11_stakeholder-management]] |

---

_Last updated: 2026-06-09_
