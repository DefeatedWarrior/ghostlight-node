"""ESP-NODE-2RDM rev1: single source of truth for the board.
Each part: ref, symbol (lib:name), footprint (lib:name), value, x, y, rot, nets {pad: net}.
Coordinates are board-relative mm (0..100 x 0..80), y down.
"""
BOARD_W, BOARD_H = 100.0, 100.0

R0603 = ("Device:R", "Resistor_SMD:R_0603_1608Metric")
C0603 = ("Device:C", "Capacitor_SMD:C_0603_1608Metric")
C0805 = ("Device:C", "Capacitor_SMD:C_0805_2012Metric")
LED0603 = ("Device:LED", "LED_SMD:LED_0603_1608Metric")

PARTS = []


def P(ref, sym, fp, val, x, y, rot=0, nets=None, dnp=False, lcsc=""):
    PARTS.append(dict(ref=ref, sym=sym, fp=fp, val=val, x=x, y=y, rot=rot,
                      nets=nets or {}, dnp=dnp, lcsc=lcsc))


def R(ref, val, x, y, a, b, rot=0, lcsc=""):
    P(ref, *R0603, val, x, y, rot, {"1": a, "2": b}, lcsc=lcsc)


def C(ref, val, x, y, a, b, rot=0, big=False, lcsc=""):
    P(ref, *(C0805 if big else C0603), val, x, y, rot, {"1": a, "2": b}, lcsc=lcsc)


# ---------------------------------------------------------------- mounting
for i, (x, y) in enumerate([(4, 4), (96, 4), (4, 72), (96, 96)], 1):
    P(f"H{i}", "Mechanical:MountingHole", "MountingHole:MountingHole_3.2mm_M3",
      "M3", x, y, 0, {})

# ---------------------------------------------------------------- MCU
P("U1", "RF_Module:ESP32-S3-WROOM-1", "RF_Module:ESP32-S3-WROOM-1",
  "ESP32-S3-WROOM-1-N8", 50, 12.5, 0, {
      "1": "GND", "40": "GND", "41": "GND", "2": "+3V3", "3": "EN",
      "4": "W5500_RST",   # IO4
      "5": "LED_P1",      # IO5
      "6": "LED_P2",      # IO6
      "7": "LED_P3",      # IO7
      "8": "DMX2_TX",     # IO15
      "9": "DMX1_RX",     # IO16
      "10": "DMX1_TX",    # IO17
      "11": "DMX2_RX",    # IO18
      "13": "USB_DM",     # IO19
      "14": "USB_DP",     # IO20
      "17": "W5500_INT",  # IO9
      "18": "W5500_CS",   # IO10
      "19": "W5500_MOSI",  # IO11
      "20": "W5500_SCK",  # IO12
      "21": "W5500_MISO",  # IO13
      "22": "BIAS3",      # IO14
      "23": "DIR3",       # IO21
      "24": "EXP4",       # IO47
      "25": "LED_STATUS",  # IO48
      "27": "BOOT",       # IO0
      "31": "EXP1",       # IO38
      "32": "DMX1_DIR",   # IO39
      "33": "DMX2_DIR",   # IO40
      "34": "EXP2",       # IO41
      "35": "EXP3",       # IO42
      "36": "UART0_RX",   # RXD0 = GPIO44
      "37": "UART0_TX",   # TXD0 = GPIO43
      "38": "BIAS2",      # IO2
      "39": "BIAS1",      # IO1
  }, lcsc="C2913202")
C("C1", "10uF", 36.5, 7.5, "+3V3", "GND", big=True)
C("C2", "100nF", 36.5, 11.0, "+3V3", "GND")
R("R1", "10k", 36.5, 15.0, "+3V3", "EN")
C("C3", "1uF", 36.5, 18.5, "EN", "GND")
P("SW1", "Switch:SW_Push", "Button_Switch_SMD:SW_SPST_TL3342", "BOOT", 14, 22, 0,
  {"1": "BOOT", "2": "GND"})
P("SW2", "Switch:SW_Push", "Button_Switch_SMD:SW_SPST_TL3342", "RESET", 14, 12, 0,
  {"1": "EN", "2": "GND"})

# status LED (WS2812B on 5V through a Schottky to bring VDD down so 3.3 V data meets VIH)
P("LED1", "LED:WS2812B", "LED_SMD:LED_WS2812B_PLCC4_5.0x5.0mm_P3.2mm", "WS2812B",
  26, 30, 0, {"1": "LED_VDD", "2": "", "3": "GND", "4": "LED_DIN"})
R("R2", "330", 26, 36, "LED_STATUS", "LED_DIN")
P("D5", "Device:D_Schottky", "Diode_SMD:D_SMA", "SS14", 18, 36, 0,
  {"1": "LED_VDD", "2": "+5V"})
C("C4", "100nF", 32, 30, "LED_VDD", "GND")

# ---------------------------------------------------------------- power
P("J4", "Connector:USB_C_Receptacle_USB2.0_16P",
  "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12", "USB-C (device/sink)", 11, 75.0, 0, {
      "A1": "GND", "B12": "GND", "B1": "GND", "A12": "GND",
      "A4": "VBUS", "B9": "VBUS", "A9": "VBUS", "B4": "VBUS",
      "A5": "CC1", "B5": "CC2",
      "A6": "USB_DP", "B6": "USB_DP", "A7": "USB_DM", "B7": "USB_DM",
      "S1": "GND"})
R("R3", "5.1k", 4.5, 59, "CC1", "GND")
R("R4", "5.1k", 7.5, 59, "CC2", "GND")
P("U6", "Power_Protection:USBLC6-2SC6", "Package_TO_SOT_SMD:SOT-23-6",
  "USBLC6-2SC6", 18, 64, 0,
  {"1": "USB_DP", "6": "USB_DP", "3": "USB_DM", "4": "USB_DM", "2": "GND", "5": "VBUS"})
P("F1", "Device:Polyfuse", "Fuse:Fuse_1206_3216Metric", "PTC 1.1A", 6, 52, 90,
  {"1": "VBUS", "2": "VBUS_F"})
P("D3", "Device:D_Schottky", "Diode_SMD:D_SMA", "SS14", 6, 44, 90,
  {"1": "+5V", "2": "VBUS_F"})
P("J6", "Connector:Conn_01x02_Pin", "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical",
  "5V_EXT (PoE splitter / DC)", 4, 28, 0, {"1": "5V_EXT", "2": "GND"})
P("D4", "Device:D_Schottky", "Diode_SMD:D_SMA", "SS14", 6, 36, 90,
  {"1": "+5V", "2": "5V_EXT"})
P("C5", "Device:CP", "Capacitor_SMD:CP_Elec_6.3x5.4", "220uF", 18, 50, 0,
  {"1": "+5V", "2": "GND"})
P("U5", "Regulator_Linear:AMS1117-3.3", "Package_TO_SOT_SMD:SOT-223-3_TabPin2",
  "AMS1117-3.3", 28, 52, 0, {"1": "GND", "2": "+3V3", "3": "+5V"}, lcsc="C6186")
C("C6", "10uF", 22, 58, "+5V", "GND", big=True)
C("C7", "22uF", 34, 58, "+3V3", "GND", big=True)

# ---------------------------------------------------------------- debug header
P("J7", "Connector:Conn_01x03_Pin", "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
  "DEBUG UART0 (GND/TX/RX)", 70, 12, 0,
  {"1": "GND", "2": "UART0_TX", "3": "UART0_RX"})

# ---------------------------------------------------------------- expansion / port 3 header
P("J5", "Connector:Conn_01x12_Pin", "Connector_PinHeader_2.54mm:PinHeader_1x12_P2.54mm_Vertical",
  "PORT3/EXPANSION", 92, 12, 0, {
      "1": "+3V3", "2": "+5V", "3": "GND", "4": "UART0_TX", "5": "UART0_RX",
      "6": "DIR3", "7": "BIAS3", "8": "LED_P3", "9": "EXP1", "10": "EXP2",
      "11": "EXP3", "12": "EXP4"})
R("R5", "10k", 86, 20, "DIR3", "GND")

# ---------------------------------------------------------------- Ethernet
P("U2", "Interface_Ethernet:W5500", "Package_QFP:LQFP-48_7x7mm_P0.5mm", "W5500",
  42, 44, 90, {
      "1": "TXN", "2": "TXP", "5": "RXN", "6": "RXP",
      "3": "GND", "9": "GND", "14": "GND", "16": "GND", "19": "GND", "29": "GND", "48": "GND",
      "4": "AVDD", "8": "AVDD", "11": "AVDD", "15": "AVDD", "17": "AVDD", "21": "AVDD",
      "10": "EXRES1", "18": "VBG", "20": "TOCAP", "22": "V1P2",
      "28": "+3V3", "25": "LED_LINK", "27": "LED_ACT",
      "30": "XI", "31": "XO",
      "32": "W5500_CS", "33": "W5500_SCK", "34": "W5500_MISO", "35": "W5500_MOSI",
      "36": "W5500_INT", "37": "W5500_RST",
      "43": "PMODE", "44": "PMODE", "45": "PMODE",
  }, lcsc="C32843")
P("L1", "Device:L", "Inductor_SMD:L_0603_1608Metric", "FB 120R@100MHz", 52, 38, 0,
  {"1": "+3V3", "2": "AVDD"})
for i, (x, y) in enumerate([(30, 38), (30, 41), (30, 47), (30, 50)]):
    C(f"C{10+i}", "100nF", x, y, "AVDD", "GND")
C("C14", "10uF", 55, 41, "AVDD", "GND", big=True)
C("C15", "100nF", 55, 47, "+3V3", "GND")
R("R6", "12.4k 1%", 55, 50, "EXRES1", "GND")
C("C16", "22nF", 36, 52, "VBG", "GND")
C("C17", "4.7uF", 40, 52, "TOCAP", "GND", big=True)
C("C18", "10uF", 46, 52, "V1P2", "GND", big=True)
P("Y1", "Device:Crystal_GND24", "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm", "25MHz",
  46, 32, 0, {"1": "XI", "2": "GND", "3": "XO", "4": "GND"})
C("C19", "18pF", 41, 32, "XI", "GND")
C("C20", "18pF", 51, 32, "XO", "GND")
R("R7", "1M", 46, 28.5, "XI", "XO")
R("R8", "10k", 34, 36, "+3V3", "PMODE")
R("R9", "10k", 38, 36, "+3V3", "W5500_RST")
R("R10", "10k", 30, 33, "+3V3", "W5500_CS")
R("R11", "10k", 34, 33, "+3V3", "W5500_INT")
P("J1", "Connector:RJ45_Hanrun_HR911105A_Horizontal",
  "ESPNODE:RJ45_Hanrun_HR871150C", "HR871150C", 10, 89.2, 180, {
      "1": "TXP", "2": "TXN", "4": "RXP", "5": "RXN", "3": "TCT",
      "7": "POE_A1", "8": "POE_A2", "9": "POE_B1", "10": "POE_B2",
      "11": "JLED_ACT_A", "12": "LED_ACT", "13": "JLED_LNK_A", "14": "LED_LINK",
      "SH": "CHASSIS"}, lcsc="C19724786")
C("C21", "100nF", 8, 75, "TCT", "+3V3")
R("R50", "220", 13, 75, "+3V3", "JLED_ACT_A", rot=90)
R("R51", "220", 16.5, 75, "+3V3", "JLED_LNK_A", rot=90)
# PoE: SDAPO DP9700-5V isolated 802.3af PD module (pin map from datasheet)
P("PS1", "Connector:Conn_01x10_Pin", "ESPNODE:PoE_SDAPO_DP9700", "DP9700-5V", 25.8, 78, 0, {
      "1": "POE_A1", "2": "POE_A2", "3": "POE_B1", "4": "POE_B2", "7": "GND", "8": "5V_EXT"},
  lcsc="C5380091")
P("C50", "Device:CP", "Capacitor_SMD:CP_Elec_6.3x5.4", "220uF", 86, 74, 0, {"1": "5V_EXT", "2": "GND"})
C("C23", "10nF", 48, 62, "CHASSIS", "GND")
R("R12", "1M", 51, 62, "CHASSIS", "GND")

# ---------------------------------------------------------------- DMX ports (identical x2)


def dmx_port(n, cx, trx_ref, tvs_ref, jref, jt_ref, q_ref, base, jo_ref=None):
    t, r, d = f"DMX{n}_TX", f"DMX{n}_RX", f"DMX{n}_DIR"
    A, B = f"DMX{n}_A", f"DMX{n}_B"     # A = DMX+ (XLR pin 3), B = DMX- (XLR pin 2)
    P(trx_ref, "Interface_UART:MAX485E", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
      "SN65HVD72DR", cx + 6, 50, 0,
      {"1": r, "2": d, "3": d, "4": t, "5": "GND", "6": A, "7": B, "8": "+3V3"}, lcsc="C48125")
    C(f"C{base}", "100nF", cx + 12, 47, "+3V3", "GND")
    R(f"R{base}", "10k", cx + 12, 51, d, "GND")
    P(tvs_ref, "Diode:SM712_SOT23", "Package_TO_SOT_SMD:SOT-23", "SM712", cx + 3, 63, 0,
      {"1": A, "2": B, "3": "GND"}, lcsc="C2943053")
    R(f"R{base+1}", "240 1%", cx + 1, 56, "+3V3", A)
    R(f"R{base+2}", "240 1%", cx + 5, 56, B, f"BIAS{n}_N")
    P(q_ref, "Transistor_FET:2N7002", "Package_TO_SOT_SMD:SOT-23", "2N7002", cx + 9, 56, 0,
      {"1": f"BIAS{n}", "2": "GND", "3": f"BIAS{n}_N"})
    R(f"R{base+3}", "100k", cx + 13.5, 56, f"BIAS{n}", "GND")
    R(f"R{base+4}", "120 1%", cx + 1, 60, A, f"TERM{n}")
    P(jt_ref, "Connector:Conn_01x02_Pin",
      "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", f"TERM{n}", cx + 8, 61, 0,
      {"1": f"TERM{n}", "2": B})
    P(jref, "Connector:Screw_Terminal_01x03",
      "TerminalBlock:TerminalBlock_bornier-3_P5.08mm", f"DMX{n}", cx + 2, 73, 0,
      {"1": B, "2": A, "3": "GND"})
    P(jo_ref, "Connector:Screw_Terminal_01x03",
      "TerminalBlock:TerminalBlock_bornier-3_P5.08mm", f"DMX{n}_OUT", cx + 14, 73, 0,
      {"1": B, "2": A, "3": "GND"})
    R(f"R{base+5}", "1k", cx + 9, 43.5, f"LED_P{n}", f"LEDK{n}")
    P(f"D{base}", *LED0603, f"P{n}", cx + 13, 43.5, 0, {"1": "GND", "2": f"LEDK{n}"})


dmx_port(1, 52, "U3", "D1", "J2", "J2T", "Q1", 30, "J2O")
dmx_port(2, 74, "U4", "D2", "J3", "J3T", "Q2", 40, "J3O")
