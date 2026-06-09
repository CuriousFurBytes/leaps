# Module 06: Typography and Color

[← Module 05](../05_grid/) | [Topic Home](../../README.md) | [Next → Module 07](../07_responsive-design/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow)
![Time](https://img.shields.io/badge/time-5h-orange)

---

## Overview

Typography and colour are the two most powerful tools a developer has for communicating hierarchy, tone, and brand through CSS alone. A page with correct layout but poor typography and colour choices is nearly unreadable; a page with imperfect layout but excellent typography can still feel polished and professional.

This module covers all CSS font properties — `font-family`, `font-size`, `font-weight`, `font-style`, `line-height`, `letter-spacing`, `text-align`, and more — plus how to load custom web fonts with `@font-face` and how to use services like Google Fonts. It then covers the full colour toolkit: named colours, hex, `rgb()`, `hsl()`, `oklch()`, and gradients. The module concludes with **CSS custom properties** (CSS variables), which transform how you manage colour and typography across a design system.

---

## Prerequisites

- Module 01: Introduction to CSS — inheritance (typography properties are the primary inheritable properties)
- Module 03: Box Model and Layout — understanding how text fits within boxes

---

## Objectives

By the end of this module, you will be able to:

1. Control all key typographic properties: family, size, weight, style, line height, letter spacing, and alignment
2. Load and use a custom web font with `@font-face` and with a third-party font service
3. Specify colours using hex, `rgb()`, `hsl()`, and `oklch()`, and explain the strengths of each format
4. Create linear and radial gradients as background images
5. Define and use CSS custom properties (variables) for colours and typography tokens
6. Implement a complete colour theme that can be changed by modifying only the custom property definitions on `:root`

---

## Module Contents

This module is a stub. Full content will be added in a future expansion.

When complete, it will cover:

- **Font properties** — `font-family` stacks and system fonts, `font-size` (absolute vs relative units: `px`, `rem`, `em`, `%`), `font-weight`, `font-style`, `font-variant`, `font-display`
- **Text properties** — `line-height`, `letter-spacing`, `word-spacing`, `text-align`, `text-decoration`, `text-transform`, `text-indent`, `text-overflow`, `white-space`
- **Custom web fonts** — `@font-face` syntax, `src` with `format()`, `font-display: swap` for performance, Google Fonts and self-hosting
- **Colour formats** — named colours, hex (`#rrggbb`, `#rrggbbaa`), `rgb()`/`rgba()`, `hsl()`/`hsla()`, `oklch()` (the modern perceptually uniform format), `color-mix()`
- **Gradients** — `linear-gradient()`, `radial-gradient()`, `conic-gradient()`, repeated gradients, multiple backgrounds
- **CSS custom properties** — defining on `:root`, `var()` with fallbacks, scoping to a component, `@property` for typed custom properties
- **Design tokens** — colour, spacing, typography, and border-radius tokens; how custom properties enable theming and dark mode (preview for Module 09)
