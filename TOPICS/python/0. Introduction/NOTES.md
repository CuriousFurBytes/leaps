# Module 0: Introduction — Notes

[← Module Home](./README.md) | [Topic Home](../README.md)

Personal study notes for Module 0. Written while working through the material.

*Newest entries at the top. Date-stamp each session.*

---

## 2025-05-22 — Started Module 0

**What I did today:**
- Read through README.md — got the history and philosophy overview
- Installed Python 3.12 via Homebrew
- Spent ~30 min in the REPL just experimenting
- Ran `import this` — the Zen of Python is interesting
- Wrote my first script (`hello.py`)

**What clicked:**

The REPL is really powerful for experimenting. Being able to type `2 + 2` and immediately see `4`, or try a string method and instantly see the result — it makes experimentation feel instant and low-stakes. I'm used to Java where you have to write a whole class, compile, run... this is so much faster for quick tests.

The f-string syntax feels natural. `f"Hello, {name}!"` is readable even without knowing Python. I like how it closely mirrors how you'd write the sentence in English.

**Key observations from the REPL:**

```python
# Python integers have NO upper limit — this is wild
>>> 2 ** 100
1267650600228229401496703205376

# Integer division vs true division
>>> 10 / 3      # true division — always returns float
3.3333333333333335
>>> 10 // 3     # floor division — truncates to int
3

# type() tells you what something is
>>> type(42)
<class 'int'>
>>> type(3.14)
<class 'float'>
>>> type("hello")
<class 'str'>
>>> type(True)
<class 'bool'>
>>> type(None)
<class 'NoneType'>
```text

**The Zen — three principles that stood out:**

1. **"Readability counts"** — When I look at my hello.py script, I can read it almost like English. That's clearly intentional. I'm going to make variable names descriptive even when writing "quick" scripts.

2. **"Errors should never pass silently"** — I've been burned by swallowed errors in other code before. I'll be careful never to write `except: pass` unless I have a really good reason.

3. **"Simple is better than complex"** — This is a reminder not to over-engineer. If there's a one-liner that's clear, use it. If the one-liner is confusing, use three clear lines instead.

**What's still unclear:**
- What exactly is a "module" in Python vs a "package"? The `import datetime` — that's a module from the standard library. But how does Python find it? Where is it stored? (→ add to QUESTIONS.md, probably answered in Module 6)
- Virtual environments: I set one up but I'm fuzzy on exactly WHY it helps. More on this when I get to Module 6.

**How I feel about this topic:**
Excited. Python feels fast to get started with compared to other languages I've tried. The REPL makes it feel like a conversation rather than a compile-run cycle.

---

## Notes Template for Future Sessions

*(Copy this block for each study session)*

```text
## YYYY-MM-DD — [session title]

**What I did:**
-

**What clicked:**


**Code examples that helped me understand:**
\```python
# example here
\```

**What's still unclear:**
-

**Connections to other things I know:**
-
```text

---

*These notes are for personal reference. Write honestly — confusion documented now becomes insight later.*
