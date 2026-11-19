# Troubleshooting

| Symptom | Check |
|---|---|
| Boot loop after flashing | Old `sdkconfig` still has PSRAM enabled: delete it and run `idf.py fullclean` |
| No Ethernet link | W5500 3V3 and SPI lines, jack orientation, W5500_RST pull-up |
| Fixture flickers or is dead | A/B swapped, termination, ground |
| Phantom RDM responses | Bias/termination on an idle line, cable quality |
| PoE does not power up | Switch/injector is 802.3af, DP9700 orientation, 5V_EXT feed |
| Port LEDs dim | 1 kΩ series resistor; 330 Ω is suggested for rev2 |
| Cannot flash | Hold BOOT while pressing RESET, check USB cable carries data |

Known hardware issues: `docs/11-known-issues-and-verification-status.md`.
