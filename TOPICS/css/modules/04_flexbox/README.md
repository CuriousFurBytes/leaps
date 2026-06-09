# Module 04: Flexbox

[← Module 03](../03_box-model-and-layout/) | [Topic Home](../../README.md) | [Next → Module 05](../05_grid/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow)
![Time](https://img.shields.io/badge/time-5h-orange)

---

## Overview

The CSS Flexible Box Layout module — **Flexbox** — is a one-dimensional layout algorithm that arranges items along a single axis (row or column). It is the most widely used CSS layout tool for components: navigation bars, toolbars, form rows, card grids, sidebars, media objects, and anything where items need to be distributed, aligned, or sized dynamically within a single direction.

Before Flexbox, achieving common layouts like "three equal-width columns with equal spacing" or "a button group aligned to the right of a container" required float hacks, negative margins, or table display tricks. Flexbox replaced all of these for component-level layout with a clean, intuitive model.

This module covers every flex container and flex item property, the distinction between the main axis and cross axis, and a library of real-world layout patterns you can use immediately. By the end you will never need a float for layout again.

---

## Prerequisites

- Module 03: Box Model and Layout — understanding of `display` and the block/inline model
- Basic understanding that CSS layout properties affect the flow of elements on the page

---

## Objectives

By the end of this module, you will be able to:

1. Create a flex container with `display: flex` and explain what changes for its children
2. Control direction and wrapping with `flex-direction` and `flex-wrap`
3. Align items along the main axis with `justify-content` and along the cross axis with `align-items`
4. Explain the difference between `flex-grow`, `flex-shrink`, and `flex-basis`, and use the `flex` shorthand
5. Use `align-self` to override cross-axis alignment for individual flex items
6. Control visual order with the `order` property
7. Build five common layout patterns using only Flexbox: centred hero, navigation bar, card row, sidebar + content, footer pinned to bottom

---

## Module Contents

This module is a stub. Full content will be added in a future expansion.

When complete, it will cover:

- **Flex container properties** — `display: flex/inline-flex`, `flex-direction`, `flex-wrap`, `flex-flow` (shorthand), `justify-content`, `align-items`, `align-content`, `gap`
- **Flex item properties** — `flex-grow`, `flex-shrink`, `flex-basis`, `flex` (shorthand), `align-self`, `order`
- **The flex algorithm** — how the browser distributes free space using `flex-grow`; how it compresses items using `flex-shrink`; the role of `flex-basis` as the starting size
- **Common patterns** — centred content (both axes), navigation with `space-between`, equal-height card row, sticky footer, responsive menu that wraps to multiple lines
- **Flexbox gotchas** — `flex` shorthand vs individual properties (they have different defaults); `min-width: 0` for items that need to shrink below their content size; why `align-items: stretch` can cause unexpected height
- **Flexbox vs Grid** — when to use which: Flexbox for one-directional components, Grid for two-dimensional page layout; they are complementary, not competing
