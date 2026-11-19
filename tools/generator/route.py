import sys, subprocess, os
import pcbnew
src, dst = sys.argv[1], sys.argv[2]
b = pcbnew.LoadBoard(src)
from pcbnew import FromMM as mm
ns = b.GetDesignSettings().m_NetSettings
d = ns.m_DefaultNetClass
d.SetClearance(mm(0.15)); d.SetTrackWidth(mm(0.2)); d.SetViaDiameter(mm(0.5)); d.SetViaDrill(mm(0.3))
POWER = []

for z in list(b.Zones()):      # route GND as real copper; pours are re-added afterwards
    b.Remove(z)

dsn = src.replace(".kicad_pcb", ".dsn"); ses = src.replace(".kicad_pcb", ".ses")
print("export dsn:", pcbnew.ExportSpecctraDSN(b, dsn))
import re as _re
txt = open(dsn).read()
m = _re.search(r"\(class kicad_default \"\"(.*?)\n\s+\(circuit", txt, _re.S)
names = m.group(1).split()
rest = [n for n in names if n not in POWER]


open(dsn, "w").write(txt)
print("power nets moved into class Power:", len(POWER))
for f in (ses,):
    if os.path.exists(f): os.remove(f)
r = subprocess.run(["xvfb-run", "-a", "java", "-jar", "/home/claude/tools/freerouting.jar",
                    "-de", dsn, "-do", ses, "-mp", os.environ.get("MP","40")], capture_output=True, text=True, timeout=1500)
print(r.stdout[-1500:]); print(r.stderr[-800:])
print("ses exists:", os.path.exists(ses))

