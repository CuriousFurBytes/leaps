# Projects — Module 01: Introduction to APIs

> These projects are scoped to the concepts covered in Module 01.
> For the full topic project list spanning all difficulty levels, see the [topic-level PROJECTS.md](../../PROJECTS.md).

---

## Module-Appropriate Projects

These projects are designed to reinforce Module 01's concepts: HTTP anatomy, REST constraints,
making API calls, and understanding over/under-fetching.

---

### P1: API Explorer CLI Tool [Beginner]

**Description:** Build a command-line tool that accepts a GitHub username as an argument and
prints a summary: the user's name, bio, number of public repos, and their 3 most recently
updated repository names. No authentication required (public data).

**Concepts from this module:**
- Making GET requests with Python `requests`
- Parsing JSON responses
- Reading status codes and handling 404 gracefully
- Understanding that `GET /users/{username}` and `GET /users/{username}/repos` are two separate REST resources

**Estimated Time:** 3–5 hours

**Starting Point:** Blank Python file. Start with `requests.get("https://api.github.com/users/torvalds")` and inspect the response.

**Success Criteria:**
- [ ] Accepts a username as a command-line argument (`python explorer.py torvalds`)
- [ ] Prints name, bio, public repo count
- [ ] Lists 3 most recently updated repositories
- [ ] Handles the case where the user doesn't exist (404) with a friendly message
- [ ] Code is commented and readable

---

### P2: REST API Design Document [Beginner]

**Description:** Choose a domain you know well (a podcast app, a fitness tracker, a library,
a restaurant ordering system). Write a REST API design document that defines the resource model,
URI structure, HTTP methods, and example request/response pairs for at least 5 endpoints.
No code required — this is a design exercise.

**Concepts from this module:**
- REST uniform interface constraint
- Resource identification with URIs
- HTTP method semantics
- Thinking in nouns (resources) not verbs (actions)

**Estimated Time:** 2–4 hours

**Starting Point:** Blank Markdown document. Start by listing all the "things" (resources) in your domain.

**Success Criteria:**
- [ ] At least 5 distinct REST endpoints defined
- [ ] All URI use noun-based plural naming (no `/getX`, no `/doY`)
- [ ] Correct HTTP methods for each operation
- [ ] Example request and response JSON for each endpoint
- [ ] Correct status codes documented for success and the most likely error case

---

### P3: HTTP Transaction Logger [Intermediate]

**Description:** Write a Python script that uses the `requests` library to make 5–10 API calls
to different public APIs, and logs each transaction to a file. Each log entry should include:
timestamp, method, URL, status code, response time (in ms), and whether the response was
cached (check the `Age` or `X-Cache` headers if present).

**Concepts from this module:**
- HTTP request anatomy
- Status codes in the wild
- HTTP headers (especially caching-related ones)
- Practical use of the `requests` library

**Estimated Time:** 4–6 hours

**Starting Point:** Install `requests`. Try `curl -v https://jsonplaceholder.typicode.com/posts/1` first to see what headers come back.

**Success Criteria:**
- [ ] Makes at least 5 API calls to at least 2 different public APIs
- [ ] Logs each transaction with all required fields
- [ ] Measures and logs response time
- [ ] At least one log entry shows a non-200 status code (use `/posts/99999` on JSONPlaceholder)
- [ ] Comments explain what each significant header means

---

## Project Attempt Template

When you attempt a project, fill in this template:

```markdown
# Project: [Name]

**Started:** YYYY-MM-DD
**Completed:** YYYY-MM-DD
**Time Spent:** N hours

## What I Built
[Description]

## Link / Location
[GitHub repo or file path]

## What I Learned
- [Learning 1]
- [Learning 2]

## What Was Hard
[What challenged you and how you worked through it]

## What I'd Do Differently
[Honest retrospective]
```
