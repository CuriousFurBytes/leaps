# Module 1: Variables and Types

[← Introduction](../0.%20Introduction/) | [Topic Home](../README.md) | [Next → Functions](../2.%20Functions/)

![Status](https://img.shields.io/badge/status-Not%20Started-lightgrey)
![Module](https://img.shields.io/badge/module-1%20of%209-blue)
![Time](https://img.shields.io/badge/time-4--5%20hours-green)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner-brightgreen)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Core Concepts](#core-concepts)
  - [Variable Assignment and Naming Rules](#variable-assignment-and-naming-rules)
  - [Dynamic Typing](#dynamic-typing)
  - [int — Integers](#int--integers)
  - [float — Floating Point Numbers](#float--floating-point-numbers)
  - [str — Strings](#str--strings)
  - [bool — Booleans](#bool--booleans)
  - [None — The Null Value](#none--the-null-value)
  - [bytes — Binary Data](#bytes--binary-data)
  - [type() and isinstance()](#type-and-isinstance)
- [Common Beginner Mistakes](#common-beginner-mistakes)
- [Practical Examples](#practical-examples)
- [Mental Models](#mental-models)
- [Module Resources](#module-resources)

---

## Overview

Variables are the fundamental mechanism for storing and naming data in any programming language. In Python, variable assignment is simple — `x = 42` — but the type system beneath it is rich and worth understanding deeply.

Python uses **dynamic typing**: a variable's type is determined at runtime based on the value it holds, not by a declaration. This makes Python fast to write but requires you to think carefully about what types your variables contain at any given moment.

This module covers all of Python's **primitive built-in types** and the operations on each. Master these and you have the foundation for everything else in Python.

---

## Learning Goals

By the end of this module, you will be able to:

1. Assign variables using correct Python naming conventions
2. Explain what dynamic typing means and how it differs from static typing
3. Use `int`, `float`, `str`, `bool`, `None`, and `bytes` correctly
4. Perform arithmetic with integers including `//` (floor division) and `%` (modulo)
5. Explain the floating-point precision issue and use the `decimal` module when precision matters
6. Create and manipulate strings using slicing, methods, and f-strings
7. Understand boolean truthiness and short-circuit evaluation
8. Use `type()` to inspect types and `isinstance()` for type checking
9. Convert between types using `int()`, `float()`, `str()`, `bool()`
10. Identify and avoid the `== None` vs `is None` pitfall

---

## Prerequisites

- **Required:** Module 0 — Introduction (you can run Python scripts and use the REPL)
- No prior programming experience with types is required, but helps

---

## Core Concepts

### Variable Assignment and Naming Rules

In Python, variables are created the moment you assign a value. No declaration needed.

```python
# Assignment
x = 42
name = "Alice"
is_active = True
temperature = 98.6

# Multiple assignment
a = b = c = 0       # a, b, and c all equal 0

# Tuple unpacking
x, y = 10, 20       # x = 10, y = 20
a, b = b, a         # swap — a Pythonic idiom

# Augmented assignment
count = 0
count += 1           # count = count + 1
count -= 1
count *= 2
count //= 2          # integer division and assign
```

**Naming rules (required by Python):**
- Must start with a letter or underscore: `x`, `_private`, `my_var` ✓
- Can contain letters, numbers, underscores: `user_1`, `MAX_SIZE` ✓
- Case-sensitive: `name` and `Name` are different variables
- Cannot be a keyword: `for`, `if`, `class`, `return`, etc. are reserved

**Naming conventions (PEP 8 — strongly recommended):**

```python
# Variables and functions: snake_case
user_name = "alice"
total_price = 99.99

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
PI = 3.14159

# Classes: PascalCase
class UserAccount:
    pass

# "Private" (convention, not enforced): single underscore prefix
_internal_counter = 0

# Name mangling (class internals): double underscore prefix
__private = "not easily accessed from outside"
```

> [!TIP]
> Variable names should be descriptive. `user_age` is better than `a`. Single-letter names are only acceptable as loop counters (`i`, `j`) or mathematical variables where the context makes meaning clear.

---

### Dynamic Typing

Python is **dynamically typed**: variable types are checked at runtime, not at compile time. A variable can hold any type at any time — even different types at different points in the program.

```python
# x starts as an int
x = 42
print(type(x))   # <class 'int'>

# Same variable now holds a string
x = "hello"
print(type(x))   # <class 'str'>

# And now a list
x = [1, 2, 3]
print(type(x))   # <class 'list'>
```

**Contrast with static typing (Java/C++):**

```java
// Java — type is declared and fixed
int x = 42;
x = "hello";   // compile error!
```

**Dynamic typing tradeoffs:**

| Advantage | Disadvantage |
|-----------|-------------|
| Faster to write — no type annotations required | Type errors occur at runtime, not compile time |
| Flexible — functions work on many types | Harder to reason about large codebases |
| Less boilerplate | Slower (type checks at runtime) |

**Type hints (Python 3.5+):** Python supports optional type annotations that don't enforce types at runtime but enable static analysis tools (mypy, Pylance) to catch type errors before running:

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

age: int = 25
```

---

### int — Integers

Python integers are arbitrary-precision: they can be any size without overflow.

```python
# Integer literals
x = 42
x = -17
x = 1_000_000       # underscores for readability (PEP 515)
x = 0xFF            # hexadecimal = 255
x = 0b1010          # binary = 10
x = 0o17            # octal = 15

# Arithmetic operators
print(10 + 3)     # 13   addition
print(10 - 3)     # 7    subtraction
print(10 * 3)     # 30   multiplication
print(10 / 3)     # 3.3333... true division — ALWAYS returns float
print(10 // 3)    # 3    floor division — rounds DOWN (toward negative infinity)
print(10 % 3)     # 1    modulo — remainder after floor division
print(10 ** 3)    # 1000 exponentiation
print(-10 // 3)   # -4   (floor of -3.33... is -4, not -3!)

# Conversion
int("42")         # 42 — parse string as int
int(3.9)          # 3  — truncate (does NOT round)
int("0xFF", 16)   # 255 — parse hex string
int("1010", 2)    # 10  — parse binary string

# Built-in int functions
abs(-5)           # 5   absolute value
pow(2, 10)        # 1024 — same as 2**10 but can take modulus: pow(2,10,100) = 24
divmod(17, 5)     # (3, 2) — returns (quotient, remainder) as tuple
```

> [!NOTE]
> `//` is floor division, not truncation. `-7 // 2` is `-4` (floor of -3.5), not `-3`. For truncating toward zero, use `int(-7 / 2)` which gives `-3`.

---

### float — Floating Point Numbers

Floats represent real numbers (with a decimal point). They use IEEE 754 double-precision (64-bit) format.

```python
# Float literals
x = 3.14
x = -0.001
x = 1.5e6       # scientific notation = 1,500,000.0
x = 2.5e-3      # = 0.0025

# Arithmetic
print(0.1 + 0.2)    # 0.30000000000000004  (!!!)
print(0.1 + 0.2 == 0.3)  # False (!!!)
```

**The floating-point precision problem:**

This is one of the most important things to understand about computer arithmetic. `0.1` cannot be represented exactly in binary floating-point — the closest representable value is approximately `0.10000000000000000555...`. When you add `0.1 + 0.2`, tiny errors accumulate.

```python
# Never do this for financial calculations:
price = 0.10
tax = 0.30
total = price + tax   # 0.4 — seems fine
# But:
if total == 0.4:      # might be False due to float imprecision!
    pass

# Compare with tolerance instead:
import math
math.isclose(0.1 + 0.2, 0.3)   # True

# Or use decimal for exact arithmetic:
from decimal import Decimal
total = Decimal("0.10") + Decimal("0.30")
print(total)          # 0.40 (exact)
print(total == Decimal("0.40"))  # True

# Or use fractions:
from fractions import Fraction
total = Fraction(1, 10) + Fraction(3, 10)
print(total)          # 2/5
```

```python
# float built-ins
round(3.14159, 2)    # 3.14
abs(-2.5)            # 2.5
float("3.14")        # 3.14 — parse string as float
float("inf")         # math.inf — positive infinity
float("nan")         # math.nan — Not a Number

import math
math.floor(3.7)      # 3 — round down
math.ceil(3.2)       # 4 — round up
math.sqrt(16)        # 4.0 — square root
math.isfinite(x)     # True if not inf or nan
math.isnan(x)        # True if nan
```

---

### str — Strings

Strings are **immutable** sequences of Unicode characters. Once created, a string cannot be modified — operations on strings return new strings.

```python
# String literals — four equivalent ways:
s = "hello"
s = 'hello'
s = """hello"""         # triple-quote — can span multiple lines
s = '''hello'''

# Multiline strings
message = """This is a
multiline string.
Newlines are preserved."""

# Raw strings (no escape processing)
path = r"C:\Users\Alice\Documents"  # backslash is literal

# Byte strings (not str — see bytes section)
data = b"binary data"

# String operations
greeting = "Hello, World!"
print(len(greeting))          # 13 — number of characters
print(greeting[0])            # 'H' — indexing (0-based)
print(greeting[-1])           # '!' — negative index (from end)
print(greeting[0:5])          # 'Hello' — slicing [start:stop]
print(greeting[7:])           # 'World!' — slice to end
print(greeting[:5])           # 'Hello' — slice from start
print(greeting[::2])          # 'Hlo ol!' — every second character
print(greeting[::-1])         # '!dlroW ,olleH' — reverse

# String methods (return NEW strings — strings are immutable)
print("hello".upper())                # 'HELLO'
print("HELLO".lower())                # 'hello'
print("hello world".title())          # 'Hello World'
print("  hello  ".strip())            # 'hello'
print("hello world".replace("world", "Python"))  # 'hello Python'
print("a,b,c".split(","))             # ['a', 'b', 'c']
print(",".join(["a", "b", "c"]))      # 'a,b,c'
print("hello".startswith("he"))       # True
print("hello".endswith("lo"))         # True
print("hello world".find("world"))    # 6 (index) or -1 if not found
print("hello".center(11, "-"))        # '---hello---'
print("42".zfill(5))                  # '00042'

# f-strings (Python 3.6+) — the preferred way to format strings
name = "Alice"
age = 30
score = 9.5
print(f"Name: {name}")               # Name: Alice
print(f"Age in 5 years: {age + 5}") # Age in 5 years: 35
print(f"Score: {score:.1f}%")        # Score: 9.5%
print(f"{name!r}")                    # 'Alice' (repr)
print(f"{name!s}")                    # Alice (str, default)
print(f"{1000000:,}")                 # 1,000,000 (number formatting)
print(f"{0.75:.0%}")                  # 75% (percentage)
print(f"{name=}")                     # name='Alice' (debug format, 3.8+)

# Escape sequences in strings
print("line 1\nline 2")    # newline
print("col1\tcol2")        # tab
print("say \"hello\"")     # quote inside string
print("C:\\Users\\Alice")  # literal backslash
```

---

### bool — Booleans

`bool` is a subclass of `int` in Python. `True == 1` and `False == 0`.

```python
# Boolean values
t = True
f = False

# Boolean operators
print(True and False)    # False — both must be True
print(True or False)     # True  — at least one must be True
print(not True)          # False

# Comparison operators — return bool
print(5 > 3)       # True
print(5 < 3)       # False
print(5 == 5)      # True  (equality)
print(5 != 3)      # True  (not equal)
print(5 >= 5)      # True
print(5 <= 4)      # False

# Chained comparisons (Pythonic)
x = 5
print(1 < x < 10)     # True — equivalent to: 1 < x and x < 10
print(0 <= x <= 100)  # True

# Truthiness — every object has a truth value
# Falsy values: False, 0, 0.0, "", [], {}, set(), None, custom __bool__ returning False
# Everything else is truthy

bool(0)       # False
bool(0.0)     # False
bool("")      # False
bool([])      # False
bool({})      # False
bool(None)    # False

bool(1)       # True
bool(0.1)     # True
bool("x")     # True
bool([0])     # True (list with one element, even if element is 0)

# Short-circuit evaluation
# `and` returns the first falsy value, or the last value if all are truthy
print(0 and "hello")   # 0 (short-circuit: 0 is falsy, return it)
print(1 and "hello")   # "hello" (1 is truthy, evaluate "hello")
print("" and 42)       # "" (falsy, short-circuit)

# `or` returns the first truthy value, or the last value if all are falsy
print(0 or "default")  # "default" (0 is falsy, try next)
print("name" or "default")  # "name" (truthy, return it)

# Practical use: default values
name = user_input or "Anonymous"
result = expensive_cache.get(key) or expensive_compute(key)
```

---

### None — The Null Value

`None` is Python's null value — it represents the absence of a value. It's the only instance of `NoneType`.

```python
# None is used to represent "no value"
result = None
config = None

# Functions without a return statement implicitly return None
def do_nothing():
    pass

print(do_nothing())   # None

# The correct way to check for None: use `is`, not `==`
x = None
if x is None:         # CORRECT — identity check
    print("x is None")

if x is not None:     # CORRECT
    print("x has a value")

# Why not `==`?
if x == None:   # Works but wrong style — PEP 8 recommends `is`
    pass
# The problem: a custom object could override __eq__ to return True when compared to None
# `is` tests object identity (same object in memory) — reliable and clear
```

> [!WARNING]
> Always use `is None` and `is not None` to check for None. Using `== None` or `!= None` is a PEP 8 violation and can fail with objects that override `__eq__`.

---

### bytes — Binary Data

`bytes` objects represent immutable sequences of integers in the range 0-255. Used for binary data, encoding/decoding.

```python
# bytes literals
b = b"hello"              # byte string literal
b = bytes([72, 101, 108]) # from list of ints

# Encoding str to bytes
text = "hello"
encoded = text.encode("utf-8")    # b'hello'
encoded = text.encode("ascii")    # b'hello'
encoded = "café".encode("utf-8")  # b'caf\xc3\xa9'

# Decoding bytes to str
decoded = b"hello".decode("utf-8")  # "hello"

# bytes operations (similar to str)
b = b"hello world"
print(b[0])          # 104 (integer, not character)
print(b[0:5])        # b'hello'
print(len(b))        # 11
```

---

### type() and isinstance()

```python
# type() returns the exact type of an object
print(type(42))        # <class 'int'>
print(type(3.14))      # <class 'float'>
print(type("hello"))   # <class 'str'>
print(type(True))      # <class 'bool'>
print(type(None))      # <class 'NoneType'>

# Exact type comparison (rarely what you want in production)
type(42) == int        # True
type(42) == float      # False

# isinstance() — preferred for type checking
# Also checks subclasses
isinstance(42, int)        # True
isinstance(True, int)      # True — bool is a subclass of int!
isinstance(42, (int, float))   # True — check multiple types with a tuple

# Why isinstance() is better:
class MyInt(int):
    pass

x = MyInt(5)
type(x) == int       # False — exact match only
isinstance(x, int)   # True  — checks inheritance chain

# Type conversion
int("42")       # 42
float("3.14")   # 3.14
str(42)         # "42"
bool(0)         # False
list("abc")     # ['a', 'b', 'c']
```

---

## Common Beginner Mistakes

> [!WARNING]
> **Using `== None` instead of `is None`**
> `== None` checks equality, which can be overridden by custom classes. `is None` checks identity — whether the object IS the None singleton. Always use `is None`.
> ```python
> # Wrong:
> if x == None: ...
> # Right:
> if x is None: ...
> ```

> [!WARNING]
> **Mutable default arguments (preview — full coverage in Module 2)**
> Default values in function signatures are evaluated ONCE, not per call. If the default is a mutable object (list, dict), it's shared across all calls. This is a famous Python gotcha — covered fully in Module 2.

> [!WARNING]
> **Forgetting that `//` floors toward negative infinity**
> `7 // 2 = 3` but `-7 // 2 = -4` (not -3). Floor always rounds toward negative infinity, not toward zero. If you need truncation toward zero, use `int(a / b)`.

> [!WARNING]
> **Comparing floats with `==`**
> `0.1 + 0.2 == 0.3` is `False` in Python (and most languages). Use `math.isclose()` for float comparison or the `decimal` module for exact decimal arithmetic.

> [!WARNING]
> **Strings are immutable — methods return new strings**
> ```python
> name = "alice"
> name.upper()          # Does nothing useful — result is discarded!
> name = name.upper()   # Correct — reassign the result
> ```

---

## Practical Examples

### Example 1: Temperature Converter

```python
# Convert between Celsius and Fahrenheit

def celsius_to_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32

def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5 / 9

# Test it
boiling_c = 100.0
boiling_f = celsius_to_fahrenheit(boiling_c)
print(f"{boiling_c}°C = {boiling_f}°F")    # 100.0°C = 212.0°F

freezing_f = 32.0
freezing_c = fahrenheit_to_celsius(freezing_f)
print(f"{freezing_f}°F = {freezing_c}°C")  # 32.0°F = 0.0°C
```

### Example 2: Type-Aware Calculator

```python
def safe_divide(a, b):
    """Divide a by b, returning None if division is impossible."""
    if not isinstance(a, (int, float)):
        print(f"Error: a must be a number, got {type(a).__name__}")
        return None
    if not isinstance(b, (int, float)):
        print(f"Error: b must be a number, got {type(b).__name__}")
        return None
    if b == 0:
        print("Error: division by zero")
        return None
    return a / b

print(safe_divide(10, 3))     # 3.333...
print(safe_divide(10, 0))     # Error: division by zero / None
print(safe_divide("10", 3))   # Error: a must be a number / None
```

### Example 3: String Processing

```python
# Clean and parse a messy user input
raw = "  Alice Smith , 42 , New York  "
parts = [part.strip() for part in raw.split(",")]
name = parts[0]
age = int(parts[1])
city = parts[2]

print(f"Name: {name}")        # Name: Alice Smith
print(f"Age: {age}")          # Age: 42
print(f"City: {city}")        # City: New York
print(f"Type of age: {type(age).__name__}")  # Type of age: int
```

---

## Mental Models

**Think of variables as labels, not boxes:**

In Python, variables don't store values — they are *names* that point to objects. When you write `x = 42`, you create an integer object `42` in memory and attach the label `x` to it. When you write `x = "hello"`, you attach the label `x` to a new string object — the old `42` object still exists until the garbage collector reclaims it.

```python
x = [1, 2, 3]
y = x           # y and x both point to the SAME list object
y.append(4)
print(x)        # [1, 2, 3, 4] — x is also changed!
```

This matters: assigning `y = x` for mutable objects does NOT copy — it creates a second reference to the same object.

**Types are properties of objects, not variables:**

In Python, the *object* has a type, not the variable. `x = 42` — the integer `42` is of type `int`. The name `x` is just a label with no type of its own. This is why `x` can later point to a string — the label doesn't care.

---

## Module Resources

| Resource | Link |
|----------|------|
| Exercises | [EXERCISES.md](./EXERCISES.md) |
| Test | [TEST.md](./TEST.md) |

---

*Module 1 of 9 — Python Topic*
