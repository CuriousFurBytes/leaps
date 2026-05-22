---
name: Generate Lab
category: Interactive Content
version: 1.0
parameters:
  - name: TOPIC_NAME
    description: The topic directory name
    example: networking
  - name: MODULE_NUMBER
    description: The zero-padded module number this lab corresponds to
    example: 03
  - name: LAB_TYPE
    description: The type of lab — Setup, Implementation, Debugging, Integration, or Capstone
    example: Implementation
---

# Generate Lab

## Description

Generates a complete, step-by-step interactive lab for a specific module. Unlike exercises (which are short, focused problems) and notebooks (which are exploratory), labs are guided, goal-oriented sessions where the learner builds something real from start to finish. Labs have a concrete artifact as their output — a running program, a configured system, a working algorithm, a filled-in diagram.

Labs are stored in `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/labs/lab-[N]/` and use the template from `TEMPLATES/lab/README.md`.

## Usage

1. Copy the prompt text below
2. Replace `[TOPIC_NAME]`, `[MODULE_NUMBER]`, and `[LAB_TYPE]` with your values
3. Paste into your AI assistant with access to this repository

**LAB_TYPE values:**
- `Setup` — configure an environment, install tools, verify the setup works
- `Implementation` — build a working implementation of the module's core concept
- `Debugging` — diagnose and fix a broken system
- `Integration` — combine the module's concepts with prior modules or external tools
- `Capstone` — open-ended project using all concepts from the module

## Prompt

```
You are a leaps lab generation agent. Your task is to create a complete interactive lab for a learning module.

## Parameters
- TOPIC_NAME: [TOPIC_NAME]
- MODULE_NUMBER: [MODULE_NUMBER]
- LAB_TYPE: [LAB_TYPE]

## Step 1: Read the Module and Templates

Read:
1. `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/README.md` — all module concepts
2. `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/EXERCISES.md` — what practice exists already
3. `TEMPLATES/lab/README.md` — the lab template to follow
4. `environments/[TOPIC_NAME]/` — existing environment files (Dockerfile, requirements, etc.)
5. All previous module README files — understand the full context

Identify:
- What the learner has already built (from exercises and prior labs)
- What tools and environment are available
- What concept in this module is best learned by doing it, not just reading about it

## Step 2: Design the Lab Concept

Choose a lab concept appropriate for LAB_TYPE:

**Setup labs** are appropriate for:
- Module 01 of any topic (setting up the development environment)
- Any module that introduces a new tool, framework, or runtime
- Topics where getting the environment right is itself a learning challenge

**Implementation labs** are appropriate for:
- Modules that introduce a core algorithm, data structure, or language feature
- When building something from scratch reveals the concept better than reading about it
- When the module's concept is most understood through immediate feedback from a running system

**Debugging labs** are appropriate for:
- Modules that cover error handling, ownership rules, type systems, or complex semantics
- When the most common misconception produces a specific bug or error
- After implementation labs — debug the thing you just built

**Integration labs** are appropriate for:
- Modules that combine multiple prior concepts
- When the interesting part is how concepts interact, not how they work in isolation
- When the topic has external systems to interact with (APIs, databases, services)

**Capstone labs** are appropriate for:
- The last 1–3 modules of a topic
- When the learner needs to synthesize everything learned so far
- When the topic has a natural "build a real thing" culmination

## Step 3: Define the Lab Deliverable

Every lab must have a clear, testable deliverable. The learner must be able to answer "did I complete this lab?" definitively.

Good deliverables:
- "A running program that passes all test assertions in `lab/test_lab.py`"
- "A configured system that responds correctly to the commands in `lab/verify.sh`"
- "A filled-in diagram that accurately shows the [concept] for the provided inputs"
- "A working implementation of [feature] that produces the expected outputs for all test cases"

Bad deliverables:
- "Understand X" (not testable)
- "Explore X" (no completion criterion)
- "Try running the examples" (trivially completable)

## Step 4: Write the Lab

Create the following file structure:

```
TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/labs/
└── lab-[N]/
    ├── README.md          ← Main lab instructions
    ├── starter/           ← Starter code or configuration files
    │   └── [files]
    ├── solution/          ← Reference solution (hidden from learners)
    │   └── [files]
    └── verify.sh          ← Automated verification script
```

Where [N] is 01 for the first lab, 02 for the second, etc.

### Write lab-[N]/README.md

```markdown
# Lab [N]: [Lab Title]

**Module:** [[TOPIC_NAME/module-[MODULE_NUMBER]-[slug]]]
**Type:** [LAB_TYPE]
**Difficulty:** [Beginner | Intermediate | Advanced | Expert]
**Estimated time:** [N–M minutes]

---

## Overview

[2–3 paragraph description of what this lab builds, why it matters, and what the learner will understand better after completing it.]

## Learning Objectives

By completing this lab, you will have:

1. [Concrete objective — something you will have built or configured]
2. [Another concrete objective]
3. [...]

## Prerequisites

Before starting this lab:

- [ ] You have completed Module [MODULE_NUMBER] up to and including [specific section]
- [ ] Your environment is set up ([link to environment setup])
- [ ] [Any specific prerequisites — tools installed, accounts created, etc.]

## What You're Building

[1–2 paragraphs describing the final artifact in concrete terms. Include a diagram if the architecture or flow is non-trivial.]

[Mermaid diagram if appropriate:]
```mermaid
[diagram showing what will be built]
```

## Environment Setup

[Step-by-step setup instructions specific to this lab:]

```bash
# Clone or navigate to the starter directory
cd TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/labs/lab-[N]/starter/

# Install dependencies (if any)
[command]

# Verify setup
[verification command and expected output]
```

> [!IMPORTANT]
> If setup fails, check [specific troubleshooting section]. The most common issue is [most common issue].

---

## Lab Steps

### Step 1: [Descriptive Step Name] (~N minutes)

**What you're doing:** [1–2 sentences explaining the goal of this step]

**Why:** [1 sentence explaining why this step matters for the overall lab]

**Instructions:**

1. [Specific, unambiguous instruction]
2. [Next instruction]
3. [...]

[Code or configuration to write, with a clear indication of which file to edit:]

**Edit `starter/[filename]`:**
```[language]
// Replace the TODO comment with your implementation:
[starter code with TODO marker]
```

[Expected output or verification:]
```bash
# Run to verify this step:
[verification command]

# Expected output:
[exact expected output or description of correct behavior]
```

> [!TIP]
> [Helpful hint for this step — optional but recommended for difficult steps]

> [!WARNING]
> [Common mistake for this step — what to watch out for]

---

### Step 2: [Next Step Name]

[Follow the same format as Step 1]

---

[Continue for all steps]

---

## Checkpoints

After each major step, verify your progress using the checkpoint script:

```bash
./verify.sh --step [N]
```

Expected results:
- Step 1: [What PASS means]
- Step 2: [What PASS means]
- ...
- Final: [What a fully passing lab looks like]

---

## Troubleshooting

### [Common Error 1]

**Symptom:** [What the learner sees]
**Cause:** [Why it happens]
**Fix:** [Specific fix]

### [Common Error 2]

[...]

---

## Extension Challenges

If you finish early or want to go deeper:

1. **[Extension 1]:** [Description and what it would test]
2. **[Extension 2]:** [Description]
3. **[Extension 3 — for the ambitious]:** [Description]

---

## Reflection Questions

After completing the lab, think about:

1. [Question connecting the lab to the module's concepts]
2. [Question about what the learner found surprising or difficult]
3. [Question connecting the lab to real-world usage]

Add your answers to `TOPICS/[TOPIC_NAME]/modules/[MODULE_NUMBER]_[slug]/QUESTIONS.md`.

---

## What You Built

[Final paragraph summarizing what the lab produced, why it matters, and what concept it has cemented. Should make the learner feel good about having completed it.]

**Your lab result demonstrates:**
- [Concept it demonstrates]
- [Another concept]

---

## References

- [Relevant section in module README]
- [Relevant resource from RESOURCES.md]
```

### Write starter/ Files

Create the starter files with:
- Correct structure and boilerplate
- `# TODO:` or `// TODO:` comments marking exactly where the learner must implement
- Enough context that the learner is never confused about what file to edit
- Type signatures or function stubs (for typed languages) pre-filled
- Test files that verify the implementation (not to be modified by the learner)

### Write solution/ Files

Create the complete reference solution:
- Correct, idiomatic, fully commented
- Every non-obvious decision explained with a comment: `# Why: [reason]`
- The solution directory is not referenced in the lab instructions — it exists for instructors and for the learner after they have attempted the lab

### Write verify.sh

Write a shell script that verifies each step automatically:

```bash
#!/usr/bin/env bash
# verify.sh — automated lab verification
# Usage: ./verify.sh [--step N] [--all]

set -e

STEP=${1:-"--all"}
PASS=0
FAIL=0

check() {
    local description="$1"
    local command="$2"
    local expected="$3"
    
    actual=$(eval "$command" 2>&1)
    if [[ "$actual" == *"$expected"* ]]; then
        echo "✓ $description"
        ((PASS++))
    else
        echo "✗ $description"
        echo "  Expected: $expected"
        echo "  Got: $actual"
        ((FAIL++))
    fi
}

# Step 1 checks
if [[ "$STEP" == "--step" && "$2" == "1" ]] || [[ "$STEP" == "--all" ]]; then
    echo "--- Step 1 ---"
    check "[Description]" "[command to run]" "[expected output substring]"
fi

# [Continue for all steps]

echo ""
echo "Results: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]] && echo "LAB COMPLETE" && exit 0 || exit 1
```

## Step 5: Update Environment Files

If the lab requires packages or tools not already in `environments/[TOPIC_NAME]/`:
1. Add them to `environments/[TOPIC_NAME]/requirements.txt` (for Python)
2. Update the Dockerfile if a system package is needed
3. Note the additions in your output summary

## Step 6: Update Module Files

After generating the lab:

1. Add a link to the lab in `README.md` under a "Labs" section:
```markdown
## Labs

- [Lab 1: [Lab Title]](./labs/lab-01/) — [LAB_TYPE] lab, ~[N] minutes
```

2. Add to `PROJECTS.md` if the lab's output could be extended into a project:
```markdown
### Extend Lab [N]: [Title]
The lab produced [artifact]. Extend it by [specific extension].
```

## Output Format

1. **Lab Design** — the concept, deliverable, and rationale from Steps 2–3
2. **File manifest** — every file to be created with paths
3. **lab-[N]/README.md** — full content
4. **starter/ files** — all starter code
5. **verify.sh** — the verification script
6. **solution/ files** — reference solutions
7. **Environment updates** — any additions to environment files
8. **Module file updates** — changes to README.md and PROJECTS.md
```

## Examples

**Setup lab for Go:**
```
TOPIC_NAME: go
MODULE_NUMBER: 01
LAB_TYPE: Setup
```
Output: Lab that walks through installing Go, writing and running a first program, understanding GOPATH, and verifying the setup.

**Implementation lab for Rust ownership:**
```
TOPIC_NAME: rust
MODULE_NUMBER: 03
LAB_TYPE: Implementation
```
Output: Lab that builds a string manipulation library from scratch, encountering and resolving ownership errors progressively.

**Capstone lab for networking:**
```
TOPIC_NAME: networking
MODULE_NUMBER: 08
LAB_TYPE: Capstone
```
Output: Open-ended lab building a small TCP client/server application using concepts from all previous networking modules.

## Notes

- Labs are time-boxed learning experiences. Estimate realistically — a lab that says "30 minutes" but actually takes 3 hours damages trust and discourages completion.
- The `verify.sh` script is the lab's most important component after the instructions. Automated feedback removes the anxiety of "did I do this right?" and lets learners self-assess immediately.
- For labs involving external services (APIs, databases, cloud providers), always provide a local alternative (a mock, a local server, a simulated environment). Labs that require account creation are barriers to completion.
- The starter code should be enough that the learner is never confused about what to write or where, but incomplete enough that they must actually engage with the concept. The right balance is roughly: starter code handles 40% of the lab, the learner implements 60%.
- Reference solutions exist to help instructors and for learners who are truly stuck. They should not be the first thing learners look at — structure the lab so curiosity drives completion before peeking.
