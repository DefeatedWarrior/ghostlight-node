import sys, re
import pcbnew
from pcbnew import FromMM as mm
src, ses, dst = sys.argv[1:4]
OX, OY = 60.0, 40.0
b = pcbnew.LoadBoard(src)

def tok(s):
    return re.findall(r'"[^"]*"|\(|\)|[^\s()]+', s)
def parse(t):
    st = [[]]
    for x in t:
        if x == '(':
            st.append([])
        elif x == ')':
            n = st.pop(); st[-1].append(n)
        else:
            st[-1].append(x.strip('"'))
    return st[0][0]
tree = parse(tok(open(ses).read()))
def find(n, key):
    return [c for c in n if isinstance(c, list) and c and c[0] == key]
routes = find(tree, 'routes')[0]
res = find(routes, 'resolution')[0]          # ['resolution','um','10']
scale = 1.0 / (float(res[2]) * 1000.0)       # unit -> mm
netout = find(routes, 'network_out')[0]
layers = {"F.Cu": pcbnew.F_Cu, "B.Cu": pcbnew.B_Cu}
nets = {ni.GetNetname(): ni for ni in b.GetNetInfo().NetsByName().values()}
def pt(x, y):
    return pcbnew.VECTOR2I(mm(float(x) * scale), mm(-float(y) * scale))
# remove any existing tracks first (keep EPAD vias that are net GND at U1? rebuild handles those; keep all existing)
nseg = nvia = 0
for n in find(netout, 'net'):
    name = n[1]
    ni = nets.get(name)
    if ni is None:
        print("unknown net", name); continue
    for w in find(n, 'wire'):
        for path in find(w, 'path'):
            layer = layers[path[1]]; width = float(path[2]) * scale
            xy = path[3:]
            pts = [(xy[i], xy[i + 1]) for i in range(0, len(xy) - 1, 2)]
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                if (x1, y1) == (x2, y2):
                    continue
                t = pcbnew.PCB_TRACK(b)
                t.SetStart(pt(x1, y1)); t.SetEnd(pt(x2, y2))
                t.SetWidth(mm(width)); t.SetLayer(layer); t.SetNet(ni)
                b.Add(t); nseg += 1
    for v in find(n, 'via'):
        m = re.search(r'(\d+):(\d+)_um', v[1])
        dia, drill = (float(m.group(1)) / 1000, float(m.group(2)) / 1000) if m else (0.6, 0.3)
        pos = pt(v[2], v[3])
        if any(abs(t.GetPosition().x - pos.x) < mm(0.05) and abs(t.GetPosition().y - pos.y) < mm(0.05)
               for t in b.GetTracks() if t.Type() == pcbnew.PCB_VIA_T):
            continue
        via = pcbnew.PCB_VIA(b)
        via.SetPosition(pos); via.SetViaType(pcbnew.VIATYPE_THROUGH)
        via.SetWidth(mm(dia)); via.SetDrill(mm(drill)); via.SetNet(ni)
        b.Add(via); nvia += 1
print("segments", nseg, "vias", nvia)
filler = pcbnew.ZONE_FILLER(b); filler.Fill(b.Zones())
b.BuildConnectivity()
pcbnew.SaveBoard(dst, b)
