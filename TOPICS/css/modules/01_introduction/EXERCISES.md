# Exercises: Module 01 — Introduction to CSS

## Instructions

Complete each exercise in order. Exercises increase in difficulty.
You will need a text editor and a web browser to complete these exercises.
Create a new `.html` file and a companion `.css` file for each exercise (or use one file pair and replace the content between exercises).

Submit your answers by committing your solution files or by editing the `<details>` blocks below with your notes.

---

## Easy Exercises (1–3)

### Exercise 1

**Difficulty:** Easy
**Objective:** Write a valid CSS rule and link it to an HTML page

Create an HTML file `exercise1.html` with a heading and two paragraphs. Create a companion `exercise1.css` and link it using `<link rel="stylesheet">`. Apply these styles:

- All `<h1>` elements: `font-size: 2rem`, `color: #1e293b`
- All `<p>` elements: `font-size: 1rem`, `color: #64748b`, `line-height: 1.7`

Verify the styles apply by opening the file in a browser.

<details>
<summary>Solution</summary>

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Exercise 1</title>
  <link rel="stylesheet" href="exercise1.css">
</head>
<body>
  <h1>My Heading</h1>
  <p>First paragraph of text here.</p>
  <p>Second paragraph of text here.</p>
</body>
</html>
```

```css
h1 {
  font-size: 2rem;
  color: #1e293b;
}

p {
  font-size: 1rem;
  color: #64748b;
  line-height: 1.7;
}
```

</details>

---

### Exercise 2

**Difficulty:** Easy
**Objective:** Identify which CSS origin applies to a property

Open any webpage in your browser. Open DevTools (F12), select an element (e.g., a heading), and look at the "Styles" panel. Answer these questions in the space below:

1. Find a style that comes from the user-agent stylesheet (it will be labelled "user agent stylesheet" in Chrome/Firefox). What property is it?
2. Find a style that is being overridden (shown with a strikethrough). What is overriding it?
3. Is there a style with `!important`? If so, where does it come from?

```
My answers:
1. 
2. 
3. 
```

<details>
<summary>Sample answers (your results will vary by site)</summary>

A common observation on most pages:

1. The `<h1>` or `<p>` element will show user-agent styles like `display: block`, `margin-block-start: 0.67em`, or `font-size: 2em` sourced from the "user agent stylesheet".
2. Often you will see `color`, `font-size`, or `margin` with a strikethrough because the page's author stylesheet has a more specific or later rule.
3. CSS resets and frameworks often use `!important` on utility classes — for example, `display: none !important` on a `.hidden` class.

</details>

---

### Exercise 3

**Difficulty:** Easy
**Objective:** Demonstrate order-of-appearance cascade resolution

Create a stylesheet with two rules that target the same element:

```css
/* Add this to your stylesheet and predict which color the <h2> will be */
h2 {
  color: teal;
}

h2 {
  color: coral;
}
```

1. What colour does the `<h2>` render in? Why?
2. Now swap the order of the two rules. What colour does it render in now?
3. Without looking at the CSS, how would you use DevTools to discover which rule was "winning"?

<details>
<summary>Solution</summary>

1. The `<h2>` renders **coral** — because both rules have the same specificity (`0,0,1`), the one that appears later wins.
2. After swapping, it renders **teal** for the same reason.
3. In DevTools (Elements panel → Styles tab), the winning declaration is displayed normally. Losing declarations are shown with a strikethrough. The panel also shows the source file and line number, so you can see which rule is later in the file.

</details>

---

## Medium Exercises (4–6)

### Exercise 4

**Difficulty:** Medium
**Objective:** Calculate specificity scores and predict the winning rule

For each HTML element below, calculate the specificity of every matching rule and state which color will be applied. Show your work as `(A,B,C)` scores.

```html
<p id="intro" class="lead">Opening paragraph</p>
<a href="#" class="nav-link">Nav item</a>
<button type="submit" class="btn btn-primary">Submit</button>
```

```css
/* Rules for the <p> */
p                 { color: black; }
.lead             { color: gray; }
#intro            { color: navy; }
#intro.lead       { color: teal; }

/* Rules for the <a> */
a                 { color: blue; }
.nav-link         { color: green; }
a.nav-link:hover  { color: red; }  /* Ignore this one — :hover is not currently active */

/* Rules for the <button> */
button            { color: black; }
.btn              { color: white; }
.btn.btn-primary  { color: yellow; }
button.btn        { color: orange; }
```

<details>
<summary>Solution</summary>

**`<p id="intro" class="lead">`:**
- `p` → `(0,0,1)` → black
- `.lead` → `(0,1,0)` → gray
- `#intro` → `(1,0,0)` → navy
- `#intro.lead` → `(1,1,0)` → **teal** ← winner (highest B when A is tied at 1)

**`<a href="#" class="nav-link">`** (`:hover` not active):
- `a` → `(0,0,1)` → blue
- `.nav-link` → `(0,1,0)` → **green** ← winner (higher B)

**`<button type="submit" class="btn btn-primary">`:**
- `button` → `(0,0,1)` → black
- `.btn` → `(0,1,0)` → white
- `.btn.btn-primary` → `(0,2,0)` → yellow
- `button.btn` → `(0,1,1)` → orange
- Winner: `.btn.btn-primary` → `(0,2,0)` — **yellow** (highest B)

</details>

---

### Exercise 5

**Difficulty:** Medium
**Objective:** Observe and control CSS inheritance

Create the following HTML structure:

```html
<div class="article">
  <h2>Article Title</h2>
  <p>Article paragraph with a <a href="#">link inside</a> it.</p>
  <ul>
    <li>List item one</li>
    <li>List item two</li>
  </ul>
</div>
```

Then answer and implement:

1. Set `color: #1e40af` and `font-family: Georgia, serif` on `.article`. Which child elements inherit these values?
2. The link (`<a>`) probably does not inherit the color. Why? Use `color: inherit` to fix it.
3. Set `border: 2px solid red` on `.article`. Does it appear on the `<h2>`, `<p>`, or `<li>` elements? Why or why not?
4. Use `font: unset` on the `<h2>` to reset its font to the browser default. What changes?

<details>
<summary>Solution</summary>

```css
.article {
  color: #1e40af;
  font-family: Georgia, serif;
  border: 2px solid red;
}

/* 1. h2, p, li all inherit color and font-family */
/* 2. Fix the link color */
.article a {
  color: inherit; /* Now the link uses #1e40af instead of browser default blue */
}

/* 3. Border does NOT appear on children — border is a non-inherited property.
   Only .article itself has the red border. */

/* 4. Reset h2 font */
.article h2 {
  font: unset;
  /* The h2 font-family, font-size, and font-weight all reset to their initial/inherited values.
     Because font-family inherits and we unset it, it will inherit Georgia from .article.
     font-size and font-weight may reset to their initial values (medium/normal). */
}
```

</details>

---

### Exercise 6

**Difficulty:** Medium
**Objective:** Debug a specificity conflict using DevTools

Given the following HTML and CSS:

```html
<nav id="primary-nav" class="site-nav">
  <a href="#" class="nav-link active">Home</a>
  <a href="#" class="nav-link">About</a>
</nav>
```

```css
a.nav-link {
  color: #374151;
  text-decoration: none;
}

.site-nav a {
  color: #6b7280;
}

#primary-nav .active {
  color: #2563eb;
  font-weight: bold;
}

.nav-link.active {
  color: hotpink;  /* You want this to win */
}
```

1. For the first `<a>` (which has classes `nav-link` and `active`), calculate each rule's specificity and determine which color actually applies.
2. Without using `!important` or IDs, rewrite `.nav-link.active` so it wins against `#primary-nav .active`.

<details>
<summary>Solution</summary>

**Specificity calculation for the first `<a>`:**

- `a.nav-link` → `(0,1,1)` → color: #374151
- `.site-nav a` → `(0,1,1)` → color: #6b7280 ← later than `a.nav-link`, so this wins over it
- `#primary-nav .active` → `(1,1,0)` → color: #2563eb ← **WINS** (A=1 beats A=0)
- `.nav-link.active` → `(0,2,0)` → color: hotpink ← loses to the ID rule

The applied color is **#2563eb** (blue).

**Fix without !important or ID:**
To beat `#primary-nav .active` (which has A=1), we need our rule to also have A≥1, or... we can use `:is()` to trick specificity. Actually the only clean approaches without IDs are:

Option A — restructure the HTML so the ID is not needed for this rule:
```css
/* Use the same ID in our rule to match specificity, then rely on order */
#primary-nav .nav-link.active {
  color: hotpink;  /* (1,2,0) — wins because B is higher than (1,1,0) */
}
```

Option B — use CSS cascade layers (Module 10 concept — acceptable to look up):
```css
@layer overrides {
  .nav-link.active { color: hotpink; }
}
```

The lesson: ID selectors in stylesheets make specificity management hard. This is why many CSS architectures (BEM, utility-first) avoid IDs entirely.

</details>

---

## Hard Exercises (7–8)

### Exercise 7

**Difficulty:** Hard
**Objective:** Build a complete styled page using cascade, specificity, and inheritance

Build a single HTML page that includes:
- A `<header>` with a site title and navigation (3 links)
- A `<main>` with a `<section>` containing an `<h2>`, two `<p>` elements, and a `<blockquote>`
- A `<footer>` with a copyright line

CSS requirements:
- Use only external CSS (no inline styles, no `<style>` tags)
- Set a global font using the `<body>` element (demonstrate inheritance)
- Use at least one class selector, one compound selector, and one pseudo-class
- Make visited links a different color from unvisited links using `:visited`
- The `<blockquote>` should have a left border and italic text

**Constraint:** Do not use any CSS that you need `!important` to make work.

<details>
<summary>Solution hint</summary>

```css
/* Global font inheritance */
body {
  font-family: system-ui, -apple-system, sans-serif;
  color: #374151;
  line-height: 1.6;
  margin: 0;
  padding: 2rem;
}

/* Header */
header {
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
}

/* Navigation links — compound selector */
nav a {
  color: #2563eb;
  text-decoration: none;
  margin-right: 1rem;
}

/* Pseudo-class for visited state */
nav a:visited {
  color: #7c3aed;
}

nav a:hover {
  text-decoration: underline;
}

/* Blockquote styling */
blockquote {
  border-left: 4px solid #3b82f6;
  margin: 1.5rem 0;
  padding: 0.5rem 1rem;
  font-style: italic;
  color: #6b7280;
}

footer {
  margin-top: 2rem;
  font-size: 0.875rem;
  color: #9ca3af;
}
```

</details>

---

### Exercise 8

**Difficulty:** Hard
**Objective:** Identify and fix three CSS bugs

The following CSS is broken. Each section has a deliberate bug. Identify the bug, explain why it is a bug, and write the fix.

```css
/* Bug 1 */
.container {
  wdith: 800px;           /* Bug: ??? */
  max-width: 100%;
}

/* Bug 2 */
h1, h2, h3 {
  font-family: 'Helvetica Neue', Arial, sans-serif
  font-weight: bold;      /* Bug: ??? */
}

/* Bug 3 */
.button {
  color: white;
  background-color: blue;
}

#submit-button {
  background-color: gray;
}

.button.primary {
  background-color: green;  /* Bug: this never wins for <button id="submit-button" class="button primary"> */
}
```

<details>
<summary>Solution</summary>

**Bug 1:** `wdith` is a typo — CSS silently ignores unknown properties.
```css
.container {
  width: 800px;   /* Fixed spelling */
  max-width: 100%;
}
```

**Bug 2:** Missing semicolon after `font-family` declaration. CSS will ignore `font-family` and the parser will merge the two declarations into one broken value.
```css
h1, h2, h3 {
  font-family: 'Helvetica Neue', Arial, sans-serif;  /* Added semicolon */
  font-weight: bold;
}
```

**Bug 3:** Specificity conflict. `#submit-button` has specificity `(1,0,0)`, which beats `.button.primary` with `(0,2,0)`. So the `green` background never applies.

Fix option 1 — remove the ID from the CSS and use only classes:
```css
/* Don't use #submit-button in CSS — use a class instead */
.button { ... }
.button.primary { background-color: green; }  /* Now wins with (0,2,0) */
```

Fix option 2 — increase specificity of `.button.primary` to match:
```css
#submit-button.button.primary {
  background-color: green;  /* (1,2,0) — now wins */
}
```

The first fix is the correct approach — avoid IDs in stylesheets.

</details>

---

## Expert Exercise (9)

### Exercise 9

**Difficulty:** Expert
**Objective:** Explain and demonstrate the full cascade for a complex element

Given this HTML:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    /* Internal stylesheet */
    p { color: purple; }
  </style>
  <link rel="stylesheet" href="external.css">
</head>
<body>
  <article id="post" class="featured">
    <p style="color: green;" class="highlight">
      This paragraph has four competing color declarations.
    </p>
  </article>
</body>
</html>
```

```css
/* external.css */
p { color: red; }
.highlight { color: blue; }
#post p { color: orange; }
article.featured .highlight { color: pink; }
```

1. List every declaration that applies to the `<p>` element for the `color` property.
2. For each, state its origin, specificity score, and position relative to others.
3. Step through the cascade algorithm (origin → specificity → order) and state the winning value.
4. Write a short paragraph (3–5 sentences) explaining this result to a colleague who is new to CSS.
5. Bonus: What single change to the external.css would make `color: blue` win without touching the HTML or using `!important`?

<details>
<summary>Solution</summary>

**Declarations for `color` on the `<p>`:**

| # | Declaration | Origin | Specificity | Notes |
|---|-------------|--------|-------------|-------|
| 1 | `color: purple` (internal `<style>`) | Author | `(0,0,1)` | Before external.css |
| 2 | `color: red` (external.css `p` rule) | Author | `(0,0,1)` | After internal |
| 3 | `color: blue` (external.css `.highlight`) | Author | `(0,1,0)` | |
| 4 | `color: orange` (external.css `#post p`) | Author | `(1,0,1)` | |
| 5 | `color: pink` (external.css `article.featured .highlight`) | Author | `(0,2,0)` | |
| 6 | `color: green` (inline `style=""`) | Author (inline) | Overrides all selectors | |

**Cascade walkthrough:**
- Stage 1 (Origin): All are author-origin, no `!important` — all proceed to specificity.
- Inline styles beat all selector-based rules → `color: green` from `style=""` wins immediately.
- No need to compare further.

**Result:** The `<p>` is **green**.

**Explanation for a new colleague:**
"CSS has a priority system called the cascade that decides which rule wins when multiple rules set the same property. First, it looks at where the rule comes from — browsers have their own styles, developers write stylesheets, and HTML elements can have inline styles right on them. Inline styles always win over stylesheet rules unless something uses `!important`. In this case the paragraph has `style='color: green'` directly on it, so no matter what the stylesheets say, the paragraph is green. If you remove the inline style, then the rule with the most specific selector wins — in this case `#post p` with its ID selector would make the paragraph orange."

**Bonus — make `color: blue` win:**
Increase `.highlight`'s specificity above `(1,0,1)` — but we cannot beat an inline style with any selector. However, the question says "without `!important`" and without touching the HTML. This is actually **impossible** with regular CSS — inline styles beat all selectors. The only CSS solutions are `!important` or JavaScript removing the inline style.

This illustrates exactly why inline styles should not be used for styling in production: they are nearly impossible to override cleanly from a stylesheet.

</details>
