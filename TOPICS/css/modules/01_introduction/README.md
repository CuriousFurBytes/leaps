# Module 01: Introduction to CSS

[← Topic Home](../../README.md) | [Next → Module 02](../02_selectors-and-specificity/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-beginner-green)
![Time](https://img.shields.io/badge/time-4h-orange)

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Key Concepts](#key-concepts)
6. [Examples](#examples)
7. [Common Pitfalls](#common-pitfalls)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

---

## Overview

This module introduces CSS — what it is, why it exists, and the three fundamental mechanisms that govern all CSS behaviour: the **cascade**, **specificity**, and **inheritance**. These are not advanced topics to defer until later; they are the operating logic of the entire language. Every layout bug, every unexpected style, and every debugging session you will ever have with CSS will trace back to one of these three mechanisms.

CSS exists because the web needed a way to separate *what* a page says (HTML content and structure) from *how* it looks (presentation). Before CSS, developers used HTML attributes and elements like `<font>`, `<center>`, and `bgcolor` to style pages. Every visual change required touching the HTML. On a site with hundreds of pages, changing the font meant editing hundreds of files. CSS solved this by letting one stylesheet drive the appearance of an entire site.

By the end of this module you will be able to write your first stylesheet, attach it to an HTML page, and — crucially — predict which rule the browser will apply when two rules compete. That predictive ability is what distinguishes CSS that is easy to maintain from CSS that becomes a mystery.

---

## Prerequisites

- A working understanding of HTML: elements, attributes, nesting, and the concept of the DOM (Document Object Model)
- A text editor and a modern web browser with developer tools (Chrome DevTools or Firefox DevTools)
- No prior CSS knowledge is required

> [!TIP]
> Open your browser's developer tools (F12 in most browsers) as you read. The "Elements" panel lets you inspect any element's applied styles in real time — it is the single best learning tool for CSS.

---

## Objectives

By the end of this module, you will be able to:

1. Explain what CSS is, why it exists, and how it relates to HTML
2. Write a valid CSS rule with a selector, property, and value
3. Link an external stylesheet to an HTML document
4. Describe the three-step cascade algorithm (origin → specificity → order)
5. Calculate the specificity score of any selector
6. Identify which CSS properties inherit and which do not
7. Use `inherit`, `initial`, and `unset` to control inherited values deliberately
8. Debug a simple specificity conflict using browser developer tools

---

## Theory

### CSS Syntax and Rule Structure

A CSS stylesheet is a collection of **rules**. Each rule consists of two parts: a **selector** and a **declaration block**.

```css
/* This is a CSS rule */
p {                           /* ← selector: targets all <p> elements */
  color: #374151;             /* ← declaration: property "color", value "#374151" */
  font-size: 1rem;            /* ← declaration: property "font-size", value "1rem" */
  line-height: 1.6;           /* ← declaration: property "line-height", value "1.6" */
}
```

The **selector** identifies which element(s) the rule applies to. The **declaration block** (everything between `{` and `}`) contains one or more **declarations**. Each declaration is a **property** (a named characteristic, like `color` or `font-size`) paired with a **value**.

There are three ways to attach CSS to an HTML document:

```html
<!-- Method 1: External stylesheet (strongly preferred for all real projects) -->
<link rel="stylesheet" href="styles.css">

<!-- Method 2: Internal stylesheet (acceptable for single-page demos) -->
<style>
  p { color: navy; }
</style>

<!-- Method 3: Inline style (avoid — it has the highest specificity and is hard to override) -->
<p style="color: navy;">Some text</p>
```

External stylesheets are the correct approach for any project with more than one page. They allow a single file to control the appearance of an entire site, and they are cached by the browser after the first request.

---

### How Browsers Apply CSS

When a browser loads an HTML page, it follows a defined sequence to produce the final visual output:

1. **Parse HTML** — the browser reads the HTML and builds a tree of nodes called the **DOM** (Document Object Model)
2. **Parse CSS** — the browser reads all CSS (external files, `<style>` blocks, inline styles) and builds a second tree called the **CSSOM** (CSS Object Model)
3. **Compute styles** — for each DOM element, the browser works out which CSS declarations apply to it, applying the **cascade algorithm** to resolve conflicts
4. **Layout** — the browser calculates the size and position of every box on the page
5. **Paint** — the browser draws the pixels to the screen

Understanding step 3 — the computation of styles — is the focus of this module. The cascade algorithm is the set of rules the browser follows to answer: "When two or more declarations try to set the same property on the same element, which one wins?"

---

### The Cascade Algorithm

The word "cascading" in CSS refers to this decision algorithm. It has three stages, applied in order:

**Stage 1 — Origin and Importance**

CSS rules come from multiple *origins*. From lowest to highest priority:

1. **User-agent stylesheet** — the browser's built-in styles (e.g., `<h1>` is bold, `<a>` is blue). Every browser ships with one.
2. **Author stylesheet** — the CSS written by the web developer (that's you). This overrides user-agent styles.
3. **User stylesheet** — styles set by the browser user (rare today, but was more common when users customised accessibility settings via browser CSS)

The `!important` annotation reverses this order for the property it is applied to, making even user-agent `!important` rules win. This is why `!important` exists: it allows users to override author styles for accessibility reasons (e.g., forcing a minimum font size). Authors who overuse it undermine that intent.

**Stage 2 — Specificity**

When two rules are from the same origin and neither uses `!important`, the more *specific* selector wins.

**Stage 3 — Order of Appearance**

When two rules have identical origin and identical specificity, the one that appears *later* in the stylesheet wins. This is the simplest stage: later = wins.

```css
/* Both rules have the same specificity: (0,1,0) */
/* Order decides: the second rule wins */
.title {
  color: navy;    /* This loses */
}

.title {
  color: crimson; /* This wins — it appears later */
}
```

---

### Specificity — The Scoring System

Specificity is a three-component score, written as `(A, B, C)`:

- **A** — count the number of **ID selectors** (`#id`) in the selector
- **B** — count the number of **class selectors** (`.class`), **attribute selectors** (`[type="text"]`), and **pseudo-classes** (`:hover`, `:focus`)
- **C** — count the number of **type selectors** (`p`, `div`, `h1`) and **pseudo-elements** (`::before`, `::after`)

The universal selector (`*`) and combinators (` `, `>`, `+`, `~`) contribute zero to specificity.

Compare scores left to right. A higher A beats any B or C. If A is tied, compare B. If B is tied, compare C.

```css
/* Specificity calculations */

p              { }  /* (0,0,1) — one type selector */
.warning       { }  /* (0,1,0) — one class selector */
p.warning      { }  /* (0,1,1) — one type + one class */
#sidebar       { }  /* (1,0,0) — one ID selector */
#sidebar p     { }  /* (1,0,1) — one ID + one type */
.nav > a:hover { }  /* (0,2,1) — two pseudo/class + one type */
```

Inline styles (written as the `style` attribute on an element) have the highest specificity of all — higher than any selector. This is why overriding inline styles from a stylesheet is so difficult, and why inline styles should be used sparingly.

`!important` is not part of the specificity score. It is a separate mechanism that declares "this declaration must win regardless of specificity". Competing `!important` declarations are then sorted by specificity and origin — but this is an edge case you should avoid by design.

```css
/* Example: which color applies to a <p class="warning" id="alert"> element? */

p               { color: black;  }  /* (0,0,1) — loses */
.warning        { color: orange; }  /* (0,1,0) — loses */
#alert          { color: red;    }  /* (1,0,0) — WINS */
p.warning       { color: yellow; }  /* (0,1,1) — loses to #alert */
```

---

### Inheritance — Values That Flow Downward

Some CSS properties **inherit**: their computed value flows automatically from a parent element to all its descendants unless overridden. Others do not inherit.

**Properties that inherit by default** (a non-exhaustive list):

- Typography: `color`, `font-family`, `font-size`, `font-weight`, `font-style`, `line-height`, `letter-spacing`, `text-align`, `text-transform`
- Lists: `list-style`, `list-style-type`
- Tables: `border-collapse`
- Cursor: `cursor`, `visibility`

**Properties that do NOT inherit by default** (a non-exhaustive list):

- Box model: `margin`, `padding`, `border`, `width`, `height`
- Backgrounds: `background`, `background-color`, `background-image`
- Layout: `display`, `position`, `float`, `top`, `left`

This design is intentional. It would be inconvenient if setting `background: red` on a `<body>` made every paragraph, span, and link red too. But it *is* useful that setting `font-family` on `<body>` makes every element on the page use that font by default.

You can explicitly control inheritance using four special values that apply to *any* property:

```css
.child {
  color: inherit;   /* Force inheritance — use parent's computed value */
  color: initial;   /* Reset to the property's CSS spec default (often 'black' for color) */
  color: unset;     /* If the property normally inherits, act like inherit; if not, act like initial */
  color: revert;    /* Reset to the browser's user-agent stylesheet value */
}
```

The `unset` value is especially practical: it clears any author-applied value without knowing in advance whether the property inherits.

```css
/* A utility class that removes all inherited font styling without knowing which fonts were set */
.reset-text {
  font: unset;    /* Resets font-family, font-size, font-weight, etc. in one declaration */
  color: unset;
}
```

---

## Key Concepts

**cascade** — The three-stage algorithm (origin, specificity, order) that the browser uses to determine which CSS declaration applies when multiple declarations target the same property on the same element. See [[css/glossary#cascade]].

**specificity** — A three-component score (A, B, C) measuring how precisely a selector targets an element. Higher specificity wins over lower specificity when both rules are from the same origin. Inline styles beat all selectors; `!important` beats all specificity. See [[css/glossary#specificity]].

**inheritance** — The mechanism by which certain CSS property values flow automatically from a parent element to its children. Typography properties like `color` and `font-family` inherit; layout properties like `margin` and `border` do not. See [[css/glossary#inheritance]].

**selector** — The part of a CSS rule that identifies which element(s) to style. Can range from a type selector (`p`) targeting all paragraphs to a compound selector (`#sidebar nav > a:hover`) targeting a very specific subset of links. See [[css/glossary#selector]].

**declaration** — A single `property: value` pair inside a CSS rule's declaration block. Multiple declarations are separated by semicolons.

**rule** — A complete CSS statement consisting of a selector and a declaration block: `selector { property: value; }`.

**user-agent stylesheet** — The browser's built-in default CSS. It is why headings are bold and links are blue before you write a single line of CSS. All author stylesheets override it (unless a user-agent rule uses `!important`).

**`!important`** — An annotation appended to a declaration value (`color: red !important`) that causes it to win the cascade regardless of specificity. Should be reserved for user accessibility overrides and narrow utility classes. Overusing it creates "specificity wars" where every rule needs `!important` to work.

---

## Examples

### Example 1 — Writing and Linking a Stylesheet

A minimal HTML page with an external stylesheet:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My First CSS</title>
  <!-- Link the external stylesheet — path is relative to this HTML file -->
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <h1>Hello, CSS</h1>
  <p class="intro">This paragraph has a class.</p>
  <p>This paragraph has no class.</p>
</body>
</html>
```

```css
/* styles.css */

/* Type selector — applies to all <p> elements */
p {
  color: #374151;       /* Dark grey text */
  font-size: 1rem;
  line-height: 1.6;
}

/* Class selector — applies only to elements with class="intro" */
.intro {
  color: #1d4ed8;       /* Blue text — overrides the p rule because .intro has higher specificity */
  font-weight: bold;
}

/* Type selector — applies to <h1> */
h1 {
  font-size: 2rem;
  color: #111827;
}
```

The `<p class="intro">` element will be blue and bold because `.intro` (specificity `0,1,0`) beats `p` (specificity `0,0,1`).

---

### Example 2 — Specificity in Action

This example demonstrates specificity resolution with three competing rules:

```html
<section id="main-content">
  <p class="note warning">Be careful here.</p>
</section>
```

```css
/* Rule A — type selector */
p {
  color: black;     /* Specificity: (0,0,1) */
}

/* Rule B — class selector */
.warning {
  color: orange;    /* Specificity: (0,1,0) — beats Rule A */
}

/* Rule C — descendant with ID */
#main-content p {
  color: navy;      /* Specificity: (1,0,1) — beats Rules A and B */
}
```

The paragraph will be **navy**, because Rule C has an ID selector (A=1), which beats both Rule A (A=0) and Rule B (A=0) regardless of B or C values.

To verify: open the browser DevTools, select the element, and look at the "Computed" tab — you will see the winning declaration highlighted and the losing declarations shown with strikethroughs.

---

### Example 3 — Inheritance and `inherit`

This example shows how `color` inherits but `border` does not:

```html
<div class="card">
  <h2>Card Title</h2>     <!-- Will inherit color from .card -->
  <p>Card body text.</p>  <!-- Will inherit color from .card -->
  <a href="#">Learn more</a>  <!-- Will NOT inherit color — browsers override it for links -->
</div>
```

```css
.card {
  color: #1e293b;           /* This inherits to h2, p, and (potentially) a */
  border: 1px solid #e2e8f0; /* This does NOT inherit — only .card gets the border */
  padding: 1.5rem;
  background: #ffffff;       /* Does NOT inherit */
}

/* Force the link inside .card to use the inherited color */
.card a {
  color: inherit;   /* Explicitly inherit from .card instead of using the browser's default link color */
}
```

Without `color: inherit` on `.card a`, the link would be blue (or purple if visited) because the browser's user-agent stylesheet sets `a { color: -webkit-link; }` which takes priority over inherited values.

---

## Common Pitfalls

### Pitfall 1 — Specificity Wars from Over-Qualifying Selectors

**The mistake:** Writing overly long selectors to "make sure" a rule applies. This increases specificity so high that overriding it later requires even longer selectors or `!important`.

```css
/* Wrong — needlessly long, high specificity */
body main section article .card .card-title h2 {
  font-size: 1.5rem;
}
```

```css
/* Right — use the simplest selector that is specific enough */
.card-title {
  font-size: 1.5rem;
}
```

Why this happens: developers see a rule not applying and instinctively add more context. The real fix is to understand which other rule is winning (via DevTools) and resolve the conflict at its source.

---

### Pitfall 2 — Abusing `!important`

**The mistake:** Using `!important` as a first resort to "force" a style, rather than understanding and fixing the specificity problem.

```css
/* Wrong — this creates a problem: any future override also needs !important */
.button {
  background-color: blue !important;
  color: white !important;
}
```

```css
/* Right — understand WHY the rule wasn't applying, fix the specificity properly */
.button {
  background-color: blue;
  color: white;
}
/* If a previous rule was winning, lower its specificity or restructure the stylesheet */
```

`!important` is appropriate in two narrow cases: in a user accessibility stylesheet (where the user must be able to override author styles), and in small utility classes like `.visually-hidden` where you need an override to be guaranteed regardless of context.

---

### Pitfall 3 — Forgetting That Inline Styles Override Everything

**The mistake:** Writing a stylesheet rule and being confused when it doesn't apply — not realising there is an inline style on the element.

```html
<!-- This inline style will win over any external stylesheet rule -->
<p style="color: red;">I will always be red.</p>
```

```css
/* This rule loses — inline styles have higher specificity than any selector */
.content p {
  color: navy;  /* Will not apply */
}
```

```css
/* Wrong fix — adding !important to fight the inline style */
.content p {
  color: navy !important;  /* Works but is now fragile */
}
```

The correct fix is to remove the inline style from the HTML. Inline styles mix presentation into structure, defeating the purpose of having a stylesheet. If the inline style is coming from a third-party library or CMS you cannot control, document the reason for using `!important`.

---

### Pitfall 4 — Confusing `display: none` and `visibility: hidden`

These are related but different:

```css
/* Wrong — using the wrong property for the intended behaviour */
.hidden-but-takes-space {
  display: none;        /* Removes the element from flow — takes no space */
}

/* Right */
.hidden-but-takes-space {
  visibility: hidden;   /* Element is invisible but still occupies space */
}
```

`display: none` removes the element from the layout entirely — other elements will fill its space. `visibility: hidden` makes it invisible but preserves its layout footprint. Choose deliberately based on which behaviour you want.

---

## Cross-Links

- [[javascript-typescript-react]] — JavaScript can read and modify CSS via `element.style`, `element.classList`, and `getComputedStyle()`. Understanding the cascade is necessary to predict how JS style changes interact with stylesheet rules.
- [[networks]] — CSS files are fetched over HTTP. Understanding how `<link rel="stylesheet">` affects the critical rendering path and how HTTP caching interacts with stylesheet versioning is covered in [[networks]].
- [[qa-testing]] — Visual regression testing and accessibility auditing (WCAG colour contrast, focus visibility) rely on a thorough understanding of applied styles. See [[qa-testing]] for tooling like axe and Playwright visual snapshots.

---

## Summary

- CSS stands for Cascading Style Sheets and its purpose is to separate presentation (how things look) from structure (the HTML content itself).
- A CSS rule consists of a **selector** and a **declaration block** containing one or more `property: value` declarations.
- The browser resolves conflicts between competing CSS rules using the **cascade algorithm**, which checks three things in order: (1) origin and importance, (2) specificity, (3) order of appearance.
- **Specificity** is a three-part score (A, B, C) where ID selectors contribute to A, class/attribute/pseudo-class selectors to B, and type/pseudo-element selectors to C. Higher A beats any B or C; compare left-to-right.
- **Inheritance** means that certain properties (primarily typography properties like `color`, `font-family`, `line-height`) pass their values from parent elements to children. Layout and spacing properties do not inherit.
- You can control inheritance explicitly with `inherit` (force inheritance), `initial` (reset to spec default), `unset` (inherit if it normally would, otherwise initial), and `revert` (reset to user-agent default).
- `!important` overrides all specificity; use it only when genuinely necessary (accessibility overrides, narrow utility classes).
- The browser's DevTools are your best friend for debugging CSS — the Computed styles panel shows which rule is winning and why.
