# DMX Wiring

Each port has an IN and an OUT terminal wired in parallel on one transceiver, so a port is an input or an output as a whole. The OUT terminal is just a second place to attach a cable (daisy chain).

Terminal order, left to right as silkscreened: **B, A, GND**.

- A = DMX+ (XLR pin 3), B = DMX− (XLR pin 2) as labelled in the design. **Polarity has not been verified on hardware:** check it with your first fixture and swap if needed.
- Termination: 120 Ω via jumper. Enable only at the end of a line.
- Bias: switched by GPIO1 / GPIO2 (off by default). The firmware does not drive these yet.
- The SN65HVD72 has receiver fail-safe for open, shorted and idle buses, which matters for RDM listen windows.

Details: `docs/05-dmx-ports.md`.
