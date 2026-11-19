# 🌐 Ethernet and PoE

## W5500

| Item | Value |
|---|---|
| Controller | WIZnet W5500 (LQFP-48, U2) over SPI |
| Pins | CS 10, MOSI 11, SCK 12, MISO 13, INT 9, RST 4 |
| Clock | 25 MHz crystal Y1, 18 pF load caps, 1 MΩ across |
| Mode | PMODE pins tied high (auto-negotiation) |
| Pull-ups | 10 kΩ on RST, CS and INT |
| Analog | 3V3 through ferrite L1, 12.4 kΩ on EXRES1, 22 nF VBG, 4.7 µF TOCAP, 10 µF V1P2 |

> [!NOTE]
> The analog network was inferred from the WIZnet reference design, not compared line by line. Do that before volume production.

## Magjack J1 (Hanrun HR871150C)

Link and activity LEDs go to the W5500 through 220 Ω to 3V3 (about 6 mA each). The jack overhangs the board edge by about 0.5 mm on purpose.

> [!WARNING]
> The jack pin map was decoded from a datasheet drawing, not a physical part. Check TX/RX pairs, PoE centre taps and LED polarity by continuity on the first board.

## PoE (802.3af)

An **SDAPO DP9700-5V** isolated PD module (PS1) does detection, classification and an isolated 5 V / 2 A converter, so no PD controller is needed on the board. Input 37-57 V, isolation 1.5 kV. Both mode A and mode B pairs are connected. Output goes to `5V_EXT`, then D4 into `+5V`.

### Before applying PoE

1. Confirm the module body orientation against a real part and that it clears C50 and the terminals.
2. Measure the unloaded output at C50.
3. Use a real 802.3af switch or injector. **Never use a passive 24/48 V injector** unless you have confirmed it supports 802.3af detection.
4. PoE is the **last** step of [[Bring-up Checklist]].

### Without PoE

Leave PS1 and C50 unpopulated and power from USB or J6. This saves about USD 4-5.5 per board.
