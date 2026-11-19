# Getting Started

1. **PCB:** upload `fabrication/ghostlight-node-rev1-gerbers.zip` to JLCPCB (2 layers, 100 × 100 mm, 1.6 mm, HASL lead-free).
2. **Parts:** import `bom/BOM_order_purchase.csv` into the LCSC BOM tool, scale for your board count, add about 10 % spare passives. The PoE module (DP9700) had low stock when checked, so verify first.
3. **Assemble** by hand (0603/0805 passives, SOIC-8, LQFP-48 and the module). See `docs/09-assembly-guide.md`.
4. **Bring up** in this order: USB power, 3V3, Ethernet, DMX, PoE last. See [[Bring-up Checklist]].
5. **Flash** the firmware in `firmware/`: see [[Firmware]].

Tools you will want: soldering iron and hot air, multimeter, USB-C cable, a USB-UART adapter (optional, for the debug header), a DMX tester or fixture, an Art-Net/sACN source.
