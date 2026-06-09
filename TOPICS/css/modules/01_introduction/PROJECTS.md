# Projects: Module 01 — Introduction to CSS

> These projects are suitable immediately after completing Module 01. Each focuses on the cascade, specificity, and inheritance — the core concepts from this module.

---

## Project A — Style an Unstyled HTML Article

**Difficulty:** Beginner
**Estimated time:** 1.5–2 hours

**Brief:**
Start with a bare HTML file representing a blog article (no stylesheets attached) and write a complete CSS stylesheet for it from scratch. The goal is to produce a readable, clean page using only the knowledge from Module 01 — no layout systems yet.

**Starter HTML structure:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Article</title>
  <!-- Add your stylesheet link here -->
</head>
<body>
  <header>
    <h1>The Early History of CSS</h1>
    <p class="byline">By A. Learner · June 2026</p>
  </header>
  <main>
    <section>
      <h2>Before CSS</h2>
      <p>Before CSS was standardised, web pages were styled using HTML attributes...</p>
      <blockquote>
        "The web would be a better place without font tags." — Hypothetical quote
      </blockquote>
    </section>
    <section>
      <h2>Håkon's Proposal</h2>
      <p>In 1994, Håkon Wium Lie proposed the first CSS draft...</p>
    </section>
  </main>
  <footer>
    <p>&copy; 2026 My Learning Site</p>
  </footer>
</body>
</html>
```

**Requirements:**
- Use `<body>` to set a global font via inheritance (demonstrate that children receive it)
- Style `header`, `main`, and `footer` as distinct regions
- Style `.byline` to look visually secondary to the `<h1>`
- Style `<blockquote>` with a left border and different background colour
- Add `:hover` effects to any links

**What you are demonstrating:** inheritance, type selectors, class selectors, basic cascade

---

## Project B — The Specificity Challenge Page

**Difficulty:** Beginner
**Estimated time:** 1–1.5 hours

**Brief:**
Create a page whose purpose is to visually demonstrate specificity. Build 6–8 elements, each styled by competing rules of different specificity. Label each element in the HTML with a comment explaining which rule wins and why. This project is about understanding, not aesthetics.

**Example structure:**

```html
<!-- Element 1: type vs class — which wins? -->
<p class="highlight">Should I be black (type) or gold (class)?</p>

<!-- Element 2: class vs ID — which wins? -->
<p class="danger" id="urgent">Should I be orange (class) or crimson (ID)?</p>

<!-- Element 3: Inheritance vs explicit -->
<div style="color: purple;">
  <p>Do I inherit purple from my parent, or is a stylesheet rule stronger?</p>
</div>
```

**What you are demonstrating:** direct comparison of all specificity levels, visible proof of cascade logic

---

## Project C — Themed Typography Page

**Difficulty:** Beginner
**Estimated time:** 2–3 hours

**Brief:**
Build a page that demonstrates CSS inheritance for typography. The page should have a clearly defined "theme" — a consistent font, colour palette, and scale — applied entirely through inheritance and a small number of rules. The challenge is to achieve visual consistency with *as few rules as possible*.

**Constraints:**
- Limit yourself to a maximum of 15 CSS declarations total (not rules — declarations)
- All heading sizes must be set via type selectors, not classes
- Use only `color`, `font-family`, `font-size`, `line-height`, `margin`, and `padding`

**Aim:** Produce a page where you can change the entire look by modifying just the `<body>` rule.

**What you are demonstrating:** the power of inheritance, DRY (Don't Repeat Yourself) CSS, the relationship between type selectors and inheritance

---

## Project D — Debug a Broken Stylesheet

**Difficulty:** Beginner (with a harder component)
**Estimated time:** 1–2 hours

**Brief:**
You are given a stylesheet with six deliberate bugs. Your job is to find all six, explain each bug, and write the fix. This project is about reading CSS critically and using DevTools to trace problems.

**Setup:** Copy the following into an `index.html` and `broken.css`, open in a browser, and find the bugs:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Debug Me</title>
  <link rel="stylesheet" href="broken.css">
</head>
<body>
  <header id="site-header" class="header">
    <h1>Bug Hunt</h1>
    <nav class="nav">
      <a href="#" class="nav-link active">Home</a>
      <a href="#" class="nav-link">About</a>
    </nav>
  </header>
  <main>
    <p class="intro important-text">Introductory paragraph.</p>
    <p>Regular paragraph.</p>
  </main>
</body>
</html>
```

```css
/* broken.css — find all 6 bugs */

/* Bug 1 */
body {
  font-famly: Arial, sans-serif;
  color: #333;
}

/* Bug 2 */
.header {
  background-colour: #f8f9fa;
  padding: 1rem;
}

/* Bug 3 */
.nav-link {
  color: #2563eb
  text-decoration: none;
}

/* Bug 4 — I want .active to be bold, but it isn't */
#site-header a {
  font-weight: normal;
}
.active {
  font-weight: bold;
}

/* Bug 5 */
.intro {
  font-size: 1.2rem;
  color: #1e40af;
}
.important-text {
  font-size: 1.2rem;
  Color: darkred;
}

/* Bug 6 */
main p:first-child {
  margin-top: 0 !important
  margin-bottom: 1rem;
}
```

Write your findings in a `BUGS.md` file alongside the CSS.

**What you are demonstrating:** reading CSS critically, specificity conflicts, common syntax errors, DevTools inspection
