# Exercises — Module 0: Introduction

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

## Exercise 1: Install Go and Verify [🟢 Easy] [1 pt]

### Context
Before you can write any Go code, you need a working Go installation. This exercise confirms that your environment is ready and that you know how to check it. It's a warm-up to confirm you have the most basic prerequisite: a working toolchain.

### Task
Install Go on your system (or confirm it's already installed) and verify the installation by running three commands.

### Requirements
- [ ] Running `go version` prints a Go 1.18 or later version string
- [ ] Running `go env GOPATH` prints a directory path (not an error)
- [ ] Running `go env GOROOT` prints the Go installation directory

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

Go's official installation guide is at `go.dev/doc/install`. Follow the instructions for your operating system. After installation, you may need to open a new terminal window for the PATH changes to take effect.

</details>

<details>
<summary>Hint 2 (only if Hint 1 wasn't enough)</summary>

If `go version` says "command not found", Go is installed but not on your PATH. On Linux/macOS, check if `/usr/local/go/bin` needs to be added to your PATH in `~/.bashrc` or `~/.zshrc`. On Windows, the installer usually handles this automatically.

</details>

### Expected Output / Acceptance Criteria
```
$ go version
go version go1.21.5 linux/amd64   (version and OS/arch will differ)

$ go env GOPATH
/home/yourname/go                   (a real directory path)

$ go env GOROOT
/usr/local/go                       (your Go installation path)
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

This exercise has no code solution — it is a setup verification. The steps are:

1. Visit `go.dev/dl/` and download the installer for your OS
2. Follow the installation instructions for your platform
3. Open a new terminal and run the three verification commands

**Common wrong answers and why they fail:**
- Running `go version` and getting `go version go1.14` — this is too old; generics (1.18) and recent standard library improvements (1.21) require a newer version. Update Go.
- Getting `go version go1.21.5 linux/arm64` on an M1/M2 Mac — this is actually correct for Apple Silicon. The architecture being `arm64` rather than `amd64` is expected.

</details>

---

## Exercise 2: Write and Run Hello World [🟢 Easy] [1 pt]

### Context
The canonical first program in any language. Writing it yourself (not copying) builds the muscle memory of the required structure: package declaration, import, and main function.

### Task
Create a new directory, create a file named `main.go` inside it, and write a Go program that prints `Hello, World!`. Run it with `go run`.

### Requirements
- [ ] File is named `main.go` and begins with `package main`
- [ ] The `fmt` package is imported
- [ ] `func main()` is present and is the entry point
- [ ] Running `go run main.go` prints exactly `Hello, World!`
- [ ] You wrote this by hand — no copy-paste

### Hints
<details>
<summary>Hint 1</summary>

The program needs exactly three things: `package main`, `import "fmt"`, and `func main()` containing a call to `fmt.Println`. All three are required — remove any one and it either won't compile or won't run.

</details>

### Expected Output / Acceptance Criteria
```
Hello, World!
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, World!")
}
```

**Explanation:**
`package main` declares this as an executable program. `import "fmt"` brings in the formatting package. `func main()` is the entry point — execution starts here. `fmt.Println` writes its argument to stdout followed by a newline.

</details>

---

## Exercise 3: Run with go run [🟢 Easy] [1 pt]

### Context
`go run` is the fastest way to test a Go program during development. This exercise ensures you understand the difference between `go run` (run without leaving a binary) and `go build` (compile to a binary). Both are essential daily tools.

### Task
Take your `hello.go` from Exercise 2 and run it two ways: with `go run` and with `go build`. Confirm both produce `Hello, World!` and observe the difference.

### Requirements
- [ ] `go run main.go` runs the program and prints the output
- [ ] `go build -o hello .` creates a binary file named `hello` in the current directory
- [ ] Running `./hello` (Linux/macOS) or `hello.exe` (Windows) produces the same output
- [ ] You can explain the difference between the two commands

### Hints
<details>
<summary>Hint 1</summary>

After `go build -o hello .`, list the files in the directory with `ls -la`. You should see a binary named `hello`. On Linux/macOS you run it with `./hello`; on Windows it may be `hello.exe`.

</details>

### Expected Output / Acceptance Criteria
```
$ go run main.go
Hello, World!

$ go build -o hello .
$ ./hello
Hello, World!
```

### Solution
<details>
<summary>Show Solution</summary>

```bash
# Run without compiling to disk
go run main.go

# Compile to a binary
go build -o hello .

# Run the binary
./hello      # Linux/macOS
# hello.exe  # Windows
```

**Explanation:**
`go run` compiles the program to a temporary location and runs it — no binary is left behind in your working directory. `go build` compiles and writes the binary to disk. For development, `go run` is faster. For deployment or distribution, `go build` is what you use.

</details>

---

## Exercise 4: Print Go Version with runtime Package [🟡 Medium] [2 pts]

### Context
The `runtime` package provides information about the running Go environment. Using it demonstrates that you can import and call a package beyond `fmt`, and it's a practical introduction to reading Go package documentation.

### Task
Write a Go program that prints the current Go version, the operating system, the CPU architecture, and the number of available CPUs. Use only the `runtime` package (and `fmt` for printing).

### Requirements
- [ ] Program uses `runtime.Version()` to get the Go version string
- [ ] Program uses `runtime.GOOS` to get the operating system name
- [ ] Program uses `runtime.GOARCH` to get the CPU architecture
- [ ] Program uses `runtime.NumCPU()` to get the CPU count
- [ ] Output is formatted clearly (one piece of information per line)

### Hints
<details>
<summary>Hint 1</summary>

`runtime.Version()` is a function call — it returns a `string`. `runtime.GOOS` and `runtime.GOARCH` are variables (string constants), not function calls — no parentheses needed. `runtime.NumCPU()` is a function that returns an `int`.

</details>

### Expected Output / Acceptance Criteria
```
Go version:   go1.21.5
OS:           linux
Architecture: amd64
CPUs:         8
```
(Exact values will match your system.)

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Println("Go version:  ", runtime.Version())
	fmt.Println("OS:          ", runtime.GOOS)
	fmt.Println("Architecture:", runtime.GOARCH)
	fmt.Println("CPUs:        ", runtime.NumCPU())
}
```

**Explanation:**
`runtime` is a standard library package — no installation needed. The multiple-import form uses a parenthesized block. `fmt.Println` accepts multiple arguments separated by commas and inserts a space between them automatically.

**Alternative approaches:**
`fmt.Printf("Go version: %s\n", runtime.Version())` is equally valid if you prefer `Printf`'s format string style.

</details>

---

## Exercise 5: Greeting Program with a Function [🟡 Medium] [2 pts]

### Context
Functions are the primary unit of code organization in Go. This exercise introduces defining your own function with a parameter, calling it multiple times, and using `fmt.Sprintf` to build strings. It's the first step beyond a single-line `main` function.

### Task
Write a Go program that defines a `greet` function accepting a name as a string parameter. The function should return a greeting string (not print it directly). Call `greet` from `main` for at least three different names and print the results.

### Requirements
- [ ] A function `greet(name string) string` is defined outside of `main`
- [ ] The function returns a formatted string like `"Hello, Alice! Welcome to Go."`
- [ ] `main` calls `greet` at least three times with different names
- [ ] `main` prints the returned strings using `fmt.Println`
- [ ] The function does not call `fmt.Println` itself — it only returns a string

### Hints
<details>
<summary>Hint 1</summary>

To return a value from a function, declare a return type after the parameter list: `func greet(name string) string { ... }`. Use `fmt.Sprintf` inside the function to build the greeting string and return it.

</details>

<details>
<summary>Hint 2</summary>

`fmt.Sprintf` works like `fmt.Printf` but returns a string instead of printing it:
```go
s := fmt.Sprintf("Hello, %s!", name)
return s
```

</details>

### Expected Output / Acceptance Criteria

```
Hello, Alice! Welcome to Go.
Hello, Bob! Welcome to Go.
Hello, Charlie! Welcome to Go.
```

### Solution
<details>
<summary>Show Solution</summary>

```go
package main

import "fmt"

// greet returns a personalized greeting string.
func greet(name string) string {
	return fmt.Sprintf("Hello, %s! Welcome to Go.", name)
}

func main() {
	fmt.Println(greet("Alice"))
	fmt.Println(greet("Bob"))
	fmt.Println(greet("Charlie"))
}
```

**Explanation:**
The function signature `func greet(name string) string` says: "greet takes a string called name and returns a string." `fmt.Sprintf` formats and returns a string without printing it. In `main`, we call `greet` and pass the result directly to `fmt.Println`. This separation — build the string in one function, print in another — is a good habit that makes testing easier.

**Alternative approaches:**
Using string concatenation (`"Hello, " + name + "! Welcome to Go."`) also works but is less idiomatic than `fmt.Sprintf` for formatted strings.

</details>

---

## Exercise 6: Use go fmt on Intentionally Bad Formatting [🟡 Medium] [2 pts]

### Context
`go fmt` is not optional in Go — it enforces a single canonical formatting style. This exercise builds the habit of running `go fmt` and shows you exactly what it fixes. Understanding what the formatter does (and trusting it) is part of working as a Go developer.

### Task
Take the following poorly formatted Go program, save it to a file, run `go fmt` on it, and observe what changes. Then describe at least three formatting issues that `go fmt` fixed.

```go
package main
import   "fmt"
func main(){
fmt.Println( "Hello" )
x:=42
fmt.Println(x)  }
```

### Requirements
- [ ] You saved the badly formatted code to a real file
- [ ] You ran `go fmt` (or `go fmt ./...`) on it
- [ ] The file is now correctly formatted
- [ ] You can name at least three specific things `go fmt` changed

### Hints
<details>
<summary>Hint 1</summary>

Save the code to `bad.go` (make sure it still says `package main`). Then run `go fmt bad.go` and open the file again to see the changes. Compare the before and after.

</details>

<details>
<summary>Hint 2</summary>

Look specifically at: spacing around `:=`, the placement of `{`, indentation inside `main`, and spacing inside `fmt.Println( ... )`.

</details>

### Expected Output / Acceptance Criteria

After `go fmt`, the file should look like:

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello")
	x := 42
	fmt.Println(x)
}
```

Three things `go fmt` fixed:
1. Added a blank line between `import` and `func main()`
2. Added proper tab indentation inside the function body
3. Removed the extra space inside `fmt.Println( "Hello" )` → `fmt.Println("Hello")`
4. Fixed the spacing around `:=` (`x:=42` → `x := 42`)
5. Moved the closing `}` to its own line

### Solution
<details>
<summary>Show Solution</summary>

```bash
# Save the bad code to bad.go, then:
go fmt bad.go
# or for all files in the module:
go fmt ./...
```

**Explanation:**
`go fmt` (which internally calls `gofmt`) reformats Go source code according to a single standard. It is not configurable — there are no style options. This is intentional: the goal is that all Go code, everywhere, looks the same, so you can read any Go codebase without adjusting to its style. The formatter handles tabs vs spaces, blank lines, spacing around operators, import grouping, and more.

</details>

---

## Exercise 7: Multi-File Program [🔴 Hard] [3 pts]

### Context
Real Go programs are not single files. This exercise introduces the concept of multiple `.go` files in the same package — they share the same namespace, so functions defined in one file are visible in another without any import. This is how Go programs are actually organized.

### Task
Create a directory with two files: `main.go` and `math.go`. In `math.go`, define two functions: `add(a, b int) int` and `multiply(a, b int) int`. In `main.go`, call both functions and print the results. Both files must be in `package main`.

### Requirements
- [ ] `math.go` contains `add` and `multiply` functions in `package main`
- [ ] `main.go` calls both functions from `main()` without any import of `math.go`
- [ ] Running `go run .` (note the `.`, not a filename) runs both files together
- [ ] Running `go build .` compiles both files into a single binary
- [ ] The program prints correct results for addition and multiplication

### Hints
<details>
<summary>Hint 1 (structural hint — try designing without this first)</summary>

When you have multiple files in a package, you run them with `go run .` (the dot means "all .go files in this directory"), not `go run main.go`. Using `go run main.go` alone will fail because `add` and `multiply` are defined in a different file.

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

Both files must declare `package main` at the top. They don't need to import each other — they're already in the same package. Functions defined in `math.go` are automatically available in `main.go` (and vice versa) because they share a package namespace.

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

```
myprogram/
  main.go    — has package main, import "fmt", func main() calling add() and multiply()
  math.go    — has package main, func add(a, b int) int, func multiply(a, b int) int
```
No imports between the files are needed.

</details>

### Expected Output / Acceptance Criteria

```
add(3, 4) = 7
multiply(3, 4) = 12
```

### Solution
<details>
<summary>Show Solution</summary>

**math.go:**
```go
package main

// add returns the sum of a and b.
func add(a, b int) int {
	return a + b
}

// multiply returns the product of a and b.
func multiply(a, b int) int {
	return a * b
}
```

**main.go:**
```go
package main

import "fmt"

func main() {
	fmt.Printf("add(3, 4) = %d\n", add(3, 4))
	fmt.Printf("multiply(3, 4) = %d\n", multiply(3, 4))
}
```

**Step-by-step explanation:**

1. Both files declare `package main` — they belong to the same package.
2. `math.go` defines helper functions. No `import` needed since it doesn't use any packages.
3. `main.go` imports `fmt` for printing and calls `add` and `multiply` directly — no import of `math.go` needed because they share a package namespace.
4. `go run .` tells Go to compile all `.go` files in the current directory as one unit.

**Why this approach:**
Go's package system means all files sharing a package name are compiled together. This lets you organize code across files without a Java-style import-per-class system. In real codebases, a package might have dozens of `.go` files, each grouping related functionality, all sharing the same package namespace.

**What a weaker solution looks like and why it fails:**
Using `go run main.go` gives `undefined: add` because Go only compiles the files you name explicitly (unless you use `.` to mean "all files here").

</details>

---

## Exercise 8: Use go vet to Find a Bug [🔴 Hard] [3 pts]

### Context
`go vet` finds likely mistakes that compile but are almost certainly wrong. This exercise trains the habit of running `go vet` as part of development — and shows you what kind of bugs it catches that the compiler misses.

### Task
Save the following buggy program to a file and run `go vet` on it. Identify the bug, explain why it's a problem, and fix it.

```go
package main

import "fmt"

func main() {
	name := "Alice"
	age := 30
	fmt.Printf("Name: %s, Age: %s\n", name, age)
}
```

### Requirements
- [ ] You ran `go vet ./...` or `go vet main.go` and captured its output
- [ ] You can explain what the bug is in plain English
- [ ] You can explain why this compiles successfully despite being wrong
- [ ] You fixed the bug so `go vet` reports no issues and the output is correct

### Hints
<details>
<summary>Hint 1</summary>

Look at the `fmt.Printf` call carefully. Count the number of format verbs (`%s`, `%d`, etc.) and compare them to the number and types of arguments passed.

</details>

<details>
<summary>Hint 2</summary>

`%s` is the verb for strings. `%d` is the verb for integers. `age` is an `int`, not a `string`. Using `%s` with an integer doesn't print the number — it prints something unexpected.

</details>

### Expected Output / Acceptance Criteria

`go vet` output before fix:
```
./main.go:8:2: fmt.Printf format %s has arg age of wrong type int
```

Program output before fix (what `go run` actually prints):
```
Name: Alice, Age: %!s(int=30)
```

After fix, program output:
```
Name: Alice, Age: 30
```

### Solution
<details>
<summary>Show Solution</summary>

**The bug:** `%s` is used to format `age`, which is an `int`. `%s` means "format this as a string." When `fmt.Printf` gets an `int` where it expects a string, it prints the error notation `%!s(int=30)`.

**Why it compiles:** Go's type system doesn't check `fmt.Printf` format strings at compile time — they're just strings at the language level. The `go vet` tool performs the additional analysis that the compiler doesn't.

**Fixed code:**
```go
package main

import "fmt"

func main() {
	name := "Alice"
	age := 30
	fmt.Printf("Name: %s, Age: %d\n", name, age)
}
```

Change `%s` to `%d` (decimal integer) for `age`.

**Step-by-step explanation:**
1. `%s` → string, `%d` → decimal integer, `%f` → float, `%v` → any (default format), `%T` → type
2. `go vet` checks that format verbs match argument types — this is one of its most useful checks
3. Run `go vet ./...` as part of your standard workflow before committing code

</details>

---

## Exercise 9: Set Up a Go Module and Add a Dependency [⭐ Challenge] [5 pts]

### Context
Real Go programs use external packages. This exercise walks through the full modern Go module workflow: initializing a module, adding an external dependency, importing it, and understanding what the resulting `go.mod` and `go.sum` files contain. This is how every non-trivial Go project starts.

### Task
Create a new directory, initialize a Go module, write a program that uses the `golang.org/x/text/cases` package to convert a string to title case, and run it successfully. Then examine `go.mod` and `go.sum` to understand what was recorded.

### Requirements
- [ ] A new directory is created and `go mod init` is run inside it
- [ ] `go get golang.org/x/text` is run to add the dependency
- [ ] `go.mod` contains a `require` directive for `golang.org/x/text`
- [ ] `go.sum` exists and contains cryptographic hashes
- [ ] The program uses `cases.Title` from `golang.org/x/text/cases` and `language.English` from `golang.org/x/text/language`
- [ ] The program converts `"hello, world"` to `"Hello, World"` and prints it
- [ ] `go mod tidy` runs without errors after the program is complete

### Hints
<details>
<summary>Hint 1 (structural hint)</summary>

The steps in order:
1. `mkdir mymodule && cd mymodule`
2. `go mod init example.com/mymodule`
3. Write `main.go` with the import paths (see below)
4. `go get golang.org/x/text`
5. `go run .`
6. `go mod tidy`

</details>

<details>
<summary>Hint 2 (import paths)</summary>

You need two imports:
- `"golang.org/x/text/cases"` — provides `cases.Title`
- `"golang.org/x/text/language"` — provides `language.English`

The `cases.Title` function returns a `cases.Caser` which has a `String` method.

</details>

<details>
<summary>Hint 3 (usage pattern)</summary>

```go
caser := cases.Title(language.English)
result := caser.String("hello, world")
```

</details>

### Expected Output / Acceptance Criteria

```
Hello, World
```

And `go.mod` should look something like:
```
module example.com/mymodule

go 1.21

require golang.org/x/text v0.14.0
```

### Solution
<details>
<summary>Show Solution</summary>

```bash
mkdir mymodule
cd mymodule
go mod init example.com/mymodule
go get golang.org/x/text
```

**main.go:**
```go
package main

import (
	"fmt"

	"golang.org/x/text/cases"
	"golang.org/x/text/language"
)

func main() {
	caser := cases.Title(language.English)
	result := caser.String("hello, world")
	fmt.Println(result)
}
```

```bash
go run .
go mod tidy
```

**Step-by-step explanation:**

1. `go mod init example.com/mymodule` creates `go.mod` with the module path and current Go version.
2. `go get golang.org/x/text` downloads the package, adds it to `go.mod`, and records hashes in `go.sum`.
3. The program imports two sub-packages from the `golang.org/x/text` module — each sub-package is a separate import path.
4. `go run .` compiles all `.go` files in the current directory with the downloaded dependencies.
5. `go mod tidy` removes any unused dependencies and adds any missing ones.

**Why this approach:**
`golang.org/x/text` is a well-maintained package from the Go team's "extended standard library." Using it here demonstrates the real module workflow with a trustworthy, well-known package.

**What a weaker solution looks like and why it fails:**
Simply calling `strings.ToUpper` or `strings.Title` misses the point — the exercise is about the module workflow, not string manipulation. `strings.Title` is also deprecated because it doesn't handle Unicode correctly.

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 — Install and Verify | — | —/1 | — | — |
| Exercise 2 — Hello World | — | —/1 | — | — |
| Exercise 3 — go run vs go build | — | —/1 | — | — |
| Exercise 4 — runtime Package | — | —/2 | — | — |
| Exercise 5 — Greeting Function | — | —/2 | — | — |
| Exercise 6 — go fmt | — | —/2 | — | — |
| Exercise 7 — Multi-File Program | — | —/3 | — | — |
| Exercise 8 — go vet Bug | — | —/3 | — | — |
| Exercise 9 — Module + Dependency | — | —/5 | — | — |
| **Total** | | **—/20** | | |

**Passing threshold:** 13/20 (65%). Aim for 17/20 (85%) before taking the test.
