# Cheatsheet: JavaScript, TypeScript and React

> Quick reference for the most commonly used syntax and patterns.
> This is not a substitute for the modules — use it for revision and as a desk reference.

---

## JavaScript Array Methods

```javascript
const nums = [1, 2, 3, 4, 5];

// map — transform each element, return new array
const doubled = nums.map(n => n * 2);           // [2, 4, 6, 8, 10]

// filter — keep elements where predicate is true
const evens = nums.filter(n => n % 2 === 0);    // [2, 4]

// reduce — fold array to a single value
const sum = nums.reduce((acc, n) => acc + n, 0); // 15

// find — first element matching predicate (or undefined)
const first = nums.find(n => n > 3);             // 4

// findIndex — index of first match (or -1)
const idx = nums.findIndex(n => n > 3);          // 3

// some — true if any element matches
const hasEven = nums.some(n => n % 2 === 0);    // true

// every — true if all elements match
const allPos = nums.every(n => n > 0);           // true

// flat — flatten nested arrays
const nested = [[1, 2], [3, 4]];
const flat = nested.flat();                       // [1, 2, 3, 4]

// flatMap — map then flatten one level
const words = ['hello world', 'foo bar'];
const letters = words.flatMap(s => s.split(' ')); // ['hello', 'world', 'foo', 'bar']

// includes — check membership
nums.includes(3);                                 // true

// slice — extract subarray (non-mutating)
nums.slice(1, 3);                                 // [2, 3]

// spread to copy or combine
const copy = [...nums];
const combined = [...nums, 6, 7];
```

---

## Async Patterns

```javascript
// Promises
fetch('/api/data')
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));

// async/await (preferred)
async function loadData() {
  try {
    const res = await fetch('/api/data');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    return data;
  } catch (err) {
    console.error('Failed:', err);
    throw err;  // re-throw so caller knows it failed
  }
}

// Promise.all — run multiple async operations in parallel
async function loadAll() {
  const [users, posts] = await Promise.all([
    fetch('/api/users').then(r => r.json()),
    fetch('/api/posts').then(r => r.json()),
  ]);
  return { users, posts };
}

// Promise.allSettled — like Promise.all but doesn't short-circuit on failure
const results = await Promise.allSettled([
  fetch('/api/a').then(r => r.json()),
  fetch('/api/b').then(r => r.json()),
]);
// results[0] = { status: 'fulfilled', value: ... }
// results[1] = { status: 'rejected',  reason: ... }
```

---

## TypeScript Type Syntax

```typescript
// Primitive types
let name: string = 'Alice';
let age: number = 30;
let active: boolean = true;
let nothing: null = null;
let missing: undefined = undefined;

// Union types
let id: string | number = 'abc';
id = 123; // also valid

// Literal types
type Direction = 'north' | 'south' | 'east' | 'west';
type StatusCode = 200 | 400 | 401 | 404 | 500;

// Arrays
let scores: number[] = [90, 85, 77];
let tags: Array<string> = ['js', 'ts']; // equivalent

// Tuples
let point: [number, number] = [10, 20];

// Object types with interface
interface User {
  id: number;
  name: string;
  email?: string;         // optional
  readonly createdAt: Date; // readonly
}

// Type alias (can express anything interface can, plus unions/intersections)
type ID = string | number;
type Point = { x: number; y: number };

// Generics
function identity<T>(value: T): T {
  return value;
}

function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

// Utility types
type PartialUser = Partial<User>;          // all fields optional
type RequiredUser = Required<User>;        // all fields required
type ReadonlyUser = Readonly<User>;        // all fields readonly
type UserName = Pick<User, 'id' | 'name'>; // only id and name
type WithoutEmail = Omit<User, 'email'>;   // everything except email
type UserOrNull = User | null;
type NonNullUser = NonNullable<UserOrNull>; // removes null/undefined

// Type narrowing
function printId(id: string | number) {
  if (typeof id === 'string') {
    console.log(id.toUpperCase()); // TypeScript knows id is string here
  } else {
    console.log(id.toFixed(2));    // TypeScript knows id is number here
  }
}
```

---

## React Hooks API

```typescript
import { useState, useEffect, useContext, useReducer,
         useMemo, useCallback, useRef } from 'react';

// useState — local component state
const [count, setCount] = useState<number>(0);
setCount(count + 1);          // direct value
setCount(prev => prev + 1);  // functional update (safe with stale closures)

// useEffect — side effects and subscriptions
useEffect(() => {
  document.title = `Count: ${count}`;
  return () => { /* cleanup runs before next effect or unmount */ };
}, [count]); // dependency array — effect runs when count changes

useEffect(() => { /* runs once on mount */ }, []);
useEffect(() => { /* runs on every render */ }); // no array — usually a mistake

// useRef — mutable ref, does not trigger re-render
const inputRef = useRef<HTMLInputElement>(null);
inputRef.current?.focus();

// Storing a mutable value (not for rendering)
const prevCountRef = useRef<number>(0);

// useMemo — memoize expensive computation
const expensiveValue = useMemo(() => compute(a, b), [a, b]);

// useCallback — memoize function reference (for stable props/deps)
const handleClick = useCallback(() => setCount(c => c + 1), []);

// useReducer — complex state logic
type Action = { type: 'increment' } | { type: 'reset' };
function reducer(state: number, action: Action): number {
  switch (action.type) {
    case 'increment': return state + 1;
    case 'reset':     return 0;
  }
}
const [state, dispatch] = useReducer(reducer, 0);
dispatch({ type: 'increment' });

// useContext — consume context without prop drilling
const theme = useContext(ThemeContext); // ThemeContext created with createContext()
```

---

## Common React Patterns

```typescript
// Function component with typed props
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary';
}

function Button({ label, onClick, disabled = false, variant = 'primary' }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {label}
    </button>
  );
}

// Custom hook pattern
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setStoredValue = (newValue: T) => {
    setValue(newValue);
    window.localStorage.setItem(key, JSON.stringify(newValue));
  };

  return [value, setStoredValue] as const;
}

// Conditional rendering
function Status({ isLoading, error, data }: StatusProps) {
  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;
  if (!data) return null;
  return <div>{data.name}</div>;
}

// List rendering — always provide a stable key
function List({ items }: { items: Item[] }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}

// Context pattern
const ThemeContext = createContext<'light' | 'dark'>('light');

function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  );
}
```
