# 5. DMX / RS-485 ports

Two identical ports. Part references are shown as DMX1 / DMX2.

| Part | DMX1 | DMX2 |
|---|---|---|
| Transceiver (SN65HVD72DR, SOIC-8) | U3 | U4 |
| Decoupling (100 nF) | C30 | C40 |
| DIR pull-down (10 k) | R30 | R40 |
| TVS (SM712) | D1 | D2 |
| Bias pull-up to A (240 ohm) | R31 | R41 |
| Bias pull-down leg on B (240 ohm) | R32 | R42 |
| Bias switch (2N7002) | Q1 | Q2 |
| Gate pull-down (100 k) | R33 | R43 |
| Termination resistor (120 ohm) | R34 | R44 |
| Termination jumper | J2T | J3T |
| IN / OUT terminals | J2 / J2O | J3 / J3O |
| Port LED and resistor | D30, R35 (1 k) | D40, R45 (1 k) |
| MCU pins | UART1 TX17 RX16 DIR39 | UART2 TX15 RX18 DIR40 |

## Transceiver

SN65HVD72: a 3.3 V half-duplex RS-485 transceiver, 250 kbps, which is the right speed for DMX512 (250 kbaud). Its receiver is fail-safe for an **open, shorted or idle** bus, which keeps the receive line from producing noise while nothing drives the bus (for example during RDM listen windows). This is stated in the device functional-modes table of the TI datasheet.

- Pin map (standard SOIC-8 RS-485 pinout): 1 R (RO), 2 /RE, 3 DE, 4 D (DI), 5 GND, 6 A, 7 B, 8 VCC. Pin-compatible RS-485 transceivers can be swapped in the BOM, but a substitute must keep the fail-safe behaviour and at least +/-8 kV IEC 61000-4-2 ESD rating (or rely on the TVS) to be equivalent.
- /RE and DE are tied together to the DIR GPIO. DIR high = transmit (receiver disabled). DIR low = receive. A 10 k pull-down keeps the port in receive mode while the MCU is in reset.

## Bias and termination

```
          +3V3
            |
          R31/R41  240 ohm
            |
   A  ------+-------------------------------+---- (to transceiver pin 6, terminals, TVS)
            |                                |
       R34/R44 120 ohm                       |
            |                                |
         [J2T/J3T jumper]                    |
            |                                |
   B  ------+----+---------------------------+---- (to transceiver pin 7, terminals, TVS)
                 |
              R32/R42 240 ohm
                 |
              Q1/Q2 drain --- source to GND, gate = BIASn (R33/R43 100 k to GND)
```

- **Bias (GPIO switchable)**: BIAS1 (GPIO1) / BIAS2 (GPIO2) high turns on the 2N7002, completing a 240 ohm pull-up on A and a 240 ohm pull-down on B. The default (GPIO low / reset) is bias off. With the 240 ohm pull-up on A always connected, A is weakly pulled up even when bias is off.
- **Termination (jumper)**: fit a shunt on J2T / J3T to connect 120 ohm across A and B. Fit it only on the last device of a line.
- With bias enabled and the terminator fitted, the idle differential voltage is roughly 0.6 V into the 120 ohm terminator (3.3 V x 120 / (240 + 120 + 240)), and the bias network draws about 5.5 mA. **These values were chosen by the designer, not taken from the E1.20 specification text; check the idle line with a scope** (see [docs/10](10-bring-up-and-test.md)). The receiver's built-in fail-safe means the bias network is a second layer, not the only protection against noise.

## Protection

One SM712 asymmetric TVS per port from A and B to GND (working range -7 V to +12 V, matching the RS-485 common-mode range). There is no isolation and no series fuse on the A/B lines.

## Wiring to XLR connectors

The board uses screw terminals. Wire them to panel-mount XLRs (3-pin or 5-pin DMX):

| Board terminal | XLR pin | DMX signal |
|---|---|---|
| GND | 1 | Shield / common |
| B | 2 | Data - (as labelled in the design) |
| A | 3 | Data + (as labelled in the design) |

5-pin XLR pins 4 and 5 (secondary data) are not connected on this board.

**The A / B polarity labelling is not verified against a known-good fixture.** RS-485 vendors disagree on which line is called A, and the board silkscreen says only A and B. Verify on a scope with a known device (or swap two wires) before trusting it; this is on the pre-order checklist in [docs/11](11-known-issues-and-verification-status.md).

## IN and OUT terminals

IN and OUT on a port are two screw terminals wired in parallel to the same bus: A to A, B to B, GND to GND. They are the same node, not a repeater, so a port is **either** a source **or** a sink for the whole port at a time, and a chain is formed by wiring the OUT terminal onward.
