# Answers: Module 02 — Flask Routing and Views

## Answer Key

### Easy Questions

**Q1:** A route maps an HTTP method and path to code that handles the request.
**Q2:** Flask is small, explicit, and composable.
**Q3:** Django provides integrated batteries such as ORM, admin, auth, and security defaults.
**Q4:** FastAPI provides typed request handling, validation, and OpenAPI documentation.
**Q5:** Validation checks and converts untrusted input before application logic relies on it.

### Medium Questions

**Q6:** A client sends an HTTP request; the framework routes it to a handler; the handler runs application logic; the framework returns a response.
**Q7:** Adapters handle HTTP details while domain logic models business behavior in plain Python.
**Q8:** Methods communicate intent and help clients, servers, caches, and security controls behave correctly.
**Q9:** Mixing persistence, HTTP, and domain behavior in one place makes testing and change harder.
**Q10:** Defaults help when teams need consistent auth, admin, database, and security behavior quickly.

### Hard Questions

**Q11:** A correct answer checks type or truthiness, strips whitespace, and returns a clear success/error result.
**Q12:** Use a state-changing method such as `DELETE /account` with authentication, CSRF/session protection where relevant, and confirmation controls.
**Q13:** Good answers use nouns, ids, and methods such as `GET /notes`, `POST /notes`, and `GET /notes/{id}`.
**Q14:** A good answer isolates the handler with a test client and replaces slow external dependencies with fakes or fixtures.

### Expert Questions

**Q15:** A strong answer justifies Django for admin/product workflows, FastAPI for partner APIs if needed, and explicit boundaries between systems.
**Q16:** A strong answer connects input contracts, routing organization, data transactions, tests, and future framework migration costs.

### Bonus Questions

**Bonus 1:** Good answers include CSRF, injection, auth bypass, insecure secrets, or unsafe deserialization plus a specific mitigation.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
