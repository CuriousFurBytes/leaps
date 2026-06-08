# Module 0: Introduction — Resources

[← Module Home](./README.md) | [Topic Resources](../RESOURCES.md) | [Topic Home](../README.md)

Resources specific to Module 0: getting Python installed and running your first code. These are supplementary to the topic-wide [RESOURCES.md](../RESOURCES.md).

---

## Getting Python Installed

| Resource | URL | Notes |
|----------|-----|-------|
| Python Downloads | https://www.python.org/downloads/ | Official installer for all platforms |
| pyenv (Linux/macOS) | https://github.com/pyenv/pyenv | Version manager — recommended for managing multiple Python versions |
| pyenv-win (Windows) | https://github.com/pyenv-win/pyenv-win | pyenv for Windows |
| uv | https://astral.sh/uv | Modern, fast Python version and package manager |

### Platform-Specific Guides

**macOS:**
```bash
# Option 1: Use Homebrew (recommended)
brew install python3

# Option 2: Use pyenv
brew install pyenv
pyenv install 3.12.3
pyenv global 3.12.3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Windows:**
- Download the installer from python.org
- During installation: check "Add Python to PATH"
- Or use `winget install Python.Python.3.12`

---

## Online Python Environments (No Installation Required)

If you want to experiment before installing locally:

| Platform | URL | Notes |
|----------|-----|-------|
| Python.org Shell | https://www.python.org/shell/ | Official browser-based Python REPL |
| Replit | https://replit.com/ | Full online IDE; free tier available |

> [!NOTE]
> Online environments are useful for getting started quickly, but install Python locally as soon as possible. Real development happens locally, and you'll need the command line for the exercises in later modules.

---

## First Steps Resources

| Resource | URL | Notes |
|----------|-----|-------|
| Python.org Tutorial: Informal Intro | https://docs.python.org/3/tutorial/introduction.html | Official; covers numbers, strings, and lists |
| Python.org: Using the Interpreter | https://docs.python.org/3/tutorial/interpreter.html | How to use the REPL and run scripts |
| Automate the Boring Stuff, Ch. 1 | https://automatetheboringstuff.com/2e/chapter1/ | Free; practical and beginner-friendly |
| Real Python: Python Hello World | https://realpython.com/python-first-steps/ | Well-structured beginner walkthrough |

---

## The Zen of Python

| Resource | URL | Notes |
|----------|-----|-------|
| PEP 20 — The Zen of Python | https://peps.python.org/pep-0020/ | Official source; brief and worth reading |
| PEP 8 — Style Guide | https://peps.python.org/pep-0008/ | The Python style guide — read it early |

---

## Understanding Python Versions

| Resource | URL | Notes |
|----------|-----|-------|
| What's New in Python (index) | https://docs.python.org/3/whatsnew/ | Changelogs for every Python version |
| Python 2 vs 3 Guide | https://docs.python.org/3/howto/pyporting.html | Official porting guide |
| Python Developer's Guide | https://devguide.python.org/ | For understanding the development process |

---

*Module 0 resources — for broader Python resources, see [../RESOURCES.md](../RESOURCES.md)*
