#!/bin/bash

T="/data1/botta/trees_SOS_010217" ## do NOT give a trailing /
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-15_sos16_full"  ## do NOT give a trailing /

FL=35.9 ## med-MET and hig-MET
RL=33.2 ## low-MET
QUEUE="-j 4" #"-q all.q"
BLIND="-X blinding" #""

## python makeShapeCardsSusy.py susy-ewkino/crwz/mca_includesM17.txt susy-ewkino/crwz/cuts_crwz.txt 1 '1,0.5,1.5' susy-ewkino/crwz/systs_crwz.txt -P /pool/ciencias/HeppyTrees/RA7/Prod23Jan/ftsXuanNacho/skimsForNachov2 --Fs {P}/leptonJetReCleanerSusyEWK2L --Fs {P}/leptonBuilderEWK --FMCs {P}/bTagEventWeightFullSim2L  -j 20 -l 35.867 --s2v --tree treeProducerSusyMultilepton --mcc susy-ewkino/crwz/lepchoice-crwz-FO.txt --mcc susy-ewkino/mcc_triggerdefs.txt  -f   -p data -p prompt.* -p convs.* -p fakes_.* -p rares.*  -W 'puw_nInt_Moriond(nTrueInt)*getLepSF(LepGood1_conePt,LepGood1_eta,LepGood1_pdgId,1)*getLepSF(LepGood2_conePt,LepGood2_eta,LepGood2_pdgId,1)*getLepSF(LepGood3_conePt,LepGood3_eta,LepGood3_pdgId,1)*bTagWeight' --load-macro susy-ewkino/functionsSF.cc --load-macro susy-ewkino/functionsPUW.cc  --plotgroup fakes_appldata+=promptsub --plotgroup fakes_appldata_ewk_Up+=promptsub_ewk_Up --plotgroup fakes_appldata_ewk_Dn+=promptsub_ewk_Dn  --od ~/cardWZCRewk -o binWZ -b binWZ --sp prompt_WZ --neglist promptsub --neglist promptsub_ewk_Up --neglist promptsub_ewk_Dn


need to give --sp
also need to define a model "WZCR", "DYTTCR", "VVCR" 

## DY --sp prompt_dy --sp prompt_tt

## TT --sp prompt_dy --sp prompt_tt

## VV --sp prompt_VV ==> this already needs the TT and DY SFs included

## WZ --sp prompt_WZ



