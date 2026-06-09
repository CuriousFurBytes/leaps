# Module 09: CSS Architecture

[← Module 08](../08_animations-and-transitions/) | [Topic Home](../../README.md) | [Next → Module 10](../10_modern-css/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-orange)
![Time](https://img.shields.io/badge/time-5h-orange)

---

## Overview

Writing CSS that works for 10 pages is easy. Writing CSS that a team of 5 can maintain across 500 pages, over 3 years, without it turning into an incomprehensible tangle of overrides — that requires **CSS architecture**.

CSS architecture is the discipline of organising, naming, and scoping CSS so that stylesheets remain predictable, scalable, and maintainable as a project grows. This module covers the major methodologies that have emerged to solve this problem: BEM (Block Element Modifier), OOCSS (Object-Oriented CSS), SMACSS (Scalable and Modular Architecture for CSS), CSS Modules (scoped by build tools), and the utility-first approach popularised by Tailwind CSS.

None of these approaches is universally correct — each has trade-offs, and most large projects blend several. But knowing them all gives you the vocabulary and tooling to make informed architectural decisions and to read and contribute to any team's CSS codebase.

---

## Prerequisites

- Modules 01–08 — specifically: specificity (BEM exists primarily to avoid specificity problems), custom properties (used in design tokens), and all layout and visual modules

---

## Objectives

By the end of this module, you will be able to:

1. Explain the problem CSS architecture solves and why flat stylesheets fail at scale
2. Write CSS using the BEM naming methodology (Block__Element--Modifier)
3. Identify the OOCSS principles of separating structure from skin and container from content
4. Describe the SMACSS file organisation categories (Base, Layout, Module, State, Theme)
5. Explain how CSS Modules (used in React and other component frameworks) scope CSS to individual components
6. Describe the utility-first approach (Tailwind CSS) and compare it to component-based methodologies
7. Choose an appropriate CSS architecture strategy for a given project context

---

## Module Contents

This module is a stub. Full content will be added in a future expansion.

When complete, it will cover:

- **The problem** — how specificity wars, global scope, dead code, and naming collisions emerge as CSS scales; why the cascade is both CSS's greatest feature and its greatest source of maintenance pain
- **BEM — Block Element Modifier** — naming convention: `.block`, `.block__element`, `.block--modifier`; how BEM eliminates specificity issues by keeping all selectors at `(0,1,0)`; BEM in practice with real component examples
- **OOCSS — Object-Oriented CSS** — Nicole Sullivan's two principles: separate structure from skin (visual properties), separate container from content (avoid location-dependent styles)
- **SMACSS — Scalable and Modular Architecture for CSS** — Jonathan Snook's five categories of CSS rules and how to organise files by category
- **CSS Modules** — build-tool-scoped CSS (used with webpack, Vite, Next.js, etc.); local scope by default; `:global` escape hatch; `composes` for composition
- **Utility-first CSS (Tailwind concepts)** — the idea of composing UI from small, single-purpose classes rather than component classes; the `@apply` directive; design token integration; trade-offs (HTML verbosity vs CSS maintainability)
- **Choosing an architecture** — decision framework: team size, project scale, whether you control the HTML, whether you use a component framework, performance budget
- **Design tokens and CSS custom properties** — managing a token system as a design/development contract; naming conventions for tokens (primitive → semantic → component)
