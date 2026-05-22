# Python — Glossary

[← Topic Home](./README.md)

Definitions for Python-specific terminology. Organized alphabetically. Add new terms as you encounter them.

---

## A

### BDFL (Benevolent Dictator For Life)
The informal title historically given to Guido van Rossum as Python's creator and long-time lead. Guido stepped down from this role in 2018; Python is now governed by an elected Steering Council.

### Bytecode
The intermediate, platform-independent representation of Python source code produced by the Python compiler. When you run a `.py` file, Python compiles it to bytecode (`.pyc` files stored in `__pycache__/`) before the interpreter executes it. Bytecode is not machine code — it runs on the Python Virtual Machine (PVM), not directly on the CPU.

```python
import dis
dis.dis(lambda x: x + 1)  # shows bytecode disassembly
```

---

## C

### Context Manager
An object that defines `__enter__` and `__exit__` methods, allowing it to be used with the `with` statement. Context managers guarantee cleanup code runs even if an exception occurs. The most common example is file handling:

```python
with open("file.txt") as f:
    data = f.read()
# f.close() is called automatically here, even on error
```

### CPython
The reference implementation of Python, written in C. When people say "Python," they usually mean CPython. Other implementations exist (PyPy, Jython, IronPython), but CPython is the standard. Understanding CPython internals (GIL, reference counting) is important for performance-sensitive work.

---

## D

### Decorator
A callable that takes a function (or class) as input and returns a modified version. Decorators use the `@` syntax and are applied at definition time. They are a powerful metaprogramming tool for adding functionality like logging, authentication, or memoization without modifying the original function body.

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before call")
        result = func(*args, **kwargs)
        print("After call")
        return result
    return wrapper

@my_decorator
def greet(name):
    print(f"Hello, {name}!")
```

### Duck Typing
Python's approach to typing: if an object has the required methods and attributes, it can be used in place of a formal type — regardless of its actual class. "If it walks like a duck and quacks like a duck, it's a duck." This enables flexible, polymorphic code without rigid inheritance hierarchies.

```python
def make_sound(animal):
    animal.speak()  # Works for any object with a speak() method
```

### Dunder Methods (Magic Methods)
Methods with double underscores on both sides (e.g., `__init__`, `__str__`, `__len__`, `__add__`). They define how objects interact with Python's built-in operations and syntax. Also called "magic methods" or "special methods."

```python
class Vector:
    def __init__(self, x, y): self.x, self.y = x, y
    def __add__(self, other): return Vector(self.x + other.x, self.y + other.y)
    def __repr__(self): return f"Vector({self.x}, {self.y})"
```

---

## G

### GC (Garbage Collection)
Python's mechanism for reclaiming memory from objects no longer in use. Python uses two strategies: **reference counting** (primary) and a **cyclic garbage collector** (handles circular references that reference counting misses). The `gc` module provides access to the garbage collector.

### Generator
A special type of iterator created with a function that uses `yield` instead of `return`. Generators produce values lazily — one at a time — making them memory-efficient for large sequences. Generator expressions use `()` syntax similar to list comprehensions.

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

gen = fibonacci()
print(next(gen))  # 0
print(next(gen))  # 1
print(next(gen))  # 1

# Generator expression
squares = (x**2 for x in range(1000000))  # No memory allocated for all 1M values
```

### GIL (Global Interpreter Lock)
A mutex in CPython that allows only one thread to execute Python bytecode at a time. The GIL simplifies memory management (reference counting is not thread-safe without it) but prevents true CPU parallelism across threads. CPU-bound code should use `multiprocessing` or concurrent.futures to bypass the GIL. I/O-bound code uses `threading` or `asyncio` effectively despite the GIL.

> [!NOTE]
> Python 3.13 introduces an experimental "free-threaded" mode (PEP 703) that removes the GIL. This is a major ongoing change to CPython.

---

## I

### Interpreter (Interpreted Language)
Python is interpreted rather than compiled to machine code ahead-of-time. The Python interpreter reads and executes code directly (after compilation to bytecode). This enables interactive use (REPL) and faster iteration but is generally slower than ahead-of-time compiled languages like C or Rust.

### Iterator Protocol
The interface an object must implement to be iterable: `__iter__()` (returns the iterator) and `__next__()` (returns the next value, raises `StopIteration` when exhausted). All Python `for` loops use this protocol under the hood.

```python
class Countdown:
    def __init__(self, n): self.n = n
    def __iter__(self): return self
    def __next__(self):
        if self.n <= 0: raise StopIteration
        self.n -= 1
        return self.n + 1
```

---

## L

### LEGB Rule
Python's scoping rule: when resolving a name, Python searches in this order: **L**ocal → **E**nclosing → **G**lobal → **B**uilt-in. Understanding LEGB is essential for understanding closures and avoiding subtle bugs.

### List Comprehension
A concise, readable syntax for creating lists by applying an expression to each item in an iterable, with optional filtering. Preferred over `map`/`filter` for simple transformations.

```python
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
matrix = [[row[i] for row in [[1,2],[3,4],[5,6]]] for i in range(2)]
```

---

## M

### Metaclass
A class whose instances are classes. In Python, `type` is the default metaclass. Metaclasses allow customization of class creation — useful for ORMs, API frameworks, and advanced patterns. `class Foo(metaclass=MyMeta):` syntax is used. Generally considered an advanced topic; "if you wonder whether you need a metaclass, you don't."

### Module
A single `.py` file containing Python definitions and statements. Modules are the basic unit of code reuse in Python. Import with `import module_name` or `from module_name import something`.

---

## N

### Namespace
A mapping from names to objects. Python has multiple namespaces (local, global, built-in) organized hierarchically. The `dir()` and `vars()` functions inspect namespaces. Namespaces are implemented as dictionaries.

---

## P

### PEP (Python Enhancement Proposal)
The design documents used to propose changes to Python. PEPs go through a community review process before being accepted or rejected. PEP 8 (style guide) and PEP 20 (Zen of Python) are the most famous. Read all accepted PEPs at https://peps.python.org/.

### pip
The standard package installer for Python. Downloads and installs packages from PyPI (Python Package Index). Included with Python since version 3.4.

```bash
pip install requests        # install a package
pip install -r requirements.txt  # install from a requirements file
pip list                    # show installed packages
pip freeze > requirements.txt  # export installed packages
```

### PyPy
An alternative Python implementation written in Python itself (using RPython), featuring a JIT (just-in-time) compiler. PyPy is often significantly faster than CPython for long-running, CPU-bound code. Not compatible with all CPython C extensions.

### Python Virtual Machine (PVM)
The runtime engine that executes Python bytecode. Not a separate program — it's the component of the Python interpreter that runs `.pyc` bytecode. Part of CPython's architecture.

---

## R

### Reference Counting
CPython's primary memory management strategy: every object has a count of how many references point to it. When the count reaches zero, the memory is immediately reclaimed. More predictable than garbage collection, but cannot handle circular references alone (hence the supplemental cyclic GC).

### REPL (Read-Eval-Print Loop)
An interactive programming environment that reads a user input, evaluates it, prints the result, and loops back. The Python REPL is invoked by running `python` (or `python3`) with no arguments. Essential for experimentation. Enhanced REPLs: IPython, Jupyter.

---

## S

### Scope
The region of a program where a name binding is visible. See **LEGB Rule**. Python does not have block scope (like C/Java) — only function, class, and module scope matter.

### String Interning
An optimization where Python reuses the same object for identical short strings and identifiers, rather than creating new string objects. Interned strings can be compared with `is` (identity) instead of `==` (equality), though you should not rely on this behavior in production code.

---

## V

### Virtual Environment
An isolated Python environment with its own interpreter and package set, separate from the system Python. Prevents dependency conflicts between projects. Created with `python -m venv .venv`. Activated with `source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows).

---

## W

### Wheel
A pre-built binary distribution format for Python packages (`.whl` files). Wheels install faster than source distributions because they don't require compilation. Modern packages on PyPI typically distribute wheels for common platforms.

---

*Add new terms as you encounter them. Keep definitions concise but precise.*
