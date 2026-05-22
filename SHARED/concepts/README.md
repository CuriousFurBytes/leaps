# Shared Concepts

Shared concept files document ideas that are **domain-general**: they recur across multiple
topics in leaps, and each topic's treatment of them is better understood against a common
foundation.

A concept file is not a complete tutorial. It is the distilled core — the mental model,
the vocabulary, and the key distinctions — that a learner should have before (or while)
studying how a specific topic handles the concept. Topic modules link here with phrases
like "See also: [[memory-management]] in SHARED/concepts/".

---

## Index of Concept Files

### Planned

| Concept | Topics That Use It | File |
|---|---|---|
| Memory Management | C, Rust, Python, Operating Systems, Computer Architecture | `memory-management.md` |
| Concurrency & Parallelism | Go, Rust, Python, Operating Systems, Distributed Systems | `concurrency.md` |
| Algorithms & Complexity | All programming topics, Discrete Mathematics | `algorithms-complexity.md` |
| Data Structures | All programming topics | `data-structures.md` |
| Type Systems | Haskell, Rust, TypeScript, Programming Language Theory | `type-systems.md` |
| Error Handling | Python, Rust, Go, JavaScript | `error-handling.md` |
| Abstraction & Modularity | All programming topics, System Design | `abstraction.md` |
| State & Mutation | Python, Rust, Haskell, Operating Systems | `state-and-mutation.md` |
| Recursion | All programming topics, Discrete Mathematics | `recursion.md` |
| I/O and Side Effects | All programming topics, Operating Systems | `io-side-effects.md` |
| Serialization | Python, Rust, Go, Data Engineering, Networking | `serialization.md` |
| Caching | Operating Systems, Networking, Computer Architecture, Web | `caching.md` |
| Probability & Uncertainty | Machine Learning, Statistics, Physics, Economics | `probability-uncertainty.md` |
| Optimization | Machine Learning, Calculus, Algorithms, Operations Research | `optimization.md` |
| Information Theory | Machine Learning, Compression, Cryptography | `information-theory.md` |
| Invariants & Proofs | All programming topics, Mathematics | `invariants-and-proofs.md` |

---

## How to Create a New Concept File

1. Check this index first — the concept may already exist or be planned.
2. Open an issue using the [Content Improvement](../../.github/ISSUE_TEMPLATE/content-improvement.yml)
   template with the path `SHARED/concepts/` and type "Other".
3. Create the file `SHARED/concepts/<concept-name>.md` following the structure below.
4. Add a row to the index table above.
5. Add `[[<concept-name>]]` cross-links in every topic module that uses the concept.

### Concept File Structure

```markdown
# <Concept Name>

> One-sentence definition that a newcomer could use.

## Core Idea

The essential mental model in 2-4 paragraphs. No jargon without definition.
Prefer analogies. Prefer concrete examples over abstract ones.

## Key Distinctions

Common confusions and how to resolve them.
(e.g., "concurrency vs. parallelism", "heap vs. stack allocation")

## How Different Topics Approach This

### In [Topic A](../../TOPICS/topic-a/)
Brief treatment specific to that topic.

### In [Topic B](../../TOPICS/topic-b/)
Brief treatment specific to that topic.

## Common Mistakes

What learners (and AI agents) get wrong about this concept.

## Further Reading

- Link to primary source or canonical reference
- Link to the relevant leaps topic module(s)
```

---

## Design Principles

**Accuracy over completeness.** A concept file that is correct but brief is more
valuable than one that is comprehensive but contains errors. If you are uncertain,
say so explicitly and leave a `<!-- TODO: verify -->` comment.

**No duplication.** If a topic module explains a concept thoroughly, the concept file
should summarize and link to it — not copy it.

**Cross-link aggressively.** Every concept file should link to every topic module that
uses or extends the concept. This is what makes leaps a knowledge graph rather than a
collection of isolated notes.
