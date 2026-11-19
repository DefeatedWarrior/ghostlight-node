# 3. Pin map and connectors

The GPIO assignments below are taken from the board source (`tools/generator/design.py`) and match the firmware's `board.h` for the DMX ports and the W5500. Module pin numbers are the pin numbers of the ESP32-S3-WROOM-1 module.

## GPIO assignments

| GPIO | Module pin | Net | Function |
|---|---|---|---|
| 0 | 27 | BOOT | BOOT button (to GND), strapping pin |
| 1 | 39 | BIAS1 | DMX1 bias switch (2N7002 gate, active high) |
| 2 | 38 | BIAS2 | DMX2 bias switch (active high) |
| 4 | 4 | W5500_RST | W5500 reset (10 k pull-up to 3V3) |
| 5 | 5 | LED_P1 | DMX1 port LED (through 1 k) |
| 6 | 6 | LED_P2 | DMX2 port LED (through 1 k) |
| 7 | 7 | LED_P3 | J5 pin 8, third port LED |
| 9 | 17 | W5500_INT | W5500 interrupt (10 k pull-up) |
| 10 | 18 | W5500_CS | W5500 chip select (10 k pull-up) |
| 11 | 19 | W5500_MOSI | SPI MOSI |
| 12 | 20 | W5500_SCK | SPI clock |
| 13 | 21 | W5500_MISO | SPI MISO |
| 14 | 22 | BIAS3 | J5 pin 7, third port bias |
| 15 | 8 | DMX2_TX | UART2 TX |
| 16 | 9 | DMX1_RX | UART1 RX |
| 17 | 10 | DMX1_TX | UART1 TX |
| 18 | 11 | DMX2_RX | UART2 RX |
| 19 | 13 | USB_DM | USB D- |
| 20 | 14 | USB_DP | USB D+ |
| 21 | 23 | DIR3 | J5 pin 6, third port direction (10 k pull-down R5) |
| 38 | 31 | EXP1 | J5 pin 9 |
| 39 | 32 | DMX1_DIR | DMX1 driver enable / receiver disable (10 k pull-down) |
| 40 | 33 | DMX2_DIR | DMX2 driver enable (10 k pull-down) |
| 41 | 34 | EXP2 | J5 pin 10 |
| 42 | 35 | EXP3 | J5 pin 11 |
| 43 | 37 | UART0_TX | J7 pin 2 and J5 pin 4 |
| 44 | 36 | UART0_RX | J7 pin 3 and J5 pin 5 |
| 47 | 24 | EXP4 | J5 pin 12 |
| 48 | 25 | LED_STATUS | WS2812B status LED data (through 330 ohm) |
| EN | 3 | EN | RESET button, 10 k pull-up, 1 uF to GND |

Not connected: GPIO 3, 8, 35, 36, 37, 45, 46 and the flash-reserved GPIO 26-34 on the module. GPIO 35-37 are free on the N8 (no PSRAM) but are not routed anywhere. The strapping pins GPIO0 (BOOT) and EN are the only strapping pins used.

## Connectors

### J1: RJ45 (HR871150C, PoE-capable magjack)

Right-angle through-hole jack with integrated magnetics, link and activity LEDs, and the four PoE centre taps brought out as pins. The jack overhangs the board edge by about 0.5 mm. See [docs/04](04-ethernet-and-poe.md).

### J2, J2O, J3, J3O: DMX terminals (3-pos, 5.08 mm)

| Ref | Port | Role |
|---|---|---|
| J2 | DMX1 | IN |
| J2O | DMX1 | OUT (wired in parallel with J2) |
| J3 | DMX2 | IN |
| J3O | DMX2 | OUT (wired in parallel with J3) |

Pins left to right (as silkscreened): **B, A, GND**.

IN and OUT on a port are the same electrical bus on the same transceiver, so a port is either an output or an input for the whole port at a time, and the OUT terminal just provides a second place to attach a cable (daisy chain).

### J2T, J3T: termination jumpers (1x2 header)

Fit a 2.54 mm shunt to connect a 120 ohm terminator across A and B of that port. Fit it only at the **last device** on a DMX line.

### J4: USB-C

Device (sink) only, USB 2.0. CC1 and CC2 each have a 5.1 k pull-down (R3, R4). The connector is 16-pin (HRO TYPE-C-31-M-12), USB D+ / D- are tied across both rows.

### J5: expansion header (1x12, 2.54 mm)

| Pin | Signal | Note |
|---|---|---|
| 1 | +3V3 | |
| 2 | +5V | rail after the input diode (about 4.5-4.7 V), not a regulated 5 V |
| 3 | GND | |
| 4 | UART0_TX (GPIO43) | shared with the J7 console |
| 5 | UART0_RX (GPIO44) | shared with the J7 console |
| 6 | DIR3 (GPIO21) | 10 k pull-down on the board |
| 7 | BIAS3 (GPIO14) | |
| 8 | LED_P3 (GPIO7) | |
| 9 | EXP1 (GPIO38) | |
| 10 | EXP2 (GPIO41) | |
| 11 | EXP3 (GPIO42) | |
| 12 | EXP4 (GPIO47) | |

The header was designed so a third-port daughterboard (transceiver on UART0, direction, bias, LED) can be attached. **UART0 is also the debug console on J7, so port 3 and the J7 console cannot both be used**; use the USB-C port as the console when a third port is fitted (see [docs/06](06-usb-programming-debug.md)).

### J6: 5 V input (1x2 header)

Pin 1 `5V_EXT`, pin 2 `GND`. Pin 1 is also connected to the PoE module output. See the warning in [docs/02](02-architecture-and-power.md).

### J7: debug UART0 (1x3 header)

Pin 1 GND, pin 2 TX (ESP TX, connect to the adapter's RX), pin 3 RX (ESP RX, connect to the adapter's TX). 3.3 V logic only.

### Buttons and LEDs

| Ref | Function |
|---|---|
| SW1 | BOOT (GPIO0) |
| SW2 | RESET (EN) |
| LED1 | WS2812B status (GPIO48) |
| D30, D40 | Port 1 and port 2 activity LEDs (green, 0603) |
| J1 LEDs | Link (green) and activity (yellow) in the RJ45 jack |
