# Glossary: JavaScript, TypeScript and React

> Key terms used throughout this topic. Terms appear in the order they are typically encountered
> while working through the modules. Cross-references to related terms are noted where helpful.

---

## async/await

A syntax layer introduced in ES2017 that makes asynchronous code appear synchronous. An `async` function always returns a Promise. Inside an `async` function, the `await` keyword pauses execution of that function (without blocking the thread) until the awaited Promise resolves or rejects. Under the hood, `async`/`await` is syntactic sugar over Promises and the generator protocol — it does not create new concurrency primitives. See also: *Promise*, *event loop*.

---

## closure

A function that "closes over" variables from its surrounding lexical scope, retaining access to those variables even after the outer function has returned. Closures are fundamental to JavaScript: they power module patterns, callbacks, event handlers, memoization, and React hooks. A closure is not a copy of the value at the time the function is created — it is a live reference to the variable binding. This is why loop closures with `var` often surprise beginners.

---

## component

In React, a component is a function (or, in legacy code, a class) that accepts *props* as input and returns JSX describing what to render. Components are the fundamental unit of composition in React. They can be composed arbitrarily — a component can render other components, receive components as props, or return an array of components. Stateless components that return the same output for the same props are called "pure" components. See also: *props*, *state*, *JSX*.

---

## event loop

The mechanism that allows JavaScript — a single-threaded language — to handle asynchronous operations without blocking. The event loop continuously checks whether the call stack is empty; when it is, it moves the next callback from the task queue (macrotask queue) onto the stack. Microtasks (Promise callbacks) are drained completely before the next macrotask runs. Understanding the event loop is essential for debugging async timing issues, understanding why `setTimeout(fn, 0)` does not run immediately, and understanding how React's batched state updates work.

---

## generic

A TypeScript feature that allows types to be parameterized — that is, to accept a type variable that is specified by the caller rather than hardcoded. Generics enable writing reusable, type-safe functions and data structures. For example, `Array<T>` is a generic type: `Array<string>` and `Array<number>` are the same data structure but with different element types, and the type system enforces that only the correct type is placed in each array. Without generics, you would have to write separate versions of utility functions for every type they might operate on.

---

## hook

A hook is a special function in React that lets function components opt into React features like state, side effects, context, and refs. Hooks begin with the word `use` by convention (`useState`, `useEffect`, `useContext`, `useReducer`, `useMemo`, `useCallback`, `useRef`). Custom hooks are ordinary functions that call built-in hooks, allowing stateful logic to be extracted and reused across components. Hooks must only be called at the top level of a function component or another hook — never inside loops, conditions, or nested functions.

---

## hydration

The process of attaching React's event handlers and component state to HTML that was rendered on the server (SSR) and sent to the browser. When a server-rendered page arrives in the browser, it looks correct but is inert — hydration "activates" it by running the React component tree in the browser and reconciling it against the existing DOM. If the server-rendered HTML and the client-rendered output do not match, you get a "hydration mismatch" error. See also: *virtual DOM*.

---

## interface

A TypeScript construct that describes the shape of an object — its properties, their types, and whether they are optional or readonly. Interfaces support declaration merging (you can define the same interface in two places and TypeScript merges them) and are open-ended (can be extended). They are often used to describe API response shapes, component props types, and domain objects. In most cases, `interface` and `type` alias are interchangeable for object shapes, but interfaces are preferred when extension or declaration merging is needed.

---

## JSX

JavaScript XML — a syntax extension for JavaScript that lets you write HTML-like markup directly in JavaScript code. JSX is not HTML: it is syntactic sugar that compiles to `React.createElement()` calls (or the newer JSX transform, `_jsx()`). JSX is used to describe the UI tree in React components. Key differences from HTML: `class` becomes `className`, `for` becomes `htmlFor`, all tags must be closed, and JavaScript expressions are embedded with curly braces `{expression}`.

---

## Promise

An object representing the eventual result (or failure) of an asynchronous operation. A Promise is in one of three states: *pending* (the operation is in progress), *fulfilled* (the operation completed successfully, with a value), or *rejected* (the operation failed, with a reason). Promises can be chained with `.then()` and `.catch()`, or used with `async`/`await`. The key insight about Promises is that they are not threads — they are a structured way to register callbacks that run when the event loop is free. See also: *async/await*, *event loop*.

---

## props

Short for "properties" — the data passed from a parent component to a child component in React. Props are read-only from the child's perspective: a component must never mutate its own props. Props can be any JavaScript value: strings, numbers, booleans, objects, arrays, functions, or even other React components. The pattern of passing a function as a prop (often called a "callback prop" or "handler prop") is how child components communicate back up to their parents. See also: *state*, *component*.

---

## prototype chain

JavaScript's mechanism for inheritance between objects. Every JavaScript object has an internal `[[Prototype]]` reference pointing to another object (its prototype). When you access a property on an object, JavaScript first checks the object itself, then its prototype, then the prototype's prototype, continuing up the chain until it reaches `null` (the top of the chain). ES2015 `class` syntax is syntactic sugar over the prototype chain — `class Dog extends Animal` sets `Dog.prototype`'s `[[Prototype]]` to `Animal.prototype`. Understanding the prototype chain explains how methods on `Array.prototype` (like `.map()`, `.filter()`, `.reduce()`) are accessible on every array.

---

## state

Data managed by a React component that, when changed, causes the component to re-render. State is created with the `useState` hook (or `useReducer` for complex state). Unlike props (which are owned by the parent), state is owned and controlled by the component that declares it. State should contain only the minimum information needed to render correctly — derived values should be computed on the fly, not stored in state. Changing state is always done by calling the setter function returned by `useState`; direct mutation of the state variable does not trigger a re-render.

---

## TypeScript type

The fundamental building block of TypeScript's type system. A type is a set of values that a variable can hold. TypeScript includes primitive types (`string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`), object types, array types, function types, union types (`string | number`), intersection types (`A & B`), literal types (`"GET" | "POST"`), and special types (`any`, `unknown`, `never`, `void`). Types can be named with a `type` alias. Unlike interfaces, type aliases can represent primitives, unions, intersections, and tuples — not just object shapes.

---

## virtual DOM

React's in-memory representation of the UI tree. Instead of modifying the real DOM directly (which is slow), React maintains a virtual copy of the DOM tree in JavaScript. When state or props change, React creates a new virtual DOM tree and diffs it against the previous one (a process called "reconciliation"). Only the differences are applied to the real DOM. This batching of changes is what makes React performant even with frequent state updates. With React 18's concurrent rendering, the virtual DOM diff can be interrupted and prioritized.
