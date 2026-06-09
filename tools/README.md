# Tools

Third-party integrations, helper configurations, and utility files that make working with **leaps** smoother across different editors and workflows.

---

## Purpose

The files here are not learning content — they are the scaffolding that lets your tools understand and enhance the repository structure. Think of this directory as the "meta-layer": configuration that makes editors smarter, note apps more powerful, and documentation sites prettier.

---

## Supported Tools

### VS Code

Pre-configured settings and extension recommendations for the best VS Code experience with leaps.

| File | Purpose |
|---|---|
| `vscode-settings.json` | Workspace settings (formatting, Markdown, Python) |
| `vscode-extensions.json` | Recommended extension list with descriptions |

**How to use:**
- Copy `vscode-settings.json` to `.vscode/settings.json` at the repo root.
- Copy `vscode-extensions.json` to `.vscode/extensions.json` — VS Code will prompt you to install recommended extensions automatically.

---

### Obsidian

Obsidian treats the leaps repo as a vault. Wiki-links (`[[topic]]`) work natively, and Dataview queries power dashboards across all notes.

| File | Purpose |
|---|---|
| `obsidian-dataview-queries.md` | 10+ ready-to-use Dataview queries for tracking progress |

**How to use:**
1. Open the leaps root as an Obsidian vault.
2. Install the [Dataview](https://github.com/blacksmithgu/obsidian-dataview) community plugin.
3. Copy queries from `obsidian-dataview-queries.md` into any note to build dashboards.

Recommended Obsidian plugins for leaps:
- **Dataview** — query frontmatter and inline fields across all notes
- **Templater** — use the templates in `TEMPLATES/` with variables
- **Calendar** — visualize daily study log entries
- **Excalidraw** — inline diagrams inside notes
- **Git** — sync changes from within Obsidian

---

### Zensical

The leaps knowledge base is published as a [Zensical](https://zensical.org/) book — the modern static-site generator by the Material for MkDocs team.

Configuration lives in `zensical.toml` at the repo root (`docs_dir = "TOPICS"`). The site is built to `site/` and deployed to GitHub Pages on every push to `main` via `.github/workflows/docs.yml`.

```bash
pip install zensical
zensical serve            # local preview with live reload
zensical build --clean    # static site in site/
```

---

## How to Add a New Tool Integration

1. Create the configuration file(s) in this directory.
2. Add a section to this README describing:
   - What the tool is
   - Which files are relevant
   - How to activate/install the configuration
3. If the tool requires a specific directory structure (e.g., `.obsidian/`), document that it lives outside `tools/` and explain why.

---

## Directory Structure

```
tools/
├── README.md                       # This file
├── vscode-settings.json            # VS Code workspace settings
├── vscode-extensions.json          # VS Code extension recommendations
└── obsidian-dataview-queries.md    # Dataview queries for Obsidian dashboards
```
