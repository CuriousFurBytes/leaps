# Test: Module 01 — Introduction to CSS

**Instructions:** Answer all questions. Write your answers directly below each question in the `> Answer:` block.
Bonus questions are optional and can raise your score above 100%.

**Total Points:** 37 pts (Easy: 5 × 1 pt + Medium: 5 × 2 pts + Hard: 4 × 3 pts + Expert: 2 × 5 pts)
**Bonus Available:** 6 pts

---

## Section 1: Easy Questions (1 pt each)

**Q1.** What does the acronym CSS stand for?

> Answer:

---

**Q2.** What are the three parts of a CSS declaration?

> Answer:

---

**Q3.** Which HTML element is used to link an external stylesheet to a web page?

> Answer:

---

**Q4.** True or false: The `color` CSS property is inherited by default.

> Answer:

---

**Q5.** In the cascade algorithm, what happens when two rules have the same origin and the same specificity?

> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Explain the difference between a CSS property and a CSS value. Give one example of each.

> Answer:

---

**Q7.** Rank the following from lowest to highest specificity. Show the `(A,B,C)` score for each:
- `div`
- `.card`
- `#main`
- `div.card`
- `#main .card`

> Answer:

---

**Q8.** A developer writes two rules:
```css
.alert { color: orange; }
.warning { color: red; }
```
The element is `<p class="alert warning">`. Which color applies, and why?

> Answer:

---

**Q9.** What is the difference between `display: none` and `visibility: hidden`?

> Answer:

---

**Q10.** Name three CSS properties that inherit by default and three that do not.

> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** Calculate the specificity of each selector below and list them from lowest to highest specificity. If two are equal, state that:
- `*`
- `li`
- `ul li`
- `ul > li.item`
- `#nav li.item`
- `a:hover`

> Answer:

---

**Q12.** Debug the following CSS. The developer wants the button text to be white, but it is appearing as black. Identify the problem and write the corrected CSS:

```html
<button id="submit" class="btn btn-primary">Submit</button>
```

```css
.btn {
  background-color: #2563eb;
  color: white;
}

#submit {
  color: black;
}
```

> Answer:

---

**Q13.** A developer adds `!important` to five rules to fix a specificity conflict. Three months later the site is hard to maintain because every new rule needs `!important` too. Explain why this happens, and describe the correct approach for resolving the original specificity conflict.

> Answer:

---

**Q14.** Write the CSS to make every `<a>` element inside a `.card` component inherit its text color from the card, instead of using the browser's default link colour. Explain why this solution works.

```html
<div class="card" style="color: #1e293b;">
  <p>Read more: <a href="#">Click here</a></p>
</div>
```

> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** A student says: "I just set `color` on the `<body>` element. Why do my links still have a different color — doesn't the body pass its color down to everything?" Write a thorough explanation (at least 4 sentences) that covers: how inheritance works, why `<a>` elements behave differently, what the user-agent stylesheet has to do with it, and how to fix it properly.

> Answer:

---

**Q16.** You are debugging a production site where a component's `background-color` is being overridden somewhere. Describe a systematic, step-by-step process for diagnosing and fixing the problem using only browser DevTools — no searching the codebase. Your answer should mention at least: how to open DevTools, how to find the element, where to look for the winning and losing declarations, how to trace the source file, and one approach for permanently resolving the conflict.

> Answer:

---

## Bonus Questions (variable pts)

**Bonus 1.** Why does CSS call its priority algorithm "cascading"? What physical metaphor does the name evoke, and how does the metaphor map onto the actual algorithm? (+2 pts)

> Answer:

---

**Bonus 2.** Håkon Wium Lie proposed CSS in 1994. What problem was he solving that HTML attributes alone could not? Name at least two limitations of the pre-CSS approach that CSS was designed to address. (+2 pts)

> Answer:

---

**Bonus 3.** The `revert` keyword was added to CSS to address a limitation of `initial`. What is that limitation, and when would you choose `revert` over `initial`? (+2 pts)

> Answer:
