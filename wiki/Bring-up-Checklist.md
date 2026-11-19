# Bring-up Checklist

Do these in order and stop at the first failure.

- [ ] Visual inspection, no solder bridges; resistance between 5V and GND is not a short
- [ ] USB power only: 5 V and 3V3 rails correct, no hot parts
- [ ] Flash firmware, console output on USB or J7
- [ ] Ethernet link LED, node answers Art-Net poll
- [ ] DMX out on both ports, check with a fixture or tester; check A/B polarity
- [ ] DMX in and RDM discovery
- [ ] PoE last, from an 802.3af switch or injector

Record your results and open an issue: results from the first board feed rev2. Full plan: `docs/10-bring-up-and-test.md`.
