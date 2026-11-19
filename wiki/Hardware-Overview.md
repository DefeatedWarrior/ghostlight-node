# 🔧 Hardware Overview

<img src="https://raw.githubusercontent.com/DefeatedWarrior/ghostlight-node/main/docs/images/board-front.png" width="560" alt="front">

## Block diagram

```mermaid
flowchart TB
  subgraph Power
    USB[USB-C VBUS] --> PTC[PTC 1.1 A] --> D3[SS14]
    POE[RJ45 PoE] --> PS1[DP9700-5V] --> V5X[5V_EXT]
    J6[J6 5 V header] --> V5X
    V5X --> D4[SS14]
    D3 --> V5[+5V rail]
    D4 --> V5
    V5 --> LDO[AMS1117-3.3] --> V33[+3V3]
  end
  subgraph Logic
    MCU[ESP32-S3-WROOM-1-N8]
    ETH[W5500]
    MCU <-- SPI --> ETH
  end
  ETH <--> MAG[HR871150C magjack]
  MCU -- UART1 --> T1[SN65HVD72 #1] --> P1[DMX1 IN/OUT]
  MCU -- UART2 --> T2[SN65HVD72 #2] --> P2[DMX2 IN/OUT]
  MCU -- GPIO48 --> LED[WS2812B]
  MCU <-- native USB --> USBC[USB-C]
```

## Main parts

| Block | Part | Ref |
|---|---|---|
| MCU | ESP32-S3-WROOM-1-N8 | U1 |
| Ethernet | W5500, 25 MHz crystal | U2, Y1 |
| Jack | Hanrun HR871150C | J1 |
| PoE | SDAPO DP9700-5V | PS1 |
| DMX transceivers | SN65HVD72DR | U3, U4 |
| DMX TVS | SM712 | D1, D2 |
| 3.3 V regulator | AMS1117-3.3 | U5 |
| USB ESD | USBLC6-2SC6 | U6 |
| Status LED | WS2812B | LED1 |

## Board layout

| Front | Back (silkscreen, mirrored) |
|---|---|
| <img src="https://raw.githubusercontent.com/DefeatedWarrior/ghostlight-node/main/docs/images/board-front.png" width="320"> | <img src="https://raw.githubusercontent.com/DefeatedWarrior/ghostlight-node/main/docs/images/board-back.png" width="320"> |

The back silkscreen carries the GPIO map, licence and revision.

## Design choices

- **Hand assembly:** 0603/0805 passives, SOIC-8, LQFP-48. No BGA, no fine-pitch QFN.
- **Cost:** the N8 module (no PSRAM) and a single-chip PoE module keep the BOM small.
- **IN and OUT per port:** two terminals in parallel on one transceiver for daisy chaining.
- **Expansion:** header J5 for a third port or other add-ons.

More detail: [`docs/12-pcb-design-notes.md`](https://github.com/DefeatedWarrior/ghostlight-node/blob/main/docs/12-pcb-design-notes.md).
