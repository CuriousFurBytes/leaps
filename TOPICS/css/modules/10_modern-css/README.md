# Module 10: Modern CSS

[← Module 09](../09_css-architecture/) | [Topic Home](../../README.md) | [Next → Module 11](../11_performance-and-accessibility/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-orange)
![Time](https://img.shields.io/badge/time-5h-orange)

---

## Overview

CSS has undergone a renaissance since 2020. Features that were either impossible or required JavaScript workarounds are now native to CSS. This module covers the class of capabilities that define "modern CSS": **container queries**, the **`:has()` relational pseudo-class**, **cascade layers (`@layer`)**, **logical properties**, and **subgrid**. Each of these is broadly supported in modern browsers and changes the way experienced developers write CSS.

Container queries are arguably the most significant layout feature since Grid: instead of applying styles based on the *viewport* width (media queries), you can apply styles based on the *container* the component lives in. This enables truly reusable components that adapt to their context.

Cascade layers `@layer` solve the specificity management problem that CSS architecture methodologies have been working around for 20 years. They let you explicitly declare the order of precedence between groups of styles, making specificity deterministic and reducing the need for high-specificity selectors.

---

## Prerequisites

- Modules 01–09 — especially the cascade (Module 01), selectors (Module 02), responsive design (Module 07), and CSS architecture (Module 09)

---

## Objectives

By the end of this module, you will be able to:

1. Write container queries with `@container` and explain how they differ from media queries
2. Use the `:has()` relational pseudo-class to style parents based on their children
3. Declare cascade layers with `@layer` and use them to control the order of specificity without raising selector specificity
4. Rewrite directional properties (`margin-left`, `border-right`) using logical properties (`margin-inline-start`, `border-inline-end`) for internationalisation support
5. Use subgrid to align nested items to a parent grid's tracks
6. Identify which modern CSS features require fallbacks for older browser support

---

## Module Contents

This module is a stub. Full content will be added in a future expansion.

When complete, it will cover:

- **Container queries** — `container-type: inline-size`, `@container` syntax, named containers, container query units (`cqi`, `cqb`, etc.); why they are more powerful than media queries for component libraries
- **`:has()` pseudo-class** — selecting a parent based on its children; real-world patterns: style a `<li>` if it contains an `<a>`, style a form field if it contains an invalid input, style a card differently if it has an image
- **Cascade layers (`@layer`)** — declaring layers, layer order, unnamed layers, overriding between layers; how `@layer` interacts with `!important`; using layers to integrate third-party CSS without specificity conflicts
- **Logical properties** — physical vs logical: `margin-left` → `margin-inline-start`; block vs inline axes; `padding-block`, `border-inline`, `inset-inline-start`; why logical properties are necessary for RTL/LTR language support
- **Subgrid** — `grid-template-columns: subgrid` and `grid-template-rows: subgrid`; aligning form labels to a parent grid; aligning card content across a row of cards
- **Other modern features** — `@scope` for scoped styles, `@starting-style` for entry animations, `light-dark()` colour function, `text-wrap: balance/pretty`, `anchor positioning` preview
- **Progressive enhancement with `@supports`** — testing for feature support before using it; providing fallbacks for older browsers
