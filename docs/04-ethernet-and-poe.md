# 4. Ethernet and PoE

## W5500 Ethernet

| Item | Value |
|---|---|
| Controller | WIZnet W5500 (LQFP-48, U2), SPI to the ESP32-S3 |
| SPI | CS GPIO10, MOSI GPIO11, SCK GPIO12, MISO GPIO13, INT GPIO9, RST GPIO4 |
| Clock | 25 MHz crystal Y1 (HCI XC32M4-25.000-F20NJDT, 20 pF load), 18 pF caps C19 / C20, 1 M across the crystal (R7) |
| Mode | PMODE pins 43-45 tied together to 3V3 through R8 (10 k): tied high so the W5500 starts in all-capable auto-negotiation mode (PMODE 111; confirm against the W5500 datasheet) |
| Pull-ups | R9 on RST, R10 on CS, R11 on INT (10 k each, to 3V3) |
| Analog supply | 3V3 through ferrite bead L1 (BLM18AG121SN1D, 120 ohm @ 100 MHz) to `AVDD`, with 4 x 100 nF (C10-C13) and 10 uF (C14) |
| Other analog network | R6 12.4 k 1 % on EXRES1, C16 22 nF on VBG, C17 4.7 uF on TOCAP, C18 10 uF on V1P2, C15 100 nF on 3V3 |

The W5500's analog network values were inferred from the WIZnet reference design and **have not been compared line by line to the current reference schematic**. Do that before volume production (see [docs/11](11-known-issues-and-verification-status.md)).

### Magjack (J1, Hanrun HR871150C)

| Jack pin | Net | Notes |
|---|---|---|
| 1 | TXP | to W5500 pin 2 |
| 2 | TXN | to W5500 pin 1 |
| 3 | TCT | TX centre tap, decoupled to 3V3 through C21 (100 nF) |
| 4 | RXP | to W5500 pin 6 |
| 5 | RXN | to W5500 pin 5 |
| 6 | not connected | |
| 7, 8 | POE_A1, POE_A2 | PoE centre taps, pairs 1/2 and 3/6 |
| 9, 10 | POE_B1, POE_B2 | PoE centre taps, spare pairs 4/5 and 7/8 |
| 11 | JLED_ACT_A | activity LED anode, through R50 (220 ohm) to 3V3 |
| 12 | LED_ACT | activity LED cathode, to W5500 ACTLED (pin 27) |
| 13 | JLED_LNK_A | link LED anode, through R51 (220 ohm) to 3V3 |
| 14 | LED_LINK | link LED cathode, to W5500 LINKLED (pin 25) |
| SH | CHASSIS | shield, tied to GND through 10 nF (C23) and 1 M (R12) |

**Verify the pin map before relying on it.** It was decoded from the jack's datasheet drawing (the label text could not be extracted), not from a physical sample. The jack footprint is the custom `ESPNODE:RJ45_Hanrun_HR871150C`. Check TX/RX pair orientation, the PoE centre tap pins, and the LED polarity with a continuity test on the first board.

The W5500 LED outputs sink the LED current. With a 220 ohm resistor from 3.3 V and a typical LED forward voltage near 2 V, the current is roughly 6 mA. Check that against the W5500's LED output drive rating; if it is too high, raise R50 / R51 (a larger resistor only dims the LED).

The Ethernet pairs run about 35-45 mm on the board. They are not impedance-controlled or length-matched, which is acceptable for 10/100 Mbps.

## PoE (802.3af)

PoE is provided by an **SDAPO DP9700-5V** isolated PD module (PS1). The module provides detection, classification, an isolated DC-DC converter and a 5 V / 2 A output, so the board does not need its own PD controller.

| Module pin | Net | Meaning |
|---|---|---|
| 1 | POE_A1 | VA1: centre tap of pairs 1/2 |
| 2 | POE_A2 | VA2: centre tap of pairs 3/6 |
| 3 | POE_B1 | VB1: spare pairs 4/5 |
| 4 | POE_B2 | VB2: spare pairs 7/8 |
| 5, 6, 9, 10 | not connected | |
| 7 | GND | output - (-VDC) |
| 8 | 5V_EXT | output + (+VDC) |

- Input range per the module datasheet: 37-57 V. Output 5 V, 2 A. Isolation 1.5 kV.
- The module output goes to `5V_EXT` (bulk C50, 220 uF), then through D4 (SS14) into the `+5V` rail.
- Spare-pair (mode B) and data-pair (mode A) PoE are both connected to the module.

### Checks before applying PoE

1. **Module orientation.** The footprint reserves about 10.5 mm either side of the pin row. Confirm against a real module that the body sits on the correct side of pin 1 and does not collide with C50 or the terminals.
2. **Output voltage with no load**, measured at C50 before the board's logic is powered from it.
3. **Test with a proper 802.3af PoE switch or injector.** Never connect a passive 24 V or 48 V injector until you have checked that the injector supports 802.3af detection.
4. See [docs/10](10-bring-up-and-test.md): PoE is the last step of the bring-up.
