# Cars, Maintenance and Automotive Knowledge — Cheat Sheet

> [!TIP]
> This cheat sheet is a reference for **after you've learned the material** — not a shortcut
> to avoid learning it. If you're looking something up here before truly understanding it,
> go back to the relevant module first. A cheat sheet only helps people who already know
> what they're looking for.

---

## Quick Navigation

- [Maintenance Intervals](#maintenance-intervals)
- [Fluid Identification Guide](#fluid-identification-guide)
- [Common OBD-II Codes](#common-obd-ii-codes)
- [Warning Light Reference](#warning-light-reference)
- [Tire Size Decoder](#tire-size-decoder)
- [Battery Voltage Reference](#battery-voltage-reference)
- [Brake Inspection Thresholds](#brake-inspection-thresholds)
- [Pre-Trip Checklist](#pre-trip-checklist)
- [Emergency Procedures](#emergency-procedures)
- [Tool Reference](#tool-reference)

---

## Maintenance Intervals

_These are general guidelines. Always check your owner's manual for your specific vehicle._

| Service | Typical Interval | Notes |
|---------|-----------------|-------|
| Engine oil change (conventional) | 3,000–5,000 miles or 3–6 months | Older interval; rarely needed for modern engines |
| Engine oil change (synthetic) | 7,500–15,000 miles or 1 year | Check owner's manual — many modern cars spec 10k+ miles |
| Engine air filter | 15,000–30,000 miles | More often if driving dusty roads |
| Cabin air filter | 15,000–25,000 miles | Easy DIY; often forgotten |
| Tire rotation | Every 5,000–7,500 miles | Can be done at every other oil change |
| Tire pressure check | Monthly | Temperature changes pressure ~1 PSI per 10°F change |
| Brake pad inspection | Every 20,000 miles or annually | Replace when < 3mm friction material remains |
| Coolant flush | Every 2 years (green/IAT) or 5 years (orange/OAT) | Check coolant type and color |
| Transmission fluid | 30,000–60,000 miles (manual) / 60,000–100,000 miles (auto) | Many "lifetime" fluids still benefit from changes |
| Spark plugs (copper) | 30,000 miles | Check gap at each change |
| Spark plugs (iridium/platinum) | 60,000–100,000 miles | Don't clean — replace |
| Serpentine belt | 60,000–100,000 miles | Inspect annually for cracking/glazing |
| Timing belt | 60,000–105,000 miles | **Critical** — check your specific vehicle! |
| Battery | Test every 2 years; replace every 3–5 years | Hot climates shorten battery life |
| Brake fluid | Every 2 years or 45,000 miles | Absorbs moisture over time; lowers boiling point |
| Power steering fluid | 50,000–100,000 miles | Less critical in electric power steering systems |

---

## Fluid Identification Guide

| Fluid | Normal Color | Where It Drips / Leaks | Smell/Texture |
|-------|-------------|----------------------|---------------|
| Engine oil | Amber/brown (new), dark brown/black (used) | Under engine; oily stain | Petroleum smell; slippery |
| Coolant | Green, orange, pink, or blue | Under front of engine; sweet smell | Sweet/syrupy smell; slimy feel |
| Brake fluid | Clear to light yellow | Near wheel wells; brake master cylinder | Sharp, almost alcohol-like |
| Transmission fluid | Red/pink (new ATF), dark red/brown (old) | Under center/middle of car | Slightly sweet petroleum smell |
| Power steering fluid | Red or clear | Near front wheels; steering column area | Similar to ATF |
| Differential/gear oil | Dark brown/black | Rear of car (RWD/4WD); very thick | Sulfur/rotten egg smell when hot |
| Windshield washer | Blue, purple, pink | Rare leak; usually a hose | Soapy/alcohol smell; very thin |
| Water condensation | Clear water | Under rear of car (AC drainage) | None; odorless |

> [!WARNING]
> Green or orange puddles under the front of the car that smell sweet are coolant — a significant leak needs immediate attention. Driving with low coolant causes rapid engine overheating and can destroy the engine in minutes.

---

## Common OBD-II Codes

_The most frequently encountered codes and their most common causes. Always verify with a full diagnosis._

| Code | Description | Most Common Causes |
|------|-------------|-------------------|
| P0171 | System Too Lean (Bank 1) | Vacuum leak, MAF sensor, fuel pressure low, O2 sensor |
| P0300 | Random/Multiple Cylinder Misfire | Spark plugs, ignition coils, fuel injectors, compression |
| P0301–P0308 | Cylinder N Misfire | Spark plug/coil on that cylinder, injector, compression |
| P0420 | Catalyst System Efficiency Below Threshold | Failing catalytic converter, exhaust leak, O2 sensor |
| P0440 | Evaporative Emission System (EVAP) Leak | Loose gas cap (most common!), EVAP hoses, purge valve |
| P0455 | EVAP System Large Leak | Loose or missing gas cap; check cap first |
| P0505 | Idle Control System Malfunction | IAC valve dirty/failed, vacuum leak |
| P0700 | Transmission Control System Malfunction | Check with transmission-specific scan; may need shop |
| P0715 | Input/Turbine Speed Sensor Circuit | Transmission sensor; often needs dealer diagnosis |
| P0010/P0020 | Camshaft Position Actuator | VVT system; often low oil or oil quality issue |

**DTC Code Structure:**
- First letter: **P** = Powertrain, **C** = Chassis, **B** = Body, **U** = Network/Communication
- Second digit: **0** = Generic (SAE standard), **1** = Manufacturer-specific
- Digits 3–4: System (01=fuel/air, 03=ignition, 04=emissions, 07=transmission)
- Digits 5–6: Specific fault number

---

## Warning Light Reference

| Light / Symbol | Color | Urgency | Meaning | Action |
|----------------|-------|---------|---------|--------|
| Engine (check engine / MIL) | Yellow/orange | Medium | ECM has stored a fault code | Scan with OBD-II; drive normally if no other symptoms |
| Oil pressure | Red | CRITICAL | Oil pressure critically low | **Stop engine immediately** — driving will destroy engine |
| Temperature | Red | CRITICAL | Engine overheating | Pull over safely, turn off engine; do not open radiator |
| Battery | Red | High | Charging system failure | Reduce electrical load; drive to destination or safe stop |
| Brake | Red | High | Parking brake on OR brake fluid low | Check parking brake; check brake fluid level |
| TPMS (tire) | Yellow | Medium | Tire pressure low (or sensor fault) | Check all tire pressures; adjust to door-jamb spec |
| ABS | Yellow | Medium | ABS system fault | Regular brakes still work; ABS won't activate |
| Airbag / SRS | Yellow | Medium | Airbag system fault | Airbags may not deploy in crash; service soon |
| Traction/Stability | Yellow (blinking) | Informational | System actively intervening | Normal; steady light = system disabled or faulty |
| Fuel | Yellow | Low | Low fuel | Refuel soon; reserve varies by vehicle |

> [!IMPORTANT]
> Red warning lights always require immediate action or immediate safe stop. Yellow lights mean service soon. Never ignore a red oil pressure or temperature light while the engine is running.

---

## Tire Size Decoder

```
Example: 205/55R16 91H

205  = Section width in millimeters (tread width)
 55  = Aspect ratio — sidewall height as % of width (55% × 205 = 113 mm sidewall)
  R  = Radial construction (almost universal on modern cars)
 16  = Wheel/rim diameter in inches
 91  = Load index (91 = 615 kg / 1356 lb max load per tire)
  H  = Speed rating (H = 130 mph / 210 km/h max)
```

**Common Speed Ratings:**
| Letter | Max Speed |
|--------|-----------|
| S | 180 km/h (112 mph) |
| T | 190 km/h (118 mph) |
| H | 210 km/h (130 mph) |
| V | 240 km/h (149 mph) |
| W | 270 km/h (168 mph) |

---

## Battery Voltage Reference

| Condition | Voltage | Meaning |
|-----------|---------|---------|
| Fully charged (resting) | 12.6–12.7 V | Healthy |
| 75% charged (resting) | 12.4 V | Acceptable |
| 50% charged (resting) | 12.2 V | Weak; charge soon |
| 25% charged (resting) | 12.0 V | Nearly depleted |
| Dead (resting) | < 11.9 V | Replace or charge |
| Engine running (alternator output) | 13.5–14.5 V | Healthy alternator |
| Engine running (low) | < 13.0 V | Failing alternator |
| Engine running (high) | > 14.8 V | Voltage regulator fault |

---

## Brake Inspection Thresholds

| Measurement | Threshold | Action |
|-------------|-----------|--------|
| Brake pad friction material thickness | 3 mm (1/8 inch) | Replace if at or below |
| Rotor lateral runout | > 0.001 inch | Replace rotor |
| Rotor thickness (check manufacturer spec) | Below minimum | Replace; do not resurface |
| Brake fluid color | Dark brown/black | Flush; water contamination |
| Brake fluid moisture content | > 3.5% water | Flush |

---

## Pre-Trip Checklist

_Complete before any trip over 200 miles or before driving in extreme weather._

- [ ] Engine oil level — check dipstick; top up if needed
- [ ] Coolant level — visible in reservoir; add if low (correct type!)
- [ ] Brake fluid level — in reservoir behind master cylinder
- [ ] Tire pressure — all four tires + spare; adjust to door-jamb specification
- [ ] Tire condition — no visible damage, embedded objects, or low tread
- [ ] Lights — headlights, taillights, brake lights, turn signals all functional
- [ ] Windshield wipers — streak-free; replace if worn
- [ ] Washer fluid — full
- [ ] Battery — no corrosion on terminals; secure
- [ ] Belts — no visible cracks or fraying on serpentine belt
- [ ] Brakes — pedal firm and not spongy; no grinding or squealing on test application
- [ ] Emergency kit present (see Module 11)

---

## Emergency Procedures

### Engine Overheating

```
Temperature gauge in red → Pull over immediately
Engine off → Wait 20–30 minutes (never open a hot radiator cap)
Check coolant reservoir level (cold only)
If low → add coolant or water as temporary measure
If hoses collapsed or steam visible → call for tow
```

### Dead Battery / Jump Start

```
Position cars (do not let them touch)
Red cable → dead battery (+) → good battery (+)
Black cable → good battery (-) → unpainted metal on dead car (NOT battery -)
Start working car → wait 2 minutes → start dead car
Remove in reverse order: black from metal → black from good → red from good → red from charged
```

### Flat Tire

```
Gradually reduce speed → hazard lights on
Steer to safe, flat location → park away from traffic
Chock wheels if available
Loosen lug nuts BEFORE jacking (use body weight)
Place jack at manufacturer-specified jack point
Raise car until flat tire 6 inches off ground
Remove lug nuts and wheel → mount spare
Hand-tighten lug nuts in star pattern → lower car → torque to 80–120 ft-lb (confirm for your car)
Maximum speed on spare: 50 mph (80 km/h) for donut spare; full-size spare = normal
```

---

## Tool Reference

| Tool | Use | Minimum Quality |
|------|-----|----------------|
| OBD-II Bluetooth scanner | Read fault codes | Any ELM327-compatible ($20+) |
| Socket set (metric + SAE) | General fasteners | 1/4" and 3/8" drive set |
| Torque wrench | Fasteners requiring precision | 3/8" drive, 10–150 ft-lb range |
| Floor jack | Lifting vehicle | 2-ton minimum; 3-ton preferred |
| Jack stands (pair) | Supporting lifted vehicle | NEVER use only a jack |
| Multimeter | Electrical diagnosis | Any digital multimeter ($15+) |
| Tire pressure gauge | Checking tire pressure | Dial or digital |
| Brake bleeding kit | Brake fluid flush | Hand-pump bleeder kit |
| Oil filter wrench | Removing tight filters | Match to your filter size |
| Feeler gauge set | Spark plug gapping, clearances | 0.001"–0.025" range |

---

## Module Cross-References

| If you need to recall... | See module |
|--------------------------|-----------|
| How to check all fluids | [[cars-maintenance/modules/01_introduction]] |
| Oil types and oil change procedure | [[cars-maintenance/modules/02_fluids-and-filters]] |
| Tire sizing, pressure, brake inspection | [[cars-maintenance/modules/03_tires-and-brakes]] |
| Battery testing and jump starting | [[cars-maintenance/modules/04_battery-and-electrical]] |
| Timing belt and engine failure signs | [[cars-maintenance/modules/05_engine-fundamentals]] |
| Shock/strut diagnosis and alignment | [[cars-maintenance/modules/06_suspension-and-steering]] |
| OBD-II scanning and DTC interpretation | [[cars-maintenance/modules/07_diagnostics-and-obd2]] |
| Step-by-step repair procedures | [[cars-maintenance/modules/08_diy-repairs]] |
| Pre-purchase inspection checklist | [[cars-maintenance/modules/09_buying-used-cars]] |
| EV charging levels and battery care | [[cars-maintenance/modules/10_electric-vehicles]] |
| Emergency procedures and pre-trip | [[cars-maintenance/modules/11_road-trips-and-emergencies]] |

---

_Last updated: 2026-06-09_
