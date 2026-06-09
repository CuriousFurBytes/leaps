# Module 03: Box Model and Layout

[← Module 02](../02_selectors-and-specificity/) | [Topic Home](../../README.md) | [Next → Module 04](../04_flexbox/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-beginner-green)
![Time](https://img.shields.io/badge/time-5h-orange)

---

## Overview

Every element rendered by a browser is a rectangular box. The **CSS box model** defines exactly how that box is sized: it has four concentric layers (content, padding, border, margin) and its total visual size depends on which "box-sizing mode" is active. Understanding the box model is not optional — it is the prerequisite for every layout technique in CSS.

This module covers the complete box model, the `display` property and how it controls whether an element participates in block flow, inline flow, or a new formatting context, and the four positioning schemes (`static`, `relative`, `absolute`, `fixed`, and `sticky`). It also introduces the concept of the **stacking context** and `z-index`, which controls depth ordering.

Before Flexbox and Grid existed, all page layouts were built with floats and positioned elements — techniques that are still relevant for specific use cases today. This module covers them as precursors to the modern layout modules that follow.

---

## Prerequisites

- Module 01: Introduction to CSS — cascade, specificity, rule syntax
- Module 02: Selectors and Specificity — how to target elements accurately

---

## Objectives

By the end of this module, you will be able to:

1. Explain the four layers of the CSS box model (content, padding, border, margin) and calculate an element's total rendered size
2. Use `box-sizing: border-box` correctly and explain why it is the recommended default
3. Describe the difference between block and inline formatting contexts
4. Use `display` values — `block`, `inline`, `inline-block`, `none` — appropriately
5. Position elements using `static`, `relative`, `absolute`, `fixed`, and `sticky` positioning
6. Explain what a stacking context is and use `z-index` to control depth ordering
7. Use the `overflow` property to control content that exceeds its container

---

## Module Contents

This module is a stub. Full content will be added in a future expansion.

When complete, it will cover:

- **The box model** — content box, padding box, border box, margin box; `width` and `height`; the infamous `content-box` vs `border-box` difference and why `border-box` won
- **Margin collapse** — vertical margins between adjacent blocks collapse to the larger of the two; why this catches every beginner (and many experts) off guard
- **The `display` property** — `block` (full-width, stacks vertically), `inline` (flows in text, no width/height), `inline-block` (flows in text but accepts dimensions), `none` (removes from flow), `contents` (removes the box but keeps children)
- **Formatting contexts** — block formatting context (BFC), inline formatting context (IFC); how `overflow: hidden` creates a BFC and clears floats
- **Positioning** — `static` (normal flow), `relative` (offset without removing from flow, creates a positioning parent), `absolute` (removed from flow, positioned relative to nearest positioned ancestor), `fixed` (relative to viewport), `sticky` (hybrid: relative until scroll threshold, then fixed)
- **Stacking context and z-index** — what creates a new stacking context (`position` + `z-index`, `opacity`, `transform`, `filter`); why `z-index` sometimes "doesn't work"
- **Floats (legacy)** — `float: left/right`, clearfix, why floats fell out of favour for layout
- **Overflow** — `overflow: visible/hidden/scroll/auto`; practical uses like scroll containers and BFC creation
