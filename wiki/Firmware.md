# 💾 Firmware

The firmware lives in [`firmware/`](https://github.com/DefeatedWarrior/ghostlight-node/tree/main/firmware). It uses ESP-IDF v5.2.6 and the MIT licence, and started as **ESP-NODE-2RDM** by ThinhCNTT22. It still calls itself `ESP-NODE-2RDM` in places.

> [!WARNING]
> The rev1 build compiles with no warnings, and CI builds it on every change, but **it has not been run on a Ghostlight board yet**. The same firmware runs on the N16R8 dev-board prototype.

## Build and flash

```bash
cd firmware
tools/build.sh ghostlight-rev1                          # build
tools/build.sh ghostlight-rev1 -p /dev/ttyACM0 flash monitor
```

`tools/build.sh` loads ESP-IDF itself if `~/esp/esp-idf` holds v5.2.6; otherwise run `. $IDF_PATH/export.sh` first. Plain `idf.py build` builds rev1 too. If you have an `sdkconfig` left over from an older firmware, delete it first, because it keeps its old settings.

To enter download mode over USB-C, hold **BOOT**, tap **RESET**, then release BOOT.

## Boards

| `tools/build.sh …` | Hardware | Flash / PSRAM |
|---|---|---|
| `ghostlight-rev1` | this board (ESP32-S3-WROOM-1-N8) | 8 MB / none |
| `esp-node-2rdm` | ESP32-S3 N16R8 dev-board prototype | 16 MB / 8 MB |
| `esp32-devkitc` | original ESP32 DevKitC + W5500 + 2 transceivers (never run) | 4 MB / none |

Each board has its own partition table. Flashing a build made for a different board erases the stored settings and scenes.

## What rev1 uses

| Signal | GPIO | Firmware |
|---|---|---|
| DMX 1 / 2 TX, RX, DIR | 17 / 15, 16 / 18, 39 / 40 | UART1 / UART2 |
| DMX bias switches | 1 / 2 | low at boot, high while the port is an output or RDM controller |
| Port LEDs | 5 / 6 | off = disabled, slow blink = no data, on = data, fast blink = identify / test |
| W5500 (SPI2) | SCK 12, MOSI 11, MISO 13, CS 10, INT 9 | Ethernet |
| W5500 reset | 4 | hardware reset when the driver starts |
| Status LED | 48 | WS2812 |
| BOOT button | 0 | hold 10 s to factory reset |

### Partition table (8 MB, `partitions_8mb.csv`)

| Name | Type | Offset | Size |
|---|---|---|---|
| nvs | data | 0x9000 | 0x5000 |
| otadata | data | 0xe000 | 0x2000 |
| phy_init | data | 0x10000 | 0x1000 |
| ota_0 | app | 0x20000 | 0x1A0000 |
| ota_1 | app | 0x1C0000 | 0x1A0000 |
| littlefs | data | 0x360000 | 0x400000 |
| coredump | data | 0x760000 | 0x10000 |

The app is about 1.11 MB, which is 68 % of each 1.625 MB slot.

## Feature switches

Under **menuconfig → ESP-NODE → Features** (`tools/build.sh ghostlight-rev1 menuconfig`) you can switch off sACN, RDM, scenes, DMX tools, the web log, mDNS or Ethernet. All of them are on by default.

## Memory

With no PSRAM everything runs from the 512 KB internal SRAM, about half of which is used statically. Watch `heap_caps_get_free_size()` during an Art-Net/sACN burst with Wi-Fi, Ethernet and the web UI active.

More: [`firmware/docs/DEVELOPING.md`](https://github.com/DefeatedWarrior/ghostlight-node/blob/main/firmware/docs/DEVELOPING.md) and [`docs/13-firmware-integration.md`](https://github.com/DefeatedWarrior/ghostlight-node/blob/main/docs/13-firmware-integration.md).
