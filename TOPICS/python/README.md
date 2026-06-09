# Python

![Status](https://img.shields.io/badge/status-Active-brightgreen)
![Modules](https://img.shields.io/badge/modules-0%2F9%20completed-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner--Intermediate-blue)
![Language](https://img.shields.io/badge/language-Python-3776AB?logo=python&logoColor=white)

> A versatile, readable, and powerful general-purpose programming language.

> [!NOTE]
> **Key Strengths of Python**
> - **Readable syntax**: Python reads almost like English prose, making it ideal for beginners and experienced developers alike
> - **Rich ecosystem**: Over 500,000 packages on PyPI covering virtually every domain: web, data science, ML, automation, and more
> - **Versatile**: Python excels at scripting, web development, data analysis, machine learning, system automation, and scientific computing
> - **Large community**: One of the most popular languages in the world with an active, welcoming community and extensive documentation

---

## Table of Contents

- [Overview](#overview)
- [Historical Context](#historical-context)
- [Real-World Applications](#real-world-applications)
- [Learning Objectives](#learning-objectives)
- [Difficulty and Time Estimate](#difficulty-and-time-estimate)
- [Prerequisites](#prerequisites)
- [Learning Modules](#learning-modules)
- [Progress](#progress)
- [Milestones](#milestones)
- [Test Scores](#test-scores)
- [Projects](#projects)
- [Resources](#resources)
- [Related Topics](#related-topics)
- [Learning Journal](#learning-journal)

---

## Overview

Python is a high-level, interpreted, general-purpose programming language emphasizing code readability and simplicity. Created with the philosophy that there should be one—and preferably only one—obvious way to do things, Python has become one of the most widely used languages in the world.

Python's design is guided by the **Zen of Python** (PEP 20), a collection of aphorisms that capture the language's core philosophy. Key principles include:

- *Beautiful is better than ugly*
- *Explicit is better than implicit*
- *Simple is better than complex*
- *Readability counts*
- *There should be one—and preferably only one—obvious way to do it*

**Key Features:**
- **Interpreted**: Code is executed line-by-line; no compile step needed during development
- **Dynamically typed**: Variable types are determined at runtime
- **Garbage collected**: Automatic memory management via reference counting + cyclic GC
- **Multi-paradigm**: Supports procedural, object-oriented, and functional programming styles
- **Batteries included**: Extensive standard library covering I/O, networking, math, text processing, and more

---

## Historical Context

Python was created by **Guido van Rossum**, a Dutch programmer, while he was at Centrum Wiskunde & Informatica (CWI) in the Netherlands. Guido conceived Python as a successor to the ABC language and began development during the Christmas holiday of 1989 — making it, in his words, a "holiday project." The language is named after the BBC comedy series *Monty Python's Flying Circus*, not the snake.

### Version History Timeline

| Year | Version | Milestone |
|------|---------|-----------|
| 1989 | 0.x dev | Guido begins Python as a holiday project |
| 1991 | 0.9.0 | First public release on alt.sources Usenet |
| 1994 | 1.0 | Python 1.0 released; lambda, map, filter, reduce added |
| 2000 | 2.0 | List comprehensions, garbage collection, Unicode support |
| 2008 | 3.0 | Python 3 released — major breaking changes, cleaner design |
| 2020 | 2.7 EOL | Python 2.7 officially reaches end-of-life |
| 2023 | 3.12 | Improved error messages, per-interpreter GIL, performance gains |

### Python 2 vs Python 3

Python 3, released in 2008, introduced intentional backward-incompatible changes to fix long-standing design issues. Key changes included:

- `print` became a function: `print("hello")` instead of `print "hello"`
- Integer division changed: `5 / 2 == 2.5` (not `2`)
- Strings are Unicode by default
- `range()` returns an iterator instead of a list
- Many standard library modules were reorganized and renamed

Python 2 reached end-of-life on January 1, 2020. **All new Python code should use Python 3.**

---

## Real-World Applications

| Domain | Tools / Frameworks | Examples |
|--------|--------------------|---------|
| Web Development | Django, Flask, FastAPI | Instagram, Pinterest, Dropbox |
| Data Science | NumPy, Pandas, Matplotlib | Financial analysis, research |
| Machine Learning | PyTorch, TensorFlow, scikit-learn | GPT models, image recognition |
| Automation & Scripting | subprocess, os, pathlib | DevOps pipelines, file processing |
| Scientific Computing | SciPy, SymPy | Academic research, simulations |
| Education | turtle, IDLE | Teaching programming fundamentals |
| Network/Systems | socket, asyncio, Paramiko | Network tools, SSH automation |
| Cybersecurity | Scapy, pwntools | Security research, CTFs |

---

## Learning Objectives

By completing this topic, you will be able to:

1. Write and execute Python scripts from the command line and in interactive environments
2. Declare variables, understand dynamic typing, and use all built-in primitive types
3. Write functions with various parameter types including *args and **kwargs
4. Apply control flow constructs (if/elif/else, for, while, comprehensions)
5. Use Python's core data structures: lists, tuples, dicts, and sets effectively
6. Design and implement classes following OOP principles (encapsulation, inheritance, polymorphism)
7. Organize code into modules and packages; use pip and virtual environments
8. Read from and write to files; handle exceptions gracefully with try/except
9. Write concurrent programs using threading, multiprocessing, and asyncio
10. Apply Pythonic idioms and follow PEP 8 style guidelines
11. Use the Python standard library to solve common programming tasks
12. Debug Python programs using the built-in debugger (pdb) and print-based debugging
13. Write unit tests using pytest
14. Profile and optimize Python code for performance

---

## Difficulty and Time Estimate

| Aspect | Rating |
|--------|--------|
| **Overall Difficulty** | Beginner-Intermediate |
| **Syntax Learning Curve** | Low — very readable |
| **Conceptual Depth** | High — many advanced concepts exist |
| **Estimated Time to Basic Proficiency** | ~50-80 hours |
| **Estimated Time to Intermediate Proficiency** | ~150-200 hours |
| **Estimated Time to Advanced** | 500+ hours of practice |

Python is one of the most beginner-friendly languages for learning programming fundamentals. However, mastering advanced concepts like metaclasses, descriptors, async/await, and CPython internals requires significant dedicated study.

---

## Prerequisites

- **Required**: Basic computer literacy (creating files, using a terminal)
- **Helpful**: [[operating-systems]] — understanding how processes and file systems work
- **Helpful**: Basic understanding of what a program is

No prior programming experience required for Modules 0-3.

---

## Learning Modules

| # | Module | Status | Points | Notes |
|---|--------|--------|--------|-------|
| 0 | [Introduction](./0.%20Introduction/) | - [ ] Not Started | 0 pts | Install, REPL, first script |
| 1 | [Variables and Types](./1.%20Variables%20and%20Types/) | - [ ] Not Started | 0 pts | Primitives, dynamic typing |
| 2 | [Functions](./2.%20Functions/) | - [ ] Not Started | 0 pts | def, scope, closures, decorators |
| 3 | [Control Flow](./3.%20Control%20Flow/) | - [ ] Not Started | 0 pts | if/else, loops, comprehensions |
| 4 | [Data Structures](./4.%20Data%20Structures/) | - [ ] Not Started | 0 pts | list, dict, set, tuple |
| 5 | [Object-Oriented Programming](./5.%20Object-Oriented%20Programming/) | - [ ] Not Started | 0 pts | classes, inheritance, polymorphism |
| 6 | [Modules and Packages](./6.%20Modules%20and%20Packages/) | - [ ] Not Started | 0 pts | import, pip, virtualenv |
| 7 | [File I/O and Error Handling](./7.%20File%20IO%20and%20Error%20Handling/) | - [ ] Not Started | 0 pts | open, try/except, pathlib |
| 8 | [Concurrency](./8.%20Concurrency/) | - [ ] Not Started | 0 pts | threading, multiprocessing, asyncio |

---

## Progress

**Modules Completed:** 0 / 9  
**Total Points:** 0  
**Completion:** `░░░░░░░░░░░░░░░░░░░░ 0%`

---

## Milestones

- [ ] Wrote first Python script
- [ ] Understand data types and variables
- [ ] Can write functions and use modules
- [ ] Built a working CLI application
- [ ] Built a web scraper
- [ ] Comfortable with OOP in Python
- [ ] Built a REST API using Flask or FastAPI
- [ ] Used Python for data analysis with Pandas

---

## Test Scores

| Module | Date | Score | Grade | Notes |
|--------|------|-------|-------|-------|
| — | — | — | — | — |

---

## Projects

See [PROJECTS.md](./PROJECTS.md) for the complete project list with descriptions.

**Quick overview:**
- **Beginner**: Number guessing game, calculator, todo CLI app
- **Intermediate**: Web scraper, CSV data analyzer, REST API client
- **Advanced**: Build a CLI framework, simple HTTP server from scratch
- **Capstone**: Python linter, contribute to CPython

---

## Resources

See [RESOURCES.md](./RESOURCES.md) for the full curated resource list.

**Quick links:**
- [Official Python Documentation](https://docs.python.org/3/)
- [Real Python](https://realpython.com/)
- [Automate the Boring Stuff](https://automatetheboringstuff.com/) (free online)

---

## Related Topics

- [[linux]] — Python scripting is deeply tied to OS interaction
- [[networking]] — Python is used extensively for network programming
- [[data-science]] — NumPy, Pandas, Matplotlib form the data science stack
- [[algorithms]] — Python is popular for algorithm study and interview prep
- [[web-development]] — Django, Flask, FastAPI for backend web development
- [[docker]] — Containerizing Python applications

---

## Learning Journal

*Use this section to record insights, "aha moments", frustrations, and connections you make while learning Python.*

---

<!-- AI Metadata — do not edit manually -->
## AI Metadata

```yaml
topic: python
version: 1.0.0
created: 2024-01-01
last_updated: 2024-01-01
difficulty: beginner-intermediate
estimated_hours: 200
tags:
  - programming
  - scripting
  - backend
  - data-science
  - automation
modules_count: 9
language: python
paradigms:
  - procedural
  - object-oriented
  - functional
related_topics:
  - linux
  - networking
  - data-science
  - algorithms
  - web-development
  - docker
```
<!-- end AI Metadata -->
