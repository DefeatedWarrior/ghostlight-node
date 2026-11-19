# Pin Map

| GPIO | Net | Function |
|---|---|---|
| 0 | BOOT | BOOT button (strapping) |
| 1 / 2 | BIAS1 / BIAS2 | DMX bias switches, active high |
| 4 | W5500_RST | W5500 reset |
| 5 / 6 | LED_P1 / LED_P2 | Port LEDs |
| 9 | W5500_INT | W5500 interrupt |
| 10 / 11 / 12 / 13 | CS / MOSI / SCK / MISO | W5500 SPI |
| 16 / 17 | DMX1 RX / TX | UART1 |
| 15 / 18 | DMX2 TX / RX | UART2 |
| 39 / 40 | DMX1_DIR / DMX2_DIR | Driver enable |
| 19 / 20 | USB D- / D+ | Native USB |
| 43 / 44 | UART0 TX / RX | J7 debug and J5 |
| 48 | LED_STATUS | WS2812B |
| 7, 14, 21, 38, 41, 42, 47 | | J5 expansion (see `docs/03`) |

Full table with module pin numbers: `docs/03-pinout-and-connectors.md`.
