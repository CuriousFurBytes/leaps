#!/usr/bin/env python3
"""
progress_report.py - Generate a progress report across all LEAPS topics.

Scans TOPICS/ directories, reads README.md files for checklist items and test
score tables, and outputs a formatted terminal report or JSON.

Usage:
    python progress_report.py
    python progress_report.py --topic python
    python progress_report.py --json
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Repository layout
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_DIR = REPO_ROOT / "TOPICS"

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# Matches completed checklist items:  - [x] anything
RE_CHECKED = re.compile(r"^\s*-\s*\[x\]", re.IGNORECASE | re.MULTILINE)
# Matches unchecked checklist items:  - [ ] anything
RE_UNCHECKED = re.compile(r"^\s*-\s*\[ \]", re.MULTILINE)
# Matches "- [~]" (in-progress) items
RE_IN_PROGRESS = re.compile(r"^\s*-\s*\[~\]", re.IGNORECASE | re.MULTILINE)

# Test score table row: | ModuleName | Date | Score | Grade | Notes |
# We look for rows that contain a numeric score like "23/30" or "85%"
RE_SCORE_FRACTION = re.compile(r"(\d+)\s*/\s*(\d+)")
RE_SCORE_PERCENT = re.compile(r"(\d+(?:\.\d+)?)\s*%")

# Difficulty line in topic README frontmatter or table
RE_DIFFICULTY = re.compile(
    r"\*\*Difficulty\*\*\s*\|\s*(beginner|intermediate|advanced|expert)",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


class ModuleProgress:
    """Progress data for a single module directory."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.name = path.name
        self.checked: int = 0
        self.unchecked: int = 0
        self.in_progress: int = 0
        self.test_scores: list[float] = []  # percentages 0–100
        self.last_modified: float = 0.0


class TopicProgress:
    """Progress data for a single topic directory."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.name = path.name
        self.display_name = " ".join(w.capitalize() for w in path.name.split("-"))
        self.modules: list[ModuleProgress] = []
        self.checked_total: int = 0      # from topic README checklist
        self.unchecked_total: int = 0
        self.in_progress_total: int = 0
        self.test_scores: list[float] = []
        self.difficulty: str = "unknown"
        self.last_modified: float = 0.0
        self.readme_exists: bool = False

    @property
    def total_checklist_items(self) -> int:
        return self.checked_total + self.unchecked_total + self.in_progress_total

    @property
    def completion_pct(self) -> float:
        total = self.total_checklist_items
        if total == 0:
            return 0.0
        return round(self.checked_total / total * 100, 1)

    @property
    def avg_test_score(self) -> float | None:
        all_scores = self.test_scores
        for mod in self.modules:
            all_scores = all_scores + mod.test_scores
        if not all_scores:
            return None
        return round(sum(all_scores) / len(all_scores), 1)

    @property
    def module_count(self) -> int:
        return len(self.modules)

    @property
    def completed_modules(self) -> int:
        """Count modules whose README has at least one checked item and no unchecked items."""
        count = 0
        for mod in self.modules:
            if mod.checked > 0 and mod.unchecked == 0:
                count += 1
        return count


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def parse_test_scores(text: str) -> list[float]:
    """Extract test score percentages from markdown text."""
    scores: list[float] = []
    for line in text.splitlines():
        # Skip header lines
        if line.strip().startswith("|") and ("Score" in line or "Grade" in line or "---" in line):
            continue
        # Look for fraction scores first: 23/30 → 76.7%
        m = RE_SCORE_FRACTION.search(line)
        if m:
            earned, total = int(m.group(1)), int(m.group(2))
            if total > 0 and earned <= total * 2:  # sanity: earned can exceed total (bonus)
                scores.append(min(round(earned / total * 100, 1), 100.0))
            continue
        # Look for percentage scores
        m2 = RE_SCORE_PERCENT.search(line)
        if m2:
            pct = float(m2.group(1))
            if 0 <= pct <= 100:
                scores.append(pct)
    return scores


def parse_readme_checklist(text: str) -> tuple[int, int, int]:
    """Return (checked, unchecked, in_progress) counts from markdown text."""
    checked = len(RE_CHECKED.findall(text))
    unchecked = len(RE_UNCHECKED.findall(text))
    in_progress = len(RE_IN_PROGRESS.findall(text))
    return checked, unchecked, in_progress


def parse_difficulty(text: str) -> str:
    """Extract difficulty level from a topic README."""
    m = RE_DIFFICULTY.search(text)
    if m:
        return m.group(1).lower()
    # Fallback: look for difficulty in YAML-like block or table
    for line in text.splitlines():
        lower = line.lower()
        if "difficulty" in lower:
            for level in ("beginner", "intermediate", "advanced", "expert"):
                if level in lower:
                    return level
    return "unknown"


def get_last_modified(path: Path) -> float:
    """Return the most recent mtime (float) of any file under path."""
    if path.is_file():
        return path.stat().st_mtime
    latest: float = 0.0
    try:
        for p in path.rglob("*"):
            if p.is_file():
                mtime = p.stat().st_mtime
                if mtime > latest:
                    latest = mtime
    except PermissionError:
        pass
    return latest


def format_age(mtime: float) -> str:
    """Return a human-readable age string like '2 days ago'."""
    if mtime == 0.0:
        return "unknown"
    now = datetime.now(tz=timezone.utc).timestamp()
    delta = now - mtime
    if delta < 60:
        return "just now"
    if delta < 3600:
        return f"{int(delta / 60)} min ago"
    if delta < 86400:
        return f"{int(delta / 3600)} hr ago"
    days = int(delta / 86400)
    if days == 1:
        return "1 day ago"
    if days < 30:
        return f"{days} days ago"
    if days < 365:
        months = int(days / 30)
        return f"{months} month{'s' if months > 1 else ''} ago"
    years = int(days / 365)
    return f"{years} year{'s' if years > 1 else ''} ago"


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------


def scan_module(module_path: Path) -> ModuleProgress:
    """Scan a single module directory and return its progress."""
    mp = ModuleProgress(module_path)
    mp.last_modified = get_last_modified(module_path)

    readme = module_path / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8", errors="replace")
        mp.checked, mp.unchecked, mp.in_progress = parse_readme_checklist(text)

    # Check TEST.md and ANSWERS.md for scores
    for fname in ("TEST.md", "ANSWERS.md", "README.md"):
        fpath = module_path / fname
        if fpath.exists():
            text = fpath.read_text(encoding="utf-8", errors="replace")
            mp.test_scores.extend(parse_test_scores(text))

    return mp


def scan_topic(topic_path: Path) -> TopicProgress:
    """Scan a topic directory and return its progress."""
    tp = TopicProgress(topic_path)
    tp.last_modified = get_last_modified(topic_path)

    readme = topic_path / "README.md"
    if readme.exists():
        tp.readme_exists = True
        text = readme.read_text(encoding="utf-8", errors="replace")
        tp.checked_total, tp.unchecked_total, tp.in_progress_total = parse_readme_checklist(text)
        tp.test_scores = parse_test_scores(text)
        tp.difficulty = parse_difficulty(text)

    # Scan modules/ subdirectory
    modules_dir = topic_path / "modules"
    if modules_dir.is_dir():
        for entry in sorted(modules_dir.iterdir()):
            if entry.is_dir() and not entry.name.startswith("."):
                tp.modules.append(scan_module(entry))
    else:
        # Some topics may have modules directly under topic dir (old layout)
        for entry in sorted(topic_path.iterdir()):
            if entry.is_dir() and not entry.name.startswith(".") and entry.name not in (
                "modules", "notebooks", "labs", "assets"
            ):
                # Check if it looks like a module (has a README)
                if (entry / "README.md").exists():
                    tp.modules.append(scan_module(entry))

    return tp


def scan_all_topics() -> list[TopicProgress]:
    """Scan all topics under TOPICS/ and return a list of TopicProgress objects."""
    if not TOPICS_DIR.exists():
        return []

    topics: list[TopicProgress] = []
    for entry in sorted(TOPICS_DIR.iterdir()):
        if entry.is_dir() and not entry.name.startswith(".") and entry.name != "README.md":
            # Skip if it's just a README (not a directory)
            topics.append(scan_topic(entry))

    return topics


# ---------------------------------------------------------------------------
# Recent activity
# ---------------------------------------------------------------------------


def get_recent_files(n: int = 5) -> list[tuple[Path, float]]:
    """Return the N most recently modified markdown files across all topics."""
    files: list[tuple[Path, float]] = []
    if not TOPICS_DIR.exists():
        return files
    for p in TOPICS_DIR.rglob("*.md"):
        if not p.name.startswith("."):
            try:
                mtime = p.stat().st_mtime
                files.append((p, mtime))
            except OSError:
                pass
    files.sort(key=lambda x: x[1], reverse=True)
    return files[:n]


# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------


def bar(pct: float, width: int = 20) -> str:
    """Return a simple ASCII progress bar."""
    filled = round(pct / 100 * width)
    filled = max(0, min(width, filled))
    return "[" + "█" * filled + "░" * (width - filled) + "]"


def format_score(score: float | None) -> str:
    if score is None:
        return "  —  "
    return f"{score:5.1f}%"


def print_topic_summary(tp: TopicProgress) -> None:
    """Print a one-line summary for a topic."""
    if tp.module_count > 0:
        mod_str = f"{tp.completed_modules}/{tp.module_count}"
    else:
        # Fall back to checklist
        total = tp.total_checklist_items
        done = tp.checked_total
        mod_str = f"{done}/{total} items"

    pct = tp.completion_pct
    score_str = format_score(tp.avg_test_score)
    difficulty_short = tp.difficulty[:3].upper() if tp.difficulty != "unknown" else "  —"

    print(
        f"  {tp.display_name:<22} {mod_str:<12} {bar(pct, 16)}  {pct:5.1f}%  "
        f"{score_str}  {difficulty_short}"
    )


def print_topic_detail(tp: TopicProgress) -> None:
    """Print a detailed report for a single topic."""
    print()
    print(f"  {'─' * 60}")
    print(f"  Topic: {tp.display_name}  ({tp.name})")
    print(f"  Difficulty: {tp.difficulty.capitalize()}")
    print(f"  Last activity: {format_age(tp.last_modified)}")
    print(f"  {'─' * 60}")
    print()

    if tp.modules:
        print(f"  {'Module':<35} {'Status':<12} {'Score':<8}")
        print(f"  {'─' * 55}")
        for mod in tp.modules:
            total_items = mod.checked + mod.unchecked + mod.in_progress
            if mod.checked > 0 and mod.unchecked == 0:
                status = "Complete"
            elif mod.checked > 0:
                status = f"{mod.checked}/{total_items} done"
            elif total_items > 0:
                status = "Not started"
            else:
                status = "Empty"

            score_str = format_score(mod.test_scores[-1] if mod.test_scores else None)
            print(f"  {mod.name:<35} {status:<12} {score_str}")
    else:
        total = tp.total_checklist_items
        done = tp.checked_total
        in_prog = tp.in_progress_total
        print(f"  Checklist items: {done} complete, {in_prog} in progress, "
              f"{tp.unchecked_total} remaining (total {total})")

    print()
    if tp.test_scores or any(m.test_scores for m in tp.modules):
        all_scores = tp.test_scores[:]
        for m in tp.modules:
            all_scores.extend(m.test_scores)
        if all_scores:
            avg = sum(all_scores) / len(all_scores)
            best = max(all_scores)
            worst = min(all_scores)
            print(f"  Test scores: avg {avg:.1f}%  best {best:.1f}%  worst {worst:.1f}%")
            print()

    pct = tp.completion_pct
    print(f"  Overall: {bar(pct, 30)} {pct:.1f}%")
    print()


def print_full_report(topics: list[TopicProgress], recent: list[tuple[Path, float]]) -> None:
    """Print the full terminal report."""
    today = datetime.now().strftime("%Y-%m-%d")

    # Global stats
    total_topics = len(topics)
    total_modules = sum(tp.module_count for tp in topics)
    total_completed_modules = sum(tp.completed_modules for tp in topics)
    all_scores: list[float] = []
    for tp in topics:
        all_scores.extend(tp.test_scores)
        for m in tp.modules:
            all_scores.extend(m.test_scores)
    global_pct = (total_completed_modules / total_modules * 100) if total_modules > 0 else 0.0

    print()
    print(f"  LEAPS Progress Report — {today}")
    print(f"  {'═' * 60}")
    print()

    if not topics:
        print("  No topics found under TOPICS/.")
        print("  Run:  python SCRIPTS/new_topic.py <name>  to create one.")
        print()
        return

    # Column headers
    print(f"  {'Topic':<22} {'Modules':<12} {'Progress':<20} {'Pct':>7}  {'Avg':>6}  Lvl")
    print(f"  {'─' * 72}")

    for tp in topics:
        print_topic_summary(tp)

    print(f"  {'─' * 72}")

    # Global summary row
    mod_str = f"{total_completed_modules}/{total_modules}"
    global_avg = (sum(all_scores) / len(all_scores)) if all_scores else None
    score_str = format_score(global_avg)
    print(
        f"  {'GLOBAL':<22} {mod_str:<12} {bar(global_pct, 16)}  {global_pct:5.1f}%  {score_str}"
    )
    print()

    # Stats box
    print(f"  Summary")
    print(f"  {'─' * 40}")
    print(f"  Topics:            {total_topics}")
    print(f"  Total modules:     {total_modules}")
    print(f"  Completed modules: {total_completed_modules}")
    print(f"  Global completion: {global_pct:.1f}%")
    if global_avg is not None:
        print(f"  Average test score:{global_avg:6.1f}%")
    print()

    # Recent activity
    if recent:
        print(f"  Recent activity")
        print(f"  {'─' * 40}")
        for fpath, mtime in recent:
            try:
                rel = fpath.relative_to(REPO_ROOT)
            except ValueError:
                rel = fpath
            print(f"  {format_age(mtime):<14} {rel}")
        print()


# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------


def build_json_report(topics: list[TopicProgress], recent: list[tuple[Path, float]]) -> dict[str, Any]:
    today = datetime.now().isoformat()
    total_modules = sum(tp.module_count for tp in topics)
    total_completed = sum(tp.completed_modules for tp in topics)
    all_scores: list[float] = []
    for tp in topics:
        all_scores.extend(tp.test_scores)
        for m in tp.modules:
            all_scores.extend(m.test_scores)

    topics_data = []
    for tp in topics:
        tp_scores = tp.test_scores[:]
        for m in tp.modules:
            tp_scores.extend(m.test_scores)

        topics_data.append({
            "name": tp.name,
            "display_name": tp.display_name,
            "difficulty": tp.difficulty,
            "module_count": tp.module_count,
            "completed_modules": tp.completed_modules,
            "completion_pct": tp.completion_pct,
            "avg_test_score": tp.avg_test_score,
            "last_modified": datetime.fromtimestamp(tp.last_modified).isoformat() if tp.last_modified else None,
            "modules": [
                {
                    "name": m.name,
                    "checked": m.checked,
                    "unchecked": m.unchecked,
                    "in_progress": m.in_progress,
                    "test_scores": m.test_scores,
                    "last_modified": datetime.fromtimestamp(m.last_modified).isoformat() if m.last_modified else None,
                }
                for m in tp.modules
            ],
        })

    recent_data = []
    for fpath, mtime in recent:
        try:
            rel = str(fpath.relative_to(REPO_ROOT))
        except ValueError:
            rel = str(fpath)
        recent_data.append({"file": rel, "modified": datetime.fromtimestamp(mtime).isoformat()})

    return {
        "generated_at": today,
        "summary": {
            "total_topics": len(topics),
            "total_modules": total_modules,
            "completed_modules": total_completed,
            "global_completion_pct": round(total_completed / total_modules * 100, 1) if total_modules > 0 else 0.0,
            "avg_test_score": round(sum(all_scores) / len(all_scores), 1) if all_scores else None,
        },
        "topics": topics_data,
        "recent_activity": recent_data,
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="progress_report.py",
        description="Generate a progress report across all LEAPS topics.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON instead of the formatted terminal report.",
    )
    parser.add_argument(
        "--topic",
        metavar="TOPIC",
        default=None,
        help="Show a detailed report for one specific topic (e.g. --topic python).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not TOPICS_DIR.exists():
        print(f"ERROR: TOPICS/ directory not found at {TOPICS_DIR}", file=sys.stderr)
        print("       Run this script from the leaps repository root.", file=sys.stderr)
        return 1

    topics = scan_all_topics()
    recent = get_recent_files(n=5)

    # Filter to a single topic if requested
    if args.topic:
        slug = args.topic.strip().lower()
        topics = [t for t in topics if t.name == slug]
        if not topics:
            print(f"ERROR: No topic found with name '{slug}'.", file=sys.stderr)
            available = [t.name for t in scan_all_topics()]
            if available:
                print(f"       Available topics: {', '.join(available)}", file=sys.stderr)
            return 1

    if args.json:
        report = build_json_report(topics, recent)
        print(json.dumps(report, indent=2))
        return 0

    if args.topic and topics:
        print_topic_detail(topics[0])
    else:
        print_full_report(topics, recent)

    return 0


if __name__ == "__main__":
    sys.exit(main())
