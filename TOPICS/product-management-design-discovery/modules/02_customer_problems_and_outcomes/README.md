# Module 02: Customer Problems and Outcomes

> Define customers, problems, outcomes, and success measures before jumping to features.

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

## Overview

Product teams create leverage when they can name the right customer problem with enough precision that many possible solutions can be compared. This module moves from role clarity into opportunity clarity. It teaches how to distinguish users, buyers, customers, stakeholders, jobs, pains, gains, business outcomes, product outcomes, and leading indicators.

Historically, product teams have swung between two incomplete habits: shipping stakeholder-requested features and optimizing narrow metrics without understanding human context. Human-centered design pushed teams toward empathy and observation; outcome-driven product practice pushed teams toward measurable behavior change. Mature discovery combines both: the team describes a real human struggle and defines what should improve if the product response works.

## Prerequisites

- Module 01: Product Thinking and the PM Role in this topic.
- Ability to identify a product or service you use and describe who benefits from it.
- Basic awareness that implementation constraints from [[distributed-systems-architecture]] can affect which outcomes are practical.

## Objectives

By the end of this module, you will be able to:

- Separate customer segments, user roles, buyers, and affected stakeholders.
- Write problem statements that are observable, specific, and solution-neutral.
- Define outcomes and indicators that reveal whether the problem is improving.
- Detect weak metrics, vanity metrics, and misleading success claims.

## Theory

### Customers Are Not a Single Blob

A product may have users, buyers, approvers, administrators, support teams, regulators, and people indirectly affected by a workflow. Discovery suffers when a team says "the customer" without naming which actor is being studied. In B2B products, the economic buyer may care about cost and risk while the daily user cares about speed and fewer errors. In consumer products, the user and buyer may be the same person, but there may still be caregivers, moderators, or communities affected by the design.

```yaml
actors:
  daily_user: "clinic receptionist scheduling appointments"
  buyer: "operations director controlling software budget"
  affected_party: "patient waiting for an appointment"
  support_team: "internal staff resolving scheduling mistakes"
```

### Problem Statements Should Describe Evidence, Not Wishes

A strong problem statement names who struggles, in what situation, what they are trying to accomplish, what blocks them, and why it matters. It should not smuggle in the solution. The statement "users need export to spreadsheet" is often a proposed solution. The underlying problem might be that managers cannot combine product data with finance data during weekly reporting. That problem might be solved by exports, integrations, better dashboards, or changes to the reporting workflow.

```markdown
# Problem Statement Pattern
When [specific actor] is [specific situation], they struggle to [job or goal]
because [observable constraint], causing [impact].
```

### Outcomes Translate Problems Into Change

Outcomes are measurable changes in behavior or conditions. They differ from outputs, which are things the team ships. "Launch saved searches" is output; "reduce repeated search setup time by 50% for weekly active recruiters" is an outcome. Outcomes create focus, but they can be harmful if chosen carelessly. A metric can improve while user trust, accessibility, or long-term retention worsens, so PMs must pair quantitative indicators with qualitative understanding and guardrails.

```csv
output,outcome,guardrail
"saved search alerts","fewer repeated manual searches","unsubscribe rate does not spike"
"bulk edit","less time correcting records","error recovery remains clear"
"AI summary","faster case triage","sensitive data is not exposed"
```

### Good Opportunity Framing Enables Better Tradeoffs

Once the customer, problem, and outcome are clear, the team can compare options. They can ask which solution addresses the problem fastest, which creates new risks, and which aligns with strategy. This is where product management connects discovery to design and delivery. The frame does not remove judgment; it makes judgment explicit enough to inspect.

```bash
cat <<'EOF' > opportunity.md
Customer: Operations directors at multi-site clinics
Problem: They cannot spot appointment backlog differences until patients complain
Outcome: Detect high-risk locations earlier each week
Next evidence: Review support tickets and interview five directors
EOF
```

## Key Concepts

- **Customer segment:** A meaningful group with similar context, constraints, and reasons to care. Segments should be behaviorally useful, not just demographic labels.
- **User role:** The person who directly interacts with the product or service. A user may not be the buyer or the primary beneficiary.
- **Problem statement:** A solution-neutral description of a struggle in context. It should be specific enough to investigate and broad enough to allow multiple solutions.
- **Outcome:** A measurable change that indicates the problem is improving. Outcomes usually need leading indicators and guardrails.
- **Vanity metric:** A number that looks good but does not meaningfully prove progress toward the outcome. Page views, signups, or feature clicks can be vanity metrics when disconnected from value.

## Examples

### Scenario: From Export Request to Reporting Problem

```yaml
request: "Export dashboard data to CSV"
problem_frame:
  actor: "regional operations manager"
  situation: "preparing Monday staffing report"
  struggle: "cannot compare appointment volume with payroll spreadsheet"
  impact: "staffing decisions lag by a week"
  outcome: "reduce report preparation from 3 hours to 45 minutes"
```

This reframing keeps export as one option but allows the team to consider integrations, scheduled reports, or redesigned dashboards.

## Common Pitfalls

### Mistake 1: Defining the Customer Too Broadly

```yaml
wrong:
  customer: "everyone who uses the app"
```

```yaml
correct:
  customer: "first-time clinic receptionists scheduling follow-up appointments during peak morning hours"
```

Broad customers create vague discovery and weak prioritization. Specific segments reveal real constraints.

### Mistake 2: Measuring Only Output

```csv
wrong_metric,problem
"feature shipped","does not prove customer behavior improved"
```

```csv
better_metric,reason
"repeat setup time reduced","connects directly to the workflow pain"
```

Shipping is necessary for delivery, but not sufficient for product success.

### Mistake 3: Choosing a Metric That Encourages Harm

```yaml
wrong:
  metric: "increase notifications sent"
```

```yaml
correct:
  metric: "increase useful alerts acknowledged"
  guardrail: "complaints and opt-outs stay below baseline"
```

Metrics shape behavior. Guardrails protect trust, privacy, accessibility, and long-term quality.

## Cross-Links

- [[distributed-systems-architecture]]
- [[security-privacy-pentesting]]
- [[ai-ml]]

## Summary

- Customer problems must be specific, observable, and solution-neutral.
- Users, buyers, stakeholders, and affected parties may be different people.
- Outcomes describe behavior or condition changes, while outputs describe shipped work.
- Good metrics need guardrails to avoid local optimization and user harm.
- Opportunity framing gives teams a better basis for comparing product bets.
