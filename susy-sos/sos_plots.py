### Note: modifications needed after ICHEP:
### puw2016_vtx_13fb(nVert) has been replaced with puw2016_nTrueInt_13fb(nTrueInt)
### filters are applied only on data 

#!/usr/bin/env python
import sys
import re

ODIR=sys.argv[1]

dowhat = "plots" 
#dowhat = "dumps" 
#dowhat = "yields" 
#dowhat = "limits"


## change file for systematics here
#SYST="susy-sos/syst/susy_sos_dummy.txt" ## dmmy for SMS combination test
#SYST="susy-sos/syst/susy_sos_dummy2.txt" ## dummy for SMS combination test 
#SYST="susy-sos/syst/susy_sos_syst_test.txt" ##For freezing - few banchmark points
SYST="susy-sos/syst/susy_sos3l_syst_test2_scan.txt" ##For scan
#SYST="susy-sos/syst/susy_sos_syst_scan_combination.txt" ## For combination (RC change!)
PLOTandCUTS="susy-sos/mca-2los-test2-mc.txt susy-sos/2los_tight.txt" ## check later where is replaced. You need to specify there the mca, since they will not be replaced as for "plots" (due to different input order of combineCards)


def base(selection):


    #CORE="-P /data1/botta/trees_SOS_80X_130716_Scans/ --mcc susy-sos/mcc-lepWP.txt" # --FMCs {P}/eventBTagWeight"
    #CORE="-P /data/gpetrucc/TREES_80X_SOS_111016_NoIso --Fs {P}/0_both3dCleanLoose_noIso_v2 --mcc susy-sos/lepchoice-recleaner.txt"
    #Freezing
    #CORE="-P /data1/botta/trees_SOS_010217 --Fs {P}/0_both3dlooseClean_v1 --FMCs {P}/0_eventBTagWeight_v1 --mcc susy-sos/lepchoice-recleaner.txt"
    #Pre-approval
    CORE="-P /data1/botta/trees_SOS_010217 --Fs {P}/0_both3dlooseClean_v2 --FMCs {P}/0_eventBTagWeight_v2 --mcc susy-sos/lepchoice-recleaner.txt"
    CORE+=" -j 8 -f -l 35.9 --s2v --tree treeProducerSusyMultilepton --mcc susy-sos/mcc-sf1.txt --neg" #--mcc susy-sos/2los_triggerdefs.txt #12.9 - 35.9 - 18.1
    if dowhat == "plots": CORE+=" --lspam 'CMS Preliminary' --legendWidth 0.14 --legendFontSize 0.04"
    GO = ""
    if selection=='2los':
        if (dowhat != "limits") : GO="susy-sos/mca-2los-test2-mc.txt susy-sos/2los_tight.txt " #susy-sos/mca-2los-mc.txt
        GO="%s %s"%(CORE,GO) 
        #ICHEP
        #GO="%s -L susy-sos/functionsSOS.cc -L susy-sos/lepton_trigger_SF.cc -W 'leptonSF_SOS(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,0)*leptonSF_SOS(LepGood2_pdgId,LepGood2_pt,LepGood2_eta,0)*triggerSF_SOS(met_pt,metmm_pt(LepGood1_pdgId,LepGood1_pt,LepGood1_phi,LepGood2_pdgId,LepGood2_pt,LepGood2_phi,met_pt,met_phi),0)*puw2016_nTrueInt_13fb(nTrueInt)*eventBTagSF'"%GO 
        #Freezing MORIOND17 (trigger SF and recoMu/Ele just 1)
        GO="%s -L susy-sos/functionsSOS.cc -L susy-sos/lepton_trigger_SF.cc -W 'triggerSF_SOS(LepGood1_pt,LepGood1_eta,LepGood2_pt,LepGood2_eta,met_pt,metmm_pt(LepGood1_pdgId,LepGood1_pt,LepGood1_phi,LepGood2_pdgId,LepGood2_pt,LepGood2_phi,met_pt,met_phi),0)*leptonSF_SOS(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,0)*leptonSF_SOS(LepGood2_pdgId,LepGood2_pt,LepGood2_eta,0)*puw2016_nTrueInt_36fb(nTrueInt)*bTagWeight'"%GO #getPUW(nTrueInt)
        #FSR MORIOND17
        #GO="%s -L susy-sos/functionsSOS.cc -L susy-sos/lepton_trigger_SF.cc -W 'triggerSF_SOS(met_pt,metmm_pt(LepGood1_pdgId,LepGood1_pt,LepGood1_phi,LepGood2_pdgId,LepGood2_pt,LepGood2_phi,met_pt,met_phi),0)*puw2016_nTrueInt_36fb(nTrueInt)'"%GO #getPUW(nTrueInt)
        #FSR MORIOND17 - ICHEP DATA
        #GO="%s -L susy-sos/functionsSOS.cc -L susy-sos/lepton_trigger_SF.cc -W 'triggerSF_SOS(met_pt,metmm_pt(LepGood1_pdgId,LepGood1_pt,LepGood1_phi,LepGood2_pdgId,LepGood2_pt,LepGood2_phi,met_pt,met_phi),0)*puw2016_nTrueInt_13fb(nTrueInt)'"%GO 
        if dowhat == "plots": GO+=" susy-sos/2los_plots.txt"     
    elif selection=='3l':    
        if (dowhat != "limits") : GO="susy-sos/mca-3l-test2-mc.txt susy-sos/3l_tight.txt " 
        GO="%s %s"%(CORE,GO) 
        #GO="%s -L susy-sos/functionsSOS.cc -W 'puw2016_nTrueInt_36fb(nTrueInt)*bTagWeight'"%GO 
        GO="%s -L susy-sos/functionsSOS.cc -L susy-sos/lepton_trigger_SF.cc -W 'leptonSF_SOS(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,0)*leptonSF_SOS(LepGood2_pdgId,LepGood2_pt,LepGood2_eta,0)*leptonSF_SOS(LepGood3_pdgId,LepGood3_pt,LepGood3_eta,0)*triggerSF_3l(LepGood1_pt,LepGood1_eta, LepGood2_pt, LepGood2_eta, LepGood3_pt, LepGood3_eta, met_pt, metmmm_pt(LepGood1_pt, LepGood1_phi, LepGood2_pt, LepGood2_phi,LepGood3_pt,LepGood3_phi, met_pt, met_phi, lepton_Id_selection(LepGood1_pdgId, LepGood2_pdgId, LepGood3_pdgId)), lepton_permut( LepGood1_pdgId, LepGood2_pdgId, LepGood3_pdgId))*puw2016_nTrueInt_36fb(nTrueInt)*bTagWeight'"%GO 
        if dowhat == "plots": GO+=" susy-sos/3l_plots.txt"     
    else:
        raise RuntimeError, 'Unknown selection'

    return GO

def procs(GO,mylist):
    return GO+' '+" ".join([ '-p %s'%l for l in mylist ])
def sigprocs(GO,mylist):
    return procs(GO,mylist)+' --showIndivSigs --noStackSig'
def runIt(GO,name,plots=[],noplots=[]):
    if '_74vs76' in name: GO = prep74vs76(GO)
    if   dowhat == "plots":  print 'python mcPlots.py',"--pdir %s/%s"%(ODIR,name),GO,' '.join(['--sP %s'%p for p in plots]),' '.join(['--xP %s'%p for p in noplots]),' '.join(sys.argv[3:])
    elif dowhat == "yields": print 'echo %s; python mcAnalysis.py'%name,GO,' '.join(sys.argv[3:])
    elif dowhat == "dumps":  print 'echo %s; python mcDump.py'%name,GO,' '.join(sys.argv[3:])
    elif (dowhat == "limits" and ('_unblind' in name) ): 
        name_tmp = name
        #name_tmp=name.replace('2los_', '',1)
        # comment: for the moment recycling plots and noplots as a container for histo name and binning when running 'limits' mode (to be improved) 
        print 'echo %s; python makeShapeCardsSusy.py'%name_tmp,PLOTandCUTS,' '.join(['%s'%p for p in plots]),' '.join(['%s'%p for p in noplots]),SYST,' -o %s'%name_tmp,' ',GO," --od %s"%(ODIR),' --hardZero ',' '.join(sys.argv[3:])
    elif (dowhat == "limits" and ('_unblind' in name)==0 and ('CR'in name)==0 ):
        name_tmp = name
        #name_tmp=name.replace('2los_', '',1)
        # comment: for the moment recycling plots and noplots as a container for histo name and binning when running in 'limits' mode (to be improved) 
        print 'echo %s; python makeShapeCardsSusy.py'%name_tmp,PLOTandCUTS,' '.join(['%s'%p for p in plots]),' '.join(['%s'%p for p in noplots]),SYST,' -o %s'%name_tmp,' ',GO," --od %s"%(ODIR),' --asimov --hardZero ',' '.join(sys.argv[3:]) 
    elif (dowhat == "limits" and 'CR'in name):
        name_tmp = name
        #name_tmp=name.replace('2los_', '',1)
        # comment: for the moment recycling plots and noplots as a container for histo name and binning when running in 'limits' mode (to be improved) 
        print 'echo %s; python makeShapeCardsSusy.py'%name_tmp,PLOTandCUTS,' '.join(['%s'%p for p in plots]),' '.join(['%s'%p for p in noplots]),SYST,' -o %s'%name_tmp,' ',GO," --od %s"%(ODIR),' '.join(sys.argv[3:])     
    else:
        raise RuntimeError, 'Unknown selection'
def add(GO,opt):
    return '%s %s'%(GO,opt)
def setwide(x):
    x2 = add(x,'--wide')
    x2 = x2.replace('--legendWidth 0.35','--legendWidth 0.20')
    return x2
def fulltrees(x):
    return x.replace('TREES_76X_200216_jecV1M2_skimOnlyMC_reclv8','TREES_76X_200216_jecV1M2')

if __name__ == '__main__':

    torun = sys.argv[2]



    ### SR plots: Pure MC Sig+Bkg, Data-Driven Bkgs, Variations for TT and DY syst, Application region Bins, DATA! --- Also for limits computations

    if '2los_SR_' in torun:
        x = base('2los')
        if(dowhat != "limits"): x = add(x,"--perBin")   
        if '_mc' in torun: 
            if(dowhat != "limits"):x = add(x,"--noStackSig --showIndivSigs ") 
        if '_ddbkg' in torun: 
            if(dowhat != "limits"):x = add(x,"--noStackSig --showIndivSigs --showMCError") 
            x = x.replace('mca-2los-mc.txt','mca-2los-mc-frdata.txt') #ICHEP trees
            x = x.replace('mca-2los-test2-mc.txt','mca-2los-test2-mc-frdata.txt') #Moriond trees
            #PLOTandCUTS="susy-sos/mca-2los-mc-frdata.txt susy-sos/2los_tight.txt" #ICHEP trees
            #PLOTandCUTS="susy-sos/mca-2los-test2-mc-frdata.txt susy-sos/2los_tight.txt" #Moriond trees   
            PLOTandCUTS="susy-sos/mca-2los-test2-mc-frdata_FastSimTChi_onepoint.txt susy-sos/2los_tight.txt" #Moriond trees   
        if '_appl' in torun:
            if(dowhat != "limits"):x = add(x,"--noStackSig --showIndivSigs") 
            x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt') #ICHEP trees
            x = x.replace('mca-2los-test2-mc.txt','mca-2los-test2-mcdata.txt') #Moriond trees
            x = add(x,"-I ^TT ")  
        if '_unblind' in torun:
            if(dowhat != "limits"):x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
            x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') #ICHEP trees
            x = x.replace('mca-2los-test2-mc.txt','mca-2los-test2-mcdata-frdata.txt') #Moriond trees
            #PLOTandCUTS="susy-sos/mca-2los-mcdata-frdata.txt susy-sos/2los_tight.txt" #ICHEP trees
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata.txt susy-sos/2los_tight.txt" #Moriond trees 
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_FastSimTChi.txt susy-sos/2los_tight.txt" #Moriond trees SCAN          
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_TChiWZ_comb_extra.txt susy-sos/2los_tight.txt" #Moriond combination trees SCAN          
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_FastSimTChi_onepoint.txt susy-sos/2los_tight.txt" #Moriond trees SCAN          
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_FastSimTChi_noMET.txt susy-sos/2los_tight.txt" #Moriond trees SCAN - no MET      
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_FastSimT2tt_onepoint.txt susy-sos/2los_tight.txt" #Moriond trees SCAN - onepoint
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_FastSimTN2N1_TN2C1_pheno.txt susy-sos/2los_tight.txt" #Moriond trees SCAN  - Higgsino
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_FastSimpMSSM.txt susy-sos/2los_tight.txt" #Moriond trees SCAN  - Higgsino pMSSM
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_FastSimT2tt.txt susy-sos/2los_tight.txt" #Moriond trees SCAN  - stop  
            PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_FastSimTChi_onepoint.txt susy-sos/2los_tight.txt" #Moriond trees   
        if '_met125_mm' in torun: 
            x = add(x,"-E ^pt5sublep -E ^mm -E ^upperMediumMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET ")
            x = x.replace('-l 12.9','-l 10.1') 
            x = x.replace('-l 35.9','-l 33.2') 
            x = x.replace('-l 18.1','-l 15.3') 
            if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-lowmet.txt') 
        if '_met200' in torun: 
            x = add(x," -E ^mediumMET -X ^triggerAll -E ^triggerMET ") 
            if '_ewk' in torun:
               x = add(x," -E ^upperHighMETEWK ")  
            if '_stop' in torun:
               x = add(x," -E ^upperHighMETStop ")  
            if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-highmet.txt') 
        if '_met300' in torun: 
            x = add(x," -X ^triggerAll -E ^triggerMET ") 
            if '_ewk' in torun:
               x = add(x," -E ^highMETEWK ")  
            if '_stop' in torun:
               x = add(x," -E ^highMETStop ")  
            if(dowhat != "limits"):x = x.replace('mcc-sf1.txt','mcc-sf-highmet.txt') 
        if '_ewk' in torun:
            x = add(x,"--xp T2tt_350_dM20 -E ^MT -E ^SF -E ^pt5sublep")
            if dowhat == "limits":
                runIt(x,torun,["m2l"],["'[4,10,20,30,50]'"])
            else: 
                if'_bins' in torun: 
                    runIt(x,'%s/all'%torun,['SR_bins_EWKino'])
                if'_Vars' in torun: 
                    runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop'])
        if '_stop' in torun:
            x = add(x,"--xp TChiWZ_150_dM20,TChiWZ_150_dM7 ") 
            if dowhat == "limits":
                runIt(x,torun,["LepGood1_pt"],["'[5,12,20,30]'"])
            else:
                if '_bins' in torun: 
                    runIt(x,'%s/all'%torun,['SR_bins_stop']) 
                if '_Vars' in torun: 
                    runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop'])    
    if '3l_SR_' in torun:
        x = base('3l')  
        if(dowhat != "limits"): x = add(x,"--perBin")   
        if '_mc' in torun: 
            if(dowhat != "limits"):x = add(x,"--noStackSig --showIndivSigs ") 
        if '_ddbkg' in torun: 
            if(dowhat != "limits"):x = add(x,"--noStackSig --showIndivSigs ") #--showMCError
            x = x.replace('mca-3l-test2-mc.txt','mca-3l-test2-mc-frmc.txt') #Moriond trees
            PLOTandCUTS="susy-sos/mca-3l-test2-mc-frmc_FastSimTChiWZ.txt susy-sos/3l_tight.txt" #Moriond trees scan  
            #PLOTandCUTS="susy-sos/mca-3l-test2-mc-frmc.txt susy-sos/3l_tight.txt" #Moriond trees   
        if '_met75' in torun: 
            x = x.replace('-l 35.9','-l 16.2') 
            x = add(x," -X ^triggerAll -E ^triggerTripleMu -E ^pt5subleps ")
            if '_lowPt' in torun:
                x = add(x," -E ^lowpt3l ")
            if '_highPt' in torun:
                x = add(x," -E ^highpt3l ")
            if dowhat == "limits":
                runIt(x,torun,["minMllSFOS"],["'[4,10,20,30,50]'"])
            else: 
                if'_bins' in torun: 
                    runIt(x,'%s/all'%torun,['SR_bins_3l'])
        if '_met125' in torun: 
            x = x.replace('-l 35.9','-l 33.2') 
            x = add(x," -X ^mumumu -X ^lowMET -X minAFAS -E ^mml -E ^mediumMET -X ^triggerAll -E ^triggerDoubleMuMET  -E ^pt5subleps")
            if '_lowPt' in torun:
                x = add(x," -E ^lowpt3l ")
            if '_highPt' in torun:
                x = add(x," -E ^highpt3l ")
            if dowhat == "limits":
                runIt(x,torun,["minMllSFOS"],["'[4,10,20,30,50]'"])
            else: 
                if'_bins' in torun: 
                    runIt(x,'%s/all'%torun,['SR_bins_3l'])
        if '_met200' in torun:     
            x = add(x," -X ^mumumu -X ^lowMET -X minAFAS -E ^highMET -X ^triggerAll -E ^triggerMET ")
            if dowhat == "limits":
                runIt(x,torun,["minMllSFOS"],["'[4,10,20,30,50]'"])
            else: 
                if'_bins' in torun: 
                    runIt(x,'%s/all'%torun,['SR_bins_3l'])


    ### DY Control Region Data-MC, LowMET and HighMET              
    if '2los_CR_DY_vars' in torun:
        x = base('2los')
        if(dowhat != "limits"): x = add(x,"--noStackSig --showIndivSigs ")
        if '_data' in torun: 
            if(dowhat != "limits"):x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt') #ICHEP trees
            if(dowhat != "limits"):x = x.replace('mca-2los-test2-mc.txt','mca-2los-test2-mcdata.txt') #Moriond trees
            #PLOTandCUTS="susy-sos/mca-2los-mcdata.txt susy-sos/2los_tight.txt" #ICHEP trees
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata.txt susy-sos/2los_tight.txt" #Moriond trees
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_FastSimTChi.txt susy-sos/2los_tight.txt" #Moriond trees SCAN   
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_TChiWZ_comb_extra.txt susy-sos/2los_tight.txt" #Moriond combination trees SCAN   
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_FastSimTChi_onepoint.txt susy-sos/2los_tight.txt" #Moriond trees SCAN   
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_FastSimTChi_noMET.txt susy-sos/2los_tight.txt" #Moriond trees SCAN - no MET   
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_FastSimT2tt_onepoint.txt susy-sos/2los_tight.txt" #Moriond trees SCAN - onepoint
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_FastSimTN2N1_TN2C1_pheno.txt susy-sos/2los_tight.txt" #Moriond trees SCAN - Higgsino
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_FastSimpMSSM.txt susy-sos/2los_tight.txt" #Moriond trees SCAN - Higgsino pMSSM
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_FastSimT2tt.txt susy-sos/2los_tight.txt" #Moriond trees SCAN  - stop    
            PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_FastSimTChi_onepoint.txt susy-sos/2los_tight.txt" #Moriond trees   
            if(dowhat != "limits"):x = add(x,"--showRatio --maxRatioRange -2 5") #--showMCError
            if(dowhat == "limits" and ('_stop20' in torun)):x = add(x,"--xp TChiWZ_150_dM20")
            if(dowhat == "limits" and (('_ewk20' in torun) or ('_ewk7' in torun) or ('_ewkHig' in torun))):x = add(x,"--xp T2tt_350_dM20")
        if '_met200' in torun:
            x = add(x," -E ^mediumMET -E ^MT -X ^TT -E ^CRDYTT -R ^ledlepPt NoUpledlepPt '20 < LepGood1_pt || fabs(LepGood1_ip3d)>0.01 || fabs(LepGood1_sip3d)>2 || fabs(LepGood2_ip3d)>0.01 || fabs(LepGood2_sip3d)>2' -R mtautau Invmtautau '0.<mass_tautau(met_pt,met_phi,LepGood1_pt,LepGood1_eta,LepGood1_phi,LepGood2_pt,LepGood2_eta,LepGood2_phi)&&mass_tautau(met_pt,met_phi,LepGood1_pt,LepGood1_eta,LepGood1_phi,LepGood2_pt,LepGood2_eta,LepGood2_phi)<160.' -X ^triggerAll -E ^triggerMET") #--scale-process DYJets 0.96
        if '_met125' in torun:
            x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
            x = add(x," -E ^mm -E ^upperMediumMET -E ^MT -X ^TT -E ^CRDYTT -R ^ledlepPt NoUpledlepPt '20 < LepGood1_pt || fabs(LepGood1_ip3d)>0.01 || fabs(LepGood1_sip3d)>2 || fabs(LepGood2_ip3d)>0.01 || fabs(LepGood2_sip3d)>2' -R mtautau Invmtautau '0.<mass_tautau(met_pt,met_phi,LepGood1_pt,LepGood1_eta,LepGood1_phi,LepGood2_pt,LepGood2_eta,LepGood2_phi)&&mass_tautau(met_pt,met_phi,LepGood1_pt,LepGood1_eta,LepGood1_phi,LepGood2_pt,LepGood2_eta,LepGood2_phi)<160.' -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -E ^pt5sublep") #--scale-process DYJets 0.90
            x = x.replace('-l 12.9','-l 10.1') 
            x = x.replace('-l 35.9','-l 33.2')
            x = x.replace('-l 18.1','-l 15.3') 
        if dowhat == "limits":
            runIt(x,torun,["nLepGood"],["1,-0.5,0.5"])
        else:
            runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop'])




    ### TT Control Region Data-MC, LowMET and HighMET         
    if '2los_CR_TT_vars' in torun:
        x = base('2los')
        if(dowhat != "limits"): x = add(x,"--noStackSig --showIndivSigs ")
        if '_data' in torun:
            if(dowhat != "limits"):x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt') #ICHEP trees
            if(dowhat != "limits"):x = x.replace('mca-2los-test2-mc.txt','mca-2los-test2-mcdata.txt') #Moriond trees
            #PLOTandCUTS="susy-sos/mca-2los-mcdata.txt susy-sos/2los_tight.txt" #ICHEP trees
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata.txt susy-sos/2los_tight.txt" #Moriond trees
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_FastSimTChi.txt susy-sos/2los_tight.txt" #Moriond trees SCAN
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_TChiWZ_comb_extra.txt susy-sos/2los_tight.txt" #Moriond combination trees SCAN             
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_FastSimTChi_onepoint.txt susy-sos/2los_tight.txt" #Moriond trees SCAN          
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_FastSimTChi_noMET.txt susy-sos/2los_tight.txt" #Moriond trees SCAN - no MET   
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_FastSimT2tt_onepoint.txt susy-sos/2los_tight.txt" #Moriond trees SCAN - onepoint         
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_FastSimTN2N1_TN2C1_pheno.txt susy-sos/2los_tight.txt" #Moriond trees SCAN - Higgsino         
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_FastSimpMSSM.txt susy-sos/2los_tight.txt" #Moriond trees SCAN - Higgsino pMSSM        
            #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_FastSimT2tt.txt susy-sos/2los_tight.txt" #Moriond trees SCAN  - stop 
            PLOTandCUTS="susy-sos/mca-2los-test2-mcdata_FastSimTChi_onepoint.txt susy-sos/2los_tight.txt" #Moriond trees   
            if(dowhat != "limits"):x = add(x,"--showRatio --maxRatioRange -2 5") #--showMCError
            if(dowhat == "limits" and ('_stop20' in torun)):x = add(x,"--xp TChiWZ_150_dM20")
            if(dowhat == "limits" and (('_ewk20' in torun) or ('_ewk7' in torun) or ('_ewkHig' in torun))):x = add(x,"--xp T2tt_350_dM20")            
        if '_met200' in torun:             
            x = add(x," -E ^mediumMET -X ^TT -E ^CRttTT -X ^bveto -E ^btag -R ^ledlepPt NoUpledlepPt '5 < LepGood1_pt' -X ^triggerAll -E ^triggerMET") # --scale-process TT 0.91
        if '_met125' in torun:             
            x = add(x," -E ^mm -E ^upperMediumMET -X ^TT -E ^CRttTT -X ^bveto -E ^btag -E ^pt5sublep -R ^ledlepPt NoUpledlepPt '5 < LepGood1_pt' -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET") # --scale-process TT 0.84
            x = x.replace('-l 12.9','-l 10.1')  
            x = x.replace('-l 35.9','-l 33.2')
            x = x.replace('-l 18.1','-l 15.3') 
        if dowhat == "limits":
            runIt(x,torun,["nLepGood"],["1,-0.5,0.5"])
        else:
            runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop'])

                


    ### SS Stop-like Control Region (high MET)
    if '2los_CR_SS' in torun: 
        x = base('2los')
        x = add(x,"-E ^mediumMET -X ^triggerAll -E ^triggerMET -X ^opposite-sign -E ^same-sign ")# --fitRatio 1
        if(dowhat != "limits"): x = add(x,"--noStackSig --showIndivSigs --showMCError")
        if(dowhat != "limits"):x = add(x,"--showRatio --maxRatioRange -2 5") 
        x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') #ICHEP trees
        x = x.replace('mca-2los-test2-mc.txt','mca-2los-test2-mcdata-frdata.txt') #Moriond trees
        #PLOTandCUTS="susy-sos/mca-2los-mcdata-frdata.txt susy-sos/2los_tight.txt" #ICHEP trees
        #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata.txt susy-sos/2los_tight.txt" #Moriond trees     
        #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_TChiWZ_comb_extra.txt susy-sos/2los_tight.txt" #Moriond combination trees SCAN          
        #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_FastSimTChi_onepoint.txt susy-sos/2los_tight.txt" #Moriond trees SCAN          
        #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_FastSimTChi_noMET.txt susy-sos/2los_tight.txt" #Moriond trees SCAN - no MET
        #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_FastSimT2tt_onepoint.txt susy-sos/2los_tight.txt" #Moriond trees SCAN - onepoint
        #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_FastSimTN2N1_TN2C1_pheno.txt susy-sos/2los_tight.txt" #Moriond trees SCAN - Higgsino
        #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_FastSimpMSSM.txt susy-sos/2los_tight.txt" #Moriond trees SCAN - Higgsino pMSSM
        #PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_FastSimT2tt.txt susy-sos/2los_tight.txt" #Moriond trees SCAN  - stop  
        PLOTandCUTS="susy-sos/mca-2los-test2-mcdata-frdata_FastSimTChi_onepoint.txt susy-sos/2los_tight.txt" #Moriond trees   
        if dowhat == "limits":
            runIt(x,torun,["LepGood1_pt"],["'[5,12,20,30]'"])
        else:
            #runIt(x,'%s/all'%torun,['SR_bins_stop'])    
            if '_bins' in torun: 
                runIt(x,'%s/all'%torun,['SR_bins_stop']) 
            if '_Vars' in torun: 
                runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop']) 
 


    ### WW Control Region, Data-MC, HighMET             
    if '2los_CR_WW_vars' in torun:
        x = base('2los')
        x = add(x,"--noStackSig --showIndivSigs")
        if '_data' in torun: 
            x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt') #ICHEP trees
            x = x.replace('mca-2los-test2-mc.txt','mca-2los-test2-mcdata.txt') #Moriond trees
            x = add(x,"--showRatio --maxRatioRange -2 5") #--showMCError
        if '_met200' in torun:             
            x = add(x,"-E ^mediumMET -X ^TT -E ^CRttTT -R ^ledlepPt NoUpledlepPt '20 < LepGood1_pt' -E ^ZVeto -X ^MT -E ^InvMT -X ^triggerAll -E ^triggerMET")
        if '_met125' in torun:    
            x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
            x = add(x,"-E ^mm -E ^upperMediumMET -X ^TT -E ^CRttTT -R ^ledlepPt NoUpledlepPt '20 < LepGood1_pt' -E ^ZVeto -X ^MT -E ^InvMT -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -E ^pt5sublep")
            x = x.replace('-l 12.9','-l 10.1') 
            x = x.replace('-l 35.9','-l 33.2')
            x = x.replace('-l 18.1','-l 15.3') 
        runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop'])            




    ### FR WJets closure
    if '2los_FR_Closure_vars' in torun:
        x = base('2los')
        x = add(x,"--plotmode nostack --sp WJets --plotmode norm")
        x = x.replace('mca-2los-test2-mc.txt','mca-2los-mc-closuretest.txt')       
        x = add(x," --showRatio --maxRatioRange 0 4 --ratioDen QCDFR_WJets --ratioNums WJets") #-X lowMET -X HT -X METovHT
        runIt(x,'%s/all'%torun)


     ##################################
     ##################################
     ##################################


#     ### MC Distributions with Signal shapes normalized to Bkg, n-minus1 option
#     if '2los_SR_vars' in torun:
#         x = base('2los')
#         if 'ewk_met200' in torun: 
#             x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET -E ^SF -E ^pt5sublep -E ^MT") 
#             if '_unblind' in torun:
#                 x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
#                 #x = add(x,"--plotmode norm")
#                 x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') #remove signal
#                 x = x.replace('mcc-sf1.txt','mcc-sf-highmet.txt') 
#         if 'ewk_met125' in torun: 
#             x = add(x,"-E ^upperMET -E ^mm -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -E ^pt5sublep -E ^MT")
#             if '_unblind' in torun:
#                 x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
#                 #x = add(x,"--plotmode norm")
#                 x = x.replace('-l 12.9','-l 10.1')
#                 x = x.replace('-l 35.9','-l 33.2')
#                 x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
#                 x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') #remove signal
#                 x = x.replace('mcc-sf1.txt','mcc-sf-lowmet.txt')
#         if 'stop_met200' in torun: 
#             x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET ") 
#             if '_unblind' in torun:
#                 x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
#                 #x = add(x,"--plotmode norm")
#                 x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') #remove signal
#                 x = x.replace('mcc-sf1.txt','mcc-sf-highmet.txt')
#         if 'stop_met125' in torun: 
#             x = add(x,"-E ^upperMET -E ^mm -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -E ^pt5sublep ")
#             if '_unblind' in torun:
#                 x = add(x,"--noStackSig --showIndivSigs --showRatio --maxRatioRange -2 5 --showMCError") 
#                 #x = add(x,"--plotmode norm")
#                 x = x.replace('-l 12.9','-l 10.1')
#                 x = x.replace('-l 35.9','-l 33.2')
#                 x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
#                 x = x.replace('mca-2los-mc.txt','mca-2los-mcdata-frdata.txt') #remove signal
#                 x = x.replace('mcc-sf1.txt','mcc-sf-lowmet.txt')
#         if '_nminus1' in torun: 
#             x = add(x,"--n-minus-one")
#             x = x.replace('-f','')
#             x = add(x,"--noStackSig --showIndivSigShapes --xp TChiNeuWZ_95,T2ttDeg_300,T2ttDeg_315")
#             #x = add(x,"--plotmode norm")
#         runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop'])

            


#     ### FR Application region, Data-MC, LowMET and HighMET 
#     if '2los_CR_FF_vars' in torun:
#         x = base('2los')
#         x = add(x,"--noStackSig --showIndivSigs --xp TChiNeuWZ_95")
#         if '_data' in torun: 
#             x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
#             x = add(x,"--showRatio --maxRatioRange -2 5 ") #--showMCError 
#         if '_met200_ewk_all' in torun:             
#             x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET -I ^TT -E ^pt5sublep -E ^SF -E ^MT") 
#             x = x.replace('-l 12.9','-l 12.9')
#         if '_met125_ewk_all' in torun: 
#             x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
#             x = add(x,"-E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -I ^TT -E ^pt5sublep -E ^MT") 
#             x = x.replace('-l 12.9','-l 10.1')  
#         if '_met200_stop_all' in torun:             
#             x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET -I ^TT") 
#             x = x.replace('-l 12.9','-l 12.9')
#         if '_met125_stop_all' in torun: 
#             x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
#             x = add(x,"-E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -I ^TT -E ^pt5sublep") 
#             x = x.replace('-l 12.9','-l 10.1')  
#         if '_met200_ewk_1T1F' in torun:             
#             x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET -E ^pt5sublep -E ^SF -E ^MT -X ^TT -E ^TnotT") 
#             x = x.replace('-l 12.9','-l 12.9')
#         if '_met125_ewk_1T1F' in torun: 
#             x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
#             x = add(x,"-E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -E ^pt5sublep -E ^MT -X ^TT -E ^TnotT") 
#             x = x.replace('-l 12.9','-l 10.1')  
#         if '_met200_stop_1T1F' in torun:             
#             x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET -X ^TT -E ^TnotT")  
#             x = x.replace('-l 12.9','-l 12.9')
#         if '_met125_stop_1T1F' in torun: 
#             x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
#             x = add(x,"-E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -E ^pt5sublep -X ^TT -E ^TnotT") 
#             x = x.replace('-l 12.9','-l 10.1')
#         if '_met200_ewk_1F1F' in torun:             
#             x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET -E ^pt5sublep -E ^SF -E ^MT -X ^TT -E ^notTnotT") 
#             x = x.replace('-l 12.9','-l 12.9')
#         if '_met125_ewk_1F1F' in torun: 
#             x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
#             x = add(x,"-E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -E ^pt5sublep -E ^MT -X ^TT -E ^notTnotT") 
#             x = x.replace('-l 12.9','-l 10.1')  
#         if '_met200_stop_1F1F' in torun:             
#             x = add(x,"-E ^highMET -X ^triggerAll -E ^triggerMET -X ^TT -E ^notTnotT")  
#             x = x.replace('-l 12.9','-l 12.9')
#         if '_met125_stop_1F1F' in torun: 
#             x = x.replace('puw2016_vtx_4fb(nVert)', 'puw2016_vtx_postTS_1p4fb(nVert)' )
#             x = add(x,"-E ^mm -E ^upperMET -E ^runRange -X ^triggerAll -E ^triggerDoubleMuMET -E ^pt5sublep -X ^TT -E ^notTnotT") 
#             x = x.replace('-l 12.9','-l 10.1')         
#         runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop'])


 




# # to be added if we want to relax these cuts in CR with MET>200
# #-X ^HT -X ^Upsilon_veto -R ^ISRjet noIDISRjet 'Jet1_pt > 25 && fabs(Jet1_eta)<2.4' -R METovHT relaxMETovHT '(met_pt/(htJet25-LepGood1_pt-LepGood2_pt))>(2/3)'


#     # ### WZ Control Region, Data-MC, HighMET         
#     # if '2los_CR_WZ_vars' in torun:
#     #     x = base('2los')
#     #     x = add(x,"--noStackSig --showIndivSigs --xp TChiNeuWZ_95")
#     #     if '_data' in torun: 
#     #         x = x.replace('mca-2los-mc.txt','mca-2los-mcdata.txt')
#     #         x = add(x,"--showRatio --maxRatioRange -2 5") #--showMCError
#     #     if '_met200' in torun:             
#     #         x = add(x,"-E ^highMET -E ^MT -R ^TT CRTTTT 'LepGood1_isTightCRTT && LepGood2_isTightCRTT' -R ^ledlepPt NoUpledlepPt '20 < LepGood1_pt' -X ^dilep -X ^opposite-sign -X ^Mll -E ^minMll -E ^triLep -E ^Zpeak -X ^triggerAll -E ^triggerMET -X ^HT -X ^Upsilon_veto -R METovHT relaxMETovHT '(met_pt/(htJet25-LepGood1_pt-LepGood2_pt))>(2/3)' ")
#     #         x = x.replace('-l 12.9','-l 12.9')
#     #     runIt(x,'%s/all'%torun,[],['SR_bins_EWKino','SR_bins_stop'])


