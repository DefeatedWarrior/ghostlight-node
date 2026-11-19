# Generator scripts (reference)

These Python scripts generated the rev1 board, schematic and BOM. See [docs/14-regenerating-the-design.md](../../docs/14-regenerating-the-design.md).

- They reference absolute paths from the machine that produced the board (`/home/claude/pcb/...`): edit them before running.
- They need KiCad 7's Python (`pcbnew`), `kiutils`, Java with Freerouting 1.9.0, and `xvfb-run`.
- `design.py` is the netlist source of truth (parts, values, nets, LCSC numbers). `layout.py` holds placement overrides.
- The hand-made footprints (`ESPNODE.pretty`) are checked in under `hardware/kicad/`; there is no script for them in this folder.
- Treat the checked-in board in `hardware/kicad/` as the source for manufacturing. Re-running the pipeline will give a different (non-deterministic) routing.
