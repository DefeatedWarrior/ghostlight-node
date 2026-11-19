# 🔥 Assembly Guide

Hot air or a hotplate makes the W5500, ESP32 module and USB-C connector much easier.

## Order of work

1. **Hardest first**
   - **U2 W5500** (LQFP-48, 0.5 mm): tack two corners, flux, drag-solder, clean bridges with braid.
   - **J4 USB-C:** signal pins first, then shield posts.
   - **U1 ESP32-S3:** castellated pads and the centre ground pad. Antenna end hangs at the board edge with nothing under it.
2. **SOIC / SOT:** U3, U4, U5 (tab to the large pad), U6, Q1, Q2, D1, D2.
3. **Passives:** 0603 first, then 0805 (C1, C6, C7, C14, C17, C18). Crystal Y1 has no polarity.
4. **Polarised parts**
   - **D3, D4, D5 (SS14):** cathode band toward the +5V side (D5 toward `LED_VDD`).
   - **D30, D40 LEDs:** cathode to GND.
   - **LED1 WS2812B:** pin 1 marked on the board.
   - **C5, C50:** + mark toward the 5 V rail.
5. **Through-hole:** headers, screw terminals (wire entry toward the edge), J1 RJ45, and **PS1 last** because it covers most of the board.
6. Shunts on J2T/J3T only if the node is the last device on a DMX line.

## After soldering

- [ ] Inspect under magnification: bridges on W5500, USB-C, ESP32, SOIC pins.
- [ ] Orientation of diodes, LEDs, electrolytics.
- [ ] +3V3 to GND and +5V to GND are **not** shorts.
- [ ] Clean flux with isopropyl alcohol.

Then go to [[Bring-up Checklist]].
