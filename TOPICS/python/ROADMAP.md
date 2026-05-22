# Python Learning Roadmap

[← Topic Home](./README.md)

This roadmap shows the recommended progression through the Python topic modules. Each phase builds on the previous one. Follow the phases in order — jumping ahead is possible but not recommended.

---

## Visual Roadmap

```mermaid
flowchart TD
    START([🐍 Start Here]) --> M0

    subgraph PHASE1["Phase 1: Foundation (Modules 0–2)"]
        M0["Module 0\nIntroduction\n2–3 hrs"]
        M1["Module 1\nVariables & Types\n4–5 hrs"]
        M2["Module 2\nFunctions\n5–6 hrs"]
        M0 --> M1 --> M2
    end

    subgraph PHASE2["Phase 2: Core Data (Modules 3–4)"]
        M3["Module 3\nControl Flow\n4–5 hrs"]
        M4["Module 4\nData Structures\n6–8 hrs"]
        M3 --> M4
    end

    subgraph PHASE3["Phase 3: Architecture (Modules 5–6)"]
        M5["Module 5\nObject-Oriented\n8–10 hrs"]
        M6["Module 6\nModules & Packages\n4–5 hrs"]
        M5 --> M6
    end

    subgraph PHASE4["Phase 4: Advanced (Modules 7–8)"]
        M7["Module 7\nFile I/O & Errors\n5–6 hrs"]
        M8["Module 8\nConcurrency\n8–10 hrs"]
        M7 --> M8
    end

    PHASE1 --> PHASE2 --> PHASE3 --> PHASE4

    PHASE4 --> COMPLETE(["✅ Core Python Complete"])

    COMPLETE --> WEB["Specialization:\nWeb Development\nDjango / FastAPI"]
    COMPLETE --> DATA["Specialization:\nData Science\nNumPy / Pandas"]
    COMPLETE --> ML["Specialization:\nMachine Learning\nPyTorch / TensorFlow"]
    COMPLETE --> AUTO["Specialization:\nAutomation\nscripting / DevOps"]
```text

---

## Phase Breakdown

### Phase 1: Foundation (Modules 0–2)
**Goal:** Get Python installed, understand its fundamentals, and write reusable code.

| Module | Key Topics | Estimated Time | Checkpoint |
|--------|-----------|----------------|------------|
| 0: Introduction | Install Python, REPL, first script, Zen of Python | 2–3 hours | Can run Python scripts |
| 1: Variables & Types | int, float, str, bool, None, type(), dynamic typing | 4–5 hours | Understands type system |
| 2: Functions | def, params, return, scope, closures, lambdas | 5–6 hours | Can write modular code |

**Phase 1 Project:** Build a simple command-line calculator.

---

### Phase 2: Core Data (Modules 3–4)
**Goal:** Control program execution and work with Python's powerful built-in collections.

| Module | Key Topics | Estimated Time | Checkpoint |
|--------|-----------|----------------|------------|
| 3: Control Flow | if/elif/else, for, while, break/continue, comprehensions | 4–5 hours | Can write complex logic |
| 4: Data Structures | list, dict, set, tuple, namedtuple, deque | 6–8 hours | Chooses right structure |

**Phase 2 Project:** Build a word-frequency counter for text files.

---

### Phase 3: Architecture (Modules 5–6)
**Goal:** Write well-organized, reusable, maintainable Python programs.

| Module | Key Topics | Estimated Time | Checkpoint |
|--------|-----------|----------------|------------|
| 5: OOP | class, __init__, inheritance, polymorphism, dunder methods | 8–10 hours | Can design class hierarchies |
| 6: Modules & Packages | import, __init__.py, pip, venv, pypi | 4–5 hours | Can structure a project |

**Phase 3 Project:** Build a CLI task manager with OOP design.

---

### Phase 4: Advanced (Modules 7–8)
**Goal:** Handle real-world programming challenges: files, errors, and concurrency.

| Module | Key Topics | Estimated Time | Checkpoint |
|--------|-----------|----------------|------------|
| 7: File I/O & Errors | open, pathlib, try/except, custom exceptions, context managers | 5–6 hours | Robust error handling |
| 8: Concurrency | threading, multiprocessing, asyncio, GIL | 8–10 hours | Can write concurrent code |

**Phase 4 Project:** Build a concurrent web scraper with error handling.

---

## Total Time Estimate

| Phase | Time Range |
|-------|-----------|
| Phase 1: Foundation | 11–14 hours |
| Phase 2: Core Data | 10–13 hours |
| Phase 3: Architecture | 12–15 hours |
| Phase 4: Advanced | 13–16 hours |
| **Total Core Python** | **~46–58 hours** |

> [!NOTE]
> These estimates are for reading, taking notes, and completing exercises. Add 2x–3x for project work and deep practice.

---

## After Completion: Specialization Paths

Once all 9 core modules are complete, choose a specialization based on your goals:

### Web Development Path
```text
FastAPI → SQLAlchemy → PostgreSQL → Docker → deployment
   or
Django → DRF → PostgreSQL → Redis → Celery
```text
Recommended topics: [[web-development]], [[docker]], [[databases]]

### Data Science Path
```text
NumPy → Pandas → Matplotlib → Seaborn → Jupyter
  → Scikit-learn → Statistics → SQL
```text
Recommended topics: [[data-science]], [[statistics]], [[sql]]

### Machine Learning Path
```text
NumPy + Pandas → Scikit-learn → PyTorch → deep learning
```text
Recommended topics: [[machine-learning]], [[linear-algebra]], [[calculus]]

### Automation / DevOps Path
```text
os/pathlib → subprocess → argparse → schedule
  → Paramiko → Ansible with Python
```text
Recommended topics: [[linux]], [[networking]], [[docker]]

---

## Study Tips

1. **Don't rush Phase 1.** A solid understanding of variables, types, and functions makes everything else easier.
2. **Type everything.** Don't copy-paste code. Typing builds muscle memory.
3. **Read error messages carefully.** Python's error messages are excellent and usually tell you exactly what went wrong.
4. **Use the REPL** for quick experiments — it gives instant feedback.
5. **Build projects at the end of each phase** — this cements knowledge far better than reading alone.
6. **Read other people's code.** Browse GitHub for Python projects you find interesting.
