# 8. Ordering guide

## 1. PCB (JLCPCB or any fab)

Upload `fabrication/ghostlight-node-rev1-gerbers.zip` (12 files: 2 copper layers, 2 masks, 2 silkscreens, 2 paste, outline, drill, drill map, job file).

| Setting | Value |
|---|---|
| Layers | 2 |
| Dimensions | 100 x 100 mm (JLCPCB's cheapest price tier has historically stopped at 100 x 100 mm, so the board was kept at that size; check current pricing and do not enlarge it) |
| Thickness | 1.6 mm |
| Surface finish | HASL (lead-free if available) |
| Copper | 1 oz |
| Minimums used | 0.15 mm clearance, 0.2 mm track, 0.5 mm via with 0.3 mm drill |
| Solder paste stencil | not needed for hand assembly with a soldering iron; order one if you reflow |
| SMT assembly | not set up; see below |

The J1 jack overhangs the board edge by about 0.5 mm. That is intentional.

## 2. Parts (LCSC)

1. Open LCSC's BOM tool and upload `bom/BOM_order_purchase.csv` (columns: `lcsc`, `qty_per_board`).
2. Set the quantity multiplier to the number of boards.
3. Add about 10 % spares on resistors, capacitors and LEDs; hand assembly loses parts.
4. **Check stock for every line.** Known tight lines at the time of the last check (2026-11-11): the DP9700 PoE module (22 in stock), the HR871150C jack (14-248), and the 220 uF capacitors if you pick a different part.
5. Out-of-stock parts have in-stock substitutes listed in [docs/07](07-bom-and-sourcing.md); if you swap a part, update `bom/` and the schematic value.

## 3. Alternatives if stock runs out

- **PoE module**: any isolated 802.3af PD module with a 5 V / 2 A output and a similar pinout can be used, but the footprint (`ESPNODE:PoE_SDAPO_DP9700`) is specific to the DP9700. A different module needs a new footprint.
- **PoE-optional builds**: leave PS1 and C50 unpopulated and power the board from USB or J6. The RJ45 magjack stays the same (the PoE pins just go to nothing). This saves about $4-5.5 per board.
- **Magjack**: any pin-compatible 10/100 magjack with LEDs; a PoE-capable one is needed only if PoE is used.

## 4. Assembly service (not set up)

The files `bom/BOM_order.csv` and `fabrication/gerbers/pos.csv` are in KiCad's native format and **are not formatted for JLCPCB's SMT assembly upload** (different column names, rotation conventions). The design was made for **hand assembly**, so no assembly-house flow was tested. The PoE module, screw terminals, headers, the magjack and the electrolytic capacitors are through-hole or large parts that most assembly services do not place.

## 5. Pre-order checklist

- [ ] Re-checked LCSC stock for every line, especially PS1, J1, the crystal and the electrolytics
- [ ] Read [docs/11](11-known-issues-and-verification-status.md)
- [ ] Printed the footprints 1:1 and held the real J1, PS1, J4, SW1 / SW2 and the terminals against them (optional but recommended for the first order)
- [ ] Decided what to do about the firmware changes needed for the N8 module ([docs/13](13-firmware-integration.md))
- [ ] Ordered enough 2.54 mm shunts and one 1x40 pin header strip
