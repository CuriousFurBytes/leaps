# Test: Module 01 — Introduction to DevOps and Platform Engineering

**Instructions:** Answer all questions. Write your answers directly below each question.
Bonus questions are optional and can raise your score above 100%.

**Total Points:** 37 pts (Easy: 5 + Medium: 10 + Hard: 12 + Expert: 10)
**Bonus Available:** 5 pts

---

## Section 1: Easy Questions (1 pt each)

**Q1.** What is the "wall of confusion" in DevOps, and which two organizational groups does it divide?

> Answer:

---

**Q2.** List the four DORA key metrics by name.

> Answer:

---

**Q3.** What does the acronym "MTTR" stand for, and what DORA tier represents "elite" performance for this metric?

> Answer:

---

**Q4.** In which year was the first DevOpsDays conference held, and who organized it?

> Answer:

---

**Q5.** What is "toil" as defined in the SRE model? Give one example.

> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Explain the First Way of DevOps in your own words. Why does reducing batch size improve flow?

> Answer:

---

**Q7.** What is the difference between an SLO and an SLA? Give an example of each for a hypothetical payment API.

> Answer:

---

**Q8.** What is a "golden path" in Platform Engineering, and why does it reduce cognitive load on application teams?

> Answer:

---

**Q9.** The DORA research found that elite performers simultaneously achieve high deployment frequency AND low change failure rate. Why does this seem counterintuitive, and what explains it?

> Answer:

---

**Q10.** What is Conway's Law? How is it relevant to the design of an Internal Developer Platform?

> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** The following bash script is intended to check if a service is running and restart it if not. Find and fix at least two bugs or bad practices:

```bash
#!/bin/bash
SERVICE=nginx

status=$(systemctl status $SERVICE)
if [ $status == "active" ]; then
    echo "Service is running"
else
    echo "Service is down, restarting"
    systemctl restart $SERVICE
fi
```

Write the corrected script with an explanation of each fix.

> Answer:

---

**Q12.** A company runs 12 microservices. Each service team manages its own Kubernetes configuration, Terraform code, Prometheus alerting rules, and CI/CD pipeline. The company is growing and wants to add 8 more services next year.

Describe the cognitive load problem this creates and explain how Platform Engineering would address it. What would the Platform team build, and what would it allow application teams to stop worrying about?

> Answer:

---

**Q13.** An organization's blameless postmortem process has been running for 6 months. Engineers are filling out the template correctly, but incident rates have not improved and the same types of failures recur. What is likely going wrong, and what would you change?

> Answer:

---

**Q14.** Design a simple shell script (pseudocode or working bash) that calculates deployment frequency from git tags. Assume deployment tags follow the pattern `deploy-YYYYMMDD-HH`. The script should output the average number of deployments per day over the last 30 days.

> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** The DevOps Handbook describes the tension between speed (deployment frequency, lead time) and stability (change failure rate, MTTR) as a "false dilemma." Synthesize what you have learned in this module to explain why elite organizations achieve both simultaneously, while low performers are stuck trading one for the other. Your answer should reference the Three Ways and at least two specific practices.

> Answer:

---

**Q16.** You are a Platform Engineering lead joining an organization that has a "DevOps team" of 8 people responsible for all CI/CD, Kubernetes administration, and deployment automation for 40 application engineers across 12 teams. The DevOps team is a bottleneck — teams wait 2 weeks for new pipeline configurations, 1 week for Kubernetes namespace changes, and infrastructure requests take 3 weeks.

Design a 12-month transformation plan to move this organization toward a true Platform Engineering model. Your plan must address: (a) the organizational change required, (b) what the platform must provide for teams to self-serve, (c) how you measure success, and (d) what you do with the existing DevOps team's skills.

> Answer:

---

## Bonus Questions

**Bonus 1.** (+5 pts) The DORA research uses the term "cluster analysis" to identify performance groups. Why is this methodology stronger than simply ranking organizations by a single metric? What would be lost if DORA had defined "elite" as simply "top 25% by deployment frequency"?

> Answer:
