# leaps Prompt Library

> Reusable AI prompt templates for the **Learning Environment for Any Progressive Subject**

This directory contains production-grade prompts for use with any AI assistant (Claude, ChatGPT, Gemini, Copilot, Cursor, and others). Each prompt is designed to work with the leaps repository structure and produces output that conforms to the standards in [`CONTRIBUTING.md`](../CONTRIBUTING.md).

---

## What Prompts Are For

Prompts in this library automate the most time-consuming parts of building and maintaining a leaps knowledge base:

- **Content generation** — Create entire topics, modules, exercises, and tests from scratch
- **Progress management** — Resume learning where you left off, track completions
- **Grading** — Evaluate test answers and record scores in a consistent format
- **Knowledge graph maintenance** — Find and add cross-links between related topics
- **Reinforcement** — Generate spaced-repetition sessions targeting your weak areas
- **Interactive content** — Generate Jupyter notebooks and hands-on labs

Prompts do not replace your judgment. They accelerate the scaffolding work so you can spend your time understanding, not formatting.

---

## How to Use These Prompts

### Method 1: Copy Into an AI Chat

1. Open the prompt file you want
2. Copy the text inside the ```` ``` ```` fenced block under the **Prompt** section
3. Replace all `[PARAMETER_NAME]` placeholders with your actual values
4. Paste into your AI assistant's chat interface
5. Send and review the output

### Method 2: Reference via Claude Code CLI

If you are using Claude Code in this repository:

```bash
# From the repo root, tell Claude to use a prompt template:
# "Use the prompt in PROMPTS/generate-module.md to generate module 4 for the rust topic"
```

Claude Code will read the prompt file, apply your parameters, and execute directly against the repository files.

### Method 3: Chain Prompts for a Full Workflow

Prompts are designed to be chainable. A typical "start a new topic" workflow:

```
1. generate-roadmap.md    → Plan the learning path
2. create-topic.md        → Create the full topic structure
3. generate-module.md     → Fill in each module (repeat)
4. generate-exercises.md  → Expand exercise sets
5. generate-test.md       → Create module tests
6. generate-notebook.md   → Add interactive notebooks
7. knowledge-graph-update.md → Connect to other topics
```

A typical "study session" workflow:

```
1. continue-topic.md         → Resume from last completed module
2. answer-questions.md       → Get answers to your logged questions
3. grade-test.md             → Grade your completed test
4. reinforcement-session.md  → Review weak areas from grading history
```

---

## Parameter Conventions

All prompts use `[PARAMETER_NAME]` syntax for required parameters. Replace the entire `[BRACKET_EXPRESSION]` including the brackets with your value.

| Convention | Meaning |
|---|---|
| `[TOPIC_NAME]` | The topic directory name (e.g., `rust`, `linear-algebra`) |
| `[MODULE_NUMBER]` | Zero-padded module number (e.g., `03`, `10`) |
| `[MODULE_NAME]` | Human-readable module title (e.g., `Traits and Generics`) |
| `[DIFFICULTY_LEVEL]` | One of: `Beginner`, `Intermediate`, `Advanced`, `Expert` |
| `[TOPIC_A]`, `[TOPIC_B]` | Two topics to cross-reference |
| `_OR_ALL` suffix | Pass either a specific value or the literal string `all` |
| `_OR_AUTO` suffix | Pass a specific value or `auto` to let the AI determine it |

---

## Prompt Categories

### Content Creation
Prompts for building new learning material from scratch.

### Learning Continuation
Prompts for resuming and progressing through existing topics.

### Assessment
Prompts for generating and grading tests.

### Knowledge Graph
Prompts for maintaining cross-links and relationships between topics.

### Interactive Content
Prompts for Jupyter notebooks and hands-on labs.

### Reinforcement
Prompts for spaced repetition and targeted review.

---

## Prompt Index

| File | Category | Description |
|---|---|---|
| [`create-topic.md`](create-topic.md) | Content Creation | Create a complete new topic with full directory structure, README, roadmap, and first module |
| [`continue-topic.md`](continue-topic.md) | Learning Continuation | Resume learning in an existing topic from the last completed module |
| [`generate-module.md`](generate-module.md) | Content Creation | Generate a complete module with README, notes, exercises, test, and resources |
| [`generate-test.md`](generate-test.md) | Assessment | Generate a comprehensive multi-tier test for a module or range of modules |
| [`grade-test.md`](grade-test.md) | Assessment | Grade a completed test, record the score, and generate reinforcement recommendations |
| [`answer-questions.md`](answer-questions.md) | Learning Continuation | Read and answer all open questions in a module's QUESTIONS.md |
| [`cross-reference.md`](cross-reference.md) | Knowledge Graph | Find conceptual connections between topics and add bidirectional wiki-links |
| [`generate-notebook.md`](generate-notebook.md) | Interactive Content | Generate a Jupyter notebook with theory, visualizations, and exercises for a module |
| [`generate-exercises.md`](generate-exercises.md) | Content Creation | Expand a module's EXERCISES.md with new problems across difficulty levels |
| [`reinforcement-session.md`](reinforcement-session.md) | Reinforcement | Run a spaced repetition session targeting weak areas from grading history |
| [`generate-lab.md`](generate-lab.md) | Interactive Content | Generate an interactive hands-on lab with step-by-step exercises and expected outcomes |
| [`knowledge-graph-update.md`](knowledge-graph-update.md) | Knowledge Graph | Scan all topics for concepts and update cross-links across the entire repository |
| [`generate-roadmap.md`](generate-roadmap.md) | Content Creation | Generate or update a topic's ROADMAP.md with learning path, milestones, and time estimates |

---

## Adding New Prompts

If you develop a prompt that works well and is reusable across topics, contribute it:

1. Copy the header format from an existing prompt file (the YAML frontmatter block)
2. Name the file descriptively in `kebab-case.md`
3. Fill in all sections: Description, Usage, Prompt, Examples, Notes
4. Add it to the table above in this README
5. Open a PR with type `docs`: `docs: prompts — add [prompt-name] prompt`

**Quality bar for prompts:** A prompt is production-quality if it produces usable output the first time on a topic the prompt author has never worked on. Test your prompt on at least two different topics before contributing it.

---

## Versioning

Prompts are versioned in their YAML frontmatter (`version: 1.0`). When you significantly modify a prompt's behavior, increment the version and add a note in the file's **Notes** section describing what changed. This helps users who have existing workflows know whether to update their usage.

---

*These prompts are part of the leaps repository. See [`CONTRIBUTING.md`](../CONTRIBUTING.md) for contribution guidelines.*
