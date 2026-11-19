import design, csv, collections, math, sys
# (value, footprint-name) -> (LCSC, MPN/description, status). status: OK = number matched to part name in LCSC search results
# ("OK*" = matched in an earlier lookup page); CHECK = plausible, confirm footprint/stock at checkout
M = {
 "ESP32-S3-WROOM-1-N8": ("C2913198","Espressif ESP32-S3-WROOM-1-N8","OK*"),
 "W5500": ("C32843","WIZnet W5500 LQFP-48","OK*"),
 "HR871150C": ("C19724786","Hanrun HR871150C 10/100 PoE RJ45 magjack","OK*"),
 "DP9700-5V": ("C5380091","SDAPO DP9700-5V PoE PD module 5V/2A","OK*"),
 "SN65HVD72DR": ("C48125","TI SN65HVD72DR","OK*"),
 "SM712": ("C2943053","SM712 SOT-23 TVS","OK*"),
 "AMS1117-3.3": ("C6186","AMS1117-3.3 SOT-223","OK*"),
 "USBLC6-2SC6": ("C7519","ST USBLC6-2SC6","OK"),
 "SS14": ("C2480","MDD SS14 SMA","OK"),
 "2N7002": ("C8545","JSCJ 2N7002 SOT-23","OK"),
 "WS2812B": ("C114586","Worldsemi WS2812B-B/W 5050","OK"),
 "USB-C (device/sink)": ("C165948","HRO TYPE-C-31-M-12","OK"),
 "PTC 1.1A": ("C22366107","BORN SMD1206-110/6N PTC","OK"),
 "220uF": ("C32514","Honor RVT0J221M0605 220uF 6.3V 6.3x5.4","OK"),
 "25MHz": ("C2842189","HCI XC32M4-25.000-F20NJDT 3225 25MHz 20pF","CHECK"),
 "FB 120R@100MHz": ("C76892","Murata BLM18AG121SN1D","OK"),
 "BOOT": ("C2886898","E-Switch TL3342F160QG","OK"),
 "RESET": ("C2886898","E-Switch TL3342F160QG","OK"),
 "100nF": ("C1591","Samsung CL10B104KB8NNNC 100nF 50V X7R","OK"),
 "10uF": ("C15850","Samsung CL21A106KAYNNNE 10uF 0805","OK"),
 "1uF": ("C29936","Samsung CL10B105KA8NNNC 1uF 25V X7R 0603","OK"),
 "22uF": ("C45783","Samsung CL21A226MAQNNNE 22uF 0805","OK"),
 "4.7uF": ("C1779","Samsung CL21A475KAQNNNE 4.7uF 0805","OK"),
 "18pF": ("C107040","Yageo CC0603JRNPO9BN180 18pF 50V NP0","OK"),
 "22nF": ("C21122","Samsung CL10B223KB8NNNC 22nF","OK"),
 "10nF": ("C1589","Samsung CL10B103KB8NNNC 10nF","OK"),
 "10k": ("C25804","UNI-ROYAL 0603WAF1002T5E","OK"),
 "1k": ("C21190","UNI-ROYAL 0603WAF1001T5E","OK"),
 "330": ("C23138","UNI-ROYAL 0603WAF3300T5E","OK"),
 "220": ("C22962","UNI-ROYAL 0603WAF2200T5E","OK"),
 "5.1k": ("C23186","UNI-ROYAL 0603WAF5101T5E","OK"),
 "1M": ("C22935","UNI-ROYAL 0603WAF1004T5E","OK"),
 "100k": ("C25803","UNI-ROYAL 0603WAF1003T5E","OK"),
 "120 1%": ("C22787","UNI-ROYAL 0603WAF1200T5E","OK"),
 "240 1%": ("C23350","UNI-ROYAL 0603WAF2400T5E","OK"),
 "12.4k 1%": ("C227572","Yageo AC0603FR-0712K4L 12.4k 1%","OK"),
 "P1": ("C12065","LITEON LTST-C193TGKT-5A emerald green 0603","OK"),
 "P2": ("C12065","LITEON LTST-C193TGKT-5A emerald green 0603","OK"),
}
HDR = ("C2337","BOOMELE 2.54mm 1x40P pin header (snap to length)","OK")
TERM = ("C474953","Cixi Kefa KF128-5.08-3P-AA screw terminal","OK")
SHUNT = ("C2689176","XFCN F254D-02-065-PT-B 2.54mm jumper shunt","CHECK")
rows = collections.OrderedDict()
for p in design.PARTS:
    if p['ref'].startswith('H'): continue
    key = p['val']; fp = p['fp'].split(':')[1]
    if "PinHeader" in fp: info = HDR; key = fp
    elif "TerminalBlock" in fp: info = TERM; key = "Screw terminal 3P 5.08"
    else:
        info = M.get(key) or (p.get('lcsc') and (p['lcsc'], key, "OK*"))
        if not info: info = ("", key, "MISSING")
    k = (key, fp)
    rows.setdefault(k, [info, []])[1].append(p['ref'])
out = []
for (key, fp), (info, refs) in rows.items():
    out.append([info[0], " ".join(refs), len(refs), key, fp, info[1], info[2]])
out.sort(key=lambda r: r[1])
w = csv.writer(open(sys.argv[1], "w", newline=""))
w.writerow(["lcsc", "refs", "qty", "value", "footprint", "part", "status"])
for r in out: w.writerow(r)
# merge into purchase list by LCSC number
buy = collections.OrderedDict()
for r in out: buy[r[0]] = buy.get(r[0], 0) + r[2]
buy["C2689176"] = 2   # shunts for TERM1/TERM2
w2 = csv.writer(open(sys.argv[1].replace(".csv", "_purchase.csv"), "w", newline=""))
w2.writerow(["lcsc", "qty_per_board"])
for k, v in buy.items(): w2.writerow([k, v])
print(len(out), "lines;", sum(1 for r in out if r[6] in ("MISSING",)), "missing;", sum(1 for r in out if r[6] == "CHECK"), "to check")
