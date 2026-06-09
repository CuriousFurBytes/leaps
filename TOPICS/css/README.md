# CSS — Cascading Style Sheets

![Status](https://img.shields.io/badge/status-in--progress-yellow)
![Modules Completed](https://img.shields.io/badge/modules-0%2F12-lightgrey)
![Last Updated](https://img.shields.io/badge/updated-2026--06--09-blue)

> CSS is the language that controls how HTML elements look and are laid out in the browser — it is the entire visual layer of the web.

> [!NOTE]
> **Topic Overview**
> CSS (Cascading Style Sheets) is a stylesheet language that describes the presentation of a document written in HTML or XML. It controls typography, colour, spacing, layout, animation, and every other visual aspect of a webpage. CSS is one of the three core technologies of the World Wide Web alongside HTML and [[javascript-typescript-react]].
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

CSS (Cascading Style Sheets) is the stylesheet language of the web. It gives web authors the power to separate the *presentation* of a document from its *structure* (HTML) and *behaviour* (JavaScript). With CSS you can control fonts, colours, spacing, borders, backgrounds, layout algorithms, transitions, animations, and complex responsive behaviour — all without touching the HTML content itself.

The "cascading" in CSS refers to the algorithm the browser uses to determine which rule wins when multiple rules apply to the same element. This cascade, combined with the concepts of *specificity* and *inheritance*, is the heart of the language and the source of both its power and its most common frustrations for beginners.

### Why It Matters

Every visual aspect of the web you see in a browser is CSS. The Netflix interface, the GitHub UI, the government forms you fill in, the news articles you read — all of these are HTML structured by CSS. Understanding CSS is not optional for anyone who works on the front end. It is the single technology that transforms plain text content into the polished, responsive, and accessible experiences that users expect.

Understanding CSS is valuable because:

- It underpins front-end web development — a skill used directly in every product company, agency, and startup building web interfaces
- It develops the mental model for layout and visual design — transferable to native mobile design, print layout, and design systems
- Proficiency in it is expected in roles such as front-end engineer, full-stack developer, UX engineer, and design-systems engineer

### Key Features of This Topic

- **The Cascade and Specificity** — the algorithm that resolves conflicting style rules, giving CSS predictability once understood
- **Box Model** — every element is a rectangular box; understanding this model is the foundation of all layout work
- **Modern Layout Systems** — Flexbox and Grid are fully supported, production-ready layout engines that replaced float-based hacks
- **Responsive Design** — media queries, container queries, and fluid units let a single stylesheet serve screens from a 320 px phone to a 4 K monitor

---

## Historical Context

CSS was proposed by **Håkon Wium Lie** on **10 October 1994**, while working at CERN alongside Tim Berners-Lee. Before CSS, web pages were styled using HTML attributes (`<font>`, `<center>`, `bgcolor`) — mixing structure and presentation in a way that made large sites nightmarish to maintain. Lie's proposal was to create a separate language purely for presentation, with a cascade that let both authors and readers contribute style rules.

The World Wide Web Consortium (W3C) published the first official CSS specification in 1996. Browser vendors were initially slow to adopt it consistently, and the decade from 1996 to 2006 was marked by painful browser incompatibilities that drove developers to table-based layouts and JavaScript hacks. Gradually, standards compliance improved, and by the early 2010s CSS had become a stable, powerful foundation.

### Timeline

| Year | Event |
|------|-------|
| 1994 | Håkon Wium Lie proposes CSS at CERN; first public proposal published |
| 1996 | CSS Level 1 (CSS1) published as a W3C recommendation — covers fonts, colours, margins, borders |
| 1998 | CSS Level 2 (CSS2) published — adds positioning, z-index, media types, and generated content |
| 2004 | Internet Explorer 6's incomplete CSS2 support drives widespread float-based layout hacks |
| 2011 | CSS 2.1 published as a W3C recommendation, codifying the actual browser behaviour of CSS2 |
| 2011 | CSS3 begins shipping as independent modules (Selectors, Backgrounds, Transitions, Animations) |
| 2012 | Flexbox ships in major browsers after several spec revisions |
| 2017 | CSS Grid Layout ships in Chrome, Firefox, and Safari within weeks of each other |
| 2020+ | Container queries, cascade layers (`@layer`), `:has()`, logical properties, and subgrid gain broad support |
| Today | CSS is actively developed in W3C working groups; new features ship every year |

---

## Real-World Applications

CSS is actively used across every domain of software development that touches a user interface:

- **Streaming Platforms** — Netflix uses sophisticated CSS animations, custom properties, and responsive grid layouts to deliver a consistent experience across TVs, phones, tablets, and browsers
- **Developer Tools and Design Systems** — GitHub's Primer design system and Google's Material Design use CSS custom properties and utility-class approaches to maintain consistent UI at scale
- **CSS Frameworks** — Bootstrap (component-based) and Tailwind CSS (utility-first) are used in millions of production web applications; deep CSS knowledge is what separates framework users from framework extenders
- **Data Visualisation** — CSS transforms and animations are used alongside SVG to produce interactive charts and dashboards
- **Publishing and Editorial** — Online newspapers, magazines, and documentation sites (MDN, Stripe Docs) use advanced CSS typography and layout features to produce professional reading experiences
- **E-commerce** — Shopify, WooCommerce, and custom storefronts rely on CSS for product grids, cart interfaces, responsive checkouts, and accessibility-compliant form styling

---

## Learning Objectives

By completing this topic in full, you will be able to:

1. Explain the cascade algorithm, specificity scoring, and inheritance — and debug style conflicts without resorting to `!important`
2. Construct semantic, accessible HTML+CSS layouts using Flexbox and CSS Grid from scratch
3. Build fully responsive designs using mobile-first media queries, fluid typography, and responsive images
4. Apply CSS architecture methodologies (BEM, OOCSS, utility-first) to maintain large stylesheets on real projects
5. Implement smooth, performant CSS transitions and keyframe animations while respecting `prefers-reduced-motion`
6. Use modern CSS features — container queries, cascade layers, `:has()`, logical properties, and subgrid — in production code
7. Audit and improve CSS performance (critical CSS, rendering pipeline, layout/paint/composite layers)
8. Build and document a complete, accessible, themeable design system with CSS custom properties and dark mode support

---

## Difficulty & Time Estimate

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Beginner → Expert |
| **Estimated Total Hours** | 60–80 hours |
| **Prerequisites** | Basic HTML knowledge |
| **Recommended Pace** | 5–7 hours/week |
| **Topic Type** | Practical (Computational — all concepts require CSS code) |
| **Suitable For** | Absolute beginners, self-taught developers, CS students, designers learning to code |

---

## Prerequisites

Before starting this topic, you should have a working understanding of:

- Basic HTML — specifically: HTML document structure, common elements (`div`, `p`, `h1`–`h6`, `ul`, `li`, `a`, `img`, `input`, `form`), and how browsers parse HTML into the DOM tree
- A text editor and a modern browser with developer tools (Chrome DevTools or Firefox DevTools)

> [!TIP]
> Not sure if you're ready? Attempt Module 01 and gauge how it feels.
> If you can write a basic HTML page with headings, paragraphs, and links, you are ready to start.
> CSS knowledge is built entirely through writing and experimenting — open a browser and try things as you read.

---

## Learning Modules

| # | Module | Difficulty | Status | Score |
|---|--------|-----------|--------|-------|
| 01 | [Introduction to CSS](./modules/01_introduction/) | Beginner | - [ ] | —/— |
| 02 | [Selectors and Specificity](./modules/02_selectors-and-specificity/) | Beginner | - [ ] | —/— |
| 03 | [Box Model and Layout](./modules/03_box-model-and-layout/) | Beginner | - [ ] | —/— |
| 04 | [Flexbox](./modules/04_flexbox/) | Intermediate | - [ ] | —/— |
| 05 | [Grid](./modules/05_grid/) | Intermediate | - [ ] | —/— |
| 06 | [Typography and Color](./modules/06_typography-and-color/) | Intermediate | - [ ] | —/— |
| 07 | [Responsive Design](./modules/07_responsive-design/) | Intermediate | - [ ] | —/— |
| 08 | [Animations and Transitions](./modules/08_animations-and-transitions/) | Advanced | - [ ] | —/— |
| 09 | [CSS Architecture](./modules/09_css-architecture/) | Advanced | - [ ] | —/— |
| 10 | [Modern CSS](./modules/10_modern-css/) | Advanced | - [ ] | —/— |
| 11 | [Performance and Accessibility](./modules/11_performance-and-accessibility/) | Expert | - [ ] | —/— |
| 12 | [Capstone Project](./modules/12_capstone-project/) | Expert | - [ ] | —/— |

**Status key:** ` ` Not started · `~` In progress · `x` Complete

---

## Progress

### Overall Progress

```
[░░░░░░░░░░░░░░░░░░░░] 0 / 12 modules complete (0%)
```

_Update this bar as you complete modules. Each block = 5% of total modules._

```
Legend:  ░ = not started   ▒ = in progress   █ = complete
Example: [███████▒░░░░░░░░░░░░] 7.5 / 12 modules (62%)
```

### Point Tracker

| Category | Earned | Possible | Percentage |
|----------|--------|----------|------------|
| Module Tests | 0 | 444 | 0% |
| Exercises | 0 | 120 | 0% |
| Projects | 0 | 90 | 0% |
| Bonus | 0 | — | — |
| **Total** | **0** | **654** | **0%** |

---

## Milestones

- [ ] **First Step** — Complete Module 01 (Introduction to CSS)
- [ ] **Foundation Built** — Complete Modules 01–03 with ≥ 70% on each test
- [ ] **Layout Master** — Complete Modules 04–05 (Flexbox and Grid)
- [ ] **Halfway There** — Complete 6 of 12 modules
- [ ] **Design Systems Ready** — Complete Modules 06–09
- [ ] **Core Mastery** — Score ≥ 80% on all core module tests
- [ ] **First Project Shipped** — Complete at least one Beginner or Intermediate project
- [ ] **Topic Complete** — All 12 modules finished
- [ ] **Deep Work** — Complete the Capstone Project (Module 12)

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

See [RESOURCES.md](./RESOURCES.md) for a curated and verified list of books, courses, videos, and tools.

**Top picks so far** _(fill in as you study)_:

1. _To be filled in_
2. _To be filled in_
3. _To be filled in_

---

## Related Topics

Topics that complement, extend, or are required for CSS:

- [[javascript-typescript-react]] — JavaScript manipulates CSS classes and inline styles at runtime; React component libraries are built on CSS; CSS-in-JS tools require JS knowledge
- [[networks]] — understanding how browsers request and cache CSS files, the critical rendering path, and HTTP/2 push for stylesheet delivery
- [[qa-testing]] — visual regression testing, accessibility audits (WCAG), and testing styled components with tools like Playwright and axe

See also the [ROADMAP.md](./ROADMAP.md) for how this topic fits into broader learning paths.

---

## Learning Journal

_Date-stamp each entry. Write honestly — confusion documented now becomes insight later._
_Newest entries at the top._

---

_Add new journal entries above this line, newest first._

---

## AI Metadata

```yaml
# Maintained by LEAPS tooling — manual edits will be overwritten on next sync
last_ai_expansion: "2026-06-09"
topic_slug: "css"
topic_name: "CSS — Cascading Style Sheets"
module_count: 12
modules_complete: 0
total_points_earned: 0
total_points_possible: 654
completion_percentage: 0
difficulty: "Beginner → Expert"
estimated_hours: 70
prerequisites:
  - "html"
related_topics:
  - "javascript-typescript-react"
  - "networks"
  - "qa-testing"
tags:
  - "web"
  - "front-end"
  - "styling"
  - "layout"
  - "design"
creator: "Håkon Wium Lie"
year_created: "1994"
```
