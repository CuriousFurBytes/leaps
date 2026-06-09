# Test — Module 01: Introduction to Computer Networks

**Topic:** [[networks]]
**Module:** [[networks/modules/01_introduction]]

---

## Before You Begin

> [!WARNING]
> **Do not look at ANSWERS.md or your notes during the test.**
> The purpose of this test is to surface what you truly know vs. what you think you know.
> An inflated score is worthless. An honest score shows you exactly where to focus next.

**Instructions:**
1. Close all notes, the module README, and any reference materials.
2. Set a timer. Note your start time below.
3. Attempt every question — partial credit exists.
4. After finishing, grade yourself using ANSWERS.md.
5. Record your score in the [Grading Record](#grading-record) at the bottom.

**Start time:** ___________
**End time:** ___________
**Total time:** ___________

---

## Scoring Table

| Section | Question Type | Points Each | # Questions | Max Points |
|---------|--------------|-------------|-------------|------------|
| Section 1: Recall | Easy | 1 pt | 5 | 5 pts |
| Section 2: Conceptual | Medium | 2 pts | 3 | 6 pts |
| Section 3: Applied | Hard | 3 pts | 2 | 6 pts |
| Section 4: Scenario | Hard | 3 pts | 1 | 3 pts |
| Section 5: Discussion | Medium | 2 pts | 1 | 2 pts |
| **Total** | | | **12** | **22 pts** |
| Section 6: Bonus | Expert | +5 pts | 1 | +5 pts |

**Passing score:** 15/22 (68%) &nbsp;·&nbsp; **Target score:** 18/22 (82%)

---

## Section 1: Recall (5 questions × 1 pt = 5 pts)

_Quick recall questions. Answer from memory in 1–3 sentences each._

**1.1** What is the PDU name at each of the 7 OSI layers (list them from Layer 1 to Layer 7)?

> _Your answer:_

---

**1.2** What does TTL stand for, and what is its purpose in an IP packet?

> _Your answer:_

---

**1.3** Name three differences between a hub and a switch.

> _Your answer:_

---

**1.4** At which OSI layer does a router operate, and what addressing information does it use to make forwarding decisions?

> _Your answer:_

---

**1.5** What is encapsulation in the context of the network stack?

> _Your answer:_

---

## Section 2: Conceptual Understanding (3 questions × 2 pts = 6 pts)

_Demonstrate that you understand the "why", not just the "what"._

**2.1** Explain why Ethernet (Layer 2) frames must be replaced at every router hop while IP (Layer 3) packets pass through unchanged. What would break if frames were not replaced?

> _Your answer:_

---

**2.2** A colleague tells you: "TCP/IP has 7 layers, just like OSI." Is this correct?
If not, what is the accurate understanding, and how should you explain the relationship between the two models?

> _Your answer:_

---

**2.3** Compare and contrast packet switching and circuit switching. What problem does packet switching solve that circuit switching cannot handle efficiently? Give a concrete example.

> _Your answer:_

---

## Section 3: Applied / Practical (2 questions × 3 pts = 6 pts)

_Show that you can use your knowledge to solve real problems._

**3.1** You run the following command and get this output:

```bash
ping -c 3 192.168.1.1
```

```
PING 192.168.1.1: 56 data bytes
Request timeout for icmp_seq 0
Request timeout for icmp_seq 1
Request timeout for icmp_seq 2
```

And then:

```bash
curl http://192.168.1.1
```

```html
<html><body>Router Admin Panel</body></html>
```

a) What does the `ping` failure tell you?
b) What does the successful `curl` tell you?
c) What is likely happening at the network level? What would you check next?

> _Your answer:_

---

**3.2** A packet originates from host A (IP: 10.0.1.5, MAC: aa:bb:cc:dd:ee:01) and needs to reach host B (IP: 10.0.2.7, MAC: 11:22:33:44:55:66). They are on different subnets. Between them is a single router with two interfaces:
- eth0: 10.0.1.1, MAC: aa:bb:cc:dd:ee:99
- eth1: 10.0.2.1, MAC: 11:22:33:44:55:77

Describe the source and destination MAC and IP addresses at these two points in the journey:
- **Frame 1:** leaving host A toward the router
- **Frame 2:** leaving the router toward host B

> _Your answer:_

---

## Section 4: Scenario / Debugging (1 question × 3 pts = 3 pts)

_Analyze a realistic scenario and identify what's wrong or what should be done._

**4.1** A developer has written a Python application that sends data to a remote server. They report: "My application works fine locally, but when I deploy it, some messages are received out of order by the server."

The developer tells you:
- They are using UDP
- Messages are sent about 100ms apart
- The path from client to server involves multiple routers

a) Is this behavior expected? Why or why not?
b) What protocol-level explanation accounts for out-of-order delivery?
c) What would you recommend the developer do to fix this? Give two options with tradeoffs.

> _Your answer:_

---

## Section 5: Essay / Discussion (1 question × 2 pts = 2 pts)

_Open-ended. There is more than one good answer. Show your reasoning._

**5.1** The OSI model was published in 1984. TCP/IP predates it (ARPANET's TCP/IP transition was in 1983) and is what the internet actually runs on. Yet networking engineers still talk about "Layer 3" and "Layer 7" using OSI terminology. Why do you think the OSI model persists in professional discourse even though it's not what the internet implements? Is it still useful?

Consider at least two perspectives in your answer.

> _Your answer (aim for 3–6 sentences):_

---

## Section 6: Bonus Challenge (1 question × +5 pts)

> [!NOTE]
> This question is optional. It will not count against you if you skip it or get it wrong.
> Only attempt it after completing Sections 1–5.

**6.1** The `traceroute` tool works by sending packets with incrementing TTL values and listening for ICMP Time Exceeded responses. Some traceroutes show `***` for intermediate hops and then successfully reach the destination.

Design an alternate traceroute implementation that would work even when routers are configured to not send ICMP Time Exceeded messages. What protocol or technique would you use, and what are the tradeoffs of your approach? (Hint: think about what `traceroute` on Windows uses by default vs. `traceroute` on Linux.)

> _Your answer:_

---

## Self-Assessment

After grading your test, answer these questions honestly:

**What did I get right and why?**
> _Your reflection:_

**What did I get wrong and why did I make that mistake?**
> _Your reflection:_

**What should I review before moving to the next module?**
> _Your reflection:_

**What score did I get? Do I feel it accurately reflects my understanding?**
> _Your reflection:_

---

## Grading Record

_Append a new row each time you take this test. Do not overwrite previous attempts._

| Date | Attempt | S1 (5) | S2 (6) | S3 (6) | S4 (3) | S5 (2) | Bonus (5) | Total (22) | Grade | Notes |
|------|---------|--------|--------|--------|--------|--------|-----------|-----------|-------|-------|
| — | 1 | — | — | — | — | — | — | —/22 | — | First attempt |

**Grade scale:** A ≥ 90% (≥20/22) &nbsp;·&nbsp; B ≥ 80% (≥18/22) &nbsp;·&nbsp; C ≥ 70% (≥15/22) &nbsp;·&nbsp; D ≥ 60% (≥13/22) &nbsp;·&nbsp; F < 60%

---

_See [ANSWERS.md](./ANSWERS.md) for the answer key. Review it only after completing the test._
