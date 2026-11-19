# 📍 Pin Map

Module pin numbers are those of the ESP32-S3-WROOM-1.

| GPIO | Pin | Net | Function |
|---|---|---|---|
| 0 | 27 | BOOT | BOOT button (strapping) |
| 1 | 39 | BIAS1 | DMX1 bias switch, active high |
| 2 | 38 | BIAS2 | DMX2 bias switch, active high |
| 4 | 4 | W5500_RST | W5500 reset (10 k pull-up) |
| 5 | 5 | LED_P1 | DMX1 port LED |
| 6 | 6 | LED_P2 | DMX2 port LED |
| 7 | 7 | LED_P3 | J5 pin 8 |
| 9 | 17 | W5500_INT | W5500 interrupt |
| 10 | 18 | W5500_CS | SPI chip select |
| 11 | 19 | W5500_MOSI | SPI MOSI |
| 12 | 20 | W5500_SCK | SPI clock |
| 13 | 21 | W5500_MISO | SPI MISO |
| 14 | 22 | BIAS3 | J5 pin 7 |
| 15 | 8 | DMX2_TX | UART2 TX |
| 16 | 9 | DMX1_RX | UART1 RX |
| 17 | 10 | DMX1_TX | UART1 TX |
| 18 | 11 | DMX2_RX | UART2 RX |
| 19 / 20 | 13 / 14 | USB D− / D+ | native USB |
| 21 | 23 | DIR3 | J5 pin 6 (10 k pull-down) |
| 38 | 31 | EXP1 | J5 pin 9 |
| 39 | 32 | DMX1_DIR | driver enable |
| 40 | 33 | DMX2_DIR | driver enable |
| 41 | 34 | EXP2 | J5 pin 10 |
| 42 | 35 | EXP3 | J5 pin 11 |
| 43 | 37 | UART0_TX | J7 pin 2, J5 pin 4 |
| 44 | 36 | UART0_RX | J7 pin 3, J5 pin 5 |
| 47 | 24 | EXP4 | J5 pin 12 |
| 48 | 25 | LED_STATUS | WS2812B data (330 Ω) |
| EN | 3 | EN | RESET button |

Not connected: GPIO 3, 8, 35, 36, 37, 45, 46 and the flash-reserved GPIO 26-34.
