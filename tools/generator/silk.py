import pcbnew, sys
from pcbnew import FromMM as F, ToMM as T
OX, OY = 60.0, 40.0
b = pcbnew.LoadBoard(sys.argv[1])
FS, BS = pcbnew.F_SilkS, pcbnew.B_SilkS
def V(x, y): return pcbnew.VECTOR2I(F(x + OX), F(y + OY))
def rect(bb, m=0.0):
    return (T(bb.GetX()) - OX - m, T(bb.GetY()) - OY - m, T(bb.GetRight()) - OX + m, T(bb.GetBottom()) - OY + m)
def hit(a, c): return not (a[2] <= c[0] or c[2] <= a[0] or a[3] <= c[1] or c[3] <= a[1])

for r_ in ('J2','J2O','J3','J3O'):
    b.FindFootprintByReference(r_).Reference().SetVisible(False)
obst = {FS: [], BS: []}
pads = {FS: [], BS: []}
vias = []
for f in b.GetFootprints():
    for p in f.Pads():
        r_ = rect(p.GetBoundingBox(), 0.25)
        if p.IsOnLayer(pcbnew.F_Cu): pads[FS].append(r_)
        if p.IsOnLayer(pcbnew.B_Cu): pads[BS].append(r_)
    for g in f.GraphicalItems():
        if g.GetLayer() in obst: obst[g.GetLayer()].append(rect(g.GetBoundingBox(), 0.15))
    for fld in (f.Reference(),):
        if fld.IsVisible() and fld.GetLayer() in obst: obst[fld.GetLayer()].append(rect(fld.GetBoundingBox(), 0.15))
for t in b.GetTracks():
    if t.GetClass() == 'PCB_VIA': vias.append(rect(t.GetBoundingBox(), 0.25))
bodies = [rect(f.GetBoundingBox(False, False), 0.4) for f in b.GetFootprints()]
placed, skipped = [], []
EDGE = 0.6
def ok(r, layer):
    if r[0] < EDGE or r[1] < EDGE or r[2] > 100 - EDGE or r[3] > 100 - EDGE: return False
    for o in pads[layer] + obst[layer]:
        if hit(r, o): return False
    for o in placed:
        if o[0] == layer and hit(r, o[1]): return False
    return True
def mk(text, x, y, size, layer, just, ang, bold=False):
    t = pcbnew.PCB_TEXT(b)
    t.SetText(text); t.SetLayer(layer)
    t.SetTextSize(pcbnew.VECTOR2I(F(size), F(size)))
    t.SetTextThickness(F(0.2 if bold else 0.15))
    t.SetHorizJustify({'c': pcbnew.GR_TEXT_H_ALIGN_CENTER, 'l': pcbnew.GR_TEXT_H_ALIGN_LEFT, 'r': pcbnew.GR_TEXT_H_ALIGN_RIGHT}[just])
    t.SetVertJustify(pcbnew.GR_TEXT_V_ALIGN_CENTER)
    t.SetTextAngle(pcbnew.EDA_ANGLE(ang, pcbnew.DEGREES_T))
    if layer == BS: t.SetMirrored(True)
    t.SetPosition(V(x, y))
    return t
def place(text, cands, size=1.0, layer=FS, just='c', bold=False):
    for (x, y, *rest) in cands:
        j = rest[0] if rest else just
        ang = rest[1] if len(rest) > 1 else 0
        t = mk(text, x, y, size, layer, j, ang, bold)
        r = rect(t.GetBoundingBox(), 0.0)
        r = (r[0] - 0.1, r[1] - 0.1, r[2] + 0.1, r[3] + 0.1)
        if ok(r, layer):
            b.Add(t); placed.append((layer, r)); return (x, y)
    skipped.append(text); return None
def near(ax, ay, rad=14, step=1.0, just='c'):
    pts = [(ax + dx * step, ay + dy * step, just) for dx in range(-int(rad/step), int(rad/step)+1) for dy in range(-int(rad/step), int(rad/step)+1)]
    return sorted(pts, key=lambda p: (p[0]-ax)**2 + (p[1]-ay)**2)
def around(x, y, dxs=(0,), dys=(0, -1, 1, -2, 2, -3, 3), *rest):
    return [(x + dx, y + dy, *rest) for dy in dys for dx in dxs]

# terminal pin labels (above each pad row) and port tags
for ref, tag in (("J2", "DMX1 IN"), ("J2O", "DMX1 OUT"), ("J3", "DMX2 IN"), ("J3O", "DMX2 OUT")):
    f = b.FindFootprintByReference(ref)
    pp = {p.GetNumber(): p for p in f.Pads()}
    for num, lab in (("1", "B"), ("2", "A"), ("3", "GND")):
        x = T(pp[num].GetX()) - OX
        place(lab, [(x, 90.8), (x, 90.5), (x, 91.0)], size=0.9, bold=True)
    xc = T(pp["2"].GetX()) - OX
    place(tag, [(xc, y) for y in (92.6, 92.0, 93.2, 91.6)], size=1.0, layer=BS, bold=True)
# jumpers / buttons / connectors
for ref in ("J2T", "J3T"):
    f = b.FindFootprintByReference(ref); x = T(f.GetX()) - OX; y = T(f.GetY()) - OY
    place("120R TERM", [(x + 2.0, y + 1.3, 'l'), (x - 2.0, y + 1.3, 'r'), (x, y - 2.5, 'c'), (x, y + 6.5, 'c')], size=0.9)
for ref, lab in (("SW1", "BOOT"), ("SW2", "RESET")):
    f = b.FindFootprintByReference(ref); x = T(f.GetX()) - OX; y = T(f.GetY()) - OY
    place(lab, [(x + 5.2, y, 'l'), (x - 5.2, y, 'r'), (x, y - 3.8, 'c'), (x, y + 3.8, 'c')], size=1.0, bold=True)
f = b.FindFootprintByReference("J7"); x = T(f.GetX()) - OX
for n, lab in (("1", "GND"), ("2", "TX"), ("3", "RX")):
    p = [q for q in f.Pads() if q.GetNumber() == n][0]
    place(lab, [(x + 1.8, T(p.GetY()) - OY, 'l')], size=0.9)
place("DEBUG UART0 3V3", [(x - 0.8, 9.0, 'l'), (x - 0.8, 8.2, 'l'), (x, 20.5, 'c')], size=0.9)
f = b.FindFootprintByReference("J6")
for n, lab in (("1", "5V IN"), ("2", "GND")):
    p = [q for q in f.Pads() if q.GetNumber() == n][0]
    y = T(p.GetY()) - OY
    place(lab, [(6.6, y, 'l'), (6.6, y + 0.8, 'l')], size=0.9)
place("USB-C", near(12, 31), size=1.0, bold=True)
place("ETH + PoE", near(12, 74), size=1.0, bold=True)
# J5 expansion labels (left of header)
f = b.FindFootprintByReference("J5")
names = ["3V3", "5V", "GND", "U0TX", "U0RX", "DIR3", "BIAS3", "LED3", "IO38", "IO41", "IO42", "IO47"]
pads5 = sorted([p for p in f.Pads()], key=lambda p: int(p.GetNumber()))
for p, lab in zip(pads5, names):
    y = T(p.GetY()) - OY
    place(lab, [(T(p.GetX()) - OX - 1.8, y, 'r'), (T(p.GetX()) - OX + 1.8, y, 'l')], size=0.8)
place("EXPANSION", [(92, 8.0, 'c'), (92, 7.2, 'c'), (92, 44.0, 'c')], size=0.9, bold=True)
# branding block (front): grid search, shrinking if needed
def try_block(blk):
    for by in range(30, 98, 2):
        for bx in range(2, 70, 2):
            ps, yy, good = [], by, True
            for size, text, bold in blk:
                t = mk(text, bx, yy, size, FS, 'l', 0, bold)
                r = rect(t.GetBoundingBox(), 0)
                r = (r[0] - 0.1, r[1] - 0.1, r[2] + 0.1, r[3] + 0.1)
                if (not ok(r, FS)) or any(hit(r, o) for o in bodies): good = False; break
                ps.append((t, r)); yy += size + 0.9
            if good:
                for t, r in ps: b.Add(t); placed.append((FS, r))
                print("branding block at", bx, by); return True
    return False
done = False
for ts in (2.4, 2.0, 1.6):
    blk = [(ts, "ESP-NODE-2RDM", True), (1.0, "rev1  Art-Net/sACN > DMX512 x2", False), (1.0, "PoE 802.3af / USB-C / RDM", False), (1.0, "Open hardware CERN-OHL-P-2.0", False)]
    if try_block(blk): done = True; break
if not done: skipped.append("BRANDING BLOCK")
# back side info
back = ["ESP-NODE-2RDM rev1", "CERN-OHL-P-2.0 open hardware", "DMX1 UART1 TX17 RX16 DIR39  BIAS1 IO1",
        "DMX2 UART2 TX15 RX18 DIR40  BIAS2 IO2", "W5500 CS10 MOSI11 MISO13 SCK12 INT9 RST4",
        "PORT LED IO5 IO6  STATUS WS2812 IO48  BOOT IO0"]
yy = 20
for i, line in enumerate(back):
    place(line, [(50, yy, 'c')], size=1.2 if i == 0 else 1.0, layer=BS, bold=(i == 0)); yy += 2.2
pcbnew.SaveBoard(sys.argv[2], b)
print("skipped:", skipped)
