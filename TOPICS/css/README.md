# CSS

> A zero-to-expert path for styling resilient, accessible, responsive interfaces with Cascading Style Sheets.

## Table of Contents
1. [Why Learn CSS?](#why-learn-css)
2. [Prerequisites](#prerequisites)
3. [Module Map](#module-map)
4. [Cross-Links](#cross-links)
5. [Quick Reference](#quick-reference)

## Why Learn CSS?
CSS is the presentation language of the web. It controls how documents look across screen sizes, input methods, languages, user preferences, and devices without changing the underlying meaning of the content.

Learning CSS deeply matters because visual interface work is not only decoration. Layout, spacing, contrast, motion, and responsive behavior all affect whether people can understand and use a product. A strong CSS practitioner can turn semantic [[html]] into durable product surfaces while preserving [[accessibility]] and performance.

CSS has evolved from basic document styling into a modern design engineering platform. The cascade, selectors, layout algorithms, custom properties, media queries, container queries, animations, and architecture patterns let teams build scalable systems rather than one-off pages.

## Prerequisites
- Basic computer literacy: folders, files, and editing plain text.
- [[html]] — helpful for understanding elements, attributes, document structure, and semantic markup.
- [[web-development]] — optional background for browsers, URLs, and developer tools.
- No prior CSS knowledge is assumed; Module 01 starts from ground zero.

## Module Map
| # | Module | Difficulty | Status |
|---|--------|------------|--------|
| 01 | [Introduction and the Cascade](./modules/01_introduction/README.md) | Beginner | [ ] |
| 02 | [Selectors and the Box Model](./modules/02_selectors_box_model/README.md) | Beginner | [ ] |
| 03 | [Layout Fundamentals](./modules/03_layout_fundamentals/README.md) | Intermediate | [ ] |
| 04 | Responsive Design and Media Queries | Intermediate | [ ] |
| 05 | Typography, Color, and Visual Systems | Intermediate | [ ] |
| 06 | Flexbox and Grid Deep Dive | Advanced | [ ] |
| 07 | Cascade Layers, Specificity, and Architecture | Advanced | [ ] |
| 08 | Animation, Transitions, and Interaction States | Advanced | [ ] |
| 09 | Accessibility, Internationalization, and User Preferences | Advanced | [ ] |
| 10 | Performance, Debugging, and Browser Internals | Expert | [ ] |
| 11 | Design Systems and Production CSS Strategy | Expert | [ ] |
| 12 | [Capstone Project](./modules/12_capstone_project/README.md) | Expert | [ ] |

## Cross-Links
- [[html]] — CSS styles structured markup, so semantic HTML is the foundation.
- [[javascript]] — JavaScript often changes classes, attributes, and state that CSS reacts to.
- [[accessibility]] — CSS choices affect readability, focus visibility, motion safety, and usability.
- [[design-systems]] — mature CSS is usually organized around reusable tokens, components, and patterns.

## Quick Reference
| Need | CSS Tool |
|---|---|
| Select an element type | `button { ... }` |
| Select a class | `.card { ... }` |
| Select an id | `#site-header { ... }` |
| Declare a property | `property: value;` |
| Reuse a value | `--space-3: 1rem;` and `var(--space-3)` |
| Control layout | `display: flex;` or `display: grid;` |
| Respond to viewport size | `@media (min-width: 48rem) { ... }` |
| Respond to container size | `@container (min-width: 32rem) { ... }` |
| Respect reduced motion | `@media (prefers-reduced-motion: reduce) { ... }` |

```css
/* Minimal CSS rule: selector, declaration block, property, and value. */
.card {
  padding: 1rem;
  border: 1px solid currentColor;
}
```
