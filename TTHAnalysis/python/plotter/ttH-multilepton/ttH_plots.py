#!/usr/bin/env python
import sys
import re

ODIR=sys.argv[1]
YEAR=sys.argv[2]
lumis = {
'2016': '35.9',
'2017': '41.4',
'2018': '59.7',
}

dowhat = "plots" 
#dowhat = "dumps" 
#dowhat = "yields" 

P0="/eos/cms/store/cmst3/group/tthlep/peruzzi"
#if 'cmsco01'   in os.environ['HOSTNAME']: P0="/data1/peruzzi"
#if 'cmsphys10' in os.environ['HOSTNAME']: P0="/data1/g/gpetrucc"
TREESALL = "--xf THQ_LHE,THW_LHE,TTWW,TTTW,TTWH -F Friends {P}/3_recleaner_v1/{cname}_Friend.root --FMC Friends {P}/2_triggerSequence_v1/{cname}_Friend.root" # FIXME
TREESONLYSKIM = "-P "+P0+"/NanoTrees_TTH_300519_v5pre/%s "%(YEAR,)
TREESONLYFULL = "-P "+P0+"/NanoTrees_TTH_300519_v5pre/%s "%(YEAR,)
TREESONLYMEMZVETO = "-P "+P0+"/NanoTrees_TTH_300519_v5pre/%s "%(YEAR,)
TREESONLYMEMZPEAK = "-P "+P0+"/NanoTrees_TTH_300519_v5pre/%s "%(YEAR,)

def base(selection):

    CORE=' '.join([TREESALL,TREESONLYSKIM])
    CORE+=" -f -j 8 -l %s --s2v -L ttH-multilepton/functionsTTH.cc --tree NanoAOD --mcc ttH-multilepton/lepchoice-ttH-FO.txt --split-factor=-1 --WA prescaleFromSkim "%(lumis[YEAR],)# --neg"
    RATIO= " --maxRatioRange 0.0  1.99 --ratioYNDiv 505 "
    RATIO2=" --showRatio --attachRatioPanel --fixRatioRange "
    LEGEND=" --legendColumns 2 --legendWidth 0.25 "
    LEGEND2=" --legendFontSize 0.042 "
    SPAM=" --noCms --topSpamSize 1.1 --lspam '#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}' "
    if dowhat == "plots": CORE+=RATIO+RATIO2+LEGEND+LEGEND2+SPAM+"  --showMCError --rebin 4 --xP 'nT_.*' --xP 'debug_.*'"

    if selection=='2lss':
        GO="%s ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt "%CORE
#        GO="%s -W 'vtxWeight2017*eventBTagSF*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],2)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],2)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)'"%GO
        if dowhat in ["plots","ntuple"]: GO+=" ttH-multilepton/2lss_3l_plots.txt --xP '^lep(3|4)_.*' --xP '^(3|4)lep_.*' --xP 'kinMVA_3l_.*' "
        if dowhat == "plots": GO=GO.replace(LEGEND, " --legendColumns 3 --legendWidth 0.52 ")
        if dowhat == "plots": GO=GO.replace(RATIO,  " --maxRatioRange 0.6  1.99 --ratioYNDiv 210 ")
        GO += " --binname 2lss "
    elif selection=='3l':
        GO="%s ttH-multilepton/mca-3l-mc.txt ttH-multilepton/3l_tight.txt "%CORE
#        GO="%s -W 'vtxWeight2017*eventBTagSF*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)'"%GO
        if dowhat in ["plots","ntuple"]: GO+=" ttH-multilepton/2lss_3l_plots.txt --xP '^(2|4)lep_.*' --xP '^lep4_.*' --xP 'kinMVA_2lss_.*' "
        if dowhat == "plots": GO=GO.replace(LEGEND, " --legendColumns 3 --legendWidth 0.42 ")
        GO += " --binname 3l "
    elif selection=='4l':
        GO="%s ttH-multilepton/mca-4l-mc.txt ttH-multilepton/4l_tight.txt "%CORE
#        GO="%s -W 'vtxWeight2017*eventBTagSF*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)*leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[3]],LepGood_pt[iLepFO_Recl[3]],LepGood_eta[iLepFO_Recl[3]],3)*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)'"%GO
        if dowhat in ["plots","ntuple"]: GO+=" ttH-multilepton/2lss_3l_plots.txt --xP '^(2|3)lep_.*' --xP '^lep(1|2|3|4)_.*' --xP 'kinMVA_.*' "
        if dowhat == "plots": GO=GO.replace(LEGEND, " --legendColumns 2 --legendWidth 0.3 ")
        if dowhat == "plots": GO=GO.replace(RATIO,  " --maxRatioRange 0.0  2.99 --ratioYNDiv 505 ")
        GO += " --binname 4l "
    else:
        raise RuntimeError, 'Unknown selection'

    return GO

def procs(GO,mylist):
    return GO+' '+" ".join([ '-p %s'%l for l in mylist ])
def sigprocs(GO,mylist):
    return procs(GO,mylist)+' --showIndivSigs --noStackSig'
def runIt(GO,name,plots=[],noplots=[]):
    if '_74vs76' in name: GO = prep74vs76(GO)
    if dowhat == "plots":  
        if not ('forcePlotChoice' in sys.argv[4:]): print 'python mcPlots.py',"--pdir %s/%s"%(ODIR,name),GO,' '.join(['--sP %s'%p for p in plots]),' '.join(['--xP %s'%p for p in noplots]),' '.join(sys.argv[4:])
        else: print 'python mcPlots.py',"--pdir %s/%s"%(ODIR,name),GO,' '.join([x for x in sys.argv[4:] if x!='forcePlotChoice'])
    elif dowhat == "yields": print 'echo %s; python mcAnalysis.py'%name,GO,' '.join(sys.argv[4:])
    elif dowhat == "dumps":  print 'echo %s; python mcDump.py'%name,GO,' '.join(sys.argv[4:])
    elif dowhat == "ntuple": print 'echo %s; python mcNtuple.py'%name,GO,' '.join(sys.argv[4:])
def add(GO,opt):
    return '%s %s'%(GO,opt)
def setwide(x):
    x2 = add(x,'--wide')
    x2 = x2.replace('--legendWidth 0.35','--legendWidth 0.20')
    return x2
def fulltrees(x):
    return x.replace("mixture_jecv6prompt_datafull_jul20_skimOnlyMC","mixture_jecv6prompt_datafull_jul20")
def doprescale3l(x):
    x2 = x.replace("mixture_jecv6prompt_datafull_jul20_skimOnlyMC","TREES_80X_180716_jecv6_skim_3ltight_relax")
    x2 = x2.replace("--Fs {P}/4_kinMVA_without_MEM_v5 --Fs {P}/8_bTagSF_12fb_v45","--Fs {P}/4_kinMVA_with_MEM_v5 --Fs {P}/7_MEM_v5 --Fs {P}/8_bTagSF_12fb_v5")
#    x2 = add(x2,"--sP kinMVA.*")
    return x2

allow_unblinding = False

if __name__ == '__main__':

    torun = sys.argv[3]

    if (not allow_unblinding) and '_data' in torun and (not any([re.match(x.strip()+'$',torun) for x in ['.*_appl.*','cr_.*']])): raise RuntimeError, 'You are trying to unblind!'

    if '2lss_' in torun:
        x = base('2lss')
        if '_appl' in torun: x = add(x,'-I ^TT ')
        if '_1fo' in torun:
            x = add(x,"-A alwaystrue 1FO 'LepGood1_isTight+LepGood2_isTight==1'")
            x = x.replace("--xP 'nT_.*'","")
        if '_2fo' in torun: x = add(x,"-A alwaystrue 2FO 'LepGood1_isTight+LepGood2_isTight==0'")
        if '_relax' in torun: x = add(x,'-X ^TT ')
        if '_data' in torun: x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
        if '_table' in torun:
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-table.txt')
        if '_frdata' in torun:
            if '_blinddata' in torun:
                x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
                x = add(x,'--xp data')
            elif not '_data' in torun: raise RuntimeError
            x = x.replace('mca-2lss-mcdata.txt','mca-2lss-mcdata-frdata.txt')
            if '_table' in torun:
                x = x.replace('mca-2lss-mcdata-frdata.txt','mca-2lss-mcdata-frdata-table.txt')

        if '_mll200' in torun:
            x = add(x,"-E ^mll200 ")

        if '_splitfakes' in torun:
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-flavsplit.txt')
            
        if '_closuretest' in torun:
            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-closuretest.txt')
            x = x.replace("--maxRatioRange 0 3","--maxRatioRange 0.5 1.5")
            x = add(x,"--AP --plotmode nostack --sP 'kinMVA.*2lss.*'")
            x = add(x,"-p FR_QCD -p FR_TT -p TT_all --ratioDen FR_QCD --ratioNums FR_TT --errors ")
            if '_closuretest_norm' in torun:
                x = x.replace("--plotmode nostack","--plotmode norm")
                x = add(x,"--fitRatio 1")
            if '_bloose' in torun: x = add(x,'-E ^BLoose ')
            if '_btight' in torun: x = add(x,'-E ^BTight ')
            if '_nobcut' in torun: x = add(x,'-X ^2b1B ')
            if '_notrigger' in torun: x = add(x,'-X ^trigger ')

        if '_varsFR' in torun:
            torun += "_"+sys.argv[-1]
            x = x.replace('mca-2lss-mc.txt','mca-2lss-data-frdata-%s.txt'%sys.argv[-1])
            x = x.replace("--maxRatioRange 0 3","--maxRatioRange 0 2")
            x = add(x,"--plotmode nostack --sP kinMVA_2lss_ttbar --sP kinMVA_2lss_ttV")
            x = add(x,"--ratioDen fakes_data --ratioNums fakes_data_%s --errors"%sys.argv[-1])
            if '_varsFR_norm' in torun:
                x = x.replace("--plotmode nostack","--plotmode norm")
                x = add(x,"--fitRatio 1")

        runIt(x,'%s'%torun)
        if '_flav' in torun:
            for flav in ['mm','ee','em']: runIt(add(x,'-E ^%s'%flav),'%s/%s'%(torun,flav))
        if '_cats' in torun:
            for cat in ['b2lss_1tau','b2lss_ee_0tau_neg','b2lss_ee_0tau_pos',\
                            'b2lss_em_0tau_bl_neg','b2lss_em_0tau_bl_pos','b2lss_em_0tau_bt_neg','b2lss_em_0tau_bt_pos',\
                            'b2lss_mm_0tau_bl_neg','b2lss_mm_0tau_bl_pos','b2lss_mm_0tau_bt_neg','b2lss_mm_0tau_bt_pos']:
                runIt(add(x,'-E ^%s'%cat),'%s/%s'%(torun,cat))


    if '3l_' in torun:
        x = base('3l')
        if '_appl' in torun: x = add(x,'-I ^TTT ')
        if '_1fo' in torun:
            x = add(x,"-A alwaystrue 1FO 'LepGood1_isTight+LepGood2_isTight+LepGood3_isTight==2'")
            x = x.replace("--xP 'nT_.*'","")
        if '_relax' in torun: x = add(x,'-X ^TTT ')
        if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
        if '_frdata' in torun:
            if '_blinddata' in torun:
                x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
                x = add(x,'--xp data')
            elif not '_data' in torun: raise RuntimeError
            x = x.replace('mca-3l-mcdata.txt','mca-3l-mcdata-frdata.txt')
            if '_prescale' in torun:
                x = doprescale3l(x)
                x = x.replace('mca-3l-mcdata-frdata.txt','mca-3l-mcdata-frdata-prescale.txt')
            if '_table' in torun:
                x = x.replace('mca-3l-mcdata-frdata.txt','mca-3l-mcdata-frdata-table.txt')
        else:
            if 'data' in torun and '_prescale' in torun:
                raise RuntimeError # trees not ready
                x = doprescale3l(x)
                x = x.replace('mca-3l-mcdata.txt','mca-3l-mcdata-prescale.txt')
            elif '_prescale' in torun:
                raise RuntimeError # trees not ready
                x = doprescale3l(x)
                x = x.replace('mca-3l-mc.txt','mca-3l-mc-prescale.txt')
        if '_table' in torun:
            x = x.replace('mca-3l-mc.txt','mca-3l-mc-table.txt')
        if '_closuretest' in torun:
            x = x.replace('mca-3l-mc.txt','mca-3l-mc-closuretest.txt')
            x = x.replace("--maxRatioRange 0 3","--maxRatioRange 0.5 1.5")
            x = add(x,"--AP --plotmode nostack --sP 'kinMVA_.*3l.*'")
            x = add(x,"-p FR_QCD -p FR_TT -p TT_all --ratioDen FR_QCD --ratioNums FR_TT --errors --xf '^TTJets.*_ext'")
            if '_closuretest_norm' in torun:
                x = x.replace("--plotmode nostack","--plotmode norm")
                x = add(x,"--fitRatio 1")
            if '_notrigger' in torun: x = add(x,'-X ^trigger ')
        if '_varsFR' in torun:
            torun += "_"+sys.argv[-1]
            x = x.replace('mca-3l-mc.txt','mca-3l-data-frdata-%s.txt'%sys.argv[-1])
            x = x.replace("--maxRatioRange 0 3","--maxRatioRange 0 2")
            x = add(x,"--plotmode nostack --sP kinMVA_3l_ttbar --sP kinMVA_3l_ttV_withMEM --sP kinMVA_3l_ttV")
            x = add(x,"--ratioDen fakes_data --ratioNums fakes_data_%s --errors"%sys.argv[-1])
            if '_varsFR_norm' in torun:
                x = x.replace("--plotmode nostack","--plotmode norm")
                x = add(x,"--fitRatio 1")
        if '_x2j' in torun:
            x = add(x,"-E ^x2j ")
        runIt(x,'%s'%torun)
        if '_cats' in torun:
            for cat in ['b3l_bl_neg','b3l_bl_pos','b3l_bt_neg','b3l_bt_pos']:
                runIt(add(x,'-E ^%s'%cat),'%s/%s'%(torun,cat))

    if '4l_' in torun:
        x = base('4l')
        if '_appl' in torun: x = add(x,'-I ^TTTT ')
        if '_relax' in torun: x = add(x,'-X ^TTTT ')
        if '_data' in torun: x = x.replace('mca-4l-mc.txt','mca-4l-mcdata.txt')
        if '_frdata' in torun:
            if '_blinddata' in torun:
                x = x.replace('mca-4l-mc.txt','mca-4l-mcdata.txt')
                x = add(x,'--xp data')
            elif not '_data' in torun: raise RuntimeError
            x = x.replace('mca-4l-mcdata.txt','mca-4l-mcdata-frdata.txt')
        runIt(x,'%s'%torun)

    if 'cr_3j' in torun:
        x = base('2lss')
        if '_data' in torun: x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
        if '_frdata' in torun:
            if not '_data' in torun: raise RuntimeError
            x = x.replace('mca-2lss-mcdata.txt','mca-2lss-mcdata-frdata.txt')
        x = add(x,"-R ^4j 3j 'nJet25==3'")
        plots = ['2lep_.*','nJet25','nBJetLoose25','nBJetMedium25','met','metLD','htJet25j','mhtJet25','mtWmin','htllv','kinMVA_2lss_ttbar','kinMVA_2lss_ttV','kinMVA_2lss_bins7']
        runIt(x,'%s'%torun,plots)
        if '_flav' in torun:
            for flav in ['mm','ee','em']:
                runIt(add(x,'-E ^%s '%flav),'%s/%s'%(torun,flav),plots)

    if 'cr_ttbar' in torun:
        x = base('2lss')
        x = fulltrees(x) # for mc same-sign
        x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata-ttbar.txt')
        if '_data' not in torun: x = add(x,'--xp data')
        if '_appl' in torun: x = add(x,'-I ^TT ')
        if '_1fo' in torun: x = add(x,"-A alwaystrue 1FO 'LepGood1_isTight+LepGood2_isTight==1'")
        if '_leadmupt25' in torun: x = add(x,"-A 'entry point' leadmupt25 'abs(LepGood1_pdgId)==13 && LepGood1_pt>25'")
        if '_norm' in torun:
            x = add(x,"--sp '.*' --scaleSigToData")
        x = add(x,"-I same-sign -X ^4j -X ^2b1B -E ^2j -E ^em ")
        if '_highMetNoBCut' in torun: x = add(x,"-A 'entry point' highMET 'met_pt>60'")
        else: x = add(x,"-E ^1B ")
        plots = ['2lep_.*','met','metLD','nVert','nJet25','nBJetMedium25','nBJetLoose25','nBJetLoose40','nBJetMedium40',"'kinMVA_input.*'"]
        runIt(x,'%s'%torun,plots)

    if 'cr_zjets' in torun:
        x = base('2lss')
        x = fulltrees(x) # for mc same-sign
        x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata-ttbar.txt')
        x = x.replace('--maxRatioRange 0 3','--maxRatioRange 0.8 1.2')
        if '_data' not in torun: x = add(x,'--xp data')
        x = add(x,"-I same-sign -X ^2b1B -X ^Zee_veto -A alwaystrue mZ 'mZ1>60 && mZ1<120'")
        for flav in ['mm','ee']:
            runIt(add(x,'-E ^%s -X ^4j'%flav),'%s/%s'%(torun,flav))
            runIt(add(x,'-E ^%s -X ^4j -E ^2j '%flav),'%s_2j/%s'%(torun,flav))
            runIt(add(x,'-E ^%s '%flav),'%s_4j/%s'%(torun,flav))

    if 'cr_wz' in torun:
        x = base('3l')
        if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
        if '_frdata' in torun:
            if not '_data' in torun: raise RuntimeError
            x = x.replace('mca-3l-mcdata.txt','mca-3l-mcdata-frdata.txt')
        x = add(x,"-I 'Zveto' -X ^2b1B -E ^Bveto ")
        plots = ['lep3_pt','metLD','nBJetLoose25','3lep_worseIso','minMllAFAS','3lep_worseMVA','3lep_mtW','kinMVA.*','htJet25j','nJet25']
        runIt(x,'%s'%torun,plots)

    if 'cr_ttz' in torun:
        x = base('3l')
        if '_data' in torun: x = x.replace('mca-3l-mc.txt','mca-3l-mcdata.txt')
        if '_frdata' in torun:
            if not '_data' in torun: raise RuntimeError
            x = x.replace('mca-3l-mcdata.txt','mca-3l-mcdata-frdata.txt')
        plots = ['lep2_pt','met','nJet25','mZ1']
        x = add(x,"-I 'Zveto' -X ^2b1B -E ^gt2b -E ^1B ")
        runIt(x,'%s'%torun,plots)
        x = add(x,"-E ^4j ")
        runIt(x,'%s_4j'%torun,plots)
