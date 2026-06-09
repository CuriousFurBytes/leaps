# Module 01: Product Thinking and the PM Role

> Learn what product management is, how design and discovery fit, and how good PMs turn ambiguity into responsible decisions.

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

Product management, design, and discovery are often confused because they meet in the same messy place: deciding what should exist next. Product management is accountable for outcomes and tradeoffs, design makes user needs and possible futures tangible, and discovery is the learning system that reduces uncertainty before delivery. This module establishes the mental model for that work.

The beginner mistake is to think a product manager is a feature writer, meeting scheduler, or miniature CEO. In healthy teams, the PM is a decision catalyst. They create clarity about customers, problems, goals, constraints, and evidence so that designers, engineers, researchers, data partners, sales, support, and leaders can make better choices together.

## Prerequisites

- None. This is the first module in the topic.
- Ability to read plain-language business documents and discuss tradeoffs respectfully.
- Curiosity about how software and service teams collaborate; [[distributed-systems-architecture]] is useful later but not required now.

## Objectives

By the end of this module, you will be able to:

- Explain how product management, design, and discovery differ and reinforce each other.
- Convert a feature request into a problem, outcome, assumption, and learning step.
- Identify common product risks before a team commits to delivery.
- Use lightweight artifacts to communicate product reasoning.

## Theory

### Product Work Starts With Uncertainty

Modern product work inherited ideas from brand management, industrial design, usability research, agile delivery, and Lean Startup experimentation. Each tradition reacted to a different failure mode: companies building for internal politics, teams ignoring human behavior, projects discovering usability problems too late, and organizations measuring output instead of impact. Discovery exists because most product ideas are partly wrong at the start. The responsible response is not paralysis; it is structured learning.

```yaml
feature_request:
  request: "Add saved searches"
  possible_customer_problem: "Recruiters repeat the same filtered search every morning"
  desired_outcome: "Reduce repeated setup time and missed candidate checks"
  riskiest_assumption: "The repeated search is frequent enough to justify workflow changes"
```

### The PM Role Is About Outcomes, Not Authority

A PM rarely has direct authority over engineering, design, research, sales, or support, yet must help those groups converge. That is why good PMs rely on context, evidence, and trust more than command. They keep strategy connected to user reality, convert ambiguity into options, and make tradeoffs visible. A PM should not replace designers, researchers, or engineers; they should improve the conditions in which those specialists make decisions.

```markdown
# Product Decision Note
Customer: Hiring teams at companies with 50-300 employees
Problem: Recruiters repeat high-signal searches manually
Outcome: Fewer missed candidate reviews per week
Team bet: Test saved search alerts before building full automation
```

### Discovery Connects Problem, Solution, and Delivery Risk

Product risk is not one thing. Value risk asks whether customers care. Usability risk asks whether people can use the solution. Feasibility risk asks whether the team can build and operate it. Viability risk asks whether it works for the business, legal, support, and go-to-market model. Discovery chooses methods that match the risk rather than running interviews, surveys, or prototypes by habit.

```csv
risk,type,learning_method
"Users do not repeat searches often",value,"behavioral interviews and usage logs"
"Users cannot understand alert controls",usability,"low-fidelity prototype test"
"Alerts are expensive to compute",feasibility,"engineering spike"
"Alerts create compliance issues",viability,"legal and privacy review"
```

### Design Makes Ideas Critiquable

Design is not decoration at the end of product work. Sketches, journey maps, wireframes, service blueprints, and prototypes allow teams to see assumptions. When an idea is visible, customers can react to situations, engineers can spot constraints, and stakeholders can debate tradeoffs. The artifact is a thinking tool, not proof by itself.

```bash
cat <<'EOF' > discovery-checklist.md
- What customer behavior did we observe?
- What assumption changed because of evidence?
- What risk remains before delivery?
- What decision do we need now?
EOF
```

## Key Concepts

- **Product outcome:** A measurable change in customer, user, or business behavior. Outcomes are stronger than output lists because they explain why a feature matters.
- **Discovery:** The structured work of reducing product uncertainty before or during delivery. It includes research, analysis, prototyping, experiments, and stakeholder learning.
- **Product risk:** A reason an idea might fail even if the team builds it correctly. Value, usability, feasibility, and viability risks need different learning methods.
- **Stakeholder alignment:** Shared understanding of the problem, constraints, evidence, and decision. Alignment is not universal agreement; it is clarity about the tradeoff being made.
- **Opportunity:** A customer problem, need, or desire that could support a valuable product bet. Good opportunities are specific enough to investigate.

## Examples

### Scenario: Turning a Sales Request Into Discovery

A sales teammate asks for "enterprise dashboards." The PM asks what deal risk or customer workflow is behind the request.

```yaml
input: "Enterprise dashboards"
reframed:
  customer: "Operations directors at multi-site clinics"
  problem: "Cannot compare appointment backlogs across locations"
  outcome: "Identify overloaded clinics before patients churn"
  next_step: "Interview three directors and review support tickets"
```

The tradeoff is speed versus confidence. A PM can acknowledge urgency while still asking for enough evidence to avoid building the wrong dashboard.

## Common Pitfalls

### Mistake 1: Treating a Feature Request as the Problem

```yaml
wrong:
  problem: "Build saved searches"
```

```yaml
correct:
  problem: "Recruiters repeat the same search and miss late-arriving candidates"
```

The wrong version hides the customer struggle. The correct version lets the team compare multiple solutions.

### Mistake 2: Running One Favorite Discovery Method for Every Risk

```csv
wrong_risk,wrong_method
"Can we operate this at scale?","Customer interviews"
```

```csv
correct_risk,better_method
"Can we operate this at scale?","Engineering spike and production cost model"
```

Interviews are powerful for behavior and motivation, but they cannot answer every feasibility or operational question.

### Mistake 3: Confusing Alignment With Approval

```markdown
Wrong: "Everyone liked the idea in the meeting."
```

```markdown
Correct: "Everyone understands the risk, owner, decision date, and fallback option."
```

Approval can be shallow. Alignment requires shared context and explicit tradeoffs.

## Cross-Links

- [[distributed-systems-architecture]]
- [[javascript-typescript-react]]
- [[security-privacy-pentesting]]

## Summary

- Product management, design, and discovery are complementary decision disciplines.
- PMs are accountable for clarity about outcomes and tradeoffs, not unilateral command.
- Discovery reduces value, usability, feasibility, and viability risk.
- Design artifacts make assumptions visible enough to critique.
- Good product work starts with customer problems and evidence before feature commitment.
