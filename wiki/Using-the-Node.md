# 🎚️ Using the Node

Summarised from the firmware README. Behaviour on real Ghostlight hardware is untested.

## Features

| Area | What it does |
|---|---|
| **Protocols** | Art-Net v4 (UDP 6454), sACN E1.31 with multicast |
| **Ports** | 2 independent DMX/RDM ports, 512 channels each, about 44 Hz output, per-port universe mapping with offset |
| **Input** | DMX input monitoring |
| **RDM** | Master (discovery, get/set) and responder |
| **Merge** | HTP, LTP, LAST, BACKUP, up to 4 sources per port, source timeout 2-10 s |
| **Network** | Ethernet (W5500), Wi-Fi station with multiple profiles, Wi-Fi AP fallback, static or DHCP |
| **Web UI** | Configuration, live DMX display over WebSocket, RDM panel, network stats, OTA firmware update |

## First boot

1. Power on. The status LED shows blue while booting.
2. The node connects by priority: **Ethernet → Wi-Fi station → Wi-Fi AP**.
3. Open the web interface:
   - Ethernet / Wi-Fi station: `http://<device-ip>`
   - AP fallback: join the network `ArtnetNode-XXXX`, then open `http://192.168.4.1`
4. Set network options, port modes (Output / Input / RDM) and universes.

## Status LED

| Colour | Meaning |
|---|---|
| Blue | booting / AP mode |
| Green | Ethernet connected |
| Cyan | Wi-Fi station connected |
| Red | error |

The two green port LEDs (D30, D40) are for per-port activity once the firmware drives them (`BOARD_PORT_LED_GPIO`).

> [!NOTE]
> Default AP and credential values are in the firmware docs. Change any default password before using the node on a shared network.

## Sending data

Point any Art-Net or sACN controller at the node. Match the universe numbers to the ports in the web UI, and use a wired connection for show use.
