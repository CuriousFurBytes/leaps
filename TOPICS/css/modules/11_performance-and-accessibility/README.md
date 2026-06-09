# Module 11: Performance and Accessibility

[← Module 10](../10_modern-css/) | [Topic Home](../../README.md) | [Next → Module 12](../12_capstone-project/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-expert-red)
![Time](https://img.shields.io/badge/time-6h-orange)

---

## Overview

Writing correct CSS is not enough at professional scale. CSS that is correct but slow delays the page's first paint and damages user experience and SEO rankings. CSS that is correct but inaccessible excludes users who rely on screen readers, keyboard navigation, or colour contrast — violating legal requirements in many jurisdictions and failing a significant portion of your audience.

This module covers two of the most important expert-level CSS concerns. On the **performance** side: how the browser's rendering pipeline (style → layout → paint → composite) works, which CSS properties trigger which pipeline stages, how to use Chrome DevTools' Performance panel to identify CSS regressions, and the critical CSS technique for improving time-to-first-paint. On the **accessibility** side: WCAG colour contrast requirements, visible focus indicators, the `prefers-reduced-motion` and `prefers-contrast` queries, and the `visually-hidden` pattern for screen-reader-only content.

---

## Prerequisites

- All previous modules — this module applies knowledge from every earlier module rather than introducing new CSS properties

---

## Objectives

By the end of this module, you will be able to:

1. Explain the browser rendering pipeline stages (style, layout, paint, composite) and which CSS property changes trigger each stage
2. Identify performance bottlenecks in CSS using Chrome DevTools' Performance and Layers panels
3. Implement critical CSS inline rendering for above-the-fold content
4. Audit a page for WCAG 2.1 AA colour contrast compliance and fix failing combinations
5. Implement keyboard-navigable focus styles that meet WCAG 2.4.7 (Focus Visible)
6. Apply the `visually-hidden` CSS pattern to provide accessible text to screen readers without visual impact
7. Write a complete `prefers-reduced-motion` strategy for a site with CSS animations
8. Use `@media (forced-colors: active)` to support Windows High Contrast Mode

---

## Module Contents

This module is a stub. Full content will be added in a future expansion.

When complete, it will cover:

- **The rendering pipeline** — style recalculation, layout (reflow), paint, and composite; what triggers each stage; the "pixel pipeline" mental model from Google's rendering architecture
- **Compositor-only properties** — `transform` and `opacity` only trigger compositing (fast); `top/left/width/height` trigger layout (slow); `background-color/box-shadow` trigger paint (medium)
- **CSS performance tools** — Chrome DevTools: Performance tab, Layers panel, Rendering flags (show paint rectangles, layer borders); Lighthouse CSS audit
- **Critical CSS** — inlining above-the-fold styles in `<style>` to eliminate render-blocking stylesheet requests; `<link rel="preload">` for stylesheets; tools like `critical` (Node.js)
- **Selector performance** — how browsers read selectors right-to-left; why overly broad selectors have a cost; the myth of "expensive selectors" in modern browsers (they are fast, but still worth understanding)
- **WCAG colour contrast** — AA (4.5:1 for normal text, 3:1 for large text) and AAA (7:1) levels; `hsl()` and `oklch()` for creating accessible palettes; tools: WebAIM Contrast Checker, Chrome DevTools accessibility audit
- **Focus styles** — WCAG 2.4.7 Focus Visible; `:focus-visible` vs `:focus`; custom focus ring patterns that satisfy both design and accessibility requirements
- **`visually-hidden` pattern** — hiding content from sighted users while keeping it available to assistive technology
- **`prefers-reduced-motion` strategy** — comprehensive approach: disable keyframe animations, reduce transition durations, test with OS reduced motion setting enabled
- **`forced-colors` media query** — Windows High Contrast Mode; which CSS properties are overridden by the browser in forced-colors mode; the `ButtonText`, `LinkText`, `Canvas` system colour keywords
