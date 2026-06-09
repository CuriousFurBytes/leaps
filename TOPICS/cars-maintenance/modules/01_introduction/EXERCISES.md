# Exercises — Module 01: Introduction to Your Vehicle

> Work through exercises in order — they're designed to build on each other.
> Attempt each problem genuinely before looking at the solution.
> Seeing the solution first might feel like progress, but it isn't.

---

## Instructions

1. **Attempt first.** Spend at least the estimated time on each problem before checking hints or solutions.
2. **Write your work.** Don't just read — actually write or describe your answer.
3. **Check your answer** against the acceptance criteria, not just the solution.
4. **Score yourself honestly** in the [Scoring Log](#scoring-log) at the bottom.
5. If you're stuck after a genuine effort, use the hints one at a time — not all at once.

---

## Difficulty Legend

| Symbol | Difficulty | Expected Time | Points |
|--------|-----------|--------------|--------|
| 🟢 Easy | Recall and basic application | 5–10 min | 1 pt |
| 🟡 Medium | Requires combining 2+ concepts | 15–25 min | 2 pts |
| 🔴 Hard | Multi-step, requires real problem-solving | 30–60 min | 3 pts |
| ⭐ Challenge | Open-ended; more than one good answer | 60+ min | 5 pts |

---

## Exercise 1: Name the Six Systems [🟢 Easy] [1 pt]

### Context
Before you can maintain or diagnose a car, you need to be fluent in the language of its systems.

### Task
Without looking at your notes, list the six major vehicle systems covered in this module and write one sentence describing each one's job.

### Requirements
- [ ] All six systems named correctly
- [ ] Each described in one accurate sentence

### Hints
<details>
<summary>Hint 1 (try without this first)</summary>

Think of what happens when you drive from a parked position to highway speed: what systems are active at each stage?

</details>

### Expected Output / Acceptance Criteria

```
Six systems with accurate one-sentence descriptions each.
Full credit: all 6 correct. Partial (0.5): 4–5 correct.
```

### Solution
<details>
<summary>Show Solution (attempt first!)</summary>

1. **Engine/Powertrain** — Converts fuel into mechanical energy (rotating crankshaft).
2. **Transmission** — Multiplies torque and selects gear ratios to match engine output to driving conditions.
3. **Braking System** — Converts kinetic energy to heat through friction to slow and stop the vehicle.
4. **Suspension and Steering** — Connects wheels to body; absorbs road impacts; allows directional control.
5. **Electrical System** — Starts the engine, generates electricity to charge the battery, and powers all electronic systems.
6. **Cooling System and HVAC** — Manages engine operating temperature; controls cabin air temperature and quality.

</details>

---

## Exercise 2: The Four-Stroke Sequence [🟢 Easy] [1 pt]

### Context
The four-stroke cycle is the fundamental operating principle of most passenger car engines. You need to be able to recite and explain it without hesitation.

### Task
List the four strokes in order and describe what physically happens in the cylinder during each stroke (piston direction, valve states, what enters/exits the cylinder).

### Requirements
- [ ] All four strokes named in correct order
- [ ] Piston direction described for each stroke
- [ ] Valve state (which valves are open/closed) described for each

### Hints
<details>
<summary>Hint 1</summary>

Think of the cycle as: fill → squeeze → bang → blow.

</details>

### Expected Output / Acceptance Criteria

```
Four strokes in order, each with piston direction and valve states.
Full credit: all correct. Partial: minor error in one stroke.
```

### Solution
<details>
<summary>Show Solution</summary>

1. **Intake** — Piston moves DOWN; intake valve OPEN; exhaust valve CLOSED. Air-fuel mixture drawn into cylinder.
2. **Compression** — Piston moves UP; both valves CLOSED. Mixture compressed; spark plug fires near TDC.
3. **Combustion (Power)** — Piston pushed DOWN by expanding combustion gases; both valves still CLOSED. Only power-producing stroke.
4. **Exhaust** — Piston moves UP; exhaust valve OPEN; intake valve CLOSED. Burned gases pushed out of cylinder.

</details>

---

## Exercise 3: Warning Light Urgency Assessment [🟡 Medium] [2 pts]

### Context
You're driving when three warning lights appear. Your response to each determines whether you protect the engine or waste money on a tow for a non-issue.

### Task
For each of the following scenarios, state: (a) what the light likely means, (b) the urgency level, and (c) what you should do.

**Scenario A:** A red light shaped like an oil can appears while driving on the highway.

**Scenario B:** A yellow light shaped like a circle with "ABS" inside it appears while braking to a stop.

**Scenario C:** A yellow outline of an engine appears on your commute to work.

### Requirements
- [ ] Correct identification of each light's meaning
- [ ] Correct urgency classification (critical / high / medium / low)
- [ ] Appropriate recommended action for each

### Hints
<details>
<summary>Hint 1</summary>

Color is your first guide: red = critical or high urgency. Yellow = medium or low.

</details>

<details>
<summary>Hint 2</summary>

Think about what each system does and what happens if it fails completely while driving.

</details>

### Expected Output / Acceptance Criteria

Full credit: all three scenarios correctly identified with appropriate actions.
Partial (1 pt): two of three correct.

### Solution
<details>
<summary>Show Solution</summary>

**Scenario A (Red oil can):** Oil pressure critically low. **CRITICAL urgency.** Pull over safely immediately and turn off the engine. Check oil level. Do not restart until the cause is identified. Driving even 1–2 minutes can destroy the engine.

**Scenario B (Yellow ABS):** ABS system fault. **Medium urgency.** Regular friction braking still works fully — the anti-lock system just won't activate in an emergency stop. Safe to drive to your destination. Schedule service within a week.

**Scenario C (Yellow engine outline):** Check-engine light / MIL. **Medium urgency.** A fault code has been stored by the ECM. Note any symptoms (rough idle, strange smell, power loss). Drive normally if no other symptoms. Scan with OBD-II reader within a week.

</details>

---

## Exercise 4: Fluid Location and Identification [🟡 Medium] [2 pts]

### Context
You are asked to perform a fluid check on a vehicle you've never worked on before. You need to locate and identify the correct check points for each fluid.

### Task
For each of the following fluids, describe: (a) where to find the check point, (b) what the normal level indication looks like, and (c) one warning sign of contamination or a problem.

Fluids: Engine oil, Coolant, Brake fluid

### Requirements
- [ ] Correct check location for all three
- [ ] Correct description of how to read the level for all three
- [ ] At least one valid contamination warning sign for each

### Hints
<details>
<summary>Hint 1</summary>

Two of these three are checked via reservoir visual inspection; one requires a dipstick.

</details>

### Expected Output / Acceptance Criteria

```
Three fluids, each with location, level check method, and contamination warning sign.
Full credit: all correct. Partial (1 pt): two of three complete.
```

### Solution
<details>
<summary>Show Solution</summary>

**Engine oil:**
- Location: Oil dipstick, typically a brightly-colored handle near the engine
- Level check: Pull dipstick, wipe clean, reinsert fully, pull again — read between MIN and MAX marks
- Contamination warning: Milky or frothy oil (coolant contamination) = stop driving immediately; gritty texture = very overdue for change

**Coolant:**
- Location: Translucent overflow/reservoir tank near the radiator; has MIN and MAX lines
- Level check: Visual inspection of reservoir level (never open radiator cap on hot engine)
- Contamination warning: Brown/rusty color = corrosion; oily film on top = oil contamination (possible head gasket leak)

**Brake fluid:**
- Location: Master cylinder reservoir, typically on the firewall driver's side under the hood
- Level check: Visual inspection through semi-transparent reservoir or remove cap to check
- Contamination warning: Dark brown/black color = water saturation, boiling point reduced; very low level with new pads = potential brake leak

</details>

---

## Exercise 5: Pre-Drive Safety Inspection Scenario [🔴 Hard] [3 pts]

### Context
You've just acquired a used car and are preparing to drive it for the first time. You know nothing about its service history. Before driving, you want to perform a 10-minute safety check to identify any obvious issues that could make the drive dangerous.

This is a multi-step problem — you need to prioritize and sequence your checks intelligently.

### Task
Design a 10-minute pre-drive inspection procedure for an unknown used vehicle. List all checks in the order you would perform them, explain why each check matters from a safety perspective, and specify what result would cause you to refuse to drive the car until it was corrected.

### Requirements
- [ ] At least 8 distinct checks included
- [ ] Checks prioritized in a logical order (most safety-critical first)
- [ ] Safety consequence explained for each check
- [ ] Clear pass/fail criteria defined for each check
- [ ] The procedure is realistic and completable in approximately 10 minutes

### Hints
<details>
<summary>Hint 1 (structural hint — try designing without this first)</summary>

Think about what could cause you to lose control, stop ability, or visibility. Start with those.

</details>

<details>
<summary>Hint 2 (conceptual hint)</summary>

Divide checks into: under-hood (fluids, belts), exterior (tires, lights, body), and interior (controls, dashboard).

</details>

<details>
<summary>Hint 3 (near-solution hint — only if truly stuck)</summary>

Start with brakes (can you stop?), then tires (are you in contact with the road?), then fluids (will it overheat or lose oil pressure?), then lights (can others see you and can you see?).

</details>

### Expected Output / Acceptance Criteria

A written procedure with 8+ checks, each with safety rationale and pass/fail criteria. Evaluation based on safety focus, logical ordering, and realistic detail.

### Solution
<details>
<summary>Show Solution</summary>

**10-Minute Pre-Drive Safety Inspection:**

**Under Hood (3 minutes):**
1. **Engine oil** — Check level and color. FAIL: Below MIN or milky appearance. Why: Low/no oil = engine destruction in minutes.
2. **Coolant level** — Check reservoir. FAIL: Below MIN. Why: Overheating destroys engines rapidly.
3. **Brake fluid** — Check level. FAIL: Below MIN. Why: Low brake fluid may indicate a leak, which means total brake failure is possible.
4. **Serpentine belt** — Quick visual. FAIL: Cracks, fraying, or shredded appearance. Why: Belt break = loss of power steering, alternator charging, possibly water pump (overheating).

**Exterior (4 minutes):**
5. **All four tires** — Visual inspection for obvious damage, sidewall bulges, severe wear, or near-flat appearance. FAIL: Sidewall bulge or nearly flat. Why: Tire failure at speed = loss of control.
6. **All exterior lights** — Have someone confirm headlights (low+high), taillights, both brake lights, and both turn signals. FAIL: Any brake light non-functional. Why: Rear-end collision risk.
7. **Windshield** — Check for cracks in driver's sight lines. FAIL: Large crack in direct sightline. Why: Visibility and structural integrity (windshield braces the roof in a rollover).

**Interior (3 minutes):**
8. **Dashboard warning lights** — Start engine, observe which lights stay on after startup. FAIL: Red oil pressure or red temperature stays on. Why: These indicate immediate mechanical hazard.
9. **Brakes** — Before moving, press brake pedal firmly. FAIL: Spongy, sinks to floor, or very low pedal height. Why: Indicates air in lines or leak — brakes may not work.
10. **Steering** — Turn wheel slightly left and right. FAIL: Excessive play (more than 1–2 inches of wheel movement before tires respond). Why: Loose steering = poor control at speed.

**Any FAIL item = do not drive until resolved or further inspected.**

</details>

---

## Scoring Log

_Record your performance honestly. Include the date and whether you used hints._

| Exercise | Date | Score | Used Hints? | Notes |
|----------|------|-------|-------------|-------|
| Exercise 1 | — | —/1 | — | — |
| Exercise 2 | — | —/1 | — | — |
| Exercise 3 | — | —/2 | — | — |
| Exercise 4 | — | —/2 | — | — |
| Exercise 5 | — | —/3 | — | — |
| **Total** | | **—/9** | | |

**Passing threshold:** 6/9 (67%). Aim for 8/9 (89%) before taking the test.
