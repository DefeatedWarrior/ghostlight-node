"""Post-route: island removal, GND stitching vias, J4 ground pads solid, refill."""
import sys, math
import pcbnew
from pcbnew import FromMM as mm, ToMM
src, dst = sys.argv[1:3]
OX, OY, W, H = 60.0, 40.0, 100.0, 100.0
b = pcbnew.LoadBoard(src)
gnd = b.FindNet("GND")

for z in b.Zones():
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
for fp in b.GetFootprints():
    if fp.GetReference() == "J4":
        for pad in fp.Pads():
            if pad.GetNetname() == "GND":
                pad.SetZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
    if fp.GetReference() == "J6":
        for pad in fp.Pads():
            if pad.GetNetname() == "GND":
                pad.SetZoneConnection(pcbnew.ZONE_CONNECTION_FULL)

# obstacle list: all pads (box) and track segments, other nets
pads = []
for fp in b.GetFootprints():
    for pad in fp.Pads():
        bb = pad.GetBoundingBox()
        pads.append((ToMM(bb.GetLeft()), ToMM(bb.GetTop()), ToMM(bb.GetRight()), ToMM(bb.GetBottom())))
pads_n = []
for fp in b.GetFootprints():
    for pad in fp.Pads():
        bb = pad.GetBoundingBox()
        pads_n.append((ToMM(bb.GetLeft()), ToMM(bb.GetTop()), ToMM(bb.GetRight()), ToMM(bb.GetBottom()), pad.GetNetname()))
segs_n = []
segs = []; vias = []
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_VIA_T:
        vias.append((ToMM(t.GetPosition().x), ToMM(t.GetPosition().y), ToMM(t.GetWidth()) / 2))
    else:
        segs.append((ToMM(t.GetStart().x), ToMM(t.GetStart().y), ToMM(t.GetEnd().x), ToMM(t.GetEnd().y), ToMM(t.GetWidth()) / 2))
        segs_n.append(segs[-1] + (t.GetNetname(),))
def dseg(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / L))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))
CLR = 0.6 / 2 + 0.2   # via radius + clearance
def free(x, y):
    for l, t, r, bt in pads:
        if l - CLR - 0.1 < x < r + CLR + 0.1 and t - CLR - 0.1 < y < bt + CLR + 0.1:
            return False
    for x1, y1, x2, y2, hw in segs:
        if dseg(x, y, x1, y1, x2, y2) < hw + CLR + 0.05:
            return False
    for vx, vy, vr in vias:
        if math.hypot(x - vx, y - vy) < vr + CLR + 0.3:
            return False
    return True
def free_ex(x, y, own):
    if 24 < x - OX < 76 and y - OY < 6.6:
        return False
    # like free(), but ignore the pad this via belongs to (net GND) so it can sit close
    for l, t, r, bt, net in pads_n:
        if net == 'GND':
            continue
        if l - CLR - 0.05 < x < r + CLR + 0.05 and t - CLR - 0.05 < y < bt + CLR + 0.05:
            return False
    for x1, y1, x2, y2, hw, net in segs_n:
        if net == 'GND':
            continue
        if dseg(x, y, x1, y1, x2, y2) < hw + CLR + 0.05:
            return False
    for vx, vy, vr in vias:
        if math.hypot(x - vx, y - vy) < vr + CLR + 0.3:
            return False
    return True

# ---- tie J4's two separate VBUS lead groups together with a clearance-checked back-layer link
def tie_vbus():
    CL = 0.15 + 0.03
    obs_seg = {pcbnew.F_Cu: [], pcbnew.B_Cu: []}; obs_via = []; obs_pad = {pcbnew.F_Cu: [], pcbnew.B_Cu: []}
    vb_vias, vb_front = [], []
    for t in b.GetTracks():
        if t.Type() == pcbnew.PCB_VIA_T:
            p = t.GetPosition(); rec = (ToMM(p.x), ToMM(p.y), ToMM(t.GetWidth()) / 2)
            (vb_vias if t.GetNetname() == "VBUS" else obs_via).append(rec)
        else:
            s_, e_ = t.GetStart(), t.GetEnd()
            rec = (ToMM(s_.x), ToMM(s_.y), ToMM(e_.x), ToMM(e_.y), ToMM(t.GetWidth()) / 2)
            if t.GetNetname() == "VBUS":
                if t.GetLayer() == pcbnew.F_Cu: vb_front.append(rec)
            else:
                obs_seg[t.GetLayer()].append(rec)
    for fp in b.GetFootprints():
        for pad in fp.Pads():
            if pad.GetNetname() == "VBUS": continue
            bb = pad.GetBoundingBox(); r = (ToMM(bb.GetLeft()), ToMM(bb.GetTop()), ToMM(bb.GetRight()), ToMM(bb.GetBottom()))
            if pad.IsOnLayer(pcbnew.F_Cu): obs_pad[pcbnew.F_Cu].append(r)
            if pad.IsOnLayer(pcbnew.B_Cu): obs_pad[pcbnew.B_Cu].append(r)
    def pad_d(x, y, r):
        dx = max(r[0] - x, 0, x - r[2]); dy = max(r[1] - y, 0, y - r[3]); return math.hypot(dx, dy)
    def pt_ok(x, y, rad, layers):
        for ly in layers:
            for sg in obs_seg[ly]:
                if dseg(x, y, sg[0], sg[1], sg[2], sg[3]) < rad + sg[4] + CL: return False
            for r in obs_pad[ly]:
                if pad_d(x, y, r) < rad + CL: return False
        for vx, vy, vr in obs_via:
            if math.hypot(x - vx, y - vy) < rad + vr + CL: return False
        return True
    def seg_ok(x1, y1, x2, y2, hw):
        n_ = max(2, int(math.hypot(x2 - x1, y2 - y1) / 0.05))
        return all(pt_ok(x1 + (x2 - x1) * k / n_, y1 + (y2 - y1) * k / n_, hw, [pcbnew.B_Cu]) for k in range(n_ + 1))
    # anchor: a VBUS via near J4's first lead group; targets: points along front-layer VBUS copper elsewhere
    j4 = [fp for fp in b.GetFootprints() if fp.GetReference() == "J4"][0]
    leads = sorted({round(ToMM(p.GetY()), 2) for p in j4.Pads() if p.GetNetname() == "VBUS"})
    if len(leads) < 2: return
    top, bot = leads[0], leads[-1]
    anchors = [v for v in vb_vias if abs(v[1] - top) < 3.0] or []
    tgt = []
    for x1, y1, x2, y2, hw in vb_front:
        if min(y1, y2) > bot - 1.5:
            n_ = max(1, int(math.hypot(x2 - x1, y2 - y1) / 0.2))
            tgt += [(x1 + (x2 - x1) * k / n_, y1 + (y2 - y1) * k / n_) for k in range(n_ + 1)]
    best = None
    for ax, ay, _ in anchors:
        for tx, ty in tgt:
            if not pt_ok(tx, ty, 0.25, [pcbnew.F_Cu, pcbnew.B_Cu]): continue
            for path in ([(ax, ay), (ax, ty), (tx, ty)], [(ax, ay), (tx, ay), (tx, ty)], [(ax, ay), (tx, ty)]):
                if all(seg_ok(p[0], p[1], q[0], q[1], 0.15) for p, q in zip(path, path[1:])):
                    L = sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(path, path[1:]))
                    if best is None or L < best[0]: best = (L, path, (tx, ty))
    if not best:
        print("WARNING: no clean path to tie VBUS lead groups"); return
    L, path, (tx, ty) = best
    v = pcbnew.PCB_VIA(b); v.SetPosition(pcbnew.VECTOR2I(mm(tx), mm(ty)))
    v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetWidth(mm(0.5)); v.SetDrill(mm(0.3)); v.SetNet(b.FindNet("VBUS")); b.Add(v)
    for p, q in zip(path, path[1:]):
        t = pcbnew.PCB_TRACK(b); t.SetStart(pcbnew.VECTOR2I(mm(p[0]), mm(p[1]))); t.SetEnd(pcbnew.VECTOR2I(mm(q[0]), mm(q[1])))
        t.SetWidth(mm(0.3)); t.SetLayer(pcbnew.B_Cu); t.SetNet(b.FindNet("VBUS")); b.Add(t)
    print("VBUS lead groups tied on B.Cu, link length %.1f mm" % L)
tie_vbus()
# refresh obstacle lists so later via placement sees the new link
segs.clear(); segs_n.clear(); vias.clear()
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_VIA_T:
        vias.append((ToMM(t.GetPosition().x), ToMM(t.GetPosition().y), ToMM(t.GetWidth()) / 2))
    else:
        rec = (ToMM(t.GetStart().x), ToMM(t.GetStart().y), ToMM(t.GetEnd().x), ToMM(t.GetEnd().y), ToMM(t.GetWidth()) / 2)
        segs.append(rec); segs_n.append(rec + (t.GetNetname(),))
n = 0
step = 5.0
y = 6.0
while y < H - 3:
    x = 6.0
    while x < W - 3:
        ax, ay = OX + x, OY + y
        # keep out of the antenna rule-area band at the top
        if not (24 < x < 76 and y < 13) and free(ax, ay):
            v = pcbnew.PCB_VIA(b)
            v.SetPosition(pcbnew.VECTOR2I(mm(ax), mm(ay)))
            v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetWidth(mm(0.6)); v.SetDrill(mm(0.3)); v.SetNet(gnd)
            b.Add(v); vias.append((ax, ay, 0.3)); n += 1
        x += step
    y += step
# every GND SMD pad on F.Cu gets its own via nearby, so no pad depends on a small copper island
added = 0
dirs = [(1,0),(-1,0),(0,1),(0,-1),(0.7,0.7),(-0.7,0.7),(0.7,-0.7),(-0.7,-0.7)]
for fp in b.GetFootprints():
    for pad in fp.Pads():
        if pad.GetNetname() != "GND" or pad.GetAttribute() != pcbnew.PAD_ATTRIB_SMD:
            continue
        if fp.GetReference() == "U1" and pad.GetNumber() == "41":
            continue
        px, py = ToMM(pad.GetPosition().x), ToMM(pad.GetPosition().y)
        hw = max(ToMM(pad.GetSizeX()), ToMM(pad.GetSizeY())) / 2
        # already has a via within 1.6 mm? then skip
        if any(math.hypot(px - vx, py - vy) < hw + 1.6 for vx, vy, _ in vias):
            continue
        for r in (hw + 0.85, hw + 1.3, hw + 1.8):
            ok = False
            for dx, dy in dirs:
                ax, ay = px + dx * r, py + dy * r
                if OX + 0.8 < ax < OX + W - 0.8 and OY + 0.8 < ay < OY + H - 0.8 and free_ex(ax, ay, pad):
                    v = pcbnew.PCB_VIA(b)
                    v.SetPosition(pcbnew.VECTOR2I(mm(ax), mm(ay)))
                    v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetWidth(mm(0.6)); v.SetDrill(mm(0.3)); v.SetNet(gnd)
                    b.Add(v); vias.append((ax, ay, 0.3)); added += 1; ok = True; break
            if ok: break
print("per-pad ground vias:", added)
print("stitching vias added:", n)
for fp in b.GetFootprints():
    if fp.GetReference() == "Y1":
        for pad in fp.Pads():
            if pad.GetNetname() == "GND":
                pad.SetZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
# connect any front-pour fragment that contains no GND via/through-hole pad
fixed = 0
for _ in range(3):
    gv = [(ToMM(t.GetPosition().x), ToMM(t.GetPosition().y)) for t in b.GetTracks()
          if t.Type() == pcbnew.PCB_VIA_T and t.GetNetname() == "GND"]
    for fp in b.GetFootprints():
        for p in fp.Pads():
            if p.GetNetname() == "GND" and p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH:
                gv.append((ToMM(p.GetX()), ToMM(p.GetY())))
    added_now = 0
    for z in b.Zones():
        if z.GetLayer() != pcbnew.F_Cu:
            continue
        ps = z.GetFilledPolysList(pcbnew.F_Cu)
        for i in range(ps.OutlineCount()):
            if any(ps.Contains(pcbnew.VECTOR2I(mm(x), mm(y)), i) for x, y in gv):
                continue
            bb = ps.Outline(i).BBox()
            x0, y0, x1, y1 = [ToMM(v) for v in (bb.GetLeft(), bb.GetTop(), bb.GetRight(), bb.GetBottom())]
            best = None
            yy = y0
            while yy <= y1:
                xx = x0
                while xx <= x1:
                    pts = [(xx, yy)] + [(xx + dx, yy + dy) for dx, dy in ((.4, 0), (-.4, 0), (0, .4), (0, -.4))]
                    if all(ps.Contains(pcbnew.VECTOR2I(mm(px), mm(py)), i) for px, py in pts):
                        if free_ex(xx, yy, None):
                            best = (xx, yy); break
                    xx += 0.2
                if best: break
                yy += 0.2
            if best:
                v = pcbnew.PCB_VIA(b)
                v.SetPosition(pcbnew.VECTOR2I(mm(best[0]), mm(best[1])))
                v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetWidth(mm(0.6)); v.SetDrill(mm(0.3)); v.SetNet(gnd)
                b.Add(v); vias.append((best[0], best[1], 0.3)); added_now += 1
            else:
                print("could not place via in fragment at", round(x0 - OX, 1), round(y0 - OY, 1))
    fixed += added_now
    if not added_now:
        break
    pcbnew.ZONE_FILLER(b).Fill(b.Zones())
print("fragment vias added:", fixed)
# stubs: small fragments that cannot hold a via get their GND pad tied to a nearby via with a short trace
def free_trk(x, y, hw=0.15):
    for l, t, r, bt, net in pads_n:
        if net == 'GND':
            continue
        if l - hw - 0.22 < x < r + hw + 0.22 and t - hw - 0.22 < y < bt + hw + 0.22:
            return False
    for x1, y1, x2, y2, w, net in segs_n:
        if net == 'GND':
            continue
        if dseg(x, y, x1, y1, x2, y2) < w + hw + 0.22:
            return False
    for vx, vy, vr in vias:
        if math.hypot(x - vx, y - vy) < vr + hw + 0.25 and (vx, vy, vr) not in newv:
            return False
    return True
newv = []
stubs = 0
gv = lambda: [(ToMM(t.GetPosition().x), ToMM(t.GetPosition().y)) for t in b.GetTracks()
              if t.Type() == pcbnew.PCB_VIA_T and t.GetNetname() == "GND"]
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
for z in b.Zones():
    if z.GetLayer() != pcbnew.F_Cu:
        continue
    ps = z.GetFilledPolysList(pcbnew.F_Cu)
    cur = gv()
    frag_bad = [i for i in range(ps.OutlineCount())
                if not any(ps.Contains(pcbnew.VECTOR2I(mm(x), mm(y)), i) for x, y in cur)]
    for i in frag_bad:
        for fp in b.GetFootprints():
            for pad in fp.Pads():
                if pad.GetNetname() != "GND" or pad.GetAttribute() != pcbnew.PAD_ATTRIB_SMD:
                    continue
                if not ps.Contains(pad.GetPosition(), i):
                    continue
                px, py = ToMM(pad.GetPosition().x), ToMM(pad.GetPosition().y)
                done = False
                for rad in [1.2 + 0.4 * k for k in range(0, 10)]:
                    for k in range(16):
                        ang = k * math.pi / 8
                        vx, vy = px + rad * math.cos(ang), py + rad * math.sin(ang)
                        if not (OX + 0.8 < vx < OX + W - 0.8 and OY + 0.8 < vy < OY + H - 0.8):
                            continue
                        if not free_ex(vx, vy, None):
                            continue
                        n_s = max(2, int(rad / 0.1))
                        if all(free_trk(px + (vx - px) * s / n_s, py + (vy - py) * s / n_s) for s in range(1, n_s)):
                            v = pcbnew.PCB_VIA(b)
                            v.SetPosition(pcbnew.VECTOR2I(mm(vx), mm(vy)))
                            v.SetViaType(pcbnew.VIATYPE_THROUGH); v.SetWidth(mm(0.6)); v.SetDrill(mm(0.3)); v.SetNet(gnd)
                            b.Add(v); vias.append((vx, vy, 0.3)); newv.append((vx, vy, 0.3))
                            tr = pcbnew.PCB_TRACK(b)
                            tr.SetStart(pad.GetPosition()); tr.SetEnd(pcbnew.VECTOR2I(mm(vx), mm(vy)))
                            tr.SetWidth(mm(0.3)); tr.SetLayer(pcbnew.F_Cu); tr.SetNet(gnd)
                            b.Add(tr); stubs += 1; done = True; break
                    if done: break
                if not done:
                    print("no stub route for pad", fp.GetReference(), pad.GetNumber())
print("stubs added:", stubs)
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
b.BuildConnectivity()
pcbnew.SaveBoard(dst, b)
