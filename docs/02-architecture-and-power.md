# 2. Architecture and power tree

## Power tree

```
USB-C VBUS --> PTC F1 (1.1 A) --> D3 (SS14) -----------+
                                                       |
J6 5V_EXT ------------------------> D4 (SS14) --------+--> +5V rail --> AMS1117-3.3 (U5) --> +3V3
                                                       |        |
PoE: RJ45 J1 --> DP9700-5V (PS1) --> 5V_EXT --> D4 ----+        +--> D5 (SS14) --> WS2812B VDD (LED_VDD)
                                                       |
                                                    C5 220 uF
```

- **Diode-OR**: USB VBUS (through D3) and `5V_EXT` (through D4) both feed `+5V`, so USB and the other source never back-feed each other.
- **PoE module and J6 share one net**: the DP9700 output and the J6 header are connected directly together on `5V_EXT`, with no diode between them. **Use only one of them at a time.** Do not put an external 5 V supply on J6 while a PoE module is powered, and do not power J6 from a different regulated supply than the PoE module output, or the two supplies will fight each other.
- **Rail voltage**: `+5V` is the source voltage minus one SS14 drop, so roughly 4.5-4.7 V when loaded. This is the voltage on J5 pin 2 ("5V") and on the WS2812 supply path. It is not a regulated 5.0 V.
- **3.3 V**: AMS1117-3.3 (U5) with 10 uF in (C6) and 22 uF out (C7). The LDO dropout (about 1.1 V at 1 A) is covered by the 4.5 V rail.
- **Bulk capacitors**: C5 (220 uF, +5V) and C50 (220 uF, 5V_EXT), both 6.3 x 5.4 mm SMD electrolytics rated 6.3 V. The rails sit about 1.5 V below the rating, which is thin for rev2 (see [docs/15](15-roadmap.md)).
- **Status LED**: the WS2812B is powered from `LED_VDD` = `+5V` minus an SS14, so its VDD is about 4.2 V and its data-high threshold (0.7 x VDD, about 2.9 V) is met by a 3.3 V GPIO. R2 (330 ohm) is in series with the data line.

## Current budget (estimates, verify on the bench)

| Load | Typical | Peak |
|---|---|---|
| ESP32-S3 (Wi-Fi TX peaks) | ~100-150 mA at 3.3 V | up to ~350-400 mA |
| W5500 | ~130 mA at 3.3 V | ~150 mA |
| 2 x SN65HVD72 + bias networks | < 20 mA | ~25 mA each when driving, plus ~5.5 mA bias when enabled |
| WS2812B | ~1-10 mA (one LED at low brightness) | 60 mA at full white |

The 3.3 V rail can reach roughly 500-600 mA at the peaks, which is about 0.6-0.8 A on the 5 V side once the LDO's pass-through is counted. That is **above the 500 mA a default USB port may supply**. On USB alone, expect brownouts if Wi-Fi and Ethernet are both active at full load; use PoE or an external supply for real use. AMS1117 power dissipation is (V_in - 3.3 V) x I, about 0.5-0.7 W at 0.5 A with a 4.6 V input, which the SOT-223 tab and the copper pour handle but will run warm.

## Isolation and grounding

- A single `GND` plane connects USB, the DMX terminals, and the logic.
- The PoE module is isolated (1.5 kV per the module datasheet), so the Ethernet side and shield (`CHASSIS`) are separate from `GND` on the PoE side. The RJ45 shield (`CHASSIS`) is tied to `GND` through C23 (10 nF) and R12 (1 M) in parallel.
- Because nothing isolates the DMX ports from USB, plugging in a laptop while a long DMX run is connected to a different earth can cause ground loops. Use an isolated USB hub or an isolated RS-485 version on rev2 if this matters.

## ESD and surge

- USB: USBLC6-2SC6 on D+ / D- (VBUS pin also tied).
- DMX: one SM712 asymmetric TVS (A, B, GND) per port. This clamps to -7 V / +12 V, matching RS-485 common-mode limits.
- No extra surge protection on the 5 V inputs beyond the PTC on USB.
