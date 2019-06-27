#!/bin/bash

T="/data1/peruzzi/trees_SOS_030518" ## do NOT give a trailing /
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-15_sos17_full"  ## do NOT give a trailing /

FL=41.4 ## med-MET and hig-MET
RL=37.1 ## low-MET
QUEUE="-j 4" #"-q all.q"
BLIND="-X blinding" #""


## 2L CR VV
## =================================================================

## Nominal
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

## default data-driven fakes
#python susy-interface/plotmaker.py sos2l vvLow $T $O -l $RL --make datasig --plots perCateg -o SR --flags "--perBin $BLIND" $QUEUE
#python susy-interface/plotmaker.py sos2l vvMed $T $O -l $FL --make datasig --plots perCateg -o SR --flags "--perBin $BLIND" $QUEUE

## fakes from MC
python susy-interface/plotmaker.py sos2l vvLow $T $O -l $RL --make datasig --plots all -o SRmc --flags "--perBin $BLIND" -p "data;prompt_.*;rares;fakes_matched_.*" $QUEUE --mccs "susy-sos-v1/mcc_triggerdefs.txt;susy-sos-v1/crvv/mcc_vv_2017.txt;susy-sos-v1/mcc_sos.txt;susy-sos-v1/2l/mcc_sf_met.txt;susy-sos-v1/2l/mcc2017/mcc_sf_fakes_ttLow.txt" --cuts susy-sos-v1/crvv/cuts_vv_2017.txt --mca susy-sos-v1/2l/mca_sos_2017.txt -W 'wBG17' --smcfriends 0_pileup_v1
python susy-interface/plotmaker.py sos2l vvMed $T $O -l $FL --make datasig --plots all -o SRmc --flags "--perBin $BLIND" -p "data;prompt_.*;rares;fakes_matched_.*" $QUEUE --mccs "susy-sos-v1/mcc_triggerdefs.txt;susy-sos-v1/crvv/mcc_vv_2017.txt;susy-sos-v1/mcc_sos.txt;susy-sos-v1/2l/mcc_sf_met.txt;susy-sos-v1/2l/mcc2017/mcc_sf_fakes_ttLow.txt" --cuts susy-sos-v1/crvv/cuts_vv_2017.txt --mca susy-sos-v1/2l/mca_sos_2017.txt -W 'wBG17' --smcfriends 0_pileup_v1

## semi-data-driven fakes
#python susy-interface/plotmaker.py sos2l vvLow $T $O -l $RL --make datasig --plots perCateg -o SRsemi --flags "--perBin $BLIND --plotgroup fakes_applmc1+=fakes_applmc2" -p "data;prompt_.*;rares;fakes_applmc1;fakes_applmc2" $QUEUE
#python susy-interface/plotmaker.py sos2l vvMed $T $O -l $FL --make datasig --plots perCateg -o SRsemi --flags "--perBin $BLIND --plotgroup fakes_applmc1+=fakes_applmc2" -p "data;prompt_.*;rares;fakes_applmc1;fakes_applmc2" $QUEUE


## Sideband
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#### SIDEBAND: MC fakes
##python susy-interface/plotmaker.py sos2l vvLow $T $O -l $RL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched_.*" -o AR --flags "-X twoTight -E oneNotTight --perBin $BLIND" $QUEUE
##python susy-interface/plotmaker.py sos2l vvMed $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched_.*" -o AR --flags "-X twoTight -E oneNotTight --perBin $BLIND" $QUEUE
##
#### SIDEBAND: MC fakes WITH SCALE FACTORS APPLIED
##python susy-interface/plotmaker.py sos2l vvLow $T $O -l $RL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matchedBoth_.*" -o ARsc --flags "-X twoTight -E oneNotTight --perBin $BLIND" $QUEUE
##python susy-interface/plotmaker.py sos2l vvMed $T $O -l $RL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matchedBoth_.*" -o ARsc --flags "-X twoTight -E oneNotTight --perBin $BLIND" $QUEUE
##
#### SIDEBAND: MC fakes (1LNT)
##python susy-interface/plotmaker.py sos2l vvLow $T $O -l $RL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched_.*" -o AR1F --flags "-X twoTight -E oneLNT --perBin $BLIND" $QUEUE
##python susy-interface/plotmaker.py sos2l vvMed $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched_.*" -o AR1F --flags "-X twoTight -E oneLNT --perBin $BLIND" $QUEUE
##
#### SIDEBAND: MC fakes (1LNT) WITH SCALE FACTOR APPLIED
##python susy-interface/plotmaker.py sos2l vvLow $T $O -l $RL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched1_.*" -o AR1Fsc --flags "-X twoTight -E oneLNT --perBin $BLIND" $QUEUE
##python susy-interface/plotmaker.py sos2l vvMed $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched1_.*" -o AR1Fsc --flags "-X twoTight -E oneLNT --perBin $BLIND" $QUEUE
##
#### SIDEBAND: MC fakes (2LNT)
##python susy-interface/plotmaker.py sos2l vvLow $T $O -l $RL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched_.*" -o AR2F --flags "-X twoTight -E twoLNT --perBin $BLIND" $QUEUE
##python susy-interface/plotmaker.py sos2l vvMed $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched_.*" -o AR2F --flags "-X twoTight -E twoLNT --perBin $BLIND" $QUEUE
##
#### SIDEBAND: MC fakes (2LNT) WITH SCALE FACTOR APPLIED
##python susy-interface/plotmaker.py sos2l vvLow $T $O -l $RL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched2_.*" -o AR2Fsc --flags "-X twoTight -E twoLNT --perBin $BLIND" $QUEUE
##python susy-interface/plotmaker.py sos2l vvMed $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched2_.*" -o AR2Fsc --flags "-X twoTight -E twoLNT --perBin $BLIND" $QUEUE




