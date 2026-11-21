# 13. Firmware integration

The firmware lives in its own repository, [ghostlight-node-firmware](https://github.com/DefeatedWarrior/ghostlight-node-firmware) (ESP-IDF 5.2.6). This page lists what the rev1 hardware needs from it.

> **Status:** everything below is done. rev1 has its own board profile: settings in `boards/ghostlight-rev1/sdkconfig.defaults`, pins in `components/board/include/boards/ghostlight_rev1.h`, partition table `partitions_8mb.csv` (paths in the firmware repository). Build and flash with `tools/build.sh ghostlight-rev1 -p PORT flash monitor` (plain `idf.py build` builds rev1 too). It builds with no warnings and the app fits its slot with 32 % to spare, but **it has not been run on a Ghostlight board yet**. See [`docs/DEVELOPING.md`](https://github.com/DefeatedWarrior/ghostlight-node-firmware/blob/main/docs/DEVELOPING.md) for the other boards and the build-time feature switches.

## 1. N16R8 to N8 module (done: board profile)

The original firmware assumed 16 MB flash and 8 MB octal PSRAM. The N8 module has 8 MB quad flash and **no PSRAM**.

In `sdkconfig.defaults`:

```
# replace
CONFIG_ESPTOOLPY_FLASHSIZE_16MB=y
# with
CONFIG_ESPTOOLPY_FLASHSIZE_8MB=y

# remove these (no PSRAM on the N8: with SPIRAM_BOOT_INIT enabled the boot fails)
CONFIG_SPIRAM=y
CONFIG_SPIRAM_MODE_OCT=y
CONFIG_SPIRAM_SPEED_80M=y
CONFIG_SPIRAM_BOOT_INIT=y
CONFIG_SPIRAM_MALLOC_RESERVE_INTERNAL=32768
```

Delete `sdkconfig` (or run `idf.py fullclean` and regenerate) after editing the defaults, because the existing generated `sdkconfig` keeps the old values. `CONFIG_ESPTOOLPY_FLASHMODE_DIO` and 80 MHz flash can stay.

The firmware allocates its diagnostic log ring from PSRAM with a fallback to internal RAM (`components/diag/diag.c`), so no code change is required for that, but check heap use with the larger buffers (Art-Net / sACN receive buffers, web UI) once PSRAM is gone.

## 2. Partition table for 8 MB (done: `partitions_8mb.csv`)

The original 16 MB `partitions.csv` ends at 0x830000, which is past the end of an 8 MB (0x800000) flash. A layout that fits, with two app slots (rollback OTA), LittleFS and a core dump area:

```
# Name,     Type, SubType,  Offset,    Size
nvs,        data, nvs,      0x9000,    0x5000
otadata,    data, ota,      0xe000,    0x2000
phy_init,   data, phy,      0x10000,   0x1000
ota_0,      app,  ota_0,    0x20000,   0x1A0000
ota_1,      app,  ota_1,    0x1C0000,  0x1A0000
littlefs,   data, spiffs,   0x360000,  0x400000
coredump,   data, coredump, 0x760000,  0x10000
```

Each app slot is 1.625 MB, which leaves about 0.5 MB of headroom over a 1.1 MB application. LittleFS gets 4 MB and the table ends at 0x770000, under the 0x800000 limit. The firmware builds with this table (the app is about 1.11 MB, 68 % of a slot); adjust the slot sizes if the application grows.

## 3. Pin definitions (done: `boards/ghostlight_rev1.h`)

The existing DMX and W5500 pins already match the hardware. Port LEDs and the new signals need updates:

```c
#define BOARD_NAME              "ESP-NODE-2RDM"   /* existing firmware identifier; the product is the Ghostlight Node */
#define BOARD_DMX_PORTS         2

/*                               port 1  port 2 */
#define BOARD_DMX_UART          { 1,      2  }
#define BOARD_DMX_TX_GPIO       { 17,     15 }
#define BOARD_DMX_RX_GPIO       { 16,     18 }
#define BOARD_DMX_DIR_GPIO      { 39,     40 }   /* driver enable, receiver disable */

#define BOARD_DMX_BIAS_GPIO     { 1,      2  }   /* NEW: bias switch, active high */
#define BOARD_PORT_LED_GPIO     { 5,      6  }   /* was { -1, -1 } */

#define BOARD_STATUS_LED_GPIO   48               /* WS2812 */
#define BOARD_RESET_BUTTON_GPIO 0                /* BOOT, active low */

#define BOARD_W5500_RST_GPIO    4                /* NEW (named BOARD_ETH_RST_GPIO in the firmware) */
```

In the board profile the W5500 reset is named `BOARD_ETH_RST_GPIO`. The firmware drives the bias pins **low during boot** and sets them high only while the port is an output or RDM controller (the controller biases the line, as E1.20 expects).

## 4. W5500 hardware reset (done)

`network_manager.c` passes the board's `BOARD_ETH_RST_GPIO` (GPIO4 on rev1, with a pull-up) to the W5500 driver as `reset_gpio_num`, so the driver resets the chip in hardware when it starts.

## 5. Console

| Use | Pins |
|---|---|
| UART0 debug console | J7 (GPIO43 TX / GPIO44 RX) |
| USB console | native USB (USB-Serial-JTAG or CDC) |
| Third DMX port on J5 | uses UART0 (GPIO43 / 44); switch the console to USB (`CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG=y`) |

## 6. Memory and Wi-Fi/Ethernet

With no PSRAM, the whole firmware runs from the ESP32-S3's 512 KB internal SRAM. Check `heap_caps_get_free_size()` during an Art-Net / sACN burst with Wi-Fi and Ethernet both active and the web UI open.
