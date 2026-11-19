#!/bin/bash
cd /home/claude/pcb
for i in 1 2 3 4 5 6 7 8 9 10 11 12; do
  mp=$(( 30 + (i*7) % 40 ))
  echo "TRY $i MP=$mp" >> /tmp/search.log
  ./chain.sh $mp >> /tmp/search.log 2>&1
  last=$(tail -1 /tmp/search.log)
  if /usr/bin/python3 - "$last" <<'PY'
import sys, ast
d = ast.literal_eval(sys.argv[1])
bad = {"clearance","unconnected_items","hole_clearance","hole_near_hole","shorting_items","via_dangling","track_dangling","copper_edge_clearance","solder_mask_bridge","courtyards_overlap","holes_co_located","drill_out_of_range","track_width","annular_width","starved_thermal"}
sys.exit(1 if bad & set(d) else 0)
PY
  then cp out/final_w.kicad_pcb out/best.kicad_pcb; cp out/final_w.kicad_pro out/best.kicad_pro; echo "CLEAN $i $mp" >> /tmp/search.log; break; fi
done
echo DONE >> /tmp/search.log
