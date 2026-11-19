# Hardware Overview

| Block | Part |
|---|---|
| MCU | ESP32-S3-WROOM-1-N8 (8 MB flash, no PSRAM) |
| Ethernet | W5500 over SPI, HR871150C PoE magjack |
| PoE | SDAPO DP9700-5V isolated module, 5 V / 2 A |
| DMX | 2 × SN65HVD72 RS-485 transceiver, SM712 TVS per port |
| USB | USB-C device, USBLC6 ESD, 1.1 A PTC |
| LEDs | WS2812B status, one LED per DMX port, jack link/activity |
| Board | 100 × 100 mm, 2 layers, four M3 holes |

Power sources (USB, external 5 V, PoE) are diode-OR'd onto the 5 V rail. See `docs/02-architecture-and-power.md`.

Connectors: **J1** RJ45, **J2/J2O** DMX1 IN/OUT, **J3/J3O** DMX2 IN/OUT, **J5** 12-pin expansion, **J7** UART0 debug, plus USB-C.
