# Answers: Module 12 — Capstone API Platform

## Answer Key

### Easy Questions
**Q1:** An API contract is the durable agreement covering inputs, outputs, errors, side effects, and compatibility expectations.
**Q2:** HTTP metadata matters for caching, content negotiation, authentication, tracing, and error interpretation.
**Q3:** A representation is the serialized form of a resource or object returned to a client, commonly JSON.
**Q4:** Query, mutation, or subscription.
**Q5:** Authorization, validation, caching, latency, observability, compatibility, or abuse resistance.

### Medium Questions
**Q6:** REST is an architectural style around resources, representations, uniform interfaces, statelessness, and cacheability; JSON is only a format.
**Q7:** Resource design starts from stable identities and HTTP semantics; graph schema design starts from typed objects, fields, and client-selected traversal.
**Q8:** Flexible clients can ask for many shapes, so servers need cost controls, batching, authorization checks, and better observability.
**Q9:** A strong error includes a machine-readable type, human message, relevant fields, and no sensitive leakage.
**Q10:** Compatibility requires additive changes, deprecation windows, stable semantics, and tests that protect existing clients.

### Hard Questions
**Q11:** Full credit includes a method such as `GET /articles/123`, success body, relevant status codes, and headers or error behavior.
**Q12:** Full credit includes a valid query with variable or literal ID and nested author name selection.
**Q13:** The design mutates state through GET and action naming; use `PATCH /articles/123` with a body and proper authorization/error semantics.
**Q14:** Full credit explains cursor or stable keyset pagination and avoids fragile offset-only assumptions for changing datasets.

### Expert Questions
**Q15:** Full credit covers additive REST fields, GraphQL nullable additions or new fields, deprecation, documentation, contract tests, and client communication.
**Q16:** Full credit covers metrics, logs, traces, rate limits, authorization, caching or batching, query complexity, alerts, and runbook behavior.

### Bonus Questions
**Bonus 1:** Full credit compares gateway routing/cross-cutting policy with BFF client-specific composition and discusses team ownership tradeoffs.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
