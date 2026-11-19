# 6. USB, programming and debug

## USB-C (J4)

- USB 2.0 full-speed device (sink). The ESP32-S3 uses its native USB peripheral (D- on GPIO19, D+ on GPIO20), so no USB-UART bridge chip is fitted.
- CC1 and CC2 have 5.1 k pull-downs (R3, R4), so a USB-C host or charger will supply the default 5 V.
- D+ / D- go through a USBLC6-2SC6 ESD array (U6) with its VBUS pin tied to VBUS.
- VBUS goes through a 1.1 A resettable fuse (F1, BORN SMD1206-110/6N) and a Schottky diode (D3) into the +5V rail. The diode stops the board from back-feeding VBUS when powered from PoE or J6.
- Reminder: the USB-only current budget is marginal; see [docs/02](02-architecture-and-power.md).

## Programming the firmware

Two ways in:

1. **Native USB**: hold BOOT (SW1, GPIO0), tap RESET (SW2), release BOOT. The chip enumerates as a USB device in download mode and `esptool.py` / ESP-IDF `idf.py flash` can program it. After the first flash the same USB port can also provide a USB-Serial-JTAG console or a CDC console, depending on firmware configuration.
2. **UART0** (J7) with a 3.3 V USB-UART adapter, if native USB is unavailable.

Both paths need GPIO0 low at reset; BOOT does that.

## Debug console

| Option | Pins | Notes |
|---|---|---|
| UART0 header J7 | GPIO43 (TX) / GPIO44 (RX), pins GND / TX / RX | 3.3 V logic only, 115200 by default |
| USB-C | native USB | Needed if a third DMX port is attached to J5, because J5 also uses UART0 |

Connect the adapter **crossed**: adapter RX to J7 TX, adapter TX to J7 RX, adapter GND to J7 GND. Never connect an adapter's 5 V line.

## Reset and boot

| Control | Effect |
|---|---|
| RESET (SW2) | pulls EN low; EN has a 10 k pull-up (R1) and 1 uF (C3) for the power-on delay |
| BOOT (SW1) | pulls GPIO0 low; hold it through a reset to enter download mode |
