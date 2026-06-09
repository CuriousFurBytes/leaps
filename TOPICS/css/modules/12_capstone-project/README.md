# Module 12: Capstone Project — Build a Complete Design System

[← Module 11](../11_performance-and-accessibility/) | [Topic Home](../../README.md)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-expert-red)
![Time](https://img.shields.io/badge/time-15--20h-orange)

---

## Overview

This is the capstone module. You will build a **complete, responsive CSS design system** from scratch — including design tokens, base styles, a component library, dark mode support, and full accessibility compliance. This is not a tutorial with a prescribed solution. It is a real project: open-ended, ambitious, and representative of the kind of work a senior front-end developer would produce.

A design system is the canonical set of styles, components, and guidelines that a product team uses to build consistent user interfaces. Companies like Stripe, Shopify, GitHub, and Atlassian publish their design systems publicly (Stripe's Carbon, Shopify's Polaris, GitHub's Primer, Atlassian's Design System). You will build something of similar scope — scaled for a single developer — that synthesises every concept from this topic.

> [!IMPORTANT]
> This module provides scaffolding, milestones, and staged hints. It does **not** provide a complete solution to copy. The build work is yours. Use the Help sections when genuinely stuck. The goal is for you to leave this module having made all the key decisions and built something you can show as real work.

---

## Project Brief

**What you are building:** A design system called `[your-name]-ui` — a single CSS file (or organised set of CSS files) and a demonstration HTML page that shows all components in use.

**What it must include:**

1. **Design tokens** — CSS custom properties for all colours, spacing, typography, border radii, and shadows
2. **Dark mode** — full dark mode support using `@media (prefers-color-scheme: dark)` and token overrides
3. **Base styles** — reset/normalise, `box-sizing: border-box`, accessible focus styles, `prefers-reduced-motion` strategy
4. **Typography scale** — at least 5 font sizes from a defined scale, applied consistently
5. **Component library** — at minimum:
   - Button (with variants: primary, secondary, danger; and states: hover, focus, active, disabled)
   - Form elements (text input, checkbox, radio button, select — all styled and accessible)
   - Card component (image, heading, body text, footer action)
   - Navigation bar (responsive, keyboard accessible)
   - Badge / tag component
6. **Accessibility compliance** — every component passes WCAG 2.1 AA colour contrast; all interactive elements have visible focus indicators
7. **Documentation page** — the demonstration HTML file should double as documentation: show each component, with its class names labelled

---

## Milestones

Work through these milestones in order. Each builds on the previous and is a natural commit point.

### Milestone 1 — Design Tokens

Create your token system as CSS custom properties on `:root`. Define:
- A colour palette: primary (5 shades), neutral (9 shades), semantic colours (success, warning, error, info)
- Spacing scale (at least 8 steps, e.g. 4px → 64px)
- Typography: 2–3 font families, 6 font sizes, 3 font weights, 3 line heights
- Border radii (none, sm, md, lg, full/pill)
- Shadows (sm, md, lg)
- Dark mode variants for all semantic colours

**Deliverable:** A `tokens.css` file and a verification that changing one token updates all components that use it.

---

### Milestone 2 — Base Styles

Write the reset/base layer:
- `box-sizing: border-box` for everything
- Remove default margins on headings and paragraphs
- Set `body` font using your token
- Accessible focus ring (`:focus-visible` with an offset outline using your primary colour token)
- `prefers-reduced-motion` rule that disables all transitions and animations for users who request it
- `forced-colors` support: ensure interactive elements are distinguishable

**Deliverable:** A `base.css` file. Test by opening a plain HTML page and verifying all defaults are sensible.

---

### Milestone 3 — Typography

Build the typography component:
- Define heading styles (`h1`–`h6`) using your type scale tokens
- Define `body` text, `small` text, `lead` (large intro paragraph), and a `code`/`pre` monospace style
- Implement a `.prose` container class that applies readable article typography (max-width, line-height, paragraph spacing)

**Deliverable:** A `typography.css` file and a demo section in your HTML showing all type styles.

---

### Milestone 4 — Button Component

Build the button component — arguably the most complex single component in any design system:
- `.btn` base class
- Variants: `.btn--primary`, `.btn--secondary`, `.btn--danger`, `.btn--ghost`
- Sizes: `.btn--sm`, `.btn--lg`
- States: `:hover`, `:focus-visible`, `:active`, `:disabled` (must be visually distinct from the default state)
- Icon support: `.btn--icon-left`, `.btn--icon-right` (using Flexbox)

**Deliverable:** A `button.css` file. Test every variant and state manually and with a colour contrast tool.

---

### Milestone 5 — Form Components

Build styled, accessible form components:
- Text input (default, focus, error, disabled states)
- Checkbox and radio button (custom-styled with `appearance: none`, retaining keyboard accessibility)
- Select element
- Textarea
- Form label + input + helper text + error message layout

**Deliverable:** A `forms.css` file. Verify: tab through the form — all elements must show visible focus indicators.

---

### Milestone 6 — Card and Navigation

Build the remaining components:
- **Card** — image (responsive, `object-fit: cover`), heading, body, footer with action
- **Navigation bar** — horizontal on desktop (Flexbox), stacked on mobile (media query), keyboard accessible

**Deliverable:** `card.css` and `nav.css`.

---

### Milestone 7 — Documentation Page

Build the `index.html` that demonstrates and documents the entire system:
- All components shown in their default, hover, focus, active, and disabled states
- Component names and class names are visible as labels
- Dark mode: when you enable dark mode on your OS, the entire page should switch
- A token reference table showing all custom property names and their light/dark values

**Deliverable:** `index.html`. Run Lighthouse (Chrome DevTools → Lighthouse tab) and aim for ≥ 90 on Accessibility.

---

## Acceptance Criteria

Your completed capstone must satisfy all of these:

- [ ] All design tokens are CSS custom properties and every component uses them (no hardcoded colour values in component files)
- [ ] Dark mode works automatically based on system preference
- [ ] All text meets WCAG 2.1 AA contrast (4.5:1 for body text, 3:1 for large text) in both light and dark modes
- [ ] All interactive elements have a visible `:focus-visible` state
- [ ] `prefers-reduced-motion: reduce` disables all CSS animations and transitions
- [ ] The page is navigable by keyboard alone (Tab, Shift+Tab, Enter, Space)
- [ ] Lighthouse Accessibility score ≥ 90
- [ ] The `index.html` documentation page accurately shows all components and their class API

---

## Getting Unstuck

<details>
<summary>Milestone 1 hint — Design Tokens</summary>

Start with colours. A common approach is to define primitive tokens first (raw colours) and then semantic tokens (which primitive a semantic concept maps to):

```css
:root {
  /* Primitive colours */
  --color-blue-500: #3b82f6;
  --color-blue-600: #2563eb;
  --color-gray-900: #111827;
  --color-gray-100: #f3f4f6;

  /* Semantic tokens (reference primitives) */
  --color-action-primary: var(--color-blue-500);
  --color-action-primary-hover: var(--color-blue-600);
  --color-text: var(--color-gray-900);
  --color-surface: var(--color-gray-100);
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-text: var(--color-gray-100);      /* Flip text and surface for dark mode */
    --color-surface: var(--color-gray-900);
  }
}
```

Only semantic tokens need dark mode overrides. Primitive tokens never change.

See also: Module 06 (Custom Properties), Module 09 (Design Tokens section).

</details>

<details>
<summary>Milestone 2 hint — Accessible Focus Ring</summary>

The modern accessible focus ring uses `:focus-visible` (only shows for keyboard navigation, not mouse clicks) and `outline-offset` to separate the ring from the element:

```css
:focus-visible {
  outline: 2px solid var(--color-action-primary);
  outline-offset: 2px;
  border-radius: 2px; /* Match the element's border-radius */
}
```

Never use `outline: none` without providing an alternative focus indicator. See Module 11 (Focus Styles).

</details>

<details>
<summary>Milestone 4 hint — Disabled Button Styles</summary>

A disabled button must be visually distinct but not confusable with an active state. A common pattern:

```css
.btn:disabled,
.btn[aria-disabled="true"] {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}
```

Always test with a keyboard: a disabled button should not receive focus (use the `disabled` HTML attribute, not just CSS). The `aria-disabled="true"` version receives focus but announces itself as disabled — useful when you want keyboard users to discover why a button is unavailable.

</details>

<details>
<summary>Milestone 5 hint — Custom Checkbox</summary>

Styling checkboxes requires hiding the native checkbox and creating a custom one with `::before`:

```css
.checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox input[type="checkbox"] {
  appearance: none;
  width: 1rem;
  height: 1rem;
  border: 2px solid var(--color-border);
  border-radius: 2px;
  position: relative;
  flex-shrink: 0;
}

.checkbox input[type="checkbox"]:checked {
  background-color: var(--color-action-primary);
  border-color: var(--color-action-primary);
}

.checkbox input[type="checkbox"]:checked::before {
  content: "";
  display: block;
  width: 0.35rem;
  height: 0.6rem;
  border: 2px solid white;
  border-top: none;
  border-left: none;
  transform: rotate(45deg) translate(1px, -1px);
  position: absolute;
  left: 3px;
  top: 1px;
}

.checkbox input[type="checkbox"]:focus-visible {
  outline: 2px solid var(--color-action-primary);
  outline-offset: 2px;
}
```

</details>

<details>
<summary>General hint — File organisation</summary>

A sensible file structure for this project:

```
my-design-system/
├── index.html           ← documentation page
├── css/
│   ├── tokens.css       ← Milestone 1
│   ├── base.css         ← Milestone 2
│   ├── typography.css   ← Milestone 3
│   ├── button.css       ← Milestone 4
│   ├── forms.css        ← Milestone 5
│   ├── card.css         ← Milestone 6
│   ├── nav.css          ← Milestone 6
│   └── main.css         ← @import all of the above (or link them individually in <head>)
```

Import order matters — tokens must load before any component that uses them.

</details>

---

## Further Reading

- GitHub Primer Design System: [primer.style](https://primer.style) — a real open-source design system to study
- Radix UI Themes: see how design tokens are documented alongside components
- [web.dev — Building a design system](https://web.dev/learn/design/) — Google's practical design system series
- Module 06: Typography and Color — CSS custom properties reference
- Module 09: CSS Architecture — BEM and design token naming conventions
- Module 11: Performance and Accessibility — WCAG contrast and focus style reference
