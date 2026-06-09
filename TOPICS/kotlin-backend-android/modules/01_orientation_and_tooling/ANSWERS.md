# Answers: Module 01 — Orientation and Tooling

## Answer Key

### Easy Questions
**Q1:** The main goal is to understand and apply Orientation and Tooling in the Kotlin backend and Android learning path.
**Q2:** Answers vary; should accurately define a module term such as nullable type, wrapper, source set, DTO, or runtime.
**Q3:** Backend examples include HTTP APIs, persistence, transactions, and monitoring; Android examples include UI, lifecycle, permissions, and device networking.
**Q4:** `./gradlew test`.
**Q5:** Runnable examples let learners verify mental models and catch setup or syntax errors early.

### Medium Questions
**Q6:** Reproducibility ensures the same source and build metadata produce the same result across machines and CI.
**Q7:** A server is long-running and request-oriented; Android is lifecycle-driven and constrained by device resources.
**Q8:** Null-safety forces absence into the type system so external input is checked before unsafe use.
**Q9:** Shared DTOs help when backend and Android must agree on request and response shapes without duplicating contracts manually.
**Q10:** Maven may fit an established backend organization while Gradle is required or conventional for Android.

### Hard Questions
**Q11:** A full-credit answer provides a valid `data class` and returns a copied instance with `completed = true` or equivalent.
**Q12:** The bug is `!!`; a safe fix uses `title?.length ?: 0` or validates before use.
**Q13:** A strong layout separates `src/main`, `src/test`, and any shared module from platform-specific backend or Android modules.
**Q14:** A strong answer includes clear messaging, retry behavior, preserved user intent, and no crash.

### Expert Questions
**Q15:** A strong design covers UI state, network client, DTO contract, Spring controller, service, persistence boundary, validation, and tests at multiple layers.
**Q16:** A strong answer justifies wrapper usage, pinned versions, CI commands, artifact boundaries, and why Gradle, Maven, or both match team constraints.

### Bonus Questions
**Bonus 1:** Accept thoughtful risks such as observability gaps, release signing, API versioning, migration failures, or coroutine cancellation bugs with a credible investigation plan.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
