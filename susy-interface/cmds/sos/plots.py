import datetime, os, ROOT

today = datetime.datetime.now().strftime("%Y-%m-%d")
#today = "2018-06-14"

## == configuration =================================

##tag  = "vtavolarTest_newFtrees_SR_bkgOnly_noHLT"
tag  = "vtavolarTest_cards_data"

pfx  = ""
#####pfx  = "_sc"

add  = ""
#add  = "--SP era2017"
#add = "--sP jetEta --sP nJet25Eta1p0 --sP nJet25Eta1p4 --sP nJet25Eta2p0"
#add  = "--sP yields --sP SR_.*"
#add  = "--sP lep1.*"
#add  = "--sP SR_2l_col_fine"

do = 0 ## only all plots
#do = 1 ## only SR cards
#do = 2 ## only cards for all plots

runBkgs = True
runSigs = True
model   = "TChiWZ"


## --------------------------------------------------

treedirs = {
            ###2016: "/data1/botta/trees_SOS_010217"  ,
###            2016: "/data1/cheidegg/trees_SOS_010217_skimmed",
            2016: "/afs/cern.ch/user/p/peruzzi/work/sostrees/trees_SOS_010217/;/afs/cern.ch/work/v/vtavolar/SusySOSSW_2_clean/CMSSW_8_0_25/src/CMGTools/TTHAnalysis/python/plotter;/afs/cern.ch/work/v/vtavolar/SusySOSSW_2_clean/CMSSW_8_0_25/src/CMGTools/TTHAnalysis/python/plotter/data1/botta/trees_SOS_010217;/data1/botta/trees_SOS_010217",
	    
##            2016: "/afs/cern.ch/user/v/vtavolar/SusySOS/cleanTest/CMSSW_8_0_25/src/CMGTools/TTHAnalysis/python/plotter/data1/botta/trees_SOS_010217/",
            ####2017: "/afs/cern.ch/user/v/vtavolar/SusySOS/cleanTest/CMSSW_8_0_25/src/CMGTools/TTHAnalysis/python/plotter/data1/peruzzi/trees_SOS_030518"         ,
	    2017: "/eos/cms/store/user/ipapaver/susySOS_trees_FixEE17;/afs/cern.ch/user/v/vtavolar/work/SusySOSSW_2_clean/CMSSW_8_0_25/src/CMGTools/TTHAnalysis/python/plotter/checkMETFix_bkgTrees"        , 
           }

plotdir  = "/afs/cern.ch/user/v/vtavolar/www/SusySOS"
carddir  = "/afs/cern.ch/user/v/vtavolar/work/SusySOS/cards"

scales = [
          #("_noSF", "--replInMccs mcc2016/mcc_sf_met125.txt:mcc_sf_met.txt --replInMccs mcc2016/mcc_sf_met200.txt:mcc_sf_met.txt --replInMccs mcc2017/mcc_sf_met125.txt:mcc_sf_met.txt --replInMccs mcc2017/mcc_sf_met200.txt:mcc_sf_met.txt"),
          ("", ""),
         ]

modes = {
         2: [
             ###("SR"       , "data;prompt_.*;rares;fakes_appldata"       , None                        ),
###             ("SRmc"     , "data;prompt_.*;rares;fakes_matched_.*"     , None                        ),
##		("SRmc"     , "prompt_.*;rares;fakes_matched_.*"     , None                        ),
             ("SRsemi"   , "data;prompt_.*;rares;fakes_applmcBoth"     , None                        ),
             #("AR"       , "data;prompt_.*;rares;fakes_matched_.*"     , "-X twoTight -E oneNotTight"),
             #("AR1F"     , "data;prompt_.*;rares;fakes_matched_.*"     , "-X twoTight -E oneLNT"     ),
             #("AR2F"     , "data;prompt_.*;rares;fakes_matched_.*"     , "-X twoTight -E twoLNT"     )
             #("AR_sc"    , "data;prompt_.*;rares;fakes_matchedBoth_.*" , "-X twoTight -E oneNotTight"),
             #("AR1F_sc"  , "data;prompt_.*;rares;fakes_matched1_.*"    , "-X twoTight -E oneLNT"     ),
             #("AR2F_sc"  , "data;prompt_.*;rares;fakes_matched2_.*"    , "-X twoTight -E twoLNT"     )
             #("closure"  , "fakes_matched_.*;fakes_applmcBoth"        , None                        ),
             #("closure1F", "fakes_matched1fake_.*;fakes_applmc1"      , None                        ),
             #("closure2F", "fakes_matched2fake_.*;fakes_applmc2"      , None                        ),
            ],
         3: [
             #("SR"       , "data;prompt_.*;rares;fakes_appldata"       , None                          ),
###             ("SRmc"     , "data;prompt_.*;rares;fakes_matched_.*"     , None                          ),
##		("SRmc"     , "prompt_.*;rares;fakes_matched_.*"     , None                          ),
             ("SRsemi"   , "data;prompt_.*;rares;fakes_applmcBoth"     , None                          ),
             #("AR"       , "data;prompt_.*;rares;fakes_matched_.*"     , "-X threeTight -E oneNotTight"),
             #("AR1F"     , "data;prompt_.*;rares;fakes_matched_.*"     , "-X threeTight -E oneLNT"     ),
             #("AR2F"     , "data;prompt_.*;rares;fakes_matched_.*"     , "-X threeTight -E twoLNT"     ),
             #("AR3F"     , "data;prompt_.*;rares;fakes_matched_.*"     , "-X threeTight -E threeLNT"   )
             #("AR_sc"    , "data;prompt_.*;rares;fakes_matchedBoth_.*" , "-X threeTight -E oneNotTight"),
             #("AR1F_sc"  , "data;prompt_.*;rares;fakes_matched1_.*"    , "-X threeTight -E oneLNT"     ),
             #("AR2F_sc"  , "data;prompt_.*;rares;fakes_matched2_.*"    , "-X threeTight -E twoLNT"     ),
             #("AR3F_sc"  , "data;prompt_.*;rares;fakes_matched3_.*"    , "-X threeTight -E threeLNT"   )
             #("closure"  , "fakes_sideband_.*;fakes_applmcBoth"        , None                          ),
             #("closure1F", "fakes_sideband1fake_.*;fakes_applmc1"      , None                          ),
             #("closure2F", "fakes_sideband2fake_.*;fakes_applmc2"      , None                          ),
             #("closure3F", "fakes_sideband3fake_.*;fakes_applmc3"      , None                          ),
            ],
        }

redlumi16 = 33.2
fullumi16 = 35.9
redlumi17 = 37.1
fullumi17 = 41.4

regions = [
           ("sos2l16", "2lss16"      , fullumi16, "sig_T2tt_.*"), \
           ("sos2l16", "2losEwkLow16", redlumi16, "sig_TChiWZ_.*"), \
           ("sos2l16", "2losEwkMed16", fullumi16, "sig_TChiWZ_.*"), \
           ("sos2l16", "2losEwkHig16", fullumi16, "sig_TChiWZ_.*"), \
           ("sos2l16", "2losColLow16", redlumi16, "sig_T2tt_.*"), \
           ("sos2l16", "2losColMed16", fullumi16, "sig_T2tt_.*"), \
           ("sos2l16", "2losColHig16", fullumi16, "sig_T2tt_.*"), \
           ####("sos3l16", "3lMin16"     , redlumi16, "sig_TChiWZ_.*"), \
           ("sos3l16", "3lLow16"     , redlumi16, "sig_TChiWZ_.*"), \
           ("sos3l16", "3lMed16"     , fullumi16, "sig_TChiWZ_.*"), \
           ("sos2l16", "dyLow16"     , redlumi16, "sig_T2tt_.*"), \
           ("sos2l16", "dyMed16"     , fullumi16, "sig_T2tt_.*"), \
           ("sos2l16", "ttLow16"     , redlumi16, "sig_T2tt_.*"), \
           ("sos2l16", "ttMed16"     , fullumi16, "sig_T2tt_.*"), \
           #("sos2l16", "vvLow16"     , redlumi16, "sig_TChiWZ_.*"), \
           #("sos2l16", "vvMed16"     , fullumi16, "sig_TChiWZ_.*"), \
           #("sos3l16", "wzMin16"     , fullumi16, "sig_TChiWZ_.*"), \
           #("sos3l16", "wzLow16"     , fullumi16, "sig_TChiWZ_.*"), \
           #("sos3l16", "wzMed16"     , fullumi16, "sig_TChiWZ_.*"), \

##           ("sos2l17", "2lss17"      , fullumi17, "sig_T2tt_.*"), \
##           ("sos2l17", "2losEwkLow17", redlumi17, "sig_TChiWZ_.*"), \
##           ("sos2l17", "2losEwkMed17", fullumi17, "sig_TChiWZ_.*"), \
##           ("sos2l17", "2losEwkHig17", fullumi17, "sig_TChiWZ_.*"), \
##           ("sos2l17", "2losColLow17", redlumi17, "sig_T2tt_.*"), \
##           ("sos2l17", "2losColMed17", fullumi17, "sig_T2tt_.*"), \
##           ("sos2l17", "2losColHig17", fullumi17, "sig_T2tt_.*"), \
##           ("sos3l17", "3lLow17"     , redlumi17, "sig_TChiWZ_.*"), \
##           ("sos3l17", "3lMed17"     , fullumi17, "sig_TChiWZ_.*"), \
##           ("sos2l17", "dyLow17"     , redlumi17, "sig_T2tt_.*"), \
##           ("sos2l17", "dyMed17"     , fullumi17, "sig_T2tt_.*"), \
##           ("sos2l17", "ttLow17"     , redlumi17, "sig_T2tt_.*"), \
##           ("sos2l17", "ttMed17"     , fullumi17, "sig_T2tt_.*"), \
##           ("sos2l17", "vvLow17"     , redlumi17, "sig_TChiWZ_.*"), \
##           ("sos2l17", "vvMed17"     , fullumi17, "sig_TChiWZ_.*"), \
##           ("sos3l17", "wzMin17"     , fullumi17, "sig_TChiWZ_.*"), \
##           ("sos3l17", "wzLow17"     , fullumi17, "sig_TChiWZ_.*"), \
##           ("sos3l17", "wzMed17"     , fullumi17, "sig_TChiWZ_.*"), \
          ]


###plotbase = "python susy-interface/plotmaker.py {C} {R} \"{T}\" {O} -l {L} --make datasig --plots all -o {S} --flags \"--perBin {F}\" {P} {A} -W '{W}' -j 8"
plotbase = "python susy-interface/plotmaker.py {C} {R} \"{T}\" {O} -l {L} --make bkgs --plots all -o {S} --flags \"--perBin {F}\" {P} {A} -W '{W}' -j 8"
cardbkgs = "python susy-interface/scanmaker.py {C} {R} \"{T}\" {O} -l {L} --models {M} -o {S} --bkgOnly --redoBkg --flags \"{F}\" --mca susy-sos-v1/{FS}/mca_sos_{YR}_forScan_sdd.txt -j 4"
cardsigs = "python susy-interface/scanmaker.py {C} {R} \"{T}\" {O} -l {L} --models {M} -o {S} --sigOnly --flags \"{F}\" --postfix '--postfix-pred fakes_applmcBoth*=fixFakePredictionForZeroEvts --frFile $CMSSW_BASE/src/CMGTools/TTHAnalysis/data/fakerate/{FR} --frMap FR_SOS_QCD_FL_data_comb --mpfr {R}' --mca susy-sos-v1/{FS}/mca_sos_{YR}_forScan_sdd.txt -j 4"


## == code ==========================================


## all plots
if do == 0:
	for region in regions:
		year = 2017 if region[0][-2:]=="17" else 2016
		shyr = "17" if year==2017           else "16"
		nlep = 3    if "3l" in region[0]    else 2
	
		for mode in modes[nlep]: 
			for scale in scales:
				out    = plotdir+"/"+today+"_sos"+shyr+"_"+tag
				procs  = "-p \""+mode[1]+";"+region[3]+"\"" if mode[1] else ""
				flags  = mode[2]+" "+add if mode[2] else add
				print plotbase.format(C=region[0], R=region[1], T=treedirs[year], O=out, L=region[2], S=mode[0]+scale[0]+pfx, F=flags, P=procs, A=scale[1], W="wBG")
				print 



## SR cards
if do == 1:
	association = {"2lss":"SRsemi", "2los":"SRsemi", "3l":"SRsemi", "dy":"SRmc", "tt":"SRmc", "wz":"SRmc"}
	#association = {"2lss":"SR", "2los":"SR", "3l":"SR", "dy":"SRmc", "tt":"SRmc", "wz":"SRmc"}

	for region in regions:

		if "vv" in region[1]: continue

		year = 2017 if region[0][-2:]=="17" else 2016
		shyr = "17" if year==2017           else "16"
		nlep = 3    if "3l" in region[0]    else 2

		for key,value in association.iteritems():
			if not key in region[1]: continue

			for mode in modes[nlep]:
				if not mode[0]==value: continue

				out    = carddir+"/"+today+"_sos"+shyr+"_"+tag
				flags  = mode[2]+" "+add if mode[2] else add

				## run Bkgs first
				if runBkgs:
					print cardbkgs.format(C=region[0], R=region[1], T=treedirs[year], O=out, L=region[2], M=model, S="SR", F=flags, FS=str(nlep)+"l", YR=str(year))
					print

				## run Sigs
				if runSigs:
					print cardsigs.format(C=region[0], R=region[1], T=treedirs[year], O=out, L=region[2], M=model, S="SR", F=flags, FR="FR_PR_SOS_v3.1.root", FS=str(nlep)+"l", YR=str(year))
					print 

## all cards for all plots
if do == 2:
	pass




## to do list:
## * check if this makes sense
## * update susy-interface including also MCA's and all that stuff, remove scale factor MCCs and unnecessary fake MCAs
## * write sumWZ.py script both for cards and plots
## * write scale.py script (combines CR cards, runs mlfit, prints SF, scales plots) -> all DY, TT, VV (no scaling), WZ
## * write prefit.py script (extracts prefit shapes and applies them to the plots, also plots the relative size of the uncertainty)
## * write postfit.py script (takes combined cards from SPM, runs mlfit, scales plots and uncertainties)




