# 14. Regenerating the design

The board and schematic were produced by Python scripts, kept in `tools/generator/`. They are included for reference and reproducibility of the **netlist and placement**; the committed board and gerbers are the source of truth for manufacturing. The routed result is not reproducible bit-for-bit (the autorouter is non-deterministic).

> The scripts contain absolute paths from the machine where they ran (`/home/claude/pcb`) and expect KiCad 7's Python (`pcbnew`), `kiutils`, Java + Freerouting 1.9.0 and `xvfb-run`. You will need to edit the paths before running anything.

## Pipeline

| Step | Script | What it does |
|---|---|---|
| 1 | `design.py` | single source of truth: parts, values, footprints and nets |
| 2 | `layout.py` | placement overrides |
| 3 | `build_pcb.py` | creates the `.kicad_pcb` with footprints, outline, mounting holes and nets |
| 4 | `route.py` / `import_ses.py` | sets the design rules (0.15 mm clearance, 0.2 mm track, 0.5 / 0.3 mm via), removes the pours so GND is routed as copper, exports a Specctra DSN, runs Freerouting, then imports the session (SES) back |
| 5 | `finish.py` | post-route clean-up: island removal, GND stitching vias, solid ground pads on the USB-C shield, zone refill |
| 6 | `widen.py` | widens the `+3V3`, `+5V`, `VBUS`, `VBUS_F` and `5V_EXT` tracks (0.5 / 0.35 / 0.25 mm steps, where space allows) |
| 7 | `drc.py` | runs KiCad's DRC through pcbnew and prints the violation counts |
| 8 | `silk.py` | adds the silkscreen labels, title block and back-side text |
| 9 | `gen_sch.py` | generates the net-label schematic and the `ESPNODE.kicad_sym` symbol library |
| 10 | `bom.py` | writes `BOM_order.csv` and `BOM_order_purchase.csv` |

`chain.sh` runs steps 3-7 (step 8, `silk.py`, is run separately on the finished board) in order (`MP` = Freerouting pass limit); `search.sh` repeats it with different pass limits until DRC is clean.

## Editing the design by hand

The simplest path for rev2 is to **open the KiCad project directly** (`hardware/kicad/ghostlight-node-rev1.kicad_pro`), edit the schematic and board in KiCad, and re-run DRC. Keep `design.py` only if you want to keep regenerating from scripts.

## Exporting fabrication files from KiCad 7

```
kicad-cli pcb export gerbers --layers F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,F.Paste,B.Paste,Edge.Cuts -o out/ board.kicad_pcb
kicad-cli pcb export drill --format excellon --excellon-units mm --generate-map --map-format gerberx2 -o out/ board.kicad_pcb
kicad-cli pcb export pos --format csv --units mm --side both -o out/pos.csv board.kicad_pcb
kicad-cli sch export netlist -o out/net.net schematic.kicad_sch
```

(The output directory must already exist.) Always keep the `.kicad_pro` next to the `.kicad_pcb` when running DRC, because the design rules are stored in it.
