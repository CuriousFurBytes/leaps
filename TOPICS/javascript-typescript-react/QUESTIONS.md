# JavaScript, TypeScript and React — Questions

> This file tracks big-picture, cross-module questions about JavaScript, TypeScript, and React.
> For questions specific to a single module, use that module's `QUESTIONS.md` instead.

---

## How to Use This File

1. **Write questions immediately** — when something is confusing, log it here before moving on.
2. **Be specific** — "I don't understand closures" is less useful than "Why does a closure still hold a reference to a variable after the outer function returns?"
3. **Update status** as you find answers — partial answers count.
4. **Link your answers** to the module or resource where you found the explanation.
5. **Add follow-up questions** — good answers often raise better questions.

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| 🔴 | Unanswered — needs research |
| 🟡 | Partial — have some understanding but still unclear |
| 🟢 | Answered — well understood |
| ⏸ | Deferred — not urgent; revisit later |

---

## Question Format

```markdown
### Q{{N}}: {{QUESTION_TITLE}}

**Asked:** {{YYYY-MM-DD}}
**Status:** 🔴 Unanswered

**Full question:**
Write the question in full. Include context about what prompted it.

**My current hypothesis:**
What do you think the answer might be, even if you're not sure?

**Answer:**
_To be filled in_

**Source:**
_Where did you find/confirm the answer?_

**Follow-up questions:**
- _Any new questions this answer raised_
```

---

## Questions

### Q001: When should I use TypeScript instead of plain JavaScript?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
TypeScript adds types but also adds complexity (tsconfig, build step, type errors).
Is it always worth it? Are there cases where plain JavaScript is a better choice?

**My current hypothesis:**
TypeScript seems better for large teams and large codebases. Maybe JavaScript is fine for small scripts and prototypes?

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- How hard is it to add TypeScript to an existing JavaScript project?
- Does TypeScript actually catch real bugs in practice, or is it mostly documentation?

---

### Q002: What is the difference between React and a full framework like Angular or Vue?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
React is called a "library" not a "framework". What does that actually mean in practice?
What does React not provide that a framework like Angular provides?

**My current hypothesis:**
React handles the UI rendering part only. Things like routing and data fetching require separate libraries, which gives more flexibility but also more choices to make.

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- Is the React ecosystem (React + Router + React Query + Vite) collectively a framework?
- When would I choose Vue or Angular over React?

---

### Q003: How does the JavaScript event loop actually work?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
JavaScript is single-threaded but handles async code. How does it actually do this without blocking?
What is the difference between the task queue and the microtask queue?

**My current hypothesis:**
I think the browser runs timers and network requests in the background and then calls our callbacks when done. But I don't understand the ordering rules.

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- Why do Promise callbacks always run before setTimeout callbacks, even with setTimeout(fn, 0)?
- How does React's batched state updates interact with the event loop?

---

### Q004: What are React hooks and why did they replace class components?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
I keep seeing references to "before hooks" and "after hooks". What problem did hooks solve?
Why can't you use hooks inside conditions or loops?

**My current hypothesis:**
Hooks make it easier to share stateful logic between components. Class components required patterns like HOCs and render props that were confusing.

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- Are class components deprecated or just discouraged?
- What does React internally use to track hook call order?

---

### Q005: What is the difference between SSR, SSG, and CSR in the context of Next.js?

**Asked:** 2026-06-09
**Status:** 🔴 Unanswered

**Full question:**
Next.js supports Server-Side Rendering, Static Site Generation, and Client-Side Rendering.
When should I use each? What are the performance and SEO tradeoffs?

**My current hypothesis:**
SSG is fastest for content that doesn't change. SSR is needed for dynamic content that changes per user. CSR is the default React model but bad for SEO.

**Answer:**
_To be filled in_

**Source:**
_To be filled in_

**Follow-up questions:**
- What is ISR (Incremental Static Regeneration) and how does it fit in?
- What are React Server Components and how do they differ from SSR?

---

_Add new questions above this line. Keep them numbered sequentially._

---

## Resolved Questions Archive

_Move fully answered questions (🟢) here to keep the active list manageable._

_(none yet)_

---

## Question Stats

| Status | Count |
|--------|-------|
| 🔴 Unanswered | 5 |
| 🟡 Partial | 0 |
| 🟢 Answered | 0 |
| ⏸ Deferred | 0 |
| **Total** | **5** |
