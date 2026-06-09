# Module 01: Web Language Foundations

> Learn what JavaScript is, how the web runs code, and how values, variables, functions, and browser output fit together.

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

## Overview

This module establishes the mental model needed for the rest of the JavaScript, TypeScript, and React path. Rather than memorizing syntax as isolated trivia, you will connect syntax to execution: where code runs, what values flow through it, and how small decisions become larger program behavior.

The goal is practical fluency. Each idea includes a runnable example so you can see the concept in motion, then adapt it for your own experiments. Later modules assume this foundation when they introduce larger programs, type systems, components, and production architecture.

## Prerequisites

- None; this module starts from zero.
- A text editor and a terminal.
- Node.js installed for command-line JavaScript examples, plus a modern browser for browser examples.

## Objectives

By the end of this module, you will be able to:
- Explain the purpose and runtime role of the core concepts in this module.
- Implement small runnable examples using the demonstrated syntax.
- Debug common beginner mistakes by connecting symptoms to underlying execution rules.
- Describe how this module prepares you for the next module in the path.

## Theory

### Why JavaScript Exists

JavaScript was created in 1995 so pages could respond to people without a round trip to the server for every tiny interaction. That history matters because JavaScript still lives at the boundary between documents, networks, users, and devices. The browser owns the page, the JavaScript engine executes your program, and Web APIs connect code to things such as timers, events, storage, and the document tree. Node.js later brought the same language to servers and tools, which is why the same syntax can power both a button click and a build script.

### Values, Variables, and Expressions

A JavaScript program starts with values. Numbers, strings, booleans, `null`, `undefined`, objects, arrays, and functions are the raw material. Variables are names that point at values; expressions are pieces of code that produce values. The difference is important: `const total = price * quantity` is not magic storage, it is a name bound to the result of an expression.

```javascript
// Run with: node foundations.js
const price = 12;
const quantity = 3;
const total = price * quantity;

console.log(`Total: $${total}`); // Prints the value produced by the expression.
```

### Functions and Control Flow

Functions package a repeatable idea behind a name. Control flow chooses which statements run and how many times. Together they let you move from isolated expressions to behavior: validate input, calculate a result, and report an outcome. JavaScript uses lexical scope, so a function can see variables from the surrounding block where it was defined.

```javascript
// Run with: node shipping.js
function shippingCost(subtotal) {
  // The branch chooses a rule based on the current value.
  if (subtotal >= 50) {
    return 0;
  }

  return 7;
}

console.log(shippingCost(42)); // 7
console.log(shippingCost(80)); // 0
```

### Browser Output as a Mental Model

The browser begins with an HTML document, builds a document object model, applies CSS, then lets JavaScript read events and request changes. A beginner does not need every DOM detail yet, but the mental model prevents confusion: JavaScript does not become the page; it asks the browser to change page state.

```html
<!-- Open this file in a browser. -->
<button id="count-button">Clicked 0 times</button>
<script>
  let count = 0;
  const button = document.querySelector("#count-button");

  button.addEventListener("click", () => {
    count += 1;
    button.textContent = `Clicked ${count} times`;
  });
</script>
```

## Key Concepts

- **Runtime:** The environment that executes JavaScript, such as a browser or Node.js. The same language can expose different capabilities depending on the host runtime.
- **Value:** A piece of data a program can compute with, store, pass, or return. Values are the atoms from which expressions and application state are built.
- **Function:** A named or anonymous unit of behavior that accepts inputs and returns an output. Functions make code reusable and create boundaries for reasoning.
- **Module:** A file-level boundary that can export selected values and import dependencies. Modules help programs grow without turning every variable into global state.
- **Contract:** An expectation between code and caller, such as input shape, return value, and error behavior. JavaScript documents many contracts by convention; TypeScript can encode many of them in types.

## Examples

### Example 1: Build a Small Formatter

Problem: create a reusable function that turns a user object into display text.

```javascript
const user = { id: "u1", name: "Ada Lovelace" };

function formatDisplayName(person) {
  return `${person.name} (#${person.id})`;
}

console.log(formatDisplayName(user));
```

The function keeps formatting logic in one place. If the product changes the display format later, callers do not need to duplicate the update.

### Example 2: Validate Before Continuing

Problem: stop a calculation when an input violates the expected contract.

```javascript
function divide(total, parts) {
  if (parts === 0) {
    throw new Error("Cannot divide by zero parts.");
  }

  return total / parts;
}

console.log(divide(12, 3));
```

The guard makes the failure explicit. Clear errors are easier to debug than surprising `Infinity`, `NaN`, or broken UI later.

## Common Pitfalls

### 1. Confusing assignment with comparison

Wrong approach:

```javascript
if (count = 3) { console.log("three"); }
```

Correct approach:

```javascript
if (count === 3) { console.log("three"); }
```

Assignment changes the variable; strict equality compares values without coercion.

### 2. Using a variable before defining it

Wrong approach:

```javascript
console.log(total);
const total = 5;
```

Correct approach:

```javascript
const total = 5;
console.log(total);
```

Declare names before use so the program reads in execution order.

### 3. Forgetting that browser APIs are not Node APIs

Wrong approach:

```javascript
document.querySelector("button");
```

Correct approach:

```javascript
// In Node, use console output or install a DOM environment intentionally.
console.log("No browser document exists here.");
```

The JavaScript language and host environment are related but separate.

## Cross-Links

- [[javascript-typescript-react]] for the full topic roadmap.
- [[go]] for language-independent mental models.
- [[css]] for browser, HTML, CSS, and HTTP context.
- [[go]] for vocabulary around callable behavior.

## Summary

- This module connects syntax to the runtime that executes it.
- Values, functions, modules, and contracts are the core vocabulary for the rest of the path.
- Runnable examples are the fastest way to test whether a concept is understood.
- Common mistakes usually come from confusing language behavior with host-environment behavior.
- The next module builds on this foundation with more modern JavaScript patterns and program organization.
