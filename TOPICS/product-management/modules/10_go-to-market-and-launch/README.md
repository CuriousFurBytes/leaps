# Module 10: Go-to-Market and Launch

[← Module 09: Metrics and Analytics](../09_metrics-and-analytics/) | [Topic Home](../../README.md) | [Next → Module 11: Stakeholder Management](../11_stakeholder-management/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-red)
![Time](https://img.shields.io/badge/time-3--4h-orange)

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

Shipping code is not launching a product. Launch is the deliberate act of making something available to the right users in a way that creates awareness, understanding, and adoption. Most teams underinvest in launch planning and then wonder why features don't get used.

This module covers GTM strategy structure, launch tiers (from silent technical releases to full-scale coordinated launches), pricing strategy basics, and how to develop positioning and messaging that communicates value to users and customers.

**Difficulty:** Advanced &nbsp;|&nbsp; **Estimated time:** 3–4 hours

---

## Prerequisites

- Module 04: Product Strategy — positioning and messaging flows from strategy
- Module 09: Metrics and Analytics — instrumentation planning is part of launch preparation

---

## Objectives

By the end of this module, you will be able to:

1. Write a GTM plan for a significant feature launch covering audience, positioning, messaging, and launch tier
2. Select an appropriate launch tier based on risk, audience size, and strategic importance
3. Articulate the positioning template: For... who... the product is a... that... unlike... our product...
4. Write a messaging hierarchy with a headline, three supporting points, and a clear call to action
5. Explain the basics of pricing strategy — value-based, cost-plus, and competitive pricing — and identify which is appropriate for different contexts
6. Identify what must be true before launch: instrumentation, support team readiness, and rollback plan

---

## Theory

### What "Launch" Actually Means

Launch is not a moment — it is a process. The decisions that determine a launch's success are made weeks or months before the day features become available to users.

A complete launch plan covers:

```text
AUDIENCE:         Who are we launching to? (Segment, size, characteristics)
PROBLEM:          What problem does this solve for them? (From validated discovery)
POSITIONING:      How does this fit in their world? How is it different from alternatives?
MESSAGING:        What do we say? In what order? In whose voice?
CHANNEL:          How do we reach them? (In-app, email, blog, press, social)
LAUNCH TIER:      Soft launch vs. full launch vs. phased rollout? Why?
INSTRUMENTATION:  What metrics are we tracking from day 1? Are they set up?
SUPPORT READINESS: Does support know what's launching? Do they have answers to common questions?
ROLLBACK PLAN:    What triggers a rollback, and how quickly can we execute it?
```

### Launch Tiers

Not every feature deserves the same launch treatment. Launch tiers match the investment in launch to the strategic importance and risk profile of the feature.

| Tier | Description | When to Use | Examples |
|------|-------------|------------|---------|
| **Tier 0: Silent release** | Code ships; no announcement; feature hidden or flag-gated | Technical infrastructure, internal tooling, preparatory work | Database migration, API refactor |
| **Tier 1: Limited beta** | Available to invited users only; active monitoring; gathering feedback | High-risk features; new product lines; B2B with enterprise pilots | AI writing assistant in beta |
| **Tier 2: Early access** | Available to opted-in users; feature flag; limited announcement | Significant new feature; want engaged users first | New mobile app; major redesign |
| **Tier 3: Full launch** | Available to all users; coordinated announcement across channels | Product-defining feature; strategic market moment | Major new product or flagship feature |
| **Tier 4: Major product announcement** | Press, event, coordinated marketing push, executive involvement | New product line, significant market pivot | iPhone launch equivalent |

Most features should be Tier 0–2. Tier 3 and above require significant marketing coordination and are reserved for genuinely strategic moments.

### Positioning Framework

Positioning is a statement of how your product fits into the customer's world — relative to alternatives and in terms of the value it creates.

The classic positioning template:

```text
For [target customer segment]
who [have this problem or need],
the [product/feature name] is a [category]
that [key benefit — how it solves the problem].
Unlike [alternatives/competitors],
our product [key differentiator].
```

**Example:**

```text
For project managers at growing companies (50–500 people)
who struggle to maintain visibility into distributed team progress
without spending hours compiling status reports,
StatusHQ is a project intelligence platform
that surfaces real-time status across all tools automatically.
Unlike Jira or Asana, StatusHQ requires zero manual status updates —
it pulls from where work actually happens.
```

Positioning is internal — it is the strategic foundation for messaging, not the copy itself. From positioning flows messaging.

### Messaging Hierarchy

A messaging hierarchy takes positioning and translates it into what you actually say to users:

```text
HEADLINE (what it is / what it does):
"Real-time project status. Zero manual updates."

SUBHEAD (elaboration of the headline value):
"StatusHQ connects to your existing tools and automatically surfaces what's on track, what's at risk, and what needs your attention — in one view."

THREE SUPPORTING POINTS:
1. Connect all your tools: Jira, Slack, GitHub, Google Docs — all in one status view
2. Automatic, not manual: No more asking for updates or compiling spreadsheets
3. Designed for conversations: One-click sharing to Slack, email, or slides

CALL TO ACTION:
"See your team's status in 5 minutes — free during beta"
```

### Pricing Strategy Basics

Pricing strategy is a full discipline, but PMs need a working vocabulary:

| Strategy | Description | When to Use |
|----------|-------------|------------|
| **Value-based pricing** | Price based on the value you create for the customer | B2B with measurable ROI; differentiated product |
| **Cost-plus pricing** | Price based on cost of production plus margin | Commodity products; when switching costs are low |
| **Competitive pricing** | Price relative to the market | Undifferentiated market; when value is hard to quantify |
| **Freemium** | Free tier + paid upgrade | B2C or B2B with low switching costs; when free usage creates viral adoption |
| **Usage-based** | Price per unit consumed | When value scales with usage (APIs, data, storage) |

For most B2B SaaS products, value-based pricing is most defensible: if your product saves a customer $50,000/year, you should charge significantly more than cost-plus would suggest.

---

## Key Concepts

**GTM strategy:** The plan for how a product or feature reaches its target users — covering audience, positioning, messaging, channels, launch tier, instrumentation, and rollback planning.

**Launch tier:** A classification of how much coordination and announcement a release warrants, from silent technical releases (Tier 0) to major coordinated product launches (Tier 4).

**Positioning:** The strategic description of how a product fits in the customer's world relative to alternatives and in terms of the value it creates. Internal-facing, not customer-facing copy.

**Messaging hierarchy:** The translation of positioning into customer-facing communication: headline, subhead, supporting points, and call to action.

**Instrumentation:** The metrics tracking setup required before a launch so that you can measure whether the launch succeeded from day one.

**Rollback plan:** A defined set of criteria and actions for reverting a launch if it causes unexpected negative outcomes.

---

## Examples

### Example 1: Spotify's Launch of Collaborative Playlists

Spotify's collaborative playlists feature (allowing multiple users to add to a shared playlist) was initially released as a Tier 1–2 feature — limited rollout, then early access — before becoming generally available.

Their GTM covered: Messaging focused on social use cases (road trip playlist, party music, couple's playlist). Channels were in-app education (tooltip on first use), social sharing (shareable playlist links), and blog posts for press. Instrumentation tracked: adoption rate, playlist sharing events, and whether collaborative playlists correlated with higher social engagement and friend connections.

The social mechanic made it naturally viral — users invited friends, creating a word-of-mouth channel Spotify didn't need to build.

### Example 2: The Rollback Trigger

A payments company launches a new checkout flow. Before launch, the PM defines:

- **Rollback trigger:** If checkout completion rate drops more than 5% from baseline, or if payment error rate increases more than 1%, we roll back within 4 hours.
- **Monitoring:** Real-time dashboard watching checkout step funnel and error rates from hour 1 of launch.
- **Rollback mechanic:** Feature flag — engineer can disable the new checkout in 5 minutes.

At 2 hours post-launch, a mobile-specific bug causes 12% checkout drop-off on iOS. The PM triggers rollback, notifies engineering, and publishes an internal post-mortem. The bug is fixed and the feature re-launches 3 days later. Because the team planned for rollback, the incident is contained and user impact is minimal.

---

## Common Pitfalls

**Pitfall 1: Treating every launch as a Tier 3 or Tier 4 event**
Not every feature needs a press release, a marketing campaign, and a company-wide email. Over-launching dilutes attention. Reserve big launches for genuinely strategic moments.

**Pitfall 2: Launching without instrumentation**
"We'll set up tracking after we see how it goes." After launch, you have users forming habits, support tickets accumulating, and stakeholder questions demanding answers. Instrument before you ship.

**Pitfall 3: Positioning as a customer-facing statement**
"We are the best project management tool for growing companies" is not positioning — it is marketing copy. Positioning is the internal strategic argument. Messaging is what customers see.

**Pitfall 4: No rollback plan**
Every significant feature launch carries risk. A rollback plan is not pessimism — it is professionalism. The cost of preparing a rollback plan is small; the cost of not having one when things go wrong is large.

---

## Cross-Links

- [[product-management/modules/04_product-strategy]] — Positioning flows from strategy; messaging flows from positioning
- [[product-management/modules/09_metrics-and-analytics]] — Instrumentation planning for launch is a metrics exercise
- [[product-management/modules/11_stakeholder-management]] — Launch communication to stakeholders (sales, support, executives) is a stakeholder management exercise
- [[feature-flags-monitoring]] — Feature flags are the technical mechanism for phased rollouts and rollbacks; monitoring is how you detect launch problems in real time

---

## Summary

- Launch is a process, not a moment — the decisions that determine success are made weeks before launch day
- Launch tiers match coordination investment to strategic importance: most features should be Tier 0–2; Tier 3–4 are reserved for genuinely strategic moments
- The positioning template frames product fit relative to the customer's world and alternatives; positioning is internal strategy, not customer-facing copy
- A messaging hierarchy translates positioning into what users actually read: headline → subhead → three supporting points → call to action
- Pricing strategy ranges from value-based (most defensible for differentiated B2B) to freemium (most effective for viral B2C adoption)
- Every significant launch needs instrumentation set up before go-live and a rollback plan with explicit triggers
