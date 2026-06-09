# Module 08: Animations and Transitions

[← Module 07](../07_responsive-design/) | [Topic Home](../../README.md) | [Next → Module 09](../09_css-architecture/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-orange)
![Time](https://img.shields.io/badge/time-5h-orange)

---

## Overview

CSS motion — transitions and animations — is how a static design becomes a living interface. A well-crafted transition on a button hover state makes the interaction feel physical and responsive. A loading animation communicates that work is happening. A page transition guides the user's attention. Done well, CSS motion improves usability. Done poorly, it frustrates and exhausts.

CSS provides two motion systems: **transitions** (animate from one state to another in response to a change) and **animations** (run a sequence of keyframes, with or without a trigger). Both rely on the CSS `transform` property for the most performant motion, because transforms are composited by the GPU without triggering layout recalculation.

This module covers the complete CSS motion toolkit: `transition`, `@keyframes`, `animation`, `transform` (2D and 3D), `will-change`, and — critically — the `prefers-reduced-motion` media query that makes motion accessible. By the end you will be able to implement any common UI animation without JavaScript.

---

## Prerequisites

- Module 06: Typography and Color — understanding CSS custom properties (used for animation values)
- Module 07: Responsive Design — `@media` query syntax (the same syntax used for `prefers-reduced-motion`)

---

## Objectives

By the end of this module, you will be able to:

1. Animate style changes using `transition` with appropriate duration, timing function, and delay
2. Define multi-step animations with `@keyframes` and control them with the `animation` shorthand
3. Apply 2D and 3D transforms (translate, rotate, scale, skew, perspective) without affecting document flow
4. Explain why transforms and opacity are preferred for performant animation over layout properties
5. Use `will-change` correctly (and sparingly) to promote elements to their own compositor layer
6. Implement a complete respects-motion-preference pattern using `@media (prefers-reduced-motion: reduce)`
7. Build at least three common UI animations from scratch: button hover, modal entrance, loading spinner

---

## Module Contents

This module is a stub. Full content will be added in a future expansion.

When complete, it will cover:

- **`transition`** — `transition-property`, `transition-duration`, `transition-timing-function` (ease, linear, ease-in-out, cubic-bezier), `transition-delay`, `transition` shorthand, multiple transitions
- **`@keyframes`** — defining keyframes with `from`/`to` and percentages, naming animations, reusing named animations
- **`animation`** — `animation-name`, `animation-duration`, `animation-timing-function`, `animation-delay`, `animation-iteration-count`, `animation-direction`, `animation-fill-mode`, `animation-play-state`, `animation` shorthand
- **`transform`** — 2D: `translate()`, `rotate()`, `scale()`, `skew()`, `matrix()`; 3D: `rotateX/Y/Z()`, `perspective()`, `translateZ()`, `transform-style: preserve-3d`; `transform-origin`
- **The rendering pipeline** — why layout properties (width, height, margin) trigger expensive reflows; why transform and opacity only trigger compositing; how to check in Chrome DevTools Performance panel
- **`will-change`** — promoting to a compositor layer, its costs (memory), when to use and when to remove it
- **`prefers-reduced-motion`** — the pattern for disabling or reducing motion for users who request it; WCAG 2.1 Success Criterion 2.3.3
- **Common patterns** — skeleton loading screen, fade-in on scroll (CSS-only), tooltip entrance, accordion panel, page transition with `@starting-style`
