# Module 03: TypeScript Fundamentals

> Understand TypeScript as a design-time layer over JavaScript and use it to model reliable programs.

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

- Modules 01 and 02 in this topic.
- A text editor and a terminal.
- Node.js installed for command-line JavaScript examples, plus a modern browser for browser examples.

## Objectives

By the end of this module, you will be able to:
- Explain the purpose and runtime role of the core concepts in this module.
- Implement small runnable examples using the demonstrated syntax.
- Debug common beginner mistakes by connecting symptoms to underlying execution rules.
- Describe how this module prepares you for the next module in the path.

## Theory

### TypeScript Is Not a Different Runtime

TypeScript was created to make large JavaScript programs easier to maintain. Its key idea is pragmatic: add a static type checker and erase the types before execution. The browser or Node.js still runs JavaScript. This explains both TypeScript's power and its limits. It can catch impossible property access before deployment, but it cannot automatically validate unknown JSON at runtime unless you write checks.

### Annotating Values and Function Contracts

Types describe what values are allowed. Function signatures are especially valuable because they document inputs and outputs where modules meet. Type inference handles many local variables, while explicit types are useful at boundaries where humans need a stable contract.

```typescript
// Run type-check with: npx tsc --noEmit
function formatUser(name: string, age: number): string {
  // The return type guarantees callers receive display text.
  return `${name} (${age})`;
}

const label = formatUser("Ada", 36);
console.log(label);
```

### Objects, Interfaces, and Domain Models

Interfaces and type aliases let you name shapes in the domain. A good type is not just a bag of fields; it expresses the language of the problem. Optional fields, unions, and discriminated unions model uncertainty and alternatives directly instead of relying on comments.

```typescript
type LoadingState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; items: string[] }
  | { status: "error"; message: string };

function renderMessage(state: LoadingState): string {
  if (state.status === "success") {
    return `Loaded ${state.items.length} items.`;
  }

  if (state.status === "error") {
    return state.message;
  }

  return "Waiting...";
}
```

### Unknown Data and Runtime Validation

The safest type for external data is `unknown`, not `any`. `unknown` forces you to prove what you have before using it. This habit prepares you for React applications that consume APIs: trust your own types, but verify data that crosses a network, storage, or user-input boundary.

```typescript
function isUser(value: unknown): value is { id: string; name: string } {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  const candidate = value as { id?: unknown; name?: unknown };
  return typeof candidate.id === "string" && typeof candidate.name === "string";
}

const raw: unknown = JSON.parse('{"id":"u1","name":"Grace"}');
if (isUser(raw)) {
  console.log(raw.name.toUpperCase());
}
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

### 1. Using any to silence useful errors

Wrong approach:

```javascript
function printName(user: any) { console.log(user.nmae); }
```

Correct approach:

```javascript
function printName(user: { name: string }) { console.log(user.name); }
```

`any` opts out of the checker and hides spelling and contract mistakes.

### 2. Treating TypeScript as runtime validation

Wrong approach:

```javascript
const user = responseJson as User;
```

Correct approach:

```javascript
if (isUser(responseJson)) { console.log(responseJson.name); }
```

Assertions do not inspect runtime data; guards do.

### 3. Over-typing obvious locals

Wrong approach:

```javascript
const count: number = 0;
```

Correct approach:

```javascript
const count = 0;
```

Let inference handle simple locals and spend annotations on boundaries.

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
