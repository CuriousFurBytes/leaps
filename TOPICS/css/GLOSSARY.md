# Glossary: CSS — Cascading Style Sheets

> Definitions for the key terms used throughout this topic. Terms appear in roughly the order they are introduced in the curriculum. For the global repository glossary, see [[shared/glossary]].

---

## Terms

### animation

A CSS feature that allows an element to gradually change from one style set to another, defined using `@keyframes` at-rules and applied via the `animation` property. Unlike transitions, animations can loop, run automatically (without a triggering event), and define multiple intermediate keyframes. See Module 08.

---

### at-rule

A CSS statement that begins with an `@` symbol and instructs the browser on how to behave. Examples include `@import` (load another stylesheet), `@media` (conditional styles), `@keyframes` (define an animation), `@font-face` (load a custom font), and `@layer` (declare a cascade layer). At-rules are one of the two top-level constructs in CSS (the other being qualified rules).

---

### box model

The rectangular model used by the browser to size and position every HTML element. Each element generates a box with four layers: **content** (the text or child elements), **padding** (space between content and border), **border** (a line around the padding), and **margin** (space outside the border, transparent). The `box-sizing` property controls whether `width` and `height` refer to the content box (`content-box`, the default) or the border box (`border-box`, which includes padding and border). See Module 03.

---

### cascade

The algorithm that determines which CSS rule applies when two or more rules could style the same element with the same property. The cascade considers: (1) origin and importance (user-agent styles → author styles → user styles, with `!important` reversing the order), (2) specificity (how precisely the selector targets the element), and (3) order of appearance (later rules win when origin and specificity are equal). The word "cascading" in CSS refers to this algorithm. See Module 01.

---

### custom property

A CSS variable, defined with a double-hyphen prefix (`--my-color: #3b82f6;`) and referenced with `var(--my-color)`. Custom properties are scoped to the element they are defined on (and inherited by descendants), making them powerful for theming and design tokens. Unlike preprocessor variables (Sass, Less), they are resolved at runtime by the browser, so they can be changed with JavaScript or media queries. See Module 06.

---

### flexbox

The CSS Flexible Box Layout module — a one-dimensional layout algorithm that arranges items along a single axis (either a row or a column). A flex container is created with `display: flex`. Items can grow, shrink, and align relative to each other and the container using properties like `flex-grow`, `flex-shrink`, `flex-basis`, `justify-content`, and `align-items`. Ideal for navigation bars, card rows, form layouts, and any layout where items share a common axis. See Module 04.

---

### grid

The CSS Grid Layout module — a two-dimensional layout algorithm that arranges items in rows and columns simultaneously. A grid container is created with `display: grid`. Columns and rows are defined with `grid-template-columns` and `grid-template-rows`. Items can be placed explicitly or auto-placed by the grid algorithm. Named areas, subgrid, and line-based placement give grid unmatched control for complex page layouts. See Module 05.

---

### inheritance

The mechanism by which some CSS property values are passed from a parent element to its children. Not all properties inherit — `color` and `font-size` do; `border` and `background` do not. You can force any property to inherit with `inherit`, reset to the browser default with `initial`, or reset to the cascaded value as if no rule existed with `unset`. Understanding which properties inherit prevents unexpected styles and reduces redundant declarations. See Module 01.

---

### media query

A conditional CSS construct, written with the `@media` at-rule, that applies styles only when the browser or device matches specified conditions. The most common condition is screen width (`@media (min-width: 768px)`), but queries can also target color scheme (`prefers-color-scheme`), motion preference (`prefers-reduced-motion`), orientation, resolution, and more. Media queries are the foundation of responsive design. See Module 07.

---

### pseudo-class

A selector keyword that targets an element in a specific *state*, not based on its position in the document tree alone. Pseudo-classes begin with a single colon: `:hover`, `:focus`, `:nth-child()`, `:not()`, `:checked`, `:first-child`. The `:has()` pseudo-class (Module 10) is particularly powerful as it selects a parent based on its children. See Module 02.

---

### pseudo-element

A selector keyword that creates a virtual sub-element within a real element, targeting a specific *part* of it that does not correspond to an actual HTML element. Pseudo-elements use double-colon syntax: `::before`, `::after`, `::first-line`, `::first-letter`, `::placeholder`, `::selection`. `::before` and `::after` insert generated content and are heavily used in CSS layout and decoration tricks. See Module 02.

---

### selector

The part of a CSS rule that identifies which element(s) the rule's declarations apply to. Selectors range from very broad (the type selector `p` targets all paragraphs) to very specific (the attribute selector `input[type="email"]` targets only email inputs). Understanding selector types, their specificity weights, and how they combine is fundamental to writing predictable CSS. See Modules 01 and 02.

---

### specificity

The scoring system the browser uses to decide which CSS rule wins when multiple rules target the same element and property. Specificity is calculated as a three-part score `(A, B, C)`: **A** counts ID selectors, **B** counts class/attribute/pseudo-class selectors, and **C** counts type/pseudo-element selectors. A higher score in any part overrides a lower score in that part, left to right. Inline styles beat all selectors; `!important` overrides specificity entirely. See Module 01.

---

### transform

A CSS property that applies a geometric transformation to an element without affecting the document flow — the transformed element does not push other elements around. Common functions include `translate()`, `rotate()`, `scale()`, `skew()`, and `perspective()`. Transforms are hardware-accelerated when combined with `will-change: transform`, making them the preferred tool for performant animations. See Module 08.

---

### transition

A CSS feature that animates changes to a property's value over a specified duration when the value changes (typically from a state change like `:hover`). Defined with the `transition` shorthand or its individual properties (`transition-property`, `transition-duration`, `transition-timing-function`, `transition-delay`). Transitions are simpler than animations — they go from state A to state B in response to a trigger; they cannot loop or define intermediate steps. See Module 08.
