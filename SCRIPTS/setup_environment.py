#!/usr/bin/env python3
"""
setup_environment.py - Set up the LEAPS learning environment.

Performs a one-time setup of the LEAPS repository:
  1. Checks Python version (>= 3.10 required)
  2. Checks for required tools: git, jupyter (optional)
  3. Creates TOPICS/ directory if it doesn't exist
  4. Creates a .env template file
  5. Installs Python dependencies from TEMPLATES/environment/requirements.txt (if present)
  6. Installs pre-commit hooks (if .git exists and pre-commit is available)
  7. Prints a welcome message and quick-start guide

Usage:
    python setup_environment.py
    python setup_environment.py --check-only
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Repository layout
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_DIR = REPO_ROOT / "TOPICS"
TEMPLATES_DIR = REPO_ROOT / "TEMPLATES"
SCRIPTS_DIR = REPO_ROOT / "SCRIPTS"
GIT_DIR = REPO_ROOT / ".git"
ENV_FILE = REPO_ROOT / ".env"
HOOKS_DIR = GIT_DIR / "hooks"
REQUIREMENTS_FILE = TEMPLATES_DIR / "environment" / "requirements.txt"

# Minimum Python version
MIN_PYTHON = (3, 10)

# ---------------------------------------------------------------------------
# Result tracking
# ---------------------------------------------------------------------------


class CheckResult:
    def __init__(self, name: str) -> None:
        self.name = name
        self.passed: bool = False
        self.message: str = ""
        self.fixed: bool = False

    def ok(self, msg: str = "") -> "CheckResult":
        self.passed = True
        self.message = msg
        return self

    def fail(self, msg: str) -> "CheckResult":
        self.passed = False
        self.message = msg
        return self

    def fix(self, msg: str) -> "CheckResult":
        self.passed = True
        self.fixed = True
        self.message = msg
        return self


# ---------------------------------------------------------------------------
# Check functions
# ---------------------------------------------------------------------------


def check_python_version() -> CheckResult:
    r = CheckResult("Python version")
    major, minor = sys.version_info[:2]
    ver_str = f"{major}.{minor}.{sys.version_info.micro}"
    if (major, minor) >= MIN_PYTHON:
        return r.ok(f"Python {ver_str} (>= {MIN_PYTHON[0]}.{MIN_PYTHON[1]} required)")
    return r.fail(
        f"Python {ver_str} is too old. "
        f"LEAPS requires Python >= {MIN_PYTHON[0]}.{MIN_PYTHON[1]}."
    )


def check_git() -> CheckResult:
    r = CheckResult("git")
    git_path = shutil.which("git")
    if git_path:
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True, text=True, timeout=5
            )
            ver = result.stdout.strip()
            return r.ok(f"{ver} at {git_path}")
        except Exception:
            return r.ok(f"found at {git_path}")
    return r.fail("git not found in PATH. Install git: https://git-scm.com/")


def check_git_repo() -> CheckResult:
    r = CheckResult("git repository")
    if GIT_DIR.exists():
        return r.ok(f".git/ found at {GIT_DIR}")
    return r.fail(
        f"No .git/ directory found at {REPO_ROOT}. "
        "Is this directory a git repository? Run 'git init' if needed."
    )


def check_jupyter() -> CheckResult:
    r = CheckResult("Jupyter (optional)")
    jupyter_path = shutil.which("jupyter")
    if jupyter_path:
        try:
            result = subprocess.run(
                ["jupyter", "--version"],
                capture_output=True, text=True, timeout=5
            )
            # Get the first version line
            first_line = result.stdout.strip().splitlines()[0] if result.stdout.strip() else "installed"
            return r.ok(f"Jupyter {first_line} at {jupyter_path}")
        except Exception:
            return r.ok(f"found at {jupyter_path}")
    return r.fail(
        "Jupyter not found. Install with: pip install jupyter\n"
        "         (Not required for text-only topics.)"
    )


def check_or_create_topics_dir(check_only: bool = False) -> CheckResult:
    r = CheckResult("TOPICS/ directory")
    if TOPICS_DIR.exists():
        topic_count = sum(1 for d in TOPICS_DIR.iterdir() if d.is_dir() and not d.name.startswith("."))
        return r.ok(f"{TOPICS_DIR} ({topic_count} topic(s))")
    if check_only:
        return r.fail(f"{TOPICS_DIR} does not exist (run without --check-only to create it)")
    TOPICS_DIR.mkdir(parents=True, exist_ok=True)
    return r.fix(f"Created {TOPICS_DIR}")


def check_or_create_env_file(check_only: bool = False) -> CheckResult:
    r = CheckResult(".env file")
    if ENV_FILE.exists():
        return r.ok(f"{ENV_FILE} already exists")
    if check_only:
        return r.fail(f"{ENV_FILE} not found (run without --check-only to create it)")

    env_content = """\
# LEAPS Environment Configuration
# Copy this file to .env and fill in values as needed.
# This file is NOT tracked by git (add .env to .gitignore).

# Optional: AI provider API key for agent integration
# ANTHROPIC_API_KEY=sk-ant-...
# OPENAI_API_KEY=sk-...

# Optional: Default difficulty for new topics
# LEAPS_DEFAULT_DIFFICULTY=beginner

# Optional: Override TOPICS directory path
# LEAPS_TOPICS_DIR=/path/to/topics
"""
    try:
        ENV_FILE.write_text(env_content, encoding="utf-8")
        return r.fix(f"Created {ENV_FILE}")
    except OSError as e:
        return r.fail(f"Could not create {ENV_FILE}: {e}")


def check_or_install_requirements(check_only: bool = False) -> CheckResult:
    r = CheckResult("Python requirements")
    if not REQUIREMENTS_FILE.exists():
        return r.ok("No requirements.txt found in TEMPLATES/environment/ — skipping")

    # Check if pip is available
    pip_path = shutil.which("pip") or shutil.which("pip3")
    if not pip_path:
        return r.fail("pip not found in PATH")

    if check_only:
        return r.ok(f"Requirements file: {REQUIREMENTS_FILE} (run without --check-only to install)")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE), "--quiet"],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode == 0:
            return r.fix(f"Installed packages from {REQUIREMENTS_FILE}")
        return r.fail(f"pip install failed:\n{result.stderr[:300]}")
    except subprocess.TimeoutExpired:
        return r.fail("pip install timed out after 120 seconds")
    except Exception as e:
        return r.fail(f"Failed to run pip: {e}")


def check_gitignore() -> CheckResult:
    r = CheckResult(".gitignore")
    gitignore = REPO_ROOT / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text(encoding="utf-8", errors="replace")
        has_env = ".env" in content
        has_pycache = "__pycache__" in content
        missing = []
        if not has_env:
            missing.append(".env")
        if not has_pycache:
            missing.append("__pycache__")
        if missing:
            return r.fail(
                f".gitignore missing recommended entries: {', '.join(missing)}"
            )
        return r.ok(".gitignore present and looks good")
    return r.fail(f".gitignore not found at {REPO_ROOT / '.gitignore'}")


def check_or_install_pre_commit(check_only: bool = False) -> CheckResult:
    r = CheckResult("pre-commit hooks (optional)")
    if not GIT_DIR.exists():
        return r.fail(".git/ not found — skipping pre-commit setup")

    pre_commit_path = shutil.which("pre-commit")
    if not pre_commit_path:
        return r.ok(
            "pre-commit not installed — skipping hook setup. "
            "Install with: pip install pre-commit"
        )

    pre_commit_config = REPO_ROOT / ".pre-commit-config.yaml"
    if not pre_commit_config.exists():
        return r.ok("No .pre-commit-config.yaml found — skipping hook install")

    if check_only:
        return r.ok("pre-commit available (run without --check-only to install hooks)")

    try:
        result = subprocess.run(
            ["pre-commit", "install"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        if result.returncode == 0:
            return r.fix("pre-commit hooks installed")
        return r.fail(f"pre-commit install failed: {result.stderr[:200]}")
    except Exception as e:
        return r.fail(f"Failed to install pre-commit hooks: {e}")


def check_scripts_executable() -> CheckResult:
    r = CheckResult("Script permissions")
    if os.name == "nt":
        return r.ok("Windows detected — file permissions not applicable")

    non_executable = []
    for script in SCRIPTS_DIR.glob("*.py"):
        if not os.access(script, os.X_OK):
            non_executable.append(script.name)

    if non_executable:
        return r.fail(
            f"{len(non_executable)} script(s) not executable. "
            f"Run: chmod +x SCRIPTS/*.py"
        )
    return r.ok("All .py scripts are executable")


# ---------------------------------------------------------------------------
# Printing helpers
# ---------------------------------------------------------------------------

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def _supports_color() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def colored(text: str, color: str) -> str:
    if _supports_color():
        return f"{color}{text}{RESET}"
    return text


def print_check(result: CheckResult) -> None:
    if result.fixed:
        icon = colored("[FIXED]", YELLOW)
    elif result.passed:
        icon = colored("[  OK ]", GREEN)
    else:
        icon = colored("[FAIL ]", RED)

    # Align name
    name = f"{result.name}".ljust(30)
    print(f"  {icon}  {name}  {result.message}")


def print_welcome() -> None:
    print()
    print(colored("  ╔══════════════════════════════════════════════════════╗", BLUE))
    print(colored("  ║   LEAPS — Learning Environment for Any Progressive  ║", BLUE))
    print(colored("  ║                    Subject                           ║", BLUE))
    print(colored("  ╚══════════════════════════════════════════════════════╝", BLUE))
    print()


def print_quickstart() -> None:
    print()
    print(colored("  Quick Start Guide", BOLD))
    print("  " + "─" * 50)
    print()
    print("  1. Create your first topic:")
    print("       python SCRIPTS/new_topic.py python \\")
    print('         --description "Python programming language" \\')
    print("         --difficulty beginner")
    print()
    print("  2. Validate the structure:")
    print("       python SCRIPTS/validate_structure.py")
    print()
    print("  3. Check your progress:")
    print("       python SCRIPTS/progress_report.py")
    print()
    print("  4. Generate a knowledge graph:")
    print("       python SCRIPTS/knowledge_graph.py --format markdown")
    print()
    print("  5. Set up spaced repetition:")
    print("       python SCRIPTS/spaced_repetition.py")
    print()
    print("  All scripts support --help for full usage details.")
    print()
    print("  Documentation: SCRIPTS/README.md")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="setup_environment.py",
        description="Set up the LEAPS learning environment.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Run checks only without making any changes.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    check_only = args.check_only

    print_welcome()

    mode = "Check mode — no changes will be made." if check_only else "Setup mode"
    print(f"  {mode}")
    print(f"  Repository root: {REPO_ROOT}")
    print()
    print("  Running checks...")
    print()

    results = [
        check_python_version(),
        check_git(),
        check_git_repo(),
        check_jupyter(),
        check_or_create_topics_dir(check_only),
        check_or_create_env_file(check_only),
        check_gitignore(),
        check_or_install_requirements(check_only),
        check_or_install_pre_commit(check_only),
        check_scripts_executable(),
    ]

    for r in results:
        print_check(r)

    # Summary
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    fixed = sum(1 for r in results if r.fixed)

    print()
    print("  " + "─" * 50)
    print(
        f"  Results: {passed} passed"
        + (f", {fixed} fixed" if fixed else "")
        + (f", {failed} failed" if failed else "")
    )

    if failed == 0:
        print()
        print(colored("  Environment is ready!", GREEN))
        print_quickstart()
        return 0

    # Show failures
    print()
    print(colored("  Action required:", RED))
    for r in results:
        if not r.passed:
            print(f"  • {r.name}: {r.message}")
    print()

    critical_failures = [r for r in results if not r.passed and r.name in ("Python version", "git")]
    if critical_failures:
        print(colored("  Critical issues found. Fix them before using LEAPS.", RED))
        print()
        return 1

    # Non-critical failures (jupyter, pre-commit, etc.)
    print("  Non-critical issues found. LEAPS will still work, but some features may be limited.")
    print_quickstart()
    return 0


if __name__ == "__main__":
    sys.exit(main())
