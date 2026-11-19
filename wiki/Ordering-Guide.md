# 🛒 Ordering Guide

## 1. PCB

Upload `fabrication/ghostlight-node-rev1-gerbers.zip` (12 files: 2 copper, 2 mask, 2 silk, 2 paste, outline, drill, drill map, job file).

| Setting | Value |
|---|---|
| Layers | 2 |
| Size | 100 × 100 mm (do not enlarge: JLCPCB's cheapest tier has historically stopped there; check current pricing) |
| Thickness | 1.6 mm |
| Finish | HASL, lead-free if available |
| Copper | 1 oz |
| Minimums used | 0.15 mm clearance, 0.2 mm track, 0.5/0.3 mm via |
| Stencil | not needed for hand assembly |

## 2. Parts

1. Upload `bom/BOM_order_purchase.csv` to LCSC's BOM tool (`lcsc`, `qty_per_board`).
2. Multiply by your board count.
3. Add about 10 % spares on passives and LEDs.
4. **Check stock on every line.** Tight at last check (2026-11-11): DP9700 (22), HR871150C (14-248).

## 3. If stock runs out

- **PoE module:** another isolated 802.3af PD module with a 5 V / 2 A output works only with a new footprint.
- **PoE-optional:** leave PS1 and C50 off and use USB or J6.
- **Magjack:** any pin-compatible 10/100 magjack with LEDs.

## 4. Assembly service

Not set up. The BOM and `pos.csv` are in KiCad format, not JLCPCB's SMT format, and the PoE module, terminals, headers, magjack and electrolytics are parts most services do not place.

## ✅ Pre-order checklist

- [ ] Re-checked LCSC stock for every line
- [ ] Read [[Known Issues]]
- [ ] Printed footprints 1:1 and held real J1, PS1, J4, switches and terminals against them (recommended)
- [ ] Decided about the firmware changes ([[Firmware]])
- [ ] Ordered shunts and one 1×40 header strip
