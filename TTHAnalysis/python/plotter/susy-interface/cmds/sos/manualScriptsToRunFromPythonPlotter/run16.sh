###python susy-interface/plotmaker.py sos3l16 3lLow16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 33.2 --make datasig --plots all -o SR --flags "--perBin --sP yields --sP SR_.*" -p "prompt_.*;rares;fakes_appldata;sig_TChiWZ_.*"  -W 'wBG' -j 8
###
###python susy-interface/plotmaker.py sos3l16 3lLow16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 33.2 --make datasig --plots all -o SRmc --flags "--perBin --sP yields --sP SR_.*" -p "prompt_.*;rares;fakes_matched_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
##
###python susy-interface/plotmaker.py sos3l16 3lLow16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 33.2 --make datasig --plots all -o SRsemi --flags "--perBin --sP yields --sP SR_.*" -p "prompt_.*;rares;fakes_applmcBoth;sig_TChiWZ_.*"  -W 'wBG' -j 8

##python susy-interface/plotmaker.py sos3l16 3lLow16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 33.2 --make datasig --plots all -o AR_sc --flags "--perBin -X threeTight -E oneNotTight --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matchedBoth_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8

#python susy-interface/plotmaker.py sos3l16 3lLow16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 33.2 --make datasig --plots all -o AR1F_sc --flags "--perBin -X threeTight -E oneLNT --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched1_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
#
#python susy-interface/plotmaker.py sos3l16 3lLow16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 33.2 --make datasig --plots all -o AR2F_sc --flags "--perBin -X threeTight -E twoLNT --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched2_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
#
#python susy-interface/plotmaker.py sos3l16 3lLow16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 33.2 --make datasig --plots all -o AR3F_sc --flags "--perBin -X threeTight -E threeLNT --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched3_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8

###python susy-interface/plotmaker.py sos3l16 3lMed16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o SR --flags "--perBin --sP yields --sP SR_.*" -p "prompt_.*;rares;fakes_appldata;sig_TChiWZ_.*"  -W 'wBG' -j 8
###
###python susy-interface/plotmaker.py sos3l16 3lMed16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o SRmc --flags "--perBin --sP yields --sP SR_.*" -p "prompt_.*;rares;fakes_matched_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
###
###python susy-interface/plotmaker.py sos3l16 3lMed16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o SRsemi --flags "--perBin --sP yields --sP SR_.*" -p "prompt_.*;rares;fakes_applmcBoth;sig_TChiWZ_.*"  -W 'wBG' -j 8

python susy-interface/plotmaker.py sos3l16 3lMed16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o AR_sc --flags "--perBin -X threeTight -E oneNotTight --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matchedBoth_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8

#python susy-interface/plotmaker.py sos3l16 3lMed16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o AR1F_sc --flags "--perBin -X threeTight -E oneLNT --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched1_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
#
#python susy-interface/plotmaker.py sos3l16 3lMed16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o AR2F_sc --flags "--perBin -X threeTight -E twoLNT --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched2_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
#
#python susy-interface/plotmaker.py sos3l16 3lMed16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o AR3F_sc --flags "--perBin -X threeTight -E threeLNT --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched3_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8

#####python susy-interface/plotmaker.py sos3l16 wzMin16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o SRmc --flags "--perBin --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8

#python susy-interface/plotmaker.py sos3l16 wzMin16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o AR_sc --flags "--perBin -X twoTight -E oneNotTight --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matchedBoth_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
#
#python susy-interface/plotmaker.py sos3l16 wzMin16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o AR1F_sc --flags "--perBin -X twoTight -E oneLNT --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched1_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
#
#python susy-interface/plotmaker.py sos3l16 wzMin16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o AR2F_sc --flags "--perBin -X twoTight -E twoLNT --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched2_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
#
#python susy-interface/plotmaker.py sos3l16 wzMin16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o AR3F_sc --flags "--perBin -X twoTight -E threeLNT --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched3_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8

####python susy-interface/plotmaker.py sos3l16 wzLow16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o SRmc --flags "--perBin --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
#
#python susy-interface/plotmaker.py sos3l16 wzLow16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o AR_sc --flags "--perBin -X twoTight -E oneNotTight --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matchedBoth_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
#
#python susy-interface/plotmaker.py sos3l16 wzLow16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o AR1F_sc --flags "--perBin -X twoTight -E oneLNT --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched1_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
#
#python susy-interface/plotmaker.py sos3l16 wzLow16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o AR2F_sc --flags "--perBin -X twoTight -E twoLNT --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched2_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
#
#python susy-interface/plotmaker.py sos3l16 wzLow16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o AR3F_sc --flags "--perBin -X twoTight -E threeLNT --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched3_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
#
###python susy-interface/plotmaker.py sos3l16 wzMed16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o SRmc --flags "--perBin --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8

#python susy-interface/plotmaker.py sos3l16 wzMed16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o AR_sc --flags "--perBin -X twoTight -E oneNotTight --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matchedBoth_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
#
#python susy-interface/plotmaker.py sos3l16 wzMed16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o AR1F_sc --flags "--perBin -X twoTight -E oneLNT --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched1_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
#
#python susy-interface/plotmaker.py sos3l16 wzMed16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o AR2F_sc --flags "--perBin -X twoTight -E twoLNT --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched2_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
#
#python susy-interface/plotmaker.py sos3l16 wzMed16 "/data1/cheidegg/trees_SOS_010217_skimmed" /afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus -l 35.9 --make datasig --plots all -o AR3F_sc --flags "--perBin -X twoTight -E threeLNT --sP yields --sP SR_.*" -p "data;prompt_.*;rares;fakes_matched3_.*;sig_TChiWZ_.*"  -W 'wBG' -j 8
#
