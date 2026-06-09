# Module 05: Engine Fundamentals

[← Module 04: Battery and Electrical](../04_battery-and-electrical/) | [Topic Home](../../README.md) | [Next → Module 06: Suspension and Steering](../06_suspension-and-steering/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-intermediate-yellow)
![Time](https://img.shields.io/badge/time-5h-orange)

> Deep dive into engine architecture: timing systems (belt vs. chain), cooling system components, variable valve timing, and the early warning signs of common engine failures.

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
> **This module is a stub.** Full content is planned for a future expansion.

Module 01 introduced the four-stroke cycle. This module goes deeper into engine architecture: the timing system that synchronizes camshafts to crankshaft, the cooling system that prevents overheating, and the failure modes that end engines prematurely. The timing belt is one of the highest-stakes maintenance items in automotive ownership — understanding why transforms it from an abstract service item into a maintenance item you'll never skip.

**Difficulty:** Intermediate &nbsp;|&nbsp; **Estimated time:** 5 hours

---

## Prerequisites

- [[cars-maintenance/modules/01_introduction]] — four-stroke cycle, engine overview
- [[cars-maintenance/modules/02_fluids-and-filters]] — oil and coolant systems

---

## Objectives

By the end of this module, you will be able to:

1. Explain the difference between a timing belt and a timing chain — how each works and why it matters
2. Describe the consequences of timing belt failure in interference vs. non-interference engines
3. Locate your vehicle's timing system type and service interval in the owner's manual
4. Explain the cooling system components: thermostat, water pump, radiator, coolant passages, cooling fans
5. Describe Variable Valve Timing (VVT) and why it requires the correct oil viscosity
6. Identify 5 early warning signs of common engine failures: head gasket, rod bearing, oil pump, coolant pump, and piston ring issues
7. Explain what a compression test measures and what low compression indicates

---

## Theory

### Timing Belt vs. Timing Chain

The camshaft must rotate at exactly half the crankshaft speed (one cam revolution per two crank revolutions) in perfect synchronization. Two mechanisms accomplish this: timing belts (rubber, quiet, requires scheduled replacement) and timing chains (metal, self-lubricating in engine oil, intended to last engine life but still can stretch and jump teeth).

**Interference vs. Non-Interference Engines:**

A critical distinction. In an interference engine, the valves extend far enough into the cylinder that at certain positions they occupy the same space a piston would during its travel. Timing synchronization prevents them from meeting. When that synchronization fails (belt breaks, chain jumps):
- **Interference engine**: Piston strikes open valve. Valve bends or breaks. Piston may crack. Engine is typically destroyed or requires very expensive rebuilding (often $3,000–8,000+ in parts and labor).
- **Non-interference engine**: Belt or chain fails → engine stops → car is stranded → tow to shop → belt/chain replaced → engine is fine. A $600 repair instead of an engine replacement.

Checking your engine type: consult the service manual or gates.com belt lookup tool. If your engine is interference-design and has a timing belt, the service interval (often 60,000–105,000 miles) is not optional.

### Cooling System Components

Thermostat, water pump, radiator, upper/lower radiator hoses, coolant reservoir, electric cooling fans (and fan temperature sensors). How each component fails and the symptoms. Water pump bearing failure (weeping from the weep hole, grinding noise). Thermostat stuck open (engine runs cold, poor heater performance) vs. stuck closed (engine overheats rapidly).

### Variable Valve Timing (VVT)

Modern engines use oil pressure to advance or retard camshaft position based on RPM and load, improving fuel economy and power. The VVT actuator (camshaft phaser) is controlled hydraulically using engine oil. This is why oil viscosity matters: using oil that is too thick can cause sluggish phaser response, generating fault codes (P0010, P0014, etc.) and causing rough idle. Low oil level or dirty oil with degraded viscosity can cause phaser rattle on cold start.

### Common Engine Failure Signs

| Symptom | Likely Cause | Urgency |
|---------|-------------|---------|
| Milky oil (Module 02 introduced this) | Head gasket failure | Stop driving |
| White smoke from exhaust (sweet smell) | Coolant burning in combustion | Stop driving |
| Blue smoke from exhaust (oil burning) | Piston rings or valve stem seals | Monitor/service soon |
| Knocking or tapping at idle | Low oil, rod bearing wear, or VVT phaser | Stop or reduce load |
| Rattling on cold start (disappears in seconds) | VVT phaser or timing chain tensioner | Service soon |
| Persistent ticking (oil pressure dependent) | Hydraulic lifter or valve lash | Service |
| High oil consumption (> 1 qt per 1,000 miles) | Piston rings or valve stem seals | Monitor/service |

---

## Key Concepts

- **Interference engine**: Engine where piston and valve paths overlap — timing failure causes catastrophic damage
- **Timing belt interval**: Service interval specified in owner's manual — missing it risks engine destruction
- **Thermostat**: Wax pellet valve that opens at operating temperature to allow coolant to flow to the radiator
- **Water pump**: Centrifugal pump driven by timing belt or serpentine belt; circulates coolant through engine
- **Compression test**: Test using a pressure gauge screwed into the spark plug hole; low or uneven readings indicate worn rings, bad valves, or head gasket issues
- **VVT (Variable Valve Timing)**: Oil-pressure-controlled camshaft phasing for improved efficiency and power

---

## Examples

_To be fully written in complete module expansion:_

- How to look up whether your specific engine is interference or non-interference
- Interpreting a compression test result: what 150 PSI vs. 80 PSI across cylinders means
- Recognizing head gasket failure from external symptoms before pulling the engine

---

## Common Pitfalls

- Not knowing your engine's timing belt interval and missing it
- Assuming "it's a timing chain — I don't need to worry" — chains can and do stretch and jump teeth, especially in oil-starved conditions
- Ignoring a cold-start chain rattle — it indicates a worn tensioner or chain stretch that will worsen
- Using the wrong viscosity oil in a VVT engine, causing phaser codes and rattle
- Driving after a head gasket failure — coolant in the combustion chamber causes hydrolock (incompressible liquid in cylinder destroys connecting rod)

---

## Cross-Links

- [[cars-maintenance/modules/01_introduction]] — four-stroke cycle foundational to all engine concepts here
- [[cars-maintenance/modules/02_fluids-and-filters]] — oil and coolant directly affect all systems covered in this module
- [[cars-maintenance/modules/07_diagnostics-and-obd2]] — VVT fault codes (P0010/P0014/P0020), misfire codes (P0300+), and coolant temperature sensor faults all require Module 07 skills to diagnose
- [[cars-maintenance/modules/08_diy-repairs]] — spark plug replacement procedure builds on engine anatomy covered here

---

## Summary

- Timing belt (rubber, scheduled replacement) vs. timing chain (metal, oil-lubricated, longer life but not infinite)
- Interference engines: timing failure causes valve-to-piston collision and engine destruction; non-interference engines: timing failure causes a stall
- Cooling system: thermostat regulates temperature; water pump circulates coolant; radiator dissipates heat
- VVT requires correct oil viscosity; wrong oil causes phaser faults, cold-start rattle, and rough idle
- Early warning signs save engines: white smoke (coolant), blue smoke (oil), milky oil (head gasket), cold-start rattle (chain/phaser) — all require prompt attention
