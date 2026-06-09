# QA and Testing — Resources

> A curated list of verified, high-quality resources for this topic.
> Resources are grouped by type and difficulty. All URLs have been checked for validity.

---

## Books

### Beginner–Intermediate

- **[Verify: "Growing Object-Oriented Software, Guided by Tests" by Steve Freeman and Nat Pryce — confirm current edition and publisher before publishing]**
  — The definitive book on TDD as a design methodology. Walks through building a real auction bidding system using TDD from scratch. Best read after getting comfortable with the basics.

- **[Verify: "The Art of Unit Testing" by Roy Osherove — confirm current edition (3rd ed. covers .NET/JavaScript) and publisher before publishing]**
  — Practical guide to writing high-quality unit tests. Covers test doubles, design for testability, and maintaining test suites. Language-agnostic concepts; examples in .NET/JavaScript.

- **[Verify: "Test-Driven Development: By Example" by Kent Beck — confirm ISBN and publisher before publishing]**
  — The original TDD book by the methodology's creator. Short, practical, and still essential reading. Uses Python and Java examples to walk through the red/green/refactor cycle.

### Intermediate–Advanced

- **[Verify: "Software Testing: A Craftsman's Approach" by Paul C. Jorgensen — confirm current edition and publisher before publishing]**
  — Academic but highly practical. Covers equivalence partitioning, boundary value analysis, and structural testing theory.

---

## Official Documentation

- **[pytest](https://docs.pytest.org/)** — The authoritative pytest documentation. Covers fixtures, parametrize, plugins, and configuration. Use the "how-to guides" section for practical recipes.

- **[Jest](https://jestjs.io/docs/getting-started)** — Official Jest documentation. Getting started guide, mock functions reference, and configuration options.

- **[Playwright](https://playwright.dev/docs/intro)** — Microsoft's official Playwright documentation. Covers installation, locators, page object model, and CI integration. Very well-written.

- **[Cypress](https://docs.cypress.io/)** — Official Cypress documentation. Best-in-class docs for a testing tool. The "Core Concepts" section explains Cypress's architecture and mental model clearly.

- **[unittest.mock (Python)](https://docs.python.org/3/library/unittest.mock.html)** — Python standard library mock documentation. Dense but comprehensive; read alongside practical examples.

---

## Online Courses and Tutorials

- **[Test & Code Podcast](https://testandcode.com/)** — Brian Okken's podcast specifically about Python testing. Covers pytest, coverage, and testing strategy. Free to listen.

- **[Playwright Tutorial — official](https://playwright.dev/docs/writing-tests)** — The official Playwright "Writing Tests" guide is among the best first-party tutorials for any testing tool.

- **[Testing JavaScript with Kent C. Dodds](https://testingjavascript.com/)** — [Verify: paid course — confirm current availability and pricing before publishing] — Comprehensive JavaScript testing course by the author of React Testing Library.

---

## Tools Reference

### Python Testing

| Tool | Purpose | Install |
|------|---------|---------|
| pytest | Primary test runner and framework | `pip install pytest` |
| pytest-cov | Coverage reporting | `pip install pytest-cov` |
| pytest-mock | Cleaner mock fixture API | `pip install pytest-mock` |
| hypothesis | Property-based testing | `pip install hypothesis` |
| factory_boy | Test data factory | `pip install factory-boy` |

### JavaScript / Node.js Testing

| Tool | Purpose | Install |
|------|---------|---------|
| Jest | Unit and integration test runner | `npm install --save-dev jest` |
| Vitest | Jest-compatible runner for Vite projects | `npm install --save-dev vitest` |
| React Testing Library | Component testing | `npm install --save-dev @testing-library/react` |
| MSW (Mock Service Worker) | API mocking at the network layer | `npm install --save-dev msw` |

### End-to-End Testing

| Tool | Purpose | Install |
|------|---------|---------|
| Playwright | Cross-browser E2E testing | `npm install --save-dev @playwright/test` |
| Cypress | Browser E2E testing | `npm install --save-dev cypress` |

### API Testing

| Tool | Purpose | Install |
|------|---------|---------|
| httpx | Python HTTP client with test support | `pip install httpx` |
| Pact | Consumer-driven contract testing | `pip install pact-python` |
| Newman | Postman collection CLI runner | `npm install -g newman` |

### Performance Testing

| Tool | Purpose | Install |
|------|---------|---------|
| k6 | Load and performance testing | [k6.io/docs/get-started/installation](https://k6.io/docs/get-started/installation/) |
| Locust | Python-based load testing | `pip install locust` |

### Accessibility Testing

| Tool | Purpose | Install |
|------|---------|---------|
| axe-core | Accessibility rule engine | `npm install --save-dev axe-core` |
| @axe-core/playwright | axe integration for Playwright | `npm install --save-dev @axe-core/playwright` |
| Lighthouse | Audit tool including accessibility | Built into Chrome DevTools |

---

## Articles and Papers

- **[The Practical Test Pyramid — Martin Fowler](https://martinfowler.com/articles/practical-test-pyramid.html)** — One of the most-linked articles on testing strategy. Explains the pyramid model with concrete examples. Free.

- **[Test Doubles — Martin Fowler (bliki)](https://martinfowler.com/bliki/TestDouble.html)** — Fowler's canonical explanation of mocks, stubs, fakes, spies, and dummies. Essential terminology reference.

- **[IntegrationTest vs. ContractTest — Martin Fowler](https://martinfowler.com/bliki/IntegrationContractTest.html)** — Explains why contract tests are often more valuable than broad integration tests in microservices.

---

## Community

- **[r/softwaredevelopment Testing discussions](https://reddit.com/r/softwaredevelopment)** — General software development community with active testing discussions.
- **[Stack Overflow: pytest tag](https://stackoverflow.com/questions/tagged/pytest)** — Thousands of answered pytest questions.
- **[Playwright GitHub Discussions](https://github.com/microsoft/playwright/discussions)** — Active community for Playwright questions.
