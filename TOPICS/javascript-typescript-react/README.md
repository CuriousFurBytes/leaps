# JavaScript, TypeScript and React

![Status](https://img.shields.io/badge/status-in--progress-yellow)
![Modules Completed](https://img.shields.io/badge/modules-0%2F13-lightgrey)
![Last Updated](https://img.shields.io/badge/updated-2026--06--09-blue)

> The complete modern web development stack: from JavaScript fundamentals through TypeScript's type system to building production React applications.

> [!NOTE]
> **Topic Overview**
> This topic covers the three technologies that dominate modern front-end (and increasingly
> back-end) web development: JavaScript, TypeScript, and React. You will start from absolute
> zero — no prior programming experience assumed — and progress through to expert-level topics
> including advanced TypeScript type system features, React internals, SSR/SSG, and
> production-grade full-stack application architecture.
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

JavaScript is the only programming language that runs natively in every web browser on the planet. Originally conceived as a lightweight scripting language to add interactivity to static HTML pages, it has grown into a universal runtime powering websites, mobile apps, desktop applications, servers, embedded systems, and even machine-learning pipelines. There is no other language with JavaScript's deployment reach: every time you click a button on a webpage, expand a menu, or see content load without a page refresh, JavaScript is involved.

TypeScript is a typed superset of JavaScript created at Microsoft. Where JavaScript is dynamically typed — meaning type errors surface only at runtime — TypeScript adds an optional static type layer that catches entire classes of bugs before code ever runs. TypeScript compiles down to plain JavaScript, making it compatible with every JavaScript runtime. It has become the default choice for any team building a non-trivial JavaScript application: the type annotations serve simultaneously as machine-checked documentation, editor intelligence, and a safety net for refactoring.

React is a declarative component-based UI library, originally built by Facebook (now Meta) to handle the complexity of building UIs that respond to constantly changing data. React's core insight — that a UI should be a pure function of its state, and that an efficient diffing algorithm (the "virtual DOM") can figure out the minimum set of DOM changes needed — proved transformative. React is now the most widely deployed front-end library in the world, and its component model, its hooks system, and its surrounding ecosystem (Next.js, React Native, Remix, etc.) define how most of the web is built.

Together, these three technologies — JavaScript as the runtime foundation, TypeScript as the type system, and React as the UI model — form the dominant technology stack for front-end engineers and a significant portion of full-stack engineers. Mastery of this stack opens doors to virtually every sector of the software industry.

### Why It Matters

Modern software is overwhelmingly web-first or web-adjacent. The JavaScript/TypeScript/React ecosystem is the largest ecosystem in software by number of packages (npm hosts over two million packages), by number of practitioners, and arguably by lines of code deployed in production. Even if you eventually specialise in a different area, a working understanding of this stack makes you a more effective collaborator, a better systems thinker, and a more employable engineer.

Understanding this stack is valuable because:

- It underpins front-end engineering — a skill used directly in every product company that ships a web application
- It develops the component-based mental model for building UIs — transferable to React Native, Flutter, SwiftUI, and other declarative UI systems
- Proficiency in it is expected in roles such as Front-End Engineer, Full-Stack Engineer, and React Developer

### Key Features of This Topic

- **Beginner-to-expert arc** — Modules 01–13 take you from your first `let x = 5` to building a full-stack Next.js application with authentication, API integration, and test coverage
- **TypeScript integration** — TypeScript is introduced at Module 06 and applied throughout the remaining modules
- **Practical focus** — Every concept is paired with runnable code; there is no theory without examples
- **Modern idioms** — The curriculum covers ES2022+, TypeScript 5.x, and React 18+ exclusively; legacy patterns are identified as such where relevant

---

## Historical Context

JavaScript was created by **Brendan Eich** in **1995** while working at Netscape Communications. The original version was written in just ten days, under pressure to ship it with Netscape Navigator 2.0. That origin story — ten days of design under deadline — explains many of JavaScript's quirks: `typeof null === "object"`, implicit coercion, `var` hoisting, and the infamous equality rules. Rather than seeing these as flaws to be embarrassed by, understanding their origin helps you predict and work around them.

TypeScript was created by **Anders Hejlsberg** (also the designer of C# and Delphi) at **Microsoft**, releasing publicly in **2012**. The goal was to make JavaScript practical for large-scale application development by adding optional static typing without abandoning the JavaScript ecosystem. The "optional" part was deliberate: TypeScript was designed to adopt gradually, so any valid JavaScript file is a valid TypeScript file.

React was created by **Jordan Walke** at **Facebook** and open-sourced at **JSConf US in May 2013**. It grew out of Facebook's need to build a newsfeed that was simultaneously fast, always up to date, and maintainable by a large team. The virtual DOM diffing approach, initially controversial, proved its performance claims in production and the library spread rapidly across the industry.

### Timeline

| Year | Event |
|------|-------|
| 1995 | Brendan Eich creates JavaScript ("Mocha", then "LiveScript") at Netscape in 10 days |
| 1996 | Netscape submits JavaScript to ECMA International for standardization as ECMAScript |
| 1997 | ECMAScript 1 (ES1) — the first standardized version — is published |
| 1999 | ES3 published; becomes the dominant browser JS standard for over a decade |
| 2005 | Jesse James Garrett coins "Ajax"; Google Maps shows that rich web apps are possible |
| 2009 | ES5 published; Node.js created by Ryan Dahl, bringing JavaScript to the server |
| 2012 | TypeScript 0.8 released publicly by Microsoft |
| 2013 | React open-sourced by Facebook at JSConf US |
| 2015 | ES2015 (ES6): `let`/`const`, arrow functions, classes, modules, Promises, destructuring |
| 2016 | React 15 stabilizes; Redux becomes the dominant state-management pattern |
| 2017 | `async`/`await` arrives in ES2017; Node.js 8 LTS ships |
| 2019 | React 16.8: Hooks released, transforming how React components are written |
| 2020 | TypeScript achieves near-universal adoption in large JS codebases |
| 2022 | React 18: concurrent rendering, `useTransition`, `useDeferredValue`, Suspense |
| 2023 | TypeScript 5.0; React Server Components stabilize in Next.js 13 App Router |
| Today | Actively used and expanded across industry and open-source |

---

## Real-World Applications

JavaScript, TypeScript, and React are actively used across essentially every sector of the software industry:

- **Social media and communications** — Facebook, Instagram, WhatsApp Web, Twitter/X, LinkedIn, and Slack are all built on React or React-influenced architectures. Facebook invented React to solve its own newsfeed rendering problems at scale.
- **E-commerce and marketplace platforms** — Airbnb uses React throughout its booking and listing interfaces. Shopify's storefront rendering, Etsy's product pages, and large portions of Amazon's front-end use React or React-adjacent frameworks.
- **Developer tooling** — Visual Studio Code is built with TypeScript and Electron. GitHub's web application is a large React deployment. Figma's multiplayer design canvas is built in TypeScript with WebAssembly.
- **Streaming and media** — Netflix uses React for its web interface and has contributed TypeScript tooling back to the community. Spotify's web player and Twitch's chat client are built in React.
- **Enterprise SaaS** — Atlassian (Jira, Confluence), Salesforce, and Microsoft (Teams web client, Azure portal) deploy React at scale. Atlassian was an early major TypeScript adopter in a large React codebase.
- **Financial technology** — Stripe's dashboard, Robinhood's web client, and Coinbase's exchange interface are React/TypeScript applications. TypeScript is nearly universal in fintech front-end due to the safety guarantees it provides around financial data.
- **Cloud infrastructure UI** — The AWS Amplify Console, the Vercel dashboard, the Cloudflare dashboard, and most modern cloud provider web interfaces are built with React and TypeScript.

---

## Learning Objectives

By completing this topic in full, you will be able to:

1. Write idiomatic modern JavaScript (ES2022+) including destructuring, modules, closures, Promises, async/await, and all standard array/object methods
2. Explain the JavaScript runtime model including the event loop, call stack, microtask queue, and how asynchronous code is scheduled
3. Design and implement TypeScript types, interfaces, generics, utility types, and conditional types to provide compile-time safety for real applications
4. Migrate an existing JavaScript codebase to TypeScript incrementally, resolving type errors and writing accurate declaration types
5. Build React applications using function components, hooks (`useState`, `useEffect`, `useContext`, `useReducer`, `useMemo`, `useCallback`, `useRef`, and custom hooks), and the React component lifecycle
6. Structure a multi-page React application using React Router with nested routes, lazy-loaded routes, and URL-driven state
7. Fetch and cache remote data in React using SWR or React Query, handle loading and error states, and write optimistic updates
8. Write component tests with React Testing Library that test behaviour rather than implementation, and write unit tests with Jest
9. Configure and use Vite for development and production builds, understand how tree-shaking, code splitting, and ES module bundling work
10. Implement server-side rendering (SSR) and static site generation (SSG) with Next.js, understand hydration, and choose between rendering strategies appropriately
11. Debug and profile React applications using React DevTools, identify and fix unnecessary re-renders, and apply memoization patterns correctly
12. Design and build a complete full-stack TypeScript application including authentication, API integration, database access, and a meaningful test suite

---

## Difficulty & Time Estimate

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Beginner → Expert |
| **Estimated Total Hours** | 120–180 hours (self-paced) |
| **Prerequisites** | Basic computer literacy; no prior programming experience required |
| **Recommended Pace** | 8–12 hours/week (15–20 weeks at this pace) |
| **Topic Type** | Computational (all concepts have runnable code examples) |
| **Suitable For** | Absolute beginners, developers from other languages, engineers learning front-end |

---

## Prerequisites

Before starting this topic, you should have:

- A computer with a terminal/command prompt and the ability to install software (Node.js)
- Basic familiarity with how web browsers work — no deep knowledge required
- No prior programming experience is required — Module 01 starts from absolute zero

> [!TIP]
> Not sure if you're ready? Open Module 01 and read the first two pages. If you can follow along,
> you're ready. The only genuine prerequisite is curiosity and willingness to type code into a file.

If you have prior programming experience in another language, you may skim Modules 01–03.
Use the Key Concepts and Common Pitfalls sections to check your understanding quickly.

---

## Learning Modules

| # | Module | Difficulty | Status | Score |
|---|--------|------------|--------|-------|
| 01 | [Introduction to JavaScript](./modules/01_introduction/) | Beginner | - [ ] | —/— |
| 02 | [Core JavaScript](./modules/02_core-javascript/) | Beginner | - [ ] | —/— |
| 03 | [Objects and Prototypes](./modules/03_objects-and-prototypes/) | Beginner–Intermediate | - [ ] | —/— |
| 04 | [Asynchronous JavaScript](./modules/04_asynchronous-javascript/) | Intermediate | - [ ] | —/— |
| 05 | [Browser and DOM](./modules/05_browser-and-dom/) | Intermediate | - [ ] | —/— |
| 06 | [TypeScript Fundamentals](./modules/06_typescript-fundamentals/) | Intermediate | - [ ] | —/— |
| 07 | [Advanced TypeScript](./modules/07_advanced-typescript/) | Advanced | - [ ] | —/— |
| 08 | [React Fundamentals](./modules/08_react-fundamentals/) | Intermediate–Advanced | - [ ] | —/— |
| 09 | [React Patterns](./modules/09_react-patterns/) | Advanced | - [ ] | —/— |
| 10 | [React Ecosystem](./modules/10_react-ecosystem/) | Advanced | - [ ] | —/— |
| 11 | [Build Tooling and Deployment](./modules/11_build-tooling-and-deployment/) | Advanced | - [ ] | —/— |
| 12 | [Performance and Advanced Patterns](./modules/12_performance-and-advanced/) | Expert | - [ ] | —/— |
| 13 | [Capstone Project](./modules/13_capstone-project/) | Expert | - [ ] | —/— |

**Status key:** ` ` Not started · `~` In progress · `x` Complete

---

## Progress

### Overall Progress

```
[░░░░░░░░░░░░░░░░░░░░] 0 / 13 modules complete (0%)
```

_Update this bar as you complete modules. Each block ≈ 5% of total modules._

```
Legend:  ░ = not started   ▒ = in progress   █ = complete
```

### Point Tracker

| Category | Earned | Possible | Percentage |
|----------|--------|----------|------------|
| Module Tests | 0 | 481 | 0% |
| Exercises | 0 | 130 | 0% |
| Projects | 0 | 195 | 0% |
| Bonus | 0 | — | — |
| **Total** | **0** | **806** | **0%** |

---

## Milestones

- [ ] **First Step** — Complete Module 01 (Introduction to JavaScript)
- [ ] **Foundation Built** — Complete Modules 01–03 with ≥ 70% on each test
- [ ] **Async Unlocked** — Complete Module 04 (Asynchronous JavaScript)
- [ ] **TypeScript Converted** — Complete Modules 06–07 (TypeScript fundamentals and advanced)
- [ ] **React Capable** — Complete Modules 08–09 with ≥ 80% on each test
- [ ] **Halfway There** — Complete 7 of 13 modules
- [ ] **Full-Stack Ready** — Complete Modules 08–11 with ≥ 70% on each test
- [ ] **Topic Complete** — All 13 modules finished
- [ ] **Deep Work** — Complete the Capstone Project (Module 13)
- [ ] **Expert** — Average test score ≥ 90% across all modules

---

## Test Scores

_Append a row after each test attempt. Do not overwrite previous attempts._

| Module | Date | Score | Grade | Notes |
|--------|------|-------|-------|-------|
| — | — | —/— | — | Not started |

**Grade scale:** A ≥ 90% · B ≥ 80% · C ≥ 70% · D ≥ 60% · F < 60%

---

## Projects

See [PROJECTS.md](./PROJECTS.md) for project ideas ranging from beginner to expert.

**My Projects:**

| Project Name | Difficulty | Started | Status | Link |
|-------------|------------|---------|--------|------|
| — | — | — | — | — |

---

## Resources

See [RESOURCES.md](./RESOURCES.md) for a curated list of books, courses, videos, and tools.

**Top picks so far** _(fill in as you study)_:

1. _To be filled in_
2. _To be filled in_
3. _To be filled in_

---

## Related Topics

Topics that complement, extend, or are required for JavaScript/TypeScript/React:

- [[networks]] — HTTP, REST APIs, and WebSockets; essential for understanding how React apps communicate with servers
- [[postgresql]] — Relational database knowledge required for full-stack applications (Capstone Project, Module 13)
- [[go]] — Go is a popular language for writing the backend APIs that React front-ends consume
- <!-- TODO: cross-link to [[css]] once that topic is created -->
- <!-- TODO: cross-link to [[node]] once that topic is created -->

See also the [ROADMAP.md](./ROADMAP.md) for how this topic fits into broader learning paths.

---

## Learning Journal

_Date-stamp each entry. Write honestly — confusion documented now becomes insight later._
_Newest entries at the top._

---

### 2026-06-09 — Topic Created

**What I did today:**
- Read the topic overview and ROADMAP.md
- Reviewed the module map

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
topic_slug: "javascript-typescript-react"
topic_name: "JavaScript, TypeScript and React"
module_count: 13
modules_complete: 0
total_points_earned: 0
total_points_possible: 806
completion_percentage: 0
difficulty: "Beginner → Expert"
estimated_hours: 150
prerequisites:
  - "basic-computer-literacy"
related_topics:
  - "networks"
  - "postgresql"
  - "go"
tags:
  - "javascript"
  - "typescript"
  - "react"
  - "web-development"
  - "front-end"
  - "full-stack"
creator: "Brendan Eich (JS), Anders Hejlsberg (TS), Jordan Walke (React)"
year_created: "1995 (JS), 2012 (TS), 2013 (React)"
```
