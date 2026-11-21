# ❓ FAQ

**Is it tested?** No. rev1 has not been manufactured. Its firmware builds cleanly but has not run on a board.

**Why N8 instead of N16R8?** The firmware is about 1.1 MB and does not need PSRAM, so the cheaper module is enough.

**Why SN65HVD72?** It is a 250 kbps part with receiver fail-safe for open, short and idle buses, which suits DMX and RDM. The SP3485 is only fail-safe for open inputs and has weaker ESD.

**Can I use a different RS-485 chip?** Yes if it uses the standard SOIC-8 pinout, states open/short/idle fail-safe and has adequate ESD.

**Does it do RDM?** Hardware is bidirectional and the firmware has an RDM stack; neither has been tested on this board.

**Can I skip PoE?** Yes. Leave PS1 and C50 unpopulated and use USB or J6.

**Can I add a third port?** J5 provides UART0, DIR3, BIAS3, LED3 and spare GPIOs. UART0 is shared with the debug header, so use USB as console.

**Why 100 × 100 mm?** JLCPCB's cheapest price tier has historically stopped there.

**Can I sell it?** The licence allows it (CERN-OHL-P-2.0, permissive). The name "Ghostlight Node" is not trademark-cleared.

**Does the firmware only run on this board?** No. It also runs on ESP32-S3 and original ESP32 dev boards with a W5500 and two RS485 transceivers, and other boards can be added. So far it has actually run only on the ESP32-S3 N16R8 dev-board prototype. See [[Firmware]].

**Why does the firmware say ESP-NODE-2RDM?** That is the original firmware project name; the board is still reported under it.
