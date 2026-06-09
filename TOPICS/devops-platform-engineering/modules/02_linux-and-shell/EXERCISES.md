# Exercises: Module 02 — Linux and Shell

> Full exercises will be added when this module's complete content is written.
> The following are placeholder stubs showing the planned exercise structure.

## Instructions

Complete each exercise in order. Exercises increase in difficulty.

---

## Easy Exercises (1–3)

### Exercise 1
**Difficulty:** Easy
**Objective:** Navigate the filesystem hierarchy

List the contents of `/etc`, `/var/log`, and `/proc/1` and describe what you find in each.

---

### Exercise 2
**Difficulty:** Easy
**Objective:** Basic process management

Find the PID of a running process (nginx, sshd, or any other service), send it a SIGHUP, and verify it handled the signal via `journalctl`.

---

### Exercise 3
**Difficulty:** Easy
**Objective:** File permissions

Create a directory `/tmp/lab-permissions`, set its permissions to `750`, create a file inside it owned by root, and verify that a non-root user cannot read it.

---

## Medium Exercises (4–6)

### Exercise 4
**Difficulty:** Medium
**Objective:** Write a bash script with proper error handling

Write a backup script that archives a directory, timestamps the archive, and exits with an appropriate error code if the source directory doesn't exist.

---

### Exercise 5
**Difficulty:** Medium
**Objective:** systemd unit file

Create a systemd unit file for a hypothetical web application. Include: restart policy, resource limits, security hardening directives, and logging configuration.

---

### Exercise 6
**Difficulty:** Medium
**Objective:** Log analysis with standard utilities

Parse `/var/log/auth.log` (or a similar log file) to find: the top 5 IP addresses with failed SSH login attempts, and the hours with the most login activity.

---

## Hard Exercises (7–8)

### Exercise 7
**Difficulty:** Hard
**Objective:** Complete deployment script

Write a production-quality bash deployment script that: validates prerequisites, creates a backup, performs the deployment, runs health checks, and rolls back on failure.

---

### Exercise 8
**Difficulty:** Hard
**Objective:** Advanced awk/sed/jq processing

Write a script that parses JSON application logs (one JSON object per line), extracts request duration and status code, and produces a summary report with percentile latencies.

---

## Expert Exercise (9)

### Exercise 9
**Difficulty:** Expert
**Objective:** Harden a Linux system

Given a fresh Ubuntu 22.04 server, write a hardening script that: disables root SSH login, configures fail2ban, sets up unattended security upgrades, configures auditd, and applies CIS benchmark Level 1 settings. Document each change and the threat it mitigates.
