# Exercises: Module 02 — Layered Models and Encapsulation

## Instructions
Complete each exercise in order. Exercises increase in difficulty. Submit your answers by editing this file or committing a solutions file.

---

## Easy Exercises (1–3)

### Exercise 1
**Difficulty:** Easy
**Objective:** Identify core vocabulary.

Define five terms from this module in your own words and include one real example for each.

### Exercise 2
**Difficulty:** Easy
**Objective:** Run a basic diagnostic command.

Run a safe lookup for `example.com` and record what question the command answered.

```bash
dig example.com
```

### Exercise 3
**Difficulty:** Easy
**Objective:** Separate observations from guesses.

Write three observations you can make before deciding why a service is unreachable.

## Medium Exercises (4–6)

### Exercise 4
**Difficulty:** Medium
**Objective:** Explain a traffic path.

Describe what happens when a laptop requests `https://example.com`, using at least four module concepts.

### Exercise 5
**Difficulty:** Medium
**Objective:** Interpret command output.

Given an `ip route` table from your machine, identify the default route and explain why it matters.

### Exercise 6
**Difficulty:** Medium
**Objective:** Compare related concepts.

Compare reachability, connectivity, and application health in a short table.

## Hard Exercises (7–8)

### Exercise 7
**Difficulty:** Hard
**Objective:** Build a troubleshooting checklist.

Create a five-step checklist for debugging a failed web request without assuming the cause.

### Exercise 8
**Difficulty:** Hard
**Objective:** Write runnable code that tests a service.

Write a small Python script that opens a TCP connection to a host and port, then reports success or failure.

```python
import socket

def can_connect(host, port):
    with socket.create_connection((host, port), timeout=5):
        return True

print(can_connect("example.com", 80))
```

## Expert Exercise (9)

### Exercise 9
**Difficulty:** Expert
**Objective:** Synthesize design and operations thinking.

Design a tiny office network on paper. Include users, a default gateway, DNS dependency, one internal service, one public service, and three checks you would monitor.
