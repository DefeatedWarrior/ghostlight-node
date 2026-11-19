# 💾 Firmware

The firmware lives in [`firmware/`](https://github.com/DefeatedWarrior/ghostlight-node/tree/main/firmware): ESP-IDF v5.2.6, MIT licence, originally **ESP-NODE-2RDM** by ThinhCNTT22. It still identifies the board as `ESP-NODE-2RDM`.

> [!WARNING]
> The N8 changes are applied but **not built or run on hardware yet** (no ESP-IDF was available when they were made).

## What changed for the N8 module

| File | Change |
|---|---|
| `sdkconfig.defaults` | 8 MB flash, PSRAM options removed |
| `partitions.csv` | 8 MB layout (below) |
| `components/board/include/board.h` | `BOARD_PORT_LED_GPIO { 5, 6 }`, plus unused `BOARD_DMX_BIAS_GPIO { 1, 2 }` and `BOARD_W5500_RST_GPIO 4` |

### Partition table (8 MB)

| Name | Type | Offset | Size |
|---|---|---|---|
| nvs | data | 0x9000 | 0x5000 |
| otadata | data | 0xe000 | 0x2000 |
| phy_init | data | 0x10000 | 0x1000 |
| ota_0 | app | 0x20000 | 0x1A0000 |
| ota_1 | app | 0x1C0000 | 0x1A0000 |
| littlefs | data | 0x360000 | 0x400000 |
| coredump | data | 0x760000 | 0x10000 |

Ends at 0x770000. Checked for overlaps and 64 KB app alignment only. The app is about 1.1 MB, so each 1.6 MB slot has headroom.

## Build and flash

```bash
. $IDF_PATH/export.sh
cd firmware
rm -f sdkconfig sdkconfig.old     # drop old 16 MB / PSRAM settings
idf.py set-target esp32s3
idf.py fullclean
idf.py build
idf.py -p /dev/ttyACM0 flash monitor
```

On the board, hold **BOOT**, tap **RESET**, release BOOT to enter download mode over USB-C.

## Not used by the firmware yet

- **W5500 hardware reset (GPIO4):** the driver has `reset_gpio_num = -1`. Setting it to 4 allows a hardware reset after faults.
- **DMX bias switches (GPIO1/2):** not driven, so bias is off.

## Memory

With no PSRAM everything runs from the 512 KB internal SRAM. The diagnostic log ring falls back to internal RAM automatically. Watch `heap_caps_get_free_size()` during an Art-Net/sACN burst with Wi-Fi, Ethernet and the web UI active.

More: [`docs/13-firmware-integration.md`](https://github.com/DefeatedWarrior/ghostlight-node/blob/main/docs/13-firmware-integration.md).
