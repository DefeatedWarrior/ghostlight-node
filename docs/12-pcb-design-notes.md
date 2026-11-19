# 12. PCB design notes

## Board

| Item | Value |
|---|---|
| Outline | 100 x 100 mm rectangle |
| Layers | 2 (F.Cu signals + ground pour, B.Cu signals + ground pour) |
| Thickness | 1.6 mm |
| Rules used | clearance 0.15 mm, track 0.2 mm minimum, via 0.5 mm pad with 0.3 mm drill (JLCPCB 2-layer capabilities) |
| Mounting | four M3 holes at (4, 4), (96, 4), (4, 72) and (96, 96) mm |
| Antenna | the ESP32-S3 module is at the top edge with its antenna end toward the edge. A copper keep-out (no tracks or pours) lies under the antenna, visible as a black band at the top of the front photo |
| RJ45 | the J1 jack overhangs the board edge by about 0.5 mm |

## Layout choices

- **Placement is by function** and was laid out for hand assembly: the MCU at the top, power and USB on the left, Ethernet at the bottom left, W5500 centred, DMX ports on the right, screw terminals along the bottom edge.
- **Terminals along the bottom edge** with the PoE module above them: the first outline was 100 x 80 mm, but the PoE module plus IN and OUT terminals for each port (four 3-position 5.08 mm blocks) did not fit, so the board was grown to a square 100 x 100 mm.
- **Routing** was done with Freerouting 1.9.0 and imported back into KiCad, then power nets were widened. The router is non-deterministic: the shipped board is the best of several runs that met all design rules (0 DRC errors, 0 unconnected), not a bit-for-bit reproducible result.
- **Ethernet**: TXP / TXN and RXP / RXN pairs about 35-45 mm, not length-matched, adequate for 10/100.
- **Power**: the +5V and 5V_EXT nets were widened after routing; ground is a pour on both layers with stitching vias.
- **ESD parts**: the USBLC6 is placed next to the USB-C connector; each SM712 TVS sits beside its transceiver, not at the screw terminals, so the A / B traces run to the terminals from there.
- **Thermal**: the AMS1117 dissipates (V_in - 3.3 V) x I, about 0.5-0.7 W at 0.5 A. It sits on a copper pour. Watch it during Wi-Fi + Ethernet load.

## Silkscreen

Front: reference designators, terminal pin names (B / A / GND), BOOT / RESET / USB-C / 5V IN labels, debug UART pin names, J5 pin names, "120R TERM" next to the termination jumpers, and a title block (ESP-NODE-2RDM rev1, "Art-Net/sACN > DMX512 x2", "PoE 802.3af / USB-C / RDM", "Open hardware CERN-OHL-P-2.0").

Back: IN / OUT tags under each DMX terminal (the strip between the PoE module and the terminals fits only one row of front text, so these are on the back), board name and licence, and the GPIO map (DMX1, DMX2, W5500, LEDs, BOOT).

The DMX A / B polarity is intentionally **not** stated as D+ / D- on the silkscreen until it is verified on hardware.

## Custom libraries

`hardware/kicad/ESPNODE.pretty` holds two footprints generated from datasheets:

- `RJ45_Hanrun_HR871150C` (the PoE magjack)
- `PoE_SDAPO_DP9700` (the PoE module pin row and keep-out)

and `ESPNODE.kicad_sym` holds the matching symbol for the jack. Project tables `fp-lib-table` and `sym-lib-table` reference them with `${KIPRJMOD}`.

## Files KiCad may regenerate

The board file was generated and finished by scripts (see [docs/14](14-regenerating-the-design.md)). If you open it in newer KiCad versions it will be upgraded on save. Use KiCad 7 or later; DRC should be re-run after any edit.
