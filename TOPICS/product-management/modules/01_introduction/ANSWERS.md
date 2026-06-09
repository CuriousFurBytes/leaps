# Answers: Module 01 — Introduction to Product Management

## Answer Key

### Easy Questions

**Q1:** The product manager is responsible for deciding what the team should build and why — defining the right problem to solve and ensuring the team builds something that creates value for users and the business.

**Q2:** Three commonly confused roles:
- **Project Manager:** A project manager tracks schedules and deliverables; a PM decides which work exists in the first place
- **Engineering Manager:** An EM manages engineers' careers and technical architecture; a PM partners with engineers but does not manage them
- **UX Designer:** A designer owns how the product looks and functions; a PM owns the problem space and which user needs are worth solving

**Q3:** The three dimensions: Desirability (user needs — will people want this?), Viability (business model — can the business sustain this?), Feasibility (technical/operational capability — can we build and maintain this?)

**Q4:** Output is a thing you shipped (a feature, a release, a component). Outcome is a change in user behavior or business metric that your output produced. "We shipped 3 features" is output. "We increased activation rate from 23% to 38%" is outcome.

**Q5:** Continuous discovery habits is the practice of maintaining a regular (typically weekly) cadence of direct customer contact — interviews, observations, and lightweight experiments — integrated into the team's normal workflow rather than treated as a special phase. The term was coined and systematized by Teresa Torres.

---

### Medium Questions

**Q6:** The "CEO of the product" metaphor is useful because it conveys that the PM has broad accountability for the product's success and must think across all dimensions (users, business, technology). It is misleading because it implies authority the PM does not have: CEOs can hire and fire; PMs cannot. CEOs can direct strategy unilaterally; PMs must achieve alignment through persuasion. The metaphor causes problems when PMs act as though they can command designers and engineers, which damages trust and reduces team quality.

**Q7:** The PM should not automatically build in response to volume of requests. Before building, they should: (1) Talk to 3–5 of those users directly to understand *why* they want this report format — what job are they trying to do? (2) Determine whether this is blocking renewal or is a nice-to-have. (3) Explore whether there are alternative solutions (e.g., a data export API, a BI integration, an existing solution they missed). (4) Estimate the size of the affected user population beyond the 50 tickets. Tickets are a biased sample — only the most motivated users write in. The underlying principle: volume of requests is not the same as validated user need.

**Q8:** Product discovery is the work of figuring out what to build — validating that the problem is real, that users want a solution, and that a proposed solution will work. Product delivery is the work of building the validated solution. Most teams underinvest in discovery because: discovery work is less visible and harder to measure than delivery; teams face pressure to ship, which creates urgency around building; discovery requires tolerating uncertainty, which feels uncomfortable; and most organizations reward output (what was shipped) rather than outcomes (what changed for users).

**Q9:** Sample comparison — B2C vs. B2B:
A B2C PM (e.g., at Spotify) deals with millions of users, uses quantitative signals at scale, and makes decisions primarily through data and experimentation. The job is about understanding mass user behavior and finding insights in aggregate signals.
A B2B PM (e.g., at Salesforce) deals with a small number of enterprise customers, each represented by multiple stakeholders (procurement, IT, end users). The job requires deep stakeholder management, navigating enterprise purchasing cycles, and balancing requirements from paying customers with the needs of actual end-users who may have no buying power. B2B PMs need stronger negotiation and communication skills; B2C PMs need stronger quantitative and experimentation skills.

**Q10:** The roadmap entry lists outputs (dark mode, CSV export, SSO login) with no indication of what problem each solves, why these are the priority, or what outcome success looks like. It treats the roadmap as a commitment to specific features rather than a hypothesis about what will create value.
Corrected version: `Q2: Unlock enterprise adoption — target: complete 3 enterprise pilots and achieve ≥ 80% admin satisfaction; work in this area may include SSO, audit logs, and admin controls, but exact scope will be validated with pilot customers`

---

### Hard Questions

**Q11:** Three discovery questions:
1. **Desirability — Do users want notifications?** What do users say when asked about push notifications? Have we surveyed users who have turned them off about why? The correlation between notifications and workouts might be because engaged users both allow notifications AND work out more — not because notifications cause workouts. Sending unsolicited notifications to disengaged users might trigger opt-outs rather than engagement.
2. **Viability — What's the downstream business impact of notification opt-outs?** If 20% of users turn off all notifications after receiving unsolicited Thursday nudges, that's a long-term retention risk. Does the short-term activation gain outweigh the long-term engagement loss?
3. **Feasibility — Can we personalize this at scale?** "Users who haven't worked out by Thursday" is a segment definition that requires real-time user state tracking. Do we have the infrastructure? Can we exclude users who have scheduled workouts? Can we implement an easy opt-out? What's the delay between user action and notification suppression?

**Q12:**
(a) The Discovery phase was likely skipped or rushed. The team moved from Definition directly to Development without validating the design with real users.
(b) Consequences: After 8 weeks of engineering investment, the team may discover usability problems that require significant design changes, wasting much of the engineering work. They may also discover the onboarding redesign doesn't solve the underlying activation problem because the wrong problem was being solved.
(c) Options at this stage: (1) Run a quick guerrilla usability test now (5 users, 1–2 days) to catch major issues before launch — still cheaper than fixing post-launch. (2) Soft launch to 5–10% of new users with careful monitoring to catch issues at low cost before full rollout. (3) Ship with monitoring and tight feedback loops, treating the first 2 weeks post-launch as a discovery sprint. Tradeoff: the sooner you validate, the cheaper changes are; but delaying further has its own cost (engineering is blocked, momentum is lost).

**Q13:** The Working Backwards press release forces the team to articulate the *outcome* for the user — what their life looks like after using the product — before committing to any implementation. It confronts: Who is this actually for (forces user definition)? What specific problem does it solve (forces problem clarity)? Why would someone care enough to use this (forces desirability validation)? What is the actual user benefit (forces outcome thinking over feature thinking)? By requiring the team to write believably about a product that doesn't exist yet, it surfaces assumptions that might otherwise remain implicit until after significant investment.

**Q14:** Problems with the problem statement:
1. **Solution-first framing:** "Users want dark mode" describes a solution, not a problem. What problem does dark mode solve? Eye strain? Battery life? Aesthetic preference? The problem statement should start from the user's experience, not the solution.
2. **"Because it's trendy"** is not a user need — it's a competitive pressure disguised as a user need. This leads to feature copying without understanding whether the feature creates value.
3. **"Improve user satisfaction"** is unmeasurable as stated. What specific satisfaction metric? What baseline? What target?
4. **"Help us win in the market"** is a business goal, not a user need — it belongs in the viability dimension but cannot substitute for user-need validation.
Corrected approach: First investigate *why* users might want dark mode (user interviews, NPS surveys with open-ended follow-up), identify the specific user problem, define a measurable success metric, and then evaluate whether the business case justifies the investment.

---

### Expert Questions

**Q15:** Acceptable answers should cover: Feature teams receive a list of features to execute and are measured by output (did they ship it?); they have no ownership of outcomes. Empowered product teams receive a problem to solve and are measured by outcomes (did it work?); they have autonomy to discover the best solution. Feature teams make sense when the solution space is known and constrained (e.g., maintaining a regulated compliance feature), when the team lacks the maturity to handle outcome ownership, or as a transitional state. Empowered teams make sense when innovation and user insight matter, when competitive differentiation comes from solving problems better than alternatives, and when the team has the talent to handle ambiguity productively. Strong answers will note that the "empowered" model requires organizational trust and a PM who genuinely understands users and business context — without that, it collapses.

**Q16:** Strong answers should identify: Netflix Quick Laughs represented delivery without discovery — the assumption that "short video format works on phones" was validated at TikTok but not validated for Netflix's specific user base and use case. Netflix users have a fundamentally different job (choose and commit to content) than TikTok users (discover and consume in the moment). The desirability dimension was not validated — no discovery work was done to confirm Netflix users had this job. Spotify Discover Weekly succeeded because the discovery work identified the underlying *job* (the feeling of having a musically knowledgeable friend make you a playlist) and the solution was designed to fulfill that job, not just copy a feature format. The generalizable principle: "It worked elsewhere" is a hypothesis; the question is whether the *job-to-be-done* is the same for your users.

---

## Grading Records

<!-- Grading records are appended below by AI agents. Do not edit manually. -->
