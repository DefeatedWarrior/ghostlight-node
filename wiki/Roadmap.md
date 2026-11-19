# 🗺️ Roadmap

## Fix first (from the first built board)

- Anything found in [[Known Issues]] and [[Bring-up Checklist]]: jack pin map, PoE orientation, W5500 analog network, DMX polarity and bias, LED currents.
- Run KiCad ERC in the GUI and clear the annotation warning.

## Cheap improvements

- Test points on +3V3, +5V, 5V_EXT, GND, DMX A/B and the W5500 SPI lines
- Port LED resistors to 330 Ω
- 10 V bulk capacitors on the 5 V rails
- Enclosure drawing and XLR panel template
- Drive W5500 reset and bias pins from firmware

## Variants

- PoE-optional BOM (no PS1 / C50)
- Isolated DMX with an isolated transceiver and DC-DC
- XLR-5 panel variant with a small daughterboard

## Larger ideas

- Port 3 / 4 daughterboard on J5, possibly via an SPI-to-UART bridge (SC16IS752, MAX14830)
- OLED display and user button on spare GPIOs
- microSD slot for show files
- RTC with coin cell for scheduled playback
