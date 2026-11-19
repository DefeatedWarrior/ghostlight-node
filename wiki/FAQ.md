# FAQ

**Is it tested?** No. rev1 has not been manufactured. Firmware changes are also unbuilt.

**Why N8 and not N16R8?** The app is about 1.1 MB and needs no PSRAM, so the cheaper module is enough.

**Why SN65HVD72?** It is a 250 kbps part with fail-safe for open, short and idle bus, which suits DMX and RDM.

**Does it do RDM?** The hardware supports it (bidirectional ports); the firmware includes an RDM stack, untested on this board.

**Can I add a third port?** J5 exposes UART0, DIR3, BIAS3, LED3 and spare GPIOs for a daughterboard. UART0 is shared with the debug header.

**Can I sell it?** The licence allows it (CERN-OHL-P-2.0), but the name is not trademark-cleared.
