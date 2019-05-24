import re, os, sys
from CMGTools.RootTools.samples.configTools import printSummary, mergeExtensions, doTestN
from CMGTools.RootTools.samples.autoAAAconfig import autoAAA
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
def byCompName(components, regexps):
    return [ c for c in components if any(re.match(r, c.name) for r in regexps) ]

year = int(getHeppyOption("year", "2018"))
analysis = getHeppyOption("analysis", "main")

if getHeppyOption("nanoPreProcessor"):
    if year == 2018:
        from CMGTools.RootTools.samples.samples_13TeV_RunIIAutumn18MiniAOD import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2018_MiniAOD import samples as allData
        from CMGTools.RootTools.samples.triggers_13TeV_DATA2018 import all_triggers as triggers
    elif year == 2017:
        from CMGTools.RootTools.samples.samples_13TeV_RunIIFall17MiniAOD import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2017 import dataSamples_31Mar2018 as allData
        from CMGTools.RootTools.samples.triggers_13TeV_DATA2017 import all_triggers as triggers
    elif year == 2016:
        from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv3 import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import dataSamples_17Jul2018 as allData
        from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import all_triggers as triggers
else:
    if year == 2018:
        from CMGTools.RootTools.samples.samples_13TeV_RunIIAutumn18NanoAODv4 import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2018_NanoAOD import samples as allData
        from CMGTools.RootTools.samples.triggers_13TeV_DATA2018 import all_triggers as triggers
    elif year == 2017:
        from CMGTools.RootTools.samples.samples_13TeV_RunIIFall17NanoAODv4 import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2017_NanoAOD import samples as allData
        from CMGTools.RootTools.samples.triggers_13TeV_DATA2017 import all_triggers as triggers
    elif year == 2016:
        from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16NanoAODv4 import samples as mcSamples_
        from CMGTools.RootTools.samples.samples_13TeV_DATA2016_NanoAOD import samples as allData
        from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import all_triggers as triggers


DatasetsAndTriggers = []
if year == 2018:
    if analysis == "main":
        mcSamples = byCompName(mcSamples_, [
            "T_tWch_noFullyHad$",
            "TBar_tWch_noFullyHad$",

            "DYJetsToLL_M4to50_HT70to100",
            "DYJetsToLL_M4to50_HT100to200",
            "DYJetsToLL_M4to50_HT200to400",
            "DYJetsToLL_M4to50_HT400to600",
            "DYJetsToLL_M4to50_HT600toInf",

            "DYJetsToLL_M50_HT100to200",
            "DYJetsToLL_M50_HT200to400",
            "DYJetsToLL_M50_HT400to600," 
            "DYJetsToLL_M50_HT400to600_ext2",
            "DYJetsToLL_M50_HT600to800",
            "DYJetsToLL_M50_HT800to1200",
            #"DYJetsToLL_M50_HT1200to2500",
            "DYJetsToLL_M50_HT2500toInf",

            "TTJets_DiLepton$",

            #check if VVTo2L2Nu is there
            "WWTo2L2Nu$",
            "ZZTo2L2Nu",
            "TTJets_SingleLeptonFromT$", "TTJets_SingleLeptonFromTbar$", 
            
            "WJetsToLNu_HT100to200",
            "WJetsToLNu_HT200to400",
            "WJetsToLNu_HT400to600",
            "WJetsToLNu_HT600to800",
            "WJetsToLNu_HT800to1200",
            "WJetsToLNu_HT1200to2500",
            "WJetsToLNu_HT2500toInf",

            "WZTo3LNu_fxfx$",
            "WWToLNuQQ",
            #"WZTo1L1Nu2Q",
            "ZZTo4L$",
            "WWW",#_4F
            "WZZ$",
            "WWZ", #FIX! not _4F
            "ZZZ$",
            "T_tch$",
            "TBar_tch$",
            "T_sch_lep$",
            #"WWTo2L2Nu_DPS_hpp",           
            "TTWToLNu_fxfx$",
            "TTZToLLNuNu_amc$",
            "TTZToLLNuNu_m1to10$",
            "TTGJets$",
            "TGJets_lep", 

            #missing tbc
#            "ZZTo2L2Q," 
            "WpWpJJ",
#            "WZTo1L3Nu",
#            "WGToLNuG_amcatnlo_ext",
#            "ZGTo2LG_ext",
#            "WZTo2L2Q",

            ##signal SUSY
            "SMS_TChiWZ"
            
##relics from tth             
##            "TT[WZ]_LO$",
##            "TTHnobb_pow$",
##            "TZQToLL$", "tWll$", "TTTT$", "TTWW$",
##            "WpWpJJ$",
##            "GGHZZ4L$", "VHToNonbb_ll$",
##            "WWW_ll$", "WWZ$", "WZG$",  "WW_DPS$", 
            

        ])

    if analysis == "main":
##        DatasetsAndTriggers.append( ("DoubleMuon", triggers["mumu_iso"] + triggers["3mu"]) )
        DatasetsAndTriggers.append( ("DoubleMuon", triggers["SOS_doublemulowMET"] + triggers["mumu_iso"] + triggers["3mu"]) )
        DatasetsAndTriggers.append( ("MET",     triggers["SOS_highMET"] ) )
##        DatasetsAndTriggers.append( ("SingleMuon", triggers["1mu_iso"]) ) ##which one?? ##PD SingleMuon o MET?
##conf db e cercare stream dato il nome del trigger

elif year == 2017:
    mcSamples = byCompName(mcSamples_ [
##        "DYJetsToLL_M50$", "TT(Lep|Semi)_pow", "TTHnobb_pow",
        
        ##main bkgs
        "T_tWch_noFullyHad", "TBar_tWch_noFullyHad",

        "DYJetsToLL_M4to50_HT70to100," 
        "DYJetsToLL_M4to50_HT70to100_ext1",
        "DYJetsToLL_M4to50_HT100to200,   " 
        "DYJetsToLL_M4to50_HT100to200_ext1",
        "DYJetsToLL_M4to50_HT200to400",
        "DYJetsToLL_M4to50_HT200to400_ext1",
        "DYJetsToLL_M4to50_HT400to600",
        "DYJetsToLL_M4to50_HT400to600_ext1",
        "DYJetsToLL_M4to50_HT600toInf",

        "DYJetsToLL_M50_HT100to200," 
        "DYJetsToLL_M50_HT100to200_ext1",
        "DYJetsToLL_M50_HT200to400",
        "DYJetsToLL_M50_HT200to400_ext1",
        "DYJetsToLL_M50_HT400to600",
        "DYJetsToLL_M50_HT400to600_ext1",
        "DYJetsToLL_M50_HT600to800",
        "DYJetsToLL_M50_HT800to1200",
        "DYJetsToLL_M50_HT1200to2500",
        "DYJetsToLL_M50_HT2500toInf",

        "TTJets_DiLepton",

        #main VV
        "WWTo2L2Nu",
        "ZZTo2L2Nu",

        #fakesbkg
        "TTJets_SingleLeptonFromT",
        "TTJets_SingleLeptonFromTbar",

        "WJetsToLNu_HT100to200",
        "WJetsToLNu_HT200to400",
        "WJetsToLNu_HT400to600",
        "WJetsToLNu_HT600to800",
        "WJetsToLNu_HT800to1200",
        "WJetsToLNu_HT1200to2500",
        "WJetsToLNu_HT2500toInf",

        #rarebkg
        "WZTo3LNu_fxfx",
        "WWToLNuQQ",
        "WZTo1L1Nu2Q",
        "ZZTo4L",
        "WWW", #_4F
        "WZZ",
        "WWZ", #_4F
        "ZZZ",
        "T_tch",
        "TBar_tch",
        "T_sch_lep",
        "WWTo2L2Nu_DPS_hpp",
        "TTWToLNu_fxfx",
        "TTZToLLNuNu_amc",
        "TTZToLLNuNu_m1to10",
        "TTGJets",
        "TGJets_lep"

#more to be included
#            "ZZTo2L2Q," 
            "WpWpJJ",
#            "WZTo1L3Nu",
#            "WGToLNuG_amcatnlo_ext",
#            "ZGTo2LG_ext",
#            "WZTo2L2Q",


        ##signal SUSY
        "SMS_TChiWZ"

    ])

    DatasetsAndTriggers.append( ("DoubleMuon", triggers["SOS_doublemulowMET"] + triggers["mumu_iso"] + triggers["3mu"]) )
    DatasetsAndTriggers.append( ("MET",     triggers["SOS_highMET"] ) )

elif year == 2016:
    mcSamples = byCompName(mcSamples_, [


        ##main bkgs
        "T_tWch_noFullyHad", #extensions are to be included?
        "TBar_tWch_noFullyHad",

        "DYJetsToLL_M5to50_HT100to200",
        "DYJetsToLL_M5to50_HT100to200_ext",
        "DYJetsToLL_M5to50_HT200to400",
        "DYJetsToLL_M5to50_HT200to400_ext",
        "DYJetsToLL_M5to50_HT400to600",
        "DYJetsToLL_M5to50_HT400to600_ext",
        "DYJetsToLL_M5to50_HT600toInf",
        "DYJetsToLL_M5to50_HT600toInf_ext",
##        "DYJetsToLL_M4to50_HT70to100," 
##        "DYJetsToLL_M4to50_HT70to100_ext1",
##        "DYJetsToLL_M4to50_HT100to200,   " 
##        "DYJetsToLL_M4to50_HT100to200_ext1",
##        "DYJetsToLL_M4to50_HT200to400",
##        "DYJetsToLL_M4to50_HT200to400_ext1",
##        "DYJetsToLL_M4to50_HT400to600",
##        "DYJetsToLL_M4to50_HT400to600_ext1",
##        "DYJetsToLL_M4to50_HT600toInf",


        "DYJetsToLL_M50_HT70to100", 
        "DYJetsToLL_M50_HT100to200",
        "DYJetsToLL_M50_HT100to200_ext",
        "DYJetsToLL_M50_HT200to400",
        "DYJetsToLL_M50_HT200to400_ext",
        "DYJetsToLL_M50_HT400to600",
        "DYJetsToLL_M50_HT400to600_ext",
        "DYJetsToLL_M50_HT600to800",
        "DYJetsToLL_M50_HT800to1200",
        "DYJetsToLL_M50_HT1200to2500",
        "DYJetsToLL_M50_HT2500toInf",
#        "DYJetsToLL_M50_HT100to200," 
#        "DYJetsToLL_M50_HT100to200_ext1",
#        "DYJetsToLL_M50_HT200to400",
#        "DYJetsToLL_M50_HT200to400_ext1",
#        "DYJetsToLL_M50_HT400to600",
#        "DYJetsToLL_M50_HT400to600_ext1",
#        "DYJetsToLL_M50_HT600to800",
#        "DYJetsToLL_M50_HT800to1200",
#        "DYJetsToLL_M50_HT1200to2500",
#        "DYJetsToLL_M50_HT2500toInf",

        "TTJets_DiLepton",

        #main VV
        "WWTo2L2Nu",
        "ZZTo2L2Nu",

        #fakesbkg
        "TTJets_SingleLeptonFromT",
        "TTJets_SingleLeptonFromTbar",

        "WJetsToLNu_HT70to100",
        "WJetsToLNu_HT100to200",
        "WJetsToLNu_HT100to200_ext",
        "WJetsToLNu_HT100to200_ext2",
        "WJetsToLNu_HT200to400",
        "WJetsToLNu_HT200to400_ext",
        "WJetsToLNu_HT200to400_ext2",
        "WJetsToLNu_HT400to600",
        "WJetsToLNu_HT400to600_ext",
        "WJetsToLNu_HT600to800",
        "WJetsToLNu_HT600to800_ext",
        "WJetsToLNu_HT800to1200",
        "WJetsToLNu_HT800to1200_ext",
        "WJetsToLNu_HT1200to2500",
        "WJetsToLNu_HT1200to2500_ext",
        "WJetsToLNu_HT2500toInf",
        "WJetsToLNu_HT2500toInf_ext",
##        "WJetsToLNu_HT100to200",
##        "WJetsToLNu_HT200to400",
##        "WJetsToLNu_HT400to600",
##        "WJetsToLNu_HT600to800",
##        "WJetsToLNu_HT800to1200",
##        "WJetsToLNu_HT1200to2500",
##        "WJetsToLNu_HT2500toInf",

        #rarebkg
        "WZTo3LNu_fxfx",
        "WWToLNuQQ",
        "WZTo1L1Nu2Q",
        "ZZTo4L",
        "WWW", #_4F
        "WZZ",
        "WWZ", #why not _4F?
        "ZZZ",
        "T_tch",
        "TBar_tch",
        "T_sch_lep",
##        "WWTo2L2Nu_DPS_hpp", #missing
        "TTWToLNu", "TTWToLNu_ext",  #_fxfx
        "TTZToLLNuNu", "TTZToLLNuNu_ext", "TTZToLLNuNu_ext2", #_amc
        "TTZToLLNuNu_m1to10",
        "TTGJets", "TTGJets_ext"
       # "TGJets_lep" #missing

#more to be included
        "ZZTo2L2Q," 
        "WpWpJJ",
        "WZTo1L3Nu",
        "WGToLNuG_amcatnlo",
        "WGToLNuG_amcatnlo_ext",
        "ZGTo2LG",
        "WZTo2L2Q",


        ##signal SUSY
        "SMS_TChiWZ"

###        "DYJetsToLL_M50$", "TT(Lep|Semi)_pow" 
    ])
    DatasetsAndTriggers.append( ("DoubleMuon", triggers["SOS_doublemulowMET"] + triggers["mumu_iso"] + triggers["3mu"]) )
    DatasetsAndTriggers.append( ("MET",     triggers["SOS_highMET"] ) )
# make MC
mcTriggers = sum((trigs for (pd,trigs) in DatasetsAndTriggers), [])
for comp in mcSamples:
    comp.triggers = mcTriggers

# make data
dataSamples = []; vetoTriggers = []
for pd, triggers in DatasetsAndTriggers:
    for comp in byCompName(allData, [pd]):
        comp.triggers = triggers[:]
        comp.vetoTriggers = vetoTriggers[:]
        dataSamples.append(comp)
    vetoTriggers += triggers[:]

selectedComponents = mcSamples + dataSamples
if getHeppyOption('selectComponents'):
    selectedComponents = byCompName(selectedComponents, getHeppyOption('selectComponents').split(","))
autoAAA(selectedComponents, quiet=not(getHeppyOption("verboseAAA",False)))
selectedComponents, _ = mergeExtensions(selectedComponents)

# create and set preprocessor if requested
if getHeppyOption("nanoPreProcessor"):
    from CMGTools.Production.nanoAODPreprocessor import nanoAODPreprocessor
    preproc_cfg = {2016: ("mc94X2016","data94X2016"),
                   2017: ("mc94Xv2","data94Xv2"),
                   2018: ("mc102X","data102X_ABC","data102X_D")}
    preproc_cmsswArea = "/afs/cern.ch/user/v/vtavolar/work/SusySOSSW_2_clean/nanoAOD/CMSSW_10_2_14"
    preproc_mc = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,preproc_cfg[year][0]),cmsswArea=preproc_cmsswArea,keepOutput=True)
    if year==2018:
        preproc_data_ABC = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,preproc_cfg[year][1]),cmsswArea=preproc_cmsswArea,keepOutput=True)
        preproc_data_D = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,preproc_cfg[year][2]),cmsswArea=preproc_cmsswArea,keepOutput=True)
        for comp in selectedComponents:
            if comp.isData:
                comp.preprocessor = preproc_data_D if '2018D' in comp.name else preproc_data_ABC
            else:
                comp.preprocessor = preproc_mc
    else:
        preproc_data = nanoAODPreprocessor(cfg='%s/src/PhysicsTools/NanoAOD/test/%s_NANO.py'%(preproc_cmsswArea,preproc_cfg[year][1]),cmsswArea=preproc_cmsswArea,keepOutput=True)
        for comp in selectedComponents:
            comp.preprocessor = preproc_data if comp.isData else preproc_mc

# print summary of components to process
if getHeppyOption("justSummary"): 
    printSummary(selectedComponents)
    sys.exit(0)

from CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules import *

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

# in the cut string, keep only the main cuts to have it simpler
modules = ttH_sequence_step1
conf = dict(
    muPt = 5, 
    elePt = 7, 
    #        miniRelIso = 0.4,  # we use Iperbolic, see old cfg run_susySOS_cfg.py
    sip3d = 2.5, 
    dxy =  0.05, 
    dz = 0.1, 
    minMet = 50.,
    ip3d = 0.0175,
    iperbolic_iso_0 = 20.,
    iperbloic_iso_1 = 300.,
    eleId = "mvaFall17V2noIso_WPL", ## CHECK
)
cut =  ("nMuon + nElectron >= 2 &&" + ##if heppy option fast
        "MET_pt > {minMet}"
       "Sum$(Muon_pt > {muPt} && Muon_sip3d < {sip3d}) +"
       "Sum$(Electron_pt > {muPt}  && Electron_sip3d < {sip3d} && Electron_{eleId}) >= 2").format(**conf) ## && Muon_miniPFRelIso_all < {miniRelIso} && Electron_miniPFRelIso_all < {miniRelIso}  #mettere qui MET_pt>50 #cp dal cfg la selezione
#cut  = ttH_skim_cut
muonSelection     = lambda l : abs(l.eta) < 2.4 and l.pt > conf["muPt"]  and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"]  and l.relIso03*l.pt < ( conf["iperbolic_iso_0"]+conf["iperbolic_iso_1"]/l.pt) and abs(l.ip3D) < conf["ip3d"] ##is it relIso03?  ##and l.miniPFRelIso_all < conf["miniRelIso"]
electronSelection = lambda l : abs(l.eta) < 2.5 and l.pt > conf["elePt"]  and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"] and l.relIso03*l.pt < ( conf["iperbolic_iso_0"]+conf["iperbolic_iso_1"]/l.pt) and abs(l.ip3D) < conf["ip3d"] ##is it relIso03? ##and l.miniPFRelIso_all < conf["miniRelIso"]

from CMGTools.TTHAnalysis.tools.nanoAOD.ttHPrescalingLepSkimmer import ttHPrescalingLepSkimmer
# NB: do not wrap lepSkim a lambda, as we modify the configuration in the cfg itself 
lepSkim = ttHPrescalingLepSkimmer(5, 
                                  muonSel = muonSelection, electronSel = electronSelection,
                                  minLeptonsNoPrescale = 2, # things with less than 2 leptons are rejected irrespectively of the prescale
                                  prescaleFactor = 1, ##do not apply prescale ##does it do any skimming then?
                                  minLeptons = 2, requireSameSignPair = False,
                                  jetSel = lambda j : j.pt > 25 and abs(j.eta) < 2.4, 
                                  minJets = 0, minMET = 0)

from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
lepMerge = collectionMerger(input = ["Electron","Muon"], 
                            output = "LepGood", 
                            selector = dict(Muon = muonSelection, Electron = electronSelection))

from CMGTools.TTHAnalysis.tools.nanoAOD.ttHLeptonCombMasses import ttHLeptonCombMasses
lepMasses = ttHLeptonCombMasses( [ ("Muon",muonSelection), ("Electron",electronSelection) ], maxLeps = 4)

from CMGTools.TTHAnalysis.tools.nanoAOD.autoPuWeight import autoPuWeight
from CMGTools.TTHAnalysis.tools.nanoAOD.yearTagger import yearTag
from CMGTools.TTHAnalysis.tools.nanoAOD.xsecTagger import xsecTag
from CMGTools.TTHAnalysis.tools.nanoAOD.lepJetBTagAdder import lepJetBTagCSV, lepJetBTagDeepCSV

ttH_sequence_step1 = [lepSkim, lepMerge, autoPuWeight, yearTag, xsecTag, lepJetBTagCSV, lepJetBTagDeepCSV, lepMasses]


if analysis == "frqcd":
    modules = ttH_sequence_step1_FR
    cut = ttH_skim_cut_FR 

branchsel_in = os.environ['CMSSW_BASE']+"/src/CMGTools/TTHAnalysis/python/tools/nanoAOD/branchsel_in.txt"
branchsel_out = None
compression = "ZLIB:3" #"LZ4:4" #"LZMA:9"

POSTPROCESSOR = PostProcessor(None, [], modules = modules,
        cut = cut, prefetch = True, longTermCache = True,
        branchsel = branchsel_in, outputbranchsel = branchsel_out, compression = compression)

test = getHeppyOption("test")
if test == "94X-MC":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
    TTLep_pow.files = ["/afs/cern.ch/user/g/gpetrucc/cmg/NanoAOD_94X_TTLep.root"]
    lepSkim.requireSameSignPair = False
    lepSkim.minJets = 0
    lepSkim.minMET = 0
    lepSkim.prescaleFactor = 0
    selectedComponents = [TTLep_pow]
elif test == "94X-MC-miniAOD":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
    TTLep_pow.files = [ 'root://cms-xrd-global.cern.ch//store/mc/RunIIFall17MiniAOD/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/70000/3CC234EB-44E0-E711-904F-FA163E0DF774.root' ]
    localfile = os.path.expandvars("/tmp/$USER/%s" % os.path.basename(TTLep_pow.files[0]))
    if os.path.exists(localfile): TTLep_pow.files = [ localfile ] 
    from CMGTools.Production.nanoAODPreprocessor import nanoAODPreprocessor
    TTLep_pow.preprocessor = nanoAODPreprocessor("/afs/cern.ch/work/g/gpetrucc/ttH/CMSSW_10_4_0/src/nanov4_NANO_cfg.py")
    selectedComponents = [TTLep_pow]
elif test == "102X-MC":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2), useAAA=True )
    TTLep_pow.files = TTLep_pow.files[:1]
    selectedComponents = [TTLep_pow]
elif test in ('2','3','3s'):
    doTestN(test, selectedComponents)
