#!/bin/bash

T="/data1/botta/trees_SOS_010217" ## do NOT give a trailing /
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-14_sos16_test"  ## do NOT give a trailing /

FL=35.9 ## med-MET and hig-MET
RL=33.2 ## low-MET
QUEUE="-j 4" #"-q all.q"
BLIND="-X blinding" #""


## 3L SIGNAL REGION
## =================================================================

T="/data1/peruzzi/trees_SOS_110917_noVtx" ## do NOT give a trailing /


## matched MC fakes
python susy-interface/plotmaker.py sos3l 3lLow $T $O -l $RL --make datasig --plots perCateg -o SRmc --flags "--perBin $BLIND" -p "prompt_.*;rares;fakes_matched_.*" $QUEUE
python susy-interface/plotmaker.py sos3l 3lMed $T $O -l $FL --make datasig --plots perCateg -o SRmc --flags "--perBin $BLIND" -p "prompt_.*;rares;fakes_matched_.*" $QUEUE
