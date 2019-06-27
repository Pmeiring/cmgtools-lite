#!/bin/bash

T="/data1/botta/trees_SOS_010217" ## do NOT give a trailing /
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-14_sos16_allsamples"  ## do NOT give a trailing /

FL=35.9 ## med-MET and hig-MET
RL=33.2 ## low-MET
QUEUE="-j 4 --mca susy-sos-v1/2l/mca_allsamples.txt" #"-q all.q"
BLIND="-X blinding" #""



## SEARCH REGIONS
## =================================================================

## 2L OS EWK
python susy-interface/plotmaker.py sos2l 2losEwkLow $T $O -l $RL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE
python susy-interface/plotmaker.py sos2l 2losEwkMed $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE
python susy-interface/plotmaker.py sos2l 2losEwkHig $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE

## 2L OS COLORED
python susy-interface/plotmaker.py sos2l 2losColLow $T $O -l $RL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE
python susy-interface/plotmaker.py sos2l 2losColMed $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE
python susy-interface/plotmaker.py sos2l 2losColHig $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE

## 2L SS
python susy-interface/plotmaker.py sos2l 2lss       $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE

## DY CR
python susy-interface/plotmaker.py sos2l dyLow      $T $O -l $RL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE
python susy-interface/plotmaker.py sos2l dyMed      $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE

## TT CR
python susy-interface/plotmaker.py sos2l ttLow      $T $O -l $RL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE
python susy-interface/plotmaker.py sos2l ttMed      $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE

## VV CR
python susy-interface/plotmaker.py sos2l vvLow      $T $O -l $RL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE
python susy-interface/plotmaker.py sos2l vvMed      $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE


QUEUE="-j 4 --mca susy-sos-v1/3l/mca_allsamples.txt" #"-q all.q"

### 3L 
#python susy-interface/plotmaker.py sos3l 3lLow      $T $O -l $RL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE
#python susy-interface/plotmaker.py sos3l 3lMed      $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE

### WZ CR
#python susy-interface/plotmaker.py sos3l wzMin      $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE
#python susy-interface/plotmaker.py sos3l wzLow      $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE
#python susy-interface/plotmaker.py sos3l wzMed      $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE


##### SIDEBAND
##### =================================================================
###
##### 2L OS EWK
###python susy-interface/plotmaker.py sos2l 2losEwkLow $T $O -l $RL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o ARmc --flags "--perBin $BLIND -X twoTight -E oneNotTight" $QUEUE
###python susy-interface/plotmaker.py sos2l 2losEwkMed $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o ARmc --flags "--perBin $BLIND -X twoTight -E oneNotTight" $QUEUE
###python susy-interface/plotmaker.py sos2l 2losEwkHig $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o ARmc --flags "--perBin $BLIND -X twoTight -E oneNotTight" $QUEUE
###
##### 2L OS COLORED
###python susy-interface/plotmaker.py sos2l 2losColLow $T $O -l $RL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o ARmc --flags "--perBin $BLIND -X twoTight -E oneNotTight" $QUEUE
###python susy-interface/plotmaker.py sos2l 2losColMed $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o ARmc --flags "--perBin $BLIND -X twoTight -E oneNotTight" $QUEUE
###python susy-interface/plotmaker.py sos2l 2losColHig $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o ARmc --flags "--perBin $BLIND -X twoTight -E oneNotTight" $QUEUE
###
##### 2L SS
###python susy-interface/plotmaker.py sos2l 2lss       $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o ARmc --flags "--perBin $BLIND -X twoTight -E oneNotTight" $QUEUE
###
##### DY CR
###python susy-interface/plotmaker.py sos2l dyLow      $T $O -l $RL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o ARmc --flags "--perBin $BLIND -X twoTight -E oneNotTight" $QUEUE
###python susy-interface/plotmaker.py sos2l dyMed      $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o ARmc --flags "--perBin $BLIND -X twoTight -E oneNotTight" $QUEUE
###
##### TT CR
###python susy-interface/plotmaker.py sos2l ttLow      $T $O -l $RL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o ARmc --flags "--perBin $BLIND -X twoTight -E oneNotTight" $QUEUE
###python susy-interface/plotmaker.py sos2l ttMed      $T $O -l $FL --make bkgs --plots perCateg -p "prompt_.*;fakes_matched_.*" -o ARmc --flags "--perBin $BLIND -X twoTight -E oneNotTight" $QUEUE
###
##### 3L 
##### WZ CR
###
###
