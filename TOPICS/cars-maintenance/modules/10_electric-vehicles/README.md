# Module 10: Electric Vehicles

[← Module 09: Buying Used Cars](../09_buying-used-cars/) | [Topic Home](../../README.md) | [Next → Module 11: Road Trips and Emergencies](../11_road-trips-and-emergencies/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-red)
![Time](https://img.shields.io/badge/time-5h-orange)

> The complete guide to electric vehicle ownership: BEV vs. PHEV vs. HEV, battery chemistry, charging levels (Level 1/2/3, AC/DC), battery care best practices, regenerative braking, and range anxiety management.

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

The Tesla Roadster launched in 2008 proved battery-electric vehicles could be desirable. The Model S in 2012 made them aspirational. By the 2020s, EVs and hybrids represent a significant and rapidly growing portion of new vehicle sales worldwide. An automotive-literate person in 2026 needs to understand how these powertrains work, how they differ from ICE maintenance, and what battery care means in practice — including the practices that preserve battery longevity over a 10+ year ownership horizon.

**Difficulty:** Advanced &nbsp;|&nbsp; **Estimated time:** 5 hours

---

## Prerequisites

- [[cars-maintenance/modules/01_introduction]] through [[cars-maintenance/modules/04_battery-and-electrical]] — vehicle systems and electrical fundamentals
- [[cars-maintenance/modules/05_engine-fundamentals]] — useful for comparison, though EVs don't use ICE

---

## Objectives

By the end of this module, you will be able to:

1. Distinguish between BEV (Battery Electric Vehicle), PHEV (Plug-in Hybrid), and HEV (conventional Hybrid) — and explain the ownership implications of each
2. Explain lithium-ion battery chemistry at a conceptual level: why capacity degrades over time, what accelerates degradation
3. Describe the three charging levels: Level 1 (120V AC), Level 2 (240V AC), Level 3 / DC Fast Charge — and their use cases
4. Explain what regenerative braking is, how it affects the driving experience, and why it reduces brake wear dramatically
5. Describe best practices for EV battery care: charge limits, thermal management, fast charge frequency
6. Calculate real-world range using the WLTP/EPA estimate and applying real-world adjustment factors
7. Identify the maintenance tasks that are eliminated in EVs vs. those that remain

---

## Theory

### Powertrain Types Compared

**HEV (Hybrid Electric Vehicle)**: Combines ICE with electric motor + small battery. Cannot be plugged in. Battery charged by regenerative braking and engine. Examples: Toyota Prius, Honda Accord Hybrid. Maintenance similar to ICE but with longer brake life and some additional hybrid system components.

**PHEV (Plug-in Hybrid Electric Vehicle)**: Larger battery; can be charged via plug. Runs on electric-only up to a limited range (typically 20–80 km), then switches to hybrid ICE+electric mode. Examples: Toyota RAV4 Prime, Mitsubishi Outlander PHEV. Has both ICE maintenance requirements and EV charging requirements.

**BEV (Battery Electric Vehicle)**: No ICE. Runs entirely on stored electrical energy. Charged by plug only. Examples: Tesla Model 3, Nissan Leaf, Volkswagen ID.4, BYD Han. Dramatically reduced maintenance: no oil changes, no spark plugs, no exhaust system, no timing belt. Still requires: tire rotation, brake inspection (though pads last much longer due to regen), cabin air filter, 12V auxiliary battery (separate from traction battery).

### Lithium-Ion Battery Chemistry

Most EV traction batteries use lithium-ion chemistry with various cathode materials: NMC (Nickel Manganese Cobalt), NCA (Nickel Cobalt Aluminum), LFP (Lithium Iron Phosphate — increasingly common for its safety and longevity). Key concepts:
- **State of Charge (SoC)**: 0–100% represents the usable range. Cells are typically only used between 5–95% to protect longevity.
- **Capacity degradation**: Each charge-discharge cycle causes minor capacity loss due to electrolyte degradation and SEI (solid electrolyte interface) layer growth. Modern EVs typically retain 80–90% capacity after 150,000–200,000 km.
- **Degradation accelerants**: High heat (charging in hot weather, parking hot), consistently charging to 100%, frequent DC fast charging, deep discharges (consistently below 10%).

### Charging Levels

| Level | Voltage | Power | Use Case | Typical Add Range/Hour |
|-------|---------|-------|----------|----------------------|
| Level 1 | 120V AC (US) / 110–230V | 1.4–1.9 kW | Overnight at home; emergency | 8–15 km/h |
| Level 2 | 240V AC (US) / 400V (EU) | 7–22 kW | Home EVSE; workplace; commercial | 30–100 km/h |
| Level 3 (DCFC) | 300–900V DC | 50–350 kW | Public fast charging; highway travel | 200–500+ km/h |

AC charging: vehicle's onboard charger converts AC to DC. DC fast charging: bypasses onboard charger; DC goes directly to battery pack (subject to pack's acceptance rate). Charging curve: EVs accept maximum charge rate up to ~80% SoC, then taper to protect cells. Charging from 80–100% takes as long as 20–80%.

### Regenerative Braking

When lifting the accelerator, the electric motor runs as a generator, converting kinetic energy back into electrical energy stored in the battery. In one-pedal driving modes (common in Teslas, Nissan Leaf, etc.), the car can decelerate to a near-stop using regen alone, without touching the physical brakes. Implications: front brake pads on EVs can last 5–10 times longer than ICE vehicles. However, rear brakes may wear faster (regen is typically front-biased, leaving rear friction brakes as primary rear braking). Annual brake system inspection remains important even with low pad wear.

### Range Anxiety and Real-World Range

EPA/WLTP range estimates are conducted under standardized conditions. Real-world range is typically 20–30% less in cold weather, 10–15% less at highway speeds, and significantly affected by HVAC use (heat in cold climates is particularly costly — resistive heating is inefficient; heat pump systems reduce this penalty). Planning tools: PlugShare (charging network map), ABRP (A Better Route Planner) for EV-specific trip planning with charging stops.

---

## Key Concepts

- **BEV**: Battery-only EV; no combustion engine; lowest maintenance of any vehicle type
- **PHEV**: Plug-in hybrid; has both ICE and battery; allows some EV-only operation
- **SoC (State of Charge)**: Battery charge level 0–100%; optimal daily range is typically 20–80%
- **LFP vs. NMC battery chemistry**: LFP (lithium iron phosphate) is safer, more cycle-stable, charges to 100% more routinely; NMC has higher energy density but degrades faster if routinely charged to 100%
- **Level 2 charging**: The standard home charging setup; 240V AC, installed EVSE unit; $400–1,500 installed
- **Thermal management**: Battery pack temperature control using liquid cooling or heating; essential for cold-weather performance and long-term pack health

---

## Examples

_To be fully written in complete module expansion:_

- Calculating the real-world range of a specific EV model for a highway trip in winter
- Understanding an EV's charging curve: why charging to 80% is often the recommended daily limit
- Comparing 10-year maintenance costs: BEV vs. equivalent ICE vehicle

---

## Common Pitfalls

- Charging LFP battery chemistry to only 80% (LFP is designed to charge to 100% regularly; capacity loss from this is minimal and offset by balanced cells)
- DC fast charging before understanding the vehicle's own guidance — some packs degrade faster with frequent DCFC; manufacturer guidance varies
- Ignoring the 12V auxiliary battery in an EV — it still exists and still dies, leaving the car "dead" even with a full traction pack
- Not accounting for heating in cold climates when planning range — resistive heat can use 30–40% of the energy budget at -10°C
- Assuming all EVs are plug-and-charge compatible with any charger — CHAdeMO, CCS1, CCS2, and Tesla (NACS) standards exist and are not interchangeable without adapters

---

## Cross-Links

- [[cars-maintenance/modules/04_battery-and-electrical]] — 12V system knowledge applies to the auxiliary battery in EVs; high-voltage system is entirely separate and should only be serviced by qualified technicians
- [[cars-maintenance/modules/03_tires-and-brakes]] — regenerative braking extends pad life but brakes still need annual inspection
- [[cars-maintenance/modules/07_diagnostics-and-obd2]] — EVs have OBD-II ports; additional proprietary diagnostic tools needed for BMS (Battery Management System) access
- [[cars-maintenance/modules/09_buying-used-cars]] — used EV inspection adds battery state-of-health (SoH) assessment to the checklist

---

## Summary

- BEV: no ICE; lowest maintenance; charges via plug only. PHEV: ICE + larger battery; plug-in capable. HEV: ICE + small battery; no plug.
- Lithium-ion degradation accelerated by: high heat, consistent 100% charging (NMC chemistry), frequent DC fast charging, deep discharge. Mitigate to maximize pack life.
- Charging levels: L1 (~10 km/h) for emergency; L2 (~50 km/h) for home and work; L3 DCFC (~300 km/h) for highway stops
- Regenerative braking: motor becomes generator on deceleration; recovers energy; extends brake life dramatically
- Real-world range is 20–30% below EPA/WLTP in cold weather; plan trips with charging buffer
