# Module 2: Functions — Exercises

[← Module Home](./README.md) | [Topic Home](../README.md)

10 exercises covering all aspects of Python functions. Complete them in order — they build in complexity.

**Scoring:** 10 exercises × varying pts = 30 pts possible  
**Passing:** 24 / 30 (80%)

---

## Exercise 1 — Basic Function Anatomy

**Difficulty:** Easy | **Points:** 2

### Task

Write three simple utility functions to practice the basic syntax.

### Requirements

1. `is_even(n: int) -> bool` — returns True if n is even
2. `celsius_to_kelvin(c: float) -> float` — converts Celsius to Kelvin (add 273.15)
3. `count_vowels(s: str) -> int` — counts vowels (a,e,i,o,u, case-insensitive) in a string

Each must have a docstring and type hints. Test each function.

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
def is_even(n: int) -> bool:
    """Return True if n is even, False otherwise."""
    return n % 2 == 0

def celsius_to_kelvin(c: float) -> float:
    """Convert temperature from Celsius to Kelvin."""
    return c + 273.15

def count_vowels(s: str) -> int:
    """Count the number of vowels (a,e,i,o,u) in the string s, case-insensitive."""
    return sum(1 for char in s.lower() if char in "aeiou")

# Tests
assert is_even(4) == True
assert is_even(7) == False
assert is_even(0) == True

assert celsius_to_kelvin(0) == 273.15
assert celsius_to_kelvin(100) == 373.15
assert celsius_to_kelvin(-273.15) == 0.0

assert count_vowels("hello") == 2
assert count_vowels("AEIOU") == 5
assert count_vowels("rhythm") == 0

print("All tests passed!")
```text

</details>

---

## Exercise 2 — All Parameter Types

**Difficulty:** Easy | **Points:** 2

### Task

Write a function that demonstrates all parameter types: positional, default, *args, keyword-only, **kwargs.

### Requirements

Write `format_message(template, *args, prefix="", **metadata)` that:
- `template`: a format string with `{}` placeholders
- `*args`: values to fill into the template
- `prefix`: optional string to prepend (keyword-only)
- `**metadata`: any additional key=value pairs to append as `[key=value]`

Example:
```python
format_message("Hello, {}!", "Alice", prefix="[INFO]", timestamp="12:00")
# → "[INFO] Hello, Alice! [timestamp=12:00]"
```text

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
def format_message(template: str, *args, prefix: str = "", **metadata) -> str:
    """
    Format a message with variable arguments and optional metadata.

    Args:
        template: A string with {} placeholders.
        *args: Values to substitute into the template.
        prefix: Optional prefix string (keyword-only).
        **metadata: Additional key=value pairs to append.

    Returns:
        The formatted message string.
    """
    body = template.format(*args)
    meta_str = " ".join(f"[{k}={v}]" for k, v in metadata.items())
    parts = [p for p in [prefix, body, meta_str] if p]
    return " ".join(parts)

print(format_message("Hello, {}!", "Alice"))
# Hello, Alice!

print(format_message("Hello, {}!", "Bob", prefix="[INFO]"))
# [INFO] Hello, Bob!

print(format_message("Error in {}: {}", "module", "not found", prefix="[ERROR]", code=404))
# [ERROR] Error in module: not found [code=404]
```text

</details>

---

## Exercise 3 — LEGB Scope

**Difficulty:** Medium | **Points:** 3

### Task

Predict, then verify, the output of each code snippet. Then fix the ones that have bugs.

### Requirements

For each snippet, write down what you think the output is BEFORE running it:

**Snippet A:**
```python
x = "global"
def outer():
    x = "outer"
    def inner():
        print(x)
    inner()
outer()
print(x)
```text

**Snippet B:**
```python
total = 0
def add(n):
    total += n   # what happens here?
    return total
add(5)
```text

**Snippet C:**
```python
x = 10
def modify():
    global x
    x = 20
modify()
print(x)
```text

**Snippet D:**
```python
def make_adder(n):
    def adder(x):
        return x + n
    return adder

add5 = make_adder(5)
add10 = make_adder(10)
print(add5(3))
print(add10(3))
print(add5(add10(1)))
```text

Fix Snippet B and explain why it fails.

### Solution

<details>
<summary>Click to reveal solution</summary>

**Snippet A:**
```text
outer  ← inner reads from enclosing scope (E in LEGB)
global ← outer's local x doesn't affect global x
```text

**Snippet B:** Raises `UnboundLocalError: local variable 'total' referenced before assignment`

Python sees `total += n` (which is `total = total + n`) and treats `total` as a local variable. But it's referenced before it's assigned locally.

**Fix:**
```python
total = 0
def add(n):
    global total   # option 1: use global
    total += n
    return total

# Better fix: don't use global state
def make_accumulator():
    total = 0
    def add(n):
        nonlocal total   # option 2: use nonlocal in closure
        total += n
        return total
    return add

accumulator = make_accumulator()
print(accumulator(5))   # 5
print(accumulator(3))   # 8
```text

**Snippet C:** Output is `20`. `global x` tells Python to use the module-level `x`.

**Snippet D:**
```text
8    (5 + 3)
13   (10 + 3)
16   (add5(add10(1)) = add5(11) = 11 + 5 = 16)
```text

</details>

---

## Exercise 4 — First-Class Functions

**Difficulty:** Medium | **Points:** 3

### Task

Implement a simple pipeline that applies transformations to data.

### Requirements

Write a function `pipeline(*functions)` that:
- Accepts any number of functions
- Returns a new function that applies them in sequence (left to right)
- Each function takes one argument and returns one value

Then use it to create a text processing pipeline.

```python
clean = pipeline(
    str.strip,
    str.lower,
    lambda s: s.replace("  ", " "),
)
print(clean("  Hello   World  "))   # "hello world"
```text

Also write a `transform_list(items, *functions)` that applies `pipeline(*functions)` to each item in a list.

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
from typing import Callable, TypeVar

T = TypeVar("T")

def pipeline(*functions: Callable) -> Callable:
    """
    Return a function that applies each function in sequence (left to right).

    Example:
        clean = pipeline(str.strip, str.lower)
        clean("  HELLO  ")  # "hello"
    """
    def apply(value):
        result = value
        for func in functions:
            result = func(result)
        return result
    return apply

def transform_list(items: list, *functions: Callable) -> list:
    """Apply a pipeline of functions to each item in a list."""
    transform = pipeline(*functions)
    return [transform(item) for item in items]

# Text cleaning pipeline
clean = pipeline(
    str.strip,
    str.lower,
    lambda s: " ".join(s.split()),  # normalize internal whitespace
)

print(clean("  Hello   World  "))   # "hello world"
print(clean("  PYTHON IS   GREAT  "))  # "python is great"

# Transform a list of names
names = ["  ALICE  ", "bob", "  Charlie  "]
cleaned_names = transform_list(names, str.strip, str.title)
print(cleaned_names)   # ['Alice', 'Bob', 'Charlie']
```text

</details>

---

## Exercise 5 — Mutable Default Argument

**Difficulty:** Medium | **Points:** 2

### Task

Demonstrate and fix the mutable default argument bug.

### Requirements

1. Write a function `add_item(item, collection=[])` that has the bug
2. Show the bug by calling it multiple times
3. Write the fixed version `add_item_fixed(item, collection=None)`
4. Write a test that would FAIL with the buggy version but PASS with the fixed version
5. Write a note explaining when you might INTENTIONALLY use a mutable default (hint: caching)

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
# BUGGY version
def add_item_buggy(item, collection=[]):
    """Add item to collection. BUG: default list is shared across calls."""
    collection.append(item)
    return collection

# Demonstrate the bug
list1 = add_item_buggy("a")
list2 = add_item_buggy("b")   # Expected ["b"], but...
print(list1)   # ["a", "b"] — list1 was also modified!
print(list2)   # ["a", "b"] — same list!
print(list1 is list2)   # True — they ARE the same object

# FIXED version
def add_item_fixed(item, collection=None):
    """Add item to collection. Fixed: creates new list if none provided."""
    if collection is None:
        collection = []
    collection.append(item)
    return collection

# Test that passes with fixed, fails with buggy
def test_independent_calls():
    result1 = add_item_fixed("a")
    result2 = add_item_fixed("b")
    assert result1 == ["a"], f"Expected ['a'], got {result1}"
    assert result2 == ["b"], f"Expected ['b'], got {result2}"
    assert result1 is not result2, "Should be different lists"
    print("Test passed!")

test_independent_calls()

# INTENTIONAL use of mutable default — a simple cache
def expensive_function(n, _cache={}):
    """
    Example of intentional mutable default for caching.
    The _cache dict persists between calls — this IS the intent.
    (In production, use functools.lru_cache instead)
    """
    if n not in _cache:
        print(f"Computing for {n}...")
        _cache[n] = n ** 2   # expensive computation
    return _cache[n]

print(expensive_function(5))   # Computing for 5... → 25
print(expensive_function(5))   # → 25 (from cache, no "Computing...")
print(expensive_function(3))   # Computing for 3... → 9
```text

</details>

---

## Exercise 6 — Closures

**Difficulty:** Hard | **Points:** 4

### Task

Use closures to implement stateful functions without classes.

### Requirements

1. `make_counter(start=0, step=1)` — returns a counter function with configurable start and step
2. `make_accumulator()` — returns an `add(n)` function that keeps a running total
3. `make_bounded_counter(min_val, max_val)` — counter that wraps around at the boundaries
4. `make_once(func)` — returns a wrapper that calls `func` only on the first call, then returns the cached result on subsequent calls

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
from typing import Callable

def make_counter(start: int = 0, step: int = 1) -> Callable[[], int]:
    """Return a counter function that increments by `step` each call."""
    count = start - step  # pre-subtract so first call returns start

    def counter() -> int:
        nonlocal count
        count += step
        return count

    return counter

def make_accumulator() -> Callable[[float], float]:
    """Return a function that adds numbers to a running total."""
    total = 0.0

    def add(n: float) -> float:
        nonlocal total
        total += n
        return total

    return add

def make_bounded_counter(min_val: int, max_val: int) -> Callable[[], int]:
    """Return a counter that wraps around between min_val and max_val."""
    current = min_val - 1

    def counter() -> int:
        nonlocal current
        current += 1
        if current > max_val:
            current = min_val
        return current

    return counter

def make_once(func: Callable) -> Callable:
    """Return a version of func that only runs once; subsequent calls return cached result."""
    cache = {}

    def wrapper(*args, **kwargs):
        if "result" not in cache:
            cache["result"] = func(*args, **kwargs)
        return cache["result"]

    return wrapper

# Tests
c = make_counter()
print([c() for _ in range(5)])   # [1, 2, 3, 4, 5]

c2 = make_counter(10, 5)
print([c2() for _ in range(4)])  # [10, 15, 20, 25]

acc = make_accumulator()
print(acc(10))   # 10.0
print(acc(5))    # 15.0
print(acc(-3))   # 12.0

bc = make_bounded_counter(1, 3)
print([bc() for _ in range(9)])  # [1, 2, 3, 1, 2, 3, 1, 2, 3]

call_count = 0
def expensive():
    global call_count
    call_count += 1
    return "result"

once_expensive = make_once(expensive)
print(once_expensive())   # "result"
print(once_expensive())   # "result"
print(once_expensive())   # "result"
print(f"Actually called {call_count} time(s)")  # Actually called 1 time(s)
```text

</details>

---

## Exercise 7 — Recursion

**Difficulty:** Hard | **Points:** 4

### Task

Implement three classic recursive algorithms.

### Requirements

1. `flatten(nested)` — flatten a list of arbitrarily nested lists into a flat list
2. `binary_search(sorted_list, target)` — recursive binary search, returns index or -1
3. `power_set(items)` — return all subsets of a list (2^n subsets)

For each, also implement an iterative version and compare.

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
from typing import Any

def flatten(nested: list) -> list:
    """Flatten a list of arbitrarily nested lists."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

def binary_search(sorted_list: list, target, low: int = 0, high: int = None) -> int:
    """
    Recursive binary search.
    Returns the index of target in sorted_list, or -1 if not found.
    """
    if high is None:
        high = len(sorted_list) - 1

    if low > high:
        return -1

    mid = (low + high) // 2
    if sorted_list[mid] == target:
        return mid
    elif sorted_list[mid] < target:
        return binary_search(sorted_list, target, mid + 1, high)
    else:
        return binary_search(sorted_list, target, low, mid - 1)

def power_set(items: list) -> list[list]:
    """Return all subsets of items (including empty set and full set)."""
    if not items:
        return [[]]  # Base case: only the empty set
    first = items[0]
    rest_subsets = power_set(items[1:])
    # Each subset either includes `first` or doesn't
    return rest_subsets + [[first] + subset for subset in rest_subsets]

# Tests
print(flatten([1, [2, [3, 4]], [5, 6]]))   # [1, 2, 3, 4, 5, 6]
print(flatten([1, [2, [3, [4, [5]]]]]))    # [1, 2, 3, 4, 5]

sorted_nums = [1, 3, 5, 7, 9, 11, 13]
print(binary_search(sorted_nums, 7))     # 3
print(binary_search(sorted_nums, 4))     # -1

subsets = power_set([1, 2, 3])
print(len(subsets))    # 8 (2^3)
print(sorted(subsets)) # [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
```text

</details>

---

## Exercise 8 — Decorators (Preview)

**Difficulty:** Hard | **Points:** 4

### Task

Implement two practical decorators.

### Requirements

1. `@retry(max_attempts=3, delay=0)` — retry a failing function up to `max_attempts` times
2. `@validate_types` — a decorator that checks type hints at runtime

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
import functools
import time
import inspect

def retry(max_attempts: int = 3, delay: float = 0.0, exceptions=(Exception,)):
    """
    Decorator that retries a function if it raises an exception.

    Args:
        max_attempts: Maximum number of attempts (default 3).
        delay: Seconds to wait between attempts (default 0).
        exceptions: Exception types to catch (default: all).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    print(f"Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts and delay > 0:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

# Test retry decorator
attempt_count = 0

@retry(max_attempts=3)
def flaky_function():
    global attempt_count
    attempt_count += 1
    if attempt_count < 3:
        raise ValueError(f"Temporary failure on attempt {attempt_count}")
    return "success!"

result = flaky_function()
print(f"Result: {result}")
# Attempt 1/3 failed: Temporary failure on attempt 1
# Attempt 2/3 failed: Temporary failure on attempt 2
# Result: success!

# Simple type validation decorator
def validate_types(func):
    """Check that arguments match type hints at runtime (simplified)."""
    hints = func.__annotations__
    param_names = list(inspect.signature(func).parameters.keys())

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check positional args
        for param_name, value in zip(param_names, args):
            if param_name in hints and param_name != "return":
                expected_type = hints[param_name]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Parameter '{param_name}' expected {expected_type.__name__}, "
                        f"got {type(value).__name__}"
                    )
        return func(*args, **kwargs)
    return wrapper

@validate_types
def add_numbers(a: int, b: int) -> int:
    return a + b

print(add_numbers(3, 4))    # 7
try:
    add_numbers(3, "4")     # TypeError!
except TypeError as e:
    print(f"Caught: {e}")
```text

</details>

---

## Exercise 9 — Functional Programming Patterns

**Difficulty:** Hard | **Points:** 3

### Task

Implement functional programming utilities that work like those in `functools` and `itertools`.

### Requirements

1. `my_map(func, iterable)` — your own implementation of `map` (returns a list)
2. `my_filter(predicate, iterable)` — your own `filter`
3. `my_reduce(func, iterable, initial=None)` — your own `reduce`
4. `curry(func)` — transform a multi-arg function into a chain of single-arg functions

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
from typing import Callable, TypeVar

T = TypeVar("T")
U = TypeVar("U")

def my_map(func: Callable, iterable) -> list:
    """Apply func to each item in iterable, return list of results."""
    return [func(item) for item in iterable]

def my_filter(predicate: Callable, iterable) -> list:
    """Return items from iterable where predicate(item) is True."""
    return [item for item in iterable if predicate(item)]

def my_reduce(func: Callable, iterable, initial=None):
    """
    Apply func cumulatively to items in iterable.
    If initial is provided, it's placed before items.
    """
    it = iter(iterable)
    if initial is None:
        try:
            acc = next(it)
        except StopIteration:
            raise TypeError("my_reduce() of empty sequence with no initial value")
    else:
        acc = initial

    for item in it:
        acc = func(acc, item)
    return acc

def curry(func: Callable) -> Callable:
    """
    Curry a multi-argument function.
    curry(add)(3)(5) == add(3, 5)
    """
    import inspect
    n_args = len(inspect.signature(func).parameters)

    def curried(*args):
        if len(args) >= n_args:
            return func(*args[:n_args])
        return lambda *more_args: curried(*(args + more_args))

    return curried

# Tests
print(my_map(lambda x: x**2, [1, 2, 3, 4]))   # [1, 4, 9, 16]
print(my_filter(lambda x: x % 2 == 0, range(10)))  # [0, 2, 4, 6, 8]
print(my_reduce(lambda a, b: a + b, [1, 2, 3, 4, 5]))  # 15
print(my_reduce(lambda a, b: a * b, [1, 2, 3, 4], initial=1))  # 24

@curry
def add(a, b):
    return a + b

add3 = add(3)
print(add3(5))   # 8
print(add(3)(5)) # 8
print(add(3, 5)) # 8
```text

</details>

---

## Exercise 10 — Design Challenge

**Difficulty:** Expert | **Points:** 3

### Task

Design a simple function registry system using closures and first-class functions.

### Requirements

Implement a `Registry` class (using closures — no class keyword!) that:
- Stores functions by name
- Supports `register(name)` decorator
- Supports `get(name)` to retrieve a function
- Supports `list_all()` to see registered names
- Supports `run(name, *args, **kwargs)` to call a registered function

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
def make_registry():
    """Create a function registry using closures."""
    _registry = {}

    def register(name: str):
        """Decorator to register a function under the given name."""
        def decorator(func):
            _registry[name] = func
            return func
        return decorator

    def get(name: str):
        """Retrieve a registered function by name."""
        if name not in _registry:
            raise KeyError(f"No function registered as {name!r}")
        return _registry[name]

    def list_all() -> list[str]:
        """Return a sorted list of all registered function names."""
        return sorted(_registry.keys())

    def run(name: str, *args, **kwargs):
        """Call a registered function with the given arguments."""
        return get(name)(*args, **kwargs)

    # Return a dict of the API functions (could also use a dataclass)
    return {
        "register": register,
        "get": get,
        "list_all": list_all,
        "run": run,
    }

# Create a registry
commands = make_registry()

@commands["register"]("greet")
def greet(name: str) -> str:
    return f"Hello, {name}!"

@commands["register"]("shout")
def shout(message: str) -> str:
    return message.upper() + "!!!"

@commands["register"]("double")
def double(n: int) -> int:
    return n * 2

# Use it
print(commands["list_all"]())        # ['double', 'greet', 'shout']
print(commands["run"]("greet", "Alice"))     # Hello, Alice!
print(commands["run"]("shout", "python"))    # PYTHON!!!
print(commands["run"]("double", 21))         # 42

func = commands["get"]("greet")
print(func("Bob"))   # Hello, Bob!
```text

</details>

---

*Record your score and completion date in [../README.md](../README.md)*
