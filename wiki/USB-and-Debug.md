# 🔌 USB and Debug

## USB-C (J4)

- USB 2.0 full-speed **device** using the ESP32-S3 native USB (D− GPIO19, D+ GPIO20). No bridge chip.
- 5.1 kΩ on CC1/CC2, USBLC6-2SC6 ESD array, 1.1 A PTC and an SS14 into `+5V`.

## Programming

1. **Native USB:** hold **BOOT** (SW1), tap **RESET** (SW2), release BOOT. The chip appears in download mode; use `idf.py flash` or `esptool.py`.
2. **UART0 (J7):** with a 3.3 V USB-UART adapter if native USB is unavailable.

## Console options

| Option | Pins | Notes |
|---|---|---|
| J7 | GPIO43 TX / GPIO44 RX, 3 pins GND/TX/RX | 3.3 V logic only, 115200 |
| USB-C | native USB | needed if a third port uses J5 (shares UART0) |

Connect the adapter **crossed** (adapter RX to J7 TX). Never connect an adapter's 5 V line.

## Buttons

| Control | Effect |
|---|---|
| RESET (SW2) | pulls EN low |
| BOOT (SW1) | pulls GPIO0 low; hold through reset for download mode |
