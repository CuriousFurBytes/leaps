# Shared Resources

This directory contains material that belongs to leaps as a whole rather than to any
single topic. When a concept, definition, or reference appears in more than one topic,
it lives here so that every topic can link to a single authoritative source rather than
duplicating (and potentially contradicting) itself.

---

## Directory Structure

```text
SHARED/
├── concepts/        Cross-topic concept files (memory management, concurrency, etc.)
├── glossary/        Definitions of terms used across multiple topics
└── references/      Bibliographic references cited in more than one topic
```

---

## concepts/

Concept files document ideas that are **domain-general** — they appear in multiple
disciplines and are best understood by seeing how each field treats them.

Examples: memory management appears in C, Rust, Python, and Operating Systems.
Concurrency appears in Go, Rust, Operating Systems, and Distributed Systems.
A shared concept file gives the foundational view so individual topic modules can
link to it and focus on the topic-specific perspective.

See [concepts/README.md](concepts/README.md) for the full index and contribution guide.

---

## glossary/

Definitions of terms that are used across topics. Prefer linking to a glossary entry
over redefining a term inside a topic module — consistency matters when AI agents
and human learners are building mental models across the whole repository.

Each glossary file covers a domain:
- `programming.md` — terms common to all programming topics
- `mathematics.md` — mathematical vocabulary
- `systems.md` — OS, networking, and hardware terms
- `ml-ai.md` — machine learning and AI vocabulary

---

## references/

Bibliographic entries for books, papers, and courses cited in more than one topic.
Keeping references here prevents link rot from propagating across multiple topics when
an URL changes or a book title needs a correction.

Format: each entry is a YAML block with `id`, `title`, `authors`, `year`, `url`, and
`notes` fields. Topics reference entries by id using the `cite:` shorthand.

---

## When to Put Something in SHARED

Put material in SHARED when:

- The same concept or definition would otherwise be written in two or more topic modules
- A resource (book, paper, course) is cited by two or more topics
- A mental model or technique is discipline-agnostic (e.g., debugging methodology,
  reading documentation, approaching an unfamiliar codebase)

Do **not** put material in SHARED if it is genuinely specific to one topic — keep it
in that topic's directory so context is preserved.
