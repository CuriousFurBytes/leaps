# Module 08: Agile and Delivery

[← Module 07: UX Design Fundamentals](../07_ux-design-fundamentals/) | [Topic Home](../../README.md) | [Next → Module 09: Metrics and Analytics](../09_metrics-and-analytics/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate--advanced-orange)
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

Agile is how most software product teams operate today. But Agile as commonly implemented in companies often diverges significantly from the original intent of the Agile Manifesto — and understanding the gap is crucial for PMs who want to work effectively within it.

This module covers Scrum ceremonies from the PM's perspective, the fundamentals of backlog management, how to write user stories that create shared understanding rather than confusion, the discipline of story slicing (breaking large problems into small valuable increments), and how to think about velocity and estimation without falling into the trap of treating estimates as commitments.

**Difficulty:** Intermediate–Advanced &nbsp;|&nbsp; **Estimated time:** 3–4 hours

---

## Prerequisites

- Module 06: Product Roadmaps — the roadmap feeds the backlog
- Module 07: UX Design Fundamentals — designs become the input for stories

---

## Objectives

By the end of this module, you will be able to:

1. Explain the PM's role in each Scrum ceremony (sprint planning, standup, review, retrospective)
2. Write well-formed user stories in the standard format with clear acceptance criteria
3. Slice a large feature into smaller user stories that each deliver independent value
4. Distinguish between story points as a relative complexity estimate and calendar time as a delivery estimate
5. Manage a prioritized product backlog — grooming, refining, and maintaining it
6. Identify and avoid the most common PM failures in agile delivery contexts

---

## Theory

### The Agile Manifesto and the PM

The Agile Manifesto (2001) articulates four values:
1. **Individuals and interactions** over processes and tools
2. **Working software** over comprehensive documentation
3. **Customer collaboration** over contract negotiation
4. **Responding to change** over following a plan

The manifesto explicitly de-emphasizes the kind of work most waterfall PMs did: writing comprehensive specifications upfront, creating detailed project plans, and treating requirements as contracts. This is why the "old school" PM model — write a 50-page spec, hand to engineering, wait for delivery — is largely obsolete for software products.

The PM's role in an Agile context is to ensure the team is always working on the most valuable problems and that every increment delivered moves the product toward its goals.

### Scrum Ceremonies from the PM's Perspective

**Sprint Planning (1–2 hours per sprint)**
PM's role: Present the prioritized backlog items for the upcoming sprint, explain *why* each item matters (the problem being solved, not just the feature), answer questions from engineering, and facilitate scope negotiation. The PM does NOT tell engineering how to implement stories.

**Daily Standup (15 minutes)**
PM's role: Listen for blockers. Offer context or clarification when asked. Not a status report for the PM — it's a coordination tool for engineering. PMs who dominate standups slow teams down.

**Sprint Review / Demo (1 hour)**
PM's role: Evaluate what was built against acceptance criteria. Provide clear acceptance or rejection with reasoning. Invite stakeholders and customers to see working software. This is a *feedback* session, not a status presentation.

**Sprint Retrospective (1 hour)**
PM's role: Participate as an equal team member. Raise process issues from the PM perspective (unclear acceptance criteria, too much mid-sprint scope change, etc.). Listen to engineering's perspective on PM behavior. Implement one agreed improvement.

### User Story Writing

A user story is not a specification. It is a placeholder for a conversation. The classic format:

```text
As a [type of user],
I want [to do something],
so that [I achieve a benefit].
```

The story format forces the author to state the *user* (not "the system") and the *benefit* (not just the feature). But the most important part of a user story is the acceptance criteria — the explicit definition of done.

**User Story + Acceptance Criteria template:**

```text
STORY:
As a job seeker,
I want to save a job listing,
so that I can review it later before deciding to apply.

ACCEPTANCE CRITERIA:
- Saved jobs appear in a dedicated "Saved Jobs" list accessible from the nav
- User can save a job from the listing card or the job detail page
- User can unsave a job from either the listing or the saved list
- Saved state persists across sessions (survives logout/login)
- Saved count shown as a badge on the nav item

OUT OF SCOPE (for this story):
- Organizing saved jobs into folders (separate story)
- Email reminders about saved jobs (separate story)
- Sharing saved jobs with others (separate story)

OPEN QUESTIONS:
- Maximum number of saved jobs per user? (Engineering question — affects database schema)
- Should we track which jobs the user saved for recommendations? (Requires data team input)
```

### Story Slicing

Large features are not deliverable as single stories. The art of story slicing is breaking a feature into smaller stories that each deliver independent value (not just a layer of the technical stack).

**Horizontal vs. Vertical Slicing:**

Horizontal slicing (bad): Split by technical layer
```text
Story 1: Build database schema for saved jobs
Story 2: Build API endpoint for saved jobs
Story 3: Build UI for saved jobs
```
Problem: No single story delivers user value. All three must complete before anything ships.

Vertical slicing (good): Split by user functionality
```text
Story 1: User can save a job and view it in a basic saved list (no pagination)
Story 2: Saved list supports more than 20 items (pagination added)
Story 3: Saved state synced across devices
Story 4: User can remove jobs from saved list
```
Each story delivers value; each can ship independently; later stories add depth.

### Velocity and Estimation

Story points are a relative complexity estimate, not a time estimate. A story estimated at 5 points is roughly 5x more complex than a 1-point story, in the team's collective judgment.

**Why story points, not hours?**
- Hours imply precision that doesn't exist at the design/requirements stage
- Individuals estimate hours differently based on their skill level; team-based relative estimates are more consistent
- Story points capture complexity, uncertainty, and effort holistically

**Velocity** is the team's average number of points completed per sprint over the last 3–5 sprints. Used for capacity planning, not as a performance metric. Velocity is a planning tool, not a success measure.

> [!WARNING]
> Velocity becomes toxic when managers use it to compare teams or to pressure teams to increase it. A team that increases velocity by reducing story quality, skipping tests, or inflating estimates is not improving — it is gaming the metric.

---

## Key Concepts

**Sprint:** A fixed-length work period (typically 1–2 weeks) during which the team builds a prioritized set of stories.

**User story:** A user-centered description of a feature in the format "As a [user], I want [action], so that [benefit]." Always accompanied by acceptance criteria.

**Acceptance criteria:** The specific, testable conditions that define when a story is done. Written before development begins.

**Story slicing:** Breaking large user stories into smaller, independently valuable increments that can each ship and be measured separately.

**Backlog:** The prioritized list of user stories and problems the team will work on. Groomed regularly to ensure items at the top are well-defined and ready.

**Velocity:** The team's average story points completed per sprint. A planning tool, not a performance metric.

**Definition of done:** A team-level standard describing what "complete" means for any story (e.g., coded, tested, reviewed, deployed to staging, acceptance criteria met, documentation updated).

---

## Examples

### Example 1: Good vs. Bad User Stories

**Bad:** "Build a notification system for the platform."
(No user, no benefit, no acceptance criteria — this is a project, not a story)

**Bad:** "The system should send an email when a user's trial expires."
(System as actor, not user; no benefit articulated; passive voice hides who experiences this)

**Good:**
```text
As a user on a free trial,
I want to receive an email 3 days before my trial expires,
so that I have enough time to decide whether to upgrade without being caught off guard.

Acceptance criteria:
- Email sent 3 days before trial end date
- Email contains: days remaining, what they'll lose access to, a clear CTA to upgrade
- Only sent once per user per trial period (no duplicates)
- Not sent to users who have already upgraded
```

### Example 2: Amazon's PR/FAQ as Agile Input

Amazon's "Working Backwards" process (write the press release first) produces a document that functions as a high-quality input to the agile process. The press release defines the user, the benefit, and the success criteria in customer-facing language. The FAQ surfaces assumptions and open questions before any story is written. This pre-work reduces the PM's "just in time" specification burden during sprint planning and produces better acceptance criteria.

---

## Common Pitfalls

**Pitfall 1: PM writing implementation-level stories**
"Add a POST /api/v2/saves endpoint that accepts job_id and user_id parameters" is an engineering task, not a user story. If PMs write implementation specs, they remove engineering creativity and often specify the wrong solution.

**Pitfall 2: Stories without acceptance criteria**
Stories without acceptance criteria are interpreted differently by every engineer. The PM thinks "of course it should handle the error state" while the engineer thinks "I wasn't told to." Write criteria before development starts.

**Pitfall 3: Treating velocity as a commitment**
"The team's velocity is 30 points, so they'll definitely finish these 30 points this sprint." Velocity is an average — it fluctuates. Illness, unexpected complexity, and external dependencies happen. Use velocity for planning, not promises.

**Pitfall 4: Mid-sprint scope changes**
Changing story scope mid-sprint forces engineering to partially complete work, which is significantly more expensive than completing a sprint and re-prioritizing. PMs who frequently change scope mid-sprint damage velocity and team trust.

---

## Cross-Links

- [[product-management/modules/06_product-roadmaps]] — Roadmap Now horizon items become sprint backlog items
- [[product-management/modules/07_ux-design-fundamentals]] — Designs completed in the prior phase become the input for user stories
- [[product-management/modules/09_metrics-and-analytics]] — Measuring whether shipped stories achieved their intended outcomes
- [[qa-testing]] — QA and acceptance testing are how stories are validated against acceptance criteria
- [[feature-flags-monitoring]] — Feature flags enable teams to ship code continuously without exposing incomplete features to users — a key agile delivery pattern
- [[devops-platform-engineering]] — CI/CD pipelines are the technical foundation that makes sprint cadence and frequent releases possible

---

## Summary

- Agile's core insight is that responding to change is more valuable than following a plan; the PM's role is to ensure the team works on the most valuable problems every sprint
- Scrum ceremonies are useful communication rituals: planning sets sprint scope, standups surface blockers, reviews provide feedback on working software, and retrospectives improve team process
- User stories should specify the user, the action, and the benefit — not the implementation; acceptance criteria make "done" unambiguous before development starts
- Vertical story slicing (by user value delivered) is always preferable to horizontal slicing (by technical layer); each story should independently ship and deliver value
- Story points measure relative complexity, not time; velocity is a planning tool, not a performance metric
- The most common PM failures in agile are: over-specifying implementation, missing acceptance criteria, and changing scope mid-sprint
