# Go — Projects

> Project-based learning cements knowledge in a way that reading and exercises alone cannot.
> Building something real forces you to confront gaps in your understanding and make decisions
> that tutorials never put in front of you.

---

## How to Use This File

1. Choose a project at or slightly above your current level.
2. **Don't use tutorials for your chosen project.** Tutorials are for learning, projects are for applying.
3. Document your attempt using the [Project Attempt Template](#project-attempt-template) at the bottom.
4. When you finish, link the result (repo, binary) in the table in the topic README.

---

## Beginner Projects

_Focus: get comfortable with the core tools and vocabulary._
_Complete at least one before advancing past Phase 1._

### B1: CLI Calculator

**Description:** A command-line calculator that accepts two numbers and an operator as arguments and prints the result. Handles addition, subtraction, multiplication, and division. Prints a clear error message for division by zero or invalid input.

**Concepts Reinforced:**
- `os.Args` for command-line argument parsing
- `strconv.ParseFloat` for type conversion
- `fmt.Fprintf` for formatted output to stderr
- Basic `switch` statement
- Error messages and exit codes

**Estimated Time:** 1–2 hours

**Starting Point:** Blank file — `package main` + `func main()`

**Success Criteria:**
- [ ] `./calc 10 + 5` prints `15`
- [ ] `./calc 10 / 0` prints an error message and exits non-zero
- [ ] `./calc` with wrong number of arguments prints usage and exits non-zero
- [ ] The program runs without errors

---

### B2: Hello World with Flags

**Description:** A program that greets a user by name. The name is provided via a command-line flag (`--name`). If no name is given, it defaults to "World". Add a `--count` flag to print the greeting N times.

**Concepts Reinforced:**
- The `flag` standard library package
- String and integer flags
- Default values
- `for` loop

**Estimated Time:** 1 hour

**Starting Point:** Blank file

**Success Criteria:**
- [ ] `./greet` prints `Hello, World!`
- [ ] `./greet --name Alice` prints `Hello, Alice!`
- [ ] `./greet --name Bob --count 3` prints the greeting 3 times
- [ ] `./greet --help` shows usage automatically (flag package provides this)

---

### B3: File Word Counter

**Description:** A program that reads a text file and prints the count of lines, words, and characters — similar to the Unix `wc` command. Accepts the filename as a command-line argument.

**Concepts Reinforced:**
- `os.Open` / `os.ReadFile` for file I/O
- `bufio.Scanner` for line-by-line reading
- `strings.Fields` for word splitting
- `len()` for character counting
- Error handling for missing/unreadable files

**Estimated Time:** 2–3 hours

**Starting Point:** Blank file

**Success Criteria:**
- [ ] `./wc README.md` prints line count, word count, and byte count
- [ ] Program handles a missing file with a clear error message
- [ ] Output format resembles: `   42  312 2048 README.md`
- [ ] The program runs without errors

---

## Intermediate Projects

_Focus: combine multiple concepts, handle edge cases, write clean code._
_Complete at least one before completing Phase 2._

### I1: HTTP JSON API Server

**Description:** A simple REST API server using only the Go standard library (`net/http`). Implement two endpoints: `GET /users` returns a JSON array of users, `POST /users` accepts a JSON body and adds a new user. Store users in memory (a slice).

**Concepts Reinforced:**
- `net/http` — `http.HandleFunc`, `http.ListenAndServe`
- `encoding/json` — Marshal and Unmarshal
- Structs as JSON data models
- HTTP methods and status codes
- Basic error handling in HTTP handlers

**Estimated Time:** 4–6 hours

**Starting Point:** Blank file

**Success Criteria:**
- [ ] Server starts and listens on a configurable port
- [ ] `GET /users` returns a valid JSON array
- [ ] `POST /users` with a valid JSON body adds a user and returns 201
- [ ] Invalid JSON body returns 400 with an error message
- [ ] Code is clean, readable, and commented
- [ ] No external dependencies — stdlib only

---

### I2: Simple Key-Value Store

**Description:** An in-memory key-value store exposed over HTTP. Supports `GET /key/{name}`, `PUT /key/{name}` (with body as value), and `DELETE /key/{name}`. All values are strings. The store must be safe for concurrent access.

**Concepts Reinforced:**
- `sync.RWMutex` for concurrent map access
- HTTP path parsing (manual or with `http.ServeMux`)
- Method-based routing
- Structs with methods
- Interface design (consider defining a `Store` interface)

**Estimated Time:** 5–8 hours

**Starting Point:** Blank file

**Success Criteria:**
- [ ] `PUT`, `GET`, and `DELETE` all work correctly
- [ ] Concurrent requests don't cause data races (`go test -race`)
- [ ] Missing key returns 404
- [ ] Store logic is separated from HTTP handler logic (clean separation of concerns)

---

### I3: Concurrent Web Scraper

**Description:** A program that takes a list of URLs (from a file or as arguments) and fetches each one concurrently using goroutines. Reports the HTTP status code and response time for each URL. Limits concurrency to N workers (configurable) to avoid overwhelming the network.

**Concepts Reinforced:**
- Goroutines for concurrency
- `sync.WaitGroup` to wait for all goroutines
- Channels for result collection
- Worker pool pattern
- `net/http` for HTTP requests
- `time.Now()` / `time.Since()` for timing

**Estimated Time:** 4–6 hours

**Starting Point:** Blank file

**Success Criteria:**
- [ ] URLs are fetched concurrently
- [ ] Worker count is bounded (no unbounded goroutine spawning)
- [ ] Results are printed in a readable table format
- [ ] Program handles network errors gracefully (no panics on timeout)

---

## Advanced Projects

_Focus: tackle realistic, open-ended problems. No hand-holding._
_Complete at least one to reach Applied Practitioner status._

### A1: REST API with Persistence

**Description:** A full REST API for a simple resource (e.g., tasks, notes, or bookmarks) that persists data to a JSON file on disk. Implement full CRUD: list, create, read by ID, update, delete. Include proper HTTP status codes, error responses, and graceful shutdown.

**Why This Is Hard:**
You must design the data model, the storage layer (with file locking for safety), the HTTP routing, and the request/response serialization — and keep them cleanly separated. There is no framework to lean on.

**Concepts Reinforced:**
- Interface-driven design (define a `Repository` interface; implement it with a JSON file backend)
- `encoding/json` for persistence
- `os.Signal` and `context` for graceful shutdown
- HTTP routing patterns without a framework
- Proper project structure (multiple packages)
- Error handling throughout the entire stack
- Testing with `net/http/httptest`

**Estimated Time:** 15–25 hours

**Starting Point:** Initialize a Go module with `go mod init`

**Success Criteria:**
- [ ] All CRUD endpoints work correctly
- [ ] Data persists across restarts
- [ ] Server shuts down gracefully on SIGINT/SIGTERM
- [ ] At least 70% test coverage on the business logic layer
- [ ] You can explain every design decision you made

---

### A2: Mini Shell Interpreter

**Description:** A minimal interactive shell that reads commands from stdin, forks processes to execute them, and supports pipes (`|`), output redirection (`>`), and environment variable expansion (`$VAR`). Not a complete shell — but a real one in miniature.

**Why This Is Hard:**
Process creation and I/O redirection require `os/exec` and file descriptor manipulation. Parsing the command line correctly — handling quotes, pipes, redirections — is non-trivial. This project surfaces how Unix shells actually work.

**Concepts Reinforced:**
- `os/exec` for process management
- `io.Pipe` and `os.Stdout` / `os.Stdin` redirection
- String parsing and tokenization
- `bufio.Scanner` for interactive input
- Goroutines for pipeline stages
- Environment variables (`os.Getenv`, `os.Environ`)

**Estimated Time:** 20–30 hours

**Success Criteria:**
- [ ] `ls -la` works
- [ ] `ls -la | grep go` works (pipe)
- [ ] `ls > output.txt` works (redirection)
- [ ] `$HOME` expands correctly
- [ ] `exit` exits the shell cleanly

---

## Expert / Capstone Projects

_Focus: synthesize everything. Build something you're proud to show others._
_Complete one to earn Topic Mastery status._

### E1: DevOps CLI Tool

**Description:** A production-quality CLI tool that solves a real DevOps or developer workflow problem. Examples: a tool that watches a directory and runs tests on file changes; a deployment status checker that polls a list of services; a log aggregator that tails multiple files and merges output with color coding.

**Why This Is a Capstone:**
This project requires mastery of all major topic areas. You cannot complete it with gaps — they will surface quickly. Expect to revisit earlier modules during the build.

**Core Requirements:**
- [ ] Uses concepts from at least 6 different modules
- [ ] Is non-trivial in scope (not achievable in a single sitting)
- [ ] Is documented clearly enough that someone else could understand it
- [ ] Includes a README with installation instructions, usage examples, and design notes
- [ ] Ships as a single statically-linked binary with no external runtime dependencies
- [ ] Handles all error cases gracefully — no panics in production code paths
- [ ] Has at least one meaningful test file with table-driven tests

**Estimated Time:** 20–40 hours

**Extension Ideas (if you want more challenge):**
- Publish to GitHub and make it `go install`-able
- Add cross-compilation and release binaries for Linux, macOS, and Windows
- Write a man page or shell completion script

---

## Project Attempt Template

When you attempt a project, create a folder in this topic's directory and copy this template:

```markdown
# Project: {{PROJECT_NAME}}

**Difficulty:** Beginner / Intermediate / Advanced / Expert
**Started:** {{YYYY-MM-DD}}
**Completed:** {{YYYY-MM-DD}} (or "In progress")
**Time Spent:** {{HOURS}} hours

## What I Built

{{DESCRIPTION_OF_WHAT_YOU_ACTUALLY_BUILT}}

## Link / Location

{{LINK_TO_REPO_OR_FILE}}

## What I Learned

- {{LEARNING_1}}
- {{LEARNING_2}}
- {{LEARNING_3}}

## What Was Hard

{{WHAT_WAS_CHALLENGING_AND_HOW_YOU_SOLVED_IT}}

## What I'd Do Differently

{{HONEST_RETROSPECTIVE}}

## Concepts Used

- [[go/0. Introduction]] — how you used it
- [[go/4. Composite Types]] — how you used it

## Score / Self-Assessment

On a scale of 1–5, how well do I think I executed this project? {{SCORE}}/5

Justification: {{JUSTIFICATION}}
```
