# Test: Module 01 — Introduction to JavaScript

**Instructions:** Answer all questions. Write your answers directly below each question in the `Answer:` field.
Bonus questions are optional and can raise your score above 25 points.

**Total Points:** 25 pts (Easy: 8 + Medium: 9 + Hard: 6 + Expert: 2)
**Bonus Available:** 6 pts

---

## Section 1: Easy Questions (2 pts each)

**Q1.** What year was JavaScript created, who created it, and at which company?

> Answer:

---

**Q2.** What is the difference between `null` and `undefined`? Give one example of a situation where you would encounter each.

> Answer:

---

**Q3.** List the seven primitive types in JavaScript.

> Answer:

---

**Q4.** What output does the following code produce? Explain why.

```javascript
let x;
console.log(typeof x);
console.log(x === undefined);

const y = null;
console.log(typeof y);
console.log(y === null);
```

> Answer:

---

## Section 2: Medium Questions (3 pts each)

**Q5.** Explain the difference between `==` (loose equality) and `===` (strict equality). Give two examples where `==` returns `true` but `===` returns `false`. When is it acceptable to use `==`?

> Answer:

---

**Q6.** What is hoisting in JavaScript? Explain how `var`, `let`, and `function` declarations are hoisted differently. What happens if you access a `let` variable before its declaration line?

> Answer:

---

**Q7.** Explain what a closure is in your own words. Look at the following code — what does it output, and why?

```javascript
function outer() {
  let secret = 42;
  return function inner() {
    secret++;
    return secret;
  };
}

const fn = outer();
console.log(fn()); // ?
console.log(fn()); // ?
console.log(fn()); // ?
```

> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q8.** The following code has a bug. Identify the bug, explain why it occurs, and write the corrected version.

```javascript
const results = [];
for (var i = 0; i < 3; i++) {
  results.push(function() { return i; });
}
console.log(results[0]()); // Expected: 0, Actual: ?
console.log(results[1]()); // Expected: 1, Actual: ?
console.log(results[2]()); // Expected: 2, Actual: ?
```

> Answer:

---

**Q9.** Write a function `flatten(arr)` that takes a nested array (up to 2 levels deep) and returns a new flat array. Do not use `Array.prototype.flat()`. Your function must handle arrays like `[1, [2, 3], [4, [5, 6]]]` and return `[1, 2, 3, 4, 5, 6]`.

```javascript
// Write your function here:

// Expected outputs:
// flatten([1, [2, 3], [4, [5, 6]]]) → [1, 2, 3, 4, 5, 6]
// flatten([1, 2, 3])               → [1, 2, 3]
// flatten([[1, 2], [3, 4]])         → [1, 2, 3, 4]
```

> Answer:

---

## Section 4: Expert Question (2 pts)

**Q10.** The following code is intended to print 0 through 4, with each number logged after 1 second. It does not work as intended. Describe **all** the problems with it, explain the underlying JavaScript concepts that cause each problem, and provide a working rewrite that achieves the intended behaviour.

```javascript
for (var i = 0; i < 5; i++) {
  setTimeout(function() {
    console.log(i);
  }, 1000 * i);
}
```

> Answer:

---

## Bonus Questions (2 pts each)

**Bonus 1.** What is the ECMAScript specification and how does it relate to JavaScript? What is the difference between ES5, ES2015/ES6, and ES2022? (+2 pts)

> Answer:

**Bonus 2.** Explain the difference between a function declaration and a function expression with regard to hoisting. What is the difference in behaviour between these two? (+2 pts)

```javascript
// Version A
console.log(add(2, 3));
function add(a, b) { return a + b; }

// Version B
console.log(multiply(2, 3));
const multiply = (a, b) => a * b;
```

> Answer:

**Bonus 3.** What does the rest parameter syntax (`...args`) do? How is it different from the `arguments` object available in traditional function declarations? Why can't arrow functions use `arguments`? (+2 pts)

> Answer:
