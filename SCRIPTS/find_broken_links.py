#!/usr/bin/env python3
"""
find_broken_links.py - Find broken internal links in LEAPS markdown files.

Scans all markdown files for:
  - [text](relative/path) style links
  - [[wiki-link]] style links (Obsidian-compatible)

For each link, resolves the target relative to the file's location and checks
whether it exists. Reports broken links with file, line number, and a suggested fix.

Wiki-link resolution:
  [[topic]]           → TOPICS/{topic}/
  [[topic/module]]    → TOPICS/{topic}/{module}/ or TOPICS/{topic}/modules/{module}/
  [[shared/term]]     → SHARED/{term}.md or SHARED/{term}/
  [[topic#section]]   → TOPICS/{topic}/ (section not verified)

Usage:
    python find_broken_links.py
    python find_broken_links.py --dir TOPICS/python/
    python find_broken_links.py --fix
"""

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Repository layout
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_DIR = REPO_ROOT / "TOPICS"
SHARED_DIR = REPO_ROOT / "SHARED"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


class BrokenLink(NamedTuple):
    file: Path
    line: int
    raw: str            # The raw link text as it appears in the file
    kind: str           # "markdown" or "wiki"
    target: Path | None # Resolved target (may be None for unresolvable)
    suggestion: str     # Human-readable fix suggestion


# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# [text](href) — capture href group
RE_MD_LINK = re.compile(r"\[(?:[^\]]*)\]\(([^)]+)\)")
# [[anything]] — wiki link
RE_WIKI_LINK = re.compile(r"\[\[([^\]!][^\]]*)\]\]")


# ---------------------------------------------------------------------------
# Link resolution
# ---------------------------------------------------------------------------


def resolve_markdown_link(href: str, source_file: Path) -> tuple[bool, Path | None]:
    """
    Check whether a relative markdown link resolves to an existing target.
    Returns (exists, resolved_path).
    Absolute paths and external URLs are considered valid (True, None).
    """
    if href.startswith(("http://", "https://", "ftp://", "mailto:", "//")):
        return True, None  # External link: skip

    # Strip anchor
    anchor = ""
    if "#" in href:
        href, anchor = href.split("#", 1)

    if not href:
        # Anchor-only link — always considered valid for our purposes
        return True, None

    resolved = (source_file.parent / href).resolve()

    if resolved.exists():
        return True, resolved

    # Try adding .md extension if no extension given
    if not resolved.suffix and (resolved.with_suffix(".md")).exists():
        return True, resolved.with_suffix(".md")

    return False, resolved


def resolve_wiki_link(raw: str) -> tuple[bool, Path | None, str]:
    """
    Check whether a wiki-link resolves to an existing target.
    Returns (exists, resolved_path, suggestion).
    """
    # Strip section anchor
    text = raw.strip()
    if "#" in text:
        text = text.split("#")[0].strip()

    if not text:
        return True, None, ""

    # Template placeholder — skip
    if "{{" in text:
        return True, None, ""

    parts = text.split("/")
    first = parts[0].strip()

    # [[shared/...]] → SHARED/
    if first.lower() == "shared":
        if len(parts) < 2:
            target = SHARED_DIR
            return SHARED_DIR.exists(), SHARED_DIR, f"Create SHARED/ directory"
        sub = "/".join(parts[1:])
        for candidate in (
            SHARED_DIR / sub,
            SHARED_DIR / (sub + ".md"),
            SHARED_DIR / sub.replace("-", "_"),
        ):
            if candidate.exists():
                return True, candidate, ""
        suggestion = f"Create SHARED/{sub}.md or SHARED/{sub}/"
        return False, SHARED_DIR / sub, suggestion

    # [[topic]] or [[topic/module]]
    topic_dir = TOPICS_DIR / first
    if not topic_dir.exists():
        # Case-insensitive match
        if TOPICS_DIR.exists():
            match = next(
                (d for d in TOPICS_DIR.iterdir() if d.is_dir() and d.name.lower() == first.lower()),
                None,
            )
            if match:
                return False, topic_dir, f"Check capitalisation: [[{match.name}{'/' + '/'.join(parts[1:]) if len(parts) > 1 else ''}]]"
        return False, topic_dir, f"Create TOPICS/{first}/ (run: python SCRIPTS/new_topic.py {first})"

    if len(parts) == 1:
        return True, topic_dir, ""

    # [[topic/module]]
    module_slug = parts[1].strip()
    candidates = [
        topic_dir / module_slug,
        topic_dir / "modules" / module_slug,
    ]
    # Also try matching on trailing part of directory name (e.g. 00_introduction matches introduction)
    if (topic_dir / "modules").exists():
        for d in (topic_dir / "modules").iterdir():
            if d.is_dir() and (
                d.name == module_slug
                or d.name.endswith(f"_{module_slug}")
                or d.name.endswith(f"-{module_slug}")
            ):
                candidates.append(d)

    for c in candidates:
        if c.exists():
            return True, c, ""

    suggestion = f"Create TOPICS/{first}/modules/{module_slug}/ or check slug spelling"
    return False, topic_dir / "modules" / module_slug, suggestion


# ---------------------------------------------------------------------------
# File scanning
# ---------------------------------------------------------------------------


def is_in_code_block(lines: list[str], line_idx: int) -> bool:
    """Return True if lines[line_idx] is inside a fenced code block."""
    in_block = False
    fence_char = ""
    for i, line in enumerate(lines):
        if i == line_idx:
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


def scan_file(path: Path) -> list[BrokenLink]:
    """Scan a single markdown file for broken links."""
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    lines = content.splitlines()
    broken: list[BrokenLink] = []

    for line_num, line in enumerate(lines, start=1):
        # Skip lines inside code blocks
        if is_in_code_block(lines, line_num - 1):
            continue

        # --- Standard markdown links ---
        for m in RE_MD_LINK.finditer(line):
            href = m.group(1).strip()
            exists, resolved = resolve_markdown_link(href, path)
            if not exists and resolved is not None:
                try:
                    rel_target = resolved.relative_to(REPO_ROOT)
                except ValueError:
                    rel_target = resolved
                broken.append(BrokenLink(
                    file=path,
                    line=line_num,
                    raw=m.group(0),
                    kind="markdown",
                    target=resolved,
                    suggestion=f"Target not found: {rel_target}",
                ))

        # --- Wiki links ---
        for m in RE_WIKI_LINK.finditer(line):
            raw = m.group(1)
            # Skip template placeholders
            if "{{" in raw:
                continue
            exists, resolved, suggestion = resolve_wiki_link(raw)
            if not exists:
                broken.append(BrokenLink(
                    file=path,
                    line=line_num,
                    raw=m.group(0),
                    kind="wiki",
                    target=resolved,
                    suggestion=suggestion,
                ))

    return broken


def scan_directory(root: Path) -> list[BrokenLink]:
    """Scan all .md files under root and return all broken links."""
    all_broken: list[BrokenLink] = []
    for md_file in sorted(root.rglob("*.md")):
        # Skip hidden paths
        if any(part.startswith(".") for part in md_file.parts):
            continue
        all_broken.extend(scan_file(md_file))
    return all_broken


# ---------------------------------------------------------------------------
# Interactive fix
# ---------------------------------------------------------------------------


def interactive_fix(broken: list[BrokenLink]) -> None:
    """Interactively prompt the user to fix each broken link."""
    print()
    print("  Interactive fix mode. Press Enter to skip, 'q' to quit.")
    print()

    for bl in broken:
        try:
            rel_file = bl.file.relative_to(REPO_ROOT)
        except ValueError:
            rel_file = bl.file

        print(f"  File:   {rel_file}:{bl.line}")
        print(f"  Link:   {bl.raw}")
        print(f"  Hint:   {bl.suggestion}")
        new_link = input("  Fix to: ").strip()

        if new_link.lower() == "q":
            print("  Quitting fix mode.")
            break

        if not new_link:
            print("  Skipped.")
            print()
            continue

        # Apply fix: replace the broken link text in the file
        try:
            content = bl.file.read_text(encoding="utf-8", errors="replace")
            new_content = content.replace(bl.raw, new_link, 1)
            if new_content == content:
                print("  Warning: link not found in file (may have been fixed already).")
            else:
                bl.file.write_text(new_content, encoding="utf-8")
                print(f"  Fixed in {rel_file}")
        except OSError as e:
            print(f"  Error applying fix: {e}")

        print()


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def print_broken_links(broken: list[BrokenLink]) -> None:
    current_file: Path | None = None

    for bl in broken:
        try:
            rel = bl.file.relative_to(REPO_ROOT)
        except ValueError:
            rel = bl.file

        if bl.file != current_file:
            print()
            print(f"  {rel}")
            current_file = bl.file

        kind_tag = f"[{bl.kind}]"
        print(f"    line {bl.line:<5} {kind_tag:<10} {bl.raw}")
        if bl.suggestion:
            print(f"             → {bl.suggestion}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="find_broken_links.py",
        description="Find broken internal markdown and wiki-links in the LEAPS repository.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--dir",
        metavar="DIR",
        default=None,
        help=f"Directory to scan (default: {REPO_ROOT}). Use to limit to a subtree.",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Interactively prompt to fix each broken link.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    scan_root = Path(args.dir).resolve() if args.dir else REPO_ROOT
    if not scan_root.exists():
        print(f"ERROR: '{scan_root}' does not exist.", file=sys.stderr)
        return 2

    print()
    print("  LEAPS — Broken Link Checker")
    print("  " + "─" * 50)
    print(f"  Scanning: {scan_root}")
    print()

    broken = scan_directory(scan_root)

    if not broken:
        print("  No broken links found.")
        print()
        return 0

    print_broken_links(broken)

    print()
    print(f"  {len(broken)} broken link(s) found.")

    if args.fix:
        interactive_fix(broken)
    else:
        print("  Run with --fix to interactively repair broken links.")

    print()
    return 1


if __name__ == "__main__":
    sys.exit(main())
