# Module 02: Selectors and Specificity

[← Module 01](../01_introduction/) | [Topic Home](../../README.md) | [Next → Module 03](../03_box-model-and-layout/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-beginner-green)
![Time](https://img.shields.io/badge/time-4h-orange)

---

## Overview

This module is a complete tour of every CSS selector type — from the simplest type selectors to the most powerful relational and pseudo-class selectors available in modern CSS. It deepens the specificity knowledge introduced in Module 01 and covers real-world selector strategies, including CSS reset and normalisation techniques.

CSS selectors are the mechanism that maps your style rules to specific elements in the document. A developer who knows only class and ID selectors is like a writer who knows only nouns and verbs — functional, but limited. Modern CSS includes attribute selectors, structural pseudo-classes (`:nth-child()`, `:first-of-type`, `:not()`), the relational pseudo-class `:has()`, pseudo-elements, and combinators that let you target elements based on their position in the DOM with surgical precision.

By the end of this module you will be able to write selectors that target exactly the elements you intend — and no others — without relying on adding extra classes to your HTML.

---

## Prerequisites

- Module 01: Introduction to CSS — specifically: rule syntax, how the cascade works, and the basic `(A,B,C)` specificity model

---

## Objectives

By the end of this module, you will be able to:

1. Identify and use all major CSS selector types: type, class, ID, universal, attribute, pseudo-class, pseudo-element, and combinator selectors
2. Calculate the specificity of any compound or complex selector, including those using `:is()`, `:not()`, and `:has()`
3. Use structural pseudo-classes (`:nth-child()`, `:first-of-type`, `:last-child`, etc.) to style elements based on their position in the DOM without adding classes
4. Write a minimal CSS reset or normalise stylesheet and explain why browser defaults must be addressed before styling
5. Choose the least-specific selector that correctly targets the intended element (avoiding specificity bloat)

---

## Module Contents

This module is a stub. Full content will be added in a future expansion.

When complete, it will cover:

- **Simple selectors** — type (`p`), class (`.card`), ID (`#header`), universal (`*`)
- **Attribute selectors** — `[type="text"]`, `[href^="https"]`, `[class~="btn"]`, case-insensitive matching
- **Pseudo-classes** — state-based (`:hover`, `:focus`, `:checked`, `:disabled`), structural (`:first-child`, `:last-child`, `:nth-child()`, `:nth-of-type()`), logical (`:not()`, `:is()`, `:where()`, `:has()`)
- **Pseudo-elements** — `::before`, `::after`, `::first-line`, `::first-letter`, `::placeholder`, `::selection`
- **Combinators** — descendant (` `), child (`>`), adjacent sibling (`+`), general sibling (`~`), column (`||`)
- **Specificity edge cases** — `:is()` and `:has()` take the highest specificity of their argument list; `:where()` has zero specificity; how specificity interacts with pseudo-elements
- **CSS resets** — the "reset" approach (zero everything out), the "normalise" approach (make browsers consistent), and the modern minimal reset (`box-sizing: border-box`, `margin: 0`, `padding: 0`)
- **Selector strategy** — when to use type vs class vs attribute selectors; why IDs should be avoided in stylesheets; the BEM preview
