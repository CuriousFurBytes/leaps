# Module 1: Variables and Types — Exercises

[← Module Home](./README.md) | [Topic Home](../README.md)

8 exercises covering all aspects of Python variables and built-in types. Complete them in order.

**Scoring:** 8 exercises × varying pts = 20 pts possible  
**Passing:** 16 / 20 (80%)

---

## Exercise 1 — Type Explorer

**Difficulty:** Easy | **Points:** 2 | **Estimated Time:** 20 min

### Task

Create a script that demonstrates all of Python's primitive types by assigning a variable of each type, printing the value, and printing the type.

### Requirements

1. Create variables of each type: `int`, `float`, `str`, `bool`, `None`, `bytes`
2. For each, use `print(f"{variable!r} is of type {type(variable).__name__}")`
3. Demonstrate at least one operation on each type (e.g., arithmetic on int, method on str)
4. Use the REPL to also try `isinstance(True, int)` and explain the result in a comment

### Expected Output

```text
42 is of type int
3.14 is of type float
'hello' is of type str
True is of type bool
None is of type NoneType
b'data' is of type bytes
```text

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
# type_explorer.py

# int
age = 42
print(f"{age!r} is of type {type(age).__name__}")   # 42 is of type int
print(f"  doubled: {age * 2}")

# float
pi = 3.14159
print(f"{pi!r} is of type {type(pi).__name__}")
print(f"  rounded: {round(pi, 2)}")

# str
name = "Python"
print(f"{name!r} is of type {type(name).__name__}")
print(f"  upper: {name.upper()}")

# bool
is_great = True
print(f"{is_great!r} is of type {type(is_great).__name__}")
print(f"  not is_great: {not is_great}")

# None
nothing = None
print(f"{nothing!r} is of type {type(nothing).__name__}")

# bytes
data = b"hello"
print(f"{data!r} is of type {type(data).__name__}")
print(f"  decoded: {data.decode('utf-8')}")

# Interesting: bool is a subclass of int
print(f"\nisinstance(True, int) = {isinstance(True, int)}")  # True
print(f"True + True = {True + True}")   # 2 — because True == 1
```text

</details>

---

## Exercise 2 — String Manipulation

**Difficulty:** Easy | **Points:** 2 | **Estimated Time:** 25 min

### Task

Practice the most important string operations.

### Requirements

Given the string `text = "  The Quick Brown Fox Jumps Over The Lazy Dog  "`, write code that:

1. Strips whitespace from both ends
2. Converts to lowercase
3. Splits into individual words
4. Counts the number of words
5. Joins the words back together with a single space
6. Checks if it contains the word "fox" (case-insensitive)
7. Replaces "Dog" with "Cat" (on the original, stripped string)
8. Extracts the first 3 and last 3 characters of the stripped string
9. Formats it in an f-string: `"The sentence has {n} words and {m} characters."`

### Expected Output

```text
Stripped: 'The Quick Brown Fox Jumps Over The Lazy Dog'
Lowercase: 'the quick brown fox jumps over the lazy dog'
Words: ['The', 'Quick', 'Brown', 'Fox', 'Jumps', 'Over', 'The', 'Lazy', 'Dog']
Word count: 9
Rejoined: 'The Quick Brown Fox Jumps Over The Lazy Dog'
Contains 'fox': True
Replaced: 'The Quick Brown Fox Jumps Over The Lazy Cat'
First 3 chars: 'The'
Last 3 chars: 'Dog'
The sentence has 9 words and 43 characters.
```text

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
text = "  The Quick Brown Fox Jumps Over The Lazy Dog  "

stripped = text.strip()
lowercase = stripped.lower()
words = stripped.split()
word_count = len(words)
rejoined = " ".join(words)
contains_fox = "fox" in stripped.lower()
replaced = stripped.replace("Dog", "Cat")
first_3 = stripped[:3]
last_3 = stripped[-3:]
char_count = len(stripped)

print(f"Stripped: {stripped!r}")
print(f"Lowercase: {lowercase!r}")
print(f"Words: {words}")
print(f"Word count: {word_count}")
print(f"Rejoined: {rejoined!r}")
print(f"Contains 'fox': {contains_fox}")
print(f"Replaced: {replaced!r}")
print(f"First 3 chars: {first_3!r}")
print(f"Last 3 chars: {last_3!r}")
print(f"The sentence has {word_count} words and {char_count} characters.")
```text

</details>

---

## Exercise 3 — Floating Point Exploration

**Difficulty:** Medium | **Points:** 2 | **Estimated Time:** 30 min

### Task

Investigate Python's floating-point behavior and learn to work around precision issues.

### Requirements

1. Demonstrate the `0.1 + 0.2` precision problem
2. Use `math.isclose()` to compare floats correctly
3. Use the `decimal` module to do `0.1 + 0.2` exactly
4. Use the `fractions` module to represent `1/3` exactly
5. Write a function `are_equal(a, b, tolerance=1e-9)` that compares floats with a tolerance
6. Show what `float('inf')`, `float('-inf')`, and `float('nan')` are and how they behave

### Expected Output

```text
0.1 + 0.2 = 0.30000000000000004
0.1 + 0.2 == 0.3: False
math.isclose(0.1 + 0.2, 0.3): True
Decimal: 0.1 + 0.2 = 0.3 (exact: True)
1/3 as Fraction: 1/3
are_equal(0.1+0.2, 0.3): True
inf + 1 = inf
-inf < any_number: True
nan == nan: False (NaN is never equal to anything, including itself!)
```text

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
import math
from decimal import Decimal
from fractions import Fraction

# The floating-point problem
result = 0.1 + 0.2
print(f"0.1 + 0.2 = {result}")
print(f"0.1 + 0.2 == 0.3: {result == 0.3}")
print(f"math.isclose(0.1 + 0.2, 0.3): {math.isclose(result, 0.3)}")

# Exact arithmetic with Decimal
d_result = Decimal("0.1") + Decimal("0.2")
print(f"Decimal: 0.1 + 0.2 = {d_result} (exact: {d_result == Decimal('0.3')})")

# Exact fractions
one_third = Fraction(1, 3)
print(f"1/3 as Fraction: {one_third}")
print(f"1/3 + 1/3 + 1/3 = {one_third + one_third + one_third}")  # 1

# Custom comparison function
def are_equal(a: float, b: float, tolerance: float = 1e-9) -> bool:
    """Compare two floats with a tolerance."""
    return abs(a - b) <= tolerance

print(f"are_equal(0.1+0.2, 0.3): {are_equal(0.1 + 0.2, 0.3)}")

# Special float values
inf = float("inf")
neg_inf = float("-inf")
nan = float("nan")

print(f"inf + 1 = {inf + 1}")
print(f"-inf < any_number: {neg_inf < -1e308}")
print(f"nan == nan: {nan == nan}")  # False!
print(f"math.isnan(nan): {math.isnan(nan)}")  # True — correct way to check
```text

</details>

---

## Exercise 4 — Type Conversion Chain

**Difficulty:** Medium | **Points:** 2 | **Estimated Time:** 25 min

### Task

Practice converting between types and understand where conversions can fail.

### Requirements

1. Convert each of the following to all other types (where meaningful): `42`, `"3.14"`, `True`, `"0"`, `""`, `0`
2. Document which conversions fail and why
3. Write a function `safe_int(value)` that converts a value to int, returning `None` if conversion is impossible
4. Write a function `to_bool_explicit(value)` that explicitly defines truthiness with clear rules

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
# Type conversion exploration
conversions = [42, "3.14", True, "0", "", 0, None]

for val in conversions:
    int_val = "N/A"
    float_val = "N/A"
    str_val = str(val)
    bool_val = bool(val)

    try:
        int_val = int(val) if val is not None else "N/A"
    except (ValueError, TypeError) as e:
        int_val = f"Error: {e}"

    try:
        float_val = float(val) if val is not None else "N/A"
    except (ValueError, TypeError) as e:
        float_val = f"Error: {e}"

    print(f"{val!r:10} → int: {int_val!r:20} float: {float_val!r:20} str: {str_val!r:10} bool: {bool_val}")

def safe_int(value) -> int | None:
    """Convert value to int, return None if not possible."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

print(f"\nsafe_int('42') = {safe_int('42')}")
print(f"safe_int('abc') = {safe_int('abc')}")
print(f"safe_int(3.9) = {safe_int(3.9)}")   # 3, not 4 — truncates

def to_bool_explicit(value) -> bool:
    """Explicit truthiness rules."""
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() not in ("", "false", "no", "0", "off")
    return bool(value)

print(f"\nto_bool_explicit('false') = {to_bool_explicit('false')}")
print(f"to_bool_explicit('yes') = {to_bool_explicit('yes')}")
print(f"to_bool_explicit('  ') = {to_bool_explicit('  ')}")
```text

</details>

---

## Exercise 5 — Type-Dependent Behavior

**Difficulty:** Medium | **Points:** 3 | **Estimated Time:** 30 min

### Task

Write a function that behaves differently based on the type of its input.

### Requirements

Write a function `describe(value)` that:
- If `value` is an `int`: returns `f"The integer {value} is {'even' if value % 2 == 0 else 'odd'} and {'positive' if value > 0 else 'negative' if value < 0 else 'zero'}"`
- If `value` is a `float`: returns `f"The float {value:.4f} rounded to nearest int is {round(value)}"`
- If `value` is a `str`: returns `f"The string '{value}' has {len(value)} characters and {'is' if value == value[::-1] else 'is not'} a palindrome"`
- If `value` is a `bool`: returns `f"The boolean {value} means {'yes/true/on' if value else 'no/false/off'}"`
- If `value` is `None`: returns `"No value provided"`
- Otherwise: returns `f"Unknown type: {type(value).__name__}"`

Test with: `42`, `-7`, `3.14159`, `"racecar"`, `"python"`, `True`, `None`, `[1,2,3]`

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
def describe(value) -> str:
    if isinstance(value, bool):  # bool before int — bool is a subclass of int!
        return f"The boolean {value} means {'yes/true/on' if value else 'no/false/off'}"
    elif isinstance(value, int):
        parity = "even" if value % 2 == 0 else "odd"
        sign = "positive" if value > 0 else "negative" if value < 0 else "zero"
        return f"The integer {value} is {parity} and {sign}"
    elif isinstance(value, float):
        return f"The float {value:.4f} rounded to nearest int is {round(value)}"
    elif isinstance(value, str):
        is_palindrome = value.lower() == value.lower()[::-1]
        palindrome_word = "is" if is_palindrome else "is not"
        return f"The string '{value}' has {len(value)} characters and {palindrome_word} a palindrome"
    elif value is None:
        return "No value provided"
    else:
        return f"Unknown type: {type(value).__name__}"

# Test
for test_val in [42, -7, 3.14159, "racecar", "python", True, None, [1, 2, 3]]:
    print(describe(test_val))
```text

Note: `bool` must be checked before `int` because `isinstance(True, int)` is `True` — `bool` is a subclass of `int`.

</details>

---

## Exercise 6 — Manual Type Checker

**Difficulty:** Hard | **Points:** 3 | **Estimated Time:** 45 min

### Task

Implement a simple type checker WITHOUT using `isinstance()`. This exercise helps you understand what type checking actually does.

### Requirements

Write a function `check_type(value, expected_type_name: str) -> bool` that returns `True` if `value` matches the expected type, where `expected_type_name` is a string like `"int"`, `"str"`, `"float"`, `"bool"`, `"list"`, `"dict"`, `"none"`.

Implement it using `type()` and string comparison — do NOT use `isinstance()`.

Handle edge case: `True` and `False` should pass `"bool"` but NOT `"int"` (even though `isinstance(True, int)` is `True`).

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
def check_type(value, expected_type_name: str) -> bool:
    """
    Check if value is of the given type name.
    Uses exact type matching (type()), not isinstance().
    """
    type_map = {
        "int": int,
        "float": float,
        "str": str,
        "bool": bool,
        "list": list,
        "dict": dict,
        "tuple": tuple,
        "set": set,
        "none": type(None),
        "bytes": bytes,
    }

    expected = type_map.get(expected_type_name.lower())
    if expected is None:
        raise ValueError(f"Unknown type name: {expected_type_name!r}")

    # Exact type match — type() returns the class, not the hierarchy
    return type(value) is expected

# Tests
assert check_type(42, "int") == True
assert check_type(True, "bool") == True
assert check_type(True, "int") == False   # exact match — bool is NOT int with type()
assert check_type(3.14, "float") == True
assert check_type("hello", "str") == True
assert check_type(None, "none") == True
assert check_type([], "list") == True
assert check_type({}, "dict") == True

print("All assertions passed!")

# Demonstrate the difference from isinstance():
print(f"check_type(True, 'int') = {check_type(True, 'int')}")      # False
print(f"isinstance(True, int) = {isinstance(True, int)}")           # True
```text

</details>

---

## Exercise 7 — Python Integer Internals

**Difficulty:** Hard | **Points:** 3 | **Estimated Time:** 40 min

### Task

Explore CPython's small integer caching optimization using `id()`.

### Context

CPython caches small integers (typically -5 to 256) as a performance optimization. Rather than creating a new object for `42` every time, it reuses the same object. This means two variables assigned to `42` will have the same `id()`.

### Requirements

1. Use `id()` to verify that small integers (-5 to 256) are cached (same id for same value)
2. Verify that large integers are NOT cached (different ids for same value)
3. Explain what this means for using `is` vs `==` for integer comparison
4. Document the actual caching range by finding the boundary values

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
# Python's small integer cache (CPython-specific)

# Small integers are cached
a = 100
b = 100
print(f"a = 100, b = 100")
print(f"id(a) = {id(a)}")
print(f"id(b) = {id(b)}")
print(f"a is b: {a is b}")   # True — same object!
print(f"a == b: {a == b}")   # True

# Large integers are NOT cached
x = 1000
y = 1000
print(f"\nx = 1000, y = 1000")
print(f"id(x) = {id(x)}")
print(f"id(y) = {id(y)}")
print(f"x is y: {x is y}")  # False (usually) — different objects
print(f"x == y: {x == y}")  # True — same value

# Find the boundary
print("\nFinding the caching boundary...")
for n in [256, 257, -5, -6]:
    a = n
    b = n
    print(f"n={n}: a is b = {a is b}")

# KEY LESSON: NEVER use `is` to compare integers (or any value)
# `is` tests identity (same object in memory)
# `==` tests equality (same value)
# The fact that small ints are cached is an implementation detail
# that could change — always use `==` for value comparison

print("\nConclusion: Always use == for value comparison, never `is`")
print("The only correct uses of `is`: checking for None, True, False")
```text

</details>

---

## Exercise 8 — String Interning (Expert Bonus)

**Difficulty:** Expert | **Points:** 3 bonus | **Estimated Time:** 45 min

### Task

Explore Python's string interning behavior — where identical strings share the same object — and understand when you can and cannot rely on it.

### Requirements

1. Demonstrate string interning for identifiers (simple strings that look like variable names)
2. Show that dynamically-constructed strings are NOT automatically interned
3. Use `sys.intern()` to force interning and measure performance with `timeit`
4. Write a comment explaining when string interning matters in practice

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
import sys
import timeit

# Identifier-like strings are usually interned automatically
a = "hello"
b = "hello"
print(f"'hello' is 'hello': {a is b}")  # Usually True (interned)

# Strings with spaces are usually NOT interned
a = "hello world"
b = "hello world"
print(f"'hello world' is 'hello world': {a is b}")  # Depends on Python version/context

# Dynamically constructed strings are not interned
prefix = "hel"
suffix = "lo"
dynamic = prefix + suffix
literal = "hello"
print(f"dynamic == literal: {dynamic == literal}")   # True
print(f"dynamic is literal: {dynamic is literal}")   # False (usually)

# Force interning with sys.intern()
interned_dynamic = sys.intern(prefix + suffix)
print(f"sys.intern(dynamic) is literal: {interned_dynamic is literal}")  # True

# Performance: interned string comparison can use `is` (identity check = pointer comparison)
# instead of `==` (must compare each character for non-interned strings)
# This matters when comparing the same strings millions of times (e.g., in parsers/compilers)

def compare_is(a, b):
    return a is b

def compare_eq(a, b):
    return a == b

word = sys.intern("a_very_long_identifier_string_for_testing")
same_word = sys.intern("a_very_long_identifier_string_for_testing")

n = 1_000_000
is_time = timeit.timeit(lambda: compare_is(word, same_word), number=n)
eq_time = timeit.timeit(lambda: compare_eq(word, same_word), number=n)

print(f"\nFor interned strings ({n} comparisons):")
print(f"  `is` comparison: {is_time:.3f}s")
print(f"  `==` comparison: {eq_time:.3f}s")
print(f"  Speedup: {eq_time/is_time:.1f}x")

# PRACTICAL NOTE: In normal Python code, this doesn't matter.
# String interning is only relevant for performance-critical code
# that compares huge numbers of strings (parsers, symbol tables, etc.)
# Never use `is` for string comparison in production code — use `==`.
```text

</details>

---

*Record your score and completion date in [../README.md](../README.md)*
