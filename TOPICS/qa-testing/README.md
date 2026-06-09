# QA and Testing

![Status](https://img.shields.io/badge/status-in--progress-yellow)
![Modules Completed](https://img.shields.io/badge/modules-0%2F12-lightgrey)
![Last Updated](https://img.shields.io/badge/updated-2026--06--09-blue)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner%20%E2%86%92%20Expert-blue)

> The discipline of verifying software correctness, building quality into the development process, and giving teams the confidence to ship.

> [!NOTE]
> **Topic Overview**
> QA and Testing is the practice of systematically verifying that software behaves as intended, catching defects early, and maintaining quality across a codebase's entire lifetime. This topic spans the full range from writing your first unit test to designing a company-wide QA strategy, covering unit testing, integration testing, end-to-end testing, test-driven development, BDD, performance testing, and accessibility testing.
>
> This topic is organized into progressive modules, each building on the last.
> Work through them in order unless you already have relevant prior experience —
> use the [Difficulty & Time Estimate](#difficulty--time-estimate) section and
> the [Prerequisites](#prerequisites) section to decide where to begin.

---

## Table of Contents

- [Overview](#overview)
- [Historical Context](#historical-context)
- [Real-World Applications](#real-world-applications)
- [Learning Objectives](#learning-objectives)
- [Difficulty & Time Estimate](#difficulty--time-estimate)
- [Prerequisites](#prerequisites)
- [Learning Modules](#learning-modules)
- [Progress](#progress)
- [Milestones](#milestones)
- [Test Scores](#test-scores)
- [Projects](#projects)
- [Resources](#resources)
- [Related Topics](#related-topics)
- [Learning Journal](#learning-journal)
- [AI Metadata](#ai-metadata)

---

## Overview

Software testing is the practice of executing a program with the intent of finding defects. Quality assurance is the broader discipline: the processes, culture, tools, and strategies that prevent defects from reaching users in the first place. The two are intimately connected — testing is the primary mechanism by which QA is practiced, but QA thinking shapes how we write code, design systems, and organize teams long before a single test runs.

The central insight of modern QA is that quality cannot be tested into a product after it is built. It must be built in from the start. A team that writes its tests after the code is complete will find tests that validate the code that was written, not the behavior that was required. A team that practices test-driven development (TDD) writes code that is testable by design, catches misunderstandings about requirements before they become bugs, and produces a suite of tests that serve as living documentation of the system's behavior.

### Why It Matters

Bugs found in production are dramatically more expensive to fix than bugs found during development. Barry Boehm's research, extended by subsequent industry studies, established the principle that defects found late in the lifecycle cost orders of magnitude more to fix than defects found early. The compounding effect is not just monetary — a production bug erodes user trust, requires emergency response, and often introduces regression risk when the fix is rushed.

Beyond cost, testing is a form of communication. A well-written test suite tells future developers (including your future self) exactly what the code is supposed to do. When requirements change, the failing tests pinpoint which behaviors have been affected. When a refactoring goes wrong, the test suite is the first line of defense.

Understanding QA and Testing is valuable because:

- It underpins continuous delivery — the practice of shipping code to production multiple times per day with confidence
- It develops the mental model for "correctness as a property of a system," transferable to formal verification, type systems, and design by contract
- Proficiency in it is expected in roles such as software engineer, QA engineer, DevOps engineer, and senior/staff engineer — effectively every technical role

### Key Features of This Topic

- **The Testing Pyramid** — A mental model for balancing unit, integration, and end-to-end tests by cost, speed, and confidence
- **Test-Driven Development** — A development methodology where tests are written before code, driving design and documentation simultaneously
- **Shift-Left Testing** — The practice of moving testing earlier in the development lifecycle to reduce the cost of defects
- **Modern E2E Tooling** — Playwright, Cypress, and their predecessors enable reliable browser automation at scale in CI/CD pipelines

---

## Historical Context

Software testing as a discipline emerged alongside software itself. In the 1950s, NASA and early computing pioneers had to devise ways to verify that their programs — which ran on machines worth millions of dollars — produced correct results. The first "test cases" were manual: engineers would trace through program logic by hand or compare outputs against known-good calculations.

The field gained theoretical grounding in 1969 when Edsger W. Dijkstra wrote that "program testing can be used to show the presence of bugs, but never to show their absence." This statement defined the fundamental limitation of testing: no finite set of tests can prove a program correct for all possible inputs. Testing is probabilistic evidence, not proof. This insight shaped the entire discipline: rather than seeking certainty, practitioners design test suites that maximize the probability of detecting defects while remaining economically feasible to maintain.

The Agile movement of the late 1990s and early 2000s fundamentally changed testing culture. Rather than a separate QA phase at the end of the waterfall, Agile demanded continuous testing integrated into each iteration. Kent Beck introduced Test-Driven Development (TDD) in 1999 as part of Extreme Programming, articulating the red/green/refactor cycle that remains the canonical TDD workflow. The JUnit framework (Beck and Gamma, 1997) made automated unit testing practical for Java developers and spawned the xUnit family of frameworks that now covers every major language.

Dan North extended TDD into Behavior-Driven Development (BDD) in 2006, addressing a common critique of TDD: that developers writing tests for their own code tend to test what they built rather than what was required. BDD introduced Gherkin syntax — a human-readable, stakeholder-accessible language for expressing test scenarios — and tools like Cucumber (2008) to execute those scenarios as tests.

Browser automation has a parallel history. Selenium was created in 2004 by Jason Huggins at ThoughtWorks to automate web application testing; it became the dominant tool for end-to-end browser testing for over a decade. Cypress was released in 2014 with a fundamentally different architecture (running inside the browser rather than through WebDriver), and Playwright was released by Microsoft in 2020 with support for all major browsers and a modern async API.

### Timeline

| Year | Event |
|------|-------|
| 1950s | NASA and early computer labs develop manual test case methodology |
| 1969 | Edsger Dijkstra states that testing can show bugs but not their absence |
| 1997 | JUnit created by Kent Beck and Erich Gamma; xUnit era begins |
| 1999 | Kent Beck introduces TDD as part of Extreme Programming |
| 2004 | Selenium released by Jason Huggins at ThoughtWorks |
| 2006 | Dan North introduces Behavior-Driven Development (BDD) and Gherkin |
| 2008 | Cucumber released, making BDD executable |
| 2014 | Cypress released with in-browser architecture |
| 2020 | Playwright released by Microsoft with cross-browser support |
| Today | Testing is integral to CI/CD; shift-left and DevOps testing culture mainstream |

---

## Real-World Applications

QA and Testing practices are used across every segment of software development:

- **Web Applications** — End-to-end Playwright/Cypress tests validate critical user journeys (checkout, login, onboarding) against every deployment
- **APIs and Microservices** — Contract testing with Pact ensures that services in a distributed system remain compatible across independent deployments
- **Mobile Applications** — Device farms run automated UI tests against hundreds of device/OS combinations before each release
- **Financial Systems** — Rigorous integration and regression test suites protect against calculation errors in systems where defects have legal and financial consequences
- **Safety-Critical Systems** — Aerospace, medical devices, and automotive software require formal verification methods alongside traditional testing, with certifying bodies mandating test coverage levels
- **Open Source Libraries** — Projects like React, Django, and Rust's standard library maintain comprehensive test suites as the primary mechanism for accepting contributions safely

---

## Learning Objectives

By completing this topic in full, you will be able to:

1. Explain the testing pyramid and select the appropriate type of test for any given scenario
2. Write effective unit tests in Python (pytest) and JavaScript (Jest) that are fast, isolated, and meaningful
3. Design and implement integration tests that verify behavior across component boundaries using real or simulated dependencies
4. Build end-to-end test suites with Playwright, applying the page object model and sound locator strategies
5. Practice test-driven development, writing failing tests before implementation code and applying the red/green/refactor cycle
6. Mock, stub, and spy on dependencies using unittest.mock (Python) and Jest mocks (JavaScript) without over-mocking
7. Test REST APIs with contract testing (Pact) and validate responses against OpenAPI specifications
8. Design a QA strategy for a real application, including test plan, risk prioritization, CI/CD integration, and quality metrics
9. Measure and interpret code coverage, mutation test scores, and defect escape rates to assess test suite quality
10. Integrate testing at all levels into a CI/CD pipeline with appropriate parallelization and quality gates

---

## Difficulty & Time Estimate

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Beginner → Expert |
| **Estimated Total Hours** | 50–70 hours |
| **Prerequisites** | Basic programming in Python or JavaScript, familiarity with software development |
| **Recommended Pace** | 4–5 hours/week |
| **Topic Type** | Computational (code examples in Python, JavaScript, shell) |
| **Suitable For** | Junior developers building QA skills, experienced developers formalizing testing practices, QA engineers transitioning to automated testing |

---

## Prerequisites

Before starting this topic, you should have a working understanding of:

- Basic programming in Python or JavaScript — specifically: functions, control flow, and data structures; you do not need to be an expert
- Software development lifecycle — specifically: what it means to write, run, and debug a program; familiarity with version control (git) is helpful
- Command-line basics — specifically: running commands in a terminal, installing packages with pip or npm

> [!TIP]
> Not sure if you're ready? Attempt Module 01 and gauge how it feels.
> If the terminology is entirely foreign, revisit the prerequisites above first.
> If you can follow along but things feel shaky, press on — it will solidify.

---

## Learning Modules

| # | Module | Difficulty | Status | Score |
|---|--------|-----------|--------|-------|
| 01 | [Introduction to QA and Testing](./modules/01_introduction/) | Beginner | - [ ] | —/— |
| 02 | [Unit Testing](./modules/02_unit-testing/) | Beginner | - [ ] | —/— |
| 03 | [Mocking and Test Doubles](./modules/03_mocking-and-test-doubles/) | Beginner–Intermediate | - [ ] | —/— |
| 04 | [Integration Testing](./modules/04_integration-testing/) | Intermediate | - [ ] | —/— |
| 05 | [End-to-End Testing](./modules/05_e2e-testing/) | Intermediate | - [ ] | —/— |
| 06 | [API Testing and Contract Testing](./modules/06_api-testing/) | Intermediate | - [ ] | —/— |
| 07 | [Test-Driven Development](./modules/07_test-driven-development/) | Intermediate–Advanced | - [ ] | —/— |
| 08 | [Behavior-Driven Development](./modules/08_behavior-driven-development/) | Intermediate–Advanced | - [ ] | —/— |
| 09 | [Performance Testing](./modules/09_performance-testing/) | Advanced | - [ ] | —/— |
| 10 | [Accessibility Testing](./modules/10_accessibility-testing/) | Advanced | - [ ] | —/— |
| 11 | [QA Strategy and Metrics](./modules/11_qa-strategy-and-metrics/) | Expert | - [ ] | —/— |
| 12 | [Capstone Project](./modules/12_capstone-project/) | Expert | - [ ] | —/— |

**Status key:** ` ` Not started &nbsp;·&nbsp; `~` In progress &nbsp;·&nbsp; `x` Complete

---

## Progress

### Overall Progress

```
[░░░░░░░░░░░░░░░░░░░░] 0 / 12 modules complete (0%)
```

_Update this bar as you complete modules. Each block = 5% of total modules._

```
Legend:  ░ = not started   ▒ = in progress   █ = complete
Example: [██████░░░░░░░░░░░░░░] 6 / 12 modules (50%)
```

### Point Tracker

| Category | Earned | Possible | Percentage |
|----------|--------|----------|------------|
| Module Tests | 0 | 444 | 0% |
| Exercises | 0 | 120 | 0% |
| Projects | 0 | 60 | 0% |
| Bonus | 0 | — | — |
| **Total** | **0** | **624** | **0%** |

---

## Milestones

- [ ] **First Step** — Complete Module 01 (Introduction to QA and Testing)
- [ ] **Foundation Built** — Complete Modules 01–03 with ≥ 70% on each test
- [ ] **Halfway There** — Complete 6 of 12 modules
- [ ] **Core Mastery** — Score ≥ 80% on all core module tests
- [ ] **First Project Shipped** — Write a complete test suite for a real function library
- [ ] **Topic Complete** — All 12 modules finished
- [ ] **Deep Work** — Complete the Capstone Project with all four test tiers
- [ ] **TDD Practitioner** — Complete Module 07 with ≥ 90% and submit a TDD kata solution
- [ ] **Full Stack QA** — Complete Modules 05 and 06 demonstrating E2E and contract tests

---

## Test Scores

_Append a row after each test attempt. Do not overwrite previous attempts._

| Module | Date | Score | Grade | Notes |
|--------|------|-------|-------|-------|
| — | — | —/— | — | Not started |

**Grade scale:** A ≥ 90% &nbsp;·&nbsp; B ≥ 80% &nbsp;·&nbsp; C ≥ 70% &nbsp;·&nbsp; D ≥ 60% &nbsp;·&nbsp; F < 60%

---

## Projects

See [PROJECTS.md](./PROJECTS.md) for project ideas ranging from beginner to expert.

**My Projects:**

| Project Name | Difficulty | Started | Status | Link |
|-------------|------------|---------|--------|------|
| — | — | — | — | — |

---

## Resources

See [RESOURCES.md](./RESOURCES.md) for a curated and verified list of books, courses, videos, and tools.

**Top picks so far** _(fill in as you study)_:

1. _To be filled in_
2. _To be filled in_
3. _To be filled in_

---

## Related Topics

Topics that complement, extend, or are required for QA and Testing:

- [[django-fastapi-flask]] — Web frameworks where integration and E2E testing patterns are applied; the testing module in that topic builds directly on this one
- [[javascript-typescript-react]] — Jest, React Testing Library, and Playwright are all central to frontend testing; the TypeScript type system reduces whole categories of bugs
- [[devops-platform-engineering]] — CI/CD pipelines are the infrastructure that runs your tests automatically; quality gates and test parallelization are DevOps concerns
- [[feature-flags-monitoring]] — Feature flags enable safe progressive rollout and A/B testing; monitoring provides the production-side feedback loop that testing cannot fully replace

See also the [ROADMAP.md](./ROADMAP.md) for how this topic fits into broader learning paths.

---

## Learning Journal

_Date-stamp each entry. Write honestly — confusion documented now becomes insight later._
_Newest entries at the top._

---

### 2026-06-09 — Started Topic

**What I did today:**
- Read the topic overview and ROADMAP.md
- Reviewed the testing pyramid and historical context
- Set up Python with pytest and Node.js with Jest

**What clicked:**
- _Write one thing that made sense immediately_

**What's still unclear:**
- _Write your first open question — then add it to QUESTIONS.md_

**How I feel about this topic:**
- _Honest assessment: excited / intimidated / curious / confused / etc._

---

_Add new journal entries above this line, newest first._

---

## AI Metadata

```yaml
# Maintained by LEAPS tooling — manual edits will be overwritten on next sync
last_ai_expansion: "2026-06-09"
topic_slug: "qa-testing"
topic_name: "QA and Testing"
module_count: 12
modules_complete: 0
total_points_earned: 0
total_points_possible: 624
completion_percentage: 0
difficulty: "Beginner → Expert"
estimated_hours: 60
prerequisites:
  - "basic-programming"
  - "software-development-lifecycle"
related_topics:
  - "django-fastapi-flask"
  - "javascript-typescript-react"
  - "devops-platform-engineering"
  - "feature-flags-monitoring"
tags:
  - "testing"
  - "quality-assurance"
  - "pytest"
  - "jest"
  - "playwright"
  - "tdd"
  - "bdd"
creator: "Multiple contributors — Kent Beck (TDD), Dan North (BDD), Jason Huggins (Selenium)"
year_created: "1950s–present"
```
