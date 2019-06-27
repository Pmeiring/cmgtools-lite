#!/bin/bash

T="/data1/botta/trees_SOS_010217" ## do NOT give a trailing /
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-15_sos16_full"  ## do NOT give a trailing /

FL=35.9 ## med-MET and hig-MET
RL=33.2 ## low-MET
QUEUE="-j 4" #"-q all.q"
BLIND="-X blinding" #""


## 2L CR TT
## =================================================================


## Nominal (THESE ARE ALL SCALED!)
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

## default data-driven fakes
#python susy-interface/plotmaker.py sos2l ttLow $T $O -l $RL --make datasig --plots perCateg -o SR --flags "--perBin $BLIND" $QUEUE
#python susy-interface/plotmaker.py sos2l ttMed $T $O -l $FL --make datasig --plots perCateg -o SR --flags "--perBin $BLIND" $QUEUE

## fakes from MC
#python susy-interface/plotmaker.py sos2l ttLow $T $O -l $RL --make datasig --plots perCateg -o SRmc --flags "--perBin $BLIND" -p "data;prompt_.*;rares;fakes_matched_.*" $QUEUE
#python susy-interface/plotmaker.py sos2l ttMed $T $O -l $FL --make datasig --plots perCateg -o SRmc --flags "--perBin $BLIND" -p "data;prompt_.*;rares;fakes_matched_.*" $QUEUE

## semi-data-driven fakes
#python susy-interface/plotmaker.py sos2l ttLow $T $O -l $RL --make datasig --plots perCateg -o SRsemi --flags "--perBin $BLIND --plotgroup fakes_applmc1+=fakes_applmc2" -p "data;prompt_.*;rares;fakes_applmc1;fakes_applmc2" $QUEUE
#python susy-interface/plotmaker.py sos2l ttMed $T $O -l $FL --make datasig --plots perCateg -o SRsemi --flags "--perBin $BLIND --plotgroup fakes_applmc1+=fakes_applmc2" -p "data;prompt_.*;rares;fakes_applmc1;fakes_applmc2" $QUEUE



## Nominal (THESE ARE ALL UNSCALED!)
## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

## default data-driven fakes
#python susy-interface/plotmaker.py sos2l ttLow $T $O -l $RL --make datasig --plots perCateg -o SR_crus --flags "--perBin $BLIND" $QUEUE --mccs "susy-sos-v1/mcc_triggerdefs.txt;susy-sos-v1/crtt/mcc_tt_2016.txt;susy-sos-v1/mcc_sos.txt;susy-sos-v1/2l/mcc_sf_met.txt;susy-sos-v1/2l/mcc2016/mcc_sf_fakes_ttLow.txt"
#python susy-interface/plotmaker.py sos2l ttMed $T $O -l $FL --make datasig --plots perCateg -o SR_crus --flags "--perBin $BLIND" $QUEUE --mccs "susy-sos-v1/mcc_triggerdefs.txt;susy-sos-v1/crtt/mcc_tt_2016.txt;susy-sos-v1/mcc_sos.txt;susy-sos-v1/2l/mcc_sf_met.txt;susy-sos-v1/2l/mcc2016/mcc_sf_fakes_ttLow.txt"

## fakes from MC
python susy-interface/plotmaker.py sos2l ttLow $T $O -l $RL --make datasig --plots all -o SRmc_crus --flags "--perBin $BLIND" -p "data;prompt_.*;rares;fakes_matched_.*" $QUEUE --mccs "susy-sos-v1/mcc_triggerdefs.txt;susy-sos-v1/crtt/mcc_tt_2016.txt;susy-sos-v1/mcc_sos.txt;susy-sos-v1/2l/mcc_sf_met.txt;susy-sos-v1/2l/mcc2016/mcc_sf_fakes_ttLow.txt" -W '1.0*puw_nInt_Moriond(nTrueInt)'
#python susy-interface/plotmaker.py sos2l ttMed $T $O -l $FL --make datasig --plots all -o SRmc_crus --flags "--perBin $BLIND" -p "data;prompt_.*;rares;fakes_matched_.*" $QUEUE --mccs "susy-sos-v1/mcc_triggerdefs.txt;susy-sos-v1/crtt/mcc_tt_2016.txt;susy-sos-v1/mcc_sos.txt;susy-sos-v1/2l/mcc_sf_met.txt;susy-sos-v1/2l/mcc2016/mcc_sf_fakes_ttMed.txt"

## semi-data-driven fakes
#python susy-interface/plotmaker.py sos2l ttLow $T $O -l $RL --make datasig --plots perCateg -o SRsemi_crus --flags "--perBin $BLIND --plotgroup fakes_applmc1+=fakes_applmc2" -p "data;prompt_.*;rares;fakes_applmc1;fakes_applmc2" $QUEUE --mccs "susy-sos-v1/mcc_triggerdefs.txt;susy-sos-v1/crtt/mcc_tt_2016.txt;susy-sos-v1/mcc_sos.txt;susy-sos-v1/2l/mcc_sf_met.txt;susy-sos-v1/2l/mcc2016/mcc_sf_fakes_ttLow.txt"
#python susy-interface/plotmaker.py sos2l ttMed $T $O -l $FL --make datasig --plots perCateg -o SRsemi_crus --flags "--perBin $BLIND --plotgroup fakes_applmc1+=fakes_applmc2" -p "data;prompt_.*;rares;fakes_applmc1;fakes_applmc2" $QUEUE --mccs "susy-sos-v1/mcc_triggerdefs.txt;susy-sos-v1/crtt/mcc_tt_2016.txt;susy-sos-v1/mcc_sos.txt;susy-sos-v1/2l/mcc_sf_met.txt;susy-sos-v1/2l/mcc2016/mcc_sf_fakes_ttLow.txt"



#### Sideband
#### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
##
#### SIDEBAND: MC fakes
##python susy-interface/plotmaker.py sos2l ttLow $T $O -l $RL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched_.*" -o AR --flags "-X twoTight -E oneNotTight --perBin $BLIND" $QUEUE
##python susy-interface/plotmaker.py sos2l ttMed $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched_.*" -o AR --flags "-X twoTight -E oneNotTight --perBin $BLIND" $QUEUE
##
#### SIDEBAND: MC fakes WITH SCALE FACTORS APPLIED
##python susy-interface/plotmaker.py sos2l ttLow $T $O -l $RL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matchedBoth_.*" -o ARsc --flags "-X twoTight -E oneNotTight --perBin $BLIND" $QUEUE
##python susy-interface/plotmaker.py sos2l ttMed $T $O -l $RL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matchedBoth_.*" -o ARsc --flags "-X twoTight -E oneNotTight --perBin $BLIND" $QUEUE
##
#### SIDEBAND: MC fakes (1LNT)
##python susy-interface/plotmaker.py sos2l ttLow $T $O -l $RL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched_.*" -o AR1F --flags "-X twoTight -E oneLNT --perBin $BLIND" $QUEUE
##python susy-interface/plotmaker.py sos2l ttMed $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched_.*" -o AR1F --flags "-X twoTight -E oneLNT --perBin $BLIND" $QUEUE
##
#### SIDEBAND: MC fakes (1LNT) WITH SCALE FACTOR APPLIED
##python susy-interface/plotmaker.py sos2l ttLow $T $O -l $RL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched1_.*" -o AR1Fsc --flags "-X twoTight -E oneLNT --perBin $BLIND" $QUEUE
##python susy-interface/plotmaker.py sos2l ttMed $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched1_.*" -o AR1Fsc --flags "-X twoTight -E oneLNT --perBin $BLIND" $QUEUE
##
#### SIDEBAND: MC fakes (2LNT)
##python susy-interface/plotmaker.py sos2l ttLow $T $O -l $RL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched_.*" -o AR2F --flags "-X twoTight -E twoLNT --perBin $BLIND" $QUEUE
##python susy-interface/plotmaker.py sos2l ttMed $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched_.*" -o AR2F --flags "-X twoTight -E twoLNT --perBin $BLIND" $QUEUE
##
#### SIDEBAND: MC fakes (2LNT) WITH SCALE FACTOR APPLIED
##python susy-interface/plotmaker.py sos2l ttLow $T $O -l $RL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched2_.*" -o AR2Fsc --flags "-X twoTight -E twoLNT --perBin $BLIND" $QUEUE
##python susy-interface/plotmaker.py sos2l ttMed $T $O -l $FL --make datasig --plots perCateg -p "data;prompt_.*;rares;fakes_matched2_.*" -o AR2Fsc --flags "-X twoTight -E twoLNT --perBin $BLIND" $QUEUE





