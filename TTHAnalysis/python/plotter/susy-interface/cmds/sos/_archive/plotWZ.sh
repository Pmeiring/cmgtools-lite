#!/bin/bash

T="/data1/botta/trees_SOS_010217" ## do NOT give a trailing /
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-15_sos16_full"  ## do NOT give a trailing /

FL=35.9 ## med-MET and hig-MET
RL=33.2 ## low-MET
QUEUE="-j 4" #"-q all.q"
BLIND="-X blinding" #""


## 3L CR WZ
## =================================================================


## default data-driven fakes
#python susy-interface/plotmaker.py sos3l wzMin $T $O -l $FL --make datasig --plots perCateg -o SR --flags "--perBin $BLIND" $QUEUE
#python susy-interface/plotmaker.py sos3l wzLow $T $O -l $FL --make datasig --plots perCateg -o SR --flags "--perBin $BLIND" $QUEUE
#python susy-interface/plotmaker.py sos3l wzMed $T $O -l $FL --make datasig --plots perCateg -o SR --flags "--perBin $BLIND" $QUEUE

## matched MC fakes
python susy-interface/plotmaker.py sos3l wzMin $T $O -l $FL --make datasig --plots all -o SRmc --flags "--perBin $BLIND" -p "data;prompt_.*;rares;fakes_matched_.*" $QUEUE
python susy-interface/plotmaker.py sos3l wzLow $T $O -l $FL --make datasig --plots all -o SRmc --flags "--perBin $BLIND" -p "data;prompt_.*;rares;fakes_matched_.*" $QUEUE
python susy-interface/plotmaker.py sos3l wzMed $T $O -l $FL --make datasig --plots all -o SRmc --flags "--perBin $BLIND" -p "data;prompt_.*;rares;fakes_matched_.*" $QUEUE



