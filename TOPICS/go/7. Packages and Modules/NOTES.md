# Notes — Module 7: Packages and Modules

> These are your personal study notes. Write freely and honestly.
> Incomplete notes are fine — they show where your understanding still needs work.
> Return to this file to add insights as they develop over time.

**Module:** [[go/7. Packages and Modules]]
**Topic:** [[go]]
**Date started:** YYYY-MM-DD
**Status:** In progress

---

## Concept Map

_Sketch how the concepts in this module relate to each other. Fill in the Mermaid diagram._

```mermaid
mindmap
  root((Packages & Modules))
    Package
      one directory = one package
      exported vs unexported (capitalization)
      naming conventions (lowercase, no stutter)
      splitting across files
      package-level vars and init()
      blank import side effects
      go doc comments
    Module
      go.mod (module path, go version, require)
      go.sum (integrity hashes)
      module proxy + checksum DB
      semantic versioning
      semantic import versioning v2+ rule
    Dependency Management
      go get / go mod tidy / go mod download
      go list -m all
      Minimal Version Selection (MVS)
      vendoring (go mod vendor)
    Encapsulation
      internal/ packages (toolchain-enforced)
      exported struct fields vs methods
      package design avoiding util
    Multi-Module Dev
      go.work workspaces (Go 1.18+)
      replace directives (legacy)
    Project Layout
      cmd/ for binaries
      internal/ for private packages
      pkg/ for public packages (optional)
```

_Alternative: draw this on paper, photo it, and link the image here._

---

## Key Insights

_The "aha moments" — the things that, once understood, made the rest clear._
_Be specific: "I finally understood X because Y" is more useful than "X makes sense"._

1. **Capitalization is the only access control:** _I finally understood that there is no `public`/`private` in Go because capitalization replaces both. Uppercase = public, lowercase = private. It's not a convention — the compiler enforces it._
2. **MVS means go.mod IS the lock file:** _Go doesn't need a separate lock file because MVS picks exact minimum versions deterministically from the same go.mod on any machine. go.sum handles integrity, not versioning._
3. _Add insights as you discover them_

---

## My Understanding

_Explain the core concepts in your own words, as if teaching them to someone else._
_If you can't explain it simply, you don't understand it well enough yet._

### What a package is

_Your explanation here_

_What I'm still unsure about:_ (e.g., how does the package name in the `package` declaration relate to the import path?)

### Exported vs unexported

_Your explanation here_

_What I'm still unsure about:_ (e.g., can an unexported type be returned by an exported function?)

### The go.mod file

_Your explanation here_

_What I'm still unsure about:_ (e.g., what does `// indirect` mean in a require line?)

### Minimal Version Selection

_Your explanation here_

_What I'm still unsure about:_ (e.g., what happens when two dependencies require incompatible major versions of a third dependency?)

### internal/ packages

_Your explanation here_

_What I'm still unsure about:_ (e.g., if internal/ is at the module root, who exactly can import it?)

---

## Connections to Other Topics

_How does this module connect to things you already know?_

| This module's concept | Connects to | How |
|----------------------|-------------|-----|
| Exported identifiers (capitalization) | [[go/6. Methods and Interfaces]] | Interface methods must be exported for the interface to be useful across packages; unexported methods only satisfy interfaces within the same package |
| Package-level `init()` | [[go/2. Control Flow]] | `init()` uses `defer` semantics — it runs after package-level `var` initialization and cannot be interrupted; understanding function execution order from Module 2 applies here |
| `go.mod` require + MVS | [[go/18. Build, Tooling, and Deployment]] | The module graph and version resolution feed directly into `go build`; cross-compilation, build modes, and release processes all start from a resolved module graph |

---

## Questions That Arose

_Log questions as they appear. Don't stop to answer them now — just capture them._
_Then move the serious ones to [QUESTIONS.md](./QUESTIONS.md)._

- [ ] Can an unexported type be returned from an exported function? → added to QUESTIONS.md as Q001
- [ ] What exactly does `// indirect` mean in a `require` line? → might be answered by `go help mod tidy`
- [ ] Can you have two `go.work` files in the same filesystem hierarchy? → check go.dev/ref/mod

---

## Code Snippets Worth Remembering

_Patterns, idioms, or examples that captured something important._

### The canonical module initialization sequence

```bash
mkdir myproject && cd myproject
go mod init github.com/myorg/myproject
mkdir -p cmd/server internal/config
# write code, then:
go mod tidy
git add go.mod go.sum
```

_Why I'm saving this:_ This is the start of every new Go project. `go mod init` creates go.mod; `go mod tidy` syncs it with actual imports. Both go.mod and go.sum must be committed.

---

### Adding a dependency correctly

```bash
go get github.com/some/package@v1.2.3   # pin to a specific version
go mod tidy                              # remove unused, add missing
git add go.mod go.sum
```

_Why I'm saving this:_ The three-step pattern for dependency changes: get, tidy, commit both files.

---

### go.work for local multi-module development

```bash
# From parent directory containing both modules:
go work init ./myapp ./mylib
echo "go.work" >> .gitignore
```

_Why I'm saving this:_ Use go.work instead of `replace` directives in go.mod. go.work stays local; go.mod stays clean and committable.

---

### blank import for driver registration

```go
import (
    "database/sql"
    _ "github.com/lib/pq"  // registers postgres driver, do not remove
)
```

_Why I'm saving this:_ The blank import is the only legitimate way to trigger init() side effects (driver registration, codec registration) without using the imported package's API directly. The comment explaining why it's there is important — otherwise it looks like dead code.

---

## What Tripped Me Up

_Mistakes I made, misconceptions I had, things that confused me more than they should have._
_Being honest here helps you later._

- **Package name vs import path** — I initially confused the last component of the import path (e.g., `gin` in `github.com/gin-gonic/gin`) with the package name. They usually match, but are technically separate: the directory name determines the import path component, the `package` declaration determines the package name.
- **`go.sum` vs `go.mod`** — I initially thought go.sum was like a lock file I needed to manage. It's actually maintained entirely by the go toolchain; I should never edit it by hand.

---

## Summary in My Own Words

_Write a 3–5 sentence summary of this entire module without looking at any notes._
_If you can't do this, you need more study time._

_Write your summary here after completing the module._

---

_Last updated: YYYY-MM-DD_
