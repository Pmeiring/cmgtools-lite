#!/usr/bin/env python
import sys
import re
import os
import argparse

helpText = "LEP = '2los', '3los'\n\
REG = 'sr', 'sr_col', 'cr_dy', 'cr_tt', 'cr_vv', 'cr_ss','cr_wz', 'appl', 'appl_col', 'cr_ss_1F_NoSF', 'cr_ss_2F_NoSF', 'cr_ss_2F_SF2', 'cr_ss_1F_SF1', 'cr_ss_dd', 'cr_ss_semidd', 'appl_1F_NoSF','appl_2F_NoSF', 'appl_1F_SF1F', 'appl_2F_SF2F','sr_semidd','sr_dd', 'appl_col_1F_NoSF', 'appl_col_2F_NoSF', 'sr_col_semidd', 'sr_col_dd', 'sr_3l_semidd', 'sr_closure', 'closure_norm'\n\
BIN = 'min', 'low', 'med', 'high'"
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 epilog=helpText)
parser.add_argument("outDir", help="Choose the output directory.\nOutput will be saved to 'outDir/year/LEP_REG_BIN'")
parser.add_argument("year", help="Choose the year: '2016', '2017' or '2018'")
parser.add_argument("--lep", default=None, required=True, help="Choose number of leptons to use (REQUIRED)")
parser.add_argument("--reg", default=None, required=True, help="Choose region to use (REQUIRED)")
parser.add_argument("--bin", default=None, required=True, help="Choose bin to use (REQUIRED)")
parser.add_argument("--signal", action="store_true", default=False, help="Include signal")
parser.add_argument("--data", action="store_true", default=False, help="Include data")
parser.add_argument("--norm", action="store_true", default=False, help="Normalize signal to data")
parser.add_argument("--unc", action="store_true", default=False, help="Include uncertainties")
parser.add_argument("--inPlots", default=None, help="Select plots, separated by commas, no spaces")
parser.add_argument("--exPlots", default=None, help="Exclude plots, separated by commas, no spaces")
parser.add_argument("--signalMasses", default=None, help="Select only these signal samples (e.g 'signal_TChiWZ_100_70+'), comma separated. Use only when doing 'cards'")
parser.add_argument("--doWhat", default="plots", help="Do 'plots' or 'cards'. Default = '%(default)s'")
parser.add_argument("--htcondor", action="store_true", default=False, help="Submit jobs on HTCondor. Currently only for 'cards' mode")
parser.add_argument("--queue", default="longlunch", help="HTCondor queue for job submission")
parser.add_argument("--allCards", action="store_true", default=False, help="run cards for all years, cats and bins")
parser.add_argument("--runCombine", action="store_true", default=False, help="combine cards and run limit")
parser.add_argument("--asimov", dest="asimov", default=None, help="Use an Asimov dataset of the specified kind: including signal ('signal','s','sig','s+b') or background-only ('background','bkg','b','b-only')")
args = parser.parse_args()

ODIR=args.outDir
YEAR=args.year
conf="%s_%s_%s"%(args.lep,args.reg,args.bin)

if YEAR not in ("2016","2017","2018"): raise RuntimeError("Unknown year: Please choose '2016', '2017' or '2018'")
if args.lep not in ["2los","3l"]: raise RuntimeError("Unknown choice for LEP option. Please check help" )
if args.reg not in ["sr", "sr_col", "cr_dy", "cr_tt", "cr_vv", "cr_ss","cr_ss_1F_NoSF", "cr_ss_2F_NoSF", "cr_ss_2F_SF2", "cr_ss_1F_SF1", "cr_ss_dd", "cr_ss_semidd","cr_wz", "appl","appl_1F_NoSF", "appl_2F_NoSF","appl_3F_NoSF","appl_1F_SF1F", "appl_2F_SF2F","appl_3F_SF3F",  "appl_col",  "appl_col_1F_NoSF", "appl_col_2F_NoSF", "sr_semidd","sr_dd", "sr_col_semidd", "sr_col_dd", "sr_3l_semidd", "sr_closure", "closure_norm"]: raise RuntimeError("Unknown choice for REG option. Please check help." )
if args.bin not in ["min", "low", "med", "high"]: raise RuntimeError("Unknown choice for BIN option. Please check help." )
if args.doWhat not in ["plots", "cards"]: raise RuntimeError("Unknown choice for DOWHAT option. Please check help." ) # More options to be added
if args.signalMasses and args.doWhat != "cards": print "Option SIGNALMASSES to be used only with the 'cards' option. Ignoring it...\n"

lumis = {
'2016': '35.9', # '33.2' for low MET
'2017': '41.5', # '36.7' for low MET
'2018': '59.7', # '59.2' for low MET
}
LUMI= " -l %s "%(lumis[YEAR])


submit = '{command}' 
#args.doWhat = "dumps" 
#args.doWhat = "yields" 
#args.doWhat = "ntuple"

P0="/eos/cms/store/cmst3/group/tthlep/peruzzi/NanoTrees_SOS_230819_v5/"
# P0="/afs/cern.ch/work/p/pmeiring/private/CMS/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/cfg/BatchSignalOnly/"
nCores = 8
TREESALL = " --Fs {P}/recleaner/ --FMCs {P}/bTagWeights -P "+P0+"%s "%(YEAR)
HIGGSCOMBINEDIR="/afs/cern.ch/user/v/vtavolar/work/SusySOSSW_2_clean/CMSSW_8_1_0/src"

def base(selection):
    CORE=TREESALL
    CORE+=" -f -j %d --split-factor=-1 --year %s --s2v -L susy-sos/functionsSOS.cc -L susy-sos/functionsSF.cc --tree NanoAOD --mcc susy-sos/mcc_sos.txt --mcc susy-sos/mcc_triggerdefs.txt "%(nCores,YEAR) # --neg"
    if  args.reg=="cr_ss_dd"or args.reg=='cr_ss_semidd'  or args.reg=='cr_ss_1F_SF1' or args.reg=='cr_ss_2F_SF2': CORE+="--mcc susy-sos/fakerate/%s/%s/ScaleFactors_SemiDD/mcc_SF_ss.txt"%(YEAR,args.lep)
    if args.reg=="appl_1F_SF1F" or args.reg=="appl_2F_SF2F" or args.reg=="sr_semidd" or args.reg=='sr_closure' or args.reg=='closure_norm': CORE+="--mcc susy-sos/fakerate/%s/%s/ScaleFactors_SemiDD/mcc_SF_appl_%s.txt"%(YEAR,args.lep,args.bin)
    if args.reg=="sr_col_semidd": CORE+="--mcc susy-sos/fakerate/%s/%s/ScaleFactors_SemiDD/mcc_SF_col_%s.txt"%(YEAR,args.lep,args.bin)
    if args.reg=="sr_3l_semidd" : CORE+="--mcc susy-sos/fakerate/%s/%s/ScaleFactors_SemiDD/mcc_SF_%s.txt"%(YEAR,args.lep,args.bin)
    if YEAR == "2017": CORE += " --mcc susy-sos/mcc_METFixEE2017.txt "
    RATIO= " --maxRatioRange 0.0  1.99 --ratioYNDiv 505 "
    RATIO2=" --showRatio --attachRatioPanel --fixRatioRange "
    LEGEND=" --legendColumns 2 --legendWidth 0.25 "
    LEGEND2=" --legendFontSize 0.042 "
    SPAM=" --noCms --topSpamSize 1.1 --lspam '#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}' "
    if args.doWhat == "plots": 
        CORE+=LUMI+RATIO+RATIO2+LEGEND+LEGEND2+SPAM+" --showMCError "
        if args.signal: CORE+=" --noStackSig --showIndivSigs "
        else: CORE+=" --xp signal.* "

    wBG = " '1.0' "
    #wFS = " '1.0' "
    if selection=='2los':
         GO="%s susy-sos/mca/mca-2los-%s.txt susy-sos/2los_cuts.txt "%(CORE, YEAR)
         if args.doWhat in ["plots","ntuple"]: GO+=" susy-sos/2los_plots.txt "
         if args.doWhat in ["cards"]: GO+="  mass_2(LepGood1_pt, LepGood1_eta, LepGood1_phi, LepGood1_mass, LepGood2_pt, LepGood2_eta, LepGood2_phi, LepGood2_mass) [4,10,20,30,50] "
         

         wBG = " 'puWeight*eventBTagSF*triggerSF(muDleg_SF(%s,LepGood1_pt,LepGood1_eta,LepGood2_pt,LepGood2_eta), MET_pt, metmm_pt(LepGood1_pdgId,LepGood1_pt,LepGood1_phi,LepGood2_pdgId,LepGood2_pt,LepGood2_phi,MET_pt,MET_phi), %s)*lepSF(LepGood1_pt,LepGood1_eta,LepGood1_pdgId,%s)*lepSF(LepGood2_pt,LepGood2_eta,LepGood2_pdgId,%s)' "%(YEAR,YEAR,YEAR,YEAR)
         GO="%s -W %s"%(GO,wBG)

         if args.doWhat == "plots": GO=GO.replace(LEGEND, " --legendColumns 3 --legendWidth 0.62 ")
         if args.doWhat == "plots": GO=GO.replace(RATIO,  " --maxRatioRange 0.6  1.99 --ratioYNDiv 210 ")
         if args.doWhat == "cards":         
             GO += " --binname %s "%args.bin
         else:
             GO += " --binname 2los "

 
    elif selection=='3l':
        GO="%s susy-sos/mca/mca-3l-%s.txt susy-sos/3l_cuts.txt "%(CORE,YEAR)
        if args.doWhat in ["plots","ntuple"]: GO+=" susy-sos/3l_plots.txt "
        if args.doWhat in ["cards"]: GO+="  minMllSFOS [4,10,20,30,50] "
        
        wBG = " 'puWeight*eventBTagSF*triggerSF(muDleg_SF(%s,LepGood1_pt,LepGood1_eta,LepGood2_pt,LepGood2_eta,LepGood3_pt,LepGood3_eta,lepton_permut(LepGood1_pdgId,LepGood2_pdgId,LepGood3_pdgId)), MET_pt, metmmm_pt(LepGood1_pt, LepGood1_phi, LepGood2_pt, LepGood2_phi, LepGood3_pt, LepGood3_phi, MET_pt, MET_phi, lepton_Id_selection(LepGood1_pdgId,LepGood2_pdgId,LepGood3_pdgId)), %s)*lepSF(LepGood1_pt,LepGood1_eta,LepGood1_pdgId,%s)*lepSF(LepGood2_pt,LepGood2_eta,LepGood2_pdgId,%s)*lepSF(LepGood3_pt,LepGood3_eta,LepGood3_pdgId,%s)' "%(YEAR,YEAR,YEAR,YEAR,YEAR)
        GO="%s -W %s"%(GO,wBG)

        if args.doWhat == "plots": GO=GO.replace(LEGEND, " --legendColumns 3 --legendWidth 0.42 ")
        if args.doWhat == "cards":         
            GO += " --binname %s "%args.bin
        else:
            GO += " --binname 3l "

    else:
        raise RuntimeError('Unknown selection')

    return GO

def promptsub(x):
    procs = [ '' ]
    if args.doWhat == "cards": procs += ['_FRe_norm_Up','_FRe_norm_Dn','_FRe_pt_Up','_FRe_pt_Dn','_FRe_be_Up','_FRe_be_Dn','_FRm_norm_Up','_FRm_norm_Dn','_FRm_pt_Up','_FRm_pt_Dn','_FRm_be_Up','_FRm_be_Dn']
    return x + ' '.join(["--plotgroup data_fakes%s+='.*_promptsub%s'"%(x,x) for x in procs])+" --neglist '.*_promptsub.*' "

def procs(GO,mylist):
    return GO+' '+" ".join([ '-p %s'%l for l in mylist ])

def sigprocs(GO,mylist):
    return procs(GO,mylist)+' --showIndivSigs --noStackSig'

def createPath(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def prepareSubmitter(name, cmd):
    template = [l.strip("\n") for l in open("scripts/htcondor_submitter.sh").readlines()]
    filename="/%s/src//submitJob_%s.sh"%(ODIR,name.replace("_%s"%YEAR,''))
    if args.allCards:
        filename=filename.replace("%s"%args.lep,'').replace("_%s"%args.reg,'').replace("_%s"%args.bin,'').replace('__','_')
    if os.path.isfile(filename): return
    createPath(filename)
    f = open(filename, "w")
    if args.allCards:
        name=name.replace("_%s"%YEAR,'').replace("%s"%args.lep,'').replace("_%s"%args.reg,'').replace("_%s"%args.bin,'')
        name=name.replace('__','_')
        if name.startswith('_'): name=name.replace('_','',1)
    jobid = 'job_%s'%name
    for line in template:
#        line = line.replace("[SCRIPT]"        , "%s/jobs/runJob_%s.sh"%(ODIR,name))
        line = line.replace("[SCRIPT]"        , "/%s/src//wrapRunners_%s.sh"%(ODIR,name.replace("_%s"%YEAR,'')))
        line = line.replace("[NAME]"       , name                      )
        line = line.replace("[DIR]"     , "%s/jobs/"%(ODIR)                       )
        line = line.replace("[QUEUE]"      , args.queue                                   )
        f.write(line+"\n")
    f.close()

def prepareRunner(name, cmd):
    template = [l.strip("\n") for l in open("scripts/htcondor_runner.sh").readlines()]
    filename = "%s/jobs/runJob_%s.sh"%(ODIR,name)
    createPath(filename)
    f = open(filename, "w")
    jobid = 'job_%s'%name
    cmssw  = os.popen("echo $CMSSW_BASE").read().strip('\n')
    for line in template:
        line = line.replace("[SRC]"        , "%s/src/"%cmssw)
        line = line.replace("[INST]"       , name                      )
        line = line.replace("[JOBDIR]"     , "%s/src/"%ODIR                       )
        line = line.replace("[JOBID]"      , jobid                                   )
        line = line.replace("[CMD]"      , cmd                                   )
        f.write(line+"\n")
    f.close()

def prepareWrapper(name):
    if not args.allCards:
        nameWr=name.replace("_%s"%YEAR,'')
        filename="/%s/src//wrapRunners_%s.sh"%(ODIR,nameWr)
        print filename
        if os.path.isfile(filename): return
        createPath(filename)
        f = open(filename, "w")
        f.write("#!/bin/bash\n")
        for year in ["2016","2017","2018"]:
            f.write('if test -f "%s/jobs/runJob_%s_%s.sh"; then\n'%(ODIR,nameWr,year))
            f.write('    echo "running %s"\n'%YEAR)
            f.write('    source "%s/jobs/runJob_%s_%s.sh"\n'%(ODIR,nameWr,year))
            f.write('fi\n')
    else:
        nameWr=name.replace("_%s"%YEAR,'').replace("%s"%args.lep,'').replace("_%s"%args.reg,'').replace("_%s"%args.bin,'')
        print nameWr
        filename="/%s/src//wrapRunners_%s.sh"%(ODIR,nameWr)
        print filename
        filename=filename.replace('__','_')
        print filename
        if os.path.isfile(filename): return
        createPath(filename)
        f = open(filename, "w")
        f.write("#!/bin/bash\n")
        nameSplit = name.split('_')
        for year in ["2016","2017","2018"]:
            for nlep in ["2los","3l"]:
                for ireg in ["sr","cr_ss"]:
                    for ibin in ["low","med","high"]:
                        if ibin == "high" and nlep != "2los" and ireg!="sr": continue
                        if ireg == "cr_ss" and nlep != "2los" and ibin != "med": continue
                        newName = '_'.join([nlep,ireg,ibin,nameSplit[3],nameSplit[4],year])
                        f.write('if test -f "%s/jobs/runJob_%s.sh"; then\n'%(ODIR,newName))
                        f.write('    echo "running %s"\n'%year)
                        f.write('    source "%s/jobs/runJob_%s.sh"\n'%(ODIR,newName))
                        f.write('fi\n')
        f.write( 'CARDS=""\n' )
        masses = '_'.join((args.signalMasses.rstrip('+').split('_'))[-2:])
        f.write( 'for f in `find   %s/scan/SR -name "%s"`\n'%(ODIR,masses) )
        f.write( 'do CARDS="${CARDS} `find  $f -regex .*txt`"\n'  )
        f.write( 'done\n' )
        f.write( 'echo ${CARDS}\n' )
        f.write( 'cd %s\n'%(HIGGSCOMBINEDIR) )
        f.write( 'eval `scramv1 runtime -sh`\n' )
        f.write( 'cd -\n' )
        f.write( '[ -d %s/combinedCards ] || mkdir %s/combinedCards\n'%(ODIR,ODIR) )
        f.write( 'combineCards.py -S $CARDS > %s/combinedCards/%s.txt\n' %( ODIR, masses) )
        f.write( '[ -d %s/limits ] || mkdir %s/limits\n'%(ODIR,ODIR) )
        f.write( 'combine -M Asymptotic %s/combinedCards/%s.txt -n %s -m %s > %s/limits/%s_limit.txt \n'%(ODIR, masses, masses, masses.split('_')[0], ODIR, masses ) )
        f.write( 'mv higgsCombine%s.Asymptotic.mH%s.root %s/limits \n'%(masses, masses.split('_')[0], ODIR ) )
    
    f.close()

def runIt(GO,name):
    if args.data and not args.doWhat == "cards" : name=name+"_data"
    if args.norm: name=name+"_norm"
    if args.unc: name=name+"_unc"
    if args.doWhat == "cards": mass = '_'.join(name.split('_')[-2:])
#    print name.split('_')[-2]
#    print mass
#    print name+"\n"
    if args.doWhat == "plots":  
        ret = submit.format(command=' '.join(['python mcPlots.py',"--pdir %s/%s/%s"%(ODIR,YEAR,name),GO,' '.join(['--sP %s'%p for p in (args.inPlots.split(",") if args.inPlots is not None else []) ]),' '.join(['--xP %s'%p for p in (args.exPlots.split(",") if args.exPlots is not None else []) ])]))

    if args.doWhat == "cards":  
        ret = submit.format(command=' '.join(['python makeShapeCardsNew.py --savefile',"--outdir %s/scan/SR/%s/%s/%sfb/TChiWZ/%s/sig_TChiWZ_%s/"%(ODIR,YEAR,name.replace("_%s"%mass,''),LUMI.strip('-l ').replace('.', 'p'),mass,mass),GO,' '.join(['--sP %s'%p for p in (args.inPlots.split(",") if args.inPlots is not None else []) ]),' '.join(['--xP %s'%p for p in (args.exPlots.split(",") if args.exPlots is not None else []) ]), "--xp='signal(?!.*%s).*'"%args.signalMasses.strip('signal') if args.signalMasses is not None else '', "--all-processes", "--asimov=%s"%(args.asimov) if args.asimov is not None else ''   ]))
        
    print ret
    if args.htcondor:
        prepareSubmitter("%s_%s"%(name,YEAR),ret)
        prepareRunner("%s_%s"%(name,YEAR),ret)
        prepareWrapper("%s_%s"%(name,YEAR))    

    # What is supposed to be included in sys.argv[4] and after?
    #elif args.doWhat == "yields": print 'echo %s; python mcAnalysis.py'%name,GO,' '.join(sys.argv[4:])
    #elif args.doWhat == "dumps":  print 'echo %s; python mcDump.py'%name,GO,' '.join(sys.argv[4:])
    #elif args.doWhat == "ntuple": print 'echo %s; python mcNtuple.py'%name,GO,' '.join(sys.argv[4:])

def add(GO,opt):
    return '%s %s'%(GO,opt)

def setwide(x):
    x2 = add(x,'--wide')
    x2 = x2.replace('--legendWidth 0.35','--legendWidth 0.20')
    return x2

def binChoice(x,torun):
    metBinTrig = ''
    metBinInf = ''
    metBinSup = ''
    x2 = add(x,'-E ^eventFilters$ ')
    if '_min' in torun:
        metBinTrig = 'met75'
        metBinInf = 'met75'
    elif '_low' in torun:
        metBinTrig = 'met125'
        metBinInf = 'met125'
        metBinSup = 'met200'
    elif '_med' in torun:
        metBinTrig = 'met200'
        metBinInf = 'met200'
        metBinSup = 'met250' if ( ('2los_' in torun) and ('cr_' not in torun) and ('_col' not in torun) ) else ''
        x2 = add(x2,'-X ^mm$ ')
    elif '_high' in torun:
        metBinTrig = 'met250'
        metBinInf = 'met250'
        x2 = add(x2,'-X ^mm$ ')
    if metBinInf != '': x2 = add(x2,'-E ^'+metBinInf+'$ -E ^'+metBinTrig+'_trig$ ')
    if metBinSup != '': x2 = add(x2,'-E ^'+metBinSup+'$ -I ^'+metBinSup+'$ ')

    if metBinTrig=='': print "\n--- NO TRIGGER APPLIED! ---\n"
    return x2

allow_unblinding = False


if __name__ == '__main__':

    torun = conf

    if (not args.doWhat=="cards" ) and ((not allow_unblinding) and args.data and (not any([re.match(x.strip()+'$',torun) for x in ['.*appl.*','.*cr.*','3l.*_Zpeak.*']]))): raise RuntimeError, 'You are trying to unblind!'


    if '2los_' in torun:
        x = base('2los')
        x = binChoice(x,torun)
    
        if 'sr' in torun:
            if '_col' in torun:
                x = add(x,"-X ^mT$ -X ^SF$ ")
                if '_med' in torun: 
                     x = add(x,"-X ^pt5sublep$ ")
                     x = x.replace('-E ^met200$','-E ^met200_col$')
                if '_high' in torun: 
                     x = add(x,"-X ^pt5sublep$ ")
                     x = x.replace('-E ^met250$','-E ^met300_col$')
            if '_semidd' in torun:
                x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/mca-2los-%s-semidd.txt'%(YEAR))
            if '_dd' in torun:
                x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/mca-2los-%s-dd.txt'%(YEAR))
            if '_closure' in torun:
                x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/mca-2los-%s-closure.txt'%(YEAR))
                x = add(x, "--plotmode=%s"%("nostack"))
            if '_closure_norm' in torun:
                x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/mca-2los-%s-closure.txt'%(YEAR))
                x = add(x, "--plotmode=%s"%("norm"))

        if 'appl' in torun:
            if '_col' in torun:
                x = add(x,"-X ^mT$ -X ^SF$ ")
                if '_med' in torun: 
                    x = add(x,"-X ^pt5sublep$ ")
                    x = x.replace('-E ^met200$','-E ^met200_col$')
                if '_high' in torun: 
                    x = add(x,"-X ^pt5sublep$ ")
                    x = x.replace('-E ^met250$','-E ^met300_col$')
            x = add(x,"-X ^twoTight$ ")
            x = add(x,"-E ^oneNotTight$ ")
            if '1F_NoSF' in torun:
                x = add(x, "-E ^1LNT$ -X ^oneNotTight$")
            elif '2F_NoSF' in torun:
                x = add(x, "-E ^2LNT$ -X ^oneNotTight$")
            elif '1F_SF1F' in torun:
                x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/mca-2los-%s-1F.txt'%(YEAR))
                x = add(x, " -E ^1LNT$ -X ^oneNotTight$ --sP SR_2l_ewk")
            elif '2F_SF2F' in torun:
                x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/mca-2los-%s-2F.txt'%(YEAR))
                x = add(x, "-E ^2LNT$ -X ^oneNotTight$ --sP SR_2l_ewk")


        if 'cr_' in torun:
            x = add(x, "-X ^SF$ ")

        if 'cr_dy' in torun:
            if '_med' in torun: x = x.replace('-E ^met200$','-E ^met200_CR$')
            x = add(x,"-X ^ledlepPt$ -X ^twoTight$ ")
            x = add(x,"-I ^mtautau$ ")
            x = add(x,"-E ^CRDYlepId$ -E ^CRDYledlepPt$ ")

        if 'cr_tt' in torun:
            if '_med' in torun:
                x = x.replace('-E ^met200$','-E ^met200_CR$')
                x = add(x,'-X ^pt5sublep$ ')
            x = add(x,"-X ^ledlepPt$ -X ^twoTight$ -X ^bveto$ -X ^mT$ ")
            x = add(x,"-E ^CRTTlepId$ -E ^CRTTledlepPt$ -E ^btag$ ")

        if 'cr_vv' in torun:
            if '_med' in torun:
                x = x.replace('-E ^met200$','-E ^met200_CR$')
                x = add(x,'-X ^pt5sublep$ ')
            x = add(x,"-X ^ledlepPt$ -X ^twoTight$ -X ^bveto$ -X ^mT$ ")
            x = add(x,"-E ^CRVVlepId$ -E ^CRVVleplepPt$ -E ^CRVVbveto$ -E ^CRVVmT$ ")

        if 'cr_ss' in torun:
            if '_med' in torun:
                x = x.replace('-E ^met200$','-E ^met200_CR$')
                x = add(x,'-X ^pt5sublep$ ')
            x = add(x,"-X ^mT$")
            x = add(x,"-I ^OS$  ")
            if '1F' in torun:
                x = add(x, "-E ^1LNT$ -X ^twoTight$" )
            elif '2F' in torun:
                x = add(x, "-E ^2LNT$ -X ^twoTight$" )    
            elif '_1F_SF1' in torun:
                x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/mca-2los-%s-1F.txt'%(YEAR))
                x = add(x, "-E ^1LNT$ -X ^twoTight$" )
            elif '_2F_SF2' in torun:
                x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/mca-2los-%s-2F.txt'%(YEAR))
                x = add(x, "-E ^2LNT$ -X ^twoTight$")
            elif '_dd' in torun:
                x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/mca-2los-%s-dd.txt'%(YEAR))
                x = add(x, "--sP SR_2l_ewk --sP lep1pt")
            elif '_semidd' in torun:
                x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/mca-2los-%s-semidd.txt'%(YEAR))
                x = add(x, "--sP SR_2l_ewk --sP lep1pt")

    elif '3l_' in torun:
        x = base('3l')
        x = binChoice(x,torun)
        if '_dd' in torun:
                x = x.replace('susy-sos/mca/mca-3l-%s.txt'%(YEAR),'susy-sos/mca/mca-3l-%s-dd.txt'%(YEAR))    
        if '_semidd' in torun:
                x = x.replace('susy-sos/mca/mca-3l-%s.txt'%(YEAR),'susy-sos/mca/mca-3l-%s-semidd.txt'%(YEAR))    

        if 'appl' in torun:
            x = add(x,"-X ^threeTight$ ")
            x = add(x,"-E ^oneNotTight$ ")
            if '1F_NoSF' in torun:
                x = add(x, "-E ^1LNT$ -X ^oneNotTight$ --sP yields")
            elif '2F_NoSF' in torun:
                x = add(x, "-E ^2LNT$ -X ^oneNotTight$ --sP yields")
            elif '3F_NoSF' in torun:
                x = add(x, "-E ^3LNT$ -X ^oneNotTight$ --sP yields")
            if '1F_SF1F' in torun:
                x = x.replace('susy-sos/mca/mca-2los-%s.txt'%(YEAR),'susy-sos/mca/mca-2los-%s-1F.txt'%(YEAR))
                x = add(x, "-E ^1LNT$ -X ^oneNotTight$ --sP SR_3l")
            elif '2F_SF2F' in torun:
                 x= add(x, " --xp fakes_matched1.* --xp fakes_matched3.* --xp Fakes.* --xp fakes_matchedAll.* -E ^2LNT$ -X ^oneNotTight$ --sP SR_3l")
            elif '3F_SF3F' in torun:
                 x= add(x, " --xp fakes_matched1.* --xp fakes_matched2.* --xp Fakes.* --xp fakes_matchedAll.* -E ^3LNT$ -X ^oneNotTight$ --sP SR_3l")


        if 'cr_wz' in torun:
            x = add(x,"-X ^minMll$ -X ^ZvetoTrigger$ -X ^ledlepPt$ -X ^threeTight$ -X ^pt5sublep$ ")
            x = add(x,"-E ^CRWZlepId$ -E ^CRWZmll$ ")
            if '_min' in torun: 
                x = add(x,"-E ^CRWZPtLep_MuMu$ ")
            if '_low' in torun: 
                x = add(x,"-E ^CRWZPtLep_MuMu$ ")
                x = x.replace('-E ^met125_trig','-E ^met125_trig_CR')
                x = x.replace('triggerSF','triggerWZSF')
            if '_med' in torun: x = add(x,"-E ^CRWZPtLep_HighMET$ ")


    if not args.data: x = add(x,'--xp data ')
    if args.unc: x = add(x,"--unc susy-sos/systsUnc.txt")
    if args.norm: x = add(x,"--sp '.*' --scaleSigToData ")

    if '_low' in torun :
        if YEAR=="2016" and "cr_wz" not in torun: x = x.replace(LUMI," -l 33.2 ")
        if YEAR=="2017": x = x.replace(LUMI," -l 36.7 ")
        if YEAR=="2018" and "cr_wz" not in torun: x = x.replace(LUMI," -l 59.2 ")

    if args.doWhat == "cards" and args.signalMasses:
        masses=args.signalMasses.rstrip('+').split('_')
        masses='_'.join(masses[-2:])
        torun=torun+'_'+masses
    runIt(x,'%s'%torun)

######################################################################################
# Useful options for plotting, to be used when needed
#
#        if '_1fo' in torun:
#            x = add(x,"-A alwaystrue 1FO 'LepGood1_isLepTight+LepGood2_isLepTight==1'")
#        if '_2fo' in torun: x = add(x,"-A alwaystrue 2FO 'LepGood1_isLepTight+LepGood2_isLepTight==0'")
#        if '_table' in torun:
#            x = x.replace('mca-2lss-mc.txt','mca-2lss-mc-table.txt')
#        if '_frdata' in torun: # Why?
#            x = promptsub(x)
#            if '_blinddata' in torun:
#                x = x.replace('mca-2lss-mc.txt','mca-2lss-mcdata.txt')
#                x = add(x,'--xp data ')
#            elif not '_data' in torun: raise RuntimeError
#            x = x.replace('mca-2lss-mcdata.txt','mca-2lss-mcdata-frdata.txt')
#            if '_table' in torun:
#                x = x.replace('mca-2lss-mcdata-frdata.txt','mca-2lss-mcdata-frdata-table.txt')
