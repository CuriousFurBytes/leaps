# Exercises: Module 01 — Introduction and the Cascade

## Instructions
Complete each exercise in order. Exercises increase in difficulty. Submit your answers by editing this file or committing a solutions file.

---

## Easy Exercises (1–3)

### Exercise 1
**Difficulty:** Easy
**Objective:** Identify selectors and declarations.

Annotate this stylesheet with comments explaining each selector, property, and value.

```css
.card {
  padding: 1rem;
  color: #111827;
}
```

---

### Exercise 2
**Difficulty:** Easy
**Objective:** Write a basic rule.

Create a class named `.callout` with padding, a border, and a background color.

```css
.callout {
  /* Add your declarations here. */
}
```

---

### Exercise 3
**Difficulty:** Easy
**Objective:** Recognize inheritance.

Set a text color on `body`, then override link color with an `a` rule.

```css
body {
  /* Add inherited text color. */
}

a {
  /* Add link-specific color. */
}
```

## Medium Exercises (4–6)

### Exercise 4
**Difficulty:** Medium
**Objective:** Predict cascade results.

Given two class rules targeting the same property, explain which one wins and why.

### Exercise 5
**Difficulty:** Medium
**Objective:** Use meaningful class names.

Rename three appearance-based classes into purpose-based classes and justify each rename.

### Exercise 6
**Difficulty:** Medium
**Objective:** Inspect computed styles.

Use browser developer tools to find one overridden declaration and record what overrode it.

## Hard Exercises (7–8)

### Exercise 7
**Difficulty:** Hard
**Objective:** Debug specificity.

Refactor an overly specific selector into a simple class-based selector.

```css
main section.article-list article.card.featured h2.title {
  color: rebeccapurple;
}
```

---

### Exercise 8
**Difficulty:** Hard
**Objective:** Build a reusable component style.

Create styles for a notice component with normal and urgent states.

## Expert Exercise (9)

### Exercise 9
**Difficulty:** Expert
**Objective:** Explain CSS architecture tradeoffs.

Write a short design note explaining when you would use element selectors, class selectors, and state classes in a growing application.
