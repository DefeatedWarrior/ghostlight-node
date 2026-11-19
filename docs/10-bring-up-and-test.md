# 10. Bring-up and test plan

Do these in order. **Stop and investigate at the first failure.** Use a bench power supply with current limiting if you have one. Never connect PoE first.

## 0. Before power

| Check | Expected |
|---|---|
| Resistance +5V to GND | not a short |
| Resistance +3V3 to GND | not a short |
| USB-C CC1 / CC2 to GND | about 5.1 k each (R3, R4) |
| Diode orientation (D3, D4, D5) | cathode toward the +5V side |

## 1. USB power only

Plug in USB-C (preferably through a powered hub or a bench supply set to 5 V, current limit about 300 mA first).

| Measure | Expected |
|---|---|
| +5V rail | about 4.5-4.7 V (VBUS minus the SS14 and PTC drop) |
| +3V3 rail | 3.3 V +/- 5 % |
| Supply current, nothing flashed | well under 100 mA |
| Component temperatures | nothing too hot to touch in the first minute (U5 may be warm) |

## 2. Flash and console

Hold BOOT, tap RESET, release BOOT. Confirm the USB device appears, flash the firmware, and read the console (USB or J7 at 3.3 V logic). Confirm the ESP32 boots and the status LED responds.

## 3. Ethernet

1. Connect a normal (non-PoE) switch or router with a patch cable. The jack's link and activity LEDs should light and the firmware should report a link and obtain an IP.
2. If the W5500 is not detected: probe the 25 MHz crystal, check 3V3 on the W5500 AVDD pins and the SPI lines (CS, SCK, MOSI, MISO), the RST and INT pull-ups, then compare the analog network to the WIZnet reference ([docs/11](11-known-issues-and-verification-status.md)).
3. Ping the node and send Art-Net or sACN.

## 4. DMX

1. Connect a scope or logic analyser to A and B (use differential probing or probe A and B separately against GND).
2. Send a DMX frame. Confirm 250 kbaud, break and mark-after-break timing, and that the receive pin is quiet when DIR is low and the bus is idle.
3. **Check the A / B polarity** against a known-good fixture or DMX tester and fix the labelling or wiring if needed.
4. With BIAS on, measure the idle differential on the line (should be above 200 mV into a terminated line) and confirm the receiver stays quiet (no phantom RDM responses).
5. Verify each port's termination jumper by measuring about 120 ohm across A and B with it fitted and the bus idle.
6. Check both ports, and both IN and OUT terminals, independently.

## 5. PoE (last)

1. Check the PoE module orientation and the 5V_EXT voltage with a lab PoE source or an 802.3af injector **before** connecting a load.
2. With USB disconnected, power through an 802.3af switch port. Expect the module output near 5 V and the board to boot.
3. Verify 5V_EXT, +5V and +3V3 under load (Wi-Fi + Ethernet + both DMX ports active).
4. Connect USB at the same time as PoE: nothing should back-feed (diode-OR), and current should not flow from one source into the other.

## Record results

Please open an issue with the results (scope screenshots of A/B, voltages, any wiring changes) so rev2 can be corrected.
