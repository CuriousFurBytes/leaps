#!/usr/bin/env python3
"""
update_index.py - Regenerate the TOPICS/README.md global index.

Scans all topic directories under TOPICS/, extracts metadata from each topic's
README.md (description, difficulty, module count, prerequisites, completion),
and generates/updates TOPICS/README.md with:
  - Alphabetical table of all topics
  - Category groupings (auto-detected from topic names and tags)
  - Global stats summary

Usage:
    python update_index.py
    python update_index.py --preview
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Repository layout
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_DIR = REPO_ROOT / "TOPICS"
INDEX_FILE = TOPICS_DIR / "README.md"

# ---------------------------------------------------------------------------
# Category detection heuristics
# ---------------------------------------------------------------------------

# Maps category name → list of keyword fragments (matched against topic slug)
CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "Programming Languages": [
        "python", "rust", "go", "golang", "javascript", "typescript",
        "java", "c-sharp", "csharp", "cpp", "c-plus", "ruby", "php",
        "swift", "kotlin", "scala", "haskell", "elixir", "erlang",
        "clojure", "lua", "perl", "r-lang", "julia", "dart", "zig",
    ],
    "Web Development": [
        "html", "css", "react", "vue", "angular", "svelte", "nextjs",
        "django", "flask", "fastapi", "rails", "express", "web",
        "http", "rest", "graphql", "websocket",
    ],
    "Mathematics": [
        "calculus", "algebra", "linear-algebra", "statistics", "probability",
        "discrete", "number-theory", "topology", "geometry", "analysis",
        "differential", "integral", "matrix", "vector", "combinatorics",
        "math", "maths",
    ],
    "Computer Science Fundamentals": [
        "algorithms", "data-structures", "complexity", "computability",
        "automata", "compiler", "operating-systems", "computer-architecture",
        "networks", "networking", "distributed", "concurrency", "parallelism",
        "computer-science", "cs", "theory",
    ],
    "Data & Machine Learning": [
        "machine-learning", "deep-learning", "neural", "nlp", "computer-vision",
        "data-science", "pandas", "numpy", "tensorflow", "pytorch",
        "sklearn", "scikit", "statistics", "data", "ai", "llm",
        "reinforcement", "regression", "classification",
    ],
    "DevOps & Infrastructure": [
        "docker", "kubernetes", "linux", "bash", "shell", "git",
        "ci-cd", "devops", "terraform", "ansible", "aws", "gcp",
        "azure", "cloud", "nginx", "sysadmin",
    ],
    "Databases": [
        "sql", "postgres", "postgresql", "mysql", "sqlite", "mongodb",
        "redis", "database", "nosql", "elasticsearch", "cassandra",
    ],
    "Security": [
        "security", "cryptography", "crypto", "hacking", "penetration",
        "ctf", "infosec", "authentication", "oauth", "tls", "ssl",
    ],
    "Science & Engineering": [
        "physics", "chemistry", "biology", "neuroscience", "electrical",
        "mechanical", "civil", "thermodynamics", "quantum", "astronomy",
        "ecology", "genetics", "biochemistry",
    ],
    "Humanities & Social Sciences": [
        "history", "philosophy", "economics", "sociology", "psychology",
        "linguistics", "literature", "writing", "ethics", "logic",
        "political", "geography", "anthropology",
    ],
    "Arts & Music": [
        "music", "theory", "harmony", "counterpoint", "drawing", "painting",
        "photography", "film", "design", "typography", "color",
    ],
    "Finance & Business": [
        "finance", "investing", "accounting", "economics", "business",
        "marketing", "product", "management", "strategy", "startup",
    ],
}

UNCATEGORISED = "Other"


# ---------------------------------------------------------------------------
# Topic metadata extraction
# ---------------------------------------------------------------------------


def detect_category(slug: str) -> str:
    """Auto-detect a category for a topic based on its slug."""
    slug_lower = slug.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in slug_lower:
                return category
    return UNCATEGORISED


def extract_description(text: str) -> str:
    """
    Extract the first non-empty paragraph after the H1 heading.
    Strips blockquote markers (>) and badge lines.
    """
    lines = text.splitlines()
    past_h1 = False
    paragraph_lines: list[str] = []
    in_paragraph = False

    for line in lines:
        stripped = line.strip()

        # Skip H1
        if re.match(r"^#\s+", stripped):
            if past_h1:
                break
            past_h1 = True
            continue

        if not past_h1:
            continue

        # Skip badge/shield lines
        if "img.shields.io" in stripped or stripped.startswith("!["):
            continue

        # Blockquote lines (> text) — good candidates for descriptions
        if stripped.startswith(">"):
            content = re.sub(r"^>\s*", "", stripped).strip()
            # Skip callout markers like [!NOTE]
            if content and not re.match(r"^\[!", content) and not content.startswith("_"):
                return content

        # Regular paragraph text
        if stripped and not stripped.startswith("#") and not stripped.startswith("|") \
                and not stripped.startswith("```") and not stripped.startswith("---"):
            if not in_paragraph:
                in_paragraph = True
            paragraph_lines.append(stripped)
        elif in_paragraph and not stripped:
            break

    return " ".join(paragraph_lines)[:200] if paragraph_lines else ""


def extract_difficulty(text: str) -> str:
    """Extract difficulty from markdown text."""
    # Look in YAML-like metadata block
    m = re.search(
        r"difficulty:\s*[\"']?(beginner|intermediate|advanced|expert)[\"']?",
        text, re.IGNORECASE
    )
    if m:
        return m.group(1).capitalize()

    # Look in table row: | **Difficulty** | value |
    m = re.search(
        r"\*\*Difficulty\*\*\s*\|\s*(beginner|intermediate|advanced|expert)",
        text, re.IGNORECASE
    )
    if m:
        return m.group(1).capitalize()

    # Loose keyword scan
    for line in text.splitlines():
        if "difficulty" in line.lower():
            for level in ("beginner", "intermediate", "advanced", "expert"):
                if level in line.lower():
                    return level.capitalize()

    return "—"


def extract_prerequisites(text: str) -> list[str]:
    """Extract prerequisite topic slugs from markdown text."""
    prereqs = []
    # YAML block
    m = re.search(r"prerequisites:\s*\n((?:\s+-\s+.+\n?)+)", text)
    if m:
        for line in m.group(1).splitlines():
            item = re.sub(r"^\s*-\s+[\"']?(.+?)[\"']?\s*$", r"\1", line).strip()
            # Skip placeholder values
            if item and "{{" not in item and item != "none":
                prereqs.append(item)
        return prereqs

    # Wiki-links in Prerequisites section
    in_prereq = False
    for line in text.splitlines():
        if re.match(r"^#+\s+Prerequisites", line, re.IGNORECASE):
            in_prereq = True
            continue
        if in_prereq:
            if re.match(r"^#+\s+", line):
                break
            for m2 in re.finditer(r"\[\[([^\]]+)\]\]", line):
                slug = m2.group(1).split("#")[0].split("/")[0].strip().lower()
                if slug and "{{" not in slug:
                    prereqs.append(slug)

    return prereqs


def count_modules(topic_dir: Path) -> int:
    """Count the number of module directories in a topic."""
    modules_dir = topic_dir / "modules"
    if modules_dir.is_dir():
        return sum(
            1 for d in modules_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        )
    # Fallback: count subdirs directly
    return sum(
        1 for d in topic_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".")
        and d.name not in ("labs", "assets")
    )


def count_completed_modules(topic_dir: Path) -> int:
    """Count modules that appear to be complete (have checked items in their README)."""
    modules_dir = topic_dir / "modules"
    if not modules_dir.is_dir():
        modules_dir = topic_dir

    count = 0
    for mod_dir in modules_dir.iterdir():
        if not mod_dir.is_dir() or mod_dir.name.startswith("."):
            continue
        readme = mod_dir / "README.md"
        if readme.exists():
            text = readme.read_text(encoding="utf-8", errors="replace")
            checked = len(re.findall(r"^\s*-\s*\[x\]", text, re.IGNORECASE | re.MULTILINE))
            unchecked = len(re.findall(r"^\s*-\s*\[ \]", text, re.MULTILINE))
            if checked > 0 and unchecked == 0:
                count += 1
    return count


def compute_status(checked: int, total: int) -> str:
    """Return a status string based on completion percentage."""
    if total == 0:
        return "Not Started"
    pct = checked / total * 100
    if pct == 0:
        return "Not Started"
    if pct < 25:
        return "Just Beginning"
    if pct < 50:
        return "In Progress"
    if pct < 75:
        return "Halfway"
    if pct < 100:
        return "Nearly Done"
    return "Complete"


class TopicMeta:
    """Metadata for one topic, ready for rendering."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.slug = path.name
        self.display_name = " ".join(w.capitalize() for w in path.name.split("-"))
        self.description = ""
        self.difficulty = "—"
        self.category = detect_category(path.name)
        self.module_count = 0
        self.completed_modules = 0
        self.prerequisites: list[str] = []
        self.status = "Not Started"
        self.readme_exists = False

    @property
    def completion_pct(self) -> float:
        if self.module_count == 0:
            return 0.0
        return round(self.completed_modules / self.module_count * 100, 0)

    @property
    def prereq_links(self) -> str:
        if not self.prerequisites:
            return "—"
        return ", ".join(f"[[{p}]]" for p in self.prerequisites)


def load_topic_meta(topic_dir: Path) -> TopicMeta:
    """Load and parse metadata for one topic directory."""
    meta = TopicMeta(topic_dir)
    meta.module_count = count_modules(topic_dir)
    meta.completed_modules = count_completed_modules(topic_dir)

    readme = topic_dir / "README.md"
    if readme.exists():
        meta.readme_exists = True
        try:
            text = readme.read_text(encoding="utf-8", errors="replace")
        except OSError:
            text = ""
        meta.description = extract_description(text)
        meta.difficulty = extract_difficulty(text)
        meta.prerequisites = extract_prerequisites(text)

    # Checklist-based completion from README
    if readme.exists():
        try:
            text = readme.read_text(encoding="utf-8", errors="replace")
            checked = len(re.findall(r"^\s*-\s*\[x\]", text, re.IGNORECASE | re.MULTILINE))
            unchecked = len(re.findall(r"^\s*-\s*\[ \]", text, re.MULTILINE))
            meta.status = compute_status(checked, checked + unchecked)
        except OSError:
            pass

    return meta


# ---------------------------------------------------------------------------
# Index generation
# ---------------------------------------------------------------------------


def generate_index(topics: list[TopicMeta], today: str) -> str:
    """Generate the full TOPICS/README.md content."""

    # Group by category
    categories: dict[str, list[TopicMeta]] = {}
    for t in topics:
        categories.setdefault(t.category, []).append(t)

    # Sort categories (common ones first, Other last)
    ordered_cats = sorted(
        categories.keys(),
        key=lambda c: (c == UNCATEGORISED, c)
    )

    total_topics = len(topics)
    total_modules = sum(t.module_count for t in topics)
    total_completed = sum(t.completed_modules for t in topics)
    global_pct = round(total_completed / total_modules * 100, 1) if total_modules > 0 else 0.0

    lines = [
        "# LEAPS Topics",
        "",
        "> All learning topics in this knowledge base. "
        "Each topic is a self-contained, progressively structured learning path.",
        "",
        f"**{total_topics} topic(s)** &nbsp;·&nbsp; "
        f"**{total_modules} total modules** &nbsp;·&nbsp; "
        f"**{global_pct}% complete**",
        "",
        f"_Last updated: {today}_",
        "",
        "---",
        "",
        "## All Topics (Alphabetical)",
        "",
        "| Topic | Description | Difficulty | Modules | Status |",
        "|-------|-------------|------------|---------|--------|",
    ]

    for t in sorted(topics, key=lambda x: x.display_name.lower()):
        desc = (t.description[:70] + "…") if len(t.description) > 70 else t.description
        mod_str = f"{t.completed_modules}/{t.module_count}" if t.module_count else "—"
        lines.append(
            f"| [{t.display_name}](./{t.slug}/) | {desc or '—'} | "
            f"{t.difficulty} | {mod_str} | {t.status} |"
        )

    lines += ["", "---", ""]

    # Category sections
    lines += ["## Topics by Category", ""]

    for cat in ordered_cats:
        cat_topics = sorted(categories[cat], key=lambda x: x.display_name.lower())
        lines += [
            f"### {cat}",
            "",
            "| Topic | Difficulty | Modules | Prerequisites |",
            "|-------|------------|---------|---------------|",
        ]
        for t in cat_topics:
            mod_str = f"{t.completed_modules}/{t.module_count}" if t.module_count else "—"
            lines.append(
                f"| [{t.display_name}](./{t.slug}/) | {t.difficulty} | "
                f"{mod_str} | {t.prereq_links} |"
            )
        lines += [""]

    # Stats summary
    lines += [
        "---",
        "",
        "## Statistics",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total topics | {total_topics} |",
        f"| Total modules | {total_modules} |",
        f"| Completed modules | {total_completed} |",
        f"| Global completion | {global_pct}% |",
        f"| Categories | {len(categories)} |",
        "",
        "---",
        "",
        "_This index is auto-generated by `SCRIPTS/update_index.py`. "
        "Run it again after adding new topics._",
        "",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="update_index.py",
        description="Regenerate TOPICS/README.md with a full topic index.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Print the generated index to stdout without writing to disk.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not TOPICS_DIR.exists():
        print(f"ERROR: TOPICS/ directory not found at {TOPICS_DIR}", file=sys.stderr)
        return 1

    topic_dirs = sorted(
        d for d in TOPICS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )

    if not topic_dirs:
        print("  No topics found under TOPICS/. Nothing to index.")
        return 0

    print(f"  Loading metadata for {len(topic_dirs)} topic(s)...")
    topics = [load_topic_meta(d) for d in topic_dirs]
    today = date.today().isoformat()
    index_content = generate_index(topics, today)

    if args.preview:
        print()
        print(index_content)
        return 0

    INDEX_FILE.write_text(index_content, encoding="utf-8")
    print(f"  Written: {INDEX_FILE}")
    print(f"  Topics indexed: {len(topics)}")
    print(f"  Total modules: {sum(t.module_count for t in topics)}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
