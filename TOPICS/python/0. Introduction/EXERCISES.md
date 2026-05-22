# Module 0: Introduction — Exercises

[← Module Home](./README.md) | [Topic Home](../README.md)

Complete these exercises in order. Each builds on the previous. Do not look at the solutions until you've made a genuine attempt.

**Scoring:** 5 exercises × 2 pts each = 10 pts possible  
**Record your score in:** `../README.md` test score table

---

## Exercise 1 — Hello, REPL

**Difficulty:** Easy | **Points:** 2 | **Estimated Time:** 15 min

### Context

The REPL (Read-Eval-Print Loop) is Python's interactive mode. It's your most important tool for experimentation and quick testing. Before writing scripts, you should be comfortable running code interactively.

### Task

Open a Python REPL and complete the following tasks interactively.

### Requirements

1. Start the Python REPL by running `python3` in your terminal
2. Type `print("Hello, World!")` and press Enter — observe the output
3. Type `2 + 2` and press Enter — observe that the result is printed automatically
4. Type `"Python" + " " + "is" + " " + "great"` — observe string concatenation
5. Type `type(42)` — observe the output
6. Type `type("hello")` — observe the output
7. Exit the REPL with `exit()`

### Hints

- The `>>>` prompt means Python is waiting for input
- You don't need `print()` in the REPL for simple expressions — Python prints them automatically
- If you see `...` it means Python expects more input (you started a multi-line construct)

### Expected Output

```text
>>> print("Hello, World!")
Hello, World!
>>> 2 + 2
4
>>> "Python" + " " + "is" + " " + "great"
'Python is great'
>>> type(42)
<class 'int'>
>>> type("hello")
<class 'str'>
```text

### Solution

<details>
<summary>Click to reveal solution</summary>

```bash
$ python3
Python 3.12.3 ...
>>> print("Hello, World!")
Hello, World!
>>> 2 + 2
4
>>> "Python" + " " + "is" + " " + "great"
'Python is great'
>>> type(42)
<class 'int'>
>>> type("hello")
<class 'str'>
>>> exit()
$
```text

**Key observations:**
- In the REPL, expression values are automatically printed (no `print()` needed)
- `print()` produces output without quotes; bare expressions show the repr with quotes
- `type()` tells you what kind of object something is

</details>

---

## Exercise 2 — Your First Script

**Difficulty:** Easy | **Points:** 2 | **Estimated Time:** 20 min

### Context

While the REPL is great for experimentation, real Python programs live in `.py` files. This exercise gets you writing, saving, and executing your first Python script.

### Task

Write a Python script that introduces you and prints today's date.

### Requirements

1. Create a file named `intro.py`
2. The script must print your name on its own line
3. The script must print the current date using Python's `datetime` module
4. The script must include at least 2 comments explaining what the code does
5. Run the script with `python3 intro.py` and verify the output

### Hints

- Import the `datetime` module: `import datetime`
- Get today's date: `datetime.date.today()`
- Format the date nicely: `datetime.date.today().strftime("%B %d, %Y")`
- A comment starts with `#`

### Expected Output

```text
My name is Alice.
Today is May 22, 2025.
```text

*(Your name and date will differ)*

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
# intro.py — My first Python script

import datetime

# Print my name
name = "Alice"
print(f"My name is {name}.")

# Get and print today's date
today = datetime.date.today()
formatted = today.strftime("%B %d, %Y")
print(f"Today is {formatted}.")
```text

**Key observations:**
- `import datetime` loads the standard library `datetime` module
- `datetime.date.today()` returns a `date` object representing today
- `strftime()` formats dates as strings; `%B` = full month name, `%d` = day, `%Y` = 4-digit year
- f-strings (`f"..."`) embed variable values in strings

</details>

---

## Exercise 3 — The Zen of Python

**Difficulty:** Medium | **Points:** 2 | **Estimated Time:** 30 min

### Context

The Zen of Python captures the language's design philosophy. Understanding it shapes how you think about writing Python code — not just what works, but what's considered good Python.

### Task

Run `import this` in the REPL and write explanations of three Zen principles in your own words.

### Requirements

1. Run `import this` in the REPL and read the full output
2. Choose **three** principles that resonate with you
3. For each principle, write 2–4 sentences explaining:
   - What you think the principle means
   - One concrete example of code that follows it
   - One concrete example of code that violates it
4. Write your explanations in your `NOTES.md` file (see [NOTES.md](./NOTES.md))

### Hints

- Think about code you've seen in other languages that felt messy — which principles does Python try to prevent that with?
- There are no wrong answers here. This is a reflection exercise.
- Examples don't have to be complete programs — pseudocode or brief snippets are fine

### Expected Output

(Your own written explanation in NOTES.md — no single right answer)

### Example Answer

<details>
<summary>Click to see example explanation</summary>

**Principle chosen: "Readability counts"**

This principle means that code isn't just instructions for a computer — it's a communication between humans. When I write code, I should write it so that another person (or future me) can understand it without deep analysis.

Code that follows this: Using descriptive variable names like `total_price` instead of `tp`, and writing `for item in shopping_cart:` instead of `for i in range(len(shopping_cart)):`.

Code that violates this: Cramming multiple operations onto one line like `x=a if(b>c and d!=e)else(f*g+h)` just to save vertical space.

---

**Principle chosen: "Errors should never pass silently"**

This means I shouldn't hide errors by catching all exceptions and doing nothing with them. If something went wrong, the program should say so — loudly — rather than continuing silently with bad state.

Code that follows this: `except ValueError as e: print(f"Invalid input: {e}")` — acknowledges the error and reports it.

Code that violates this: `except: pass` — silently swallows every possible exception and continues as if nothing happened. This is almost always a bug.

---

**Principle chosen: "Simple is better than complex"**

If I can accomplish something in 5 lines of simple code, I shouldn't use a 30-line class hierarchy unless I have a compelling reason. Complexity should only be introduced when simplicity genuinely can't solve the problem.

Code that follows this: Using a list comprehension `[x**2 for x in nums]` instead of building a custom iterator class just to square numbers.

Code that violates this: Implementing a Strategy pattern with abstract base classes and factories to choose between two simple behaviors that could be handled with an `if` statement.

</details>

---

## Exercise 4 — Exploring Python Versions

**Difficulty:** Medium | **Points:** 2 | **Estimated Time:** 20 min

### Context

Knowing what Python version you're running matters because language features vary by version. Python 3.10 added pattern matching, 3.8 added the walrus operator, 3.6 added f-strings. Understanding version differences helps you write compatible code and understand which features you can use.

### Task

Find the Python version installed on your system and research what's new in the latest Python 3.x release.

### Requirements

1. Run `python3 --version` in your terminal — record the version
2. Run `python3 -c "import sys; print(sys.version_info)"` — understand the output
3. In the Python REPL, run `import sys; print(sys.version)` — note the full version string
4. Look up "What's New in Python 3.12" (or whatever version you have) at https://docs.python.org/3/whatsnew/
5. Find **two** new features from your version and write a 1-sentence description of each in your NOTES.md

### Hints

- `python3 --version` gives a quick version check
- `sys.version_info` returns a named tuple with `major`, `minor`, `micro` components
- The "What's New" pages on docs.python.org are an excellent habit to check with each new release

### Expected Output

```bash
$ python3 --version
Python 3.12.3

$ python3 -c "import sys; print(sys.version_info)"
sys.version_info(major=3, minor=12, micro=3, releaselevel='final', serial=0)
```text

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
import sys

# Full version string
print(sys.version)
# e.g., '3.12.3 (main, Apr  9 2024, 08:09:14) [GCC 13.2.0]'

# Structured version info
print(sys.version_info)
# sys.version_info(major=3, minor=12, micro=3, releaselevel='final', serial=0)

# Access components
print(f"Python {sys.version_info.major}.{sys.version_info.minor}")
# Python 3.12

# Conditional logic based on version
if sys.version_info >= (3, 10):
    print("Pattern matching is available!")
if sys.version_info >= (3, 12):
    print("Type parameter syntax (PEP 695) is available!")
```text

</details>

---

## Exercise 5 — Interactive Greeter

**Difficulty:** Hard | **Points:** 2 | **Estimated Time:** 30 min

### Context

The `input()` function pauses the program and waits for the user to type something. This is the foundation of interactive command-line programs. Combined with f-strings and basic logic, you can already write useful programs after just one module.

### Task

Write a script that greets the user by name and asks for their age.

### Requirements

1. Create a file named `greeter.py`
2. Ask the user for their name using `input()`
3. Ask the user for their age using `input()` — convert to integer with `int()`
4. Print a personalized greeting that includes their name
5. Calculate and print what year they were born (use the current year)
6. Handle the case where the user enters nothing for their name — use "World" as the default
7. Handle the case where the user enters a non-numeric age — print an error message instead of crashing

### Hints

- `input("Enter your name: ")` prints the prompt and returns what the user typed as a string
- `str.strip()` removes leading/trailing whitespace
- `or` can provide a default: `name = input("Name: ").strip() or "World"`
- Handle invalid age input with a `try/except ValueError` block
- `datetime.date.today().year` gives the current year as an integer

### Expected Output

```text
Enter your name: Alice
Enter your age: 30
Hello, Alice! Welcome to Python.
You were born around 1995.
```text

Or, with no name and invalid age:

```text
Enter your name: 
Enter your age: abc
Hello, World! Welcome to Python.
Invalid age entered — please enter a whole number next time.
```text

### Solution

<details>
<summary>Click to reveal solution</summary>

```python
# greeter.py — Interactive greeter with error handling

import datetime

# Get name — use "World" if the user enters nothing
name = input("Enter your name: ").strip() or "World"

# Get age — handle invalid input gracefully
age_input = input("Enter your age: ").strip()

try:
    age = int(age_input)
    current_year = datetime.date.today().year
    birth_year = current_year - age
    age_message = f"You were born around {birth_year}."
except ValueError:
    age_message = "Invalid age entered — please enter a whole number next time."

# Print greeting
print(f"Hello, {name}! Welcome to Python.")
print(age_message)
```text

**Key observations:**
- `.strip()` removes accidental whitespace the user might have typed
- `or "World"` uses Python's short-circuit evaluation: if the left side is falsy (empty string), use the right side
- `try/except ValueError` catches the specific error that `int()` raises for non-numeric input
- Breaking the logic into clear steps with descriptive variable names makes the code readable

</details>

---

## Bonus Exercise — Exploring Help

**Difficulty:** Easy | **No points — just exploration**

In the REPL, explore Python's built-in help system:

1. Run `help()` and browse around. Exit with `q` or `quit`.
2. Run `help(print)` — read the full documentation for `print()`
3. Run `dir(str)` — look at all the methods available on strings
4. Pick one method you don't recognize (e.g., `str.zfill`) and run `help(str.zfill)` to understand it

Write down one method you discovered that you think will be useful.

---

*Record your completion in [../README.md](../README.md)*
