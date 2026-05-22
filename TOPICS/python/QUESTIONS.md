# Python — Questions

[← Topic Home](./README.md)

Topic-level questions that arose while studying Python. These are bigger-picture questions that span multiple modules. Module-specific questions belong in each module's `QUESTIONS.md`.

---

## How to Use This File

- Add questions as they occur to you — don't wait until you think you understand.
- Mark questions answered with `[x]` once you've found a satisfying answer.
- Link to the source of the answer (module, book, article, etc.).
- Leave unanswered questions here to revisit — confusion documented now becomes insight later.

---

## Questions

---

### [x] Q1: Why does Python use indentation for structure instead of braces or keywords?

**Asked:** When starting Module 0

**Answer:**
This was a deliberate design choice by Guido van Rossum based on his experience with ABC (Python's predecessor language). The reasoning is multi-layered:

1. **Readability**: In practice, well-written code in any language is indented consistently. Python simply enforces what good programmers do anyway — eliminating the visual noise of `{` and `}` while ensuring structure is always visible.

2. **No mismatch bugs**: Languages with braces allow bugs where indentation and structure diverge (the code looks nested but isn't, or vice versa). Python makes indentation the *canonical* structure indicator.

3. **The Zen**: "There should be one — and preferably only one — obvious way to do it." With indentation as the single mechanism, there's no style debate about brace placement.

The tradeoff is sensitivity to mixed tabs/spaces (solved by PEP 8's mandate to use spaces only and Python 3's explicit error on tab/space mixing).

**Source:** Module 0, PEP 20, "Python's History and Design" — Guido's blog

---

### [ ] Q2: When should I use a class versus just using functions and dictionaries?

**Asked:** Around Module 4-5

**Thoughts so far:** I know classes group data and behavior, but sometimes a dict + functions feels simpler. When does the overhead of a class actually pay off?

*This is a deeper design question. Revisit after completing Module 5 (OOP).*

---

### [ ] Q3: Python's GIL seems like a major limitation — why hasn't it been removed?

**Asked:** When reading about concurrency (Module 8 preview)

**Thoughts so far:** I've read that removing the GIL would allow true CPU parallelism, but it would break many C extensions. Is PEP 703 (Python 3.13 experimental free-threaded mode) the answer?

*Research: Look into PEP 703, Gilectomy project history, and Sam Gross's work.*

---

### [ ] Q4: How does Python actually manage memory — what's the full picture beyond "reference counting"?

**Asked:** After reading the GLOSSARY entry on GC

**Thoughts so far:** I understand that reference counting handles most cases and the cyclic GC handles cycles. But what about memory fragmentation? How does CPython's memory allocator (pymalloc) work? When does `del` actually free memory vs just decrement a refcount?

*This seems like an advanced topic. May require reading CPython Internals book.*

---

### [ ] Q5: What makes Python "slow" and how do serious Python programs achieve acceptable performance?

**Asked:** After hearing Python is 10-100x slower than C

**Thoughts so far:** I know about PyPy, Cython, numpy vectorization, and multiprocessing. But what are the specific bottlenecks — interpreter overhead, dynamic dispatch, memory layout? How do libraries like NumPy get C-level speed while being callable from Python?

*Plan: Profile some real code after Module 8, then read "High Performance Python".*

---

*Add new questions below this line.*

---
