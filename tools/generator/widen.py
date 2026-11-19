import sys, re, math, os
import pcbnew
from pcbnew import FromMM as mm, ToMM
src, dst = sys.argv[1:3]
NETS = {"+3V3", "+5V", "VBUS", "VBUS_F", "5V_EXT"}
STEPS = [0.5, 0.35, 0.25]
b = pcbnew.LoadBoard(src)
segs = [t for t in b.GetTracks() if t.Type() != pcbnew.PCB_VIA_T and t.GetNetname() in NETS]
level = {id(t): 0 for t in segs}
# only widen segments that are not tiny stubs (pad escapes stay as routed)
for t in segs:
    t.SetWidth(mm(STEPS[0] if ToMM(t.GetLength()) >= 0.8 else ToMM(t.GetWidth())))
def dseg(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1; L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / L))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))
rpt = "/tmp/claude-0/-home-claude/5f089908-5477-5b0d-842f-332773f016c5/scratchpad/wid.rpt"
for it in range(12):
    pcbnew.ZONE_FILLER(b).Fill(b.Zones()); b.BuildConnectivity()
    pcbnew.WriteDRCReport(b, rpt, pcbnew.EDA_UNITS_MILLIMETRES, True)
    txt = open(rpt).read()
    bad = 0
    for blk in re.split(r"\n(?=\[)", txt):
        k = blk.split("]")[0]
        if k not in ("[clearance", "[hole_clearance", "[shorting_items", "[copper_edge_clearance"):
            continue
        for m in re.finditer(r"@\(([\d.]+) mm, ([\d.]+) mm\): Track \[([^\]]+)\] on (\S+)", blk):
            x, y, net, layer = float(m.group(1)), float(m.group(2)), m.group(3), m.group(4).rstrip(",")
            if net not in NETS: continue
            cands = []
            for t in segs:
                if t.GetNetname() != net or t.GetLayerName() != layer: continue
                d = dseg(x, y, ToMM(t.GetStart().x), ToMM(t.GetStart().y), ToMM(t.GetEnd().x), ToMM(t.GetEnd().y))
                cands.append((d, t))
            if not cands: continue
            dmin = min(d for d, _ in cands)
            if dmin > 1.5: continue
            for d, t in cands:
                if d <= dmin + 0.05:
                    w = ToMM(t.GetWidth())
                    nxt = [s for s in STEPS if s < w - 0.01]
                    if nxt or w > 0.2:
                        t.SetWidth(mm(nxt[0] if nxt else 0.2)); bad += 1
    print("iteration", it, "violations touching power tracks:", bad)
    if not bad: break
pcbnew.SaveBoard(dst, b)
import collections
print("final power widths:", dict(collections.Counter(round(ToMM(t.GetWidth()), 2) for t in segs)))
