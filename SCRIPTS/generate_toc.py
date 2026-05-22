#!/usr/bin/env python3
"""
generate_toc.py - Generate or update Table of Contents in markdown files.

Parses headings (##, ###, ####) and inserts/updates a TOC between
<!-- TOC --> and <!-- /TOC --> markers. If no markers exist, inserts
after the first H1. Files containing <!-- NO-TOC --> are skipped.

Generates GitHub-compatible anchor links:
  - Lowercase
  - Spaces replaced with hyphens
  - Most non-alphanumeric characters removed (except hyphens)

Usage:
    python generate_toc.py README.md
    python generate_toc.py README.md --dry-run
    python generate_toc.py --dir TOPICS/python/
    python generate_toc.py --dir . --dry-run
"""

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TOC_START = "<!-- TOC -->"
TOC_END = "<!-- /TOC -->"
NO_TOC_MARKER = "<!-- NO-TOC -->"

REPO_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


class Heading(NamedTuple):
    level: int        # 2 = ##, 3 = ###, 4 = ####
    text: str         # Raw text of the heading (no #s)
    anchor: str       # GitHub-compatible anchor slug
    line: int         # 1-based line number


# ---------------------------------------------------------------------------
# Anchor generation
# ---------------------------------------------------------------------------

# Characters that GitHub strips from anchors
_RE_STRIP = re.compile(r"[^\w\s\-]", re.UNICODE)
# Collapse multiple hyphens/spaces
_RE_COLLAPSE = re.compile(r"[\s_]+")


def make_anchor(heading_text: str) -> str:
    """
    Generate a GitHub-compatible anchor slug from a heading string.

    Rules (matching GitHub's implementation):
    1. Convert to lowercase
    2. Remove everything that is not a word character, space, or hyphen
    3. Replace spaces (and underscores) with hyphens
    4. Collapse consecutive hyphens to one
    """
    text = heading_text.strip()
    # Strip inline code markers
    text = re.sub(r"`[^`]*`", lambda m: m.group(0)[1:-1], text)
    # Strip bold/italic markers
    text = re.sub(r"\*+|_+", "", text)
    # Strip link syntax [text](url) → text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Strip image syntax
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)

    text = text.lower()
    text = _RE_STRIP.sub("", text)
    text = _RE_COLLAPSE.sub("-", text)
    text = text.strip("-")
    return text


# ---------------------------------------------------------------------------
# Heading extraction
# ---------------------------------------------------------------------------


def extract_headings(lines: list[str], min_level: int = 2, max_level: int = 4) -> list[Heading]:
    """
    Extract all headings from markdown lines at the specified levels.
    Skips headings inside fenced code blocks.
    """
    headings: list[Heading] = []
    in_code_block = False
    fence_char = ""

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Track fenced code blocks
        if not in_code_block:
            m = re.match(r"^(`{3,}|~{3,})", stripped)
            if m:
                in_code_block = True
                fence_char = m.group(1)[0]
                continue
        else:
            if stripped.startswith(fence_char * 3):
                in_code_block = False
                fence_char = ""
            continue

        # Match ATX headings only (# ## ### etc.)
        m = re.match(r"^(#{1,6})\s+(.+?)(?:\s+#+\s*)?$", line)
        if m:
            level = len(m.group(1))
            if min_level <= level <= max_level:
                text = m.group(2).strip()
                headings.append(Heading(
                    level=level,
                    text=text,
                    anchor=make_anchor(text),
                    line=i,
                ))

    return headings


# ---------------------------------------------------------------------------
# TOC generation
# ---------------------------------------------------------------------------


def generate_toc_lines(headings: list[Heading], base_level: int = 2) -> list[str]:
    """
    Generate TOC markdown lines from a list of headings.
    base_level headings get no indent; each level deeper adds 2 spaces.
    """
    if not headings:
        return []

    lines = []
    # Track duplicate anchors and append -N suffix as GitHub does
    anchor_counts: dict[str, int] = {}

    for h in headings:
        anchor = h.anchor
        if anchor in anchor_counts:
            anchor_counts[anchor] += 1
            anchor = f"{anchor}-{anchor_counts[anchor]}"
        else:
            anchor_counts[anchor] = 0

        indent = "  " * (h.level - base_level)
        lines.append(f"{indent}- [{h.text}](#{anchor})")

    return lines


def build_toc_block(headings: list[Heading]) -> str:
    """Build the full TOC block including markers."""
    toc_lines = generate_toc_lines(headings)
    if not toc_lines:
        return f"{TOC_START}\n{TOC_END}\n"
    inner = "\n".join(toc_lines)
    return f"{TOC_START}\n{inner}\n{TOC_END}"


# ---------------------------------------------------------------------------
# File processing
# ---------------------------------------------------------------------------


def find_toc_markers(lines: list[str]) -> tuple[int | None, int | None]:
    """
    Return (start_index, end_index) of existing TOC markers (0-based line indices).
    start_index points to the <!-- TOC --> line.
    end_index points to the <!-- /TOC --> line.
    Returns (None, None) if not found.
    """
    start = end = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == TOC_START:
            start = i
        elif stripped == TOC_END and start is not None:
            end = i
            break
    return start, end


def find_first_h1(lines: list[str]) -> int | None:
    """Return the 0-based index of the first H1 line, or None."""
    for i, line in enumerate(lines):
        if re.match(r"^#\s+\S", line):
            return i
    return None


def should_skip(content: str) -> bool:
    """Return True if the file contains the NO-TOC marker."""
    return NO_TOC_MARKER in content


def process_file(path: Path, dry_run: bool = False) -> tuple[bool, str]:
    """
    Process a single markdown file: insert or update its TOC.

    Returns (changed: bool, message: str).
    """
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return False, f"cannot read: {e}"

    if should_skip(content):
        return False, "skipped (contains <!-- NO-TOC -->)"

    lines = content.splitlines(keepends=True)

    # Extract headings (levels 2–4 only; H1 is the title, not in TOC)
    headings = extract_headings([l.rstrip("\n\r") for l in lines], min_level=2, max_level=4)
    if not headings:
        return False, "no headings found (levels ##–####)"

    toc_block = build_toc_block(headings)
    toc_block_lines = (toc_block + "\n").splitlines(keepends=True)

    start_idx, end_idx = find_toc_markers(lines)

    if start_idx is not None and end_idx is not None:
        # Replace existing TOC block
        existing_toc_lines = lines[start_idx:end_idx + 1]
        existing_toc = "".join(existing_toc_lines).rstrip("\n")
        new_toc = toc_block

        if existing_toc == new_toc:
            return False, "TOC already up to date"

        new_lines = lines[:start_idx] + toc_block_lines + lines[end_idx + 1:]
        action = "updated"
    else:
        # Insert after first H1
        h1_idx = find_first_h1([l.rstrip("\n\r") for l in lines])
        if h1_idx is not None:
            insert_at = h1_idx + 1
            # Skip blank lines immediately after H1
            while insert_at < len(lines) and lines[insert_at].strip() == "":
                insert_at += 1
            new_lines = lines[:insert_at] + ["\n"] + toc_block_lines + ["\n"] + lines[insert_at:]
        else:
            # Prepend at the very top
            new_lines = toc_block_lines + ["\n"] + lines
        action = "inserted"

    new_content = "".join(new_lines)

    if dry_run:
        return True, f"would {action} TOC ({len(headings)} entries)"

    try:
        path.write_text(new_content, encoding="utf-8")
    except OSError as e:
        return False, f"cannot write: {e}"

    return True, f"{action} TOC ({len(headings)} entries)"


# ---------------------------------------------------------------------------
# Directory processing
# ---------------------------------------------------------------------------


def process_directory(dirpath: Path, dry_run: bool = False) -> tuple[int, int, int]:
    """
    Recursively process all .md files in a directory.
    Returns (updated, skipped, failed) counts.
    """
    updated = skipped = failed = 0

    md_files = sorted(dirpath.rglob("*.md"))
    if not md_files:
        print(f"  No .md files found in {dirpath}")
        return 0, 0, 0

    for md_file in md_files:
        # Skip hidden directories
        if any(part.startswith(".") for part in md_file.parts):
            continue
        changed, msg = process_file(md_file, dry_run=dry_run)
        try:
            rel = md_file.relative_to(REPO_ROOT)
        except ValueError:
            rel = md_file

        if "cannot" in msg:
            failed += 1
            print(f"  [FAIL ] {rel}: {msg}")
        elif "skipped" in msg or "up to date" in msg or "no headings" in msg:
            skipped += 1
            print(f"  [SKIP ] {rel}: {msg}")
        else:
            updated += 1
            prefix = "[DRY  ]" if dry_run else "[OK   ]"
            print(f"  {prefix} {rel}: {msg}")

    return updated, skipped, failed


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="generate_toc.py",
        description=(
            "Generate or update Table of Contents in markdown files. "
            "Inserts/updates between <!-- TOC --> and <!-- /TOC --> markers."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "file",
        nargs="?",
        metavar="FILE",
        help="Single markdown file to process.",
    )
    group.add_argument(
        "--dir",
        metavar="DIR",
        help="Recursively process all .md files in this directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing to disk.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.dry_run:
        print()
        print("  [DRY RUN] No files will be written.")

    print()

    if args.dir:
        dirpath = Path(args.dir).resolve()
        if not dirpath.is_dir():
            print(f"ERROR: '{args.dir}' is not a directory.", file=sys.stderr)
            return 2

        print(f"  Processing directory: {dirpath}")
        print("  " + "─" * 60)
        updated, skipped, failed = process_directory(dirpath, dry_run=args.dry_run)
        print()
        action = "Would update" if args.dry_run else "Updated"
        print(f"  Done. {action} {updated} file(s), skipped {skipped}, failed {failed}.")
        print()
        return 1 if failed else 0

    elif args.file:
        fpath = Path(args.file).resolve()
        if not fpath.exists():
            print(f"ERROR: File '{args.file}' not found.", file=sys.stderr)
            return 2
        if not fpath.suffix.lower() == ".md":
            print(f"WARNING: '{args.file}' does not have a .md extension. Processing anyway.")

        changed, msg = process_file(fpath, dry_run=args.dry_run)
        try:
            rel = fpath.relative_to(REPO_ROOT)
        except ValueError:
            rel = fpath

        if args.dry_run and changed:
            print(f"  [DRY RUN] {rel}: {msg}")
        elif changed:
            print(f"  [OK] {rel}: {msg}")
        else:
            print(f"  [--] {rel}: {msg}")
        print()
        return 0

    else:
        print("ERROR: Provide either a FILE argument or --dir DIR.", file=sys.stderr)
        print("       Run with --help for usage.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
