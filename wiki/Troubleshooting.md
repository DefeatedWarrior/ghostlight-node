# 🛠️ Troubleshooting

## Power

| Symptom | Check |
|---|---|
| Board browns out or resets on USB | A 500 mA port is not enough with Wi-Fi + Ethernet. Use PoE or external 5 V ([[Power]]) |
| +5V reads 4.5-4.7 V | Normal: the SS14 drop |
| Hot AMS1117 | Normal at 0.5 A (about 0.5-0.7 W); check for shorts if it is far hotter |
| Two supplies fighting | PoE and J6 share `5V_EXT`; use only one |

## Flashing and boot

| Symptom | Check |
|---|---|
| Boot loop after flashing | Old `sdkconfig` still has PSRAM enabled: delete it, `idf.py fullclean` |
| Cannot enter download mode | Hold BOOT, tap RESET, release BOOT; use a data-capable USB cable |
| No console | UART0 is shared with J5 pins 4-5; use USB console if a daughterboard is fitted |

## Ethernet

| Symptom | Check |
|---|---|
| No link LED | Jack pin map, TX/RX pairs, magjack orientation |
| W5500 not detected | 25 MHz crystal, AVDD 3V3, SPI lines, RST/INT pull-ups |
| Link but no IP | Switch/DHCP; try static IP in the web UI |

## DMX

| Symptom | Check |
|---|---|
| Fixture does not respond | Swap A and B; check ground and termination |
| Flicker | Termination, cable quality, bias contention |
| Phantom RDM responses | Enable bias, check termination and idle differential |
| Port LEDs dim | 1 kΩ series resistor; use 330 Ω |
| Receive unreliable | DIR pin state, TVS orientation, bus idle level |

## PoE

| Symptom | Check |
|---|---|
| No power from PoE | Switch is 802.3af, PS1 orientation, 5V_EXT at C50 |
| Smoke or damage risk | Never use a passive 24/48 V injector without 802.3af detection |

Still stuck? Open an [issue](https://github.com/DefeatedWarrior/ghostlight-node/issues) with photos and measurements.
