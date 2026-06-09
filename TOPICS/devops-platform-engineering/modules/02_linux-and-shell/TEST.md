# Test: Module 02 — Linux and Shell

> Full test will be written when this module's complete content is finalized.
> Placeholder structure below.

**Total Points:** 37 pts (Easy: 5 + Medium: 10 + Hard: 12 + Expert: 10)
**Bonus Available:** 5 pts

---

## Section 1: Easy Questions (1 pt each)

**Q1.** What is the purpose of the `/etc` directory?
> Answer:

**Q2.** What does `set -euo pipefail` do in a bash script?
> Answer:

**Q3.** What command shows all running processes with detailed information?
> Answer:

**Q4.** What octal value represents `rwxr-xr-x` permissions?
> Answer:

**Q5.** What systemd command shows the logs for a service named `nginx`?
> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Explain the difference between `SIGTERM` and `SIGKILL`. When would you use each?
> Answer:

**Q7.** What is the difference between a hard link and a symbolic link? When would you use each?
> Answer:

**Q8.** Write a cron expression that runs a script every weekday at 6:30 AM.
> Answer:

**Q9.** Explain what the `trap` command does in bash and give an example use case.
> Answer:

**Q10.** What is `stdin`, `stdout`, and `stderr`? How would you redirect stderr to a log file while letting stdout go to the terminal?
> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** Find and fix the bugs in this bash script:
```bash
#!/bin/bash
FILES = $(ls /tmp/*.log)
for file in $FILES; do
    if [ -f $file ]; then
        mv $file /archive/$file
    fi
done
```
> Answer:

**Q12.** Write a systemd service unit file for an application that: runs as a non-root user, restarts on failure, limits memory to 512MB, and protects the system filesystem from writes.
> Answer:

**Q13.** Write a bash one-liner that extracts all unique IP addresses from an nginx access log file and counts how many times each appears, sorted by frequency.
> Answer:

**Q14.** A script runs fine interactively but fails when run from cron. What are the most common causes of this and how do you debug it?
> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** Design a bash deployment script architecture for a zero-downtime rolling update of a fleet of application servers. Describe the functions you would write, the error handling strategy, and how you would handle partial failures.
> Answer:

**Q16.** Explain Linux process namespaces and cgroups. How do these kernel features enable Docker containers? What is the difference between a container and a virtual machine at the kernel level?
> Answer:

---

## Bonus

**Bonus 1.** (+5 pts) Explain what happens step-by-step when you run `ls /tmp` in a bash shell — from keypress to output. Include: shell parsing, PATH lookup, fork/exec, file descriptor inheritance, and the return of output to the terminal.
> Answer:
