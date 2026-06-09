# Educational Philosophy of leaps

leaps is not a collection of notes. It is a structured learning environment designed
around what the cognitive science of learning actually says works — not what feels
productive, not what is easy to generate, and not what looks impressive in a README.

This document explains the principles behind every structural and pedagogical decision
in the repository. Understanding it will make you a better contributor, a better learner,
and a better agent.

---

## The Problem with Most Knowledge Bases

Most personal knowledge bases, wikis, and "second brains" share the same failure mode:
they accumulate information without building understanding. Notes pile up. Links
multiply. The graph gets dense. But when you sit down to actually use the knowledge —
to solve a problem, explain a concept, or build something — the notes are not there.

This happens because **recording information is not the same as learning it.**

leaps is designed to close that gap. Every structural choice — modules, exercises,
test questions, spaced repetition hooks, cross-links — exists to make
active retrieval and application possible, not just passive consumption.

---

## Core Principles

### 1. The Spacing Effect

Hermann Ebbinghaus (1885) documented what is now called the **forgetting curve**: memory
for new material decays exponentially unless it is revisited. The countermeasure, backed
by over a century of replication, is **spaced repetition** — reviewing material at
increasing intervals as it becomes consolidated.

leaps supports this through:
- `TEST.md` files in every module, formatted to be exported to Anki or similar SRS tools
- The `progress_report.py` script that surfaces modules not revisited recently
- The `last_reviewed` frontmatter field in module READMEs

**Implication for contributors:** Test questions are not optional boilerplate. They are
the mechanism by which learned material persists.

### 2. The Testing Effect (Active Recall)

Roediger and Karpicke (2006) showed that retrieval practice — attempting to recall
information without looking at it — produces far better long-term retention than
re-reading the same material. This is sometimes called the **testing effect**.

leaps supports this through:
- `EXERCISES.md` files requiring the learner to produce output, not just recognize it
- Test questions that require explanation, not just multiple-choice recognition
- The deliberate structure of modules: learn → apply → test → review

**Implication for contributors:** An exercise that asks "which of these is a closure?"
is less valuable than one that asks "write a closure that..." Prefer production over
recognition wherever possible.

### 3. Interleaved Practice

Blocked practice (mastering one thing completely before moving to the next) feels more
effective than interleaved practice (mixing related topics), but produces worse long-term
retention and transfer. This is the **interleaving effect**, studied extensively by
Robert Bjork and colleagues.

leaps supports this through:
- Cross-links between topics that surface related material from other disciplines
- Learning path recommendations that mix topics rather than running them in pure sequence
- `SHARED/concepts/` files that let learners encounter the same concept in multiple contexts

**Implication for contributors:** When you notice that a concept in one topic appears in
another, add the cross-link. The apparent detour is the point.

### 4. The Feynman Technique

Richard Feynman's reported approach to learning: study a concept, then explain it
as if teaching it to someone with no background in the subject. Where the explanation
breaks down, the understanding is incomplete. Return to the source material and try again.

leaps supports this through:
- The requirement that modules explain concepts, not just list them
- `NOTES.md` files written as if explaining to a peer, not as raw reference material
- The AI agents guide's insistence on depth over surface coverage

**Implication for contributors:** If a module cannot explain why a concept works —
not just what it does — it is incomplete. The word "intuition" in a section heading
is a requirement, not a stylistic choice.

### 5. Desirable Difficulty

Bjork (1994) coined the term **desirable difficulty** for learning conditions that slow
acquisition but improve long-term retention: spaced practice, interleaving, reducing
feedback, generating answers before seeing them. Easy learning feels good but fades fast.

leaps is deliberately hard to passively read. The exercises are not trivial. The test
questions go beyond the obvious. This is by design.

**Implication for contributors:** Do not soften exercises to make them approachable.
Label difficulty honestly (Easy / Medium / Hard / Expert) and make Hard genuinely hard.

### 6. Project-Based Learning

Knowledge applied to a concrete goal is retained and generalized better than knowledge
studied in the abstract. This principle, associated with John Dewey's pragmatist
pedagogy and later with constructivist learning theory, motivates the inclusion of
project-scale exercises in modules.

leaps supports this through:
- Capstone project suggestions at the end of topic READMEs
- Exercises that build runnable artifacts, not just demonstrate syntax
- Learning paths designed to converge on a tangible goal (e.g., "build a compiler")

**Implication for contributors:** The best module exercises end with something the
learner has built or produced, not just answered.

### 7. The Feynman Notebook Method (Learn in Public)

One of the most reliable ways to deepen understanding is to write about what you are
learning as if publishing it. The act of anticipating a reader's confusion forces
precision. Gaps in understanding that survive private note-taking are exposed by the
demand to explain clearly.

This is why leaps is a public repository, not a private vault — and why the course
content is published as a [Zensical](https://zensical.org) book on GitHub Pages for
anyone to read. Contributions are visible. The quality bar is the public bar, not the
"good enough for me" bar.

**Implication for contributors:** Write as if a competent peer will read and critique
every word. Because they might.

### 8. Building Mental Models

A mental model is a simplified internal representation that allows prediction and
reasoning about a system. Good mental models are more valuable than comprehensive
factual coverage. A learner who understands the ownership model in Rust can reason
about unfamiliar code; a learner who memorized ownership rules cannot.

leaps structures modules to build models, not accumulate facts:
- Concept sections explain the underlying why before the how
- Analogies are encouraged (and required to be accurate)
- Common misconceptions are documented alongside correct models

**Implication for contributors:** Every module should leave the learner with at least
one robust mental model that transfers to new situations.

### 9. Connecting Disciplines

The most durable understanding comes from seeing the same idea in multiple contexts.
Transfer learning — the ability to apply knowledge from one domain to another — is
strongly associated with the breadth of contexts in which a concept has been
encountered.

leaps is explicitly cross-disciplinary. The `SHARED/` directory exists to make
cross-topic connections explicit and navigable. The learning paths in `TOPICS/README.md`
cross disciplinary boundaries deliberately.

**Implication for contributors:** When you write about a concept in one topic, look for
its analogues in other topics. The connection between eigenvalues in linear algebra and
principal components in machine learning is not a coincidence — it is the same idea
wearing different clothes.

---

## What leaps Is Not

**leaps is not a reference manual.** Official documentation is better for that.
leaps is for building understanding, not for looking up syntax.

**leaps is not a course.** It has no instructor, no deadlines, and no certificates.
The learner (human or AI) is responsible for their own progression.

**leaps is not a bookmark collection.** Resources are curated and contextualized,
not merely listed. A link without explanation of what it adds and why it matters is
not a contribution.

**leaps is not a proof of work.** The goal is genuine understanding, not a dense
graph of notes that demonstrates effort without transfer.

---

## Selected References

These are real, citable works that ground the principles above.

- Ebbinghaus, H. (1885). *Über das Gedächtnis* (Memory: A Contribution to Experimental
  Psychology). Translated by Ruger & Bussenius, 1913.
- Roediger, H. L., & Karpicke, J. D. (2006). Test-enhanced learning: Taking memory
  tests improves long-term retention. *Psychological Science, 17*(3), 249–255.
- Bjork, R. A. (1994). Memory and metamemory considerations in the training of human
  beings. In J. Metcalfe & A. Shimamura (Eds.), *Metacognition: Knowing about knowing*
  (pp. 185–205). MIT Press.
- Kornell, N., & Bjork, R. A. (2008). Learning concepts and categories: Is spacing the
  "enemy of induction"? *Psychological Science, 19*(6), 585–592.
- Brown, P. C., Roediger, H. L., & McDaniel, M. A. (2014). *Make It Stick: The Science
  of Successful Learning*. Harvard University Press.
- Carey, B. (2014). *How We Learn: The Surprising Truth About When, Where, and Why It
  Happens*. Random House.
- National Academies of Sciences, Engineering, and Medicine. (2018). *How People Learn II:
  Learners, Contexts, and Cultures*. The National Academies Press.
