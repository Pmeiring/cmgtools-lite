#!/bin/bash
export XRD_NETWORKSTACK=IPv4
cd [SRC]
eval $(scramv1 runtime -sh); 
cd CMGTools/TTHAnalysis/python/plotter
[CMD]
echo "Job for susy-sos task [INST] is done."
echo "Log files can be found at [WORK]/susy-interface/tmp/[INST]/log"
#if [ ! -z "[EMAIL]" ]; then
#  echo "Job for SUSY-Interface task [INST] is done." | mail -s "SUSY-Interface JobControl" [EMAIL]
#fi
touch [JOBDIR]/[JOBID]
