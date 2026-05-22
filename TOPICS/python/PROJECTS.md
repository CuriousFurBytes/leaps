# Python — Projects

[← Topic Home](./README.md)

A collection of project ideas organized by difficulty. Each project reinforces specific Python concepts and produces something tangible. Projects are the best way to solidify knowledge — don't skip them.

---

## My Projects

| Project Name | Difficulty | Started | Status | Link |
|-------------|------------|---------|--------|------|
| — | — | — | — | — |

---

## Beginner Projects

*Best started after completing Phase 1 (Modules 0–2)*

---

### B1: Number Guessing Game

**Description:** The computer picks a random number between 1 and 100. The user guesses repeatedly, receiving "higher" or "lower" hints until they guess correctly. Track the number of guesses.

**Concepts Reinforced:** `random` module, `while` loops, `input()`, `int()` conversion, conditional logic, f-strings

**Extensions:**
- Add a scoring system based on number of guesses
- Let the user choose the difficulty (range size)
- Track high scores across sessions using a file

**Estimated Time:** 1–2 hours

---

### B2: Command-Line Calculator

**Description:** A calculator that takes two numbers and an operator (`+`, `-`, `*`, `/`, `**`, `%`) as input and returns the result. Handle division by zero gracefully.

**Concepts Reinforced:** Functions, `match`/`case` or `if/elif`, input validation, exception handling, `while` loops for "calculate again?"

**Extensions:**
- Support parentheses with `eval()` (research the security implications)
- Build a proper expression parser without `eval()`
- Add history of calculations to a list

**Estimated Time:** 2–3 hours

---

### B3: Text File Word Counter

**Description:** Accept a text file path as a command-line argument. Count total words, unique words, and find the top 10 most frequent words. Display results in a clean formatted table.

**Concepts Reinforced:** File I/O, `sys.argv`, `str` methods, `dict` / `Counter`, string processing, `sorted()`

**Extensions:**
- Add support for multiple files
- Output results as CSV
- Exclude common stop words (a, the, is, etc.)

**Estimated Time:** 2–3 hours

---

### B4: Simple Todo CLI

**Description:** A command-line todo app that stores tasks in a JSON file. Support: `add <task>`, `list`, `done <id>`, `remove <id>`, `clear`.

**Concepts Reinforced:** File I/O, JSON, `argparse` or manual argument parsing, lists of dicts, CRUD operations

**Extensions:**
- Add due dates
- Add priority levels
- Filter by status

**Estimated Time:** 3–4 hours

---

### B5: Temperature Converter

**Description:** Convert between Celsius, Fahrenheit, and Kelvin. Accept input from the command line or interactively.

**Concepts Reinforced:** Functions, arithmetic, input/output, `argparse`

**Extensions:**
- Add a menu-driven UI
- Convert a list of temperatures from a CSV file
- Add wind chill and heat index calculations

**Estimated Time:** 1 hour

---

## Intermediate Projects

*Best started after completing Phase 2 (Modules 3–4) or Phase 3 (Modules 5–6)*

---

### I1: Web Scraper

**Description:** Scrape a public website (Wikipedia article, quotes site, news headlines) using `requests` and `BeautifulSoup`. Extract structured data and save it to a CSV or JSON file.

**Concepts Reinforced:** HTTP requests, HTML parsing, file I/O, error handling, data cleaning

**Libraries:** `requests`, `beautifulsoup4`

**Extensions:**
- Add rate limiting (`time.sleep()`) to be polite
- Scrape multiple pages by following links
- Store results in an SQLite database with `sqlite3`

**Estimated Time:** 4–6 hours

---

### I2: File Organizer

**Description:** A script that organizes files in a directory by moving them into subdirectories based on file extension (e.g., `.jpg` → `Images/`, `.pdf` → `Documents/`). Preview changes before applying.

**Concepts Reinforced:** `pathlib`, `shutil`, `os`, recursive directory walking, file metadata, dry-run pattern

**Extensions:**
- Add a config file for custom rules
- Handle duplicates intelligently (rename instead of overwrite)
- Add undo functionality with a log file

**Estimated Time:** 3–5 hours

---

### I3: Password Generator

**Description:** Generate secure passwords with configurable length, character sets (uppercase, lowercase, digits, symbols), and quantity. Copy to clipboard. Option to pronounceable passwords.

**Concepts Reinforced:** `secrets` module (NOT `random`), `string` module, `argparse`, clipboard (`pyperclip`)

**Extensions:**
- Check generated password against haveibeenpwned.com API (k-anonymity model)
- Save named passwords to an encrypted local store
- Evaluate password strength

**Estimated Time:** 2–3 hours

---

### I4: CSV Data Analyzer

**Description:** Load a CSV dataset (use a public dataset from Kaggle or data.gov). Compute summary statistics: min, max, mean, median, standard deviation per column. Detect missing values. Output a readable report.

**Concepts Reinforced:** File I/O, `csv` module, basic statistics (`statistics` module), data cleaning, tabular output with `tabulate`

**Extensions:**
- Use `pandas` for the same task — compare the approaches
- Generate a histogram for numeric columns using `matplotlib`
- Add filtering by column value

**Estimated Time:** 4–6 hours

---

### I5: REST API Client

**Description:** Build a command-line client for a public REST API (e.g., OpenWeatherMap, GitHub API, or JSONPlaceholder for testing). Fetch data, display it formatted, support multiple commands.

**Concepts Reinforced:** `requests`, JSON parsing, API keys (environment variables), `argparse`, `dataclasses` for response models

**Extensions:**
- Cache responses locally to avoid redundant API calls
- Add rate limiting awareness
- Format output in multiple formats (JSON, table, summary)

**Estimated Time:** 4–6 hours

---

## Advanced Projects

*Best started after completing all 9 modules*

---

### A1: Build a CLI Framework

**Description:** Build a minimal decorator-based CLI framework similar to Click or Typer. Support: `@app.command()` decorator, automatic help text from docstrings, argument type coercion, subcommands.

**Concepts Reinforced:** Decorators, `*args`/`**kwargs`, `inspect` module, type hints, `sys.argv` parsing, OOP

**Estimated Time:** 10–15 hours

---

### A2: Task Queue

**Description:** Build a simple persistent task queue using only the Python standard library. Support: `enqueue(func, args)`, `worker()` that processes tasks from the queue, retry on failure, task status tracking.

**Concepts Reinforced:** `multiprocessing`, `queue.Queue`, `pickle`, `sqlite3`, concurrency patterns, worker pattern

**Estimated Time:** 8–12 hours

---

### A3: Simple HTTP Server from Scratch

**Description:** Implement an HTTP/1.1 server using only `socket`. Support: GET requests, static file serving, basic routing with a decorator (`@app.route("/")`), 404 handling, proper HTTP headers.

**Concepts Reinforced:** `socket`, TCP/IP fundamentals, HTTP protocol, parsing raw bytes, threading for concurrent connections

**Estimated Time:** 8–12 hours

---

### A4: Interpreter for a Tiny Language

**Description:** Build a tree-walking interpreter for a simple expression language. Support: arithmetic, variables (`let x = 5`), `if/else`, `while`, basic functions. Write a lexer, parser (recursive descent), and evaluator.

**Concepts Reinforced:** Recursion, AST design, `dataclasses`, visitor pattern, language theory basics

**Reference:** "Writing an Interpreter in Go" (concepts apply in Python)

**Estimated Time:** 15–20 hours

---

## Expert / Capstone Projects

*For learners who want to push beyond the curriculum*

---

### E1: Python Linter (Subset)

**Description:** Build a linter that checks Python code for a subset of PEP 8 rules. Parse Python source using the `ast` module. Check for: line length, naming conventions, unused imports, bare `except:` clauses. Report violations with line numbers.

**Concepts Reinforced:** `ast` module, tree walking, pattern matching, file I/O, rule engine design

**Estimated Time:** 20–30 hours

---

### E2: Contribute to CPython

**Description:** Make a real contribution to the CPython repository. Start with the "easy" labeled issues on bugs.python.org. Fix a bug, improve documentation, or add a test.

**Concepts Reinforced:** C/Python interface, CPython development workflow, communication with core developers

**Resources:** https://devguide.python.org/

**Estimated Time:** Variable (10–50+ hours depending on issue)

---

### E3: Build a Web Framework

**Description:** Build a minimal WSGI web framework with: routing (path and method), request/response objects, middleware support, templating integration (Jinja2), and a dev server.

**Concepts Reinforced:** WSGI protocol, OOP design, decorators, HTTP, middleware pattern

**Reference:** Study Flask's source code (it's surprisingly readable)

**Estimated Time:** 20–40 hours

---

### E4: Distributed Task System

**Description:** Build a distributed task system where a coordinator distributes work to multiple worker processes (possibly across machines) using sockets or Redis as a message broker.

**Concepts Reinforced:** `multiprocessing`, `socket` or `redis-py`, serialization, fault tolerance, distributed systems concepts

**Estimated Time:** 30–50 hours

---

## Project Tracking

After completing a project, add it to the table at the top of this file and link to the code or notes.

> [!TIP]
> Even incomplete projects are valuable. Document what you learned and where you got stuck. Returning to an abandoned project after learning more is a great learning loop.
