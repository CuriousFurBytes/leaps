# Answers: Module 01 — Introduction to DevOps and Platform Engineering

## Answer Key

### Easy Questions

**Q1:** The "wall of confusion" is the organizational and cultural barrier between Development teams (incentivized to change things, ship features, move fast) and Operations teams (incentivized to keep systems stable, prevent changes, avoid outages). When these groups are separate with opposing incentives, software delivery becomes slow, adversarial, and unreliable.

**Q2:** The four DORA key metrics are: (1) Deployment Frequency, (2) Lead Time for Changes, (3) Change Failure Rate, (4) Time to Restore Service (MTTR — Mean Time to Restore).

**Q3:** MTTR stands for Mean Time to Restore (also acceptable: Mean Time to Recovery). The elite tier performance for MTTR is less than one hour.

**Q4:** The first DevOpsDays conference was held in 2009 in Ghent, Belgium. It was organized by Patrick Debois.

**Q5:** Toil (as defined by Google SRE) is work that is manual, repetitive, automatable, tactical (reactive rather than strategic), and produces no lasting improvement to the system. Example: manually SSH-ing into a server to restart a crashed process every time it fails (vs. configuring systemd to restart it automatically).

### Medium Questions

**Q6:** The First Way optimizes the flow of work from left (idea/planning) to right (running production code). Reducing batch size improves flow because smaller batches move through the delivery pipeline faster, are easier to test and validate, produce simpler deployments, enable faster rollbacks, and reduce the cognitive complexity of understanding what changed. Large batches accumulate work at each stage, create queuing delays, and make failures exponentially harder to diagnose.

**Q7:** An SLI (Service Level Indicator) is the actual measurement; an SLO is the target; an SLA is the business/contractual commitment. For a payment API: SLI = "percentage of /charge requests that succeed within 2 seconds"; SLO = "99.9% of /charge requests succeed within 2 seconds, measured over a rolling 28-day window"; SLA = "If API availability drops below 99.5% in any calendar month, customers receive a 10% credit."

**Q8:** A golden path is a pre-built, opinionated, well-supported route for accomplishing a common task (e.g., deploying a new microservice). It reduces cognitive load because application teams no longer need to understand Kubernetes, Terraform, Prometheus, CI/CD configuration, security scanning, and Vault — instead, they run one command and the platform handles all that complexity. Teams can focus on their business logic instead of infrastructure concerns.

**Q9:** It seems counterintuitive because conventional wisdom says moving faster means breaking more things. Elite performers disprove this by: (a) deploying in small batches (each change is simpler, easier to test, and trivial to roll back), (b) investing heavily in automated testing (catching failures before production, not after), (c) using feature flags (deploying code without activating features), and (d) building reliable rollback mechanisms. The opposite — infrequent large-batch deployments — produces high change failure rates because so many changes accumulate that failures are inevitable and rollback is often impossible.

**Q10:** Conway's Law states that organizations design systems mirroring their communication structures. For an IDP, this means: the platform will reflect how the Platform team is organized. If the Platform team is siloed into "infra" and "CI/CD" sub-teams, the platform will have fragmented tools. If organized around developer workflows and user journeys, the platform will feel coherent. Teams building an IDP should design their team structure around the desired platform architecture, not the reverse.

### Hard Questions

**Q11:** The script has several bugs/bad practices:

```bash
#!/usr/bin/env bash   # more portable than #!/bin/bash
set -euo pipefail    # ADDED: fail on errors, unset vars, pipeline failures

SERVICE=nginx        # OK, but ideally quoted: SERVICE="nginx"

# BUG 1: `systemctl status` returns multi-line output and a non-zero exit
# code when service is not running. Comparing with == "active" will never
# match because `status` contains many lines.
# FIX: Use `systemctl is-active` which returns "active" or "inactive"

# BUG 2: [ $status == "active" ] is dangerous if $status is empty or has spaces.
# Use [[ ]] (bash double brackets) for string comparisons.

# BUG 3: No error handling if systemctl restart fails.

if systemctl is-active --quiet "$SERVICE"; then
    echo "Service $SERVICE is running"
else
    echo "Service $SERVICE is down, attempting restart..."
    if systemctl restart "$SERVICE"; then
        echo "Restart successful"
    else
        echo "ERROR: Failed to restart $SERVICE" >&2
        exit 1
    fi
fi
```

Key fixes: use `is-active --quiet` (returns clean boolean), use double quotes around variables, use `[[ ]]` for comparisons, add error handling for the restart.

**Q12:** With 12 teams each managing their own Kubernetes, Terraform, Prometheus, and CI/CD independently, the cognitive load is: every engineer must understand all four complex tool ecosystems. When the number grows to 20 teams, each new team spends weeks setting up infrastructure before writing any product code. The same mistakes are made repeatedly across teams; security and compliance drift occurs silently.

Platform Engineering addresses this by building: (a) a service scaffolding template (one command creates a repository with pre-configured CI/CD, K8s manifests, monitoring, and dashboards), (b) a self-service portal (Backstage or equivalent) where teams register services and request namespaces/environments, (c) centralized, managed Terraform modules for common infrastructure patterns, (d) pre-built Prometheus alerting rules and Grafana dashboard templates. Application teams stop worrying about: Kubernetes RBAC configuration, Terraform state management, CI/CD pipeline syntax, Prometheus scrape config, container security scanning setup.

**Q13:** Likely causes: the postmortems identify the immediate cause ("the config was wrong") but not the systemic cause ("our deployment process does not validate configuration before apply"). Action items are assigned to individuals ("Alice will double-check configs") rather than to systems ("add config validation to the deploy pipeline"). Or the action items are completed in the postmortem but never prioritized against feature work. Fix: require action items to be systemic improvements (process, tooling, automation changes — never "Person X will be more careful"). Track action item completion rate and include it in team health metrics. Allocate dedicated time each sprint for postmortem action items.

**Q14:**
```bash
#!/usr/bin/env bash
# Calculate deployment frequency from git tags
set -euo pipefail

REPO_PATH="${1:-.}"
WINDOW_DAYS=30

cd "$REPO_PATH"

# Count deploy tags in the last 30 days
DEPLOY_COUNT=$(git tag --sort=-creatordate | grep -E '^deploy-[0-9]{8}-[0-9]{2}$' | while read -r tag; do
    TAG_DATE=$(git log -1 --format="%ct" "$tag" 2>/dev/null)
    CUTOFF=$(date -d "${WINDOW_DAYS} days ago" +%s 2>/dev/null || date -v "-${WINDOW_DAYS}d" +%s)
    if [[ "$TAG_DATE" -gt "$CUTOFF" ]]; then
        echo "$tag"
    fi
done | wc -l)

echo "Deployments in last ${WINDOW_DAYS} days: ${DEPLOY_COUNT}"
echo "Deployment frequency: $(echo "scale=2; $DEPLOY_COUNT / $WINDOW_DAYS" | bc) per day"
```

### Expert Questions

**Q15:** Elite organizations achieve speed and stability simultaneously because the practices that increase deployment frequency also reduce failure rates. The key mechanism is **small batch sizes**: deploying tiny changes means each deployment is simple, easy to understand, well-tested, and trivially reversible. The First Way (optimize flow) naturally produces high deployment frequency AND low CFR when implemented correctly — not just "deploy more often" but "deploy smaller batches, faster."

The Second Way (feedback loops) provides fast signals about failures, enabling short MTTR. Comprehensive automated testing (CI), immediate deployment monitoring (CD metrics), and fast rollback mechanisms mean that when failures do occur, they are caught and fixed within minutes, not days. Automated testing also prevents most failures before they reach production.

The Third Way (continuous improvement) creates the virtuous cycle: failures are analyzed through blameless postmortems, systemic improvements are implemented (better tests, safer deployment mechanisms, better monitoring), and the system becomes progressively more reliable even as it moves faster. Low performers are stuck because they have too few deployments to practice delivery (no Second Way feedback to improve the process) and no time allocated to improvement (no Third Way).

**Q16:** (Detailed answer expected — key elements would include: dissolve the "DevOps team" as a gatekeeper and reconstitute it as a Platform team; define an MVP platform that lets teams self-serve the most common bottlenecks first; create a service catalog and scaffolding to eliminate the 2-week "new pipeline" wait; implement GitOps so teams manage their own deployments without platform team intervention; define platform SLOs — the platform's availability and response time are products; measure success by developer satisfaction survey, lead time change, and platform team toil reduction; existing DevOps engineers become platform engineers who build and maintain the platform rather than executing requests.)

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
