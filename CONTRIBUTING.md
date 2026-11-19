# Contributing

Thanks for helping. The most useful contributions at this stage:

1. **Test results from a built rev1 board**: bring-up measurements, scope screenshots of the DMX A/B lines, W5500 behaviour, PoE behaviour. Use the checklist in [docs/10](docs/10-bring-up-and-test.md) and the known-issues list in [docs/11](docs/11-known-issues-and-verification-status.md).
2. **Corrections** to footprints, pin maps and BOM part numbers (with a datasheet or a photo of the real part).
3. **Fixes and improvements** for rev2 (see [docs/15](docs/15-roadmap.md)).

## Making hardware changes

- Use KiCad 7 or later. Edit the project in `hardware/kicad/`.
- After any change, **re-run DRC** with the `.kicad_pro` next to the `.kicad_pcb` (the rules are stored in the project file) and make sure you add no new errors.
- If you change the netlist, update `bom/` and regenerate `fabrication/` from the board.
- Update the relevant page in `docs/` in the same change, and add an entry to `CHANGELOG.md`.
- Keep pin assignments consistent with the firmware `board.h`; if a pin changes, say so in the change description.

## Reporting issues

Include the board revision, what you did, what you expected, what happened, and measurements or photos. For electrical problems, a photo of both sides of the board is very helpful.

## Licence

By contributing you agree that your contribution is released under the project licence (CERN-OHL-P-2.0).
