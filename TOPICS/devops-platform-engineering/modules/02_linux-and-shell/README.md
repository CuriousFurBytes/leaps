# Module 02: Linux and Shell

[← Module 01: Introduction](../01_introduction/) | [Topic Home](../../README.md) | [Next → Module 03: Containers](../03_containers/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Beginner--Intermediate-yellowgreen)
![Time](https://img.shields.io/badge/time-8--10h-orange)

> Linux is the operating system of the cloud. This module covers the filesystem, process management, bash scripting, systemd, cron, and user/permission management that every DevOps practitioner must master.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Key Concepts](#key-concepts)
6. [Examples](#examples)
7. [Common Pitfalls](#common-pitfalls)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

---

## Overview

> [!NOTE]
> **This module is a stub.** Full content will be added in a future update. The objectives, key topics, and cross-links are complete. Use the Resources file for self-study in the meantime.

Every container runs Linux. Every Kubernetes node runs Linux. Every CI/CD runner runs Linux. You can work with DevOps tools without understanding Linux — until something breaks, at which point you are helpless without this knowledge.

This module covers the Linux fundamentals every DevOps practitioner needs: how the filesystem is organized, how processes work, how to write reliable bash scripts, how systemd manages services, how to schedule work with cron, and how user and permission management protects multi-tenant systems.

---

## Prerequisites

- Module 01: Introduction to DevOps and Platform Engineering
- Basic familiarity with a command-line interface (any OS)

---

## Objectives

By the end of this module, you will be able to:

1. Navigate the Linux filesystem hierarchy and understand the purpose of key directories (`/etc`, `/var`, `/proc`, `/sys`, `/tmp`, `/usr`)
2. Manage processes — view running processes, send signals, understand foreground/background jobs, and use `nice`/`renice`
3. Write robust bash scripts using `set -euo pipefail`, functions, arrays, string manipulation, and proper error handling
4. Manage systemd services — create unit files, enable/disable/start/stop services, and read journal logs
5. Schedule recurring tasks with cron and understand the `crontab` syntax
6. Manage users, groups, file permissions (rwx/octal), and `sudo` configuration
7. Use standard Linux utilities — `grep`, `awk`, `sed`, `find`, `xargs`, `sort`, `uniq`, `jq` — for log analysis and data processing

---

## Theory

> [!NOTE]
> Full theory content coming soon. The following subsection titles outline what will be covered.

### The Linux Filesystem Hierarchy

The Filesystem Hierarchy Standard (FHS) defines where things live on a Linux system.

```bash
/           # root of the filesystem
├── bin/    # essential user binaries (ls, cp, mv — symlink to /usr/bin on modern systems)
├── etc/    # system configuration files (nginx.conf, passwd, hosts)
├── home/   # user home directories (/home/alice, /home/bob)
├── proc/   # virtual filesystem exposing kernel/process information
├── sys/    # virtual filesystem exposing kernel hardware state
├── tmp/    # temporary files (cleared on reboot)
├── usr/    # user programs and data (/usr/bin, /usr/lib, /usr/local)
└── var/    # variable data: logs, databases, mail (/var/log, /var/lib)
```

### Process Management

```bash
# View running processes
ps aux                           # all processes, BSD-style
ps aux | grep nginx             # filter for nginx
pgrep nginx                     # get PIDs of nginx processes
top                              # interactive process viewer
htop                             # better interactive viewer (install separately)

# Process signals
kill -SIGTERM <pid>             # graceful shutdown (process can clean up)
kill -SIGKILL <pid>             # immediate termination (cannot be caught)
kill -SIGHUP <pid>              # hangup — nginx uses this to reload config
killall nginx                   # kill all processes named nginx

# Job control
command &                        # run in background
jobs                             # list background jobs
fg %1                            # bring job 1 to foreground
nohup command &                  # run immune to hangup (survives terminal close)
```

### Bash Scripting Fundamentals

```bash
#!/usr/bin/env bash
# safe-script.sh — demonstrates essential bash patterns

set -euo pipefail
# -e: exit on error
# -u: treat unset variables as errors
# -o pipefail: if any command in a pipe fails, the whole pipe fails

# Functions
deploy_service() {
    local service_name="$1"    # local scope, named parameter
    local version="$2"

    echo "Deploying $service_name version $version"

    if ! systemctl is-active --quiet "$service_name"; then
        echo "WARNING: $service_name is not running before deploy" >&2
    fi
    # ... deployment logic ...
}

# Arrays
SERVICES=("nginx" "postgresql" "redis")
for service in "${SERVICES[@]}"; do
    echo "Checking: $service"
done

# String manipulation
VERSION="v1.2.3"
MAJOR="${VERSION%%.*}"          # remove longest match from end: "v1"
WITHOUT_V="${VERSION#v}"        # remove shortest match from start: "1.2.3"

# Trap for cleanup on exit
cleanup() {
    echo "Cleaning up temporary files..."
    rm -f /tmp/deploy-lock-$$   # $$ is the current PID
}
trap cleanup EXIT

deploy_service "nginx" "1.25.0"
```

### systemd Service Management

```bash
# Service lifecycle
systemctl start nginx
systemctl stop nginx
systemctl restart nginx
systemctl reload nginx          # reload config without restart (if supported)
systemctl status nginx          # detailed status including recent logs
systemctl enable nginx          # auto-start on boot
systemctl disable nginx

# Journal logs
journalctl -u nginx             # all logs for nginx
journalctl -u nginx -f          # follow (tail -f equivalent)
journalctl -u nginx --since "1 hour ago"
journalctl -p err               # only error-level messages
```

Custom systemd unit file example:

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application Server
After=network.target

[Service]
Type=simple
User=myapp
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/server --port 8080
Restart=on-failure
RestartSec=5s
# Security hardening
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/var/lib/myapp /var/log/myapp

[Install]
WantedBy=multi-user.target
```

### Cron and Scheduled Tasks

```bash
# crontab syntax: minute hour day-of-month month day-of-week command
# *  *  *  *  *  command
# |  |  |  |  |
# |  |  |  |  └── day of week (0-7, 0 and 7 are Sunday)
# |  |  |  └───── month (1-12)
# |  |  └──────── day of month (1-31)
# |  └─────────── hour (0-23)
# └────────────── minute (0-59)

# Examples:
0 2 * * * /opt/scripts/backup.sh           # 2 AM every day
*/15 * * * * /opt/scripts/health-check.sh  # every 15 minutes
0 9 * * 1 /opt/scripts/weekly-report.sh   # every Monday at 9 AM
```

### File Permissions and Users

```bash
# Octal permission notation
# 7 = rwx (read + write + execute)
# 6 = rw- (read + write)
# 5 = r-x (read + execute)
# 4 = r-- (read only)
# 0 = --- (no permissions)

chmod 755 script.sh              # owner: rwx, group: r-x, others: r-x
chmod 600 /etc/myapp/secret.key  # owner: rw-, group: ---, others: ---
chown myapp:myapp /opt/myapp     # set owner and group

# User and group management
useradd -r -s /bin/false myapp   # create system user (no login shell)
groupadd myapp
usermod -aG docker alice          # add alice to the docker group

# sudo configuration (/etc/sudoers.d/myapp)
# myapp ALL=(root) NOPASSWD: /bin/systemctl restart myapp.service
```

---

## Key Concepts

> Full key concepts section coming soon. Key terms include: process, signal, inode, hard link, soft link, file descriptor, stdin/stdout/stderr, exit code, shebang, unit file, crontab, umask, setuid/setgid.

---

## Examples

> Full worked examples coming soon. Will include: a complete deployment script, a log rotation script, a systemd unit for a custom service, and a cron-based monitoring script.

---

## Common Pitfalls

> Full pitfalls section coming soon. Key pitfalls include: scripts without `set -euo pipefail`, unquoted variables (word splitting), cron PATH issues, forgetting `systemctl daemon-reload` after editing unit files, and permission escalation via setuid.

---

## Cross-Links

- [[devops-platform-engineering/modules/01_introduction]] — DevOps culture concepts that motivate the automation we build with bash
- [[devops-platform-engineering/modules/03_containers]] — containers run on Linux processes; this module's knowledge is prerequisite for understanding container isolation
- [[networks]] — Linux networking tools (`ss`, `netstat`, `ip`, `iptables`) build on network fundamentals

---

## Summary

- Linux is the universal substrate for cloud infrastructure; all containers and Kubernetes nodes run it
- The FHS organizes files into a well-defined hierarchy; `/etc` for config, `/var` for state, `/proc` for runtime process info
- `set -euo pipefail` is the safety harness for bash scripts; never write production scripts without it
- systemd manages services on modern Linux; `journalctl` is the primary log viewing tool
- Cron schedules periodic tasks; the five-field syntax encodes minute, hour, day, month, day-of-week
- File permissions use the octal rwx model; principle of least privilege applies — no more permissions than necessary
- Standard Unix utilities (`grep`, `awk`, `sed`, `jq`) compose powerfully for log analysis and data processing
