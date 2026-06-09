# Python — Resources

[← Topic Home](./README.md)

A curated list of high-quality, verified resources for learning Python. Organized by format and level.

---

## Table of Contents

- [Official Documentation](#official-documentation)
- [Books](#books)
- [Online Courses and Tutorials](#online-courses-and-tutorials)
- [Video Learning](#video-learning)
- [Practice Platforms](#practice-platforms)
- [Tools and Environment](#tools-and-environment)
- [IDEs and Editors](#ides-and-editors)
- [Communities](#communities)
- [Important PEPs](#important-peps)
- [Reference Cheatsheets](#reference-cheatsheets)

---

## Official Documentation

| Resource | URL | Notes |
|----------|-----|-------|
| Python Official Docs | https://docs.python.org/3/ | Comprehensive, authoritative reference |
| Python Tutorial (Beginners) | https://docs.python.org/3/tutorial/ | Official step-by-step introduction |
| Python Standard Library | https://docs.python.org/3/library/ | Full reference for all built-in modules |
| Python Language Reference | https://docs.python.org/3/reference/ | Formal language specification |
| Python HOWTOs | https://docs.python.org/3/howto/ | Guides on specific topics (sorting, regex, etc.) |
| What's New in Python | https://docs.python.org/3/whatsnew/ | Changes per version — useful for staying current |

> [!TIP]
> Bookmark `docs.python.org/3/` — it should be your first stop when something doesn't work or you need to know what a built-in does.

---

## Books

### Beginner

| Book | Author | Notes |
|------|--------|-------|
| **Python Crash Course, 3rd Ed.** | Eric Matthes | Best beginner book; project-based, very practical |
| **Automate the Boring Stuff with Python, 2nd Ed.** | Al Sweigart | Free online at automatetheboringstuff.com; great for scripting |
| **Learn Python the Hard Way** | Zed Shaw | Highly repetition-focused; polarizing but effective for some |

> [!NOTE]
> *Automate the Boring Stuff* is available completely free at [automatetheboringstuff.com](https://automatetheboringstuff.com/). No excuses for not reading it.

### Intermediate

| Book | Author | Notes |
|------|--------|-------|
| **Fluent Python, 2nd Ed.** | Luciano Ramalho | Essential for mastering Pythonic idioms and internals |
| **Python Cookbook, 3rd Ed.** | David Beazley & Brian K. Jones | Recipe-based; covers advanced patterns |
| **Effective Python, 2nd Ed.** | Brett Slatkin | 90 specific ways to write better Python code |
| **Python Tricks: The Book** | Dan Bader | Clean, focused book on idiomatic Python |

### Advanced / Reference

| Book | Author | Notes |
|------|--------|-------|
| **CPython Internals** | Anthony Shaw | How CPython works under the hood |
| **Architecture Patterns with Python** | Harry Percival & Bob Gregory | DDD, TDD, and clean architecture in Python |
| **High Performance Python** | Micha Gorelick & Ian Ozsvald | Profiling, optimization, Cython, concurrency |

---

## Online Courses and Tutorials

| Resource | URL | Level | Notes |
|----------|-----|-------|-------|
| Real Python | https://realpython.com/ | All levels | High-quality tutorials and articles; some free, some paid |
| Python.org Tutorial | https://docs.python.org/3/tutorial/ | Beginner | Official; comprehensive and accurate |
| Full Stack Python | https://www.fullstackpython.com/ | Intermediate | Explains Python web concepts with curated links |
| Talk Python to Me Courses | https://training.talkpython.fm/ | Intermediate+ | Excellent paid courses from Michael Kennedy |

---

## Video Learning

Python tutorial series are available on all major video platforms including YouTube. Search for:

- "Python for Beginners full course" — many free, well-rated series exist
- "Python tutorial 2024/2025" — to find up-to-date content
- "Corey Schafer Python" — highly regarded tutorial series
- "Socratica Python" — concise, clearly explained concept videos
- "mCoding" — deep-dives into Python internals and advanced topics

> [!NOTE]
> Video URLs change over time. Search for the creator names above rather than following stale links.

**Podcasts:**
- *Talk Python to Me* — interviews with Python ecosystem creators and contributors
- *Python Bytes* — weekly news digest for Python developers

---

## Practice Platforms

| Platform | URL | Notes |
|----------|-----|-------|
| Exercism — Python Track | https://exercism.org/tracks/python | Free, mentor-reviewed exercises; excellent quality |
| LeetCode | https://leetcode.com/ | Algorithm/interview prep; filter by Python |
| HackerRank — Python | https://www.hackerrank.com/domains/python | Structured skill tracks |
| Codewars | https://www.codewars.com/ | Community kata; fun and competitive |
| Project Euler | https://projecteuler.net/ | Math-based programming challenges |
| Advent of Code | https://adventofcode.com/ | Annual coding challenges; popular in Python community |

---

## Tools and Environment

### Package Management

| Tool | Purpose | Notes |
|------|---------|-------|
| **pip** | Install packages from PyPI | Comes with Python; `pip install <package>` |
| **venv** | Create virtual environments | Built-in: `python -m venv .venv` |
| **pyenv** | Manage multiple Python versions | Install from github.com/pyenv/pyenv |
| **uv** | Fast package/project manager (Rust-based) | Modern replacement for pip + venv |
| **Poetry** | Dependency management + packaging | `pyproject.toml`-based; great for libraries |
| **pipx** | Install CLI tools in isolated environments | `pipx install black` |

### Code Quality

| Tool | Purpose | Command |
|------|---------|---------|
| **black** | Opinionated code formatter | `black .` |
| **ruff** | Fast linter (replaces flake8, isort, etc.) | `ruff check .` |
| **mypy** | Static type checker | `mypy src/` |
| **pytest** | Testing framework | `pytest tests/` |

### Package Repository

- **PyPI** (Python Package Index) — https://pypi.org/ — search for any package here

---

## IDEs and Editors

| Editor | Notes |
|--------|-------|
| **VS Code** | Free; use the official Python extension (`ms-python.python`) and Pylance |
| **PyCharm** | JetBrains IDE; Community edition is free; excellent for larger projects |
| **Neovim / Vim** | For those who prefer terminal; configure with LSP + pyright |
| **Thonny** | Designed for beginners; great for learning; built-in debugger visualization |

---

## Communities

| Community | Where | Notes |
|-----------|-------|-------|
| Python Subreddit | reddit.com/r/Python | General Python discussion |
| learnpython Subreddit | reddit.com/r/learnpython | Beginner-friendly help |
| Python Discord | pythondiscord.com | Active, welcoming; dedicated help channels |
| Python Forums | discuss.python.org | Official discussion forum |
| Stack Overflow | stackoverflow.com (tag: python) | Q&A; massive archive of answered questions |
| Real Python Slack | (via Real Python membership) | Community for Real Python readers |

---

## Important PEPs

PEPs (Python Enhancement Proposals) define how the language evolves. These are essential reading:

| PEP | Title | Why It Matters |
|-----|-------|---------------|
| **PEP 8** | Style Guide for Python Code | The canonical Python style guide — follow it always |
| **PEP 20** | The Zen of Python | `import this` — the philosophical foundation |
| **PEP 257** | Docstring Conventions | How to write good docstrings |
| **PEP 484** | Type Hints | How to annotate types in Python |
| **PEP 526** | Variable Annotations | Syntax for annotating variables |
| **PEP 572** | Walrus Operator `:=` | Assignment expressions (Python 3.8+) |
| **PEP 634** | Structural Pattern Matching | `match` / `case` (Python 3.10+) |

Read PEPs at: https://peps.python.org/

---

## Reference Cheatsheets

See [CHEATSHEET.md](./CHEATSHEET.md) in this topic for a quick Python syntax reference.

External cheatsheets:
- **Python Cheatsheet** — https://www.pythoncheatsheet.org/ — comprehensive, well-organized
- **Real Python Cheat Sheets** — available at realpython.com/python-cheat-sheet/

---

*Last reviewed: 2025-05-22*
