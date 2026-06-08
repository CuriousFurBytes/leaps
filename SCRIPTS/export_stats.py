#!/usr/bin/env python3
"""
export_stats.py - Export aggregated learning statistics from all LEAPS topics.

Aggregates data from all topics:
  - Total modules created/completed
  - Test scores per topic/module (from TEST.md, ANSWERS.md grading records)
  - Points earned (from PROGRESS.md and README checklists)
  - Questions logged (count of Q: entries and checklist items in QUESTIONS.md)
  - Study time estimates (from difficulty and module count)

Exports to JSON or Markdown. Shows:
  - Global completion percentage
  - Strong/weak areas (topics by average score)
  - Topics sorted by completion
  - Recommendations for review

Usage:
    python export_stats.py
    python export_stats.py --format json --output stats.json
    python export_stats.py --format markdown --output stats.md
"""

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Repository layout
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_DIR = REPO_ROOT / "TOPICS"

# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

RE_CHECKED = re.compile(r"^\s*-\s*\[x\]", re.IGNORECASE | re.MULTILINE)
RE_UNCHECKED = re.compile(r"^\s*-\s*\[ \]", re.MULTILINE)
RE_IN_PROGRESS = re.compile(r"^\s*-\s*\[~\]", re.IGNORECASE | re.MULTILINE)
RE_SCORE_FRACTION = re.compile(r"(\d+)\s*/\s*(\d+)")
RE_SCORE_PERCENT = re.compile(r"(\d+(?:\.\d+)?)\s*%")
RE_TOTAL_POINTS = re.compile(r"Total Points[:\s]+(\d+)\s*/\s*(\d+)", re.IGNORECASE)
RE_QUESTION = re.compile(r"^#+\s+(Q\d+|Question\s+\d+)", re.IGNORECASE | re.MULTILINE)
RE_GRADING_RECORD = re.compile(
    r"graded_at:\s*(.+?)\n.*?score:\s*(\d+)/(\d+).*?percentage:\s*([\d.]+)%",
    re.DOTALL,
)

# Estimated study hours by difficulty
HOURS_BY_DIFFICULTY: dict[str, float] = {
    "beginner": 2.5,
    "intermediate": 4.0,
    "advanced": 6.0,
    "expert": 8.0,
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


class ModuleStats:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.name = path.name
        self.checked: int = 0
        self.unchecked: int = 0
        self.test_scores: list[float] = []
        self.grading_records: list[dict[str, Any]] = []
        self.question_count: int = 0
        self.points_earned: int = 0
        self.points_possible: int = 0


class TopicStats:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.slug = path.name
        self.display_name = " ".join(w.capitalize() for w in path.name.split("-"))
        self.modules: list[ModuleStats] = []
        self.difficulty: str = "unknown"
        self.total_points_earned: int = 0
        self.total_points_possible: int = 0
        self.question_count: int = 0
        self.readme_checked: int = 0
        self.readme_unchecked: int = 0

    @property
    def module_count(self) -> int:
        return len(self.modules)

    @property
    def completed_modules(self) -> int:
        return sum(1 for m in self.modules if m.checked > 0 and m.unchecked == 0)

    @property
    def completion_pct(self) -> float:
        if self.module_count == 0:
            return 0.0
        return round(self.completed_modules / self.module_count * 100, 1)

    @property
    def all_test_scores(self) -> list[float]:
        scores: list[float] = []
        for m in self.modules:
            scores.extend(m.test_scores)
        return scores

    @property
    def avg_score(self) -> float | None:
        scores = self.all_test_scores
        if not scores:
            return None
        return round(sum(scores) / len(scores), 1)

    @property
    def estimated_hours(self) -> float:
        hours_per_module = HOURS_BY_DIFFICULTY.get(self.difficulty.lower(), 3.0)
        return round(self.module_count * hours_per_module, 1)

    @property
    def estimated_hours_remaining(self) -> float:
        hours_per_module = HOURS_BY_DIFFICULTY.get(self.difficulty.lower(), 3.0)
        remaining = self.module_count - self.completed_modules
        return round(remaining * hours_per_module, 1)


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def parse_scores(text: str) -> list[float]:
    """Extract test score percentages from text."""
    scores: list[float] = []
    for line in text.splitlines():
        if line.strip().startswith("|") and ("---" in line or "Score" in line or "Grade" in line):
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
            if 0 <= pct <= 100:
                scores.append(pct)
    return scores


def parse_grading_records(text: str) -> list[dict[str, Any]]:
    """Extract structured grading records from ANSWERS.md content."""
    records = []
    for m in RE_GRADING_RECORD.finditer(text):
        try:
            records.append({
                "graded_at": m.group(1).strip(),
                "earned": int(m.group(2)),
                "possible": int(m.group(3)),
                "percentage": float(m.group(4)),
            })
        except (ValueError, IndexError):
            pass
    return records


def parse_points(text: str) -> tuple[int, int]:
    """Extract total points earned/possible from PROGRESS.md or README."""
    m = RE_TOTAL_POINTS.search(text)
    if m:
        return int(m.group(1)), int(m.group(2))
    return 0, 0


def count_questions(text: str) -> int:
    """Count question entries in a QUESTIONS.md file."""
    return len(RE_QUESTION.findall(text))


def detect_difficulty(text: str) -> str:
    """Extract difficulty from markdown text."""
    m = re.search(
        r"difficulty:\s*[\"']?(beginner|intermediate|advanced|expert)[\"']?",
        text, re.IGNORECASE
    )
    if m:
        return m.group(1).lower()
    for line in text.splitlines():
        if "difficulty" in line.lower():
            for level in ("expert", "advanced", "intermediate", "beginner"):
                if level in line.lower():
                    return level
    return "unknown"


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------


def scan_module(mod_dir: Path) -> ModuleStats:
    ms = ModuleStats(mod_dir)

    for fname, attr in (("README.md", None), ("TEST.md", None), ("ANSWERS.md", None)):
        fpath = mod_dir / fname
        if not fpath.exists():
            continue
        try:
            text = fpath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        if fname == "README.md":
            ms.checked = len(RE_CHECKED.findall(text))
            ms.unchecked = len(RE_UNCHECKED.findall(text))

        scores = parse_scores(text)
        ms.test_scores.extend(scores)

        if fname == "ANSWERS.md":
            ms.grading_records.extend(parse_grading_records(text))

    # Points from PROGRESS.md equivalent (look for points table in any file)
    for fname in ("README.md", "ANSWERS.md"):
        fpath = mod_dir / fname
        if fpath.exists():
            try:
                text = fpath.read_text(encoding="utf-8", errors="replace")
                earned, possible = parse_points(text)
                if possible > 0:
                    ms.points_earned = earned
                    ms.points_possible = possible
                    break
            except OSError:
                pass

    # Questions count
    questions_file = mod_dir / "QUESTIONS.md"
    if questions_file.exists():
        try:
            text = questions_file.read_text(encoding="utf-8", errors="replace")
            ms.question_count = count_questions(text)
        except OSError:
            pass

    return ms


def scan_topic(topic_dir: Path) -> TopicStats:
    ts = TopicStats(topic_dir)

    # Topic-level README
    readme = topic_dir / "README.md"
    if readme.exists():
        try:
            text = readme.read_text(encoding="utf-8", errors="replace")
            ts.difficulty = detect_difficulty(text)
            ts.readme_checked = len(RE_CHECKED.findall(text))
            ts.readme_unchecked = len(RE_UNCHECKED.findall(text))
            earned, possible = parse_points(text)
            ts.total_points_earned = earned
            ts.total_points_possible = possible
        except OSError:
            pass

    # Topic-level PROGRESS.md
    progress = topic_dir / "PROGRESS.md"
    if progress.exists():
        try:
            text = progress.read_text(encoding="utf-8", errors="replace")
            earned, possible = parse_points(text)
            if possible > 0:
                ts.total_points_earned = earned
                ts.total_points_possible = possible
        except OSError:
            pass

    # Topic-level QUESTIONS.md
    questions = topic_dir / "QUESTIONS.md"
    if questions.exists():
        try:
            text = questions.read_text(encoding="utf-8", errors="replace")
            ts.question_count = count_questions(text)
        except OSError:
            pass

    # Scan modules
    modules_dir = topic_dir / "modules"
    search_dir = modules_dir if modules_dir.is_dir() else topic_dir
    for entry in sorted(search_dir.iterdir()):
        if entry.is_dir() and not entry.name.startswith(".") \
                and entry.name not in ("labs", "assets"):
            mod = scan_module(entry)
            ts.modules.append(mod)
            ts.question_count += mod.question_count
            if ts.total_points_possible == 0 and mod.points_possible > 0:
                ts.total_points_earned += mod.points_earned
                ts.total_points_possible += mod.points_possible

    return ts


def scan_all() -> list[TopicStats]:
    if not TOPICS_DIR.exists():
        return []
    result = []
    for d in sorted(TOPICS_DIR.iterdir()):
        if d.is_dir() and not d.name.startswith("."):
            result.append(scan_topic(d))
    return result


# ---------------------------------------------------------------------------
# Analysis helpers
# ---------------------------------------------------------------------------


def strong_areas(topics: list[TopicStats], threshold: float = 75.0) -> list[TopicStats]:
    return [t for t in topics if t.avg_score is not None and t.avg_score >= threshold]


def weak_areas(topics: list[TopicStats], threshold: float = 60.0) -> list[TopicStats]:
    return [t for t in topics if t.avg_score is not None and t.avg_score < threshold]


def review_recommendations(topics: list[TopicStats]) -> list[dict[str, str]]:
    """Generate review recommendations sorted by priority."""
    recs = []
    for t in topics:
        if t.completion_pct > 0 and t.avg_score is not None and t.avg_score < 70:
            recs.append({
                "topic": t.display_name,
                "slug": t.slug,
                "reason": f"Average test score {t.avg_score:.1f}% is below 70%",
                "priority": "high" if t.avg_score < 60 else "medium",
            })
        elif t.completion_pct > 50 and t.completion_pct < 100:
            recs.append({
                "topic": t.display_name,
                "slug": t.slug,
                "reason": f"Topic is {t.completion_pct:.0f}% complete — push to finish",
                "priority": "medium",
            })
    return sorted(recs, key=lambda r: (r["priority"] == "medium", r["topic"]))


# ---------------------------------------------------------------------------
# Exporters
# ---------------------------------------------------------------------------


def build_stats_dict(topics: list[TopicStats]) -> dict[str, Any]:
    """Build the full statistics dictionary."""
    today = date.today().isoformat()
    all_scores: list[float] = []
    total_modules = 0
    total_completed = 0
    total_questions = 0
    total_points_earned = 0
    total_points_possible = 0
    total_hours = 0.0
    total_hours_remaining = 0.0

    for t in topics:
        all_scores.extend(t.all_test_scores)
        total_modules += t.module_count
        total_completed += t.completed_modules
        total_questions += t.question_count
        total_points_earned += t.total_points_earned
        total_points_possible += t.total_points_possible
        total_hours += t.estimated_hours
        total_hours_remaining += t.estimated_hours_remaining

    global_pct = round(total_completed / total_modules * 100, 1) if total_modules > 0 else 0.0
    global_avg_score = round(sum(all_scores) / len(all_scores), 1) if all_scores else None

    topics_data = []
    for t in sorted(topics, key=lambda x: x.completion_pct, reverse=True):
        topics_data.append({
            "slug": t.slug,
            "display_name": t.display_name,
            "difficulty": t.difficulty,
            "module_count": t.module_count,
            "completed_modules": t.completed_modules,
            "completion_pct": t.completion_pct,
            "avg_test_score": t.avg_score,
            "all_test_scores": t.all_test_scores,
            "points_earned": t.total_points_earned,
            "points_possible": t.total_points_possible,
            "questions_logged": t.question_count,
            "estimated_hours_total": t.estimated_hours,
            "estimated_hours_remaining": t.estimated_hours_remaining,
        })

    return {
        "generated_at": today,
        "global": {
            "total_topics": len(topics),
            "total_modules": total_modules,
            "completed_modules": total_completed,
            "completion_pct": global_pct,
            "avg_test_score": global_avg_score,
            "total_points_earned": total_points_earned,
            "total_points_possible": total_points_possible,
            "total_questions_logged": total_questions,
            "estimated_total_hours": round(total_hours, 1),
            "estimated_hours_remaining": round(total_hours_remaining, 1),
        },
        "topics": topics_data,
        "strong_areas": [t.slug for t in strong_areas(topics)],
        "weak_areas": [t.slug for t in weak_areas(topics)],
        "recommendations": review_recommendations(topics),
    }


def render_markdown(stats: dict[str, Any]) -> str:
    """Render the statistics dictionary as a markdown report."""
    g = stats["global"]
    today = stats["generated_at"]
    lines = [
        "# LEAPS Learning Statistics",
        "",
        f"_Generated: {today}_",
        "",
        "---",
        "",
        "## Global Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Topics | {g['total_topics']} |",
        f"| Total modules | {g['total_modules']} |",
        f"| Completed modules | {g['completed_modules']} |",
        f"| Global completion | {g['completion_pct']}% |",
        f"| Average test score | {g['avg_test_score']}% |" if g['avg_test_score'] else "| Average test score | — |",
        f"| Points earned | {g['total_points_earned']} / {g['total_points_possible']} |",
        f"| Questions logged | {g['total_questions_logged']} |",
        f"| Est. total study hours | {g['estimated_total_hours']} hrs |",
        f"| Est. hours remaining | {g['estimated_hours_remaining']} hrs |",
        "",
        "---",
        "",
        "## Topics by Completion",
        "",
        "| Topic | Completion | Modules | Avg Score | Points |",
        "|-------|------------|---------|-----------|--------|",
    ]
    for t in stats["topics"]:
        mod_str = f"{t['completed_modules']}/{t['module_count']}"
        score_str = f"{t['avg_test_score']}%" if t['avg_test_score'] is not None else "—"
        pts_str = f"{t['points_earned']}/{t['points_possible']}" if t['points_possible'] else "—"
        lines.append(
            f"| {t['display_name']} | {t['completion_pct']}% | {mod_str} | {score_str} | {pts_str} |"
        )

    lines += ["", "---", ""]

    if stats["strong_areas"]:
        lines += [
            "## Strong Areas (avg score ≥ 75%)",
            "",
        ]
        for slug in stats["strong_areas"]:
            label = " ".join(w.capitalize() for w in slug.split("-"))
            lines.append(f"- [[{slug}]] ({label})")
        lines.append("")

    if stats["weak_areas"]:
        lines += [
            "## Weak Areas (avg score < 60%)",
            "",
        ]
        for slug in stats["weak_areas"]:
            label = " ".join(w.capitalize() for w in slug.split("-"))
            lines.append(f"- [[{slug}]] ({label}) — review recommended")
        lines.append("")

    if stats["recommendations"]:
        lines += [
            "---",
            "",
            "## Review Recommendations",
            "",
            "| Priority | Topic | Reason |",
            "|----------|-------|--------|",
        ]
        for rec in stats["recommendations"]:
            lines.append(
                f"| {rec['priority'].upper()} | [[{rec['slug']}]] ({rec['topic']}) | {rec['reason']} |"
            )
        lines.append("")

    lines += [
        "---",
        "",
        "_Run `python SCRIPTS/export_stats.py` to regenerate._",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="export_stats.py",
        description="Export aggregated LEAPS learning statistics.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="markdown",
        help="Output format (default: markdown).",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        default=None,
        help="Write output to FILE (default: stdout).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not TOPICS_DIR.exists():
        print(f"ERROR: TOPICS/ not found at {TOPICS_DIR}", file=sys.stderr)
        return 1

    print("  Scanning topics...", file=sys.stderr)
    topics = scan_all()

    if not topics:
        print("  No topics found.", file=sys.stderr)
        return 0

    stats = build_stats_dict(topics)

    if args.format == "json":
        output = json.dumps(stats, indent=2)
    else:
        output = render_markdown(stats)

    if args.output:
        out_path = Path(args.output).resolve()
        out_path.write_text(output, encoding="utf-8")
        print(f"  Written to {out_path}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
