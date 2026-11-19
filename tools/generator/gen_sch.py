"""Generate a net-label style KiCad 7 schematic from design.py (single source of truth)."""
import sys, os, uuid, copy, math
sys.path.insert(0, "/home/claude/pcb")
import design
from kiutils.schematic import Schematic
from kiutils.symbol import SymbolLib, Symbol
from kiutils.items.schitems import Text, SchematicSymbol, GlobalLabel, Connection, NoConnect, SymbolProjectInstance, SymbolProjectPath
from kiutils.items.common import Justify, Position, Property, Effects, Font, Stroke, PageSettings, TitleBlock
from kiutils.utils import sexpr

OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/pcb/sch/esp-node-2rdm-rev1.kicad_sch"
PROJ = os.path.basename(OUT).replace(".kicad_sch", "")
SYMDIR = "/usr/share/kicad/symbols/"
uid = lambda: str(uuid.uuid4())

# ---- custom symbols (project library ESPNODE)
def pinrow(num, name, x, y, ang):
    return (f'(pin passive line (at {x} {y} {ang}) (length 2.54) (name "{name}" (effects (font (size 1.27 1.27)))) '
            f'(number "{num}" (effects (font (size 1.27 1.27)))))')
def custom(name, ref, fp, pins, w=7.62):
    n = len(pins); h = (n + 1) // 2
    top = (h - 1) * 1.27 + 2.54
    body = f'(symbol "{name}_1_1" (rectangle (start {-w} {top+2.54}) (end {w} {-top-2.54}) (stroke (width 0.254) (type default)) (fill (type background)))'
    for i, (num, nm) in enumerate(pins):
        left = i < h
        idx = i if left else i - h
        y = round(top - idx * 2.54, 2)
        body += pinrow(num, nm, -w - 2.54 if left else w + 2.54, y, 0 if left else 180)
    body += ")"
    txt = (f'(symbol "{name}" (pin_names (offset 1.016)) (in_bom yes) (on_board yes) '
           f'(property "Reference" "{ref}" (at 0 {top+5} 0) (effects (font (size 1.27 1.27)))) '
           f'(property "Value" "{name}" (at 0 {-top-5} 0) (effects (font (size 1.27 1.27)))) '
           f'(property "Footprint" "{fp}" (at 0 0 0) (effects (font (size 1.27 1.27)) hide)) '
           f'(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide)) {body})')
    return Symbol.from_sexpr(sexpr.parse_sexp(txt))

J1_PINS = [("1","TD+"),("2","TD-"),("3","CT"),("4","RD+"),("5","RD-"),("7","VC1+"),("8","VC1-"),("9","VC2+"),("10","VC2-"),
           ("11","LED_Y_A"),("12","LED_Y_K"),("13","LED_G_A"),("14","LED_G_K"),("SH","SHIELD")]
CUSTOM = {"ESPNODE:HR871150C": custom("HR871150C", "J", "ESPNODE:RJ45_Hanrun_HR871150C", J1_PINS)}
# project symbol lib file
lib = SymbolLib(); lib.version = "20221018"; lib.generator = "esp-node-2rdm"
lib.symbols = [CUSTOM["ESPNODE:HR871150C"]]
lib.to_file(os.path.join(os.path.dirname(OUT), "ESPNODE.kicad_sym"))
for k, s in CUSTOM.items(): s.libraryNickname = k.split(":")[0]; s.entryName = k.split(":")[1]

_libs = {}
ALIAS = {"Device:CP": "Device:C_Polarized"}
def getsym(libid):
    libid = ALIAS.get(libid, libid)
    if libid in CUSTOM: return CUSTOM[libid]
    nick, name = libid.split(":")
    if nick not in _libs: _libs[nick] = SymbolLib.from_file(SYMDIR + nick + ".kicad_sym")
    for s in _libs[nick].symbols:
        if s.entryName == name:
            s = copy.deepcopy(s)
            if s.extends:                       # resolve derived symbol
                base = getsym(f"{nick}:{s.extends}")
                b = copy.deepcopy(base)
                for p in s.properties:
                    for q in b.properties:
                        if q.key == p.key: q.value = p.value
                b.entryName = name; b.extends = None; s = b
                for u in s.units: u.entryName = name
            s.libraryNickname = nick
            return s
    raise SystemExit(f"symbol not found {libid}")

def allpins(sym):
    out = []
    for u in sym.units: out += u.pins
    out += sym.pins
    return out

sch = Schematic.create_new()
sch.uuid = uid(); sch.version = "20230121"; sch.generator = "eeschema"
sch.paper = PageSettings(paperSize="A0")
sch.titleBlock = TitleBlock(title="ESP-NODE-2RDM rev1", date="2026-11", revision="1", company="Open hardware (CERN-OHL-P-2.0)",
                            comments={1: "Net-label style schematic generated from design.py; nets match the PCB"})
nsym = {}
def libsym(libid):
    if libid not in nsym:
        nsym[libid] = getsym(libid)
        sch.libSymbols.append(nsym[libid])
    return nsym[libid]

MCU = {"U1","C1","C2","C3","R1","SW1","SW2","LED1","R2","D5","C4","J5","R5","J7"}
USBP = {"J4","R3","R4","U6","F1","D3","D4","J6","C5","U5","C6","C7","C50"}
POE = {"PS1"}
D1G = {"U3","D1","Q1","J2","J2T","J2O"} | {f"{k}{n}" for k in "CRD" for n in range(30,36)}
D2G = {"U4","D2","Q2","J3","J3T","J3O"} | {f"{k}{n}" for k in "CRD" for n in range(40,46)}
def group(r):
    if r.startswith("H"): return (6, "Mounting holes")
    if r in MCU: return (0, "ESP32-S3 module, buttons, status LED, expansion and debug headers")
    if r in USBP: return (1, "USB-C (device/sink), power input OR-ing, 3.3 V regulator")
    if r in POE: return (3, "PoE: SDAPO DP9700-5V isolated 802.3af module (inputs from jack centre taps / spare pairs)")
    if r in D1G: return (4, "DMX port 1: RS-485 (SN65HVD72), TVS, bias switch, termination, IN/OUT terminals")
    if r in D2G: return (5, "DMX port 2: RS-485 (SN65HVD72), TVS, bias switch, termination, IN/OUT terminals")
    return (2, "Ethernet: W5500 + HR871150C PoE magjack (link/activity LEDs)")
parts = sorted(design.PARTS, key=lambda p: (group(p['ref'])[0],))
lastg = None
# footprints to assign
x0, y0, cellw = 30.0, 40.0, 95.0
cx, cy, rowh = x0, y0, 0.0
nets_pins = {}
warns = []
flags_needed = ["GND", "+3V3", "+5V", "VBUS", "5V_EXT", "AVDD", "VBUS_F", "V1P2", "CHASSIS"]
def eff(h=1.27): return Effects(font=Font(height=h, width=h))
cnt = 0
for p in parts:
    g = group(p['ref'])
    if g[0] != lastg:
        lastg = g[0]
        if cx > x0: cx = x0; cy += rowh + 25; rowh = 0
        else: cy += 10
        t = Text(text=g[1], position=Position(X=x0, Y=cy - 4, angle=0), effects=Effects(font=Font(height=3, width=3), justify=Justify(horizontally="left")), uuid=uid()); sch.texts.append(t); cy += 6
    if p['ref'].startswith('H'):
        libid = p['sym']
    else:
        libid = "ESPNODE:HR871150C" if p['ref'] == "J1" else p['sym']
    sym = libsym(libid)
    pins = allpins(sym)
    ys = [pp.position.Y for pp in pins] or [0]; xs = [pp.position.X for pp in pins] or [0]
    h = (max(ys) - min(ys)) + 20; w = (max(xs) - min(xs)) + 60
    if cx + max(w - 15, 45) > 1100:
        cx = x0; cy += rowh + 10; rowh = 0
    sx, sy = cx + (max(xs) - min(xs)) / 2 + 30 - (max(xs) + min(xs)) / 2, cy + (max(ys) + 8)
    sx = round(sx / 1.27) * 1.27; sy = round(sy / 1.27) * 1.27
    cx += max(w - 15, 45); rowh = max(rowh, h)
    s = SchematicSymbol()
    s.libraryNickname = sym.libraryNickname; s.entryName = sym.entryName
    s.position = Position(X=round(sx, 2), Y=round(sy, 2), angle=0)
    s.unit = 1; s.inBom = not p['ref'].startswith('H'); s.onBoard = True; s.uuid = uid()
    fp = "ESPNODE:RJ45_Hanrun_HR871150C" if p['ref'] == "J1" else p['fp']
    s.properties = [
        Property(key="Reference", value=p['ref'], id=0, position=Position(X=round(sx, 2), Y=round(sy - (max(ys) + 4), 2), angle=0), effects=eff()),
        Property(key="Value", value=p['val'], id=1, position=Position(X=round(sx, 2), Y=round(sy - (min(ys) - 4), 2), angle=0), effects=eff()),
        Property(key="Footprint", value=fp, id=2, position=Position(X=round(sx, 2), Y=round(sy, 2), angle=0), effects=Effects(font=Font(height=1.27, width=1.27), hide=True)),
        Property(key="Datasheet", value="", id=3, position=Position(X=round(sx, 2), Y=round(sy, 2), angle=0), effects=Effects(font=Font(height=1.27, width=1.27), hide=True)),
        Property(key="LCSC", value=p.get('lcsc') or "", id=4, position=Position(X=round(sx, 2), Y=round(sy, 2), angle=0), effects=Effects(font=Font(height=1.27, width=1.27), hide=True)),
    ]
    s.pins = {pp.number: uid() for pp in pins}
    s.instances = [SymbolProjectInstance(name=PROJ, paths=[SymbolProjectPath(sheetInstancePath="/" + sch.uuid, reference=p['ref'], unit=1)])]
    sch.schematicSymbols.append(s)
    pinnums = {pp.number for pp in pins}
    for k in p['nets']:
        if k not in pinnums: warns.append(f"{p['ref']} net pad {k!r} not in symbol {libid}")
    for pp in pins:
        net = p['nets'].get(pp.number)
        px, py = sx + pp.position.X, sy - pp.position.Y
        if not net:
            nc = NoConnect(); nc.position = Position(X=round(px, 2), Y=round(py, 2)); nc.uuid = uid()
            sch.noConnects.append(nc); continue
        nets_pins.setdefault(net, []).append(f"{p['ref']}.{pp.number}")
        a = math.radians(pp.position.angle or 0)
        ox, oy = -math.cos(a), math.sin(a)            # outward, schematic coords (y down)
        L = 2.54
        ex, ey = px + ox * L, py + oy * L
        wire = Connection(type="wire", points=[Position(X=round(px, 2), Y=round(py, 2)), Position(X=round(ex, 2), Y=round(ey, 2))], stroke=Stroke(width=0, type="default"), uuid=uid())
        sch.graphicalItems.append(wire)
        ang = 0 if ox > 0.5 else 180 if ox < -0.5 else 270 if oy > 0.5 else 90
        gl = GlobalLabel(text=net, shape="passive", position=Position(X=round(ex, 2), Y=round(ey, 2), angle=ang), effects=eff(), uuid=uid())
        sch.globalLabels.append(gl)
        cnt += 1

# PWR_FLAGs
flag = getsym("power:PWR_FLAG"); sch.libSymbols.append(flag)
fx, fy = x0, cy + rowh + 30
for i, net in enumerate([n for n in flags_needed if n in nets_pins]):
    s = SchematicSymbol(); s.libraryNickname = "power"; s.entryName = "PWR_FLAG"
    sx, sy = fx + i * 30, fy
    s.position = Position(X=sx, Y=sy, angle=0); s.unit = 1; s.inBom = False; s.onBoard = False; s.uuid = uid()
    ref = f"#FLG0{i+1}"
    s.properties = [Property(key="Reference", value=ref, id=0, position=Position(X=sx, Y=sy - 5, angle=0), effects=Effects(font=Font(height=1.27, width=1.27), hide=True)),
                    Property(key="Value", value="PWR_FLAG", id=1, position=Position(X=sx, Y=sy + 4, angle=0), effects=eff()),
                    Property(key="Footprint", value="", id=2, position=Position(X=sx, Y=sy, angle=0), effects=Effects(font=Font(height=1.27, width=1.27), hide=True)),
                    Property(key="Datasheet", value="", id=3, position=Position(X=sx, Y=sy, angle=0), effects=Effects(font=Font(height=1.27, width=1.27), hide=True))]
    s.pins = {"1": uid()}
    s.instances = [SymbolProjectInstance(name=PROJ, paths=[SymbolProjectPath(sheetInstancePath="/" + sch.uuid, reference=ref, unit=1)])]
    sch.schematicSymbols.append(s)
    pin = allpins(flag)[0]
    px, py = sx + pin.position.X, sy - pin.position.Y
    ex, ey = px, py + 2.54
    sch.graphicalItems.append(Connection(type="wire", points=[Position(X=px, Y=py), Position(X=px, Y=ey)], stroke=Stroke(width=0, type="default"), uuid=uid()))
    sch.globalLabels.append(GlobalLabel(text=net, shape="passive", position=Position(X=px, Y=ey, angle=270), effects=eff(), uuid=uid()))
sch.sheetInstances = []
os.makedirs(os.path.dirname(OUT), exist_ok=True)
sch.to_file(OUT)
open(OUT.replace(".kicad_sch", ".nets.txt"), "w").write("".join(f"{n}: {' '.join(sorted(v))}\n" for n, v in sorted(nets_pins.items())))
print("symbols", len(sch.schematicSymbols), "labels", cnt, "warnings", len(warns))
for w in warns: print("WARN", w)
