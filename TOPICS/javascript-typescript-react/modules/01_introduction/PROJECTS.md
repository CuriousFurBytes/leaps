# Projects: Module 01 — Introduction to JavaScript

> Project ideas appropriate for a JavaScript beginner who has completed Module 01.
> These projects use only the concepts from this module: variables, types, functions,
> control flow, and basic string/array operations.
> For more ambitious projects (React, TypeScript, APIs), see the topic-level [PROJECTS.md](../../PROJECTS.md).

---

## Project 1: Number Guessing Game

**Difficulty:** Beginner
**Estimated Time:** 2–3 hours
**Concepts Practiced:** Variables, functions, loops, conditionals, user input (Node.js `readline`)

**Description:**
Build a command-line number guessing game. The program picks a random integer between 1 and 100. The user guesses, and the program tells them "too high", "too low", or "correct!" and counts how many guesses it took.

**Requirements:**
- Use `Math.random()` and `Math.floor()` to pick a random number
- Accept user input from the command line using Node.js `readline` module
- Give appropriate hints after each guess
- Track and display the number of guesses on success
- Ask if the player wants to play again

**Stretch goals:**
- Add difficulty levels: Easy (1–50, 10 guesses), Medium (1–100, 7 guesses), Hard (1–200, 7 guesses)
- Maintain a high score (fewest guesses) across multiple rounds using a variable

---

## Project 2: FizzBuzz Variations

**Difficulty:** Beginner
**Estimated Time:** 1–2 hours
**Concepts Practiced:** Loops, conditionals, modulo operator, arrays, functions

**Description:**
The classic FizzBuzz problem, extended with variations to build your loop and conditional skills.

**Requirements:**
1. Write the classic FizzBuzz: print numbers 1–100, replacing multiples of 3 with "Fizz", multiples of 5 with "Buzz", and multiples of both with "FizzBuzz".
2. Generalize it: write a `fizzBuzz(n, rules)` function where `rules` is an array like `[{divisor: 3, word: "Fizz"}, {divisor: 5, word: "Buzz"}]`. It should work for any combination of divisors and words.
3. Write a `fizzBuzzCount(n)` function that returns an object with the count of each category: `{ fizz: X, buzz: X, fizzbuzz: X, other: X }`.

---

## Project 3: Text Analyzer

**Difficulty:** Beginner
**Estimated Time:** 3–4 hours
**Concepts Practiced:** Strings, arrays, loops, functions, objects as dictionaries

**Description:**
Build a text analysis utility that processes a string of text and produces statistics.

**Requirements:**
- Word count (split by whitespace)
- Character count (with and without spaces)
- Sentence count (split by `.`, `!`, `?`)
- Most frequent word(s) — build a frequency map using an object
- Average word length
- Longest word

**Example usage:**
```javascript
const text = "JavaScript is great. JavaScript is fun. I love JavaScript.";
const stats = analyze(text);
console.log(stats);
// {
//   wordCount: 11,
//   charCount: 58,
//   charCountNoSpaces: 48,
//   sentenceCount: 3,
//   mostFrequentWord: 'javascript',
//   topWordCount: 3,
//   averageWordLength: 4.4,
//   longestWord: 'javascript'
// }
```

**Stretch goal:** Accept the text as a command-line argument (`process.argv[2]`) so you can analyze any string without editing the code.

---

## Project 4: Mini Calculator REPL

**Difficulty:** Beginner–Intermediate
**Estimated Time:** 4–6 hours
**Concepts Practiced:** Functions, strings, parsing, loops, switch/conditionals, Node.js readline

**Description:**
Build an interactive calculator that runs in the terminal. Users type expressions like `5 + 3` and see the result immediately. The calculator keeps running until the user types `exit`.

**Requirements:**
- Accept input in the format `<number> <operator> <number>` (e.g., `10 * 4`)
- Support at least `+`, `-`, `*`, `/`, and `%` (modulo)
- Handle division by zero with a friendly error message
- Keep a history of all calculations in the current session
- Support a `history` command to show all previous calculations
- Support `clear` to reset history
- Support `exit` to quit

**Stretch goals:**
- Add memory: `memory set` saves the last result, `memory get` retrieves it
- Support chaining: `5 + 3 * 2` (with correct operator precedence)
