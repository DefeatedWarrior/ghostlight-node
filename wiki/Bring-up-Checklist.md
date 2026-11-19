# ✅ Bring-up Checklist

```mermaid
flowchart LR
  A[0 Unpowered checks] --> B[1 USB power] --> C[2 Flash + console] --> D[3 Ethernet] --> E[4 DMX] --> F[5 PoE]
```

**Stop at the first failure.** Use a current-limited bench supply if you have one. **Never connect PoE first.**

## 0. Before power

- [ ] +5V to GND: not a short
- [ ] +3V3 to GND: not a short
- [ ] CC1/CC2 to GND: about 5.1 kΩ each
- [ ] D3, D4, D5 cathodes toward +5V

## 1. USB power only (limit ~300 mA first)

- [ ] +5V about 4.5-4.7 V
- [ ] +3V3 3.3 V ± 5 %
- [ ] Current well under 100 mA with nothing flashed
- [ ] Nothing too hot in the first minute (U5 may be warm)

## 2. Flash and console

- [ ] BOOT + RESET gives a USB device; firmware flashes
- [ ] ESP32 boots, status LED responds

## 3. Ethernet

- [ ] Jack link/activity LEDs light, node gets an IP
- [ ] Ping works; Art-Net/sACN received
- [ ] If W5500 not detected: 25 MHz crystal, AVDD 3V3, SPI lines, RST/INT pull-ups, analog network vs WIZnet reference

## 4. DMX

- [ ] A/B at 250 kbaud with correct break and mark-after-break
- [ ] RX quiet when idle and DIR low
- [ ] **A/B polarity** checked with a known-good fixture
- [ ] Bias on: idle differential above 200 mV on a terminated line, no phantom RDM responses
- [ ] About 120 Ω across A-B with the jumper fitted
- [ ] Both ports, IN and OUT terminals each tested

## 5. PoE (last)

- [ ] Module orientation and 5V_EXT voltage checked before loading
- [ ] USB disconnected, 802.3af port powers and boots the board
- [ ] Rails OK under load (Wi-Fi + Ethernet + both DMX ports)
- [ ] USB plugged in at the same time: nothing back-feeds

## 📝 Record results

Open an [issue](https://github.com/DefeatedWarrior/ghostlight-node/issues) with scope screenshots of A/B, voltages and any wiring changes. This is the most useful input for rev2.
