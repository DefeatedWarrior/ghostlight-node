# 11. Known issues and verification status

rev1 has **not been built or tested**. This page separates what was checked from what was inferred, so you know what to verify on the first board.

## What was verified

| Check | Result |
|---|---|
| KiCad DRC (pcbnew, KiCad 7.0.11) | 0 clearance errors, 0 unconnected items, 0 shorts. 8 silkscreen warnings and 1 library-footprint mismatch (U1) remain and do not affect fabrication |
| PCB nets vs schematic nets | 72 nets each, no mismatches (compared from exported netlists) |
| Gerbers | Exported from the final board; copper, mask, paste and drill geometry re-compared against the earlier export |
| GPIO map vs firmware | DMX1 (UART1 17/16/39), DMX2 (UART2 15/18/40), W5500 CS/MOSI/MISO/SCK/INT (10/11/13/12/9), status LED 48, BOOT 0 match the firmware `board.h` and `network_manager.c` |
| SN65HVD72 fail-safe | The TI datasheet lists the receiver output as fail-safe high for open, short-circuit and idle bus |
| LCSC part numbers | All 39 purchase lines carry a number whose part name matched the intended part when checked on 2026-11-11 |

## What was not verified (do these before volume)

### Electrical design

1. **No ERC was run.** KiCad 7's command line has no ERC command. Open the schematic in the KiCad GUI and run Inspect > Electrical Rules Checker. The schematic is net-label style (global labels with short stubs, PWR_FLAG symbols), and KiCad reports an "annotation errors" warning on export that was not investigated.
2. **W5500 analog network** (L1, C10-C18, R6, the TX centre-tap capacitor C21 to 3V3) was inferred from the WIZnet reference design, not compared line by line. Check against the current WIZnet reference schematic.
3. **W5500 LED pins** drive the jack LEDs through 220 ohm to 3V3 (about 6 mA each). The W5500 LED output drive rating was not checked.
4. **DMX A / B polarity** and the SN65HVD72 edge behaviour need a scope or a known-good fixture; the silkscreen says only A and B.
5. **DMX bias values** (240 ohm) were chosen by the designer and not checked against the E1.20 text. Expect about 0.6 V idle differential into a terminated line and about 5.5 mA of bias current.
6. **Crystal load**: 20 pF crystal with 18 pF caps, not calculated for the actual layout.
7. **USB-only power budget**: a 500 mA USB port can brown out when Wi-Fi, Ethernet and both DMX ports run at once. Use PoE or an external 5 V supply for real use.
8. **5 V rails** use 6.3 V electrolytics with about 1.5 V of margin (see [docs/02](02-architecture-and-power.md)).

### Mechanical / footprints

9. **HR871150C pin map** was decoded from the datasheet drawing (VC1 / VC2 labels), not from a physical part. Verify TX/RX pairs, PoE centre taps and LED polarity by continuity.
10. **DP9700 body orientation** relative to the pin row is not confirmed; the footprint reserves about 10.5 mm either side of the pin row.
11. **Tactile switch**: the TL3342 footprint is assumed to match the actual switch part (E-Switch TL3342F160QG).
12. **220 uF capacitors** (6.3 x 5.4 mm) were matched by case size only; compare the datasheet drawing to the footprint.
13. **No test points** are fitted on rev1. Probing 3V3, 5V, GND and the DMX lines relies on the header pins, the capacitors and the transceiver pins.
14. **Enclosure**: there is no enclosure drawing yet. Mounting hole H3 at (4, 72) mm sits close to the RJ45 jack and the PoE module; check clearances before designing a case.

### Layout

15. **Ethernet pairs** run about 35-45 mm and the `5V_EXT` run is about 65 mm. Neither is a problem on paper (10/100, 2 A), but they were not checked on a prototype. The PCB was routed with Freerouting 1.9.0 and is not bit-for-bit reproducible.
16. **Silkscreen** has 8 warnings from existing component outlines (reference text overlapping outlines, a few outline segments clipped by the board edge or by mask openings). They affect appearance only.
17. **No SMT assembly flow tested** (see [docs/08](08-ordering-guide.md)).

### Firmware compatibility (not hardware bugs)

18. The firmware repository still targets the N16R8 module (16 MB flash, 8 MB octal PSRAM). It will not boot on the N8 until PSRAM is disabled and the flash size and partition table are cut to 8 MB. See [docs/13](13-firmware-integration.md).
19. `BOARD_PORT_LED_GPIO` is `{-1, -1}` in the firmware; the board has port LEDs on GPIO5 and GPIO6.
20. The firmware does not drive the W5500 reset (the driver is configured with `reset_gpio_num = -1`) or the DMX bias pins (GPIO1 / GPIO2). The W5500 reset line has a pull-up so the part runs, and the bias networks are off by default.
21. UART0 is shared by the J7 debug console and J5 pins 4-5; a third DMX port on J5 means using USB for the console.

## Reporting results

Open an issue describing the failure: board revision, symptom, measurements or scope screenshots, and what you changed. Results from the first built board are the most useful input for rev2.
