# Module 07: Responsive Design

[← Module 06](../06_typography-and-color/) | [Topic Home](../../README.md) | [Next → Module 08](../08_animations-and-transitions/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow)
![Time](https://img.shields.io/badge/time-6h-orange)

---

## Overview

Responsive design is the practice of building web pages that adapt their layout, typography, and visual design to the width and capabilities of the device displaying them — from a 320 px mobile phone to a 2560 px desktop monitor. It is not a single CSS feature but a combination of techniques: media queries, fluid units, flexible images, and the mobile-first design philosophy.

The term "responsive web design" was coined by Ethan Marcotte in a 2010 A List Apart article, where he described the combination of fluid grids, flexible images, and media queries that make a design adapt to its context. Before this, common practice was to build separate "mobile" and "desktop" versions of a site — a maintenance nightmare.

This module covers the full responsive toolkit: `@media` queries (width, colour scheme, motion preference, orientation), the viewport meta tag, relative units (`vw`, `vh`, `vmin`, `vmax`, `dvh`), the `clamp()` function for fluid typography, flexible images, and the mobile-first approach. Container queries (a newer, more powerful alternative to media queries) are introduced here as a preview but covered in depth in Module 10.

---

## Prerequisites

- Module 04: Flexbox and Module 05: Grid — the layout systems that make responsive design practical
- Module 06: Typography and Color — font sizes that need to be fluid

---

## Objectives

By the end of this module, you will be able to:

1. Write mobile-first CSS using `min-width` media queries
2. Use viewport units (`vw`, `vh`, `svh`, `dvh`) appropriately
3. Implement fluid typography with `clamp()`, `min()`, and `max()`
4. Make images responsive with `max-width: 100%` and `object-fit`
5. Test responsive designs using browser DevTools device emulation
6. Use `@media (prefers-color-scheme)` and `@media (prefers-reduced-motion)` for user preference adaptation
7. Describe the difference between media queries (viewport-based) and container queries (parent-based)

---

## Module Contents

This module is a stub. Full content will be added in a future expansion.

When complete, it will cover:

- **The viewport meta tag** — `<meta name="viewport" content="width=device-width, initial-scale=1">` and why it is essential
- **Media queries** — syntax, common breakpoints, `min-width` vs `max-width`, `and`/`or`/`not` operators, range syntax (`(width >= 768px)`)
- **Mobile-first design** — why "start narrow, add complexity as width increases" produces better code than the reverse
- **Fluid units** — `vw`, `vh`, `vmin`, `vmax`, `svh`, `dvh`, `lvh` (new small/large/dynamic viewport units for mobile browsers with shifting UI)
- **Fluid typography** — `font-size: clamp(1rem, 2.5vw, 1.5rem)` — the minimum, preferred, and maximum pattern
- **Flexible images** — `max-width: 100%`, `height: auto`, `srcset` and `sizes` attributes, `<picture>` element
- **User preference media queries** — `prefers-color-scheme`, `prefers-reduced-motion`, `prefers-contrast`, `forced-colors`
- **Container queries preview** — `@container` basics (full coverage in Module 10); why they are more powerful than media queries for component-level responsiveness
