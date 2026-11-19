# 🧾 Bill of Materials

39 purchase lines, every part has an LCSC number. Files: `bom/BOM_order_purchase.csv` (LCSC part + qty per board) and `bom/BOM_order.csv` (with designators and status).

> [!NOTE]
> Stock and prices were last checked on **2026-11-11** and change daily. Re-import the purchase list before ordering.

## Main parts

| Part | LCSC | Approx. price |
|---|---|---|
| ESP32-S3-WROOM-1-N8 | C2913198 | USD 3.15 |
| SDAPO DP9700-5V PoE module | C5380091 | USD 4.30-5.54 |
| WIZnet W5500 | C32843 | USD 1.83 |
| 2 × SN65HVD72DR | C48125 | USD 1.95 |
| HR871150C magjack | C19724786 | USD 1.24-1.60 |
| 4 × KF128-5.08-3P terminals | C474953 | USD 0.63 |

These sum to about **USD 14-15 per board** before passives, PCB and shipping.

## Full list

| LCSC | Refs | Qty | Value / part |
|---|---|---|---|
| C15850 | C1 C6 C14 C18 | 4 | 10 µF 0805 |
| C21122 | C16 | 1 | 22 nF |
| C1779 | C17 | 1 | 4.7 µF 0805 |
| C107040 | C19 C20 | 2 | 18 pF NP0 |
| C1591 | C2 C4 C10-C13 C15 C21 C30 C40 | 10 | 100 nF |
| C1589 | C23 | 1 | 10 nF |
| C29936 | C3 | 1 | 1 µF 25 V |
| C32514 | C5 C50 | 2 | 220 µF 6.3 V 6.3×5.4 |
| C45783 | C7 | 1 | 22 µF 0805 |
| C2943053 | D1 D2 | 2 | SM712 TVS |
| C12065 | D30 D40 | 2 | LTST-C193TGKT-5A green LED |
| C2480 | D3 D4 D5 | 3 | SS14 |
| C22366107 | F1 | 1 | PTC 1.1 A |
| C19724786 | J1 | 1 | HR871150C |
| C474953 | J2 J2O J3 J3O | 4 | screw terminal 3P 5.08 |
| C165948 | J4 | 1 | USB-C |
| C2337 | J5 J6 J7 J2T J3T | 5 | pin header (one 1×40 strip) |
| C76892 | L1 | 1 | ferrite 120R |
| C114586 | LED1 | 1 | WS2812B |
| C5380091 | PS1 | 1 | DP9700-5V |
| C8545 | Q1 Q2 | 2 | 2N7002 |
| C25804 | R1 R5 R8-R11 R30 R40 | 8 | 10 k |
| C23138 | R2 | 1 | 330 |
| C23186 | R3 R4 | 2 | 5.1 k |
| C23350 | R31 R32 R41 R42 | 4 | 240 1 % |
| C25803 | R33 R43 | 2 | 100 k |
| C22787 | R34 R44 | 2 | 120 1 % |
| C21190 | R35 R45 | 2 | 1 k |
| C22962 | R50 R51 | 2 | 220 |
| C227572 | R6 | 1 | 12.4 k 1 % |
| C22935 | R7 R12 | 2 | 1 M |
| C2886898 | SW1 SW2 | 2 | TL3342 tactile |
| C2913198 | U1 | 1 | ESP32-S3-WROOM-1-N8 |
| C32843 | U2 | 1 | W5500 |
| C48125 | U3 U4 | 2 | SN65HVD72DR |
| C6186 | U5 | 1 | AMS1117-3.3 |
| C7519 | U6 | 1 | USBLC6-2SC6 |
| C2842189 | Y1 | 1 | 25 MHz 3225 20 pF (**check**) |

Also buy two 2.54 mm shunts (C2689176) for J2T/J3T.

## Notes

- **Headers:** all five header positions are cut from one 1×40 strip; LCSC's minimum may force buying five.
- **Port LEDs** with 1 kΩ will be dim; use 330 Ω for R35/R45 if you want them brighter.
- **220 µF caps** have about 1.5 V margin; a 10 V part would be safer ([[Roadmap]]).
- **Crystal:** 20 pF load with 18 pF caps, not calculated for this layout.
- **PoE-optional build:** skip PS1 and C50 to save about USD 4-5.5.
