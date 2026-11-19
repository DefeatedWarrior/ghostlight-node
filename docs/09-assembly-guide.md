# 9. Assembly guide (hand assembly)

Tools: temperature-controlled iron with a fine tip, flux, fine solder (0.5 mm), tweezers, desoldering braid, magnification, multimeter. Hot air or a hotplate makes the W5500, the ESP32 module and the USB-C connector much easier. Look at the silkscreen photo in the README for reference designators and orientation.

## Order

1. **Smallest and most difficult first**
   - U2 (W5500, LQFP-48, 0.5 mm pitch). Tack two opposite corners, flux, drag-solder, then clean up bridges with braid. Pin 1 is marked on the silkscreen.
   - J4 (USB-C, 16 pin with through-hole shield tabs). Solder the signal pins first, then the shield posts.
   - U1 (ESP32-S3 module): solder the castellated pads and the central thermal pad (ground). The antenna end must hang at the board edge with nothing under it.
2. **SOIC / SOT**: U3, U4 (SN65HVD72, pin 1 dot toward the silkscreen 1 marker), U5 (AMS1117, tab to the large pad), U6 (USBLC6), Q1, Q2, D1, D2 (SM712 is a 3-pin SOT-23).
3. **Passives**: 0603 resistors and capacitors; 0805 capacitors (C1, C6, C14, C18, C7, C17). Take care with the crystal Y1 (3225, 4 pads; there is no polarity but keep the part flat).
4. **Polarised parts**
   - Schottky diodes D3, D4, D5 (SS14, SMA): the **cathode band goes to the +5V side** for D3 and D4 (the rail), and to the LED supply (`LED_VDD`) side for D5. Check against the silkscreen.
   - LEDs D30, D40: **cathode to GND**. Check the green marker on the part.
   - WS2812B (LED1): pin 1 marked with "1" on the board.
   - Electrolytics C5, C50: **+ mark** on the board marks the positive terminal, toward the +5V rail / `5V_EXT`.
   - PTC F1 and ferrite L1 have no polarity.
5. **Through-hole**: pin headers J5, J6, J7, J2T, J3T (snap from the 1x40 strip), screw terminals J2, J2O, J3, J3O (wire entry toward the board edge), J1 RJ45, then **PS1 (PoE module) last** because it sits over most of the board.
6. Fit shunts on J2T / J3T only if the board is the last device on a DMX line.

## After soldering

- **Visual check** under magnification: bridges on the W5500, USB-C, ESP32 and SOIC pins, correct orientation of diodes, LEDs, and electrolytics.
- **Continuity** with the board unpowered: +3V3 to GND and +5V to GND must **not** be a short (expect resistance in the hundreds of ohms to kilohms depending on the multimeter, not near zero).
- Clean flux off with isopropyl alcohol.
- Go to [docs/10](10-bring-up-and-test.md).
