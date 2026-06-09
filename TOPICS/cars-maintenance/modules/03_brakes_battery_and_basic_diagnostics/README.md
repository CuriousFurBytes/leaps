# Module 03: Brakes, Battery, and Basic Diagnostics

> Learn warning signs, basic electrical checks, brake safety symptoms, and disciplined first-step diagnosis.

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

## Overview

This module moves from routine inspection into diagnosis. You will learn how brake symptoms, battery condition, dashboard warnings, and OBD-II codes fit into a careful troubleshooting process without guessing or replacing parts prematurely.

The central habit is controlled caution: inspect first, verify the source of information, use the correct tool, and avoid turning a small maintenance task into a safety problem. Cars differ by model year, trim, engine, drivetrain, tire package, and previous repair history, so this module teaches repeatable process rather than one-size-fits-all shortcuts.

> [!WARNING]
> If a task involves lifting the vehicle, brake hydraulics, fuel, airbags, high-voltage components, steering, suspension, or unclear procedures, pause and consult the factory service information or a qualified technician.

## Prerequisites

- Modules 01 and 02 in this topic.
- Ability to read an owner manual and follow step-by-step safety instructions.
- Basic household safety habits: stable work area, good lighting, ventilation, and no distractions.

## Objectives

By the end of this module, you will be able to:

- Explain the purpose of the systems covered in this module.
- Inspect common owner-serviceable items without creating avoidable risk.
- Choose the correct information source before acting.
- Document observations in a useful maintenance log.
- Decide when a finding requires professional diagnosis.

## Theory

### Maintenance Is Risk Management

Preventive maintenance exists because parts wear, fluids age, rubber hardens, corrosion spreads, and heat cycles loosen or fatigue components. A good owner does not replace parts randomly; they observe symptoms, check service intervals, measure condition, and record evidence. This approach came from the same reliability thinking used in aviation and fleet maintenance: small, documented checks reduce surprise failures.

A simple maintenance log can be kept in plain text:

```text
2026-06-09 | 45,210 miles | Checked tire pressure cold: LF 34, RF 34, LR 33, RR 34 psi | Adjusted LR to 34 psi | No visible sidewall damage
```

The important details are date, mileage, condition, action, and follow-up. A future technician can use this record to spot patterns.

### Use the Correct Information Hierarchy

The owner manual is the first source for routine checks. A factory service manual or professional database is the source for procedures, torque specifications, lift points, wiring, and diagnostic trees. Internet videos can help visualize a job, but they should not override specifications for your exact vehicle.

```bash
# Example owner workflow written as commands for a paper checklist, not vehicle software.
printf "1. Identify vehicle year/make/model/engine.\n"
printf "2. Read owner manual maintenance section.\n"
printf "3. Record mileage and symptoms before touching parts.\n"
printf "4. Stop if the procedure requires special tools or safety training.\n"
```

### Inspection Before Action

Inspection means looking for evidence before choosing a repair. Evidence includes fluid level, odor, color, tire wear pattern, warning light state, noise conditions, vibration speed, recent work, and environmental context. Replacing the most suspicious part without verification is called parts-cannon diagnosis and often wastes money.

```text
Symptom: Car pulls right while braking.
Evidence to collect: tire pressures, tire wear, road crown, brake noise, steering vibration, fluid level, recent wheel or brake work.
Unsafe threshold: strong pull, soft pedal, warning light, or grinding noise means stop driving and seek help.
```

## Key Concepts

- **Owner manual:** The vehicle-specific routine reference for fluids, tires, warnings, and maintenance intervals.
- **Service information:** Detailed repair procedures, diagrams, torque values, and diagnostic steps for trained work.
- **Torque specification:** The measured tightening requirement for a fastener; critical on wheels, brakes, suspension, and steering.
- **Wear item:** A part expected to degrade with use, such as tires, filters, wiper blades, belts, brake pads, and fluids.
- **Safety-critical system:** Any system whose failure can cause loss of control, fire, collision, or injury.

## Examples

### Example 1: Maintenance Note

Scenario: You notice a new squeak on startup.

```text
Date: 2026-06-09
Mileage: 82,114
Symptom: Brief squeak for 2 seconds after cold start.
Conditions: Outside temperature about 40 F, no dashboard warning lights.
Action: Recorded symptom; scheduled belt inspection before long trip.
```

This note separates observation from conclusion. It does not assume the belt is bad, but it preserves useful evidence.

### Example 2: Stop/Go Decision

Scenario: You find a nail in a tire tread.

```text
Go: Tire holds pressure, nail is in central tread area, no sidewall damage, slow leak only, drive carefully to tire shop.
Stop: Tire is flat, sidewall is damaged, cords are visible, puncture is near shoulder, or vehicle feels unstable.
```

The safe decision depends on location, pressure loss, and vehicle behavior, not just the presence of a nail.

## Common Pitfalls

### Pitfall 1: Working Under a Jack Alone

Wrong:

```text
Lift vehicle with scissor jack, crawl underneath, remove shield.
```

Correct:

```text
Use level ground, chock wheels, lift at approved point, place rated jack stands, lower onto stands, shake-test, then work.
```

A jack is a lifting tool, not a support structure.

### Pitfall 2: Trusting Generic Advice Over Specifications

Wrong:

```text
Use the pressure printed on the tire sidewall as the normal inflation target.
```

Correct:

```text
Use the vehicle placard on the driver door jamb unless the owner manual says otherwise for a specific load condition.
```

The sidewall usually lists maximum pressure, not the vehicle's recommended cold pressure.

### Pitfall 3: Replacing Parts Before Diagnosing

Wrong:

```text
Check-engine light is on, so replace the oxygen sensor immediately.
```

Correct:

```text
Read the code, record freeze-frame context, inspect related wiring and vacuum leaks, then follow a diagnostic path.
```

Codes identify a detected problem area, not an automatic parts order.

## Cross-Links

- [[cars-maintenance]]
- safety practices
- basic tools
- systems thinking

## Summary

- Safe maintenance starts with information, inspection, and risk control.
- Vehicle-specific instructions matter more than generic examples.
- Documentation makes patterns visible and improves shop communication.
- Safety-critical work requires correct tools, torque specifications, and judgment.
- Knowing when to stop is part of competence, not a failure.
