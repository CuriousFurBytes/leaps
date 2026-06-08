#!/usr/bin/env python3
"""
spaced_repetition.py - Generate an SM-2-inspired spaced repetition review schedule.

Reads test scores and module completion dates from all topics and calculates
when each module should next be reviewed based on performance:

  Score ≥ 80%:   Review in 7 days
  Score 60–79%:  Review in 3 days
  Score < 60%:   Review in 1 day (tomorrow)
  Not tested:    Review immediately (mark as needing attention)
  Just completed (no score): Review in 1 day

Outputs a prioritised study plan: what to study today, this week, later.

Usage:
    python spaced_repetition.py
    python spaced_repetition.py --topic python
    python spaced_repetition.py --days 14
    python spaced_repetition.py --json
"""

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, NamedTuple

# ---------------------------------------------------------------------------
# Repository layout
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_DIR = REPO_ROOT / "TOPICS"

# ---------------------------------------------------------------------------
# SM-2-inspired interval rules (simplified)
# ---------------------------------------------------------------------------

INTERVAL_HIGH = 7     # days: score >= 80%
INTERVAL_MED = 3      # days: score 60–79%
INTERVAL_LOW = 1      # days: score < 60%
INTERVAL_NEW = 1      # days: completed but not yet tested
INTERVAL_NEVER = 0    # days: overdue right now (not started or very low score)

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

RE_CHECKED = re.compile(r"^\s*-\s*\[x\]", re.IGNORECASE | re.MULTILINE)
RE_UNCHECKED = re.compile(r"^\s*-\s*\[ \]", re.MULTILINE)
RE_SCORE_FRACTION = re.compile(r"(\d+)\s*/\s*(\d+)")
RE_SCORE_PERCENT = re.compile(r"(\d+(?:\.\d+)?)\s*%")
# Grading record date: graded_at: 2026-05-22T14:30:00Z
RE_GRADED_AT = re.compile(
    r"graded_at:\s*(\d{4}-\d{2}-\d{2})",
)
# Completion date from journal entry: ### 2026-05-22
RE_JOURNAL_DATE = re.compile(r"^###\s+(\d{4}-\d{2}-\d{2})", re.MULTILINE)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


class ModuleReview(NamedTuple):
    topic_slug: str
    topic_display: str
    module_name: str
    module_path: Path
    last_score: float | None          # 0–100, or None if never tested
    last_review_date: date | None     # date of last test/completion
    next_review_date: date            # calculated next review date
    interval_days: int                # number of days until next review
    days_overdue: int                 # positive means overdue, 0 means today


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def parse_latest_score(text: str) -> float | None:
    """Extract the most recent test score percentage from text."""
    # Prefer grading records (most reliable)
    grading_scores = []
    for m in re.finditer(
        r"percentage:\s*([\d.]+)%",
        text, re.IGNORECASE
    ):
        try:
            grading_scores.append(float(m.group(1)))
        except ValueError:
            pass

    if grading_scores:
        return grading_scores[-1]  # Most recent grading

    # Fall back to fraction scores
    scores = []
    for line in text.splitlines():
        # Skip header lines in tables
        if "Score" in line and "Grade" in line:
            continue
        m = RE_SCORE_FRACTION.search(line)
        if m:
            earned, total = int(m.group(1)), int(m.group(2))
            if 0 < total <= 200 and 0 <= earned <= total * 1.5:
                scores.append(min(round(earned / total * 100, 1), 100.0))
            continue
        m2 = RE_SCORE_PERCENT.search(line)
        if m2:
            pct = float(m2.group(1))
            if 0 < pct <= 100:
                scores.append(pct)

    return scores[-1] if scores else None


def parse_latest_date(text: str) -> date | None:
    """Extract the most recent date from a markdown file (graded_at or journal date)."""
    dates: list[date] = []

    for m in RE_GRADED_AT.finditer(text):
        try:
            dates.append(date.fromisoformat(m.group(1)))
        except ValueError:
            pass

    for m in RE_JOURNAL_DATE.finditer(text):
        try:
            dates.append(date.fromisoformat(m.group(1)))
        except ValueError:
            pass

    if dates:
        return max(dates)
    return None


def parse_module_state(mod_dir: Path) -> tuple[float | None, date | None, bool]:
    """
    Parse a module directory.
    Returns (latest_score, latest_date, has_any_completion).
    """
    score: float | None = None
    latest_date: date | None = None
    has_completion = False

    for fname in ("ANSWERS.md", "TEST.md", "README.md", "NOTES.md"):
        fpath = mod_dir / fname
        if not fpath.exists():
            continue
        try:
            text = fpath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        # Check for completion indicators
        if len(RE_CHECKED.findall(text)) > 0:
            has_completion = True

        # Parse score (prefer ANSWERS.md)
        if score is None or fname == "ANSWERS.md":
            s = parse_latest_score(text)
            if s is not None:
                score = s

        # Parse date
        d = parse_latest_date(text)
        if d is not None:
            if latest_date is None or d > latest_date:
                latest_date = d

    # Also check mtime as a fallback for completion date
    if has_completion and latest_date is None:
        try:
            newest = max(
                (mod_dir / f).stat().st_mtime
                for f in ("README.md", "NOTES.md", "TEST.md", "ANSWERS.md")
                if (mod_dir / f).exists()
            )
            latest_date = date.fromtimestamp(newest)
        except (OSError, ValueError):
            pass

    return score, latest_date, has_completion


def compute_interval(score: float | None, has_completion: bool) -> int:
    """Compute the review interval in days based on score and completion."""
    if score is None:
        if has_completion:
            return INTERVAL_NEW      # Completed but not tested
        return INTERVAL_NEVER        # Never touched
    if score >= 80:
        return INTERVAL_HIGH
    if score >= 60:
        return INTERVAL_MED
    return INTERVAL_LOW


def compute_next_review(last_date: date | None, interval: int) -> date:
    """Compute the next review date."""
    if last_date is None:
        return date.today()
    return last_date + timedelta(days=interval)


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------


def find_module_dirs(topic_dir: Path) -> list[Path]:
    modules_dir = topic_dir / "modules"
    if modules_dir.is_dir():
        return sorted(
            d for d in modules_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        )
    return sorted(
        d for d in topic_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
        and d.name not in ("labs", "assets")
    )


def build_review_list(topic_filter: str | None = None) -> list[ModuleReview]:
    """Build the full review list from all modules."""
    reviews: list[ModuleReview] = []
    today = date.today()

    if not TOPICS_DIR.exists():
        return reviews

    for topic_dir in sorted(TOPICS_DIR.iterdir()):
        if not topic_dir.is_dir() or topic_dir.name.startswith("."):
            continue
        if topic_filter and topic_dir.name != topic_filter.lower():
            continue

        topic_slug = topic_dir.name
        topic_display = " ".join(w.capitalize() for w in topic_slug.split("-"))

        for mod_dir in find_module_dirs(topic_dir):
            score, last_date, has_completion = parse_module_state(mod_dir)
            interval = compute_interval(score, has_completion)

            # Skip modules that were never touched and aren't due yet
            # (they'll show up in "never started" section)
            next_review = compute_next_review(last_date, interval)
            days_overdue = (today - next_review).days

            reviews.append(ModuleReview(
                topic_slug=topic_slug,
                topic_display=topic_display,
                module_name=mod_dir.name,
                module_path=mod_dir,
                last_score=score,
                last_review_date=last_date,
                next_review_date=next_review,
                interval_days=interval,
                days_overdue=days_overdue,
            ))

    return reviews


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------


def format_score(score: float | None) -> str:
    if score is None:
        return "  —  "
    return f"{score:5.1f}%"


def format_date(d: date | None) -> str:
    if d is None:
        return "never"
    return d.isoformat()


def module_display(m: ModuleReview) -> str:
    """Human-readable module path."""
    return f"{m.topic_display} / {m.module_name}"


def print_review_schedule(reviews: list[ModuleReview], days_ahead: int = 7) -> None:
    today = date.today()

    # Partition reviews
    overdue_urgent = [r for r in reviews if r.days_overdue > 0 and r.last_score is not None]
    due_today = [r for r in reviews if r.next_review_date == today]
    due_this_period = [
        r for r in reviews
        if 1 <= (r.next_review_date - today).days <= days_ahead
    ]
    never_started = [r for r in reviews if r.last_review_date is None and not any(
        (r.module_path / f).exists() and
        len(re.findall(r"^\s*-\s*\[x\]", (r.module_path / f).read_text(encoding="utf-8", errors="replace") if (r.module_path / f).exists() else "", re.IGNORECASE | re.MULTILINE)) > 0
        for f in ("README.md",)
    )]
    later = [
        r for r in reviews
        if (r.next_review_date - today).days > days_ahead
    ]

    print()
    print(f"  LEAPS Spaced Repetition Schedule — {today.isoformat()}")
    print(f"  {'═' * 60}")
    print()

    # Overdue
    if overdue_urgent:
        print(f"  OVERDUE ({len(overdue_urgent)}) — Study these now")
        print(f"  {'─' * 58}")
        for r in sorted(overdue_urgent, key=lambda x: -x.days_overdue):
            overdue_str = f"({r.days_overdue}d overdue)"
            print(
                f"  {module_display(r):<45} "
                f"score: {format_score(r.last_score)}  {overdue_str}"
            )
        print()

    # Due today
    if due_today:
        print(f"  DUE TODAY ({len(due_today)})")
        print(f"  {'─' * 58}")
        for r in sorted(due_today, key=lambda x: (x.last_score or 0)):
            last = f"last: {format_date(r.last_review_date)}"
            print(
                f"  {module_display(r):<45} "
                f"score: {format_score(r.last_score)}  {last}"
            )
        print()

    # Due this week
    if due_this_period:
        print(f"  DUE IN NEXT {days_ahead} DAYS ({len(due_this_period)})")
        print(f"  {'─' * 58}")
        for r in sorted(due_this_period, key=lambda x: x.next_review_date):
            due_in = (r.next_review_date - today).days
            due_str = f"in {due_in}d ({r.next_review_date.isoformat()})"
            print(
                f"  {module_display(r):<45} "
                f"score: {format_score(r.last_score)}  due {due_str}"
            )
        print()

    # Summary
    total = len(reviews)
    total_due_now = len(overdue_urgent) + len(due_today)
    print(f"  Summary")
    print(f"  {'─' * 40}")
    print(f"  Total modules tracked:  {total}")
    print(f"  Due now/overdue:        {total_due_now}")
    print(f"  Due in {days_ahead} days:         {len(due_this_period)}")
    print(f"  Due later:              {len(later)}")
    print()

    # Interval legend
    print(f"  Intervals: score ≥80% → 7 days | 60–79% → 3 days | <60% → 1 day")
    print()


# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------


def build_json_output(reviews: list[ModuleReview], days_ahead: int) -> dict[str, Any]:
    today = date.today()
    return {
        "generated_at": today.isoformat(),
        "schedule_days_ahead": days_ahead,
        "summary": {
            "total_modules": len(reviews),
            "overdue": sum(1 for r in reviews if r.days_overdue > 0 and r.last_score is not None),
            "due_today": sum(1 for r in reviews if r.next_review_date == today),
            "due_in_period": sum(
                1 for r in reviews
                if 1 <= (r.next_review_date - today).days <= days_ahead
            ),
        },
        "reviews": [
            {
                "topic": r.topic_slug,
                "module": r.module_name,
                "last_score": r.last_score,
                "last_review_date": format_date(r.last_review_date),
                "next_review_date": r.next_review_date.isoformat(),
                "interval_days": r.interval_days,
                "days_overdue": r.days_overdue,
                "path": str(r.module_path.relative_to(REPO_ROOT)),
            }
            for r in sorted(reviews, key=lambda x: x.next_review_date)
        ],
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="spaced_repetition.py",
        description="Generate an SM-2-inspired spaced repetition study schedule.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--topic",
        metavar="TOPIC",
        default=None,
        help="Limit the schedule to one topic (e.g. --topic python).",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        metavar="N",
        help="Show modules due within N days (default: 7).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON instead of the formatted terminal schedule.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not TOPICS_DIR.exists():
        print(f"ERROR: TOPICS/ not found at {TOPICS_DIR}", file=sys.stderr)
        return 1

    reviews = build_review_list(topic_filter=args.topic)

    if not reviews:
        if args.topic:
            print(f"No modules found for topic '{args.topic}'.", file=sys.stderr)
        else:
            print("No modules found. Create topics with: python SCRIPTS/new_topic.py <name>")
        return 0

    if args.json:
        data = build_json_output(reviews, days_ahead=args.days)
        print(json.dumps(data, indent=2))
        return 0

    print_review_schedule(reviews, days_ahead=args.days)
    return 0


if __name__ == "__main__":
    sys.exit(main())
