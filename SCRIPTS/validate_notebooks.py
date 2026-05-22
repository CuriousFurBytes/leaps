#!/usr/bin/env python3
"""
validate_notebooks.py - Validate Jupyter notebooks in the LEAPS repository.

Checks each .ipynb file for:
  - Valid JSON structure
  - Required cells: title markdown cell, overview/objectives cell
  - Stale execution counts (warns when outputs appear without matching counts)
  - Empty cells (cells with no source content)
  - Complete metadata (kernelspec, language_info)
  - Output artifacts that indicate notebook was run and not cleared (warns)

Optional:
  - --clear-output: Strip all cell outputs (makes notebooks git-friendly)

Returns exit code 1 if hard violations are found.

Usage:
    python validate_notebooks.py
    python validate_notebooks.py --dir notebooks/python/
    python validate_notebooks.py --clear-output
    python validate_notebooks.py --dir notebooks/ --clear-output
"""

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Repository layout
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Violation types
# ---------------------------------------------------------------------------


class Issue:
    """A single notebook issue."""

    ERROR = "ERROR"
    WARNING = "WARN "

    def __init__(
        self,
        severity: str,
        notebook: Path,
        message: str,
        cell_num: int | None = None,
    ) -> None:
        self.severity = severity
        self.notebook = notebook
        self.message = message
        self.cell_num = cell_num

    def __str__(self) -> str:
        try:
            rel = self.notebook.relative_to(REPO_ROOT)
        except ValueError:
            rel = self.notebook
        cell_tag = f" (cell {self.cell_num})" if self.cell_num is not None else ""
        return f"  [{self.severity}] {rel}{cell_tag} — {self.message}"


# ---------------------------------------------------------------------------
# Notebook loading
# ---------------------------------------------------------------------------


def load_notebook(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """
    Load and parse a .ipynb file.
    Returns (notebook_dict, error_message). error_message is None on success.
    """
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return None, f"cannot read file: {e}"

    try:
        nb = json.loads(raw)
    except json.JSONDecodeError as e:
        return None, f"invalid JSON: {e}"

    return nb, None


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------


def check_json_structure(nb: dict[str, Any], path: Path) -> list[Issue]:
    """Check that the notebook has the expected top-level structure."""
    issues = []
    required_keys = {"nbformat", "nbformat_minor", "cells", "metadata"}
    missing = required_keys - set(nb.keys())
    if missing:
        issues.append(Issue(
            Issue.ERROR, path,
            f"missing top-level keys: {', '.join(sorted(missing))}",
        ))
    if "cells" in nb and not isinstance(nb["cells"], list):
        issues.append(Issue(
            Issue.ERROR, path,
            "'cells' field is not a list",
        ))
    return issues


def check_metadata(nb: dict[str, Any], path: Path) -> list[Issue]:
    """Check that notebook metadata is complete."""
    issues = []
    meta = nb.get("metadata", {})

    if not meta:
        issues.append(Issue(
            Issue.WARNING, path,
            "metadata block is empty or missing",
        ))
        return issues

    if "kernelspec" not in meta:
        issues.append(Issue(
            Issue.WARNING, path,
            "metadata missing 'kernelspec' (needed to run the notebook)",
        ))

    if "language_info" not in meta:
        issues.append(Issue(
            Issue.WARNING, path,
            "metadata missing 'language_info'",
        ))

    return issues


def cell_source(cell: dict[str, Any]) -> str:
    """Return the source of a cell as a single string."""
    src = cell.get("source", "")
    if isinstance(src, list):
        return "".join(src)
    return str(src)


def check_empty_cells(nb: dict[str, Any], path: Path) -> list[Issue]:
    """Check for cells with no source content."""
    issues = []
    for i, cell in enumerate(nb.get("cells", []), start=1):
        src = cell_source(cell).strip()
        if not src:
            cell_type = cell.get("cell_type", "unknown")
            issues.append(Issue(
                Issue.WARNING, path,
                f"empty {cell_type} cell",
                cell_num=i,
            ))
    return issues


def check_required_cells(nb: dict[str, Any], path: Path) -> list[Issue]:
    """
    Check that the notebook has required structural cells:
    1. First cell is a markdown cell with a # H1 title
    2. Contains an 'Objectives' or 'Learning Objectives' section
    3. Contains an 'Overview' section (or the title cell serves as overview)
    """
    issues = []
    cells = nb.get("cells", [])

    if not cells:
        issues.append(Issue(Issue.ERROR, path, "notebook has no cells"))
        return issues

    # Check first cell is markdown with H1
    first = cells[0]
    if first.get("cell_type") != "markdown":
        issues.append(Issue(
            Issue.WARNING, path,
            "first cell should be a markdown cell with the notebook title (# H1)",
            cell_num=1,
        ))
    else:
        src = cell_source(first)
        if not src.strip().startswith("#"):
            issues.append(Issue(
                Issue.WARNING, path,
                "first markdown cell does not start with a # H1 heading (title missing)",
                cell_num=1,
            ))

    # Check for Objectives section
    all_source = "\n".join(cell_source(c) for c in cells)
    if "objective" not in all_source.lower():
        issues.append(Issue(
            Issue.WARNING, path,
            "no 'Objectives' section found (add a ## Learning Objectives markdown cell)",
        ))

    # Check for Overview section
    if "overview" not in all_source.lower() and "introduction" not in all_source.lower():
        issues.append(Issue(
            Issue.WARNING, path,
            "no 'Overview' or 'Introduction' section found",
        ))

    return issues


def check_stale_outputs(nb: dict[str, Any], path: Path) -> list[Issue]:
    """
    Warn about cells that have outputs (indicating the notebook was run and not cleared).
    This is a common git hygiene issue.
    """
    issues = []
    for i, cell in enumerate(nb.get("cells", []), start=1):
        outputs = cell.get("outputs", [])
        exec_count = cell.get("execution_count")

        if outputs:
            issues.append(Issue(
                Issue.WARNING, path,
                f"code cell has {len(outputs)} output(s) — run with --clear-output for git-clean notebooks",
                cell_num=i,
            ))
        elif exec_count is not None:
            issues.append(Issue(
                Issue.WARNING, path,
                f"cell has execution_count={exec_count} but no outputs (partially stale state)",
                cell_num=i,
            ))

    return issues


def check_cell_types(nb: dict[str, Any], path: Path) -> list[Issue]:
    """Check that all cells have valid cell_type values."""
    issues = []
    valid_types = {"code", "markdown", "raw"}
    for i, cell in enumerate(nb.get("cells", []), start=1):
        ct = cell.get("cell_type", "")
        if ct not in valid_types:
            issues.append(Issue(
                Issue.ERROR, path,
                f"invalid cell_type '{ct}' (must be code, markdown, or raw)",
                cell_num=i,
            ))
    return issues


# ---------------------------------------------------------------------------
# Output clearing
# ---------------------------------------------------------------------------


def clear_outputs(nb: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of the notebook with all cell outputs cleared."""
    nb_clean = copy.deepcopy(nb)
    for cell in nb_clean.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
    return nb_clean


# ---------------------------------------------------------------------------
# Per-file validation
# ---------------------------------------------------------------------------


def validate_notebook(path: Path, do_clear: bool = False) -> tuple[list[Issue], bool]:
    """
    Validate a single notebook file.
    Returns (issues, was_modified).
    """
    nb, error = load_notebook(path)
    if error:
        return [Issue(Issue.ERROR, path, error)], False

    issues: list[Issue] = []
    issues.extend(check_json_structure(nb, path))

    # Don't continue with further checks if the structure is broken
    if any(i.severity == Issue.ERROR for i in issues):
        return issues, False

    issues.extend(check_metadata(nb, path))
    issues.extend(check_cell_types(nb, path))
    issues.extend(check_empty_cells(nb, path))
    issues.extend(check_required_cells(nb, path))
    issues.extend(check_stale_outputs(nb, path))

    was_modified = False
    if do_clear:
        has_outputs = any(
            cell.get("outputs") or cell.get("execution_count") is not None
            for cell in nb.get("cells", [])
            if cell.get("cell_type") == "code"
        )
        if has_outputs:
            nb_clean = clear_outputs(nb)
            try:
                path.write_text(json.dumps(nb_clean, indent=1, ensure_ascii=False), encoding="utf-8")
                was_modified = True
            except OSError as e:
                issues.append(Issue(Issue.ERROR, path, f"failed to write cleared notebook: {e}"))

    return issues, was_modified


# ---------------------------------------------------------------------------
# Directory scanning
# ---------------------------------------------------------------------------


def find_notebooks(root: Path) -> list[Path]:
    """Find all .ipynb files under root, skipping hidden directories."""
    notebooks = []
    for p in sorted(root.rglob("*.ipynb")):
        if any(part.startswith(".") for part in p.parts):
            continue
        if ".ipynb_checkpoints" in str(p):
            continue
        notebooks.append(p)
    return notebooks


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="validate_notebooks.py",
        description="Validate Jupyter notebooks in the LEAPS repository.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--dir",
        metavar="DIR",
        default=None,
        help=f"Directory to scan for .ipynb files (default: {REPO_ROOT}).",
    )
    parser.add_argument(
        "--clear-output",
        action="store_true",
        help=(
            "Strip all cell outputs from notebooks (makes them git-friendly). "
            "Files are written in place."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    scan_root = Path(args.dir).resolve() if args.dir else REPO_ROOT
    if not scan_root.exists():
        print(f"ERROR: '{scan_root}' does not exist.", file=sys.stderr)
        return 2

    notebooks = find_notebooks(scan_root)

    print()
    print("  LEAPS — Notebook Validator")
    print("  " + "─" * 50)

    if not notebooks:
        print(f"  No .ipynb files found under {scan_root}")
        print()
        return 0

    print(f"  Found {len(notebooks)} notebook(s)")
    if args.clear_output:
        print("  Mode: clear outputs")
    print()

    all_issues: list[Issue] = []
    cleared_count = 0

    for nb_path in notebooks:
        issues, was_modified = validate_notebook(nb_path, do_clear=args.clear_output)
        all_issues.extend(issues)
        try:
            rel = nb_path.relative_to(REPO_ROOT)
        except ValueError:
            rel = nb_path

        nb_issues = [i for i in issues if i.notebook == nb_path]
        errors = [i for i in nb_issues if i.severity == Issue.ERROR]
        warnings = [i for i in nb_issues if i.severity == Issue.WARNING]

        status = "OK   "
        if errors:
            status = "ERROR"
        elif warnings:
            status = "WARN "
        if was_modified:
            status = "FIXED"
            cleared_count += 1

        print(f"  [{status}] {rel} ({len(errors)} errors, {len(warnings)} warnings)")

    # Print detailed issues
    if all_issues:
        print()
        print("  Issues:")
        for issue in all_issues:
            print(str(issue))

    print()
    error_count = sum(1 for i in all_issues if i.severity == Issue.ERROR)
    warn_count = sum(1 for i in all_issues if i.severity == Issue.WARNING)

    if not all_issues:
        print("  All notebooks valid.")
    else:
        print(
            f"  {len(all_issues)} issue(s): {error_count} error(s), {warn_count} warning(s)."
        )

    if cleared_count:
        print(f"  Cleared outputs from {cleared_count} notebook(s).")

    if not args.clear_output and warn_count > 0:
        print("  Tip: Run with --clear-output to strip stale outputs.")

    print()
    return 1 if error_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
