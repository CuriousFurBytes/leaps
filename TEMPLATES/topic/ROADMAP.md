# {{TOPIC_NAME}} — Learning Roadmap

> This roadmap is your study plan. Work through the phases in order.
> Each phase builds directly on the previous one.
> Mark your current position with **← You Are Here** and update it as you progress.

---

## Prerequisites Map

Confirm you have working knowledge of these before entering Phase 1:

```
[[{{PREREQ_TOPIC_1}}]]  ──┐
                           ├──► {{TOPIC_NAME}}  (start here)
[[{{PREREQ_TOPIC_2}}]]  ──┘
```

If either prerequisite is missing, complete it first and return here.

---

## Learning Path Visualization

```mermaid
flowchart TD
    A([Prerequisites Met]) --> B

    subgraph P1["Phase 1: Foundation  •  Weeks 1–2"]
        B[Module 00: Introduction & Setup]
        B --> C[Module 01: {{MODULE_01_NAME}}]
        C --> D[Module 02: {{MODULE_02_NAME}}]
    end

    subgraph P2["Phase 2: Core Concepts  •  Weeks 3–5"]
        E[Module 03: {{MODULE_03_NAME}}]
        E --> F[Module 04: {{MODULE_04_NAME}}]
        F --> G[Module 05: {{MODULE_05_NAME}}]
    end

    subgraph P3["Phase 3: Applied Skills  •  Weeks 6–8"]
        H[Module 06: {{MODULE_06_NAME}}]
        H --> I[Module 07: {{MODULE_07_NAME}}]
        I --> J[Module 08: {{MODULE_08_NAME}}]
    end

    subgraph P4["Phase 4: Mastery  •  Weeks 9–12"]
        K[Capstone Project]
        K --> L[Topic Review & Weak-Spot Work]
        L --> M([Topic Complete ✓])
    end

    D --> E
    G --> H
    J --> K

    style A fill:#2a9d8f,color:#fff,stroke:none
    style M fill:#2a9d8f,color:#fff,stroke:none
    style P1 fill:#edf2fb,stroke:#8d99ae
    style P2 fill:#fef3c7,stroke:#d97706
    style P3 fill:#fee2e2,stroke:#dc2626
    style P4 fill:#dcfce7,stroke:#16a34a
```

---

## Phase Breakdown

### Phase 1: Foundation

**Goal:** Understand what {{TOPIC_NAME}} is, why it matters, and build comfort with
the core vocabulary and tooling. Leave Phase 1 able to describe the topic clearly.

| Module | Name | Est. Hours | Key Skill Gained |
|--------|------|-----------|-----------------|
| 00 | Introduction & Setup | {{H_00}} | Big-picture orientation; working environment |
| 01 | {{MODULE_01_NAME}} | {{H_01}} | {{SKILL_01}} |
| 02 | {{MODULE_02_NAME}} | {{H_02}} | {{SKILL_02}} |

**Phase 1 Exit Criteria:**

- [ ] Can explain {{TOPIC_NAME}} to a non-expert in 2 minutes without notes
- [ ] Development environment is set up and all tools are working
- [ ] Scored ≥ 70% on Module 01 and Module 02 tests
- [ ] Completed at least one Beginner-level project from PROJECTS.md
- [ ] GLOSSARY.md has at least 10 entries

**Milestone unlocked:** Foundation Built

---

### Phase 2: Core Concepts

**Goal:** Develop genuine fluency with the primary tools, patterns, and mental models.
Leave Phase 2 able to solve typical problems independently.

| Module | Name | Est. Hours | Key Skill Gained |
|--------|------|-----------|-----------------|
| 03 | {{MODULE_03_NAME}} | {{H_03}} | {{SKILL_03}} |
| 04 | {{MODULE_04_NAME}} | {{H_04}} | {{SKILL_04}} |
| 05 | {{MODULE_05_NAME}} | {{H_05}} | {{SKILL_05}} |

**Phase 2 Exit Criteria:**

- [ ] Can independently solve problems involving {{CORE_SKILL_1}} without referencing notes
- [ ] Can independently solve problems involving {{CORE_SKILL_2}} without referencing notes
- [ ] Scored ≥ 75% on all Phase 2 module tests
- [ ] Completed at least one Intermediate-level project from PROJECTS.md
- [ ] CHEATSHEET.md has entries for all Phase 2 patterns

**Milestone unlocked:** Core Mastery

---

### Phase 3: Applied Skills

**Goal:** Apply knowledge to realistic, complex problems. Combine concepts across modules.
Leave Phase 3 able to approach novel problems with confidence.

| Module | Name | Est. Hours | Key Skill Gained |
|--------|------|-----------|-----------------|
| 06 | {{MODULE_06_NAME}} | {{H_06}} | {{SKILL_06}} |
| 07 | {{MODULE_07_NAME}} | {{H_07}} | {{SKILL_07}} |
| 08 | {{MODULE_08_NAME}} | {{H_08}} | {{SKILL_08}} |

**Phase 3 Exit Criteria:**

- [ ] Completed a project combining concepts from at least 3 different modules
- [ ] Scored ≥ 80% on all Phase 3 module tests
- [ ] GLOSSARY.md is comprehensive — covers all terms you've encountered
- [ ] QUESTIONS.md open questions are mostly resolved (status: 🟢)

**Milestone unlocked:** Applied Practitioner

---

### Phase 4: Mastery

**Goal:** Synthesize everything. Build something substantial. Teach or document what you know.
Leave Phase 4 confident calling yourself proficient in {{TOPIC_NAME}}.

| Activity | Est. Hours | Description |
|----------|-----------|-------------|
| Capstone Project | {{H_CAPSTONE}} | A non-trivial project using all major concepts from the topic |
| Topic Review | {{H_REVIEW}} | Revisit modules where test scores were below 80% |
| Teaching Exercise | {{H_TEACH}} | Write a blog post, explain to someone else, or make a demo |
| Final Self-Assessment | {{H_FINAL}} | Retake weakest module tests; verify overall score ≥ 80% |

**Phase 4 Exit Criteria:**

- [ ] Capstone project complete and documented in PROJECTS.md
- [ ] Overall topic score ≥ 80% (see Test Scores in topic README)
- [ ] CHEATSHEET.md is complete and genuinely useful as a reference
- [ ] GLOSSARY.md has definitions for every term you encountered throughout the topic
- [ ] At least one teaching artifact exists (blog post, write-up, recorded explanation)

**Milestone unlocked:** Topic Mastery

---

## Time Estimates Summary

| Phase | Weeks | Est. Hours | Cumulative |
|-------|-------|-----------|------------|
| Phase 1: Foundation | 1–2 | {{P1_HOURS}} | {{P1_HOURS}} hrs |
| Phase 2: Core Concepts | 3–5 | {{P2_HOURS}} | {{P1_P2_HOURS}} hrs |
| Phase 3: Applied Skills | 6–8 | {{P3_HOURS}} | {{P1_P2_P3_HOURS}} hrs |
| Phase 4: Mastery | 9–12 | {{P4_HOURS}} | {{TOTAL_HOURS}} hrs |
| **Total** | **12** | **{{TOTAL_HOURS}} hrs** | |

> [!NOTE]
> These estimates assume roughly **{{HOURS_PER_WEEK}} focused hours per week**.
> If you're studying part-time, the calendar weeks will stretch accordingly.
> Adjust the schedule to fit your life — consistency matters more than pace.

---

## Milestone Definitions

| Milestone | Earned When | Point Threshold |
|-----------|------------|----------------|
| First Step | Module 00 complete | Any score |
| Foundation Built | Phase 1 complete, all tests ≥ 70% | {{P1_POINT_THRESHOLD}} pts |
| Core Mastery | Phase 2 complete, all tests ≥ 75% | {{P2_POINT_THRESHOLD}} pts |
| Applied Practitioner | Phase 3 complete, all tests ≥ 80% | {{P3_POINT_THRESHOLD}} pts |
| Topic Mastery | Phase 4 complete, capstone done, overall ≥ 80% | {{P4_POINT_THRESHOLD}} pts |
| {{CUSTOM_MILESTONE}} | {{CUSTOM_CRITERIA}} | — |

---

## Alternative Paths

### Fast Track (If You Have Prior Experience)

If you already have solid background in {{PREREQ_TOPIC_1}} and some exposure to {{TOPIC_NAME}}:

```
Skim Module 00 → Start at Module {{FAST_TRACK_START}} → Continue normally
```

Take the Module 00 test first. If you score ≥ 85%, skip to Module {{FAST_TRACK_START}}.

### Deep Dive Path (Maximum Understanding)

For maximum depth, add these supplementary activities between phases:

- **After Phase 1:** Read {{SUPPLEMENTARY_BOOK_1}}, Chapters 1–3
- **After Phase 2:** Complete {{SUPPLEMENTARY_COURSE_1}} (free on {{PLATFORM}})
- **After Phase 3:** Read the primary research papers listed in RESOURCES.md

### Project-First Path (Learn by Building)

If you learn best by doing rather than reading:

```
Module 00 → Beginner Project → Module 01 → Beginner Project → Module 02 → ...
```

Alternate one module of theory with one hands-on project at each step.

---

## You Are Here

> **Current Phase:** _Not started_
>
> **Current Module:** _None — begin at [Module 00](./modules/00-introduction/README.md)_
>
> **Last Completed Module:** _None_
>
> **Next Action:** Open Module 00 and read the Overview section.
>
> _Update this section each time you advance to a new module or phase._
