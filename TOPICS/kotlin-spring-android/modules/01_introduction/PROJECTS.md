# Projects: Module 01 — Introduction to Kotlin

> Project ideas that apply the concepts from this module. Build something real.

---

## Beginner Projects

### Project 1: Personal Finance Tracker CLI

Build a command-line tool that tracks income and expense entries.

**What you'll build:**
- A `data class Transaction(val id: Int, val amount: Double, val description: String, val type: TransactionType)`
- A `sealed class TransactionType` with `Income` and `Expense` subclasses
- Functions to add transactions, list them, and print a summary (total income, total expenses, balance)
- Persistence to a simple text file (one transaction per line, CSV format)

**Acceptance criteria:**
- `add income 500.00 "Freelance payment"` stores an income transaction
- `add expense 45.50 "Groceries"` stores an expense
- `summary` prints total income, total expenses, and current balance
- All data persists to disk and loads on next run

**This project tests:** `data class`, sealed classes, file I/O, null safety, string templates, `when`.

---

### Project 2: Wordle Clone (Console)

Implement the popular Wordle word game in the terminal.

**What you'll build:**
- A list of 5-letter target words
- Turn-based input loop (6 guesses maximum)
- Feedback: `[G]` for correct position, `[Y]` for wrong position, `[-]` for not present
- Track the game state with a sealed class: `Playing(guessesLeft: Int)`, `Won(attempts: Int)`, `Lost(target: String)`

**Acceptance criteria:**
- Clear per-turn feedback display
- Case-insensitive input handling
- Proper handling of repeated letters
- Game summary on win or loss

**This project tests:** Sealed classes, `when`, `val`/`var`, list operations, loops, input reading.

---

## My Projects

_Track your module 01 projects here._

| Project | Started | Completed | Notes |
|---------|---------|-----------|-------|
| — | — | — | — |
