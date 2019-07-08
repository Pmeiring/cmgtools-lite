conf = dict(
    muPt = 3, 
    elePt = 5, 
    #        miniRelIso = 0.4,  # we use Iperbolic, see old cfg run_susySOS_cfg.py
    sip3d = 2.5, 
    dxy =  0.05, 
    dz = 0.1, 
    minMet = 50.,
    ip3d = 0.0175,
    iperbolic_iso_0 = 20.,
    iperbolic_iso_1 = 300.,
    eleId = "mvaFall17V2noIso_WPL", ## CHECK
)
susySOS_skim_cut =  ("nMuon + nElectron >= 2 &&" + ##if heppy option fast
        "MET_pt > {minMet}  &&"+
       "Sum$(Muon_pt > {muPt} && Muon_sip3d < {sip3d}) +"
       "Sum$(Electron_pt > {elePt}  && Electron_sip3d < {sip3d} && Electron_{eleId}) >= 2").format(**conf) ## && Muon_miniPFRelIso_all < {miniRelIso} && Electron_miniPFRelIso_all < {miniRelIso}  #mettere qui MET_pt>50 #cp dal cfg la selezione
#cut  = ttH_skim_cut
muonSelection     = lambda l : abs(l.eta) < 2.4 and l.pt > conf["muPt"]  and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"]  and l.pfRelIso03_all*l.pt < ( conf["iperbolic_iso_0"]+conf["iperbolic_iso_1"]/l.pt) and abs(l.ip3d) < conf["ip3d"] ##is it relIso03?  ##and l.miniPFRelIso_all < conf["miniRelIso"]##l.relIso03*l.pt
electronSelection = lambda l : abs(l.eta) < 2.5 and l.pt > conf["elePt"]  and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"] and l.pfRelIso03_all*l.pt < ( conf["iperbolic_iso_0"]+conf["iperbolic_iso_1"]/l.pt) and abs(l.ip3d) < conf["ip3d"] ##is it relIso03? ##and l.miniPFRelIso_all < conf["miniRelIso"] #l.relIso03*l.pt

#muonSelection     = lambda l : abs(l.eta) < 2.4 and l.pt > conf["muPt"]  and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"]  and ( ( l.pfIsolationR03.sumChargedHadronPt + max( l.pfIsolationR03.sumNeutralHadronEt +  l.pfIsolationR03.sumPhotonEt -  l.pfIsolationR03.sumPUPt/2,0.0) ) < ( conf["iperbolic_iso_0"]+conf["iperbolic_iso_1"]/l.pt)) and abs(l.ip3D) < conf["ip3d"] ##is it relIso03?  ##and l.miniPFRelIso_all < conf["miniRelIso"]##l.relIso03*l.pt
#electronSelection = lambda l : abs(l.eta) < 2.5 and l.pt > conf["elePt"]  and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"] and ( (l.chargedHadronIsoR(0.3) + max(l.neutralHadronIsoR(0.3)+l.photonIsoR(0.3)-l.rho*ele.EffectiveArea03,0)) < ( conf["iperbolic_iso_0"]+conf["iperbolic_iso_1"]/l.pt) ) and abs(l.ip3D) < conf["ip3d"] ##is it relIso03? ##and l.miniPFRelIso_all < conf["miniRelIso"] #l.relIso03*l.pt

from CMGTools.TTHAnalysis.tools.nanoAOD.ttHPrescalingLepSkimmer import ttHPrescalingLepSkimmer
# NB: do not wrap lepSkim a lambda, as we modify the configuration in the cfg itself 
lepSkim = ttHPrescalingLepSkimmer(0, ##do not apply prescale
                                  muonSel = muonSelection, electronSel = electronSelection,
                                  minLeptonsNoPrescale = 2, # things with less than 2 leptons are rejected irrespectively of the prescale
                                  minLeptons = 2, requireSameSignPair = False,
                                  jetSel = lambda j : j.pt > 25 and abs(j.eta) < 2.4  and j.jetId > 0, 
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

susySOS_sequence_step1 = [lepSkim, lepMerge, autoPuWeight, yearTag, xsecTag, lepJetBTagCSV, lepJetBTagDeepCSV, lepMasses]


#==== 
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from CMGTools.TTHAnalysis.tools.nanoAOD.ttHLepQCDFakeRateAnalyzer import ttHLepQCDFakeRateAnalyzer
lepFR = ttHLepQCDFakeRateAnalyzer(jetSel = lambda j : j.pt > 25 and abs(j.eta) < 2.4,
                                  pairSel = lambda pair : deltaR(pair[0].eta, pair[0].phi, pair[1].eta, pair[1].phi) > 0.7,
                                  maxLeptons = 1, requirePair = True)

#susySOS_sequence_step1_FR = [m for m in susySOS_sequence_step1 if m != lepSkim] + [ lepFR ]
#ttH_skim_cut_FR = ("nMuon + nElectron >= 1 && nJet >= 1 && Sum$(Jet_pt > 25 && abs(Jet_eta)<2.4) >= 1 &&" + 
#       "Sum$(Muon_pt > {muPt} && Muon_miniPFRelIso_all < {miniRelIso} && Muon_sip3d < {sip3d}) +"
#       "Sum$(Electron_pt > {muPt} && Electron_miniPFRelIso_all < {miniRelIso} && Electron_sip3d < {sip3d} && Electron_{eleId}) >= 1").format(**conf)


#==== items below are normally run as friends ====

def ttH_idEmu_cuts_E3(lep):
    if (abs(lep.pdgId)!=11): return True
    if (lep.hoe>=(0.10-0.00*(abs(lep.eta+lep.deltaEtaSC)>1.479))): return False
    if (lep.eInvMinusPInv<=-0.04): return False
    if (lep.sieie>=(0.011+0.019*(abs(lep.eta+lep.deltaEtaSC)>1.479))): return False
    return True

def conept_TTH(lep):
    if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13): return lep.pt
    if (abs(lep.pdgId)!=13 or lep.mediumId>0) and lep.mvaTTH > 0.90: return lep.pt
    else: return 0.90 * lep.pt * (1 + lep.jetRelIso)


def clean_and_FO_selection_TTH(lep):
    return lep.conept>10 and lep.jetBTagDeepCSV<0.4941 and (abs(lep.pdgId)!=11 or ttH_idEmu_cuts_E3(lep)) \
        and (lep.mvaTTH>0.90 or \
             (abs(lep.pdgId)==13 and lep.jetBTagDeepCSV<0.07 and lep.segmentComp>0.3 and 1/(1 + lep.jetRelIso)>0.60) or \
             (abs(lep.pdgId)==11 and lep.jetBTagDeepCSV<0.07 and lep.mvaFall17V1noIso>0.5 and 1/(1 + lep.jetRelIso)>0.60)) 

import numpy
from numpy import log
def calculateRawMVA(score):
    if score == -1.:
        return -999.
    elif score == 1.:
        return 999.
    else:
        return -0.5*numpy.log((1-score)/(1+score))


def SOSTightID2018(lep):
    if (lep.pt < 10): ##loose at low pt
        return lep.mvaFall17V2noIso_WPL
    else: #susy tight at higher, from https://twiki.cern.ch/twiki/pub/CMS/SUSLeptonSF/Run2_SUSYwp_EleCB_MVA_8Jan19.pdf
        mvaRaw = calculateRawMVA(lep.mvaFall17V2noIso)
        if abs(lep.eta<0.8):
            if lep.pt<25:
                return mvaRaw > 4.277 + 0.112*(lep.pt - 25)
            else:
                return mvaRaw > 4.277
        elif abs(lep.eta>=0.8) and abs(lep.eta<1.479):
            if lep.pt<25:
                return mvaRaw > 3.152 + 0.60*(lep.pt - 25)
            else:
                return mvaRaw > 3.152
        elif abs(lep.eta>=1.479):
            if lep.pt<25:
                return mvaRaw > 2.359 + 0.89*(lep.pt - 25)
            else:
                return mvaRaw > 2.359




clean_and_FO_selection_SOS = lambda lep : lep.jetBTagCSV < 0.46 ##using std csv, what about deep?

##tightLeptonSel = lambda lep : clean_and_FO_selection_TTH(lep) and (abs(lep.pdgId)!=13 or lep.mediumId>0) and lep.mvaTTH > 0.90
tightLeptonSel_SOS = lambda lep : clean_and_FO_selection_SOS(lep) and ((abs(lep.pdgId)==13 or SOSTightID2018(lep) ) and lep.pfRelIso03_all<0.5 and (lep.pfRelIso03_all*lep.pt)<5. and abs(lep.ip3d)<0.01 and lep.sip3d<2)


# (abs(lep.pdgId)!=13 or lep.mediumId>0) and lep.mvaTTH > 0.90






from CMGTools.TTHAnalysis.tools.functionsTTH import tauID_oldDMdR0p3wLT2017v2_WP # FIXME get rid of this after validation
foTauSel = lambda tau: False #tau.pt > 20 and abs(tau.eta)<2.3 and abs(tau.dxy) < 1000 and abs(tau.dz) < 0.2 and tauID_oldDMdR0p3wLT2017v2_WP(tau.pt,tau.rawMVAoldDMdR032017v2,1) and tau.idDecayMode
tightTauSel = lambda tau: False #tauID_oldDMdR0p3wLT2017v2_WP(tau.pt,tau.rawMVAoldDMdR032017v2,2)

from CMGTools.TTHAnalysis.tools.combinedObjectTaggerForCleaning import CombinedObjectTaggerForCleaning
from CMGTools.TTHAnalysis.tools.nanoAOD.fastCombinedObjectRecleaner import fastCombinedObjectRecleaner
recleaner_step1 = lambda : CombinedObjectTaggerForCleaning("InternalRecl",
                                       #looseLeptonSel = lambda lep : lep.miniPFRelIso_all < 0.4 and lep.sip3d < 8,
                                       cleaningLeptonSel = clean_and_FO_selection_SOS,
                                       FOLeptonSel = clean_and_FO_selection_SOS,
                                       tightLeptonSel = tightLeptonSel_SOS,
                                       FOTauSel = foTauSel,
                                       tightTauSel = tightTauSel,
                                       selectJet = lambda jet: abs(jet.eta)<2.4 and jet.pt > 25 and jet.jetId > 0, # FIXME need to select on pt or ptUp or ptDown
                                       coneptdef = lambda lep: conept_TTH(lep))
recleaner_step2_mc = lambda : fastCombinedObjectRecleaner(label="Recl", inlabel="_InternalRecl",
                                       cleanTausWithLooseLeptons=True,
                                       cleanJetsWithFOTaus=True,
                                       doVetoZ=False, doVetoLMf=False, doVetoLMt=False,
                                       jetPts=[25,40],
                                       jetPtsFwd=[25,40],
                                       btagL_thr=0.1522,
                                       btagM_thr=0.4941,
                                       isMC = True)
recleaner_step2_data = lambda : fastCombinedObjectRecleaner(label="Recl", inlabel="_InternalRecl",
                                         cleanTausWithLooseLeptons=True,
                                         cleanJetsWithFOTaus=True,
                                         doVetoZ=False, doVetoLMf=False, doVetoLMt=False,
                                         jetPts=[25,40],
                                         jetPtsFwd=[25,40],
                                         btagL_thr=0.1522,
                                         btagM_thr=0.4941,
                                         isMC = False)

from CMGTools.TTHAnalysis.tools.eventVars_2lss import EventVars2LSS
eventVars = lambda : EventVars2LSS('','Recl', doSystJEC=False)

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import jetmetUncertainties2016, jetmetUncertainties2017, jetmetUncertainties2018

