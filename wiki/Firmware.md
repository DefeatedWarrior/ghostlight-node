# Firmware

The firmware is in `firmware/` (ESP-IDF, MIT). It is the ESP-NODE-2RDM firmware with N8 changes applied:

- 8 MB flash, PSRAM disabled (`sdkconfig.defaults`)
- 8 MB partition table: two 1.6 MB OTA slots, 4 MB LittleFS, core dump (`partitions.csv`)
- Port LEDs on GPIO5/6 (`board.h`)

**Not built or run yet.** Before building:

```
rm sdkconfig sdkconfig.old     # drop old 16 MB / PSRAM settings
idf.py set-target esp32s3
idf.py fullclean
idf.py build flash monitor
```

Not yet used by the firmware: W5500 hardware reset (GPIO4) and DMX bias switches (GPIO1/2). Details: `docs/13-firmware-integration.md`.
