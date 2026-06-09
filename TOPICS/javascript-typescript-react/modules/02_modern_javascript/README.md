# Module 02: Modern JavaScript

> Use modern JavaScript syntax, collections, modules, errors, and data transformation patterns with confidence.

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

- Module 01: Web Language Foundations in this topic.
- A text editor and a terminal.
- Node.js installed for command-line JavaScript examples, plus a modern browser for browser examples.

## Objectives

By the end of this module, you will be able to:
- Explain the purpose and runtime role of the core concepts in this module.
- Implement small runnable examples using the demonstrated syntax.
- Debug common beginner mistakes by connecting symptoms to underlying execution rules.
- Describe how this module prepares you for the next module in the path.

## Theory

### From Script Snippets to Maintainable Programs

Modern JavaScript is the result of standardization after years of browser differences. ECMAScript editions added `let`, `const`, arrow functions, classes, modules, promises, destructuring, spread syntax, and richer collection methods. These features were not added merely for style; they help developers express intent, limit accidental mutation, and organize code into modules that tools can analyze.

### Data Transformation with Arrays and Objects

Real programs spend much of their time shaping data. Array methods such as `map`, `filter`, and `reduce` let you describe transformations directly. Objects group related fields. Destructuring and spread syntax make it easier to copy and update values without hiding mutation.

```javascript
// Run with: node totals.js
const cart = [
  { name: "Book", price: 18, quantity: 2 },
  { name: "Pen", price: 3, quantity: 5 },
];

const lineTotals = cart.map((item) => item.price * item.quantity);
const subtotal = lineTotals.reduce((sum, value) => sum + value, 0);

console.log({ lineTotals, subtotal });
```

### Modules and Boundaries

A module exports the pieces other files may use and keeps everything else private. This is a design boundary, not just a file boundary. Good modules expose a small vocabulary and hide implementation details so callers can rely on behavior rather than copying internals.

```javascript
// math.js
export function addTax(subtotal, rate) {
  // Convert a decimal rate such as 0.0825 into a rounded currency total.
  return Math.round(subtotal * (1 + rate) * 100) / 100;
}

// app.js
import { addTax } from "./math.js";
console.log(addTax(100, 0.0825));
```

### Errors and Defensive Thinking

JavaScript allows flexible inputs, which is powerful and dangerous. Defensive code checks assumptions at boundaries, throws useful errors when a contract is violated, and avoids swallowing failures. Later TypeScript modules move many checks earlier, but runtime checks still matter for user input, network data, and integration points.

```javascript
// Run with: node parse.js
function parseQuantity(raw) {
  const quantity = Number(raw);

  if (!Number.isInteger(quantity) || quantity < 1) {
    throw new Error("Quantity must be a positive integer.");
  }

  return quantity;
}

console.log(parseQuantity("3"));
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

### 1. Mutating shared objects accidentally

Wrong approach:

```javascript
const next = user;
next.name = "Ada";
```

Correct approach:

```javascript
const next = { ...user, name: "Ada" };
```

Copy before updating when other code may still depend on the old object.

### 2. Ignoring promise failures

Wrong approach:

```javascript
fetch("/api/items").then((r) => r.json());
```

Correct approach:

```javascript
fetch("/api/items")
  .then((r) => r.json())
  .catch((error) => console.error(error));
```

Every async path needs a failure path.

### 3. Exporting everything from a module

Wrong approach:

```javascript
export const internalCache = new Map();
```

Correct approach:

```javascript
const internalCache = new Map();
export function getCachedValue(key) { return internalCache.get(key); }
```

A narrow public API protects callers and implementation details.

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
