# Cheatsheet: CSS — Cascading Style Sheets

> A quick-reference guide for the most-used CSS syntax and patterns. Not a replacement for the modules — use this during and after study to jog your memory.

---

## Table of Contents

- [CSS Rule Anatomy](#css-rule-anatomy)
- [Selectors](#selectors)
- [Specificity Scoring](#specificity-scoring)
- [Box Model Diagram](#box-model-diagram)
- [Display and Positioning](#display-and-positioning)
- [Flexbox Properties](#flexbox-properties)
- [Grid Properties](#grid-properties)
- [Common Media Queries](#common-media-queries)
- [CSS Custom Properties](#css-custom-properties)
- [Useful Functions](#useful-functions)
- [At-Rules Quick Reference](#at-rules-quick-reference)

---

## CSS Rule Anatomy

```css
/* selector { property: value; } */
.card {
  background-color: #ffffff; /* property: value */
  padding: 1rem;
  border: 1px solid #e5e7eb;
}
```

---

## Selectors

| Selector | Syntax | Targets |
|----------|--------|---------|
| Universal | `*` | Every element |
| Type | `p`, `h1`, `div` | All elements of that type |
| Class | `.card`, `.btn-primary` | Elements with that class |
| ID | `#header` | The element with that ID (use sparingly) |
| Attribute | `[type="text"]` | Elements with matching attribute |
| Descendant | `nav a` | `a` anywhere inside `nav` |
| Child | `ul > li` | `li` that is a direct child of `ul` |
| Adjacent sibling | `h2 + p` | `p` immediately after `h2` |
| General sibling | `h2 ~ p` | All `p` siblings after `h2` |
| Pseudo-class | `:hover`, `:focus`, `:nth-child(2)` | Element in a state |
| Pseudo-element | `::before`, `::after`, `::first-line` | Sub-part of an element |

---

## Specificity Scoring

Specificity is a three-part score `(A, B, C)`:

| What counts | Adds to | Example |
|------------|---------|---------|
| Inline `style=""` | Overrides all | `style="color: red"` |
| ID selector `#id` | A | `#header` → (1,0,0) |
| Class `.class`, attribute `[attr]`, pseudo-class `:hover` | B | `.btn:hover` → (0,2,0) |
| Type `p`, pseudo-element `::before` | C | `p::before` → (0,0,2) |
| Universal `*`, combinators (` `, `>`, `+`, `~`) | Nothing | — |

Higher A beats higher B; higher B beats higher C. Later rules win on a tie.

`!important` overrides specificity entirely — avoid it except in utility overrides.

---

## Box Model Diagram

```
┌──────────────────────────────────┐
│             margin               │
│  ┌────────────────────────────┐  │
│  │           border           │  │
│  │  ┌──────────────────────┐  │  │
│  │  │        padding       │  │  │
│  │  │  ┌────────────────┐  │  │  │
│  │  │  │    content     │  │  │  │
│  │  │  │  width/height  │  │  │  │
│  │  │  └────────────────┘  │  │  │
│  │  └──────────────────────┘  │  │
│  └────────────────────────────┘  │
└──────────────────────────────────┘
```

```css
/* Use border-box everywhere — width includes padding and border */
*, *::before, *::after {
  box-sizing: border-box;
}
```

---

## Display and Positioning

```css
/* Common display values */
display: block;          /* Full-width block, stacks vertically */
display: inline;         /* Flows in text, no width/height */
display: inline-block;   /* Flows in text, respects width/height */
display: flex;           /* Flex container */
display: inline-flex;    /* Inline flex container */
display: grid;           /* Grid container */
display: none;           /* Hides the element (removed from flow) */

/* Positioning */
position: static;    /* Default — normal flow */
position: relative;  /* Offset from normal position; creates stacking context */
position: absolute;  /* Removed from flow; positioned relative to nearest positioned ancestor */
position: fixed;     /* Removed from flow; positioned relative to viewport */
position: sticky;    /* Switches between relative and fixed at a scroll threshold */
```

---

## Flexbox Properties

```css
/* On the flex CONTAINER */
.container {
  display: flex;
  flex-direction: row;           /* row | row-reverse | column | column-reverse */
  flex-wrap: wrap;               /* nowrap | wrap | wrap-reverse */
  justify-content: center;       /* Main axis: flex-start | flex-end | center | space-between | space-around | space-evenly */
  align-items: stretch;          /* Cross axis (single line): flex-start | flex-end | center | stretch | baseline */
  align-content: flex-start;     /* Cross axis (multi-line): same values as justify-content */
  gap: 1rem;                     /* Space between items (row-gap and column-gap) */
}

/* On flex ITEMS */
.item {
  flex-grow: 1;       /* How much to grow relative to siblings (0 = don't grow) */
  flex-shrink: 1;     /* How much to shrink (0 = don't shrink) */
  flex-basis: auto;   /* Base size before growing/shrinking */
  flex: 1 1 auto;     /* Shorthand: grow shrink basis */
  align-self: center; /* Override container's align-items for this item */
  order: 0;           /* Visual order (default 0; lower = earlier) */
}
```

---

## Grid Properties

```css
/* On the grid CONTAINER */
.grid {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;       /* Three columns */
  grid-template-rows: auto 200px;            /* Two rows */
  grid-template-columns: repeat(3, 1fr);     /* Shorthand for equal columns */
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  gap: 1rem;               /* Short for row-gap and column-gap */
  justify-items: stretch;  /* Inline axis alignment of items */
  align-items: stretch;    /* Block axis alignment of items */
}

/* On grid ITEMS */
.item {
  grid-column: 1 / 3;        /* Span from line 1 to line 3 */
  grid-row: 2 / 4;           /* Span rows 2–4 */
  grid-column: span 2;       /* Span 2 columns from current position */
  grid-area: header;         /* Place in named area */
  justify-self: center;      /* Override container's justify-items */
  align-self: end;           /* Override container's align-items */
}
```

---

## Common Media Queries

```css
/* Mobile-first breakpoints (min-width) */
/* Small (sm) — 640px+ */
@media (min-width: 640px) { }

/* Medium (md) — 768px+ */
@media (min-width: 768px) { }

/* Large (lg) — 1024px+ */
@media (min-width: 1024px) { }

/* Extra large (xl) — 1280px+ */
@media (min-width: 1280px) { }

/* Dark mode preference */
@media (prefers-color-scheme: dark) { }

/* Reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* Print */
@media print { }
```

---

## CSS Custom Properties

```css
/* Define on :root for global scope */
:root {
  --color-primary: #3b82f6;
  --color-text: #111827;
  --spacing-base: 1rem;
  --font-size-lg: 1.125rem;
}

/* Use with var() */
.button {
  background-color: var(--color-primary);
  padding: var(--spacing-base);
  font-size: var(--font-size-lg);
}

/* Provide a fallback value */
.card {
  color: var(--color-card-text, #374151);  /* Falls back if --color-card-text is not set */
}

/* Override in a component scope */
.dark-card {
  --color-card-text: #f9fafb;
}

/* Change at runtime with JavaScript */
/* document.documentElement.style.setProperty('--color-primary', '#e11d48'); */
```

---

## Useful Functions

| Function | Description | Example |
|----------|-------------|---------|
| `calc()` | Compute a value from mixed units | `width: calc(100% - 2rem)` |
| `var()` | Reference a custom property | `color: var(--color-primary)` |
| `clamp()` | Constrain a value between min and max | `font-size: clamp(1rem, 2.5vw, 1.5rem)` |
| `min()` | Use the smallest of several values | `width: min(600px, 100%)` |
| `max()` | Use the largest of several values | `padding: max(1rem, 5vw)` |
| `rgb()` / `hsl()` | Specify a colour | `color: hsl(220, 90%, 56%)` |
| `linear-gradient()` | Create a gradient background | `background: linear-gradient(to right, #3b82f6, #8b5cf6)` |
| `translate()` | Move without affecting flow | `transform: translate(-50%, -50%)` |
| `rotate()` | Rotate an element | `transform: rotate(45deg)` |
| `scale()` | Scale an element | `transform: scale(1.05)` |

---

## At-Rules Quick Reference

| At-Rule | Purpose |
|---------|---------|
| `@import` | Load another CSS file |
| `@media` | Apply rules conditionally based on media features |
| `@keyframes` | Define animation keyframes |
| `@font-face` | Load a custom web font |
| `@layer` | Declare a cascade layer to control specificity ordering |
| `@supports` | Apply rules conditionally based on CSS feature support |
| `@container` | Apply rules based on a parent container's size (container queries) |
| `@scope` | Limit the reach of a selector to a subtree |
