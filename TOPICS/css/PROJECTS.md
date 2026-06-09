# Projects: CSS — Cascading Style Sheets

> These projects range from beginner to expert. Each project is designed to be built by the learner — not copied from a solution. Start with a project that matches your current module progress.

---

## Beginner Projects

### Project 1 — Style a Blog Page

**Difficulty:** Beginner
**Recommended after:** Module 03
**Estimated time:** 2–4 hours

**Brief:**
Take a plain, unstyled HTML blog page (with a header, navigation, 2–3 article summaries, and a footer) and style it from scratch using only the fundamentals covered in Modules 01–03.

**Requirements:**
- Choose a readable font stack (system fonts are fine — no web fonts required)
- Set a consistent colour palette with at least a primary, background, and text colour
- Apply appropriate spacing (padding and margin) to all major sections
- Style the navigation links with `:hover` effects
- Make the article summaries visually distinct from the page background

**Acceptance Criteria:**
- No layout bugs: body text does not overflow its container
- No mysterious extra spacing from default browser styles (use a simple reset or `box-sizing: border-box`)
- Looks intentional — not like an unstyled page

**What you will practise:** Selectors, cascade, inheritance, box model, basic typography, pseudo-classes

---

### Project 2 — Create a Card Component

**Difficulty:** Beginner
**Recommended after:** Module 03
**Estimated time:** 2–3 hours

**Brief:**
Build a reusable card component that could represent a product, a blog post, or a team member. The card should include an image, a heading, a short paragraph, and a button.

**Requirements:**
- Image fills the full width of the card and is constrained to a fixed height (with `object-fit: cover`)
- Card has a border or shadow to lift it off the page background
- Button has distinct `:hover` and `:focus` states
- Cards should look good at both narrow (320 px) and wide (600 px) widths

**Acceptance Criteria:**
- Card uses the border-box model consistently
- No image distortion regardless of image aspect ratio
- Focus styles are visible (do not set `outline: none` without a replacement)

**What you will practise:** Box model, `object-fit`, pseudo-classes, borders, `box-shadow`

---

## Intermediate Projects

### Project 3 — Responsive Navigation and Hero Section

**Difficulty:** Intermediate
**Recommended after:** Module 07
**Estimated time:** 4–6 hours

**Brief:**
Build a responsive page header with a navigation bar (that collapses to a hamburger-style layout on small screens — CSS only, no JavaScript) and a full-viewport hero section with a centred call-to-action.

**Requirements:**
- Navigation is horizontal on wide screens and stacked vertically on narrow screens (use a media query)
- Hero section fills the full viewport height (`100vh` or `100dvh`)
- Hero has a background image with `background-size: cover` and a text overlay with sufficient contrast
- Call-to-action button is centred using Flexbox

**Acceptance Criteria:**
- Looks polished at 375 px (iPhone SE), 768 px (tablet), and 1280 px (desktop)
- Text in the hero is readable against the background image at all sizes
- Navigation links have visible `:hover` and `:focus` states

**What you will practise:** Flexbox, responsive media queries, viewport units, background properties

---

### Project 4 — CSS-Only Accordion

**Difficulty:** Intermediate
**Recommended after:** Module 08
**Estimated time:** 3–5 hours

**Brief:**
Build a functional accordion (collapsible FAQ component) using only HTML and CSS — no JavaScript. At least 4 items, where clicking an item expands its content panel.

**Technique hint:** Use the `<details>` and `<summary>` HTML elements, or use the `:checked` pseudo-class on a hidden checkbox to control panel visibility. Both are valid CSS-only approaches.

**Requirements:**
- At least 4 accordion items
- Opening and closing must animate smoothly (use a CSS transition)
- Only one item needs to expand at a time (this is a stretch goal — it is hard to achieve with CSS only; attempt it if you have completed Module 08)
- Keyboard accessible: panels must be operable with Tab and Enter/Space

**Acceptance Criteria:**
- Works without JavaScript
- Animation respects `@media (prefers-reduced-motion: reduce)`
- Keyboard users can expand and collapse panels

**What you will practise:** Transitions, `@keyframes`, pseudo-classes, accessibility-aware animation

---

## Advanced Projects

### Project 5 — Complete Design System

**Difficulty:** Advanced
**Recommended after:** Module 09
**Estimated time:** 10–15 hours

**Brief:**
Build a minimal but complete design system stylesheet — a set of base styles, typography scale, colour tokens, and component styles (buttons, forms, cards, navigation) that could serve as the CSS foundation for a real web application.

**Requirements:**
- Define all design tokens (colours, spacing scale, typography scale, border radii) as CSS custom properties on `:root`
- Implement dark mode using `@media (prefers-color-scheme: dark)` and custom property overrides
- Use BEM or another documented naming methodology consistently throughout
- Include at least: a button component (with size variants and state variants), a form component, and a card component
- Write a brief `README.md` inside the project documenting the token names and how to use the system

**Acceptance Criteria:**
- Swapping the value of one custom property updates every component that uses it
- All components pass WCAG AA colour contrast (use a contrast checker)
- The stylesheet is organised and navigable by a new team member

**What you will practise:** CSS custom properties, dark mode, BEM, component design, documentation

---

## Expert Projects

### Project 6 — Recreate a Complex Site Layout from Scratch

**Difficulty:** Expert
**Recommended after:** Module 12 (Capstone)
**Estimated time:** 15–25 hours

**Brief:**
Choose a publicly accessible, visually complex website (a streaming platform home page, a SaaS marketing site, or a news/magazine home page) and recreate its layout as faithfully as possible using only your own HTML and CSS — no copying source code, no frameworks.

**Rules:**
- You may not view the site's source HTML or CSS — only its rendered appearance
- You may use web fonts (Google Fonts or system fonts)
- JavaScript is only permitted for features that are genuinely impossible in CSS (e.g., a video player)
- You must write a short post-mortem document describing: the hardest layout problem you encountered, how you solved it, and what you would do differently

**Acceptance Criteria:**
- Layout is recognisable as the same site at desktop widths
- Mobile layout is responsive and usable
- The site is navigable by keyboard and passes an automated accessibility scan (no critical errors)
- Post-mortem document is included

**What you will practise:** Everything — this project synthesises the entire topic
