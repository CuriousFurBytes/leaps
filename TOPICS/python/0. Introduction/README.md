# Module 0: Introduction

← *(First Module)* | [Topic Home](../README.md) | [Next → Variables and Types](../1.%20Variables%20and%20Types/)

![Status](https://img.shields.io/badge/status-Not%20Started-lightgrey)
![Module](https://img.shields.io/badge/module-0%20of%209-blue)
![Time](https://img.shields.io/badge/time-2--3%20hours-green)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner-brightgreen)

---

## Table of Contents

- [Overview](#overview)
- [Learning Goals](#learning-goals)
- [Prerequisites](#prerequisites)
- [Why This Matters](#why-this-matters)
- [Historical Context](#historical-context)
- [Core Concepts](#core-concepts)
  - [Installing Python](#installing-python)
  - [The REPL](#the-repl)
  - [Your First Script](#your-first-script)
  - [The Zen of Python](#the-zen-of-python)
  - [Python Versions](#python-versions)
- [Common Beginner Mistakes](#common-beginner-mistakes)
- [Practical Examples](#practical-examples)
- [Module Resources](#module-resources)
- [Further Reading](#further-reading)

---

## Overview

This module is your entry point into Python. By the end, you will have Python installed and running on your machine, understand what the REPL is and how to use it, have written and executed your first Python script, and have a foundational sense of Python's philosophy and place in the programming landscape.

No prior programming experience is required. If you've programmed before in another language, this module will be quick — skim it and focus on what's different.

**What you'll cover:**
- Installing Python and verifying the installation
- The Python REPL — interactive experimentation
- Writing and running a `.py` script
- The Zen of Python (PEP 20) — Python's guiding philosophy
- Python 2 vs Python 3 — why it matters even in 2025

---

## Learning Goals

By the end of this module, you will be able to:

1. Install Python 3.x on your operating system (or verify an existing installation)
2. Open an interactive Python REPL session and execute expressions
3. Write a Python script in a file and run it from the command line
4. Explain Python's philosophy as expressed in the Zen of Python
5. Correctly identify whether Python code is Python 2 or Python 3
6. Use `print()` as a function and understand why it's a function (not a statement)
7. Access Python's built-in help system (`help()`)
8. Use `import this` to display the Zen of Python and explain at least three principles

---

## Prerequisites

- **Required:** Basic computer literacy — you can create files, use a terminal/command prompt, and install software
- **Helpful:** Familiarity with a text editor
- **No programming experience required**

> [!TIP]
> If you are completely new to using a terminal, spend 30 minutes with a "command line basics" tutorial before starting this module. Python is best learned alongside the command line.

---

## Difficulty and Time Estimate

| Aspect | Value |
|--------|-------|
| **Difficulty** | Beginner |
| **Estimated Time** | 2–3 hours |
| **Time with Exercises** | 3–4 hours |
| **Best Approach** | Type every example by hand — don't copy/paste |

---

## Why This Matters

Python is consistently ranked as one of the top 3 most popular programming languages in the world (TIOBE Index, Stack Overflow Developer Survey). It is:

- **The dominant language for data science and machine learning** — NumPy, Pandas, PyTorch, TensorFlow are all Python-first
- **Widely used in web backend development** — Instagram, Pinterest, Dropbox, and thousands of startups use Django or Flask
- **The go-to tool for automation and scripting** — system administrators, DevOps engineers, and researchers all rely on Python scripts
- **The most popular language for teaching programming** — used in introductory courses at MIT, Stanford, and universities worldwide

Learning Python opens doors in almost every area of software and technology. And because it reads almost like English, the barrier to getting started is lower than nearly any other language.

---

## Historical Context

Python's origin story is unusually personal. In December 1989, **Guido van Rossum** — a Dutch programmer working at Centrum Wiskunde & Informatica (CWI) in Amsterdam — was looking for a programming project to work on over the Christmas holiday. He decided to build a successor to the **ABC** language, which he had worked on at CWI. ABC was a well-designed teaching language, but it had limitations: it couldn't be extended with C modules, it had poor error messages, and it wasn't widely adopted.

Guido wanted a language that:
- Was as easy to read and write as ABC
- Could be extended and embedded in C programs
- Had better error handling
- Was "open" — freely available to modify and redistribute

The name came not from the reptile, but from **Monty Python's Flying Circus**, the BBC comedy series Guido was a fan of. Python's documentation and community have always carried a playful sense of humor — example code often uses variables named `spam` and `eggs`, references to Monty Python sketches.

Python 0.9.0 was posted to the alt.sources Usenet newsgroup on **February 20, 1991**. The language quickly attracted a community. Python 2.0 in 2000 added list comprehensions, full garbage collection, and Unicode support. Python 3.0 in 2008 broke backward compatibility intentionally to fix design mistakes — a painful but necessary step. Python 2 reached end-of-life on January 1, 2020.

Guido served as Python's BDFL (Benevolent Dictator For Life) until 2018, when he stepped down after a contentious PEP discussion. Python is now governed by an elected **Steering Council**.

---

## Core Concepts

### Installing Python

**Verify existing installation:**

```bash
python --version
# or
python3 --version
```text

Expected output: `Python 3.12.x` (or similar 3.x version)

**Installation options:**

- **macOS**: Use `brew install python3` (via Homebrew) or download from python.org
- **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install python3 python3-pip`
- **Windows**: Download the installer from https://python.org/downloads/ — check "Add Python to PATH" during installation
- **pyenv** (recommended for managing multiple versions): https://github.com/pyenv/pyenv

**Recommended: Install a recent Python 3.x**

As of 2025, Python 3.12 and 3.13 are current. Avoid Python 2.x entirely.

```bash
# After installation, verify:
python3 --version         # Python 3.12.x
python3 -m pip --version  # pip 24.x
```text

> [!NOTE]
> On some systems, `python` refers to Python 2. Use `python3` explicitly until you've configured your environment. The `python` command in this topic's material assumes Python 3.

---

### The REPL

REPL stands for **Read-Eval-Print Loop**. It is Python's interactive mode — you type an expression, Python evaluates it, prints the result, and waits for more input. It's invaluable for experimentation.

Start it by running `python3` with no arguments:

```text
$ python3
Python 3.12.3 (main, Apr  9 2024, 08:09:14) [GCC 13.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```text

The `>>>` prompt means Python is waiting for input. The `...` prompt means Python is waiting for you to finish a multi-line statement.

**Example REPL session:**

```python
>>> 2 + 2
4
>>> "hello" + " " + "world"
'hello world'
>>> 10 / 3
3.3333333333333335
>>> 10 // 3    # integer division
3
>>> 10 % 3     # modulo (remainder)
1
>>> name = "Alice"
>>> f"Hello, {name}!"
'Hello, Alice!'
>>> type(42)
<class 'int'>
>>> help(str.upper)   # built-in help system
```text

Exit the REPL with `exit()`, `quit()`, or `Ctrl+D` (Linux/macOS) / `Ctrl+Z Enter` (Windows).

> [!TIP]
> Use the REPL constantly while learning. Whenever you're unsure about how something works, test it immediately in the REPL. This feedback loop is one of Python's greatest advantages as a learning language.

---

### Your First Script

Create a file named `hello.py` with the following content:

```python
# hello.py — My first Python script
# Lines starting with # are comments — Python ignores them

print("Hello, World!")
print("Welcome to Python!")

# Variables hold values
name = "Alice"
year = 2025

# f-strings let you embed expressions in strings
print(f"Hello, {name}! It is {year}.")

# Python can do math
print(f"2 + 2 = {2 + 2}")
print(f"The square root of 144 is {144**0.5}")
```text

Run it from the command line:

```bash
python3 hello.py
```text

Expected output:
```text
Hello, World!
Welcome to Python!
Hello, Alice! It is 2025.
2 + 2 = 4
The square root of 144 is 12.0
```text

**What just happened:**
- `print()` is a built-in function that writes to standard output
- `#` starts a comment — Python ignores everything after it on that line
- `=` assigns a value to a variable
- `f"..."` is an f-string — `{}` inside evaluates the enclosed expression
- `**` is the exponentiation operator (`144**0.5` = √144 = 12.0)

---

### The Zen of Python

Python has a guiding philosophy encoded as an Easter egg. In the REPL, run:

```python
>>> import this
```text

Output:
```text
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```text

**Three principles worth dwelling on:**

1. **"Readability counts"** — Python code is written to be read as much as to be executed. Indentation as structure, verbose names over abbreviations, clarity over cleverness — these all flow from this principle. When you write Python, ask: "Would someone else understand this without a comment?"

2. **"Errors should never pass silently. Unless explicitly silenced."** — Don't suppress exceptions with empty `except:` blocks. Don't return `None` when an error occurred without flagging it. If something goes wrong, say so. This principle saves enormous debugging time in real systems.

3. **"There should be one — and preferably only one — obvious way to do it."** — Unlike Perl's philosophy of "there's more than one way to do it," Python favors a single idiomatic approach. This is why `for item in list:` is preferred over index-based loops; why list comprehensions exist; why `with open(...)` is the standard pattern. Learning "the Pythonic way" means learning to recognize and prefer the obvious approach.

---

### Python Versions

**Python 2 vs Python 3** is a settled debate: use Python 3. Python 2 reached end-of-life on January 1, 2020 and receives no security updates. Major differences that tripped up learners:

| Feature | Python 2 | Python 3 |
|---------|----------|----------|
| `print` | Statement: `print "hello"` | Function: `print("hello")` |
| Division | `5 / 2 == 2` (integer) | `5 / 2 == 2.5` (float) |
| Strings | Byte strings by default | Unicode by default |
| `range()` | Returns a list | Returns an iterator (lazy) |
| `input()` | Evaluates input as code | Returns a string |

**Why does this matter now?** You may encounter Python 2 code in legacy codebases, old tutorials, Stack Overflow answers from before 2020, and some system Python installations. Recognizing the differences helps you adapt older examples to Python 3.

**Current Python 3 versions (as of 2025):**
- Python 3.13 — latest stable, features experimental free-threaded mode
- Python 3.12 — fully stable, widely deployed
- Python 3.10+ — adds structural pattern matching (`match`/`case`)
- Python 3.8+ — adds walrus operator (`:=`), f-string debugging (`f"{x=}"`)

> [!NOTE]
> This topic targets Python 3.10+. All code examples use modern Python 3 syntax and idioms.

---

## Common Beginner Mistakes

> [!WARNING]
> **Not Using Virtual Environments**
> Installing packages globally with `pip install` without a virtual environment pollutes your system Python and causes dependency conflicts between projects. Always create a virtual environment:
> ```bash
> python3 -m venv .venv
> source .venv/bin/activate   # Linux/macOS
> # .venv\Scripts\activate    # Windows
> pip install package-name
> ```
> Make this a reflex before starting any new Python project.

> [!WARNING]
> **Mixing Python 2 and Python 3 Syntax**
> If your system has both `python` (Python 2) and `python3` (Python 3) installed, running the wrong one causes confusing errors. Always use `python3` explicitly, or use `pyenv` to manage versions. Check with `python3 --version`.

> [!WARNING]
> **Using `print` Without Parentheses**
> In Python 3, `print` is a function. `print "hello"` is a syntax error. Always use `print("hello")`. This trips up everyone who learned Python 2 first.

---

## Practical Examples

### Example 1: Using Python as a Calculator

```python
# Arithmetic operations
print(2 + 3)       # 5
print(10 - 4)      # 6
print(3 * 7)       # 21
print(15 / 4)      # 3.75 (always float in Python 3)
print(15 // 4)     # 3   (integer division, floor)
print(15 % 4)      # 3   (modulo — remainder)
print(2 ** 10)     # 1024 (exponentiation)

# Order of operations (PEMDAS/BODMAS)
print(2 + 3 * 4)   # 14 (not 20 — multiplication first)
print((2 + 3) * 4) # 20 (parentheses first)

# Python integers have no overflow!
print(2 ** 100)    # 1267650600228229401496703205376
```text

### Example 2: Getting User Input

```python
# input() always returns a string
name = input("Enter your name: ")
print(f"Hello, {name}!")

# Convert to number for math
age_str = input("Enter your age: ")
age = int(age_str)
print(f"In 10 years you will be {age + 10}.")
```text

### Example 3: Python's Built-in Help

```python
# Access help for any object, function, or module
help(print)      # full documentation for print()
help(str)        # documentation for the str type
help(str.split)  # documentation for str.split()
help()           # enter interactive help browser

# Quick attribute list
dir(str)         # list all attributes and methods of str
dir([])          # list all methods of a list
```text

---

## Module Resources

| Resource | Link |
|----------|------|
| Exercises | [EXERCISES.md](./EXERCISES.md) |
| Test | [TEST.md](./TEST.md) |
| Questions | [QUESTIONS.md](./QUESTIONS.md) |
| Notes | [NOTES.md](./NOTES.md) |
| Answers | [ANSWERS.md](./ANSWERS.md) |
| Resources | [RESOURCES.md](./RESOURCES.md) |
| Notebook | [notebooks/01_getting_started.ipynb](./notebooks/01_getting_started.ipynb) |

---

## Further Reading

- [Python Official Tutorial — Informal Introduction](https://docs.python.org/3/tutorial/introduction.html) — The official first steps guide; accurate and comprehensive
- [Automate the Boring Stuff — Chapter 1](https://automatetheboringstuff.com/2e/chapter1/) — Practical, friendly introduction with a real-world focus (free online)
- [Real Python — Python Basics](https://realpython.com/python-basics/) — Well-structured beginner track with exercises

---

*Module 0 of 9 — Python Topic*
