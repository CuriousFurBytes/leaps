# Exercises: Module 01 — Introduction to JavaScript

## Instructions

Complete each exercise in order. Exercises increase in difficulty.
Run your solutions with Node.js: `node solution.js`
Submit your answers by creating a file alongside this one (e.g., `exercise1.js`) or by adding your solution in the `<details>` block below each exercise.

---

## Easy Exercises (1–3)

### Exercise 1

**Difficulty:** Easy
**Objective:** Identify and name all JavaScript primitive types

List all seven JavaScript primitive types. For each one, write a single-line code example that declares a variable of that type and assigns an appropriate value. Use `const` for all declarations.

```javascript
// Your answer here — create 7 const declarations, one for each primitive type
```

<details>
<summary>Solution (click to reveal)</summary>

```javascript
const myString = 'hello';           // string
const myNumber = 42;                // number
const myBoolean = true;             // boolean
const myNull = null;                // null
const myUndefined = undefined;      // undefined
const mySymbol = Symbol('unique');  // symbol
const myBigInt = 9007199254740991n; // bigint
```

All seven primitives: `string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`.

</details>

---

### Exercise 2

**Difficulty:** Easy
**Objective:** Write a function that accepts a parameter and returns a value

Write a function called `greet` that:
- Accepts a single parameter `name` (a string)
- Returns the string `"Hello, [name]! Welcome to JavaScript."`
- If `name` is not provided (i.e., it is `undefined`), defaults to `"stranger"`

Test it with: `greet('Alice')`, `greet('Bob')`, and `greet()`.

```javascript
// Your function here

// Tests (add these after your function):
console.log(greet('Alice'));  // "Hello, Alice! Welcome to JavaScript."
console.log(greet('Bob'));    // "Hello, Bob! Welcome to JavaScript."
console.log(greet());         // "Hello, stranger! Welcome to JavaScript."
```

<details>
<summary>Solution (click to reveal)</summary>

```javascript
function greet(name = 'stranger') {
  return `Hello, ${name}! Welcome to JavaScript.`;
}

// Arrow function alternative:
const greet = (name = 'stranger') => `Hello, ${name}! Welcome to JavaScript.`;

console.log(greet('Alice'));  // "Hello, Alice! Welcome to JavaScript."
console.log(greet('Bob'));    // "Hello, Bob! Welcome to JavaScript."
console.log(greet());         // "Hello, stranger! Welcome to JavaScript."
```

Key points: template literals (backtick strings) with `${}` for interpolation; default parameter syntax `name = 'stranger'`.

</details>

---

### Exercise 3

**Difficulty:** Easy
**Objective:** Use a `for` loop and an accumulator to process an array

Write a function called `sumArray` that:
- Accepts an array of numbers
- Uses a `for` loop (not `reduce`) to add them all up
- Returns the total
- Returns `0` for an empty array

```javascript
// Your function here

// Tests:
console.log(sumArray([1, 2, 3, 4, 5]));  // 15
console.log(sumArray([10, -5, 3]));       // 8
console.log(sumArray([]));                // 0
console.log(sumArray([42]));              // 42
```

<details>
<summary>Solution (click to reveal)</summary>

```javascript
function sumArray(numbers) {
  let total = 0;          // accumulator — starts at 0
  for (const n of numbers) {  // for...of iterates over values
    total += n;           // add each number to the running total
  }
  return total;
}

// Alternative with a classic for loop:
function sumArray(numbers) {
  let total = 0;
  for (let i = 0; i < numbers.length; i++) {
    total += numbers[i];
  }
  return total;
}
```

</details>

---

## Medium Exercises (4–6)

### Exercise 4

**Difficulty:** Medium
**Objective:** Implement a simple counter using closures

A closure is a function that remembers the variables from its enclosing scope even after that scope has finished executing.

Write a `makeCounter` function that:
- Takes no parameters
- Returns an object with three methods: `increment()`, `decrement()`, and `getCount()`
- The counter starts at `0`
- `increment()` increases the count by 1
- `decrement()` decreases the count by 1
- `getCount()` returns the current count

The count must be stored in a variable that is private to the closure — it should not be accessible from outside the returned object.

```javascript
// Your implementation here

// Tests:
const counter = makeCounter();
console.log(counter.getCount()); // 0
counter.increment();
counter.increment();
counter.increment();
console.log(counter.getCount()); // 3
counter.decrement();
console.log(counter.getCount()); // 2

// Each counter should have its own independent count:
const counter2 = makeCounter();
counter2.increment();
console.log(counter2.getCount()); // 1
console.log(counter.getCount());  // still 2 — not affected by counter2
```

<details>
<summary>Solution (click to reveal)</summary>

```javascript
function makeCounter() {
  let count = 0;  // private variable — not accessible outside makeCounter

  return {
    increment() {
      count++;
    },
    decrement() {
      count--;
    },
    getCount() {
      return count;
    },
  };
}
```

**How closures work here:** When `makeCounter()` returns, the `count` variable would normally be garbage-collected. But because the returned methods (`increment`, `decrement`, `getCount`) all reference `count`, JavaScript keeps `count` alive — it is "closed over" by those functions. Each call to `makeCounter()` creates a new `count` variable, which is why `counter` and `counter2` have independent counts.

</details>

---

### Exercise 5

**Difficulty:** Medium
**Objective:** Write a function that deep-clones a plain object

Write a function `deepClone(obj)` that creates and returns a deep copy of a plain JavaScript object (an object that contains only strings, numbers, booleans, null, arrays, and other plain objects — no functions, no class instances).

A deep clone means changes to the clone should not affect the original, and changes to the original should not affect the clone.

```javascript
// Your implementation here
// Constraint: do not use JSON.parse/JSON.stringify (it works but you should understand why)

// Tests:
const original = {
  name: 'Alice',
  scores: [90, 85, 77],
  address: {
    city: 'New York',
    zip: '10001',
  },
};

const clone = deepClone(original);

// Modifying the clone should not affect the original:
clone.name = 'Bob';
clone.scores.push(100);
clone.address.city = 'Los Angeles';

console.log(original.name);          // 'Alice'   (unchanged)
console.log(original.scores);        // [90, 85, 77] (unchanged)
console.log(original.address.city);  // 'New York' (unchanged)
```

<details>
<summary>Solution (click to reveal)</summary>

```javascript
function deepClone(obj) {
  // Base case: if the value is not an object (or is null), return it directly
  // (primitives are already copied by value)
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  // Handle arrays
  if (Array.isArray(obj)) {
    return obj.map(item => deepClone(item)); // recursively clone each element
  }

  // Handle plain objects
  const clone = {};
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      clone[key] = deepClone(obj[key]); // recursively clone each value
    }
  }
  return clone;
}
```

**Why not JSON?** `JSON.parse(JSON.stringify(obj))` works but silently drops `undefined` values, functions, and `Symbol` keys, and converts `Date` objects to strings. Understanding the recursive approach is more illuminating.

</details>

---

### Exercise 6

**Difficulty:** Medium
**Objective:** Use array destructuring to swap two variables

In a single line of code (using destructuring assignment), swap the values of two variables `a` and `b` without using a temporary variable.

Then write a `shuffle` function that randomly shuffles an array in-place using the Fisher-Yates algorithm (look it up if needed), using destructuring to perform the swaps.

```javascript
// Part 1: single-line swap
let a = 1;
let b = 2;
// Your one-liner here
console.log(a); // 2
console.log(b); // 1

// Part 2: Fisher-Yates shuffle (shuffles in-place, returns the array)
function shuffle(arr) {
  // Your implementation here
}

// Test:
const deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
shuffle(deck);
console.log(deck); // Should be the same 10 numbers in a random order
console.log(deck.length); // 10 — no elements lost or duplicated
```

<details>
<summary>Solution (click to reveal)</summary>

```javascript
// Part 1: destructuring swap — [b, a] = [a, b]
let a = 1;
let b = 2;
[b, a] = [a, b]; // creates a temporary array, then destructures it
console.log(a); // 2
console.log(b); // 1

// Part 2: Fisher-Yates shuffle
function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    // Pick a random index from 0 to i (inclusive)
    const j = Math.floor(Math.random() * (i + 1));
    // Swap arr[i] and arr[j] using destructuring
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}
```

</details>

---

## Hard Exercises (7–8)

### Exercise 7

**Difficulty:** Hard
**Objective:** Implement a `debounce` function

A debounce function is a utility that limits how often a function can run. When you debounce a function with a delay of 300ms, it means: "don't actually call this function until the user has stopped triggering it for 300ms".

This is extremely common in practice — for example, when you want to search an API as the user types, but not on every single keystroke. You wait until they pause.

Write a `debounce(fn, delay)` function that:
- Returns a new function
- When the returned function is called, it sets a timer to call `fn` after `delay` milliseconds
- If the returned function is called again before the timer fires, it resets the timer (cancels the old one and starts a new one)
- When the timer does fire, it calls `fn` with the arguments that were passed to the debounced call

```javascript
// Your implementation here

// Test:
let callCount = 0;
const expensiveSearch = debounce((query) => {
  callCount++;
  console.log(`Searching for: ${query}`);
}, 200);

expensiveSearch('j');
expensiveSearch('ja');
expensiveSearch('jav');
expensiveSearch('java');
expensiveSearch('javas');
// Wait 200ms...
// Only ONE search should fire: "Searching for: javas"
// callCount should be 1
```

<details>
<summary>Solution (click to reveal)</summary>

```javascript
function debounce(fn, delay) {
  let timeoutId = null; // tracks the current pending timer

  return function(...args) {
    // If there's a pending timer, cancel it
    if (timeoutId !== null) {
      clearTimeout(timeoutId);
    }

    // Start a new timer
    timeoutId = setTimeout(() => {
      fn(...args);     // call the original function with the latest arguments
      timeoutId = null; // clean up after firing
    }, delay);
  };
}
```

**Key concepts used:** closures (the returned function closes over `timeoutId`), `setTimeout`/`clearTimeout`, rest parameters, spread operator.

</details>

---

### Exercise 8

**Difficulty:** Hard
**Objective:** Write a simple EventEmitter class using ES2015 class syntax

An EventEmitter is a design pattern for decoupled communication. Code that emits events does not need to know anything about the code that listens to those events.

Implement an `EventEmitter` class with three methods:
- `on(event, listener)` — register a listener function for the given event name
- `off(event, listener)` — remove a specific listener from the given event
- `emit(event, ...args)` — call all listeners registered for the given event, passing any additional arguments to each listener

```javascript
// Your implementation here

// Tests:
const emitter = new EventEmitter();

function handleData(data) {
  console.log('Received:', data);
}

emitter.on('data', handleData);
emitter.on('data', (data) => console.log('Also received:', data));

emitter.emit('data', 'hello');
// Output:
// Received: hello
// Also received: hello

emitter.off('data', handleData);
emitter.emit('data', 'world');
// Output:
// Also received: world  (handleData was removed)

emitter.emit('unknown'); // no error, just nothing happens
```

<details>
<summary>Solution (click to reveal)</summary>

```javascript
class EventEmitter {
  constructor() {
    // Map from event name to array of listener functions
    this.listeners = new Map();
  }

  on(event, listener) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(listener);
    return this; // enable chaining
  }

  off(event, listener) {
    if (!this.listeners.has(event)) return this;
    const updated = this.listeners.get(event).filter(l => l !== listener);
    this.listeners.set(event, updated);
    return this;
  }

  emit(event, ...args) {
    if (!this.listeners.has(event)) return false;
    for (const listener of this.listeners.get(event)) {
      listener(...args);
    }
    return true;
  }
}
```

</details>

---

## Expert Exercise (9)

### Exercise 9

**Difficulty:** Expert
**Objective:** Implement a `Promise.all` equivalent from scratch

`Promise.all` takes an array of Promises and returns a new Promise that:
- Resolves with an array of all resolved values (in the same order as the input) when ALL input Promises have resolved
- Rejects immediately with the reason of the FIRST input Promise that rejects

Implement `promiseAll(promises)` without using `Promise.all`. You may use `new Promise(...)` and the `.then()` / `.catch()` methods.

```javascript
// Your implementation here

// Tests:
const p1 = Promise.resolve(1);
const p2 = new Promise(resolve => setTimeout(() => resolve(2), 100));
const p3 = Promise.resolve(3);

promiseAll([p1, p2, p3]).then(values => {
  console.log(values); // [1, 2, 3] — in order, even though p2 resolved last
});

// Rejection test:
const fail = new Promise((_, reject) => setTimeout(() => reject('oops'), 50));
promiseAll([p1, fail, p3]).catch(err => {
  console.log(err); // 'oops'
});
```

<details>
<summary>Solution (click to reveal)</summary>

```javascript
function promiseAll(promises) {
  return new Promise((resolve, reject) => {
    if (promises.length === 0) {
      resolve([]); // edge case: empty array resolves immediately with []
      return;
    }

    const results = new Array(promises.length); // pre-allocate to preserve order
    let resolvedCount = 0;

    promises.forEach((promise, index) => {
      // Wrap in Promise.resolve() to handle non-Promise values in the array
      Promise.resolve(promise)
        .then(value => {
          results[index] = value;    // store result at correct index
          resolvedCount++;

          if (resolvedCount === promises.length) {
            resolve(results);        // all done!
          }
        })
        .catch(reason => {
          reject(reason);            // first rejection short-circuits everything
        });
    });
  });
}
```

**Key insights:**
- We use a pre-allocated `results` array with index-based assignment to guarantee the output is in the same order as the input, even if Promises resolve out of order.
- `resolvedCount` tracks how many have resolved; when it equals `promises.length`, we're done.
- The first `.catch()` to fire calls `reject()`, and subsequent calls to `resolve()` or `reject()` on an already-settled Promise are silently ignored (Promises can only settle once).

</details>
