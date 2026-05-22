#!/usr/bin/env python3
"""
knowledge_graph.py - Build a knowledge graph from wiki-links in the LEAPS repository.

Scans all markdown files for [[wiki-links]], builds a directed graph of
connections between topics, and exports it in the requested format.

Output formats:
  markdown  — Human-readable summary with hub topics, orphans, most-connected
  json      — {nodes: [...], edges: [...]} for web visualization (D3.js, etc.)
  dot       — Graphviz DOT format; render with: dot -Tsvg graph.dot -o graph.svg

Usage:
    python knowledge_graph.py
    python knowledge_graph.py --format json --output graph.json
    python knowledge_graph.py --format dot --output graph.dot
    python knowledge_graph.py --format markdown --output graph-summary.md
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Repository layout
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_DIR = REPO_ROOT / "TOPICS"

# ---------------------------------------------------------------------------
# Regex
# ---------------------------------------------------------------------------

RE_WIKI = re.compile(r"\[\[([^\]!][^\]]*)\]\]")


# ---------------------------------------------------------------------------
# Graph building
# ---------------------------------------------------------------------------


def slug_from_wiki(raw: str) -> str | None:
    """
    Extract the topic slug from a wiki-link raw string.
    Returns None for template placeholders or shared/ links.

    [[rust]]              → "rust"
    [[rust#ownership]]    → "rust"
    [[rust/02_ownership]] → "rust"
    [[shared/glossary]]   → None (not a topic)
    [[{{PLACEHOLDER}}]]   → None
    """
    text = raw.strip()
    if "{{" in text or "}}" in text:
        return None
    if text.lower().startswith("shared/"):
        return None
    # Strip section anchor and sub-path
    slug = text.split("#")[0].split("/")[0].strip()
    if not slug:
        return None
    return slug.lower()


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


def get_file_topic(md_file: Path) -> str | None:
    """
    Determine which topic a file belongs to.
    Returns the topic slug (name of the directory under TOPICS/), or None.
    """
    try:
        rel = md_file.relative_to(TOPICS_DIR)
        return rel.parts[0]  # First part is the topic directory name
    except ValueError:
        return None


def build_graph(scan_root: Path) -> tuple[
    dict[str, set[str]],  # adjacency: source → {targets}
    dict[str, set[str]],  # incoming: target → {sources}
    set[str],             # all known topic nodes
]:
    """
    Scan all markdown files and build the wiki-link graph.

    Returns:
        outgoing  — {source_topic: {target_topic, ...}}
        incoming  — {target_topic: {source_topic, ...}}
        all_nodes — set of all topic slugs seen (including in TOPICS/ dirs)
    """
    outgoing: dict[str, set[str]] = defaultdict(set)
    incoming: dict[str, set[str]] = defaultdict(set)

    # Seed all_nodes from actual TOPICS/ directories
    all_nodes: set[str] = set()
    if TOPICS_DIR.exists():
        for d in TOPICS_DIR.iterdir():
            if d.is_dir() and not d.name.startswith("."):
                all_nodes.add(d.name)

    for md_file in sorted(scan_root.rglob("*.md")):
        if any(part.startswith(".") for part in md_file.parts):
            continue

        source_topic = get_file_topic(md_file)
        if source_topic is None:
            continue  # File is outside TOPICS/ — skip as source

        try:
            content = md_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        lines = content.splitlines()

        for i, line in enumerate(lines):
            if is_in_code_block(lines, i):
                continue
            for m in RE_WIKI.finditer(line):
                target = slug_from_wiki(m.group(1))
                if target is None or target == source_topic:
                    continue  # Skip self-links and placeholders
                outgoing[source_topic].add(target)
                incoming[target].add(source_topic)
                all_nodes.add(target)

    return dict(outgoing), dict(incoming), all_nodes


# ---------------------------------------------------------------------------
# Graph analysis
# ---------------------------------------------------------------------------


def hub_topics(incoming: dict[str, set[str]], top_n: int = 10) -> list[tuple[str, int]]:
    """Return top_n topics by incoming link count, descending."""
    counts = {node: len(sources) for node, sources in incoming.items()}
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_n]


def orphan_topics(all_nodes: set[str], incoming: dict[str, set[str]], outgoing: dict[str, set[str]]) -> list[str]:
    """Return topics that have no incoming AND no outgoing links."""
    return sorted(
        node for node in all_nodes
        if node not in incoming and node not in outgoing
    )


def isolated_sinks(all_nodes: set[str], incoming: dict[str, set[str]], outgoing: dict[str, set[str]]) -> list[str]:
    """Return topics that have incoming links but no outgoing links (dead ends)."""
    return sorted(
        node for node in all_nodes
        if node in incoming and node not in outgoing
    )


def total_edges(outgoing: dict[str, set[str]]) -> int:
    return sum(len(v) for v in outgoing.values())


# ---------------------------------------------------------------------------
# Exporters
# ---------------------------------------------------------------------------


def export_json(
    outgoing: dict[str, set[str]],
    incoming: dict[str, set[str]],
    all_nodes: set[str],
) -> str:
    """Export graph as JSON for D3.js / web visualization."""
    nodes = []
    for node in sorted(all_nodes):
        in_count = len(incoming.get(node, set()))
        out_count = len(outgoing.get(node, set()))
        exists = TOPICS_DIR.joinpath(node).exists()
        nodes.append({
            "id": node,
            "label": " ".join(w.capitalize() for w in node.split("-")),
            "in_degree": in_count,
            "out_degree": out_count,
            "total_degree": in_count + out_count,
            "exists": exists,
        })

    edges = []
    for source, targets in sorted(outgoing.items()):
        for target in sorted(targets):
            edges.append({"source": source, "target": target})

    data = {
        "meta": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "generated_by": "knowledge_graph.py",
        },
        "nodes": nodes,
        "edges": edges,
    }
    return json.dumps(data, indent=2)


def export_dot(
    outgoing: dict[str, set[str]],
    all_nodes: set[str],
) -> str:
    """Export graph in Graphviz DOT format."""
    lines = ["digraph leaps_knowledge_graph {"]
    lines.append("  rankdir=LR;")
    lines.append('  node [shape=box, style=filled, fillcolor="#e8f4fd", fontname="Helvetica"];')
    lines.append('  edge [color="#555555"];')
    lines.append("")

    # Nodes
    for node in sorted(all_nodes):
        label = " ".join(w.capitalize() for w in node.split("-"))
        exists = TOPICS_DIR.joinpath(node).exists()
        fill = '#e8f4fd' if exists else '#ffe0e0'
        lines.append(f'  "{node}" [label="{label}", fillcolor="{fill}"];')

    lines.append("")

    # Edges
    for source in sorted(outgoing):
        for target in sorted(outgoing[source]):
            lines.append(f'  "{source}" -> "{target}";')

    lines.append("}")
    return "\n".join(lines)


def export_markdown(
    outgoing: dict[str, set[str]],
    incoming: dict[str, set[str]],
    all_nodes: set[str],
) -> str:
    """Export a human-readable markdown summary of the knowledge graph."""
    hubs = hub_topics(incoming, top_n=10)
    orphans = orphan_topics(all_nodes, incoming, outgoing)
    sinks = isolated_sinks(all_nodes, incoming, outgoing)
    n_edges = total_edges(outgoing)

    lines = [
        "# LEAPS Knowledge Graph Summary",
        "",
        f"**Nodes (topics):** {len(all_nodes)}  "
        f"**Edges (links):** {n_edges}",
        "",
        "---",
        "",
    ]

    # Hub topics
    lines += [
        "## Most Connected Topics (Hub Nodes)",
        "",
        "Topics with the most incoming wiki-links — these are the core concepts.",
        "",
        "| Rank | Topic | Incoming Links | Outgoing Links |",
        "|------|-------|----------------|----------------|",
    ]
    for rank, (node, in_count) in enumerate(hubs, start=1):
        out_count = len(outgoing.get(node, set()))
        label = " ".join(w.capitalize() for w in node.split("-"))
        exists_marker = "" if TOPICS_DIR.joinpath(node).exists() else " *(missing)*"
        lines.append(f"| {rank} | [[{node}]]{exists_marker} | {in_count} | {out_count} |")
    lines.append("")

    # Full adjacency
    lines += [
        "---",
        "",
        "## Full Topic Adjacency",
        "",
        "Each topic and the topics it links to:",
        "",
    ]
    for source in sorted(outgoing):
        targets = sorted(outgoing[source])
        target_links = ", ".join(f"[[{t}]]" for t in targets)
        label = " ".join(w.capitalize() for w in source.split("-"))
        lines.append(f"- **{label}** → {target_links}")
    if not outgoing:
        lines.append("_(no links found yet — add wiki-links to your topic files)_")
    lines.append("")

    # Orphaned topics
    if orphans:
        lines += [
            "---",
            "",
            "## Orphaned Topics",
            "",
            "Topics with no incoming or outgoing wiki-links. "
            "Consider adding cross-references.",
            "",
        ]
        for node in orphans:
            label = " ".join(w.capitalize() for w in node.split("-"))
            lines.append(f"- [[{node}]] ({label})")
        lines.append("")

    # Sink topics
    if sinks:
        lines += [
            "---",
            "",
            "## Sink Topics (Referenced But Never Link Out)",
            "",
            "These topics are referenced by others but don't link to anything. "
            "Add outgoing links to improve discoverability.",
            "",
        ]
        for node in sinks:
            in_count = len(incoming.get(node, set()))
            label = " ".join(w.capitalize() for w in node.split("-"))
            exists_marker = "" if TOPICS_DIR.joinpath(node).exists() else " *(topic not created yet)*"
            lines.append(f"- [[{node}]] — referenced {in_count} time(s){exists_marker}")
        lines.append("")

    lines += [
        "---",
        "",
        "_Generated by `SCRIPTS/knowledge_graph.py`_",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="knowledge_graph.py",
        description="Build and export the LEAPS knowledge graph from wiki-links.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--format",
        choices=["json", "dot", "markdown"],
        default="markdown",
        help="Output format (default: markdown).",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        default=None,
        help="Write output to FILE instead of stdout.",
    )
    parser.add_argument(
        "--dir",
        metavar="DIR",
        default=None,
        help=f"Root directory to scan (default: {REPO_ROOT}).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    scan_root = Path(args.dir).resolve() if args.dir else REPO_ROOT
    if not scan_root.exists():
        print(f"ERROR: Directory '{scan_root}' not found.", file=sys.stderr)
        return 2

    print(f"  Scanning {scan_root} for wiki-links...", file=sys.stderr)
    outgoing, incoming, all_nodes = build_graph(scan_root)
    n_edges = total_edges(outgoing)
    print(f"  Found {len(all_nodes)} topics, {n_edges} link(s).", file=sys.stderr)

    fmt = args.format
    if fmt == "json":
        output = export_json(outgoing, incoming, all_nodes)
    elif fmt == "dot":
        output = export_dot(outgoing, all_nodes)
    else:
        output = export_markdown(outgoing, incoming, all_nodes)

    if args.output:
        out_path = Path(args.output).resolve()
        out_path.write_text(output, encoding="utf-8")
        print(f"  Written to {out_path}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
