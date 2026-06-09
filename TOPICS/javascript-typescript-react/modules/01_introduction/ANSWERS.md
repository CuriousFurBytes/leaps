# Answers: Module 01 — Introduction to JavaScript

## Answer Key

### Easy Questions

**Q1:** JavaScript was created in **1995** by **Brendan Eich** at **Netscape Communications**. The original version was written in approximately ten days under pressure to ship with Netscape Navigator 2.0. It was initially named "Mocha", then "LiveScript", before being renamed "JavaScript" as a marketing decision capitalising on Java's popularity — despite the two languages having little in common technically.

**Q2:** `null` is an **intentional absence of a value** — it is a value that a programmer explicitly assigns to say "this has no value" or "this is empty". Example: after deleting a user, you might set `currentUser = null`. `undefined` is an **unintentional or default absence of a value** — JavaScript uses it for variables that have been declared but not assigned, function parameters that were not provided, and the implicit return value of a function with no return statement. Example: `let name;` — `name` is `undefined` because we never assigned anything to it.

**Q3:** The seven JavaScript primitive types are: `string`, `number`, `boolean`, `null`, `undefined`, `symbol`, and `bigint`.

**Q4:** Output and explanations:
```
"undefined"  — typeof x is "undefined" because x was declared with let but never assigned a value
true         — x is exactly undefined, so === comparison is true
"object"     — typeof null is "object" — this is a historic bug in JavaScript from 1995
true         — null === null is true (strict equality with no coercion)
```

---

### Medium Questions

**Q5:** `==` (loose equality) performs **type coercion** before comparing — it converts one or both values to the same type before checking. `===` (strict equality) compares both **value and type** with no coercion; different types are always unequal.

Examples where `==` is `true` but `===` is `false`:
```javascript
0 == ''      // true ('' coerces to 0); 0 === '' is false
0 == false   // true (false coerces to 0); 0 === false is false
1 == '1'     // true ('1' coerces to 1); 1 === '1' is false
null == undefined // true (special rule); null === undefined is false
```

The only acceptable use of `==` is the idiom `value == null`, which conveniently checks for both `null` and `undefined` simultaneously. In all other cases, use `===`.

**Q6:** Hoisting is JavaScript's behaviour of moving declarations to the top of their scope during the compilation phase, before code executes.

- **`function` declarations** are fully hoisted — both the name and the body. You can call a function declaration before its textual position in the file.
- **`var` declarations** are partially hoisted — the variable name is hoisted to the top of the enclosing function, but the assignment is not. Accessing a `var` variable before its assignment line gives `undefined`, not a ReferenceError.
- **`let` and `const` declarations** are also hoisted (they exist in the scope from the start), but they are placed in a **Temporal Dead Zone (TDZ)**. Accessing a `let` or `const` variable before its declaration line throws a `ReferenceError: Cannot access 'x' before initialization`.

**Q7:** A closure is a function that retains access to variables from its enclosing (outer) scope even after the outer function has finished executing. The inner function "closes over" the `secret` variable.

Output:
```
43  — fn() is called; secret starts at 42, incremented to 43, returned
44  — fn() called again; secret is still alive in the closure, incremented to 44
45  — same; incremented to 45
```

Each call to `fn()` modifies the *same* `secret` variable — there is only one `secret`, shared across all calls to `fn`. The outer function `outer()` has completed, but because `fn` holds a reference to `secret`, the variable is kept alive in memory by the garbage collector.

---

### Hard Questions

**Q8:** The bug is that `var` is **function-scoped**, not block-scoped. All three functions in the `results` array close over the *same* `i` variable. By the time any of the functions are called (after the loop), the loop has finished and `i` is `3`. So all three functions return `3`.

Actual output: `3`, `3`, `3`

**Corrected version using `let`:**
```javascript
const results = [];
for (let i = 0; i < 3; i++) {  // let creates a new binding for each iteration
  results.push(function() { return i; });
}
console.log(results[0]()); // 0
console.log(results[1]()); // 1
console.log(results[2]()); // 2
```

With `let`, each iteration creates a fresh `i` binding that is captured separately by each closure.

**Q9:**
```javascript
function flatten(arr) {
  const result = [];
  for (const item of arr) {
    if (Array.isArray(item)) {
      // item is an array — go one level deeper
      for (const inner of item) {
        if (Array.isArray(inner)) {
          // Two levels deep — spread the inner array
          for (const deepItem of inner) {
            result.push(deepItem);
          }
        } else {
          result.push(inner);
        }
      }
    } else {
      result.push(item);
    }
  }
  return result;
}
```

Alternative using `concat` and spread (more concise):
```javascript
function flatten(arr) {
  return arr.reduce((flat, item) => {
    if (Array.isArray(item)) {
      return flat.concat(item.flat()); // flat() handles the second level
    }
    return flat.concat(item);
  }, []);
}
```

---

### Expert Question

**Q10:** There are **two problems**:

**Problem 1 — `var` scoping (all logs print 5):**
`var i` is function-scoped (or global-scoped here, since there's no enclosing function). All five setTimeout callbacks close over the *same* `i` variable. By the time any timer fires (1 second later), the loop has already finished and `i === 5`. So all five callbacks print `5`, not `0, 1, 2, 3, 4`.

**Problem 2 — All timers fire at approximately the same time:**
`setTimeout(fn, 1000 * 0)` = 0ms, `setTimeout(fn, 1000 * 1)` = 1000ms, etc. This part actually works as intended for spreading out the delays — the intent was correct, but the output will be `5` at each interval.

**Working solution using `let`:**
```javascript
// let creates a new binding per iteration — each callback captures its own i
for (let i = 0; i < 5; i++) {
  setTimeout(function() {
    console.log(i);
  }, 1000 * i);
}
// Output (at 0s, 1s, 2s, 3s, 4s): 0, 1, 2, 3, 4
```

**Alternative: using an IIFE to capture the value:**
```javascript
for (var i = 0; i < 5; i++) {
  (function(j) {             // immediately-invoked function captures j by value
    setTimeout(function() {
      console.log(j);
    }, 1000 * j);
  })(i);
}
```

---

### Bonus Questions

**Bonus 1:** ECMAScript is the official specification of the scripting language standard published by ECMA International. JavaScript is the most prominent implementation of the ECMAScript specification. When browser vendors implement JavaScript, they implement the ECMAScript spec.

- **ES5** (2009): Added `strict mode`, `Array.prototype.forEach/map/filter/reduce`, `JSON.parse/stringify`, `Object.keys`. Still supported everywhere. Characterized by the "old JavaScript" patterns you see in legacy codebases.
- **ES2015 (ES6)** (2015): The largest update in the language's history. Added `let`/`const`, arrow functions, classes, template literals, destructuring, default/rest/spread, `Symbol`, `Map`, `Set`, `Promise`, modules (`import`/`export`), generators, `for...of`, and much more.
- **ES2022**: Added top-level `await`, class field declarations, `Array.prototype.at()`, `Object.hasOwn()`, private class methods, and more. The language now evolves with annual releases.

**Bonus 2:**
- **Version A** — works fine and prints `5`. `function add` is a function declaration, which is **fully hoisted** — the name and body are both available from the start of the scope. Calling it before its position in the file is legal.
- **Version B** — throws a `ReferenceError: Cannot access 'multiply' before initialization`. `const multiply` is a `const` declaration, which is hoisted but sits in the **Temporal Dead Zone** (TDZ) until the declaration line is reached. The arrow function value is only assigned when execution reaches that line.

**Bonus 3:** The **rest parameter** (`...args`) collects all remaining function arguments into a *real* array. It is part of the function's parameter list and only captures arguments not already captured by named parameters. The **`arguments` object** is an array-like (but not a real array) object that automatically exists inside non-arrow functions and holds all arguments passed to the function. Key differences:
1. `...args` creates a real `Array` with all array methods; `arguments` is array-like but lacks `map`, `filter`, etc.
2. Rest parameters capture only the "rest" (remaining args after named params); `arguments` captures all args.
3. Arrow functions do not have their own `arguments` object — they inherit `arguments` from their enclosing non-arrow function, which is surprising. This is one reason to prefer rest parameters over `arguments`.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
