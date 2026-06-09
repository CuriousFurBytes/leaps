# Module 05: Grid

[← Module 04](../04_flexbox/) | [Topic Home](../../README.md) | [Next → Module 06](../06_typography-and-color/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow)
![Time](https://img.shields.io/badge/time-6h-orange)

---

## Overview

CSS Grid Layout is a two-dimensional layout algorithm — the first in CSS history that treats both rows and columns as first-class concepts simultaneously. While Flexbox is the right tool for arranging items along a single axis, Grid is the right tool for any layout where you need to control both dimensions at once: page templates, dashboard panels, photo galleries, form layouts, and complex article designs.

Grid was the result of extensive collaboration between browser vendors, the CSS Working Group, and web developers starting around 2011. By 2017, all major browsers shipped it simultaneously — an unusually coordinated rollout that reflected the community's desire to end the era of float-based layout hacks.

This module covers explicit and implicit grids, grid tracks (rows and columns), named lines and areas, placement algorithms, alignment, and advanced patterns including subgrid. By the end you will be able to build any page layout — from simple two-column to complex magazine layouts — without touching floats or Flexbox for the structure.

---

## Prerequisites

- Module 03: Box Model and Layout — `display` values and flow concepts
- Module 04: Flexbox — understanding of the container/item model (Grid uses the same mental model)

---

## Objectives

By the end of this module, you will be able to:

1. Create a grid container with `display: grid` and define columns and rows with `grid-template-columns` and `grid-template-rows`
2. Use `fr` units, `repeat()`, `minmax()`, and `auto-fill`/`auto-fit` to create flexible, responsive grids
3. Place items explicitly using line numbers, `span`, and named areas
4. Explain the difference between explicit and implicit grid tracks
5. Align grid items using `justify-items`, `align-items`, `justify-self`, and `align-self`
6. Name grid lines and areas with `grid-template-areas` to create readable, maintainable layout code
7. Use subgrid to align nested items to the parent grid's tracks

---

## Module Contents

This module is a stub. Full content will be added in a future expansion.

When complete, it will cover:

- **Grid container properties** — `display: grid/inline-grid`, `grid-template-columns`, `grid-template-rows`, `grid-template-areas`, `grid-template` (shorthand), `gap`, `justify-items`, `align-items`, `justify-content`, `align-content`
- **Grid item properties** — `grid-column-start/end`, `grid-row-start/end`, `grid-column`, `grid-row`, `grid-area`, `justify-self`, `align-self`
- **The `fr` unit** — what "fractional unit" means; how it distributes remaining space after fixed-size tracks
- **`repeat()`, `minmax()`, `auto-fill`, `auto-fit`** — building responsive grids that reflow automatically without media queries
- **Explicit vs implicit grid** — named tracks vs auto-generated tracks; `grid-auto-rows`, `grid-auto-columns`, `grid-auto-flow`
- **Named lines and areas** — `[line-name]` syntax in `grid-template-columns`; `grid-template-areas` with named regions
- **Subgrid** — aligning nested grid items to the parent grid's tracks (a game-changer for form layouts and card designs)
- **Common page layouts** — holy grail (header/sidebar/main/aside/footer), dashboard, magazine, responsive card gallery
