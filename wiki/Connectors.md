# 🔩 Connectors

| Ref | Type | Purpose |
|---|---|---|
| J1 | RJ45 magjack | Ethernet / PoE |
| J2 / J2O | 3-pos 5.08 mm | DMX1 IN / OUT |
| J3 / J3O | 3-pos 5.08 mm | DMX2 IN / OUT |
| J2T / J3T | 1×2 header | 120 Ω termination shunts |
| J4 | USB-C | power, programming, console |
| J5 | 1×12 header | expansion |
| J6 | 1×2 header | external 5 V (pin 1 `5V_EXT`, pin 2 GND) |
| J7 | 1×3 header | UART0 debug (GND, TX, RX) |
| SW1 / SW2 | tactile | BOOT / RESET |

DMX terminals, left to right: **B, A, GND**.

## J5 expansion header

| Pin | Signal | Note |
|---|---|---|
| 1 | +3V3 | |
| 2 | +5V | about 4.5-4.7 V, not regulated 5 V |
| 3 | GND | |
| 4 | UART0_TX (GPIO43) | shared with J7 |
| 5 | UART0_RX (GPIO44) | shared with J7 |
| 6 | DIR3 (GPIO21) | 10 k pull-down on board |
| 7 | BIAS3 (GPIO14) | |
| 8 | LED_P3 (GPIO7) | |
| 9-12 | EXP1-4 (GPIO38, 41, 42, 47) | spare |

A third-port daughterboard (transceiver on UART0 + DIR3, BIAS3, LED3) fits here. UART0 is also the J7 console, so use **USB** as the console when a third port is fitted.
