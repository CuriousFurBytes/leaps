# Module 03: Design Research and Interviewing

> Plan ethical discovery research, conduct useful interviews, and synthesize evidence without overclaiming.

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

Design research helps teams understand behavior, context, motivation, constraints, and meaning. Interviews are one common method, but they are often misused as opinion collection or feature validation theater. This module teaches interviews as evidence-gathering conversations grounded in real past behavior, not as sales pitches for an idea.

The roots of this work include anthropology, ergonomics, participatory design, usability testing, and human-computer interaction. The enduring lesson is simple: people are experts in their own experience, but not always accurate predictors of future behavior. A PM or designer must listen deeply, ask about concrete situations, protect participants, and avoid pretending that a few conversations prove more than they do.

## Prerequisites

- Module 01: Product Thinking and the PM Role in this topic.
- Module 02: Customer Problems and Outcomes in this topic.
- Comfort writing open-ended questions and handling ambiguity.
- Awareness of privacy and consent concerns from [[security-privacy-pentesting]] is useful.

## Objectives

By the end of this module, you will be able to:

- Choose interviews when they fit the discovery risk and avoid them when they do not.
- Write a research plan with participants, questions, consent, and synthesis steps.
- Conduct interviews that focus on past behavior rather than leading opinions.
- Synthesize notes into patterns, confidence levels, and decisions.

## Theory

### Interviews Reveal Context, Not Market Size

Interviews are strongest when the team needs to understand how people experience a workflow, why they make tradeoffs, what language they use, and where existing alternatives fail. They are weak for estimating market size or predicting exact adoption. A participant saying "I would use that" is not the same as behavior under real cost, time pressure, social pressure, or switching friction.

```yaml
research_goal:
  good_fit: "Understand how recruiters recover from missed candidate follow-ups"
  weak_fit: "Prove 40% of the market will buy our premium plan"
  better_for_market_size: "survey, analytics, sales data, or market research"
```

### Good Questions Anchor on Real Events

Useful interviews ask about the last time a participant encountered the situation. They avoid pitching a feature and asking for approval. The interviewer wants stories: sequence, tools, constraints, emotions, workarounds, consequences, and alternatives. Follow-up questions such as "What happened next?" and "Can you show me?" often produce better evidence than clever prepared questions.

```markdown
# Interview Prompt Pattern
Tell me about the last time you had to [do the job].
What triggered it?
What did you do first?
Where did it slow down or go wrong?
What did you try instead?
What happened because of that?
```

### Ethics and Consent Are Part of Research Quality

Discovery is not neutral extraction. Participants deserve clarity about why they are being asked questions, how notes will be used, whether recordings are optional, and what information they should not disclose. Ethical research also avoids manipulative framing, protects vulnerable groups, and considers who might be harmed if a product decision is made from biased evidence. Privacy and safety are product concerns, not legal afterthoughts.

```bash
cat <<'EOF' > consent-script.md
We are learning about your current workflow, not testing you.
You can skip any question or stop at any time.
Please do not share confidential customer, patient, or employer data.
We will summarize themes, not attribute quotes without permission.
EOF
```

### Synthesis Turns Notes Into Decisions

Synthesis is the bridge from research to product judgment. Raw notes are observations. Themes are interpretations across observations. Recommendations are decisions that include confidence and risk. Good synthesis preserves traceability: a stakeholder should be able to see which observations support a theme and which assumptions remain unresolved. This protects the team from cherry-picking only the quotes that favor a preferred solution.

```csv
observation,theme,decision_impact
"Three recruiters check the same filters every morning","repeated workflow","supports saved-search opportunity"
"Two recruiters delegate this to coordinators","role variation","segment by team structure"
"One recruiter said alerts feel noisy","notification risk","prototype alert controls before build"
```

## Key Concepts

- **Research plan:** A short document naming the learning goal, participant criteria, method, script, consent plan, and synthesis approach.
- **Leading question:** A question that pushes the participant toward the answer the team wants. It weakens evidence because it measures compliance or politeness.
- **Past behavior:** Concrete actions that already happened. Past behavior is usually stronger evidence than future intent.
- **Synthesis:** The process of organizing observations into patterns, implications, and decisions. It should keep observations separate from interpretations.
- **Research ethics:** The obligations to protect participants, avoid deception, respect privacy, and represent findings honestly.

## Examples

### Scenario: Interview Script for Missed Follow-Ups

```markdown
# Research Goal
Understand how recruiters notice and recover from missed candidate follow-ups.

# Opening
We are studying current workflows. We are not evaluating your performance.

# Core Questions
- Tell me about the last time a follow-up slipped.
- How did you notice?
- What tools did you check?
- What did you do next?
- What was the consequence?
```

This script stays close to real events and avoids asking whether the participant wants a specific feature.

## Common Pitfalls

### Mistake 1: Asking for Feature Approval

```markdown
Wrong: "Would you use saved-search alerts if we built them?"
```

```markdown
Correct: "Tell me about the last time you repeated the same search. What triggered it?"
```

The wrong question invites politeness and speculation. The correct question surfaces actual behavior.

### Mistake 2: Treating Quotes as Proof

```yaml
wrong:
  evidence: "One user said this would be amazing"
```

```yaml
correct:
  evidence: "Four of six participants described repeated manual checks in weekly workflows"
```

Quotes illustrate patterns; they do not replace pattern analysis.

### Mistake 3: Hiding Contradictory Evidence

```csv
wrong_synthesis,problem
"All users need alerts","ignores two participants who delegate the work"
```

```csv
better_synthesis,reason
"Alerts may help hands-on recruiters, but delegated workflows need team visibility","preserves segmentation"
```

Contradictions often reveal segmentation or constraints. They should refine the opportunity, not be erased.

## Cross-Links

- [[security-privacy-pentesting]]
- [[ai-ml]]
- [[css]]

## Summary

- Interviews are best for context, behavior, motivation, and workflow understanding.
- Strong interview questions focus on real past events rather than future feature approval.
- Consent, privacy, and participant protection are part of research quality.
- Synthesis separates observations, themes, implications, and recommendations.
- Good research can reduce uncertainty without pretending to prove everything.
