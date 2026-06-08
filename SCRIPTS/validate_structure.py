#!/usr/bin/env python3
"""
validate_structure.py - Validate the LEAPS repository structure against conventions.

Checks:
  - Topic-level required files
  - Module-level required files
  - Module directory naming convention (NN_slug)
  - Markdown H1 appears exactly once per file
  - Code blocks have language annotations
  - Wiki-links [[topic]] resolve to existing TOPICS/ directories
  - Internal markdown links resolve to existing files

Returns exit code 1 if any violations are found (use in CI with: python validate_structure.py || exit 1).

Usage:
    python validate_structure.py
    python validate_structure.py --topic python
    python validate_structure.py --fix
    python validate_structure.py --topic rust --fix
"""

import argparse
import re
import sys
from enum import Enum
from pathlib import Path
from typing import Callable

# ---------------------------------------------------------------------------
# Repository layout
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_DIR = REPO_ROOT / "TOPICS"

# ---------------------------------------------------------------------------
# Required files
# ---------------------------------------------------------------------------

TOPIC_REQUIRED_FILES = [
    "README.md",
    "ROADMAP.md",
    "RESOURCES.md",
    "GLOSSARY.md",
    "QUESTIONS.md",
    "PROJECTS.md",
]

MODULE_REQUIRED_FILES = [
    "README.md",
    "NOTES.md",
    "QUESTIONS.md",
    "EXERCISES.md",
    "TEST.md",
    "ANSWERS.md",
    "RESOURCES.md",
]

# Module directory name pattern: "N. Module Name"  e.g. "0. Introduction", "3. Control Flow"
RE_MODULE_NAME = re.compile(r"^\d+\.\s+\S.*$")

# ---------------------------------------------------------------------------
# Violation types
# ---------------------------------------------------------------------------


class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARN "


class Violation:
    """A single structural violation."""

    def __init__(
        self,
        severity: Severity,
        path: Path,
        message: str,
        line: int | None = None,
        fixable: bool = False,
        fix_fn: Callable | None = None,
    ) -> None:
        self.severity = severity
        self.path = path
        self.message = message
        self.line = line
        self.fixable = fixable
        self.fix_fn = fix_fn

    def __str__(self) -> str:
        try:
            rel = self.path.relative_to(REPO_ROOT)
        except ValueError:
            rel = self.path
        location = f"{rel}" + (f":{self.line}" if self.line else "")
        fix_tag = " [fixable]" if self.fixable else ""
        return f"  [{self.severity.value}] {location} — {self.message}{fix_tag}"


# ---------------------------------------------------------------------------
# Individual validators
# ---------------------------------------------------------------------------


def check_topic_required_files(topic_dir: Path) -> list[Violation]:
    """Check that all required topic-level files exist."""
    violations = []
    for fname in TOPIC_REQUIRED_FILES:
        fpath = topic_dir / fname
        if not fpath.exists():
            violations.append(Violation(
                Severity.ERROR,
                topic_dir,
                f"missing required topic file: {fname}",
            ))
    return violations


def check_module_required_files(module_dir: Path) -> list[Violation]:
    """Check that all required module-level files exist.

    If the module directory contains no .md files at all it is treated as an
    unstarted placeholder and only a single WARNING is emitted (not per-file
    ERRORs), so that pre-created skeleton directories don't block CI.
    """
    existing_md = list(module_dir.glob("*.md"))
    if not existing_md:
        return [Violation(
            Severity.WARNING,
            module_dir,
            "module not yet started — no .md files found (placeholder directory)",
        )]
    violations = []
    for fname in MODULE_REQUIRED_FILES:
        fpath = module_dir / fname
        if not fpath.exists():
            violations.append(Violation(
                Severity.ERROR,
                module_dir,
                f"missing required module file: {fname}",
            ))
    return violations


def check_module_naming(module_dir: Path) -> list[Violation]:
    """Check that the module directory name follows the 'N. Module Name' pattern."""
    name = module_dir.name
    if not RE_MODULE_NAME.match(name):
        return [Violation(
            Severity.ERROR,
            module_dir,
            f"module directory '{name}' does not match pattern 'N. Module Name' "
            "(e.g. '0. Introduction', '3. Control Flow')",
        )]
    return []


def _in_code_block(lines: list[str], idx: int) -> bool:
    """Return True if lines[idx] is inside a fenced code block (``` or ~~~)."""
    in_block = False
    fence_char = ""
    for i, line in enumerate(lines):
        if i == idx:
            return in_block
        stripped = line.strip()
        if not in_block:
            m = re.match(r"^(`{3,}|~{3,})", stripped)
            if m:
                in_block = True
                fence_char = m.group(1)[0]
        else:
            if stripped.startswith(fence_char * 3):
                in_block = False
                fence_char = ""
    return in_block


def check_h1_count(md_file: Path) -> list[Violation]:
    """Check that H1 (# heading) appears exactly once in a markdown file.

    Lines inside fenced code blocks are skipped so that Python comments
    like ``# my_var = 1`` do not count as headings.
    """
    try:
        lines = md_file.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []

    h1_lines = [
        i + 1
        for i, line in enumerate(lines)
        if re.match(r"^#\s+\S", line) and not _in_code_block(lines, i)
    ]

    violations = []
    if len(h1_lines) == 0:
        violations.append(Violation(
            Severity.WARNING,
            md_file,
            "no H1 heading found (every file should have exactly one)",
        ))
    elif len(h1_lines) > 1:
        for line_num in h1_lines[1:]:
            violations.append(Violation(
                Severity.WARNING,
                md_file,
                f"multiple H1 headings found; additional H1 at line {line_num}",
                line=line_num,
            ))
    return violations


def check_code_block_annotations(md_file: Path) -> list[Violation]:
    """Check that all fenced code blocks have a language annotation."""
    try:
        lines = md_file.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []

    violations = []
    in_block = False
    fence_char = ""

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not in_block:
            # Opening fence: ``` or ~~~, with or without language
            m = re.match(r"^(`{3,}|~{3,})(.*)", stripped)
            if m:
                fence = m.group(1)
                lang = m.group(2).strip()
                in_block = True
                fence_char = fence[0]
                if not lang:
                    violations.append(Violation(
                        Severity.WARNING,
                        md_file,
                        "code block missing language annotation (e.g. ```python)",
                        line=i,
                    ))
        else:
            # Closing fence
            if stripped.startswith(fence_char * 3):
                in_block = False
                fence_char = ""

    return violations


def check_wiki_links(md_file: Path, topics_dir: Path) -> list[Violation]:
    """
    Check that [[wiki-links]] in a file resolve to existing topics or topic/module paths.
    Format: [[topic]] or [[topic/module]] or [[topic#section]] or [[shared/...]]
    """
    try:
        text = md_file.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
    except OSError:
        return []

    violations = []
    # Match [[anything]] — but not [[!image]] (Obsidian image embeds)
    RE_WIKI = re.compile(r"\[\[([^\]!][^\]]*)\]\]")

    for line_num, line in enumerate(lines, start=1):
        if _in_code_block(lines, line_num - 1):
            continue
        for m in RE_WIKI.finditer(line):
            raw = m.group(1).strip()
            # Strip section anchor
            if "#" in raw:
                raw = raw.split("#")[0].strip()
            if not raw:
                continue

            # Skip placeholder-style links like [[{{PREREQ_TOPIC_1}}]]
            if "{{" in raw or "}}" in raw:
                continue

            # Skip shared/ links (SHARED/ directory)
            if raw.startswith("shared/"):
                shared_path = REPO_ROOT / "SHARED" / raw[7:]
                if not shared_path.exists() and not (REPO_ROOT / "SHARED" / (raw[7:] + ".md")).exists():
                    violations.append(Violation(
                        Severity.WARNING,
                        md_file,
                        f"wiki-link [[{m.group(1)}]] → SHARED/{raw[7:]} not found",
                        line=line_num,
                    ))
                continue

            # Could be topic or topic/module
            parts = raw.split("/")
            topic_slug = parts[0]
            topic_dir = topics_dir / topic_slug

            if not topic_dir.exists():
                # Check case-insensitive match
                existing = [d.name for d in topics_dir.iterdir() if d.is_dir()] if topics_dir.exists() else []
                suggestion = next((e for e in existing if e.lower() == topic_slug.lower()), None)
                fix_note = f" (did you mean [[{suggestion}]]?)" if suggestion else ""
                violations.append(Violation(
                    Severity.WARNING,
                    md_file,
                    f"wiki-link [[{m.group(1)}]] → TOPICS/{topic_slug}/ not found{fix_note}",
                    line=line_num,
                ))
            elif len(parts) > 1:
                # Check module subdirectory
                module_slug = parts[1]
                # Module dirs may be under topic/modules/ or directly under topic/
                found = False
                for candidate in (topic_dir / module_slug, topic_dir / "modules" / module_slug):
                    if candidate.exists():
                        found = True
                        break
                # Also check with numeric prefix
                if not found and (topic_dir / "modules").exists():
                    for d in (topic_dir / "modules").iterdir():
                        if d.is_dir() and (d.name == module_slug or d.name.endswith(f"_{module_slug}")):
                            found = True
                            break
                if not found:
                    violations.append(Violation(
                        Severity.WARNING,
                        md_file,
                        f"wiki-link [[{m.group(1)}]] → TOPICS/{topic_slug}/{module_slug} not found",
                        line=line_num,
                    ))

    return violations


def check_internal_links(md_file: Path) -> list[Violation]:
    """
    Check that relative markdown links [text](path) resolve to existing files.
    Only checks relative paths (not http:// etc.).
    URL-encoded paths (e.g. spaces as %20) are decoded before resolution.
    """
    from urllib.parse import unquote

    try:
        text = md_file.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
    except OSError:
        return []

    RE_LINK = re.compile(r"\[(?:[^\]]*)\]\(([^)]+)\)")
    violations = []

    for line_num, line in enumerate(lines, start=1):
        if _in_code_block(lines, line_num - 1):
            continue
        for m in RE_LINK.finditer(line):
            href = m.group(1).strip()
            # Skip anchors-only, external URLs, and mailto
            if href.startswith(("http://", "https://", "mailto:", "#", "ftp:")):
                continue
            # Strip anchor fragment
            if "#" in href:
                href = href.split("#")[0]
            if not href:
                continue
            # URL-decode (e.g. spaces encoded as %20)
            href = unquote(href)
            # Resolve relative to the file's directory
            target = (md_file.parent / href).resolve()
            if not target.exists():
                violations.append(Violation(
                    Severity.WARNING,
                    md_file,
                    f"broken relative link: ({m.group(1)}) → {target} not found",
                    line=line_num,
                ))

    return violations


# ---------------------------------------------------------------------------
# Auto-fix helpers
# ---------------------------------------------------------------------------


def fix_code_block_annotations(md_file: Path) -> int:
    """Add 'text' as language annotation to unannotated code blocks. Returns count of fixes."""
    try:
        content = md_file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0

    def add_lang(match: re.Match) -> str:
        fence = match.group(1)
        rest = match.group(2)
        if not rest.strip():
            return f"{fence}text"
        return match.group(0)

    new_content, count = re.subn(r"^(`{3,}|~{3,})([ \t]*)$", add_lang, content, flags=re.MULTILINE)
    if count > 0:
        md_file.write_text(new_content, encoding="utf-8")
    return count


def fix_missing_topic_files(topic_dir: Path) -> list[str]:
    """Create stub files for any missing required topic files. Returns list of created filenames."""
    created = []
    topic_name = " ".join(w.capitalize() for w in topic_dir.name.split("-"))
    stubs = {
        "GLOSSARY.md": f"# {topic_name} — Glossary\n\n_(add terms here)_\n",
        "QUESTIONS.md": f"# {topic_name} — Questions\n\n_(log questions here)_\n",
        "RESOURCES.md": f"# {topic_name} — Resources\n\n_(add resources here)_\n",
        "PROJECTS.md": f"# {topic_name} — Projects\n\n_(add project ideas here)_\n",
        "ROADMAP.md": f"# {topic_name} — Roadmap\n\n_(define learning phases here)_\n",
    }
    for fname in TOPIC_REQUIRED_FILES:
        fpath = topic_dir / fname
        if not fpath.exists() and fname in stubs:
            fpath.write_text(stubs[fname], encoding="utf-8")
            created.append(fname)
    return created


def fix_missing_module_files(module_dir: Path) -> list[str]:
    """Create stub files for any missing required module files. Returns list of created filenames."""
    created = []
    module_name = module_dir.name
    stubs = {
        "README.md": f"# {module_name}\n\n> [!NOTE] This module is a placeholder. Content coming soon.\n\n_(Run: \"Generate module for [topic] — {module_name}\" to expand this module with AI assistance.)_\n",
        "NOTES.md": f"# Notes — {module_name}\n\n_(add study notes here)_\n",
        "QUESTIONS.md": f"# Questions — {module_name}\n\n_(log questions here)_\n",
        "EXERCISES.md": f"# Exercises — {module_name}\n\n_(add exercises here)_\n",
        "TEST.md": f"# Test — {module_name}\n\n_(test questions here)_\n",
        "ANSWERS.md": f"# Answers — {module_name}\n\n_(answer key here)_\n",
        "RESOURCES.md": f"# Resources — {module_name}\n\n_(add resources here)_\n",
    }
    for fname in MODULE_REQUIRED_FILES:
        fpath = module_dir / fname
        if not fpath.exists() and fname in stubs:
            fpath.write_text(stubs[fname], encoding="utf-8")
            created.append(fname)
    return created


# ---------------------------------------------------------------------------
# Topic / module discovery
# ---------------------------------------------------------------------------


# Directories inside a topic root that are NOT module directories
_TOPIC_NON_MODULE_DIRS = {
    "labs", "assets", "environments", "archive",
    "code", "exercises", "tests", "notes", "references",
    "simulations", "tools", "docs", "diagrams", "datasets",
}


def find_module_dirs(topic_dir: Path) -> list[Path]:
    """Return all module directories for a topic.

    A module directory is any non-hidden subdirectory whose name starts with a
    digit followed by a period (matching RE_MODULE_NAME), OR any subdirectory
    that is not in the known non-module set.  The latter fallback is kept for
    backwards compatibility but will emit naming violations.
    """
    modules_dir = topic_dir / "modules"
    if modules_dir.is_dir():
        return sorted(
            d for d in modules_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        )
    # Directories that match the numbering pattern are always modules.
    # Remaining directories not in the exclusion set are also considered
    # (so they'll get naming violations and prompt the user to fix them).
    return sorted(
        d for d in topic_dir.iterdir()
        if d.is_dir()
        and not d.name.startswith(".")
        and d.name not in _TOPIC_NON_MODULE_DIRS
    )


def find_all_md_files(topic_dir: Path) -> list[Path]:
    """Return all .md files under a topic directory."""
    return sorted(topic_dir.rglob("*.md"))


# ---------------------------------------------------------------------------
# Main validation runner
# ---------------------------------------------------------------------------


def validate_topic(topic_dir: Path, fix: bool = False) -> list[Violation]:
    """Run all checks on a single topic and return violations."""
    violations: list[Violation] = []

    # 1. Topic-level required files
    v = check_topic_required_files(topic_dir)
    if fix and v:
        created = fix_missing_topic_files(topic_dir)
        if created:
            print(f"    [FIX] Created stub files: {', '.join(created)}")
        # Re-check after fix
        v = check_topic_required_files(topic_dir)
    violations.extend(v)

    # 2. Module directories
    module_dirs = find_module_dirs(topic_dir)
    for mod_dir in module_dirs:
        # Module naming
        violations.extend(check_module_naming(mod_dir))

        # Module required files
        v = check_module_required_files(mod_dir)
        if fix and v:
            created = fix_missing_module_files(mod_dir)
            if created:
                print(f"    [FIX] {mod_dir.name}: created stub files: {', '.join(created)}")
            v = check_module_required_files(mod_dir)
        violations.extend(v)

    # 3. Markdown content checks on all .md files
    for md_file in find_all_md_files(topic_dir):
        violations.extend(check_h1_count(md_file))

        v = check_code_block_annotations(md_file)
        if fix and v:
            count = fix_code_block_annotations(md_file)
            if count:
                print(f"    [FIX] {md_file.name}: annotated {count} code block(s) with 'text'")
            v = check_code_block_annotations(md_file)
        violations.extend(v)

        violations.extend(check_wiki_links(md_file, TOPICS_DIR))
        violations.extend(check_internal_links(md_file))

    return violations


def validate_all(fix: bool = False) -> list[Violation]:
    """Validate all topics in TOPICS/."""
    if not TOPICS_DIR.exists():
        return [Violation(
            Severity.ERROR,
            TOPICS_DIR,
            "TOPICS/ directory does not exist",
        )]

    all_violations: list[Violation] = []
    topic_dirs = sorted(
        d for d in TOPICS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )

    if not topic_dirs:
        print("  No topics found under TOPICS/. Nothing to validate.")
        return []

    for topic_dir in topic_dirs:
        print(f"  Checking TOPICS/{topic_dir.name}/...")
        v = validate_topic(topic_dir, fix=fix)
        all_violations.extend(v)

    return all_violations


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def print_violations(violations: list[Violation]) -> None:
    if not violations:
        return

    errors = [v for v in violations if v.severity == Severity.ERROR]
    warnings = [v for v in violations if v.severity == Severity.WARNING]

    if errors:
        print()
        print("  Errors:")
        for v in errors:
            print(str(v))

    if warnings:
        print()
        print("  Warnings:")
        for v in warnings:
            print(str(v))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="validate_structure.py",
        description="Validate the LEAPS repository structure against conventions.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--topic",
        metavar="TOPIC",
        default=None,
        help="Validate only one specific topic (e.g. --topic python).",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help=(
            "Attempt to auto-fix simple issues: "
            "create missing stub files, annotate bare code blocks."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not TOPICS_DIR.exists():
        print(f"ERROR: TOPICS/ not found at {TOPICS_DIR}", file=sys.stderr)
        return 1

    print()
    print("  LEAPS Structure Validator")
    print("  " + "─" * 50)
    print()

    if args.topic:
        slug = args.topic.strip().lower()
        topic_dir = TOPICS_DIR / slug
        if not topic_dir.exists():
            print(f"ERROR: Topic '{slug}' not found at {topic_dir}", file=sys.stderr)
            return 1
        print(f"  Checking TOPICS/{slug}/...")
        violations = validate_topic(topic_dir, fix=args.fix)
    else:
        violations = validate_all(fix=args.fix)

    print_violations(violations)

    errors = [v for v in violations if v.severity == Severity.ERROR]
    warnings = [v for v in violations if v.severity == Severity.WARNING]

    print()
    if not violations:
        print("  All checks passed. Repository structure is valid.")
        print()
        return 0

    fixable = [v for v in violations if v.fixable]
    print(
        f"  {len(violations)} violation(s) found: "
        f"{len(errors)} error(s), {len(warnings)} warning(s)"
        + (f", {len(fixable)} auto-fixable" if fixable else "")
        + "."
    )
    if not args.fix and any(v.fixable for v in violations):
        print("  Run with --fix to auto-fix simple issues.")
    print()

    # Exit code: 1 if any errors, 0 if only warnings
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
