# Changelog

## rev1 (unreleased, untested)

Named **Ghostlight Node** (repository `ghostlight-node`). The firmware still calls the board `ESP-NODE-2RDM`.

First complete design.

- `firmware/`: ESP-NODE-2RDM firmware (MIT, ThinhCNTT22) with N8 changes applied: 8 MB flash, PSRAM disabled, 8 MB partition table, port LEDs on GPIO5/6. Not built or tested.

- 100 x 100 mm, 2-layer board with ESP32-S3-WROOM-1-N8, W5500 Ethernet and two SN65HVD72 DMX ports.
- IN and OUT 3-position screw terminals per DMX port in parallel on a single transceiver; jumper termination and GPIO-switchable bias; SM712 TVS per port.
- PoE (802.3af) via the SDAPO DP9700-5V module and the HR871150C magjack, with the jack link and activity LEDs wired to the W5500.
- USB-C device port, USBLC6 ESD protection, 1.1 A PTC, diode-OR with the 5 V header and the PoE output.
- UART0 debug header J7 and the 12-pin expansion header J5.
- Silkscreen labels for terminals (B / A / GND), buttons, headers and the project title block.
- KiCad schematic (net-label style), gerbers, BOM with LCSC part numbers, documentation.
- Switched the module from N16R8 to N8 (8 MB flash, no PSRAM).
- Replaced out-of-stock capacitors and the green LED part with in-stock alternatives (C1591, C107040, C29936, C32514, C12065).
