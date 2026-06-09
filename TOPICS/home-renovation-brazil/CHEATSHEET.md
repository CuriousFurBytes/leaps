# Home Renovation Brazil — Cheat Sheet

> [!TIP]
> This cheat sheet is a reference for **after you've learned the material** — not a shortcut
> to avoid learning it. If you're looking something up here before truly understanding it,
> go back to the relevant module first. A cheat sheet only helps people who already know
> what they're looking for.

---

## Quick Navigation

- [Material Quantity Formulas](#material-quantity-formulas)
- [Common Mix Ratios (Traços)](#common-mix-ratios-traços)
- [Electrical Quick Reference](#electrical-quick-reference)
- [Hydraulic Pipe Quick Reference](#hydraulic-pipe-quick-reference)
- [Tool List by Trade](#tool-list-by-trade)
- [Decision Guides](#decision-guides)
- [Conversion Tables](#conversion-tables)
- [Module Cross-References](#module-cross-references)

---

## Material Quantity Formulas

All formulas assume standard Brazilian materials and waste factors. Adjust waste factor
upward (to 15–20%) for complex layouts with many cuts.

### Floor and Wall Tiles (Cerâmica / Porcelanato)

```text
Area to tile (m²) = length (m) × width (m)

Tiles needed = Area ÷ tile area × (1 + waste factor)

Standard waste factor: 10% for simple layouts (0.10)
                       15% for diagonal or complex layouts (0.15)

Example:
  Room: 4.0 m × 3.5 m = 14.0 m²
  Tile: 60×60 cm (0.36 m² per tile)
  Tiles needed = 14.0 ÷ 0.36 × 1.10 = 42.8 → round up to 43 boxes if 1 tile/box
  (Most tiles come in boxes covering 1.5–2.5 m²; divide area by box coverage)
```

### Tile Adhesive Mortar (Argamassa Colante)

```text
Consumption = tile area (m²) × consumption rate (kg/m²)

Standard consumption rates:
  AC-I (dry areas, smooth substrate): 4–6 kg/m²
  AC-II (wet areas, standard use):    5–7 kg/m²
  AC-III (heavy-duty, large tiles):   6–9 kg/m²

Example:
  14.0 m² floor, using AC-II mortar at 6 kg/m²
  Mortar needed = 14.0 × 6 = 84 kg
  Bags needed = 84 ÷ 20 (standard bag size) = 4.2 → buy 5 bags
```

### Grout (Rejunte)

```text
Consumption (kg/m²) = (tile width + tile height) × joint width × tile thickness × grout density
                       ───────────────────────────────────────────────────────────────────────
                                    tile width × tile height × 1000

Simplified approximation for standard joints (3 mm):
  30×30 cm tile: ~0.5 kg/m²
  45×45 cm tile: ~0.4 kg/m²
  60×60 cm tile: ~0.3 kg/m²

Example:
  14.0 m² floor, 60×60 cm tiles, 3 mm joints
  Rejunte = 14.0 × 0.3 = 4.2 kg → buy 5 kg bag
```

### Paint Coverage

```text
Wall/ceiling area (m²) = perimeter × height (for walls)
                        = length × width (for ceiling)
Subtract door area: 2.1 × 0.9 = ~1.9 m² per door
Subtract window area: measured per window

Paint needed (litres) = area ÷ yield per litre × number of coats

Standard yields (manufacturer datasheets vary — always verify):
  PVA primer: 8–10 m²/litre
  PVA latex (interior): 10–12 m²/litre, 2 coats recommended
  Acrylic latex (interior): 10–12 m²/litre, 2 coats
  Acrylic (exterior): 8–10 m²/litre, 2 coats minimum

Example:
  Room: 4.0 × 3.5 m, ceiling height 2.7 m
  Wall area = (2 × 4.0 + 2 × 3.5) × 2.7 = 40.5 m²
  Subtract 1 door (1.9 m²) + 1 window (1.2 m²) = 37.4 m²
  Ceiling area = 14.0 m²
  Total = 51.4 m²
  Primer: 51.4 ÷ 9 = 5.7 L → buy 6 L
  PVA (2 coats): 51.4 ÷ 11 × 2 = 9.3 L → buy 10 L (standard 18 L bucket may be more economical)
```

### Mortar for Masonry (Assentamento de Blocos)

```text
Wall area (m²) = length × height (subtract openings)

Mortar consumption for 9 cm ceramic block walls: ~18–22 kg/m² of wall

Blocks needed (9×19×19 cm nominal):
  Blocks per m² ≈ 25 blocks (for 9 cm wall)
  Blocks per m² ≈ 13 blocks (for 14 cm wall)
  Add 5% waste factor

Example:
  5.0 m × 2.7 m wall = 13.5 m², subtract 1 door (1.9 m²) = 11.6 m²
  Blocks (9 cm): 11.6 × 25 × 1.05 = 304 blocks → buy 310 blocks
  Mortar: 11.6 × 20 = 232 kg → ~12 bags of 20 kg pre-mixed argamassa
```

### Chapisco, Emboço, and Reboco (Wall Plaster System)

```text
Chapisco: 4–6 kg/m² (thin coat, rough texture)
Emboço:   25–30 kg/m² for 20 mm thickness
Reboco:   10–15 kg/m² for 8 mm thickness

Cement content in a 1:3 traço emboço (cement:sand):
  1 bag cement (50 kg) + 3 × 50 kg sand = covers ~2.5 m² at 20 mm
```

---

## Common Mix Ratios (Traços)

Mix ratios (*traços*) in Brazil are given by volume (not weight) unless noted.
"1:3" means 1 part cement to 3 parts sand.

| Application | Traço (cement:lime:sand) | Notes |
|-------------|--------------------------|-------|
| Chapisco de aderência | 1:3 (cement:sand) | No lime; thin, rough consistency |
| Emboço (base coat) | 1:2:9 or 1:0.5:4.5 | With hydrated lime for workability |
| Reboco (finish coat) | 1:2:8 | Fine sand; smooth finish |
| Assentamento de blocos | 1:2:8 (with lime) | Workable, not too stiff |
| Contrapiso (floor screed) | 1:4 or 1:5 (cement:sand) | No lime; stiff mix |
| Concreto simples (non-structural) | 1:2:3 (cement:sand:stone) | fck ~15 MPa |
| Concreto estrutural (minimum residential) | 1:2:3 (C20) | fck 20 MPa; requires ART |

> [!WARNING]
> These are reference traços. Always follow the manufacturer's technical datasheet for
> industrialized (pre-mixed, *argamassa industrializada*) products — they override generic ratios.
> For structural concrete (*concreto estrutural*), always use a mix designed by a qualified engineer.

---

## Electrical Quick Reference

### Standard Brazilian Circuit Ratings (NBR 5410)

| Circuit Type | Typical Breaker | Conductor (mm²) | Notes |
|-------------|----------------|-----------------|-------|
| General lighting | 10–16 A | 1.5 or 2.5 mm² | Max 6 points per circuit |
| General sockets | 16–20 A | 2.5 mm² | Max 6 points per circuit |
| Kitchen/laundry dedicated | 20 A | 2.5 mm² | Refrigerator, microwave — each separate |
| Electric shower (*chuveiro*) | 25–40 A | 6 mm² | Dedicated circuit required |
| Air conditioning 9000–12000 BTU | 20 A | 2.5 mm² | Dedicated circuit |
| Air conditioning 18000+ BTU | 25–30 A | 4–6 mm² | Dedicated circuit |
| Main breaker (2-bed apartment) | 40–63 A | 10–16 mm² | Size per total load calculation |

### Load Calculation (Simple Method)

```text
Total load (W) = sum of all connected appliance wattages

Minimum circuit current (A) = total load (W) ÷ voltage (V)
  At 127 V: I = W ÷ 127
  At 220 V: I = W ÷ 220

Select breaker at next standard size above calculated minimum:
  Standard breaker sizes in Brazil: 6, 10, 16, 20, 25, 32, 40, 50, 63 A

Example:
  Kitchen circuit at 220 V: refrigerator (150W) + microwave (1200W) + blender (400W)
  Total = 1750 W
  I = 1750 ÷ 220 = 7.95 A → use 16 A breaker, 2.5 mm² conductor
```

---

## Hydraulic Pipe Quick Reference

### Pipe Materials and Applications

| Material | Color | Use | Pressure Rating | Notes |
|----------|-------|-----|-----------------|-------|
| PVC (rígido) | White | Cold water supply | 6 or 10 kgf/cm² | Most common; rigid |
| CPVC | Yellow/cream | Hot water supply | 10 kgf/cm² | Use above 40°C |
| PPR | Green/grey | Hot and cold supply | 10 or 20 kgf/cm² | Fusion welded; no solvents |
| PVC (esgoto) | Orange | Drainage/sewage | — (gravity) | Larger diameters; fittings differ from supply PVC |
| Copper | Copper color | High-end supply; gas | Varies | Expensive; required for gas in some specs |

### Common Drain Diameters (NBR 8160)

| Fixture | Minimum Drain Diameter |
|---------|----------------------|
| Shower (*chuveiro*) | 50 mm |
| Lavatory (*lavatório*) | 40 mm |
| Kitchen sink (*pia*) | 50 mm |
| Toilet (*vaso sanitário*) | 100 mm |
| Floor drain (*ralo*) | 50–100 mm |
| Main collector | 100 mm minimum |

---

## Tool List by Trade

### Basic Measurement and Layout Tools

| Tool | Portuguese Name | Use |
|------|----------------|-----|
| Tape measure | Trena | Measuring dimensions |
| Spirit level (1 m) | Nível de bolha | Checking level and plumb |
| Laser level | Nível a laser | Projecting level reference lines |
| Steel square | Esquadro | Checking 90° angles |
| Chalk line | Linha de giz / barbante de traçar | Marking straight reference lines |
| Plumb bob | Prumo de pedreiro | Checking vertical alignment |

### Masonry Tools

| Tool | Portuguese Name | Use |
|------|----------------|-----|
| Trowel (large) | Colher de pedreiro | Applying and spreading mortar |
| Notched trowel | Desempenadeira dentada | Applying tile adhesive |
| Rubber float | Desempenadeira de borracha | Applying grout |
| Float (sponge) | Desempenadeira de esponja | Finishing reboco surface |
| Straight-edge rule (2 m) | Régua de alumínio | Leveling mortar coats |
| Rubber mallet | Marreta de borracha | Tapping tiles into place |
| Tile spacers | Espaçadores para cerâmica | Maintaining consistent grout joints |

### Cutting Tools

| Tool | Portuguese Name | Use |
|------|----------------|-----|
| Angle grinder + diamond blade | Esmerilhadeira + disco diamantado | Cutting ceramic tiles, masonry |
| Tile cutter (manual) | Cortador de piso manual | Straight cuts on standard tiles |
| Jigsaw | Serra tico-tico | Curved cuts in wood, thin panels |
| Reciprocating saw | Serra sabre | Demolition cuts in mixed materials |
| Rotary hammer | Martelete | Drilling into concrete and masonry |

### Safety Equipment (PPE — EPI)

| Equipment | Portuguese Name | When Required |
|-----------|----------------|---------------|
| Safety glasses | Óculos de proteção | Always when cutting, grinding, or mixing |
| Dust mask (N95 or PFF2) | Máscara respiratória PFF2 | Sanding, cutting, applying dry mortars |
| Work gloves | Luvas de trabalho | Mixing mortar, handling sharp materials |
| Hearing protection | Protetor auricular | Angle grinder, hammer drill use |
| Safety boots (steel toe) | Botina de segurança | On any active construction site |
| Hard hat | Capacete | Overhead work, active construction sites |
| Knee pads | Joelheiras | Prolonged tile laying on floors |

---

## Decision Guides

### Choosing the Right Mortar for the Job

```text
What are you doing?
│
├── Bonding masonry units (blocks, bricks)?
│   └── Use argamassa de assentamento (1:2:8 with lime)
│
├── Applying a wall plaster base coat?
│   └── Use emboço mortar (1:2:9 or industrializado tipo A)
│
├── Applying a finish plaster coat?
│   └── Use reboco mortar (1:2:8 fine sand or gesso)
│
├── Setting floor or wall tiles?
│   ├── Dry area, smooth substrate → AC-I mortar
│   ├── Wet area (bathroom, kitchen) → AC-II mortar
│   └── Large format tiles (>60 cm) or swimming pool → AC-III mortar
│
└── Waterproofing before tiling?
    ├── Bathroom floor/walls → liquid impermeabilizante (2 coats)
    ├── Flat roof (laje) → asphalt sheet membrane or elastomeric coating
    └── Underground/water tank → crystalline or cementitious waterproofing
```

### Choosing Paint Type

```text
Interior or exterior?
│
├── Interior — dry areas (living room, bedroom)
│   └── PVA latex (econômico) or acrylic latex (better washability)
│
├── Interior — wet areas (bathroom, kitchen walls)
│   └── Semi-gloss or gloss enamel (esmalte) or acrylic with anti-fungal additive
│
├── Exterior — walls
│   └── Acrylic exterior (tinta acrílica para fachadas) — minimum 2 coats
│   └── Apply elastomeric (borracha acrílica) for crack-prone facades
│
└── Metal surfaces (gates, grilles, gutters)
    └── Metal primer + oil-based enamel (esmalte sintético)
```

---

## Conversion Tables

### Common Unit Conversions

| From | To | Multiply by |
|------|-----|------------|
| cm | mm | × 10 |
| m | cm | × 100 |
| m² | cm² | × 10,000 |
| kgf/cm² | MPa | × 0.0981 |
| MPa | kgf/cm² | × 10.2 |
| Litres | m³ | × 0.001 |
| Bags of 50 kg cement | 1 m³ mix | ~7–8 bags for 1:3 mortar |

### Standard Tile Sizes Available in Brazil

| Format | Common Application | Notes |
|--------|-------------------|-------|
| 20×20 cm | Bathrooms, pools | Traditional small format |
| 30×30 cm | Bathrooms, service areas | Standard residential |
| 45×45 cm | Kitchens, living rooms | Mid-format |
| 60×60 cm | Living rooms, commercial | Most popular format |
| 60×120 cm | Large spaces, modern look | Requires stiffer substrate |
| 80×80 cm | High-end residential | Heavy; requires good substrate |
| 10×100 cm (wood-look) | Living rooms | Porcelanato madeira |

### Cement Consumption per m³ of Mortar/Concrete

| Mix (cement:sand or cement:sand:stone) | Cement per m³ |
|----------------------------------------|--------------|
| 1:3 (mortar) | ~450 kg ≈ 9 bags of 50 kg |
| 1:4 (mortar) | ~360 kg ≈ 7 bags |
| 1:2:3 (concrete) | ~400 kg ≈ 8 bags |
| 1:2:4 (concrete) | ~320 kg ≈ 6 bags |

---

## Module Cross-References

| If you need to recall... | See module |
|--------------------------|-----------|
| Safety and PPE requirements | [[modules/01_introduction]] |
| How to get a building permit | [[modules/02_planning-and-permits]] |
| Whether a wall is structural | [[modules/03_foundations-and-structure]] |
| Circuit breaker sizing | [[modules/04_electrical-systems]] |
| Drain pipe sizing | [[modules/05_hydraulic-systems]] |
| Argamassa mixing ratios | [[modules/06_masonry-and-walls]] |
| Chapisco/emboço/reboco sequence | [[modules/07_wall-finishes]] |
| Tile adhesive selection | [[modules/08_flooring-and-tiling]] |
| Impermeabilização product selection | [[modules/09_painting-and-waterproofing]] |
| Roof slope requirements | [[modules/10_roofing]] |
| Solar connection rules (ANEEL) | [[modules/11_sustainable-and-smart-home]] |

---

_Last updated: 2026-06-09_
