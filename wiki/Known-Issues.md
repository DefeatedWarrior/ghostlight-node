# ⚠️ Known Issues

rev1 is **not built or tested**. This page separates what was checked from what was inferred.

## ✅ Verified

| Check | Result |
|---|---|
| KiCad DRC (7.0.11) | 0 clearance errors, 0 unconnected, 0 shorts; silkscreen warnings and one library-footprint mismatch (U1) only |
| PCB vs schematic nets | 72 nets each, no mismatches |
| Gerbers | exported from the final board and compared |
| GPIO map vs firmware | DMX UARTs and pins, W5500 SPI, status LED and BOOT match `board.h` / `network_manager.c` |
| SN65HVD72 fail-safe | open, short and idle per the TI datasheet |
| LCSC numbers | all 39 lines matched on 2026-11-11 |

## ❓ Not verified

### Electrical

1. **No ERC was run** (KiCad 7 CLI has none). Run it in the GUI; an "annotation errors" warning on export was not investigated.
2. **W5500 analog network** inferred from the WIZnet reference design.
3. **W5500 LED drive**: about 6 mA each, rating not checked.
4. **DMX A/B polarity** and edge behaviour need a scope or known-good fixture.
5. **Bias values (240 Ω)** not checked against E1.20.
6. **Crystal load** not calculated for this layout.
7. **USB-only power** is marginal ([[Power]]).
8. **5 V rails** use 6.3 V electrolytics with ~1.5 V margin.

### Mechanical

9. **HR871150C pin map** decoded from a datasheet drawing.
10. **DP9700 body orientation** unconfirmed.
11. **TL3342 switch** and **220 µF cap** footprints matched by size only.
12. **No test points.**
13. **No enclosure drawing**; mounting hole H3 sits close to the RJ45 and PoE module.

### Layout

14. Ethernet pairs run about 35-45 mm and `5V_EXT` about 65 mm; fine on paper, not prototyped. Routed with Freerouting 1.9.0 (not reproducible bit-for-bit).
15. 8 silkscreen warnings (appearance only).
16. No SMT assembly flow tested.

### Firmware

17. rev1 firmware **builds cleanly** but has **not been run** on a board.
18. Port LEDs, DMX bias switches and W5500 reset are driven by the firmware (not checked on hardware).
19. UART0 is shared by J7 and J5 pins 4-5.

Full detail: [`docs/11`](https://github.com/DefeatedWarrior/ghostlight-node/blob/main/docs/11-known-issues-and-verification-status.md).
