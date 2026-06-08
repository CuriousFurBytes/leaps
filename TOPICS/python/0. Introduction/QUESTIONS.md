# Module 0: Introduction — Questions

[← Module Home](./README.md) | [Topic Questions](../QUESTIONS.md) | [Topic Home](../README.md)

Questions that arose while studying Module 0. Module-level questions go here; bigger-picture Python questions go in the topic-level [QUESTIONS.md](../QUESTIONS.md).

---

## Questions

---

### [x] Q1: How do I install multiple versions of Python on the same machine?

**Asked:** Day 1 — I wanted to test code on both Python 3.11 and 3.12

**Answer:**
Use `pyenv` — a version manager for Python. It lets you install and switch between multiple Python versions without touching your system Python.

**Installation (Linux/macOS):**
```bash
# Install pyenv
curl https://pyenv.run | bash

# Add to your shell config (~/.bashrc or ~/.zshrc):
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Install Python versions
pyenv install 3.12.3
pyenv install 3.11.9

# Set global default
pyenv global 3.12.3

# Set local default for a project directory
pyenv local 3.11.9   # creates .python-version file
```

**For Windows:** Use `pyenv-win` (github.com/pyenv-win/pyenv-win) or the official Python installers from python.org.

**Alternative:** The newer `uv` tool (`astral.sh/uv`) also manages Python versions and is significantly faster.

**Source:** pyenv documentation, personal testing

---

### [ ] Q2: What exactly happens when Python runs my `.py` file — what's the step-by-step process?

**Asked:** After learning that Python compiles to bytecode

**Thoughts so far:** I know Python isn't purely interpreted — there's a compilation step to bytecode. But what exactly is that process? Does it happen every time? What is the `.pyc` file in `__pycache__`? Is there a VM involved?

*This seems related to CPython internals. Plan to revisit after Module 6 (Modules and Packages) which might cover `__pycache__` and import mechanics.*

---

### [ ] Q3: The REPL is great for experimenting, but is there a better interactive Python environment than the basic `>>>` REPL?

**Asked:** After the REPL felt limiting for multi-line editing

**Thoughts so far:** I've heard of IPython. The REPL doesn't support multi-line editing well and has no syntax highlighting. Is it a better option, and when should I use it?

*Try IPython as a REPL replacement — `pip install ipython`.*

---

*Add new questions below this line as they arise during study.*

---
