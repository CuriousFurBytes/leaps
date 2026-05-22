---
name: Cross Reference
category: Knowledge Graph
version: 1.0
parameters:
  - name: TOPIC_A
    description: The first topic directory name
    example: rust
  - name: CONCEPT_A
    description: The specific concept in Topic A to cross-reference (or "all" to scan the entire topic)
    example: ownership
  - name: TOPIC_B
    description: The second topic directory name
    example: cpp
  - name: CONCEPT_B
    description: The specific concept in Topic B to cross-reference (or "all" to scan the entire topic)
    example: raii
---

# Cross Reference

## Description

Finds conceptual connections between two topics (or specific concepts within those topics), adds bidirectional wiki-links at the appropriate points in both topics' content, and optionally creates a comparison document in `SHARED/` that explains the relationship in depth. This prompt is the primary mechanism for growing the leaps knowledge graph.

Running this prompt on two related topics transforms isolated learning paths into a connected understanding — readers studying one topic will naturally discover related material in the other.

## Usage

1. Copy the prompt text below
2. Replace all four parameters with your values
3. To scan an entire topic rather than a specific concept, set `CONCEPT_A` or `CONCEPT_B` to `"all"`
4. Paste into your AI assistant with access to this repository

## Prompt

```
You are a leaps knowledge graph agent. Your task is to find conceptual connections between two topics and create bidirectional cross-links.

## Parameters
- TOPIC_A: [TOPIC_A]
- CONCEPT_A: [CONCEPT_A]
- TOPIC_B: [TOPIC_B]
- CONCEPT_B: [CONCEPT_B]

## Step 1: Read Both Topics

Read the following files for TOPIC_A:
1. `TOPICS/[TOPIC_A]/README.md`
2. If CONCEPT_A is "all": read all module README.md files in `TOPICS/[TOPIC_A]/modules/`
3. If CONCEPT_A is a specific concept: find which module covers it and read that module's README.md and NOTES.md

Read the following files for TOPIC_B:
1. `TOPICS/[TOPIC_B]/README.md`
2. If CONCEPT_B is "all": read all module README.md files in `TOPICS/[TOPIC_B]/modules/`
3. If CONCEPT_B is a specific concept: find which module covers it and read that module's README.md and NOTES.md

Also read:
- `SHARED/concepts.md` — to identify concepts already in the shared knowledge base
- `SHARED/glossary.md` — to identify terms already in the global glossary

## Step 2: Concept Inventory

List every significant concept from each topic that you read. For each concept, record:
- Name
- Which file/section it appears in
- A one-sentence description of what it is

This inventory is the foundation for finding connections.

## Step 3: Find Conceptual Connections

Compare the two concept inventories and identify connections. A connection exists when:

### Type 1: Same Concept, Different Syntax/Domain
The two topics implement or express the same underlying idea. Examples:
- Rust closures ↔ Python lambda functions (both are anonymous functions capturing variables)
- Calculus chain rule ↔ automatic differentiation in machine learning (same math, different application)
- Go interfaces ↔ Rust traits (both are structural subtyping mechanisms)

### Type 2: Prerequisite Relationship
One concept in Topic A is foundational to understanding a concept in Topic B, or vice versa:
- Linear algebra vector spaces → machine learning feature spaces
- C pointer arithmetic → Rust raw pointers
- Set theory → SQL JOIN semantics

### Type 3: Contrast / Trade-off Pair
Two concepts represent alternative approaches to the same problem:
- Rust ownership vs. C++ RAII vs. Python garbage collection (memory management approaches)
- Go goroutines vs. Rust async/await (concurrency models)
- Eager evaluation vs. lazy evaluation

### Type 4: Analogical Connection
One concept is best understood by analogy to a concept in another domain:
- CPU cache hierarchy ↔ memory access patterns in algorithm design
- Hash tables ↔ dictionary lookup in natural language

### Connection Strength

Rate each connection:
- **Strong (must link):** The concepts are so related that not linking them actively harms understanding
- **Medium (should link):** The connection adds real value and would help most learners
- **Weak (optional):** The connection is real but only adds value for advanced learners or in specific contexts

Only add wiki-links for Strong and Medium connections. Document Weak connections in the comparison section without adding links to module files.

## Step 4: Plan the Cross-Links

For each Strong and Medium connection, determine:

1. **Which exact files to modify** in Topic A
2. **Which exact location within those files** to add the link (which paragraph, which sentence)
3. **How to phrase the reference** — the link should appear naturally in the prose, not be bolted on
4. **Which exact files to modify** in Topic B
5. **The reciprocal link location and phrasing** in Topic B

A good cross-link looks like this in prose:

```markdown
Rust's ownership system prevents memory leaks and dangling pointers at compile time — 
a similar goal to C++'s RAII (Resource Acquisition Is Initialization) pattern 
(see [[cpp#raii]]), but enforced by the compiler rather than by programmer discipline.
```

A bad cross-link just appends a bullet point at the bottom of a file:
```markdown
**Related:** [[cpp]]
```

Prefer in-prose links that appear naturally and explain the relationship. Only use a standalone "See also:" reference if you cannot find a natural place in the prose.

## Step 5: Add Cross-Links to Topic A Files

For each file in Topic A that needs a cross-link:

1. Read the current file content
2. Identify the exact sentence or paragraph where the link should appear
3. Insert the wiki-link naturally into the existing prose
4. If no good insertion point exists in existing prose, add a "See also" callout after the relevant section:

```markdown
> [!TIP]
> This concept has a close parallel in [[TOPIC_B#relevant-section]]. Compare the two approaches to deepen your understanding.
```

5. Write the updated file

Rules:
- Do not add the same link twice to the same file
- Do not add a link to a concept that does not yet exist in Topic B (if the module is a stub)
- After inserting, verify the wiki-link syntax is correct: `[[topic-b]]`, `[[topic-b#section-heading]]`, `[[topic-b/module-slug]]`

## Step 6: Add Cross-Links to Topic B Files

Perform the same process for Topic B — add reciprocal links back to Topic A.

The reciprocal link should be phrased differently from the Topic A link. Two files that just say "see the equivalent concept in [[other-topic]]" are not useful. Each link should explain the relationship from its topic's perspective.

## Step 7: Update SHARED/concepts.md

For each Strong connection found in Step 3, check whether the concept already has an entry in `SHARED/concepts.md`. If not, add an entry:

```markdown
## [Concept Name]

**Found in:** [[TOPIC_A#section]], [[TOPIC_B#section]]

**Core idea:** [1–2 sentence description of the underlying concept that both topics share]

**How it manifests in [TOPIC_A]:** [1 sentence]

**How it manifests in [TOPIC_B]:** [1 sentence]

**Key difference:** [What makes each topic's version unique]
```

## Step 8: Create Comparison Content (for Strong connections)

For each Strong connection where the comparison is substantial enough to warrant its own document, create a comparison file in `SHARED/`:

File path: `SHARED/compare-[concept-slug]-[topic-a]-vs-[topic-b].md`

Structure:
```markdown
# Comparing [Concept]: [TOPIC_A] vs. [TOPIC_B]

**TL;DR:** [2-sentence summary of the key difference]

---

## The Shared Problem

[What problem do both approaches solve? Why does this concept exist in both topics?]

## How [TOPIC_A] Approaches It

[Detailed explanation with code/examples from TOPIC_A's perspective]

## How [TOPIC_B] Approaches It

[Detailed explanation with code/examples from TOPIC_B's perspective]

## Side-by-Side Comparison

[Table or code comparison showing the same concept expressed in both topics]

## When to Use Each

[Guidance on choosing between them, or when each is appropriate]

## What One Approach Teaches You About the Other

[The meta-insight: what understanding one deepens about the other]

## References

- [[TOPIC_A#relevant-module]]
- [[TOPIC_B#relevant-module]]
```

## Step 9: Run the Link Validator

After all modifications, note which files were changed so the user can run:
```bash
./SCRIPTS/lint.sh --links-only
```
to verify all added wiki-links resolve correctly.

## Step 10: Output Summary

Produce a structured summary:

```
---
CROSS-REFERENCE COMPLETE: [TOPIC_A]/[CONCEPT_A] ↔ [TOPIC_B]/[CONCEPT_B]
Date: [DATE]

CONNECTIONS FOUND:
Strong (linked): [N]
Medium (linked): [N]
Weak (documented only): [N]

FILES MODIFIED:
[TOPIC_A]
  - [file path]: [what was added]
  - ...

[TOPIC_B]
  - [file path]: [what was added]
  - ...

SHARED/ UPDATES:
  - concepts.md: [N] entries added/updated
  - [comparison file]: created (if applicable)

CONNECTION SUMMARY:
1. [CONCEPT_A] in [TOPIC_A] ↔ [CONCEPT_B] in [TOPIC_B]: [Type] — [1-sentence description]
2. [...]

LINKS TO VERIFY (run ./SCRIPTS/lint.sh):
  - [[wiki-link-1]]
  - [[wiki-link-2]]
---
```

## Important Rules

1. **Read before writing.** Never modify a file without first reading its current content.
2. **Preserve all existing content.** Only add to files — never remove or restructure existing content.
3. **Add links naturally.** An added link should read as if it was always there. Avoid "ADDED LINK:" comments.
4. **Do not link to stubs.** If the target module is a stub (empty or near-empty README), note this in the output but do not add the link — broken links are worse than missing links.
5. **Both directions.** A cross-link is only complete when both topics reference each other.
6. **Do not over-link.** If a connection is weak or the topics are only tangentially related, skip it. A few high-quality links are more valuable than many low-quality ones.
```

## Examples

**Cross-reference specific concepts:**
```
TOPIC_A: rust
CONCEPT_A: ownership
TOPIC_B: cpp
CONCEPT_B: raii
```
Output: Finds the connection between Rust ownership and C++ RAII, adds bidirectional links, creates a SHARED/compare document.

**Cross-reference entire topics:**
```
TOPIC_A: calculus
CONCEPT_A: all
TOPIC_B: machine-learning
CONCEPT_B: all
```
Output: Full scan of both topics, finds all Strong/Medium connections (e.g., derivatives ↔ backpropagation, optimization ↔ gradient descent), adds links throughout.

**Cross-reference Go and Rust concurrency:**
```
TOPIC_A: go
CONCEPT_A: goroutines
TOPIC_B: rust
CONCEPT_B: async-await
```
Output: Compares Go's CSP model with Rust's async/await, creates comparison document, adds links in both concurrency module READMEs.

## Notes

- This prompt works best when both topics have at least 3 modules with substantive content. Running it on stub topics produces low-quality connections.
- For large topics (10+ modules), the scan is time-consuming. Consider narrowing with specific concepts rather than "all" for the first pass.
- The comparison documents in SHARED/ become some of the most valuable files in the repository — they represent synthesized understanding that neither topic alone can provide.
- Running this prompt repeatedly as both topics gain more content is productive. New modules in one topic often reveal new connections to the other.
