# Answers: Module 01 — Introduction to CSS

## Answer Key

### Easy Questions (1 pt each)

**Q1:** Cascading Style Sheets

**Q2:** A CSS declaration has three parts: the **property** (the name of the characteristic being set, e.g., `color`), the **value** (the setting for that property, e.g., `red`), and the **colon separator** between them. Together they form `property: value`.

**Q3:** The `<link>` element with `rel="stylesheet"` and `href` pointing to the CSS file.

**Q4:** True. `color` is one of the CSS properties that inherits by default — children receive their parent's `color` unless they have their own rule overriding it.

**Q5:** When two rules have the same origin and the same specificity, the rule that appears **later** in the stylesheet wins. This is the order-of-appearance (source order) stage of the cascade.

---

### Medium Questions (2 pts each)

**Q6:** A **property** is the name of a visual characteristic that CSS can control — e.g., `font-size`, `background-color`, `margin`. A **value** is the specific setting assigned to that property — e.g., `16px` for `font-size`, `#3b82f6` for `background-color`. Together they form a declaration: `font-size: 16px`.

**Q7:**
- `div` → `(0,0,1)` ← lowest
- `.card` → `(0,1,0)`
- `div.card` → `(0,1,1)`
- `#main` → `(1,0,0)`
- `#main .card` → `(1,1,0)` ← highest

Ranked lowest to highest: `div` < `.card` < `div.card` < `#main` < `#main .card`

**Q8:** The color `red` applies. The element has both classes, so both rules apply. Both `.alert` and `.warning` have the same specificity — `(0,1,0)`. When specificity is equal, the rule that appears **later** in the stylesheet wins. `.warning` is declared after `.alert`, so `color: red` wins. (Note: the order of classes in the HTML element's `class` attribute has no effect on CSS specificity — only source order in the CSS matters.)

**Q9:** `display: none` removes the element from the document flow entirely — it takes up no space and other elements behave as if it does not exist. `visibility: hidden` makes the element invisible but it **still occupies its space** in the layout — a gap will remain where the element would have been.

**Q10:**
- Properties that inherit: `color`, `font-family`, `line-height` (also: `font-size`, `font-weight`, `text-align`, `cursor`, etc.)
- Properties that do not inherit: `margin`, `padding`, `border` (also: `background-color`, `width`, `display`, `position`, etc.)

---

### Hard Questions (3 pts each)

**Q11:** Specificity scores and ranking:
- `*` → `(0,0,0)` ← lowest (universal selector contributes nothing)
- `li` → `(0,0,1)`
- `a:hover` → `(0,1,1)` (type + pseudo-class)
- `ul li` → `(0,0,2)` (two type selectors)
- `ul > li.item` → `(0,1,2)` (two types + one class)
- `#nav li.item` → `(1,1,1)` ← highest (ID + class + type)

Ranked: `*` < `li` < `ul li` < `a:hover` < `ul > li.item` < `#nav li.item`

**Q12:** The problem is a specificity conflict. `.btn` sets `color: white` with specificity `(0,1,0)`. The `#submit` ID rule sets `color: black` with specificity `(1,0,0)`. The ID rule has higher specificity and wins — the text is black.

Correct approach — avoid using an ID in the CSS. Change the ID rule to a class:
```css
.btn {
  background-color: #2563eb;
  color: white;
}

/* Remove the #submit rule, or replace it with a class */
/* If there was a reason to style this button differently, use a modifier class: */
.btn.btn-danger {
  color: black;
}
```

If the ID rule is unavoidable (e.g., comes from a third-party library):
```css
/* Raise .btn specificity to match the ID rule using the :is() pseudo-class trick,
   or add the ID to the selector: */
#submit.btn {
  color: white;  /* (1,1,0) — now beats #submit's (1,0,0) */
}
```

**Q13:** The problem is **specificity inflation**. When a developer adds `!important` to rule A to override rule B, rule B can only win back if it also gets `!important`. But then rule A must become more specific to win, so it needs `!important` too — and now both rules have `!important`, so specificity is compared again. As this pattern repeats, the stylesheet becomes a tangle of `!important` declarations that are impossible to override without more `!important`.

The correct approach:
1. Open DevTools and identify *exactly* which rule is winning and why (which selector has higher specificity, or which appears later).
2. Reduce the specificity of the winning rule (simplify the selector) or increase the specificity of the losing rule (add a meaningful class, not an ID).
3. Consider restructuring the stylesheet so competing rules don't exist — use a single rule for each variant.
4. Use cascade layers (`@layer`) for intentional ordering if specificity conflicts are systematic.

**Q14:**
```css
/* The fix */
.card a {
  color: inherit;  /* Inherit the color from the closest ancestor that sets it */
}
```

This works because `inherit` forces the property to take its value from the parent's (or ancestor's) **computed** color value. The `.card` ancestor has `color: #1e293b` (from the inline style in this example). Without `color: inherit`, the browser's user-agent stylesheet provides a default link colour (typically blue or purple) that is a specified value — not an inherited value. Specified values from any origin (including user-agent) take priority over inherited values. By explicitly declaring `color: inherit`, we create an author-level rule that says "take the inherited value", which beats the user-agent's specified value.

---

### Expert Questions (5 pts each)

**Q15:** Full credit answer must cover all four required points:

CSS `color` does inherit — when you set `color` on `<body>`, it does cascade down to most elements. However, `<a>` elements appear to break this because the browser's user-agent stylesheet contains a rule like `a { color: -webkit-link; }` (or equivalent). **User-agent stylesheets are specified values, not inherited values.** The cascade specification states that specified (author or user-agent) values take priority over inherited values. So even though `<body>` sets `color: #1e293b`, the user-agent's `a { color: blue; }` is a *specified* declaration that beats it — the inheritance never reaches the link.

To fix it, write an explicit author rule: `a { color: inherit; }`. This creates an author-level *specified* declaration that says "inherit from your parent". Author styles beat user-agent styles, so this wins. The link now takes its color from its nearest ancestor that has a `color` specified.

**Q16:** Step-by-step DevTools debugging:

1. Open DevTools with F12 (or Cmd+Option+I on Mac).
2. Click the cursor/inspector icon in DevTools and click the affected element on the page. Alternatively, right-click the element and choose "Inspect".
3. In the "Elements" panel (Chrome) or "Inspector" panel (Firefox), the "Styles" tab shows all declarations targeting the selected element.
4. Look for the `background-color` property. Rules are listed from highest to lowest priority. The winning rule appears at the top, un-strikethrough. Losing rules are shown with strikethroughs.
5. Hover over the source link next to the winning rule (e.g., `styles.css:42`) to see the file and line number. Click it to open the source in the "Sources" tab.
6. To find the source of an unexpected winning rule: check its selector's specificity (count IDs, classes, types), check whether it is later in the file, and check whether it is in a different stylesheet that loads after yours.
7. To fix permanently: either (a) increase the specificity of your rule to beat the unexpected winner, (b) decrease the unexpected winner's specificity if you own that code, or (c) restructure the HTML/CSS so the conflict no longer exists (e.g., use a different class name that is not matched by the unexpected rule).

---

### Bonus Questions

**Bonus 1:** The metaphor is that of water cascading down a series of steps or levels — each level passing water to the next, with higher levels taking priority. In CSS, style "flows" from multiple origins (user-agent → author → user), and at each level a rule either wins or loses to a more specific rule. Just as water fills pools at the bottom of a cascade, CSS declarations "fill in" property values through successive levels of priority. The metaphor captures both the flow from general to specific and the idea that rules from "higher" sources (author) override rules from "lower" sources (user-agent), except when `!important` reverses the flow.

**Bonus 2:** Two key limitations of the pre-CSS approach:

1. **Maintenance at scale:** Styling was embedded in HTML attributes (`<font face="Arial" color="red">`, `bgcolor="#000000"`). Changing the site's colour scheme required editing every HTML file — there was no way to update a style in one place and have it propagate everywhere.

2. **No separation of concerns:** Content and presentation were inextricably mixed. A content editor who changed a paragraph's text might accidentally break its layout. Developers, designers, and content writers all had to understand and edit the same HTML for different reasons. CSS created a clean boundary: HTML authors handle content and structure; CSS authors handle appearance.

**Bonus 3:** `initial` resets a property to its **CSS specification default** — the value defined in the CSS spec as the property's initial value. For `color`, that is `black`. For `display`, it is `inline`. However, the user-agent stylesheet (the browser's built-in CSS) may have set something different — e.g., `<h1>` has `font-size: 2em` in the user-agent stylesheet, but `initial` resets `font-size` to `medium` (the spec initial), not to `2em`.

`revert` instead resets the property to what the **user-agent stylesheet** would set — effectively "undo my author styles but keep the browser's defaults". Use `revert` when you want an element to look like it did before your stylesheet touched it (e.g., resetting a button to look like a plain button). Use `initial` when you want to start from the absolute spec baseline, ignoring browser defaults.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
