# Exercises — Module 01: Introduction to APIs

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Don't just run code mentally — actually type and run your attempt.
3. **Check your answer** against the acceptance criteria, not just the solution code.
4. **Score yourself honestly** in the [Scoring Log](#scoring-log) at the bottom.
5. If you're stuck after a genuine effort, use the hints one at a time — not all at once.

---

## Difficulty Legend

| Symbol | Difficulty | Expected Time | Points |
|--------|-----------|--------------|--------|
| 🟢 Easy | Recall and basic application | 5–10 min | 1 pt |
| 🟡 Medium | Requires combining 2+ concepts | 15–25 min | 2 pts |
| 🔴 Hard | Multi-step, requires real problem-solving | 30–60 min | 3 pts |
| ⭐ Challenge | Open-ended; more than one good answer | 60+ min | 5 pts |

---

## Exercise 1: Annotate an HTTP Transaction [🟢 Easy] [1 pt]

### Context
Understanding the anatomy of HTTP requests and responses is fundamental — every API interaction
is an HTTP transaction. This exercise confirms you can read and interpret one.

### Task
Below is a raw HTTP exchange. Annotate each line with what it represents — identify the method,
URL, headers, status code, and body sections.

```
POST /api/v1/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJSUzI1NiJ9...
Content-Length: 67

{"name": "Bob Smith", "email": "bob@example.com", "role": "editor"}

---

HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/users/99
Date: Mon, 09 Jun 2026 10:00:00 GMT

{"id": 99, "name": "Bob Smith", "email": "bob@example.com", "role": "editor"}
```

**Write your annotation in comments or in a separate document. For each line, state:**
1. What part of the request/response is it?
2. What does its value mean in this specific context?

### Requirements
- [ ] Identify all 4 parts of the request (method, URL+protocol, headers, body)
- [ ] Identify what `Authorization: Bearer ...` is for
- [ ] Explain the meaning of `201 Created`
- [ ] Explain what the `Location` header tells the client

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

The request has: a request line (method + URL + HTTP version), headers (one per line until blank line),
a blank line, and a body.

</details>

### Expected Output / Acceptance Criteria
Your annotation correctly identifies:
- `POST` as the HTTP method meaning "create a new resource"
- `/api/v1/users` as the resource being acted upon
- `Content-Type: application/json` as declaring the body format
- `Authorization: Bearer ...` as carrying authentication credentials
- `201 Created` as the success code for resource creation
- `Location: /api/v1/users/99` as pointing to the newly created resource

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

```
# REQUEST
POST /api/v1/users HTTP/1.1
# ↑ Method: POST = create a new resource
# ↑ Resource: /api/v1/users = the users collection
# ↑ Protocol: HTTP/1.1

Host: api.example.com
# ↑ Required header: tells the server which virtual host to serve

Content-Type: application/json
# ↑ Declares the body format — the server must parse it as JSON

Authorization: Bearer eyJhbGciOiJSUzI1NiJ9...
# ↑ Authentication credentials — a JWT Bearer token

Content-Length: 67
# ↑ Size of the request body in bytes

                              ← blank line separates headers from body
{"name": "Bob Smith", "email": "bob@example.com", "role": "editor"}
# ↑ Request body: the data to create the new user

# RESPONSE
HTTP/1.1 201 Created
# ↑ Status code 201 = a new resource was successfully created

Content-Type: application/json
# ↑ Response body is JSON

Location: /api/v1/users/99
# ↑ Points to the URL of the newly created resource
# ↑ The client can navigate to this URL to read the resource

{"id": 99, "name": "Bob Smith", "email": "bob@example.com", "role": "editor"}
# ↑ The created resource, including the server-assigned ID
```

**Explanation:**
The request follows REST conventions: POST to a collection resource (`/users`) with a JSON body
describing the new resource. The response uses 201 (not 200) to indicate creation, and includes
a `Location` header pointing to where the created resource lives — this is the standard REST
pattern for POST responses.

</details>

---

## Exercise 2: Identify REST Constraint Violations [🟢 Easy] [1 pt]

### Context
An API that violates REST constraints isn't necessarily bad — but understanding which constraints
it violates and why helps you reason about the tradeoffs.

### Task
For each API design below, identify which REST constraint(s) it violates and why.

**API Design A:**
```
POST /api/do-action
Body: {"action": "get_user", "userId": 42}
```

**API Design B:**
```
GET /api/users?session_id=abc123
```
*(The server looks up `abc123` in a session store to identify the user)*

**API Design C:**
```
GET /api/users/42
Response: HTTP 200 OK
Body: {"success": false, "error": "User not found"}
```

### Requirements
- [ ] Identify at least one violated constraint for each design
- [ ] Explain why each is a violation

### Hints
<details>
<summary>Hint 1</summary>

For Design A: think about the "uniform interface" constraint. What does REST say about how
resources should be addressed and how operations should be expressed?

For Design B: which constraint is specifically about the server not storing information about
the client between requests?

For Design C: which constraint requires self-descriptive messages? What does the HTTP status
code communicate here?

</details>

### Expected Output / Acceptance Criteria
Correct identification of at least one violation per design, with accurate reasoning.

### Solution
<details>
<summary>Show Solution</summary>

**Design A** violates the **Uniform Interface** constraint.
REST says resources are identified by URIs and operations are expressed using HTTP methods.
Using `POST /do-action` with an `action` parameter in the body is RPC-over-HTTP, not REST.
The correct REST design: `GET /users/42` — use the HTTP method to express the operation,
and the URI to identify the resource.

**Design B** violates the **Statelessness** constraint.
The server stores session state (the mapping `abc123 → user identity`) separately from the
request. The request alone doesn't contain all information needed to identify the client.
A stateless alternative: `GET /api/users/42` with `Authorization: Bearer <jwt_token>`,
where the token itself carries identity information and the server validates it without
a session store.

**Design C** violates the principle of **self-descriptive messages** (part of Uniform Interface)
and misuses HTTP status codes.
The server returns HTTP 200 (success) with an error in the body. The HTTP status code is
part of the message's self-description — it communicates whether the operation succeeded.
Returning 200 for a "not found" case means HTTP-level tooling (caches, monitors) can't
distinguish a success from a failure. The correct response: HTTP 404 Not Found with the error
in the body.

</details>

---

## Exercise 3: Make Real API Calls with Python [🟡 Medium] [2 pts]

### Context
Translating concepts to working code is how they become durable skills. This exercise has you
make several API calls, handle different response codes, and work with the data — applying the
HTTP anatomy from the module.

### Task
Write a Python script that does the following, using the JSONPlaceholder API:

1. Fetch the first 5 posts (`GET /posts?_limit=5`)
2. For each post, print: the post title and the user ID (from the `userId` field)
3. Fetch the user for the first post only (`GET /users/{userId}`)
4. Print the user's name and company name (`user['company']['name']`)
5. Handle the case where a resource returns 404 (simulate with `/users/99999`)

### Requirements
- [ ] Uses Python `requests` library
- [ ] Correctly uses `response.json()` to parse responses
- [ ] Handles 404 separately from other errors (not just `raise_for_status()` for everything)
- [ ] All print output is labelled (not just raw values)
- [ ] Code has at least one comment explaining non-obvious parts

### Hints
<details>
<summary>Hint 1</summary>

The endpoint `GET https://jsonplaceholder.typicode.com/posts?_limit=5` returns a list of
5 posts as a JSON array. Use `response.json()` to get a Python list.

</details>

<details>
<summary>Hint 2</summary>

To get the user ID from a post: `post['userId']`. To build the user URL:
`f"https://jsonplaceholder.typicode.com/users/{user_id}"`.

</details>

### Expected Output / Acceptance Criteria
```
=== First 5 Posts ===
1. "sunt aut facere..." (user: 1)
2. "qui est esse" (user: 1)
3. "ea molestias quasi..." (user: 1)
4. "eum et est occaecati" (user: 1)
5. "nesciunt quas odio" (user: 1)

=== Author of Post 1 ===
Name: Leanne Graham
Company: Romaguera-Crona

=== Testing 404 Handling ===
User 99999 not found (404)
```

### Solution
<details>
<summary>Show Solution</summary>

```python
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def fetch_user(user_id: int) -> dict | None:
    """Fetch a user by ID. Returns None if not found (404)."""
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    if response.status_code == 404:
        return None
    response.raise_for_status()    # Raise for 5xx, 429, etc.
    return response.json()

# Step 1 & 2: Fetch first 5 posts
response = requests.get(f"{BASE_URL}/posts", params={"_limit": 5})
response.raise_for_status()
posts = response.json()

print("=== First 5 Posts ===")
for post in posts:
    # Truncate long titles for readable output
    title_preview = post['title'][:40] + "..." if len(post['title']) > 40 else post['title']
    print(f"{post['id']}. \"{title_preview}\" (user: {post['userId']})")

# Step 3 & 4: Fetch author of first post
first_post = posts[0]
print(f"\n=== Author of Post {first_post['id']} ===")
author = fetch_user(first_post['userId'])
if author:
    print(f"Name: {author['name']}")
    print(f"Company: {author['company']['name']}")

# Step 5: Test 404 handling
print("\n=== Testing 404 Handling ===")
missing = fetch_user(99999)
if missing is None:
    print("User 99999 not found (404)")
```

**Explanation:**
The `fetch_user` function centralises the 404-handling logic so we don't repeat it.
Using `params={"_limit": 5}` is cleaner than string formatting the URL because `requests`
handles URL encoding automatically. The `response.raise_for_status()` call handles any
unexpected error codes (5xx, 429) as Python exceptions.

**Common wrong answers and why they fail:**
- Calling `response.raise_for_status()` before the 404 check — this raises an exception for 404s, preventing graceful handling.
- Using string concatenation to add query params (`URL + "?_limit=5"`) — works but is fragile; `params=` is idiomatic and handles encoding.

</details>

---

## Exercise 4: Compare REST and GraphQL Data Fetching [🟡 Medium] [2 pts]

### Context
The theory section explained over-fetching and under-fetching conceptually. This exercise makes
the comparison concrete by asking you to design both the REST and GraphQL approaches for a
given view.

### Task
You're building a "team dashboard" that shows each team member's name, their current project name,
and how many tasks are assigned to them.

The REST API has three endpoints:
- `GET /team-members` → list of `{ id, name, project_id }`
- `GET /projects/{id}` → `{ id, name, description, deadline }`
- `GET /team-members/{id}/tasks/count` → `{ count: N }`

**Part A:** Write pseudocode (or actual code) showing the REST calls needed to build the dashboard
for 5 team members. Count the total number of HTTP requests.

**Part B:** Write the equivalent GraphQL query that fetches all needed data in one request.
(Assume the GraphQL API has the types and fields you need.)

**Part C:** Write 2–3 sentences explaining the trade-off between the two approaches for this use case.

### Requirements
- [ ] Part A identifies the correct number of REST requests
- [ ] Part B is valid GraphQL query syntax
- [ ] Part C identifies at least one advantage and one disadvantage of each approach

### Hints
<details>
<summary>Hint 1</summary>

For Part A: you need one request to list all 5 members, then for each member you need their
project (1 request each) and their task count (1 request each). That's 1 + 5 + 5 = ?

</details>

<details>
<summary>Hint 2</summary>

For Part B: the GraphQL query should use nested fields — `teamMembers { name project { name } taskCount }`.
You don't need to make three separate queries — the schema defines the relationships.

</details>

### Expected Output / Acceptance Criteria
- Part A: 11 total REST requests (1 + 5 projects + 5 task counts)
- Part B: A valid GraphQL query fetching name, project.name, and taskCount in one request
- Part C: Honest assessment of the tradeoffs

### Solution
<details>
<summary>Show Solution</summary>

**Part A — REST approach:**

```python
# Request 1: get all team members
members = GET /team-members
# → [{ id: 1, name: "Alice", project_id: 10 }, { id: 2, ... }, ...]

for member in members:
    # Request N: get each member's project (5 requests for 5 members)
    project = GET /projects/{member['project_id']}

    # Request N: get each member's task count (5 more requests)
    tasks = GET /team-members/{member['id']}/tasks/count

# Total: 1 + 5 + 5 = 11 HTTP requests to render the dashboard
```

**Part B — GraphQL approach:**

```graphql
query TeamDashboard {
  teamMembers {
    name
    project {
      name
    }
    taskCount
  }
}
# Total: 1 HTTP request, 1 GraphQL query
```

**Part C — Trade-off analysis:**

REST requires 11 requests because it models each resource independently and doesn't support
relationship traversal in a single call. GraphQL collapses this to 1 request because clients
can declare the entire data graph they need. The REST approach, however, allows individual
resources to be cached (e.g., project details can be cached by ID), while the GraphQL POST
request typically cannot be cached at the HTTP layer. For a low-traffic dashboard with stable
data, REST might be equally fine; for high-volume mobile clients on variable connections,
GraphQL's single-roundtrip approach is significantly better.

</details>

---

## Exercise 5: Debug a Broken API Client [🔴 Hard] [3 pts]

### Context
This multi-step exercise requires you to identify multiple problems in a real-ish API client
and fix them. The bugs are representative of common beginner mistakes.

### Task
The following Python script is supposed to fetch the top 3 posts and create a new comment on
the first one, but it has multiple bugs. Find and fix all of them.

```python
import requests
import json

# Bug-hunting exercise: this code has multiple problems
# Find all of them, explain why each is a bug, and provide the fix

BASE = "https://jsonplaceholder.typicode.com"

# Fetch posts
posts_response = requests.get(BASE + "/posts?limit=3")
posts = posts_response.text()           # BUG 1

# Get first post
first_post = posts[0]
post_id = first_post.id                 # BUG 2

# Create a comment on the post
comment_data = json.dumps({
    "postId": post_id,
    "name": "Great post!",
    "email": "reader@example.com",
    "body": "Really enjoyed reading this."
})

comment_response = requests.post(
    BASE + f"/posts/{post_id}/comments",
    data=comment_data                   # BUG 3 (partial — works but is wrong idiomatically)
)

if comment_response == 201:             # BUG 4
    print("Comment created!")
    print(comment_response.json['id'])  # BUG 5
else:
    print(f"Failed: {comment_response.status_code}")
```

### Requirements
- [ ] Identifies all 5 bugs
- [ ] Explains why each is a bug (not just what the fix is)
- [ ] Provides correct fixed code that runs without errors
- [ ] Fixed code prints "Comment created!" and the comment's assigned ID

### Hints
<details>
<summary>Hint 1 (structural hint — try reading the code carefully first)</summary>

Bug 1 is in how the response body is being parsed.
Bug 2 is about Python dict access syntax.
Bug 3 is about how `requests` sets the `Content-Type` header.
Bug 4 is about comparing Python objects.
Bug 5 is about calling vs. accessing a method.

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

For Bug 3: when you pass `data=` with a string, `requests` sends `Content-Type: text/plain`
by default. The JSONPlaceholder API expects `Content-Type: application/json`. You can either
pass `data=comment_data` with an explicit header, or better, pass `json=original_dict` and
let requests handle serialisation and the header.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

The five fixes:
1. `.text()` → `.json()` (text is a property, but more importantly you want parsed JSON not a string)
2. `first_post.id` → `first_post['id']` (Python dicts use bracket notation, not attribute access)
3. `data=comment_data` (a pre-serialised string) → `json={"postId": ..., ...}` (let requests handle it)
4. `comment_response == 201` → `comment_response.status_code == 201`
5. `comment_response.json['id']` → `comment_response.json()['id']` (json is a method, not a property)

</details>

### Expected Output / Acceptance Criteria
Fixed code should output:
```
Comment created!
Comment ID: 501
```
(or similar — JSONPlaceholder simulates the response)

### Solution
<details>
<summary>Show Solution</summary>

```python
import requests

BASE = "https://jsonplaceholder.typicode.com"

# --- FIX 1: Use .json() method (not .text()) to parse the JSON response ---
# .text is a property that returns the raw string
# .json() is a method that parses the string to a Python dict/list
posts_response = requests.get(BASE + "/posts", params={"_limit": 3})
posts = posts_response.json()           # ← was: posts_response.text()

# --- FIX 2: Use dict bracket syntax, not attribute access ---
# Python dicts are accessed with [] not .property
first_post = posts[0]
post_id = first_post['id']              # ← was: first_post.id

# --- FIX 3: Pass the raw dict to json= and let requests serialise it ---
# Using data= with a pre-serialised string doesn't set Content-Type: application/json
# Using json= with a dict: requests serialises it AND sets the correct Content-Type header
comment_response = requests.post(
    BASE + f"/posts/{post_id}/comments",
    json={                              # ← was: data=json.dumps({...})
        "postId": post_id,
        "name": "Great post!",
        "email": "reader@example.com",
        "body": "Really enjoyed reading this."
    }
)

# --- FIX 4: Compare status_code (int), not the Response object itself ---
# comment_response is a requests.Response object, not an integer
# Comparing a Response to 201 is always False
if comment_response.status_code == 201:    # ← was: comment_response == 201
    print("Comment created!")

    # --- FIX 5: json() is a method, not a property — call it with () ---
    comment = comment_response.json()       # ← was: comment_response.json['id']
    print(f"Comment ID: {comment['id']}")
else:
    print(f"Failed: {comment_response.status_code}")
```

**Step-by-step explanation:**

1. **`.text()` vs `.json()`**: `response.text` is a *property* that returns the raw response body as a string. `response.json()` is a *method* that parses that string as JSON and returns a Python dict or list. Calling `.text()` raises `TypeError: 'str' object is not callable` because you're trying to call a string.

2. **Dict bracket notation**: Python dicts (which is what `response.json()` returns) require `d['key']` syntax for attribute access. Unlike JavaScript objects, you cannot use `d.key` for dict access. Python classes and objects use `.attr` syntax; dicts use `['key']`.

3. **`json=` vs `data=` with serialised string**: When you pass a dict to `json=`, requests serialises it to JSON and sets `Content-Type: application/json` automatically. When you pass a pre-serialised string to `data=`, requests doesn't know it's JSON and sets `Content-Type: application/x-www-form-urlencoded` by default. APIs expecting JSON may reject or misparse the request.

4. **Comparing the Response object**: `requests.get(...)` returns a `Response` object, not an integer. Comparing a `Response` to `201` always evaluates to `False` in Python (different types are never equal). You must access the `status_code` attribute: `response.status_code`.

5. **`json` is a method**: `response.json` is the method object itself; `response.json()` calls it and returns the parsed data. `response.json['id']` tries to subscript the method object, which raises `TypeError`.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1: Annotate HTTP | — | —/1 | — | — |
| Exercise 2: REST Violations | — | —/1 | — | — |
| Exercise 3: Python API calls | — | —/2 | — | — |
| Exercise 4: REST vs GraphQL | — | —/2 | — | — |
| Exercise 5: Debug the client | — | —/3 | — | — |
| **Total** | | **—/9** | | |

**Passing threshold:** 6/9 (67%). Aim for 8/9 (89%) before taking the test.
