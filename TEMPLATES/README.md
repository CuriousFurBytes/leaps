# LEAPS Templates

**Learning Environment for Any Progressive Subject** — template index for building structured knowledge bases.

These templates provide a consistent, rich starting point for every unit of learning in the LEAPS system. Copy the relevant template, fill in the placeholders, and begin building your knowledge base immediately.

---

## Template Index

| Template | Path | Purpose | When to Use |
|----------|------|---------|-------------|
| **Topic README** | `topic/README.md` | Main entry point for an entire learning subject | When starting a new top-level topic (e.g., "Linear Algebra", "Rust", "Thermodynamics") |
| **Topic Roadmap** | `topic/ROADMAP.md` | Visual learning path with phases and milestones | After creating the topic README; maps the full study journey |
| **Topic Resources** | `topic/RESOURCES.md` | Curated external resources (books, courses, videos, tools) | At topic creation; updated continuously as you discover good sources |
| **Topic Glossary** | `topic/GLOSSARY.md` | Alphabetical definitions of key terminology | Ongoing; add terms as you encounter them during study |
| **Topic Questions** | `topic/QUESTIONS.md` | Topic-level open questions and big-picture curiosities | Log questions that span multiple modules or are about the field broadly |
| **Topic Projects** | `topic/PROJECTS.md` | Project ideas organized by difficulty tier | When you want to apply what you've learned creatively |
| **Topic Cheatsheet** | `topic/CHEATSHEET.md` | Quick-reference syntax, patterns, and gotchas | After completing most modules; living reference document |
| **Module README** | `module/README.md` | Deep-dive content for one learning module | For every module in a topic; the most important template |
| **Module Notes** | `module/NOTES.md` | Personal study notes and concept maps | During and after studying each module |
| **Module Questions** | `module/QUESTIONS.md` | Module-specific questions as they arise | During study; log anything unclear immediately |
| **Module Exercises** | `module/EXERCISES.md` | Practice problems with graded difficulty and solutions | Alongside module content |
| **Module Test** | `module/TEST.md` | Structured self-assessment test with scoring | After completing module study |
| **Module Answers** | `module/ANSWERS.md` | Answer key — AI-facing, not student-facing | Created with TEST.md; review only after attempting the test |
| **Module Resources** | `module/RESOURCES.md` | Module-specific reference links | For targeted deep dives on module content |
| **Lab README** | `lab/README.md` | Guided hands-on lab with setup and exercises | When creating practical, environment-based experiments |
| **Dockerfile** | `environment/Dockerfile` | Containerized learning environment | For topics requiring specific tool versions or system dependencies |
| **devcontainer.json** | `environment/devcontainer.json` | VS Code Dev Container configuration | To create a one-click reproducible VS Code dev environment |
| **requirements.txt** | `environment/requirements.txt` | Python package dependency list by category | For any topic with Python-based exercises or labs |

---

## Directory Layout

A fully populated topic follows this structure:

```
topics/
└── your-topic-name/
    ├── README.md                       ← topic/README.md
    ├── ROADMAP.md                      ← topic/ROADMAP.md
    ├── RESOURCES.md                    ← topic/RESOURCES.md
    ├── GLOSSARY.md                     ← topic/GLOSSARY.md
    ├── QUESTIONS.md                    ← topic/QUESTIONS.md
    ├── PROJECTS.md                     ← topic/PROJECTS.md
    ├── CHEATSHEET.md                   ← topic/CHEATSHEET.md
    ├── Dockerfile                      ← environment/Dockerfile
    ├── devcontainer.json               ← environment/devcontainer.json
    ├── requirements.txt                ← environment/requirements.txt
    └── modules/
        ├── 00-introduction/
        │   ├── README.md               ← module/README.md
        │   ├── NOTES.md                ← module/NOTES.md
        │   ├── QUESTIONS.md            ← module/QUESTIONS.md
        │   ├── EXERCISES.md            ← module/EXERCISES.md
        │   ├── TEST.md                 ← module/TEST.md
        │   ├── ANSWERS.md              ← module/ANSWERS.md
        │   ├── RESOURCES.md            ← module/RESOURCES.md
        │   └── labs/
        │       └── README.md           ← lab/README.md
        ├── 01-first-concept/
        │   └── ...
        └── 02-second-concept/
            └── ...
```

---

## How to Use These Templates

### Starting a New Topic

1. Create the topic directory: `mkdir -p topics/your-topic-name/modules`
2. Copy `TEMPLATES/topic/README.md` → `topics/your-topic-name/README.md`
3. Search and replace all `{{PLACEHOLDER}}` values with real content
4. Copy and fill in `ROADMAP.md` to plan your module sequence
5. Copy the remaining topic-level files (`RESOURCES.md`, `GLOSSARY.md`, etc.)
6. Create your first module directory and copy `module/README.md` into it

### Starting a New Module

1. Create the module directory: `mkdir -p topics/your-topic/modules/00-module-name`
2. Copy `TEMPLATES/module/README.md` into the new directory
3. Copy `TEMPLATES/module/EXERCISES.md` and `TEMPLATES/module/TEST.md`
4. Fill in the module content as you study; don't wait until you "know enough"

### Setting Up an Environment

1. Copy `TEMPLATES/environment/Dockerfile` and `devcontainer.json` to your topic root
2. Replace `{{TOPIC_NAME}}` with your topic name
3. Customize `requirements.txt` to remove unneeded packages
4. Open the folder in VS Code and choose "Reopen in Container"

---

## Placeholder Convention

All templates use `{{DOUBLE_BRACE}}` syntax for values that must be filled in before use:

| Placeholder | Description |
|-------------|-------------|
| `{{TOPIC_NAME}}` | Human-readable topic name (e.g., "Linear Algebra") |
| `{{TOPIC_SLUG}}` | URL-safe lowercase name (e.g., `linear-algebra`) |
| `{{TOPIC_DESCRIPTION}}` | One-paragraph description of what the topic covers |
| `{{MODULE_NUMBER}}` | Zero-padded module number (e.g., `01`, `02`) |
| `{{MODULE_NAME}}` | Human-readable module title |
| `{{DIFFICULTY}}` | Beginner / Intermediate / Advanced / Expert |
| `{{HOURS}}` | Estimated total study hours for this unit |
| `{{PREREQUISITES}}` | Comma-separated prerequisite topics or modules |
| `{{CREATOR}}` | Original creator, inventor, or primary author of the concept |
| `{{YEAR_CREATED}}` | Year the concept was first formalized or published |
| `{{PREV_MODULE}}` | Directory name of the preceding module |
| `{{NEXT_MODULE}}` | Directory name of the following module |
| `{{YYYY-MM-DD}}` | Today's date in ISO 8601 format |

---

## Wiki-Link Convention

Internal cross-references use Obsidian-style wiki-links: `[[topic-or-module-name]]`.

These render as clickable links in Obsidian and are understood by LEAPS tooling. Always link to the topic or module directory name (slug), not the display name.

```
[[linear-algebra]]          → links to topics/linear-algebra/
[[linear-algebra/module-02-vectors]] → links to a specific module
```

---

## Template Philosophy

- **Rich over sparse.** Templates contain enough structure that removing sections is easier than inventing them from scratch.
- **Learning-first.** Every section is oriented toward building understanding, not just collecting information.
- **Progressive detail.** Start with the topic README and roadmap; fill in module-level detail as you study each one.
- **Honest tracking.** Use scoring and grading tables honestly — the goal is mastery, not the appearance of mastery.
- **Verified resources only.** Never add a book, course, or article you have not personally verified exists and is valuable.

---

## Template Versioning

| Version | Date | Notes |
|---------|------|-------|
| 1.0.0 | 2026-05-22 | Initial full template set |

---

## Contributing Templates

If you improve a template significantly:
1. Update the template in `TEMPLATES/`
2. Add an entry to the version table above
3. Ensure all placeholders follow the `{{PLACEHOLDER}}` convention
4. Do not remove sections — mark optional sections with `_(optional)_` instead
