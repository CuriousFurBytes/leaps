# Product Management, Design and Discovery — Glossary

> A living reference. Add terms as you encounter them — don't wait until you understand them perfectly.
> Writing a definition in your own words is itself a powerful learning tool.

---

## How to Add a Term

Copy this template and fill it in:

```markdown
### term-name

**Definition:** A clear, concise explanation of what this term means in the context of Product Management.

**Also known as:** Other names, abbreviations, or synonyms (if any).

**Related:** [[related-concept]], [[another-related-concept]]

**Example:**
A concrete, specific example of the term in use.
```

Keep definitions in your own words as much as possible.

---

## A

### acceptance criteria

**Definition:** The specific, measurable conditions that a feature or user story must satisfy before it is considered complete and ready for release. Acceptance criteria define the "done" state unambiguously so that engineers, designers, and PMs all agree on what success looks like before work begins.

**Also known as:** Definition of done (related but distinct — acceptance criteria are per-story; definition of done is team-wide)

**Related:** user story, backlog

**Example:**
For a user story "As a user, I want to reset my password so that I can regain access to my account," an acceptance criterion might be: "User receives an email within 60 seconds of requesting a password reset, and the reset link expires after 24 hours."

---

## B

### backlog

**Definition:** The ordered list of all work items a product team has identified as potentially valuable. The backlog is not a commitment — it is a living, prioritized list. Items at the top are well-defined and ready for development; items at the bottom may be rough ideas that haven't been refined yet.

**Also known as:** Product backlog

**Related:** sprint, epics, user story, prioritization

**Example:**
A backlog might contain 120 items ranging from "fix typo on pricing page" (small, clear) to "redesign onboarding flow" (large, vague) to "explore native mobile app" (exploratory, undefined).

---

## D

### discovery vs. delivery

**Definition:** The two fundamental modes of product work. Discovery is the work of figuring out *what* to build — validating that a problem is real, that users want a solution, and that the solution you're proposing will actually work. Delivery is the work of *building* the solution once discovery has de-risked it. Most product teams over-invest in delivery and under-invest in discovery.

**Also known as:** Product discovery / product delivery; sometimes "dual-track Agile"

**Related:** MVP, continuous discovery habits, product development lifecycle

**Example:**
A team notices users abandoning checkout at the payment step. Discovery work involves interviewing users, watching session recordings, and testing hypotheses about why (confusion? distrust? friction?). Delivery work is building the redesigned checkout flow after the root cause is identified.

---

## E

### epics

**Definition:** Large units of work that represent a significant feature area or goal, typically too large to complete in a single sprint. Epics are broken down into smaller user stories for development. They serve as organizing containers that help teams and stakeholders see the big picture.

**Also known as:** Features (loosely), initiatives (at an even higher level)

**Related:** user story, backlog, sprint

**Example:**
"Enable social login" is an epic. Under it, individual user stories might include: "As a user, I can log in with Google," "As a user, I can log in with Apple," and "As a user, I can link my social account to an existing email account."

---

## G

### go-to-market (GTM)

**Definition:** The plan for how a company or team will bring a product or feature to market. A GTM strategy covers target audience, positioning and messaging, distribution channels, pricing, and the launch plan. For a feature launch, it might be simpler — which users see it first, what the in-app announcement says, and how the support team is prepared.

**Also known as:** Launch strategy, go-to-market strategy

**Related:** product-market fit, positioning, launch tiers

---

## J

### job-to-be-done (JTBD)

**Definition:** A framework for understanding why people use products, rooted in the insight that people "hire" products and services to accomplish specific goals (jobs) in their lives. Instead of asking "what features do users want?", JTBD asks "what job is the user trying to get done?" The job is defined in terms of progress the user wants to make, not in terms of the product they use.

**Also known as:** Jobs to be done, JTBD framework

**Related:** user research, problem framing, discovery

**Example:**
The job "help me feel productive and in control of my work week" explains why people use both to-do apps and calendar apps — the products are different but hired for the same underlying job. This insight is more useful for product decisions than "users want better task management."

---

## M

### minimum viable product (MVP)

**Definition:** The smallest version of a product or feature that delivers enough value to real users that you can learn whether your core assumption is correct. An MVP is not a half-finished product — it is a complete, intentional test of a specific hypothesis. The goal is to learn, not to ship as little work as possible.

**Also known as:** MVP

**Related:** product discovery, validated learning, lean startup

**Example:**
Dropbox's MVP was a demo video — not working software — that tested whether people would want a file sync product. The 70,000 signups from the video validated the demand hypothesis before any real product was built.

---

### north star metric

**Definition:** The single metric that best captures the core value a product delivers to users and that, if improved, indicates the product is succeeding in its mission. The North Star metric is not a revenue or business metric — it is a user-value metric that predicts long-term business health. Teams make prioritization decisions partly based on whether work will move this metric.

**Also known as:** NSM, North Star

**Related:** OKR, success metrics, product strategy

**Example:**
Spotify's North Star metric is "time spent listening." Airbnb's is "nights booked." Slack's was "messages sent per user per day." Each one captures user engagement in a way that predicts retention and business growth.

---

## O

### OKR (Objectives and Key Results)

**Definition:** A goal-setting framework where an Objective is a qualitative statement of what you want to achieve, and Key Results are the 2–5 measurable outcomes that tell you whether you've achieved it. OKRs operate at a company, team, and individual level. They were developed at Intel by Andy Grove and popularized at Google.

**Also known as:** Objectives and Key Results

**Related:** north star metric, product strategy, roadmap

**Example:**

```text
Objective: Dramatically improve new user activation
  KR1: Increase users completing core action within 7 days from 23% → 40%
  KR2: Reduce median time-to-first-value from 4 days → 1 day
  KR3: Achieve NPS ≥ 45 from users in their first 30 days
```

---

## P

### product discovery

**Definition:** The ongoing process of learning what product to build — validating that the problem is real and worth solving, that users want the solution you're considering, that the solution is technically feasible, and that it fits within the business model. Discovery work reduces risk before investment in delivery. It includes user interviews, prototypes, experiments, and data analysis.

**Also known as:** Discovery, product research

**Related:** discovery vs. delivery, continuous discovery habits, MVP

---

### product-market fit

**Definition:** The state in which a product satisfies a strong market demand — users love it, tell others about it, and would be genuinely upset if it went away. Product-market fit is not a binary state; it's a spectrum. Sean Ellis's test ("how disappointed would you be if this product no longer existed?") is one common proxy — ≥40% responding "very disappointed" indicates fit.

**Also known as:** PMF

**Related:** go-to-market, north star metric, product strategy

---

## R

### roadmap

**Definition:** A communication artifact that expresses a product team's current thinking about what they will work on and why, over some time horizon. A roadmap is not a promise — it is a best-current-view that changes as new information arrives. The best roadmaps communicate outcomes (what problems will be solved) rather than outputs (which features will be shipped).

**Also known as:** Product roadmap, strategic roadmap

**Related:** backlog, OKR, prioritization, epics

**Example:**
An outcome-based roadmap might have three columns: Now (current sprint focus), Next (next 1–2 quarters), Later (future quarters). Each item describes an outcome ("reduce checkout abandonment") rather than a feature ("redesign payment step").

---

## S

### sprint

**Definition:** A fixed-length period (typically 1–2 weeks) during which a Scrum team commits to completing a specific set of work. At the end of each sprint, the team has a potentially shippable increment of the product and conducts a retrospective to improve their process.

**Also known as:** Iteration (in Kanban or non-Scrum Agile contexts)

**Related:** backlog, user story, agile, scrum

---

## U

### UX (User Experience)

**Definition:** The overall experience a person has when interacting with a product or service — including how easy it is to use, how it makes them feel, whether it meets their needs, and whether they can accomplish their goals efficiently. UX design is the discipline of intentionally designing this experience.

**Also known as:** User experience design, UX design

**Related:** product discovery, wireframing, design thinking, user research

---

### user story

**Definition:** A short, user-centered description of a piece of functionality written in the format: "As a [type of user], I want [to do something] so that [I can achieve a goal]." User stories are placeholders for a conversation between the PM, designer, and engineer — not a complete specification. They are accompanied by acceptance criteria.

**Also known as:** Story

**Related:** backlog, acceptance criteria, epics, sprint

**Example:**

```text
As a job seeker, I want to save a job listing so that I can review it later before deciding to apply.

Acceptance criteria:
- Saved jobs appear in a dedicated "Saved Jobs" list
- User can unsave a job from either the listing or the saved jobs list
- Saved jobs persist across sessions (survive logout/login)
```

---

## Glossary Stats

| Metric | Count |
|--------|-------|
| Total terms defined | 15 |
| Terms pending definition | 0 |
| Last updated | 2026-06-09 |
