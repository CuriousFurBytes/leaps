# Resources: Module 01 — Introduction to CSS

> Verified resources specific to CSS fundamentals, the cascade, specificity, and inheritance.
> All URLs are current as of 2026-06-09. Check for updated URLs if links become stale.

---

## Primary Reading

1. **[MDN — How CSS is structured](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Getting_started)** — MDN's guided introduction to writing CSS for the first time. Covers syntax, rule structure, and linking a stylesheet. Ideal companion to the first section of this module's Theory.

2. **[MDN — Cascade, specificity, and inheritance](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Cascade_and_inheritance)** — The definitive reference for the three concepts this module covers. Includes worked examples and the formal cascade algorithm. Read this alongside the Theory section.

3. **[MDN — CSS Specificity](https://developer.mozilla.org/en-US/docs/Web/CSS/Specificity)** — The dedicated MDN article for specificity, including the formal definition, all selector types, the `!important` exception, and the `:is()`, `:has()`, and `:not()` edge cases.

---

## Interactive Tools

4. **[Specificity Calculator](https://specificity.keegan.st/)** — A visual, interactive tool where you type a CSS selector and instantly see its `(A,B,C)` specificity score broken down. Excellent for checking your work on Exercise 4.

5. **[CSS Cascade Visualizer — web.dev Learn CSS](https://web.dev/learn/css/the-cascade/)** — web.dev's cascade chapter includes interactive examples that animate which rule wins and why. More accessible than the W3C spec.

---

## Reference

6. **[MDN — CSS Reference: Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference)** — Alphabetical list of every CSS property with its definition, syntax, allowed values, and inheritance status. The "Formal definition" table on each property page shows whether it inherits.

7. **[W3C CSS Cascade Level 5 Specification](https://www.w3.org/TR/css-cascade-5/)** — The formal W3C specification for the cascade algorithm. Difficult to read as a learner, but authoritative for edge cases. Worth skimming the "Origin and Importance" section to understand the full picture.

---

## Video

8. **"CSS Cascade Explained" — Kevin Powell (YouTube)** — Kevin Powell has a series of videos explaining the cascade and specificity with clear visual demonstrations. Search for "Kevin Powell CSS cascade" on YouTube. His videos are particularly useful for learners who prefer a spoken explanation alongside code.

9. **"Why is CSS so Weird?" — Mozilla Developer (YouTube)** — A history of CSS's design decisions, explaining why the cascade and specificity work the way they do. Understanding *why* the rules exist makes them far easier to remember.

---

## Browser DevTools Guides

10. **[Chrome DevTools: Inspect and Debug CSS](https://developer.chrome.com/docs/devtools/css/)** — Google's official guide to using Chrome DevTools for CSS. The "View and change CSS" section is directly applicable to the debugging exercises in this module.

11. **[Firefox DevTools: CSS Panel](https://firefox-source-docs.mozilla.org/devtools-user/page_inspector/how_to/examine_and_edit_css/)** — Firefox's documentation for its CSS inspection tools. Firefox has some excellent specificity visualisation features.
