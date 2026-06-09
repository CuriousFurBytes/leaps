# Module 02: Selectors and the Box Model

> Learn selectors, specificity, display types, and box sizing through practical CSS examples and the mental models behind them.

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

## Overview
CSS is declarative: you describe the visual result you want, then the browser combines your rules with user-agent defaults, inherited values, user preferences, and device constraints. That makes CSS powerful, but it also means the answer to "why did this look that way?" is rarely one line of code.

This module introduces the core ideas needed for reliable styling: selectors, declarations, the cascade, inheritance, and browser defaults. The goal is not to memorize every property. The goal is to learn how CSS decides which value wins, where values come from, and how a small stylesheet can transform structured [[html]] into an understandable interface.

## Prerequisites
- Module 01 in this topic.
- A text editor and a modern browser with developer tools.

## Objectives
By the end of this module, you will be able to:
- Explain how CSS rules connect selectors to declarations.
- Predict simple cascade and inheritance outcomes.
- Write and debug small stylesheets for semantic HTML.
- Use browser developer tools to inspect matched rules.

## Theory
### CSS as a Styling Contract
CSS was created so document structure and visual presentation could evolve separately. Early web pages mixed content and appearance directly in markup, which made sites hard to maintain. CSS moved presentation into a stylesheet: HTML states what something is, while CSS states how it should be presented in a given context.

A CSS rule has a selector and a declaration block. The selector identifies the elements to style; each declaration assigns a value to a property. The browser parses all applicable stylesheets, adds its own default stylesheet, considers user preferences, and computes a final value for every property on every element.

```html
<!-- Semantic HTML gives CSS meaningful hooks without describing appearance. -->
<article class="card">
  <h2>Weather report</h2>
  <p>Clear skies with a light breeze.</p>
</article>
```

```css
/* The selector targets article elements with class="card". */
.card {
  /* Padding creates inner space between content and the card edge. */
  padding: 1rem;
  /* Border uses currentColor, so it follows the inherited text color. */
  border: 1px solid currentColor;
}
```

### The Cascade and Inheritance
The cascade is the conflict-resolution algorithm that decides which declaration wins when multiple declarations target the same property. It considers origin, importance, cascade layers, specificity, source order, and whether a value is inherited. This is why a later class rule can beat an earlier class rule, but a more specific selector may beat a later broad selector.

Inheritance is different from the cascade. Some properties, especially text-related properties like `color` and `font-family`, naturally pass from parent to child. Others, like `margin` and `border`, do not. Understanding this distinction prevents over-styling and makes themes easier to maintain.

```css
/* The body color is inherited by descendants unless they set their own color. */
body {
  color: #1f2937;
  font-family: system-ui, sans-serif;
}

/* This rule affects only links, overriding the inherited color. */
a {
  color: #0f766e;
}
```

### Inspecting Computed Results
Because CSS is resolved by the browser, inspection is a core skill. Developer tools show which rules matched, which declarations were overridden, and what computed value the element actually received. Good CSS practice is investigative: write a rule, inspect the result, and adjust the smallest useful selector.

```css
/* Prefer a focused class selector over a fragile chain of element selectors. */
.notice {
  background: #fef3c7;
  padding: 0.75rem;
}

/* State can be represented with an additional class. */
.notice.is-urgent {
  background: #fee2e2;
}
```

## Key Concepts
- **Rule:** A selector plus a declaration block. Rules are the basic unit of CSS behavior.
- **Declaration:** A `property: value` pair. A declaration only matters if the property accepts the value and the rule matches an element.
- **Cascade:** The browser algorithm that chooses the winning declaration when multiple candidates apply.
- **Inheritance:** The mechanism by which selected property values flow from parent elements to descendants.
- **Computed value:** The resolved value after the browser combines defaults, inheritance, cascade, and value processing.

## Examples
### Style a Simple Card
Problem: make a reusable card that inherits site text color but adds structure.

```css
.card {
  padding: 1rem;
  border: 1px solid currentColor;
  border-radius: 0.5rem;
}
```

This uses a class because the style describes a reusable component role rather than every `article` element on the page.

## Common Pitfalls
### Using Appearance as the Only Hook
Wrong:

```css
.red-box {
  color: red;
}
```

Correct:

```css
.error-message {
  color: #b91c1c;
}
```

Name classes for meaning so future design changes do not make the class misleading.

### Fighting Inheritance Unnecessarily
Wrong:

```css
.card p,
.card li,
.card a {
  font-family: system-ui, sans-serif;
}
```

Correct:

```css
.card {
  font-family: system-ui, sans-serif;
}
```

Set inherited properties once on the nearest useful ancestor.

### Assuming Last Rule Always Wins
Wrong:

```css
#hero .title {
  color: purple;
}
.title {
  color: green;
}
```

Correct:

```css
.hero-title {
  color: green;
}
```

Specificity can beat source order, so keep selectors intentionally simple.

## Cross-Links
- [[html]]
- [[web-development]]
- [[accessibility]]

## Summary
- CSS maps structured documents to visual presentation.
- A rule combines a selector with declarations.
- The cascade resolves conflicts between competing declarations.
- Inheritance passes some property values from parents to descendants.
- Browser developer tools are essential for understanding computed styles.
