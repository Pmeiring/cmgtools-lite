#!/bin/bash
cd ~/WorkArea/physics/limits/CMSSW_7_4_7/src/
eval `scramv1 runtime -sh`
cd -

ls -1d sig_TChiWZ_* | xargs -n 1 -P 12 bash ../go.sh
#ls -1d sig_TChiWZ_* | xargs -n 1 -P 12 bash ../go_likelihood.sh
#eval `scramv1 runtime -sh`