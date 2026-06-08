# Module 2: Functions

[← Variables and Types](../1.%20Variables%20and%20Types/) | [Topic Home](../README.md) | [Next → Control Flow](../3.%20Control%20Flow/)

![Status](https://img.shields.io/badge/status-Not%20Started-lightgrey)
![Module](https://img.shields.io/badge/module-2%20of%209-blue)
![Time](https://img.shields.io/badge/time-5--6%20hours-orange)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner--Intermediate-yellow)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Core Concepts](#core-concepts)
  - [Defining and Calling Functions](#defining-and-calling-functions)
  - [Parameters and Arguments](#parameters-and-arguments)
  - [Return Values](#return-values)
  - [Scope — LEGB Rule](#scope--legb-rule)
  - [First-Class Functions](#first-class-functions)
  - [Lambda Functions](#lambda-functions)
  - [Closures](#closures)
  - [Type Hints](#type-hints)
  - [Docstrings](#docstrings)
- [Common Beginner Mistakes](#common-beginner-mistakes)
- [Mental Models](#mental-models)
- [Practical Examples](#practical-examples)
- [Module Resources](#module-resources)

---

## Overview

Functions are the primary building block for organizing Python programs into reusable, readable units. A function encapsulates a sequence of operations under a name — you define it once and call it many times.

Python's approach to functions goes beyond simple subroutines. Functions are **first-class objects** — they can be assigned to variables, passed as arguments, returned from other functions, and stored in data structures. This enables powerful patterns like higher-order functions, callbacks, and decorators.

This module covers everything from basic `def` syntax through the subtleties of scope, closures, and lambda expressions.

---

## Learning Goals

By the end of this module, you will be able to:

1. Define functions using `def` with correct syntax
2. Use positional, keyword, default, `*args`, and `**kwargs` parameters
3. Write functions with `return` statements, including multiple return values
4. Explain the LEGB scope rule and predict variable lookup behavior
5. Treat functions as first-class objects: pass them as arguments and return them
6. Write lambda functions and know when (and when not) to use them
7. Explain what a closure is and create one intentionally
8. Add type hints following PEP 484 conventions
9. Write PEP 257-compliant docstrings
10. Avoid the mutable default argument trap

---

## Prerequisites

- **Required:** Module 0 — Introduction
- **Required:** Module 1 — Variables and Types

---

## Core Concepts

### Defining and Calling Functions

```python
# Basic function definition
def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"

# Calling the function
message = greet("Alice")
print(message)    # Hello, Alice!

# A function without a return statement returns None
def say_hi():
    print("Hi!")

result = say_hi()   # prints "Hi!"
print(result)       # None

# Functions can have multiple return points
def absolute_value(x):
    if x >= 0:
        return x
    return -x

# Functions can return multiple values (as a tuple)
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 4, 1, 5, 9, 2, 6])
print(low, high)  # 1 9
```text

---

### Parameters and Arguments

Python has a rich system for defining how arguments are passed to functions:

```python
# 1. Positional parameters — matched by position
def add(a, b):
    return a + b

add(3, 5)        # a=3, b=5
add(b=5, a=3)    # keyword argument — order doesn't matter

# 2. Default parameter values
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Alice")              # "Hello, Alice!"
greet("Bob", "Good morning") # "Good morning, Bob!"
greet("Carol", greeting="Hi") # "Hi, Carol!"

# 3. *args — variable positional arguments (collected as a tuple)
def add_all(*numbers):
    return sum(numbers)

add_all(1, 2, 3)         # 6
add_all(1, 2, 3, 4, 5)   # 15
add_all()                 # 0

# 4. **kwargs — variable keyword arguments (collected as a dict)
def configure(**options):
    for key, value in options.items():
        print(f"  {key} = {value}")

configure(debug=True, port=8080, host="localhost")

# 5. Combined: positional, *args, keyword-only, **kwargs
def complex_func(pos1, pos2, *args, kw_only, **kwargs):
    print(f"pos1={pos1}, pos2={pos2}")
    print(f"extra args: {args}")
    print(f"kw_only={kw_only}")
    print(f"extra kwargs: {kwargs}")

complex_func(1, 2, 3, 4, kw_only="must_be_named", extra="yes")

# 6. Positional-only parameters (/) — Python 3.8+
def force_positional(x, y, /):
    return x + y

force_positional(1, 2)      # OK
# force_positional(x=1, y=2)  # TypeError! Can't use keyword syntax

# 7. Keyword-only parameters (*) — must be passed by keyword
def keyword_only(*, required_kw, optional_kw="default"):
    return f"{required_kw}, {optional_kw}"

keyword_only(required_kw="hello")    # OK
# keyword_only("hello")              # TypeError! Must use keyword

# 8. Unpacking when calling
numbers = [1, 2, 3]
add_all(*numbers)   # same as add_all(1, 2, 3)

config = {"debug": True, "port": 8080}
configure(**config)  # same as configure(debug=True, port=8080)
```text

**Parameter ordering rule:**

```text
def func(positional, /, normal, *args, keyword_only, **kwargs):
```text

---

### Return Values

```python
# Returning multiple values (actually a tuple)
def divmod_custom(a, b):
    quotient = a // b
    remainder = a % b
    return quotient, remainder  # returns tuple (quotient, remainder)

q, r = divmod_custom(17, 5)
result = divmod_custom(17, 5)   # result is (3, 2) — a tuple
print(result)                    # (3, 2)

# Early return for guard clauses
def safe_sqrt(x):
    if x < 0:
        return None  # early exit
    return x ** 0.5

# Implicit None return
def procedure():
    print("doing work")
    # no return statement — implicitly returns None

# Return in try/finally
def safe_open(path):
    try:
        f = open(path)
        return f.read()
    except FileNotFoundError:
        return None     # finally block still runs even after return
    finally:
        pass  # cleanup runs regardless
```text

---

### Scope — LEGB Rule

When Python encounters a name, it searches for it in this order:

1. **L**ocal — the current function's namespace
2. **E**nclosing — any enclosing function's namespace (for nested functions)
3. **G**lobal — the module's top-level namespace
4. **B**uilt-in — Python's built-in names (`print`, `len`, `range`, etc.)

```python
# LEGB demonstration
x = "global"   # Global

def outer():
    x = "enclosing"   # Enclosing

    def inner():
        x = "local"   # Local
        print(x)       # "local" — found in L

    inner()
    print(x)    # "enclosing" — inner's local x doesn't affect outer

outer()
print(x)    # "global" — outer's enclosing x doesn't affect global

# Accessing (not modifying) outer scope variables — works naturally
count = 0

def show_count():
    print(count)   # reads global count — fine

show_count()   # 0

# MODIFYING a global variable — requires `global` keyword
def increment():
    global count   # tells Python "use the global count"
    count += 1

increment()
print(count)   # 1

# `nonlocal` — modify an enclosing (non-global) variable
def make_counter():
    count = 0

    def increment():
        nonlocal count   # modify the enclosing count
        count += 1
        return count

    return increment

counter = make_counter()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
```text

> [!NOTE]
> Using `global` is often a sign of poor design. Most functions should get all their inputs via parameters and return outputs via `return`. Reserve `global` for true application-level state (logging config, feature flags) and use it sparingly.

---

### First-Class Functions

In Python, functions are objects. They can be:
- Assigned to variables
- Stored in data structures (lists, dicts)
- Passed as arguments to other functions
- Returned from functions

```python
# Assigning a function to a variable
def square(x):
    return x ** 2

my_func = square    # no () — we're referencing the function, not calling it
print(my_func(5))   # 25

# Storing functions in a list
operations = [abs, str, type]
for op in operations:
    print(op(-42))   # 42, '-42', <class 'int'>

# Passing functions as arguments (higher-order functions)
def apply(func, value):
    return func(value)

print(apply(square, 5))   # 25
print(apply(str, 42))     # '42'

# Built-in higher-order functions
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(sorted(numbers))                          # [1, 1, 2, 3, 4, 5, 6, 9]
print(sorted(numbers, reverse=True))            # [9, 6, 5, 4, 3, 2, 1, 1]

words = ["banana", "apple", "cherry", "date"]
print(sorted(words))                            # alphabetical
print(sorted(words, key=len))                   # by length
print(sorted(words, key=lambda w: w[-1]))       # by last character

# map() and filter() (return lazy iterators)
squares = list(map(square, [1, 2, 3, 4, 5]))   # [1, 4, 9, 16, 25]
evens = list(filter(lambda x: x % 2 == 0, range(10)))  # [0, 2, 4, 6, 8]

# Returning a function
def make_multiplier(factor):
    def multiplier(x):
        return x * factor   # 'factor' comes from enclosing scope
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5))   # 10
print(triple(5))   # 15
```text

---

### Lambda Functions

Lambda functions are anonymous functions defined with a single expression. They're syntactic sugar for simple, one-expression functions.

```python
# Lambda syntax: lambda arguments: expression
square = lambda x: x ** 2
add = lambda x, y: x + y

# Equivalent to:
def square(x):
    return x ** 2

# Common uses: as keys for sorting, as simple callbacks
words = ["banana", "apple", "cherry"]
sorted_by_length = sorted(words, key=lambda w: len(w))
sorted_by_last = sorted(words, key=lambda w: w[-1])

# With map and filter
squares = list(map(lambda x: x**2, range(10)))
evens = list(filter(lambda x: x % 2 == 0, range(10)))

# As default arguments or in data structures
operations = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
}
print(operations["+"](3, 5))  # 8
```text

**When NOT to use lambdas:**

```python
# BAD — this lambda is less readable than a def
process = lambda x: x.strip().lower().replace(" ", "_")

# GOOD — give it a name if it's complex
def to_slug(x):
    return x.strip().lower().replace(" ", "_")

# BAD — assigning lambda to a name (defeats the purpose of anonymity)
double = lambda x: x * 2   # use def instead

# GOOD use — inline, one-expression, throwaway
sorted(items, key=lambda item: item.priority)
```text

> [!NOTE]
> The Zen of Python says "explicit is better than implicit." If a lambda needs more than one operation or a descriptive name, use `def`. Lambdas shine when inline, anonymous, and obvious.

---

### Closures

A closure is a function that "remembers" variables from its enclosing scope even after the enclosing function has finished executing.

```python
def make_counter(start=0):
    """Return a counter function that starts at `start`."""
    count = start   # this variable is "closed over"

    def counter():
        nonlocal count
        count += 1
        return count

    return counter   # return the inner function, not its result

# The enclosing function has returned, but `count` lives on inside the closure
counter_a = make_counter()
counter_b = make_counter(10)

print(counter_a())  # 1
print(counter_a())  # 2
print(counter_b())  # 11
print(counter_a())  # 3 — counter_b's state is separate

# Practical closure: memoization
def make_memoized(func):
    cache = {}   # closed over by the wrapper

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper

@make_memoized
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(50))  # fast — results are cached

# Real-world closure: event handlers, callbacks
def make_button_handler(button_name):
    def handle_click():
        print(f"Button '{button_name}' was clicked")
    return handle_click

ok_handler = make_button_handler("OK")
cancel_handler = make_button_handler("Cancel")
ok_handler()      # Button 'OK' was clicked
cancel_handler()  # Button 'Cancel' was clicked
```text

**Inspecting closures:**

```python
def outer():
    x = 10
    def inner():
        return x
    return inner

f = outer()
print(f.__closure__)   # (<cell at 0x...>,)
print(f.__closure__[0].cell_contents)  # 10
```text

---

### Type Hints

Python 3.5+ supports optional type annotations (PEP 484). They don't affect runtime behavior but enable static analysis.

```python
# Basic type hints
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

# Optional values (Python 3.10+ union syntax)
def find_user(user_id: int) -> dict | None:
    ...

# Older syntax (Python 3.5-3.9)
from typing import Optional
def find_user(user_id: int) -> Optional[dict]:
    ...

# Complex types
from typing import List, Dict, Tuple, Callable
def process(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Callable type hint
def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)

# Variable annotations
count: int = 0
names: list[str] = []

# Type aliases
Vector = list[float]
def dot_product(v1: Vector, v2: Vector) -> float:
    return sum(a * b for a, b in zip(v1, v2))
```text

---

### Docstrings

PEP 257 defines conventions for Python docstrings. Write them for every public function.

```python
def simple_function():
    """One-line docstring for simple functions."""
    pass

def complex_function(param1: str, param2: int = 0) -> list[str]:
    """
    Short, imperative description (one line).

    Longer description if needed. Explain what the function does,
    not how it does it. This paragraph can be several sentences.

    Args:
        param1: Description of the first parameter.
        param2: Description of the second parameter. Defaults to 0.

    Returns:
        A list of strings derived from param1 by some process.
        Describe what's in the list, not just the type.

    Raises:
        ValueError: If param1 is empty.
        TypeError: If param2 is not an integer.

    Examples:
        >>> complex_function("hello", 3)
        ['hello', 'hello', 'hello']
        >>> complex_function("test")
        ['test']
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    return [param1] * param2 if param2 > 0 else [param1]
```text

---

## Common Beginner Mistakes

> [!WARNING]
> **The Mutable Default Argument Trap**
> This is one of Python's most famous bugs. Default argument values are evaluated ONCE when the function is defined, not each time it's called. If the default is mutable (like a list or dict), it's shared across all calls:
>
> ```python
> # WRONG — the list is created once and shared!
> def append_to(item, lst=[]):
>     lst.append(item)
>     return lst
>
> print(append_to(1))   # [1]
> print(append_to(2))   # [1, 2] — NOT [2]! The same list was reused!
> print(append_to(3))   # [1, 2, 3]
>
> # RIGHT — use None as default, create inside the function
> def append_to(item, lst=None):
>     if lst is None:
>         lst = []
>     lst.append(item)
>     return lst
>
> print(append_to(1))   # [1]
> print(append_to(2))   # [2] — fresh list each time
> ```

> [!WARNING]
> **Forgetting `return` — Getting None Instead of a Value**
> ```python
> def square(x):
>     x ** 2   # computed but NOT returned!
>
> result = square(5)
> print(result)   # None — not 25!
>
> # Fix:
> def square(x):
>     return x ** 2
> ```

> [!WARNING]
> **Modifying Global State Without `global`**
> ```python
> count = 0
> def increment():
>     count += 1   # UnboundLocalError! Python sees `count +=` as local assignment
>                  # but count hasn't been assigned locally yet
>
> # Fix:
> def increment():
>     global count
>     count += 1
> ```

> [!WARNING]
> **Lambda in a Loop — The Late Binding Closure Problem**
> ```python
> # WRONG — all lambdas capture the same `i` variable by reference
> functions = [lambda: i for i in range(5)]
> print([f() for f in functions])   # [4, 4, 4, 4, 4] — all return 4!
>
> # RIGHT — capture by value using a default argument
> functions = [lambda i=i: i for i in range(5)]
> print([f() for f in functions])   # [0, 1, 2, 3, 4]
> ```

---

## Mental Models

**Functions as black boxes:**

A well-designed function is a black box: it takes inputs (parameters) and produces outputs (return value) with no side effects that its caller needs to know about. What happens inside the function is invisible to the caller — only the interface (inputs and outputs) matters. This is the foundation of *encapsulation* and *abstraction*.

**Functions as objects:**

Unlike many languages, Python treats functions identically to any other object. A `def` statement creates a function object and assigns it to a name. `square = lambda x: x**2` does the same thing. This is why `sorted(items, key=some_function)` just works — `some_function` is an object you're passing like any other value.

**Closures as function + state:**

A closure is a function that carries a piece of state with it. Think of it as a function "bundled together" with the variables from its environment. This is an alternative to using objects for simple stateful operations.

---

## Practical Examples

### Example 1: Simple Utility Functions

```python
def clamp(value: float, minimum: float, maximum: float) -> float:
    """Constrain a value to be within [minimum, maximum]."""
    return max(minimum, min(value, maximum))

print(clamp(150, 0, 100))   # 100 (clamped to max)
print(clamp(-5, 0, 100))    # 0   (clamped to min)
print(clamp(50, 0, 100))    # 50  (within range)
```text

### Example 2: Higher-Order Functions

```python
def compose(*functions):
    """
    Return a function that applies each function in sequence (right to left).

    compose(f, g, h)(x) == f(g(h(x)))
    """
    def composed(x):
        result = x
        for func in reversed(functions):
            result = func(result)
        return result
    return composed

# Build a text-cleaning pipeline
import re
clean_text = compose(
    str.strip,
    str.lower,
    lambda s: re.sub(r'\s+', ' ', s),
)

messy = "  Hello   WORLD  "
print(clean_text(messy))   # "hello world"
```text

### Example 3: Decorator Pattern Preview

```python
import time
import functools

def timer(func):
    """Decorator that prints how long a function takes."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__!r} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_sum(n):
    """Sum numbers from 0 to n."""
    return sum(range(n))

total = slow_sum(10_000_000)   # 'slow_sum' took 0.2847s
```text

### Example 4: Recursive Functions

```python
def factorial(n: int) -> int:
    """
    Calculate n! recursively.

    >>> factorial(0)
    1
    >>> factorial(5)
    120
    """
    if n < 0:
        raise ValueError(f"factorial is not defined for negative numbers, got {n}")
    if n == 0:
        return 1
    return n * factorial(n - 1)

print(factorial(10))   # 3628800
```text

### Example 5: Functions with Complex Signatures

```python
def create_report(
    title: str,
    data: list[dict],
    *,
    max_rows: int = 50,
    sort_by: str | None = None,
    ascending: bool = True,
    include_totals: bool = False,
) -> str:
    """
    Generate a formatted text report from tabular data.

    Args:
        title: The report title.
        data: List of dicts, each representing one row.
        max_rows: Maximum number of rows to include. Defaults to 50.
        sort_by: Column name to sort by. If None, preserves order.
        ascending: Sort direction. Defaults to ascending (True).
        include_totals: Whether to include a totals row. Defaults to False.

    Returns:
        Formatted report as a string.
    """
    rows = data[:max_rows]
    if sort_by:
        rows = sorted(rows, key=lambda r: r.get(sort_by, ""), reverse=not ascending)

    lines = [f"=== {title} ==="]
    for row in rows:
        lines.append(str(row))

    if include_totals:
        lines.append(f"Total rows: {len(rows)}")

    return "\n".join(lines)
```text

---

## Module Resources

| Resource | Link |
|----------|------|
| Exercises | [EXERCISES.md](./EXERCISES.md) |
| Test | [TEST.md](./TEST.md) |

---

*Module 2 of 9 — Python Topic*
