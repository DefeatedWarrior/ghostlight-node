#!/bin/bash
# usage: chain.sh MP
cd /home/claude/pcb; P=/usr/bin/python3; F='Warn|leak'
$P build_pcb.py >/dev/null 2>&1
MP=$1 timeout 420 $P route.py out/esp-node-2rdm.kicad_pcb out/unused.kicad_pcb >/dev/null 2>&1
$P import_ses.py out/esp-node-2rdm.kicad_pcb out/esp-node-2rdm.ses out/routed.kicad_pcb >/dev/null 2>&1
$P finish.py out/routed.kicad_pcb out/final.kicad_pcb 2>&1 | grep -E "VBUS|fragment"
$P widen.py out/final.kicad_pcb out/final_w.kicad_pcb 2>&1 | grep final
$P drc.py out/final_w.kicad_pcb /tmp/d_$1.rpt 2>&1 | grep -v -E "$F" | tail -1
