# 15. Roadmap and ideas for rev2

## Fix first (from the first built board)

- Correct anything found in [docs/11](11-known-issues-and-verification-status.md) and [docs/10](10-bring-up-and-test.md): jack pin map, PoE orientation, W5500 analog network, DMX polarity and bias, LED currents.
- Run KiCad ERC in the GUI and clear the annotation warning.

## Cheap improvements

- **Test points** on +3V3, +5V, 5V_EXT, GND, DMX A / B and the W5500 SPI lines.
- **Port LED resistors** to 330 ohm so the LEDs are visible.
- **Bulk capacitors** to 10 V rating on the 5 V rails.
- **Enclosure drawing** and an XLR panel template.
- Consider **driving W5500 reset** and the **bias pins** from the firmware.

## Variants

- **PoE-optional** board: leave out the PS1 module and C50 (a BOM variant, same board).
- **Isolated DMX** variant using an isolated RS-485 transceiver and an isolated DC-DC, if ground loops between USB and the lighting rig are a problem.
- **XLR-5 panel** variant with the XLR connectors on a small daughterboard.

## Larger ideas

- **Port 3 / port 4 daughterboard** on J5 (transceiver on UART0, DIR3, BIAS3, LED3). If more than one extra port is wanted, an SPI-to-UART bridge (for example an SC16IS752 or MAX14830) on four of the J5 GPIOs could drive more ports, with polling instead of an interrupt line (there is no spare interrupt pin on J5 in rev1).
- **OLED display and a user button** on the J5 spare GPIOs for local configuration.
- **microSD slot** for show files (needs four SPI-capable pins, which is all of J5's spare GPIOs).
- **RTC with a coin cell** for scheduled playback.
