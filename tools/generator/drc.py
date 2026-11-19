import sys, re, collections
import pcbnew
b = pcbnew.LoadBoard(sys.argv[1])
rpt = sys.argv[2]
ok = pcbnew.WriteDRCReport(b, rpt, pcbnew.EDA_UNITS_MILLIMETRES, True)
txt = open(rpt).read()
sec = re.split(r"\*\* Found (\d+) ([^*]+) \*\*", txt)
print("DRC report written", ok)
for m in re.finditer(r"^\[(\w+)\]", txt, re.M): pass
c = collections.Counter(re.findall(r"^\[(\w+)\]", txt, re.M))
print(dict(c))
