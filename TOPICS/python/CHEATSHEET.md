# Python — Cheatsheet

[← Topic Home](./README.md)

A quick reference for Python syntax and common patterns. Not a tutorial — assumes you know the concepts and just need a syntax reminder.

---

## Data Types

```python
# Integer
x = 42
x = 1_000_000      # underscores for readability
x = 0xFF           # hex
x = 0b1010         # binary
x = 0o17           # octal

# Float
f = 3.14
f = 1.5e-3         # scientific notation = 0.0015

# Complex
c = 3 + 4j

# String
s = "hello"
s = 'world'
s = """multi
line"""
s = r"\n is a raw string"   # raw — no escape processing
s = b"bytes literal"        # bytes, not str

# Boolean
t, f = True, False

# None
nothing = None

# Check type
type(x)            # <class 'int'>
isinstance(x, int) # True
```

---

## String Operations

```python
s = "Hello, World!"

# Indexing & slicing
s[0]          # 'H'
s[-1]         # '!'
s[0:5]        # 'Hello'
s[::2]        # every second char
s[::-1]       # reverse

# Common methods
s.upper()              # 'HELLO, WORLD!'
s.lower()              # 'hello, world!'
s.strip()              # remove leading/trailing whitespace
s.lstrip("H")          # left strip specific chars
s.split(", ")          # ['Hello', 'World!']
", ".join(["a","b"])   # 'a, b'
s.replace("World","Python")  # 'Hello, Python!'
s.startswith("Hello")  # True
s.endswith("!")        # True
s.find("World")        # 7  (index, or -1 if not found)
s.count("l")           # 3
s.strip().split()      # split on any whitespace

# f-strings (Python 3.6+)
name = "Alice"
age = 30
f"{name} is {age} years old"
f"{3.14159:.2f}"       # '3.14'
f"{1000000:,}"         # '1,000,000'
f"{42:08b}"            # '00101010' (binary, zero-padded to 8)
f"{name!r}"            # repr() of name: "'Alice'"
f"{2 + 2 = }"          # '2 + 2 = 4'  (Python 3.8+ debug format)
```

---

## Collections

```python
# List — ordered, mutable, allows duplicates
lst = [1, 2, 3]
lst.append(4)         # [1, 2, 3, 4]
lst.extend([5, 6])    # [1, 2, 3, 4, 5, 6]
lst.insert(0, 0)      # [0, 1, 2, 3, 4, 5, 6]
lst.pop()             # removes and returns last
lst.pop(0)            # removes and returns index 0
lst.remove(3)         # removes first occurrence of value 3
lst.sort()            # in-place sort
sorted(lst)           # returns new sorted list
lst.reverse()         # in-place reverse
lst.index(2)          # index of first occurrence
lst.count(1)          # count of occurrences
len(lst)              # length

# Tuple — ordered, immutable
t = (1, 2, 3)
t = 1, 2, 3           # parentheses optional
a, b, c = t           # unpacking
first, *rest = t      # extended unpacking

# Dict — key-value pairs, ordered (3.7+), mutable
d = {"a": 1, "b": 2}
d["c"] = 3            # add/update
d.get("z", 0)         # get with default
d.keys()              # dict_keys view
d.values()            # dict_values view
d.items()             # dict_items view (key, value tuples)
d.pop("a")            # remove and return value
d.update({"d": 4})    # merge another dict in
{**d, "e": 5}         # merge with spread (Python 3.5+)
d | {"f": 6}          # merge operator (Python 3.9+)

# Set — unordered, unique values, mutable
s = {1, 2, 3}
s.add(4)
s.discard(99)         # remove if present (no error if absent)
s1 | s2               # union
s1 & s2               # intersection
s1 - s2               # difference
s1 ^ s2               # symmetric difference
s1 <= s2              # is s1 a subset of s2?
```

---

## Comprehensions

```python
# List comprehension
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
flat = [x for row in matrix for x in row]  # flatten nested list

# Dict comprehension
word_lengths = {word: len(word) for word in words}
inverted = {v: k for k, v in d.items()}

# Set comprehension
unique_lengths = {len(word) for word in words}

# Generator expression (lazy, memory efficient)
total = sum(x**2 for x in range(1_000_000))
```

---

## Functions

```python
# Basic definition
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

# *args — variable positional arguments (tuple)
def add(*numbers):
    return sum(numbers)

# **kwargs — variable keyword arguments (dict)
def configure(**options):
    for key, val in options.items():
        print(f"{key} = {val}")

# Positional-only (/) and keyword-only (*) parameters
def func(pos_only, /, normal, *, kw_only):
    ...

# Lambda — anonymous function (single expression)
square = lambda x: x**2
sorted(items, key=lambda x: x.name)

# Type hints (PEP 484)
def add(a: int, b: int) -> int:
    return a + b

# Docstring
def divide(a: float, b: float) -> float:
    """
    Divide a by b.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        The result of a / b.

    Raises:
        ZeroDivisionError: If b is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b
```

---

## Control Flow

```python
# if / elif / else
if x > 0:
    print("positive")
elif x < 0:
    print("negative")
else:
    print("zero")

# Ternary expression
label = "even" if x % 2 == 0 else "odd"

# for loop
for i in range(10):
    print(i)

for i, val in enumerate(items):
    print(f"{i}: {val}")

for k, v in d.items():
    print(f"{k}: {v}")

for a, b in zip(list1, list2):
    print(a, b)

# while
while condition:
    ...

# Loop control
break       # exit loop
continue    # skip to next iteration
else:       # runs if loop completed without break
    ...

# match / case (Python 3.10+)
match command:
    case "quit":
        quit()
    case "go" | "move":
        move()
    case {"action": action, "target": target}:
        do_action(action, target)
    case _:
        print("unknown command")
```

---

## Common Built-ins

```python
len(x)                  # length of collection
range(start, stop, step) # integer range (lazy)
enumerate(iterable)     # yields (index, value) pairs
zip(*iterables)         # pairs elements from multiple iterables
map(func, iterable)     # apply func to each element (lazy)
filter(func, iterable)  # keep elements where func returns True (lazy)
sorted(iterable, key=..., reverse=False)  # returns new sorted list
reversed(iterable)      # returns iterator in reverse
sum(iterable, start=0)  # sum of elements
min(iterable)           # minimum
max(iterable)           # maximum
abs(x)                  # absolute value
round(x, ndigits)       # round to n decimal places
all(iterable)           # True if all elements are truthy
any(iterable)           # True if any element is truthy
print(*objects, sep=' ', end='\n', file=sys.stdout)
input(prompt)           # read line from stdin
type(x)                 # return type of x
isinstance(x, type)     # check type
id(x)                   # memory address of object
hash(x)                 # hash value (for hashable objects)
dir(x)                  # list attributes of x
vars(x)                 # __dict__ of x
repr(x)                 # developer-readable string representation
str(x)                  # user-readable string representation
int(x), float(x), str(x), bool(x), list(x), dict(x), set(x), tuple(x)  # conversions
open(path, mode)        # open file
```

---

## File I/O

```python
# Read entire file
with open("file.txt", "r") as f:
    content = f.read()

# Read lines
with open("file.txt") as f:
    lines = f.readlines()      # list of lines (with \n)
    lines = f.read().splitlines()  # list without \n

# Iterate line by line (memory efficient)
with open("file.txt") as f:
    for line in f:
        process(line.strip())

# Write
with open("output.txt", "w") as f:
    f.write("content\n")

# Append
with open("log.txt", "a") as f:
    f.write("new entry\n")

# File modes: r (read), w (write/truncate), a (append),
#             b (binary), t (text, default), + (read+write)

# pathlib (modern, preferred)
from pathlib import Path
p = Path("data/file.txt")
p.read_text()                  # read entire file
p.write_text("content")        # write (overwrites)
p.exists()                     # True/False
p.is_file(), p.is_dir()
p.parent                       # parent directory
p.name                         # filename
p.stem                         # filename without extension
p.suffix                       # extension ('.txt')
p.with_suffix(".csv")          # change extension
list(p.parent.glob("*.txt"))   # glob pattern matching
p.mkdir(parents=True, exist_ok=True)  # create directory
```

---

## Error Handling

```python
# Basic try/except
try:
    result = risky_operation()
except ValueError as e:
    print(f"Bad value: {e}")
except (TypeError, KeyError) as e:
    print(f"Type or key error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
    raise   # re-raise
else:
    # Runs only if NO exception occurred
    print("Success:", result)
finally:
    # Always runs
    cleanup()

# Raise exceptions
raise ValueError("something went wrong")
raise RuntimeError("bad state") from original_exception  # chaining

# Custom exception
class AppError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

# Context manager for cleanup (alternative to try/finally)
with open("file") as f:
    ...
```

---

## Classes

```python
class Animal:
    # Class variable (shared across all instances)
    kingdom = "Animalia"

    def __init__(self, name: str, sound: str):
        # Instance variables
        self.name = name
        self._sound = sound   # convention: _ means "private"

    def speak(self) -> str:
        return f"{self.name} says {self._sound}"

    def __repr__(self) -> str:
        return f"Animal(name={self.name!r})"

    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_string(cls, s: str) -> "Animal":
        name, sound = s.split(":")
        return cls(name, sound)

    @staticmethod
    def is_valid_name(name: str) -> bool:
        return bool(name) and name.isalpha()

    @property
    def sound(self) -> str:
        return self._sound

    @sound.setter
    def sound(self, value: str):
        self._sound = value.lower()


class Dog(Animal):
    def __init__(self, name: str, breed: str):
        super().__init__(name, "woof")
        self.breed = breed

    def speak(self) -> str:
        return f"{super().speak()} ({self.breed})"


# Dataclass (Python 3.7+) — auto-generates __init__, __repr__, __eq__
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float
    label: str = ""
    tags: list = field(default_factory=list)

    def distance_to_origin(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5
```

---

## Common Imports

```python
import os                   # OS interface
import sys                  # System functions
import re                   # Regular expressions
import json                 # JSON encode/decode
import csv                  # CSV reading/writing
import math                 # Math functions
import random               # Random numbers (NOT cryptographic)
import secrets              # Cryptographic random
import datetime             # Dates and times
import time                 # Time utilities
import pathlib              # Object-oriented file paths
import shutil               # File operations (copy, move, rmtree)
import subprocess           # Run shell commands
import argparse             # CLI argument parsing
import logging              # Structured logging
import collections          # Counter, deque, defaultdict, namedtuple
import itertools            # Advanced iteration tools
import functools            # Higher-order functions (lru_cache, partial, reduce)
import copy                 # Shallow/deep copy
import io                   # In-memory I/O
import threading            # Threading
import multiprocessing      # Process-based parallelism
import asyncio              # Async I/O
import contextlib           # Context manager utilities
import dataclasses          # @dataclass decorator
import typing               # Type hints
import unittest             # Built-in testing
from abc import ABC, abstractmethod  # Abstract base classes
from enum import Enum, auto          # Enumerations
```

---

## Useful Patterns

```python
# Swap variables
a, b = b, a

# Flatten list of lists
flat = [x for sublist in nested for x in sublist]
# or: list(itertools.chain.from_iterable(nested))

# Count occurrences
from collections import Counter
counts = Counter(words)
most_common = counts.most_common(10)

# Default dict
from collections import defaultdict
d = defaultdict(list)
d["key"].append("value")  # no KeyError on first access

# Memoization / caching
from functools import lru_cache
@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

# Named tuples
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2)
print(p.x, p.y)

# Context manager from a function
from contextlib import contextmanager
@contextmanager
def timer():
    import time
    start = time.perf_counter()
    yield
    print(f"Elapsed: {time.perf_counter() - start:.3f}s")

with timer():
    expensive_operation()

# Chained comparison
1 < x < 10          # same as: 1 < x and x < 10

# Walrus operator (Python 3.8+)
if (n := len(data)) > 10:
    print(f"Too many items: {n}")

while chunk := f.read(8192):
    process(chunk)
```

---

*Last reviewed: 2025-05-22*
