# Module 04: Battery and Electrical Systems

[← Module 03: Tires and Brakes](../03_tires-and-brakes/) | [Topic Home](../../README.md) | [Next → Module 05: Engine Fundamentals](../05_engine-fundamentals/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-beginner-green)
![Time](https://img.shields.io/badge/time-3h-orange)

> The 12-volt electrical system powers every component in your car. Learn to test it, maintain it, safely jump-start a dead battery, and diagnose fuse and relay problems.

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

The 12-volt lead-acid battery is the heart of every conventional vehicle's electrical system. It starts the engine, powers electronics when the engine is off, and absorbs voltage spikes in the charging circuit. The alternator — driven by the serpentine belt — takes over while the engine runs, charging the battery and supplying all electrical loads. Understanding this system lets you test battery health, identify charging faults, safely jump-start any vehicle, and diagnose simple electrical problems without a mechanic.

**Difficulty:** Beginner &nbsp;|&nbsp; **Estimated time:** 3 hours

---

## Prerequisites

- [[cars-maintenance/modules/01_introduction]] — vehicle systems overview, battery location, serpentine belt
- [[cars-maintenance/modules/02_fluids-and-filters]] — no direct dependency, but Module 02 is listed as prerequisite in the sequence

---

## Objectives

By the end of this module, you will be able to:

1. Test battery voltage with a multimeter and interpret healthy vs. weak vs. dead readings
2. Identify the signs of a failing battery vs. a failing alternator
3. Jump-start a vehicle safely: correct cable sequence, safety precautions, modern vehicle considerations
4. Test alternator output voltage and identify a charging system problem
5. Locate and interpret a vehicle's fuse box; identify a blown fuse; replace it correctly
6. Explain what a relay does and how to test it
7. Describe how corrosion affects battery terminal connections and how to clean them

---

## Theory

### The 12-Volt System Architecture

Battery chemistry (lead-acid: 6 cells × 2V = 12.6V fully charged). CCA (Cold Cranking Amps) and RC (Reserve Capacity) ratings. How the battery, alternator, and voltage regulator interact. Why you can't charge a dead battery by idling (insufficient alternator output at idle to overcome charging losses).

### Battery Health Testing

Resting voltage test: healthy = 12.6V, dead = below 11.9V. Load test (battery puts out current while tested). How temperature affects battery capacity (cold weather reduces CCA significantly — why batteries fail in January). Battery age and the electrolyte sulfation process that causes permanent capacity loss.

### Alternator and Charging System

How an alternator works (rotating magnetic field induces AC current; rectified to DC). Normal charging voltage: 13.5–14.5V. Signs of alternator failure: battery light on, flickering lights, dimming at idle, electronics resetting. How to test alternator output with a multimeter. The voltage regulator's role.

### Jump-Starting Safely

Correct cable sequence: red to dead (+) → red to good (+) → black to good (−) → black to unpainted metal on dead car (not battery negative). Why the last connection goes to metal, not battery: prevents spark near hydrogen gas that batteries vent. Modern vehicle considerations: some require connecting cables to specific jump-start points; check owner's manual for vehicles with AGM or lithium batteries.

### Fuses and Relays

What fuses protect (specific circuits); where fuse boxes are located (under dash, under hood). How to read a fuse diagram. Identifying a blown fuse visually and with a test light. Relay function: a low-current switch that controls a high-current circuit. Testing a relay by substitution or with a multimeter.

---

## Key Concepts

- **CCA (Cold Cranking Amps)**: Battery's ability to deliver current at 0°F for 30 seconds; determines cold-start performance
- **Alternator**: AC generator driven by serpentine belt; converts mechanical energy to electrical energy; charges battery
- **Voltage regulator**: Controls alternator output to maintain 13.5–14.5V regardless of electrical load
- **AGM battery**: Absorbed Glass Mat — sealed, spill-proof variant; requires different charging profile; cannot be serviced
- **Parasitic drain**: Electrical current drawn from battery when vehicle is off; normal is under 50mA; excessive drain kills batteries overnight

---

## Examples

_To be fully written in complete module expansion:_

- Step-by-step multimeter test of battery and alternator
- Complete safe jump-start procedure with cable diagram
- Finding and testing a blown fuse using the fuse box diagram

---

## Common Pitfalls

- Connecting jump-start cables in wrong order (positive last or negative to battery negative) — can spark near battery hydrogen
- Jump-starting a modern vehicle without consulting the owner's manual — some EVs/hybrids have specific procedures
- Ignoring a battery that "charges up fine" but tests weak under load — a battery can recover to 12.6V but fail immediately under the starting load
- Over-tightening battery terminal clamps on AGM batteries (can crack the case)
- Assuming battery light = bad battery — it often means alternator or charging circuit failure, not the battery itself

---

## Cross-Links

- [[cars-maintenance/modules/01_introduction]] — battery and electrical system overview; serpentine belt and alternator context
- [[cars-maintenance/modules/07_diagnostics-and-obd2]] — electrical fault codes (B-codes) and network communication (U-codes) build on electrical system knowledge
- [[cars-maintenance/modules/10_electric-vehicles]] — EV high-voltage systems are entirely different from 12V systems; Module 10 addresses the differences and dangers
- [[cars-maintenance]] — CHEATSHEET.md battery voltage reference table

---

## Summary

- 12V lead-acid battery: stores energy for starting; alternator recharges during operation
- Battery health: test resting voltage and CCA; weak under load even if resting voltage is OK
- Alternator output: should be 13.5–14.5V with engine running; battery light indicates charging system fault
- Jump-starting: correct cable sequence prevents spark near hydrogen; modern vehicles may need specific procedures
- Fuses protect circuits; relays switch high-current loads; fuse box diagram is your guide
