# Module 01: Introduction to JavaScript

[← Topic Home](../../README.md) | [Next → Module 02: Core JavaScript](../02_core-javascript/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner-green)
![Time](https://img.shields.io/badge/time-8--10h-orange)

> JavaScript is the language of the web — this module explains what it is, where it came from, how it runs, and gives you your first working programs.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Key Concepts](#key-concepts)
6. [Examples](#examples)
7. [Common Pitfalls](#common-pitfalls)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

---

## Overview

This module is your entry point to JavaScript. You will learn what JavaScript is, why it exists, how it runs inside a browser and on a server (Node.js), and how to write your first programs. By the end of this module you will be able to write and execute JavaScript code, declare and use variables, work with basic data types, write functions, and control program flow with conditionals and loops.

JavaScript is unusual among programming languages in that it was invented under extreme time pressure (10 days), designed to be approachable by non-programmers, and has now become one of the most deployed runtimes in history. That history explains both its surprising power and its equally surprising quirks. Rather than fighting the quirks, this module teaches you to understand them so they never surprise you.

This module does not assume you have any programming experience. Every concept is built from the ground up. If you do have programming experience in another language (Python, Java, C#, Go, etc.), you will move quickly but should pay particular attention to the Common Pitfalls section — many of JavaScript's surprises are specific to its type coercion rules, `var` scoping, and function behavior.

---

## Prerequisites

- None. This is the absolute beginning module.
- You need Node.js installed on your machine to run JavaScript outside the browser. Install it from [https://nodejs.org](https://nodejs.org) — choose the LTS version.
- A text editor (VS Code is recommended: [https://code.visualstudio.com](https://code.visualstudio.com))

---

## Objectives

By the end of this module, you will be able to:

1. Explain what JavaScript is, where it runs, and why it was designed the way it was
2. Run a JavaScript program using both Node.js (terminal) and the browser console
3. Declare variables using `let`, `const`, and `var`, and explain the difference between them
4. Identify and use all seven JavaScript primitive types: `string`, `number`, `boolean`, `null`, `undefined`, `symbol`, and `bigint`
5. Explain type coercion and use `===` instead of `==` to avoid implicit type conversion bugs
6. Write functions using function declarations, function expressions, and arrow function syntax
7. Control program flow using `if`/`else`, `switch`, `for`, `while`, `for...of`, and `for...in`
8. Use `typeof` and basic debugging techniques (`console.log`, the Node.js REPL) to inspect values

---

## Theory

### The JavaScript Ecosystem

JavaScript was created by Brendan Eich at Netscape in 1995 over the course of approximately ten days. Netscape needed a scripting language that could be embedded in Netscape Navigator 2.0 to make web pages interactive — something simpler than Java, designed for web designers and HTML authors rather than professional programmers. The result, initially called Mocha and then LiveScript before being renamed JavaScript, shipped in December 1995.

The "JavaScript" name was a deliberate marketing decision capitalizing on the popularity of Java at the time. The two languages have virtually nothing in common technically — Java is statically typed, compiled, and class-based; JavaScript is dynamically typed, interpreted, and prototype-based. This naming confusion has persisted for thirty years and still trips up newcomers.

In 1996, Netscape submitted JavaScript to ECMA International for standardization. The resulting standard is called ECMAScript (ES). When you see references to "ES5", "ES2015", "ES6", "ES2022" — these all refer to versions of the ECMAScript specification. The language you are learning is JavaScript; the specification it follows is ECMAScript. The two names are used interchangeably in common usage.

JavaScript runs in two primary environments today. In the **browser**, the JavaScript engine is embedded in the browser itself — Chrome uses V8, Firefox uses SpiderMonkey, Safari uses JavaScriptCore. The engine compiles and executes your JavaScript code, and the browser provides additional APIs (the DOM, `fetch`, `localStorage`, `setTimeout`, etc.) that JavaScript programs can call. In **Node.js**, the V8 engine is packaged as a standalone runtime that you can install on your computer and use to run JavaScript programs from the command line, write web servers, build command-line tools, and more. Node.js was created by Ryan Dahl in 2009 and is the runtime that made JavaScript a viable server-side language.

The JavaScript package ecosystem lives at **npm** (the Node Package Manager). npm ships with Node.js and is how you install third-party JavaScript libraries — including React, TypeScript, and every other library we will use in this curriculum.

To run your first JavaScript program:

```bash
# Install Node.js from https://nodejs.org, then verify it's installed:
node --version
# Expected output: v20.x.x (or similar LTS version)
npm --version
# Expected output: 10.x.x (or similar)

# Run a JavaScript file:
node myfile.js

# Start the Node.js REPL (Read-Eval-Print Loop) — an interactive console:
node
# Then type JS expressions and press Enter to see results
# Press Ctrl+C twice or type .exit to quit
```

### Variables and Types

JavaScript variables are declared with `let`, `const`, or the legacy `var` keyword. Modern JavaScript (ES2015 and later) uses `let` and `const` exclusively. Use `const` for values that will not be reassigned; use `let` for values that will change. Avoid `var` in new code — it has different, surprising scoping rules that we will cover in Module 02.

```javascript
// const — block-scoped, cannot be reassigned
const PI = 3.14159;
const name = 'Alice';

// let — block-scoped, can be reassigned
let count = 0;
count = count + 1; // this is fine

// var — function-scoped (legacy; avoid in new code)
var oldStyle = 'avoid this';

// Trying to reassign a const throws a TypeError:
// PI = 3; // TypeError: Assignment to constant variable
```

JavaScript has seven **primitive types**. A primitive is a value that is not an object and has no methods of its own (though JavaScript auto-boxes primitives into their wrapper objects when you call methods on them).

```javascript
// string — text, enclosed in single quotes, double quotes, or backticks
const greeting = 'Hello';
const template = `Hello, ${name}!`; // template literal — backtick allows interpolation

// number — IEEE 754 double-precision floating point (integers AND decimals use this same type)
const age = 30;
const price = 9.99;
const huge = 9_007_199_254_740_991; // underscores are allowed as separators

// boolean
const isActive = true;
const hasError = false;

// null — explicit absence of a value (intentionally set to "nothing")
const user = null;

// undefined — variable declared but not assigned, or function returns nothing
let x;           // x is undefined
function foo() {} // foo() returns undefined

// symbol — unique, immutable identifier (advanced; rarely needed at beginner level)
const sym = Symbol('description');

// bigint — integers larger than Number.MAX_SAFE_INTEGER
const bigNumber = 9007199254740992n; // trailing 'n' makes it a BigInt

// Check the type of a value with typeof:
typeof 'hello'     // "string"
typeof 42          // "number"
typeof true        // "boolean"
typeof undefined   // "undefined"
typeof null        // "object"  ← famous bug, explained in Pitfalls section
typeof Symbol()    // "symbol"
typeof 42n         // "bigint"
typeof {}          // "object"
typeof []          // "object"  ← arrays are objects in JS
typeof function(){} // "function"
```

JavaScript is **dynamically typed**: you do not declare the type of a variable when you create it, and the same variable can hold different types of values at different times. JavaScript also performs **type coercion** — automatic conversion between types — in certain contexts. This is the source of many beginner bugs:

```javascript
// Implicit coercion with == (loose equality)
0 == '0'    // true  (number coerces string to number)
0 == false  // true  (false coerces to 0)
'' == false // true  (both coerce to 0/falsy)
null == undefined // true (special rule)

// Strict equality === never coerces
0 === '0'   // false (different types)
0 === false // false
null === undefined // false

// Always use === in your code.
```

### Control Flow

JavaScript provides the standard set of control flow constructs. Understanding which construct to use — and when — is a key skill.

The `if`/`else if`/`else` construct branches based on a boolean condition. Any value can be used as a condition; values that are "falsy" (`0`, `''`, `null`, `undefined`, `NaN`, `false`) evaluate to false; all other values are "truthy".

```javascript
const temperature = 22;

if (temperature > 30) {
  console.log('Hot day');
} else if (temperature > 20) {
  console.log('Nice day'); // this runs because 22 > 20
} else {
  console.log('Cold day');
}

// The switch statement — good for exact-match branching
const day = 'Monday';
switch (day) {
  case 'Monday':
  case 'Tuesday':
    console.log('Early week');
    break; // break is required to prevent fall-through
  case 'Friday':
    console.log('End of work week');
    break;
  default:
    console.log('Other day');
}
```

JavaScript has three main loop constructs. `for` loops are best for counting; `while` loops are best when the loop condition is not count-based; `for...of` is the modern idiomatic way to iterate over arrays and any iterable.

```javascript
// Classic for loop
for (let i = 0; i < 5; i++) {
  console.log(i); // 0, 1, 2, 3, 4
}

// while loop
let count = 0;
while (count < 3) {
  console.log(count); // 0, 1, 2
  count++;
}

// for...of — iterate over values of an iterable (array, string, Set, Map, etc.)
const fruits = ['apple', 'banana', 'cherry'];
for (const fruit of fruits) {
  console.log(fruit); // apple, banana, cherry
}

// for...in — iterate over enumerable property KEYS of an object
// (Use with caution on arrays — see Pitfalls section)
const person = { name: 'Alice', age: 30 };
for (const key in person) {
  console.log(key, person[key]); // "name" "Alice", "age" 30
}
```

### Functions

Functions are the fundamental unit of code reuse in JavaScript. JavaScript has three syntactic forms for functions, and they differ in important ways.

A **function declaration** is hoisted — the entire function definition is moved to the top of its scope, so you can call it before it appears in the source file. A **function expression** assigns a function to a variable; it is not hoisted (only the variable declaration is hoisted, not the assignment). An **arrow function** is a compact syntax for function expressions and additionally does not have its own `this` binding — a crucial difference we will explore in Module 03.

```javascript
// Function declaration — hoisted, can be called before it appears in code
function greet(name) {
  return `Hello, ${name}!`;
}
console.log(greet('Alice')); // "Hello, Alice!"

// Function expression — assigned to a variable, not hoisted
const add = function(a, b) {
  return a + b;
};
console.log(add(2, 3)); // 5

// Arrow function — compact syntax, no own 'this'
const multiply = (a, b) => a * b; // implicit return for single expressions
const square = n => n * n;        // single parameter, parentheses optional
const hello = () => 'Hello!';     // no parameters, empty parentheses required

// For multi-line arrow functions, use explicit return and braces:
const processArray = (arr) => {
  const filtered = arr.filter(n => n > 0);
  const doubled = filtered.map(n => n * 2);
  return doubled;
};

// Default parameters
function power(base, exponent = 2) {
  return base ** exponent;
}
power(3);    // 9  (exponent defaults to 2)
power(2, 3); // 8

// Rest parameters — collect remaining arguments into an array
function sum(...numbers) {
  return numbers.reduce((total, n) => total + n, 0);
}
sum(1, 2, 3, 4); // 10

// Functions are first-class values — they can be passed as arguments
const numbers = [3, 1, 4, 1, 5, 9];
const sorted = numbers.slice().sort((a, b) => a - b); // [1, 1, 3, 4, 5, 9]
```

---

## Key Concepts

### JavaScript Engine

The program that executes JavaScript code. Major engines include V8 (Chrome, Node.js), SpiderMonkey (Firefox), and JavaScriptCore (Safari). Modern engines use JIT (Just-In-Time) compilation: they start interpreting JavaScript bytecode and compile frequently-executed "hot" functions to machine code for performance. This is why JavaScript can be fast despite being a dynamic language. Understanding that your code runs on a specific engine helps explain why performance can vary across browsers and why some optimisations work differently in Node.js than in the browser.

### Primitive vs. Object

JavaScript values are either primitives (`string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`) or objects (everything else, including arrays, functions, and instances of classes). Primitives are **immutable** — you cannot change the value `42`; you can only create a new value. Objects are **mutable** and accessed by reference: when you assign an object to two variables, both variables point to the same object in memory, so changing it through one variable changes it for the other. This reference vs. value distinction is the source of many subtle bugs.

### Type Coercion

JavaScript's automatic conversion of values from one type to another when operators or comparisons require it. Coercion is triggered by the `==` operator, the `+` operator (when one operand is a string, the other is coerced to a string), boolean contexts (e.g., `if (someValue)`), and various built-in functions. Understanding coercion rules (or avoiding them with `===` and explicit conversions) is essential for writing predictable code. The rule of thumb: always use `===` for equality checks, and explicitly convert types when needed (`String(x)`, `Number(x)`, `Boolean(x)`).

### Scope

The region of code where a variable is accessible. `let` and `const` are **block-scoped** — they are accessible only within the `{}` block they were declared in. `var` is **function-scoped** — it is accessible anywhere within the function it was declared in, which is why it can appear to be accessible before its declaration (hoisting). Understanding scope is the foundation for understanding closures (Module 02) and the reason to prefer `let`/`const` over `var`. Each function creates a new scope; blocks (`if`, `for`, `while`) create scope for `let`/`const` but not for `var`.

### Hoisting

JavaScript's behaviour of moving variable and function declarations to the top of their scope during the compilation phase, before execution. Function declarations are fully hoisted (both the declaration and the body). `var` declarations are hoisted but their values are not — the variable exists from the start of the function but has the value `undefined` until the assignment line is reached. `let` and `const` declarations are also hoisted but placed in a "temporal dead zone" — accessing them before their declaration throws a `ReferenceError`. Practically: use `let`/`const` and declare variables before you use them, and hoisting becomes a non-issue.

### The REPL

The Node.js REPL (Read-Eval-Print Loop) is an interactive JavaScript shell. Start it by running `node` with no arguments. You can type any JavaScript expression, press Enter, and see the result immediately. The REPL is invaluable for quickly testing a piece of syntax, checking how a method behaves, or debugging a value. The browser DevTools console is a similar environment. Get comfortable using both — experienced JavaScript developers use them dozens of times per day.

---

## Examples

### Example 1: Basic Calculator

**Problem:** Build a simple calculator that supports `+`, `-`, `*`, and `/` operations.

**Goal:** Practice functions, parameters, return values, and conditional branching.

```javascript
// A simple calculator function
// Parameters: a (number), operator (string), b (number)
// Returns: the result of the operation, or an error message for unknown operators
function calculate(a, operator, b) {
  switch (operator) {
    case '+': return a + b;
    case '-': return a - b;
    case '*': return a * b;
    case '/':
      if (b === 0) {
        return 'Error: division by zero';
      }
      return a / b;
    default:
      return `Error: unknown operator "${operator}"`;
  }
}

// Test the calculator
console.log(calculate(10, '+', 5));   // 15
console.log(calculate(10, '-', 3));   // 7
console.log(calculate(6, '*', 7));    // 42
console.log(calculate(10, '/', 2));   // 5
console.log(calculate(10, '/', 0));   // "Error: division by zero"
console.log(calculate(5, '%', 3));    // "Error: unknown operator "%""
```

**What to notice:** The function uses `switch` for the operator. Division by zero is handled explicitly — in JavaScript, `10 / 0` does not throw; it returns `Infinity`. The `default` case in the switch handles unrecognised operators gracefully.

---

### Example 2: String Manipulation

**Problem:** Write functions that transform strings: reverse a string, count vowels, and capitalise each word.

**Goal:** Practice string indexing, `for` loops, and working with string methods.

```javascript
// Reverse a string
// Approach: split into characters, reverse the array, join back
function reverseString(str) {
  return str.split('').reverse().join('');
}

// Count vowels in a string (case-insensitive)
function countVowels(str) {
  const vowels = 'aeiou';
  let count = 0;
  for (const char of str.toLowerCase()) {  // for...of iterates over string characters
    if (vowels.includes(char)) {
      count++;
    }
  }
  return count;
}

// Capitalise the first letter of each word
function titleCase(str) {
  return str
    .split(' ')                          // split on spaces into word array
    .map(word => {
      if (word.length === 0) return word; // handle extra spaces
      return word[0].toUpperCase() + word.slice(1).toLowerCase();
    })
    .join(' ');                          // join back into a single string
}

// Tests
console.log(reverseString('hello'));           // "olleh"
console.log(reverseString('racecar'));         // "racecar" (palindrome)
console.log(countVowels('JavaScript'));        // 3 (a, a, i)
console.log(countVowels('rhythm'));            // 0
console.log(titleCase('the quick brown fox')); // "The Quick Brown Fox"
console.log(titleCase('HELLO WORLD'));         // "Hello World"
```

**What to notice:** `split('')` converts a string to an array of characters. `for...of` iterates over string characters directly. The `map` in `titleCase` uses an arrow function that handles the edge case of empty strings from multiple consecutive spaces.

---

### Example 3: Array Processing

**Problem:** Given an array of student test scores, compute the average, find the highest and lowest scores, and return the passing scores (≥ 60).

**Goal:** Practice array methods (`filter`, `reduce`, `Math.max/min`), and writing functions that transform data.

```javascript
const scores = [72, 85, 45, 91, 60, 38, 77, 88, 55, 93];

// Compute the average score
function average(arr) {
  if (arr.length === 0) return 0;
  const total = arr.reduce((sum, score) => sum + score, 0);
  return total / arr.length;
}

// Get the highest score
function highest(arr) {
  return Math.max(...arr);  // spread array as individual arguments to Math.max
}

// Get the lowest score
function lowest(arr) {
  return Math.min(...arr);
}

// Return only passing scores (>= 60)
function passingScores(arr, threshold = 60) {
  return arr.filter(score => score >= threshold);
}

// Generate a summary report
function report(scores) {
  const passing = passingScores(scores);
  const passRate = ((passing.length / scores.length) * 100).toFixed(1);

  return {
    count: scores.length,
    average: average(scores).toFixed(1),
    highest: highest(scores),
    lowest: lowest(scores),
    passing: passing.length,
    passRate: `${passRate}%`,
  };
}

console.log(report(scores));
// {
//   count: 10,
//   average: '70.4',
//   highest: 93,
//   lowest: 38,
//   passing: 7,
//   passRate: '70.0%'
// }
```

**What to notice:** The spread operator `...arr` unpacks the array into individual arguments — `Math.max` does not accept an array directly. `reduce` accumulates values across the array, starting from the second argument (`0`). `.toFixed(1)` rounds a number to one decimal place and returns a string.

---

## Common Pitfalls

### Pitfall 1: Using `var` and Being Surprised by Hoisting

`var` is function-scoped, not block-scoped. This means a `var` declared inside a `for` loop leaks out of the loop.

```javascript
// Wrong — var leaks out of the for block
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Expected: 0, 1, 2
// Actual: 3, 3, 3
// Reason: all three callbacks share the same 'i' variable (var is function-scoped),
// and by the time they run, the loop has finished and i === 3

// Right — let creates a new binding for each iteration
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 0, 1, 2 (each callback closes over its own 'i')
```

Use `let` and `const` everywhere. Never use `var` in new code.

---

### Pitfall 2: Using `==` Instead of `===`

JavaScript's loose equality operator `==` performs type coercion before comparison. This leads to counterintuitive results.

```javascript
// Wrong — using == leads to coercion surprises
if (userId == 0) { /* ... */ }  // true when userId is 0, "", false, null, or []
if (score == "100") { /* ... */ } // true even though score is a number and "100" is a string

// Right — always use ===
if (userId === 0) { /* ... */ }   // only true when userId is exactly the number 0
if (score === 100) { /* ... */ }  // only true when score is exactly the number 100

// Extra pitfall: the only case where == is occasionally used intentionally:
// checking for both null and undefined at once
if (value == null) { /* ... */ }  // true for both null and undefined
// Equivalent to:
if (value === null || value === undefined) { /* ... */ }
```

The rule: always use `===` for equality checks. The only exception is `value == null` which is occasionally used as shorthand to check for both `null` and `undefined`.

---

### Pitfall 3: `typeof null === "object"`

This is a well-known JavaScript bug that has existed since 1995 and cannot be fixed without breaking the web. The `typeof` operator returns `"object"` for `null`, which is incorrect.

```javascript
// Wrong — trying to check if a value is a real object using typeof
function processData(data) {
  if (typeof data === 'object') {
    // BUG: this branch also runs when data is null!
    console.log(data.name); // TypeError: Cannot read property 'name' of null
  }
}

// Right — always check for null explicitly when the value might be null
function processData(data) {
  if (data !== null && typeof data === 'object') {
    console.log(data.name); // safe — data is definitely a non-null object
  }
}

// Or use optional chaining (?.) to safely access properties
function processData(data) {
  console.log(data?.name); // undefined if data is null/undefined, no error
}
```

Always guard against `null` when checking for objects, and prefer optional chaining (`?.`) to safely navigate potentially-null values.

---

## Cross-Links

- [[networks]] — JavaScript's `fetch` API is how front-end code communicates with backend servers; HTTP concepts covered in the networks topic are directly relevant starting in Module 05
- [[go]] — Go is commonly used to build the REST APIs that JavaScript front-ends consume; comparing Go's static typing with JavaScript's dynamic typing illuminates both languages
- [[shared/glossary#closure]] — Closures are introduced here and explored deeply in Module 02; the glossary entry provides a concise reference definition
- [[javascript-typescript-react/modules/02_core-javascript]] — Module 02 builds directly on this module, covering scope, closures, and the array methods used in the examples above
- [[javascript-typescript-react/modules/04_asynchronous-javascript]] — Module 04 covers the event loop and Promises, which build on the function concepts introduced here

---

## Summary

- **JavaScript** was created in 1995 by Brendan Eich at Netscape in ten days. It is the only language that runs natively in all web browsers and has grown into a universal runtime through Node.js.
- **ECMAScript** is the official specification; JavaScript is the implementation. ES2015 (ES6) was the most transformative update, adding `let`/`const`, arrow functions, classes, modules, and Promises.
- **Environments:** JavaScript runs in the browser (V8, SpiderMonkey, JavaScriptCore) and in Node.js. Use `node filename.js` to run a file, or `node` alone to start the REPL.
- **Variables:** Use `const` for values that won't be reassigned, `let` for values that will change. Avoid `var` — it has surprising function-scoping and hoisting behaviour.
- **Seven primitives:** `string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`. Everything else is an object.
- **Type coercion:** JavaScript automatically converts types in certain contexts. Always use `===` to avoid coercion surprises. The only exception is `value == null` (checks both null and undefined).
- **Control flow:** `if`/`else` for branching; `switch` for exact-match branching; `for` for counting loops; `while` for condition-based loops; `for...of` for iterating over arrays and iterables (preferred).
- **Functions:** Three forms — declaration (hoisted), expression (not hoisted), arrow (compact, no own `this`). All are first-class values that can be passed as arguments. Default parameters and rest parameters (`...args`) are available.
- **`typeof null === "object"`** is a historic bug — always check `value !== null && typeof value === 'object'` when testing for real objects.
