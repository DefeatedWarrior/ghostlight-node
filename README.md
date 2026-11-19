# Ghostlight Node

Open-source hardware for the **Ghostlight Node**: a low-cost **Art-Net / sACN to DMX512 node** with **two bidirectional (RDM-capable) DMX ports**, built around an ESP32-S3 and a W5500 Ethernet controller. Powered over USB-C, a 5 V input, or **802.3af PoE**.

This repository holds the hardware (rev1). The firmware lives in a separate repository, where this board is currently identified as `ESP-NODE-2RDM` (the `BOARD_NAME` in its `board.h`); see [docs/13-firmware-integration.md](docs/13-firmware-integration.md) for the pin map and the config changes this board needs.

| Front | Back (silkscreen only, mirrored) |
|---|---|
| ![front](docs/images/board-front.png) | ![back](docs/images/board-back.png) |

## The name

A *ghost light* is the single bulb left burning on an otherwise dark stage. The node does the same quiet job: it keeps the rig alive and listening while nothing else is on. "Ghostlight Node" has not been trademark-cleared; search your own country's register before selling boards under it.

## Features

- **MCU:** ESP32-S3-WROOM-1-N8 module (8 MB flash, no PSRAM), on-module Wi-Fi/BLE, native USB.
- **Ethernet:** WIZnet W5500 (SPI) with an HR871150C PoE-capable magjack (link and activity LEDs wired).
- **PoE:** SDAPO DP9700-5V isolated 802.3af module (5 V / 2 A), diode-OR'd with USB and an external 5 V header.
- **2 DMX ports:** SN65HVD72 3.3 V RS-485 transceivers (250 kbps, receiver fail-safe for open / short / idle bus), switchable bias (GPIO) and 120 ohm termination (jumper), SM712 TVS per port.
- **IN and OUT per port:** two 3-pole 5.08 mm screw terminals wired in parallel on the same transceiver (B / A / GND), so a port can be daisy-chained or wired to panel XLRs.
- **USB-C** device port (programming, console), 5.1 k CC resistors, USBLC6 ESD protection, 1.1 A PTC.
- **Status:** WS2812B status LED, one LED per DMX port, BOOT and RESET buttons.
- **Debug:** UART0 3-pin header (GND / TX / RX, 3.3 V logic).
- **Expansion:** 12-pin header J5 (3V3, 5V, GND, UART0 TX/RX, DIR3, BIAS3, LED3 and four spare GPIOs) for a third-port daughterboard or other add-ons.
- **Form factor:** 100 x 100 mm, 2 layers, 1.6 mm, four M3 mounting holes, hand-assembly friendly (0603 / 0805 passives, SOIC-8, LQFP-48).

## Status

**rev1 is design-complete and DRC-clean, but has not been manufactured or tested.** Treat the first batch as a prototype run. Read [docs/11-known-issues-and-verification-status.md](docs/11-known-issues-and-verification-status.md) before ordering: it lists what was verified, what was inferred from datasheet images, and what you should check on the first board.

## Repository layout

| Path | Contents |
|---|---|
| `hardware/kicad/` | KiCad 7 project: board, schematic, symbol library `ESPNODE`, footprint library `ESPNODE.pretty` |
| `fabrication/` | Gerbers + drill (`ghostlight-node-rev1-gerbers.zip` is the upload for JLCPCB), `gerbers/pos.csv` placement file |
| `bom/` | `BOM_order.csv` (per line, with reference designators), `BOM_order_purchase.csv` (LCSC part + quantity per board), `netlist.net` |
| `docs/` | Full documentation (see index below), schematic PDF, images |
| `tools/generator/` | Python scripts that generated the board and schematic (reference only, see `tools/generator/README.md`) |

## Documentation index

1. [Overview and specifications](docs/01-overview-and-specifications.md)
2. [Architecture and power tree](docs/02-architecture-and-power.md)
3. [Pin map and connectors](docs/03-pinout-and-connectors.md)
4. [Ethernet and PoE](docs/04-ethernet-and-poe.md)
5. [DMX / RS-485 ports](docs/05-dmx-ports.md)
6. [USB, programming and debug](docs/06-usb-programming-debug.md)
7. [Bill of materials and sourcing](docs/07-bom-and-sourcing.md)
8. [Ordering guide](docs/08-ordering-guide.md)
9. [Assembly guide](docs/09-assembly-guide.md)
10. [Bring-up and test plan](docs/10-bring-up-and-test.md)
11. [Known issues and verification status](docs/11-known-issues-and-verification-status.md)
12. [PCB design notes](docs/12-pcb-design-notes.md)
13. [Firmware integration](docs/13-firmware-integration.md)
14. [Regenerating the design](docs/14-regenerating-the-design.md)
15. [Roadmap and ideas for rev2](docs/15-roadmap.md)

The schematic is in [docs/schematic.pdf](docs/schematic.pdf) (net-label style, grouped by function).

## Quick start (ordering a prototype)

1. Upload `fabrication/ghostlight-node-rev1-gerbers.zip` to JLCPCB: 2 layers, 100 x 100 mm, 1.6 mm, HASL lead-free.
2. Import `bom/BOM_order_purchase.csv` into LCSC's BOM tool, multiply by the number of boards, add about 10 % spares for passives, and check stock (see [docs/08-ordering-guide.md](docs/08-ordering-guide.md)).
3. Assemble by hand following [docs/09-assembly-guide.md](docs/09-assembly-guide.md).
4. Bring up in the order in [docs/10-bring-up-and-test.md](docs/10-bring-up-and-test.md): USB power, 3V3, Ethernet, DMX, then PoE.

## Licence

Hardware design files are released under the **CERN Open Hardware Licence Version 2 - Permissive (CERN-OHL-P-2.0)**; see [LICENSE](LICENSE). Choose a different licence if you prefer, but do so before publishing. Datasheet-derived footprints in `ESPNODE.pretty` follow the same licence.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Hardware bug reports from a built board are the most valuable contribution.

## Trademarks

Art-Net is a trademark of Artistic Licence Engineering Ltd. ESP32 is a trademark of Espressif Systems. W5500 is a trademark of WIZnet. USB-C, PoE and other names belong to their respective owners. They are used here only to describe compatibility.
