# Module 0: Introduction — Answer Key

[← Test](./TEST.md) | [Module Home](./README.md) | [Topic Home](../README.md)

> [!WARNING]
> **Do not read this before attempting the test.** The test is a learning tool — honest self-assessment reveals what you actually know versus what you think you know. Look at answers only after completing all questions you can.

---

## Section 1: Recall — Answers

**Q1. Who created Python?**

**Answer:** Guido van Rossum

Guido van Rossum is a Dutch programmer who created Python in 1989 while working at CWI (Centrum Wiskunde & Informatica) in the Netherlands. He served as Python's BDFL (Benevolent Dictator For Life) until 2018.

---

**Q2. In what year was Python first publicly released?**

**Answer:** 1991

Python 0.9.0 was first posted to the alt.sources Usenet newsgroup on February 20, 1991. Development began in December 1989 (Guido's "holiday project"), but the first public release was 1991.

*(Accept: 1989 if the student mentions it as the start of development — but the first public release was 1991.)*

---

**Q3. What file extension is used for Python source files?**

**Answer:** `.py`

Python source files use the `.py` extension. Compiled bytecode files use `.pyc` (stored in `__pycache__/`).

---

**Q4. What does REPL stand for?**

**Answer:** Read-Eval-Print Loop

- **Read:** reads user input
- **Eval:** evaluates the input as Python code
- **Print:** prints the result
- **Loop:** repeats the process

---

**Q5. What Python command displays the Zen of Python?**

**Answer:** `import this`

Typing `import this` in the Python REPL or in a Python script displays the 19 aphorisms of the Zen of Python (PEP 20), written by Tim Peters.

---

## Section 2: Conceptual Understanding — Answers

**Q6. Three key differences between Python 2 and Python 3. Why does EOL matter?**

**Model Answer:**

Three key differences:

1. **`print` statement vs function**: Python 2 uses `print "hello"` (statement); Python 3 uses `print("hello")` (function call). This is the most visible difference.

2. **Integer division**: In Python 2, `5 / 2` evaluates to `2` (integer division when both operands are integers). In Python 3, `5 / 2` evaluates to `2.5` (always true division). Use `5 // 2` for integer division in Python 3.

3. **Strings are Unicode by default**: Python 3 strings are Unicode (`str`); Python 2 strings are bytes by default and Unicode requires a `u"..."` prefix. This affects text processing significantly.

**Why EOL matters:** Python 2.7 reached end-of-life on January 1, 2020. This means it receives no security patches, bug fixes, or updates. Running Python 2 in production is a security risk. Also, all major libraries (NumPy, Pandas, Django, etc.) have dropped Python 2 support — you can no longer use the modern ecosystem with Python 2.

*(2 pts — award 1 pt for any two correct differences + partial EOL explanation)*

---

**Q7. "Errors should never pass silently" — explanation and violation example.**

**Model Answer:**

This principle means that when something goes wrong in a program, the error should be reported and handled explicitly — not hidden. Programs that silently swallow errors become impossible to debug because there's no signal that something is wrong.

**Violation example:**
```python
# BAD — silently ignores ALL errors
try:
    result = risky_calculation()
except:
    pass  # Error is gone, program continues with bad state
```

**Better approach:**
```python
try:
    result = risky_calculation()
except ValueError as e:
    logging.error(f"Calculation failed: {e}")
    result = default_value  # explicit fallback
```

The phrase "Unless explicitly silenced" acknowledges that there are legitimate cases for suppressing errors (e.g., checking if a file exists before opening it). But even then, be explicit: use `contextlib.suppress(FileNotFoundError)` rather than a bare `except: pass`.

*(2 pts — both explanation and violation example needed)*

---

**Q8. Compiled vs interpreted — where does Python fall?**

**Model Answer:**

A **compiled language** (like C or Rust) transforms source code into machine code ahead-of-time using a compiler. The resulting binary runs directly on the CPU. This produces faster code but requires a compile step before execution.

An **interpreted language** traditionally executes source code line-by-line at runtime without a separate compile step. This enables interactivity (like the REPL) and faster development cycles, but is generally slower at runtime.

**Python is both, somewhat:** CPython compiles Python source to bytecode (stored in `.pyc` files in `__pycache__/`) and then the Python Virtual Machine (PVM) interprets the bytecode. So it's "compiled to bytecode, then interpreted."

**Tradeoffs:**
- **Advantages of Python's approach:** Fast to iterate, interactive REPL, no compile step during development, runs on any system with Python installed
- **Disadvantages:** Slower execution speed than ahead-of-time compiled languages; can't distribute a binary without including Python

*(2 pts — award full marks for a clear explanation of both terms and an accurate description of Python's actual approach)*

---

## Section 3: Practical Application — Answers

**Q9. Output of arithmetic operations:**

```python
x = 10
y = 3
print(x / y)    # 3.3333333333333335  (true division — always float in Python 3)
print(x // y)   # 3                   (floor division — rounds down to int)
print(x % y)    # 1                   (modulo — remainder of 10 ÷ 3)
print(x ** y)   # 1000               (exponentiation — 10 to the power of 3)
```

*(1 pt for correct output, 1 pt for correct explanations)*

---

**Q10. Find the bug and fix it:**

**The bug:** `age` is the string `"25"`. You cannot add an integer (`1`) to a string (`"25"`) in Python 3 — this raises a `TypeError: can only concatenate str (not "int") to str`.

**Corrected code:**
```python
name = "Alice"
age = 25  # Fix 1: store as integer, not string

# Or if age must remain a string:
# age = "25"
# age_num = int(age)
# print(f"Hello, {name}! You are {age_num + 1} years old.")

print(f"Hello, {name}! You are {age + 1} years old.")
# Output: Hello, Alice! You are 26 years old.
```

*(1 pt for identifying the type error, 1 pt for correct fix)*

---

## Section 4: Scenario — Answer

**Q11. Two things to change for Python 3 compatibility:**

```python
# Original Python 2 code:
print "Starting program..."          # 1. print is a statement in Python 2
name = raw_input("Enter your name: ") # 2. raw_input() doesn't exist in Python 3
result = 10 / 4                       # 3. In Python 2: result = 2 (integer division!)
print "Result:", result
print "Hello, " + name + "!"
```

**Changes needed (minimum two required for full marks):**

1. **`print "..."` → `print("...")`**: In Python 3, `print` is a function, not a statement. All `print` lines need parentheses.

2. **`raw_input()` → `input()`**: Python 2 had both `input()` (which evaluated input as Python code — dangerous) and `raw_input()` (which returned a string). Python 3 removed `raw_input()` and `input()` now always returns a string. Using `raw_input()` in Python 3 raises `NameError`.

**Bonus (not required but worth noting):**
- `result = 10 / 4` — In Python 2, this gives `2` (integer division). In Python 3, this gives `2.5` (true division). Not an error in Python 3, but the behavior changed.

*(3 pts — 1.5 per correct, valid change identified)*

---

## Section 5: Essay — Rubric

**Q12. Why choose Python over Java, JavaScript, or C++?**

**Strong answer includes:**
- **Beginner accessibility**: Python's syntax is close to English; no boilerplate (`public static void main`); no manual memory management
- **Specific use cases**: data science/ML (NumPy, Pandas, PyTorch), scripting/automation, rapid prototyping — areas where Python has no real competition in terms of ecosystem
- **Tradeoffs acknowledged**: Python is slower than Java or C++ for CPU-bound work; JavaScript is better for browser/frontend; C++ is necessary for systems programming, game engines, embedded
- **Suitable learner profile**: Python is ideal for scientists, data analysts, beginners, and anyone whose primary goal isn't systems programming

**Award:**
- 2 pts: Specific, nuanced answer with tradeoffs mentioned
- 1 pt: General answer without specific tradeoffs
- 0 pts: Off-topic or incorrect claims

---

## Bonus Section — Answers

**B1. `__pycache__` directory:**

When Python runs a `.py` file, it first compiles it to **bytecode** — a lower-level, platform-independent representation. The bytecode is saved as a `.pyc` file in `__pycache__/`. On subsequent runs, if the `.py` file hasn't changed, Python loads the cached `.pyc` instead of recompiling, making startup faster.

The filename includes the Python version (e.g., `hello.cpython-312.pyc`) so different Python versions can coexist. You can safely delete `__pycache__/` — Python will recreate it.

---

**B2. `import antigravity`:**

Running `import antigravity` in Python opens a web browser pointing to the xkcd comic #353 — "Python" — which shows someone saying "I wrote a program that lets you do anything. Just import antigravity." It's an Easter egg celebrating Python's "batteries included" philosophy and its accessibility.

```python
>>> import antigravity
# Opens: https://xkcd.com/353/
```

---

**B3. One-liner to capitalize, then reverse:**

```python
print("hello world".title()[::-1])
# Output: dlrow olleH
```

Explanation:
- `"hello world".title()` → `"Hello World"` (capitalizes each word)
- `[::- 1]` is a slice with step `-1` — reverses the string
- `print(...)` outputs the result

*(Full credit for any working one-liner with correct output)*

---

*Answer key last reviewed: 2025-05-22*
