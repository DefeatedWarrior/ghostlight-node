import sys, json, os
sys.path.insert(0, os.path.dirname(__file__))
import pcbnew
from pcbnew import FromMM as mm
import importlib, design, layout
importlib.reload(design); importlib.reload(layout)

OX, OY = 60.0, 40.0          # board origin on the KiCad sheet
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/pcb/out/esp-node-2rdm.kicad_pcb"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
FPL = "/usr/share/kicad/footprints/"

# ---- project file with net classes (so the DSN export and DRC know widths)
pro = {
    "meta": {"filename": "esp-node-2rdm.kicad_pro", "version": 1},
    "board": {"design_settings": {
        "rules": {"min_clearance": 0.2, "min_track_width": 0.2, "min_via_diameter": 0.6,
                  "min_through_hole_diameter": 0.3, "min_copper_edge_clearance": 0.3,
                  "min_hole_to_hole": 0.5, "min_annular_width": 0.13}}},
    "net_settings": {
        "classes": [
            {"name": "Default", "clearance": 0.2, "track_width": 0.25, "via_diameter": 0.6,
             "via_drill": 0.3, "diff_pair_width": 0.25, "diff_pair_gap": 0.25,
             "diff_pair_via_gap": 0.25, "microvia_diameter": 0.3, "microvia_drill": 0.1,
             "wire_width": 6, "bus_width": 12, "line_style": 0, "pcb_color": "rgba(0, 0, 0, 0.000)",
             "schematic_color": "rgba(0, 0, 0, 0.000)"},
            {"name": "Power", "clearance": 0.2, "track_width": 0.6, "via_diameter": 0.8,
             "via_drill": 0.4, "diff_pair_width": 0.25, "diff_pair_gap": 0.25,
             "diff_pair_via_gap": 0.25, "microvia_diameter": 0.3, "microvia_drill": 0.1,
             "wire_width": 6, "bus_width": 12, "line_style": 0, "pcb_color": "rgba(0, 0, 0, 0.000)",
             "schematic_color": "rgba(0, 0, 0, 0.000)"}],
        "meta": {"version": 3},
        "netclass_patterns": [{"netclass": "Power", "pattern": p} for p in
                              ["+3V3", "+5V", "VBUS", "VBUS_F", "5V_EXT", "AVDD", "LED_VDD"]],
    },
}
json.dump(pro, open(OUT.replace(".kicad_pcb", ".kicad_pro"), "w"), indent=2)

board = pcbnew.CreateEmptyBoard()
board.SetCopperLayerCount(2)
ds = board.GetDesignSettings()
ds.SetCopperLayerCount(2)

def P(x, y):
    return pcbnew.VECTOR2I(mm(OX + x), mm(OY + y))

# ---- outline
W, H = design.BOARD_W, design.BOARD_H
pts = [(0, 0), (W, 0), (W, H), (0, H)]
for i in range(4):
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetLayer(pcbnew.Edge_Cuts)
    s.SetWidth(mm(0.1))
    s.SetStart(P(*pts[i])); s.SetEnd(P(*pts[(i + 1) % 4]))
    board.Add(s)

# ---- nets
nets = {}
def net(name):
    if not name:
        return None
    if name not in nets:
        ni = pcbnew.NETINFO_ITEM(board, name)
        board.Add(ni)
        nets[name] = ni
    return nets[name]

# ---- footprints
placed = {}
for p in design.PARTS:
    if p['ref'] in layout.POS:
        p['x'], p['y'], p['rot'] = layout.POS[p['ref']]
    lib, name = p["fp"].split(":")
    fp = pcbnew.FootprintLoad(("/home/claude/pcb/lib/" if lib == "ESPNODE" else FPL) + lib + ".pretty", name)
    if fp is None:
        raise SystemExit(f"footprint missing {p['fp']}")
    fp.SetFPID(pcbnew.LIB_ID(lib, name))
    fp.SetReference(p["ref"])
    fp.SetValue(p["val"])
    fp.SetPosition(P(p["x"], p["y"]))
    if p["rot"]:
        fp.SetOrientationDegrees(p["rot"])
    board.Add(fp)
    for pad in fp.Pads():
        n = p["nets"].get(pad.GetNumber())
        if n:
            pad.SetNet(net(n))
    if p['ref'] == 'U1':   # 0.2 mm thermal-via pads are below JLC 2-layer minimum drill (0.3)
        pl = list(fp.Pads())
        big = [pd for pd in pl if pd.GetNumber() == '41' and pd.GetSizeX() > mm(3)][0]
        EPAD_POS = (big.GetX(), big.GetY())
        for pad in pl:
            if pad.GetNumber() == '41' and pad.GetSizeX() < mm(1.0):
                fp.Remove(pad)
    placed[p["ref"]] = fp
    fp.Reference().SetVisible(not p["ref"].startswith("H"))
    fp.Value().SetVisible(False)
    for f in (fp.Reference(),):
        f.SetTextSize(pcbnew.VECTOR2I(mm(0.8), mm(0.8)))
        f.SetTextThickness(mm(0.12))

# ---- EPAD ground vias for U1 (0.3 drill / 0.6 pad)
for dx, dy in [(-1.0, -1.0), (1.0, -1.0), (-1.0, 1.0), (1.0, 1.0)]:
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(pcbnew.VECTOR2I(EPAD_POS[0] + mm(dx), EPAD_POS[1] + mm(dy)))
    v.SetViaType(pcbnew.VIATYPE_THROUGH)
    v.SetWidth(mm(0.6)); v.SetDrill(mm(0.3))
    v.SetNet(net('GND'))
    board.Add(v)

# ---- ground pours both sides
def pour(layer):
    z = pcbnew.ZONE(board)
    z.SetLayer(layer)
    z.SetNet(net("GND"))
    z.SetMinThickness(mm(0.2))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    z.SetThermalReliefGap(mm(0.3)); z.SetThermalReliefSpokeWidth(mm(0.4))
    z.SetLocalClearance(mm(0.25))
    ol = z.Outline()
    ol.NewOutline()
    for x, y in [(0.3, 0.3), (W - 0.3, 0.3), (W - 0.3, H - 0.3), (0.3, H - 0.3)]:
        ol.Append(mm(OX + x), mm(OY + y))
    board.Add(z)
pour(pcbnew.F_Cu); pour(pcbnew.B_Cu)

board.BuildConnectivity()
pcbnew.SaveBoard(OUT, board)
print("saved", OUT, "parts", len(design.PARTS), "nets", len(nets))
