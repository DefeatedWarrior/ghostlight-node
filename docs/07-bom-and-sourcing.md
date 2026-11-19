# 7. Bill of materials and sourcing

Files: `bom/BOM_order.csv` (one line per part type with reference designators, value, footprint and status) and `bom/BOM_order_purchase.csv` (LCSC part number and quantity per board, ready for the LCSC BOM tool).

- 39 purchase lines, all parts have an LCSC number.
- `OK` in the status column means the LCSC number matched the stated part name when it was checked. `OK*` means the part is also on the "check live stock and size" list below. `CHECK` means a line needs a closer look.
- **Stock and prices were last checked on 2026-11-11 and change daily.** Re-import the purchase list before ordering.

## BOM (per board)

| LCSC | Refs | Qty | Value | Part | Status |
|---|---|---|---|---|---|
| C15850 | C1 C6 C14 C18 | 4 | 10uF | Samsung CL21A106KAYNNNE 10uF 0805 | OK |
| C21122 | C16 | 1 | 22nF | Samsung CL10B223KB8NNNC 22nF | OK |
| C1779 | C17 | 1 | 4.7uF | Samsung CL21A475KAQNNNE 4.7uF 0805 | OK |
| C107040 | C19 C20 | 2 | 18pF | Yageo CC0603JRNPO9BN180 18pF 50V NP0 | OK |
| C1591 | C2 C4 C10 C11 C12 C13 C15 C21 C30 C40 | 10 | 100nF | Samsung CL10B104KB8NNNC 100nF 50V X7R | OK |
| C1589 | C23 | 1 | 10nF | Samsung CL10B103KB8NNNC 10nF | OK |
| C29936 | C3 | 1 | 1uF | Samsung CL10B105KA8NNNC 1uF 25V X7R 0603 | OK |
| C32514 | C5 C50 | 2 | 220uF | Honor RVT0J221M0605 220uF 6.3V 6.3x5.4 | OK |
| C45783 | C7 | 1 | 22uF | Samsung CL21A226MAQNNNE 22uF 0805 | OK |
| C2943053 | D1 D2 | 2 | SM712 | SM712 SOT-23 TVS | OK* |
| C12065 | D30 | 1 | P1 | LITEON LTST-C193TGKT-5A emerald green 0603 | OK |
| C12065 | D40 | 1 | P2 | LITEON LTST-C193TGKT-5A emerald green 0603 | OK |
| C2480 | D5 D3 D4 | 3 | SS14 | MDD SS14 SMA | OK |
| C22366107 | F1 | 1 | PTC 1.1A | BORN SMD1206-110/6N PTC | OK |
| C19724786 | J1 | 1 | HR871150C | Hanrun HR871150C 10/100 PoE RJ45 magjack | OK* |
| C474953 | J2 J2O J3 J3O | 4 | Screw terminal 3P 5.08 | Cixi Kefa KF128-5.08-3P-AA screw terminal | OK |
| C165948 | J4 | 1 | USB-C (device/sink) | HRO TYPE-C-31-M-12 | OK |
| C2337 | J5 | 1 | PinHeader_1x12_P2.54mm_Vertical | BOOMELE 2.54mm 1x40P pin header (snap to length) | OK |
| C2337 | J6 J2T J3T | 3 | PinHeader_1x02_P2.54mm_Vertical | BOOMELE 2.54mm 1x40P pin header (snap to length) | OK |
| C2337 | J7 | 1 | PinHeader_1x03_P2.54mm_Vertical | BOOMELE 2.54mm 1x40P pin header (snap to length) | OK |
| C76892 | L1 | 1 | FB 120R@100MHz | Murata BLM18AG121SN1D | OK |
| C114586 | LED1 | 1 | WS2812B | Worldsemi WS2812B-B/W 5050 | OK |
| C5380091 | PS1 | 1 | DP9700-5V | SDAPO DP9700-5V PoE PD module 5V/2A | OK* |
| C8545 | Q1 Q2 | 2 | 2N7002 | JSCJ 2N7002 SOT-23 | OK |
| C25804 | R1 R5 R8 R9 R10 R11 R30 R40 | 8 | 10k | UNI-ROYAL 0603WAF1002T5E | OK |
| C23138 | R2 | 1 | 330 | UNI-ROYAL 0603WAF3300T5E | OK |
| C23186 | R3 R4 | 2 | 5.1k | UNI-ROYAL 0603WAF5101T5E | OK |
| C23350 | R31 R32 R41 R42 | 4 | 240 1% | UNI-ROYAL 0603WAF2400T5E | OK |
| C25803 | R33 R43 | 2 | 100k | UNI-ROYAL 0603WAF1003T5E | OK |
| C22787 | R34 R44 | 2 | 120 1% | UNI-ROYAL 0603WAF1200T5E | OK |
| C21190 | R35 R45 | 2 | 1k | UNI-ROYAL 0603WAF1001T5E | OK |
| C22962 | R50 R51 | 2 | 220 | UNI-ROYAL 0603WAF2200T5E | OK |
| C227572 | R6 | 1 | 12.4k 1% | Yageo AC0603FR-0712K4L 12.4k 1% | OK |
| C22935 | R7 R12 | 2 | 1M | UNI-ROYAL 0603WAF1004T5E | OK |
| C2886898 | SW1 | 1 | BOOT | E-Switch TL3342F160QG | OK |
| C2886898 | SW2 | 1 | RESET | E-Switch TL3342F160QG | OK |
| C2913198 | U1 | 1 | ESP32-S3-WROOM-1-N8 | Espressif ESP32-S3-WROOM-1-N8 | OK* |
| C32843 | U2 | 1 | W5500 | WIZnet W5500 LQFP-48 | OK* |
| C48125 | U3 U4 | 2 | SN65HVD72DR | TI SN65HVD72DR | OK* |
| C6186 | U5 | 1 | AMS1117-3.3 | AMS1117-3.3 SOT-223 | OK* |
| C7519 | U6 | 1 | USBLC6-2SC6 | ST USBLC6-2SC6 | OK |
| C2842189 | Y1 | 1 | 25MHz | HCI XC32M4-25.000-F20NJDT 3225 25MHz 20pF | CHECK |

## Notes on specific lines

- **Pin headers (C2337)**: the BOM lists the five header positions (J5, J6, J2T, J3T, J7) as 5 parts, but they are all cut from a **single 1x40 strip** (21 pins used in total). Buy one strip; LCSC's minimum order may force you to buy 5.
- **Jumper shunts (C2689176)**: two 2.54 mm shunts for J2T / J3T are on the purchase list (not on `BOM_order.csv`, which lists board parts only). Buy a few extra.
- **PoE module (C5380091)**: the most expensive line (about $4-5.5). Stock was **22** when checked, which limits a first batch to a small number of boards. See [docs/08](08-ordering-guide.md) for alternatives.
- **HR871150C jack (C19724786)**: stock varied between 14 and 248 on different days; price about $1.24-1.60.
- **25 MHz crystal (C2842189, flagged CHECK)**: 3225, 20 pF load. The load capacitors C19 / C20 are 18 pF; with stray capacitance the load is close to 20 pF, but this has not been calculated for the actual layout.
- **220 uF capacitors (C32514)**: 6.3 x 5.4 mm, 6.3 V. They are on the 5 V rails with about 1.5 V of headroom to the rating. A 10 V part in the same case would be safer; none was found with matching footprint, so this is a rev2 item.
- **100 nF, 18 pF, 1 uF, green LED**: the original LCSC numbers were out of stock; the BOM uses in-stock alternatives (C1591, C107040, C29936 25 V X7R, C12065). The 1 uF capacitor is on the EN pin, so 25 V is enough.
- **Port LEDs** (D30, D40, green, forward voltage about 2.8 V) with 1 k series resistors from a 3.3 V GPIO will be **dim**. Swap R35 / R45 for 330 ohm (the 330 ohm value is already in the BOM for R2) if you want them brighter.

## Approximate cost (snapshot, 2026-11-11)

Single-unit LCSC prices for the main lines: ESP32-S3-WROOM-1-N8 about $3.15, DP9700-5V about $4.30-5.54 (depending on quantity), W5500 about $1.83, 2 x SN65HVD72DR about $1.95, HR871150C about $1.24-1.60, 4 x screw terminals about $0.63. These sum to about $14-15 per board before passives, the PCB, and shipping.

The LCSC BOM tool estimated **$25.09** for one board's cart, but that figure includes minimum-order quantities on the passives (for example 20 x 10 uF, 50 x 100 nF), so it overstates the per-board cost at volume. PCB fabrication and shipping are extra.
