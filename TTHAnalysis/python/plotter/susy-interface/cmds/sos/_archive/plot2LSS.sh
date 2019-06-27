#!/bin/bash

T="/data1/botta/trees_SOS_010217" ## do NOT give a trailing /
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-12_sos16_base"  ## do NOT give a trailing /

FL=35.9 ## med-MET and hig-MET
RL=33.2 ## low-MET
QUEUE="-j 4" #"-q all.q"
BLIND="-X blinding" #""


## 2L SS
## =================================================================


## Search Regions
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

## SR: default data-driven fakes
python susy-interface/plotmaker.py sos2l 2lss $T $O -l $FL --make datasig --plots perCateg -o SR --flags "--perBin $BLIND" $QUEUE

## SR: fakes from MC
python susy-interface/plotmaker.py sos2l 2lss $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched_.*" -o SRmc --flags "--perBin $BLIND" $QUEUE

## SR: semi-data-driven
python susy-interface/plotmaker.py sos2l 2lss $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_applmc1;fakes_applmc2" -o SRsemi --flags "--perBin $BLIND --plotgroup fakes_applmc1+=fakes_applmc2" $QUEUE



## Sideband
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

## SIDEBAND: MC fakes
python susy-interface/plotmaker.py sos2l 2lss $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched_.*" -o AR --flags "-X twoTight -E oneNotTight --perBin $BLIND" $QUEUE

## SIDEBAND: MC fakes WITH SCALE FACTORS APPLIED
python susy-interface/plotmaker.py sos2l 2lss $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matchedBoth_.*" -o ARsc --flags "-X twoTight -E oneNotTight --perBin $BLIND" $QUEUE

## SIDEBAND: MC fakes (1LNT)
python susy-interface/plotmaker.py sos2l 2lss $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched_.*" -o AR1F --flags "-X twoTight -E oneLNT --perBin $BLIND" $QUEUE

## SIDEBAND: MC fakes (1LNT) WITH SCALE FACTOR APPLIED
python susy-interface/plotmaker.py sos2l 2lss $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched1_.*" -o AR1Fsc --flags "-X twoTight -E oneLNT --perBin $BLIND" $QUEUE

## SIDEBAND: MC fakes (2LNT)
python susy-interface/plotmaker.py sos2l 2lss $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched_.*" -o AR2F --flags "-X twoTight -E twoLNT --perBin $BLIND" $QUEUE

## SIDEBAND: MC fakes (2LNT) WITH SCALE FACTOR APPLIED
python susy-interface/plotmaker.py sos2l 2lss $T $O -l $FL --make datasig --plots testing -p "data;prompt_.*;rares;fakes_matched2_.*" -o AR2Fsc --flags "-X twoTight -E twoLNT --perBin $BLIND" $QUEUE
