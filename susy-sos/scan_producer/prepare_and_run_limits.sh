#!/bin/bash
eval `scramv1 runtime -sh`

## ==> COPY this script into /python/plotter folder <==

# Set here output dirs and types of limits 
type="_unblind" ## type of limits you want to extract
## can be: '_unblind' (observed) or _ddbkg (expected)
DIR=fullsyst_2los_onepoint_unblind/ #onepoint_Stop_forPostFit_final/ #observed_limit_scan_final_moriond17_T2tt/  # local dir where all the temporary cards and histograms will be saved
version=result_v0  # if you want a different versioning inside the $DIR
WWWDIR=/afs/cern.ch/user/b/botta/www/2017/SoftAndDisplaced/trees_SOS_010217/260717 ## Directory where you want to save the final results (combined final limits)
signal="ewk" #"stop" #"ewk"
signalName="sig_TChiWZ_225_205"  #"TChiWZ_150_dM7" #"T2tt_350_dM20" #"TChiWZ_150_dM20"   #"T2tt_350_dM20" (as in mca)
echo "Producing cards from sos_plot.py"


#### 2l OS Signal Regions

python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_${signal}_met125_mm$type
python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_${signal}_met125_mm$type | sh                                                                  
python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_${signal}_met200$type
python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_${signal}_met200$type | sh 
python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_${signal}_met300$type
python susy-sos/sos_plots.py $DIR 2los_SR_bins_notriggers_${signal}_met300$type | sh                                                                      

# #### 2l OS Background region

python susy-sos/sos_plots.py $DIR 2los_CR_DY_vars_data_${signal}_met125$type
python susy-sos/sos_plots.py $DIR 2los_CR_DY_vars_data_${signal}_met125$type  | sh      
python susy-sos/sos_plots.py $DIR 2los_CR_TT_vars_dataMET_${signal}_met125$type
python susy-sos/sos_plots.py $DIR 2los_CR_TT_vars_dataMET_${signal}_met125$type  | sh                                                
python susy-sos/sos_plots.py $DIR 2los_CR_DY_vars_data_${signal}_met200$type
python susy-sos/sos_plots.py $DIR 2los_CR_DY_vars_data_${signal}_met200$type    | sh
python susy-sos/sos_plots.py $DIR 2los_CR_TT_vars_dataMET_${signal}_met200$type 
python susy-sos/sos_plots.py $DIR 2los_CR_TT_vars_dataMET_${signal}_met200$type   | sh 

python susy-sos/sos_plots.py $DIR 2los_CR_SS_bins_notriggers_${signal}_met200$type 
python susy-sos/sos_plots.py $DIR 2los_CR_SS_bins_notriggers_${signal}_met200$type | sh


##### 3l Signal region

# python susy-sos/sos_plots.py $DIR 3l_SR_bins_notriggers_${signal}_met75_lowPt3l$type
# python susy-sos/sos_plots.py $DIR 3l_SR_bins_notriggers_${signal}_met75_lowPt3l$type | sh
# python susy-sos/sos_plots.py $DIR 3l_SR_bins_notriggers_${signal}_met75_highPt3l$type 
# python susy-sos/sos_plots.py $DIR 3l_SR_bins_notriggers_${signal}_met75_highPt3l$type | sh
# python susy-sos/sos_plots.py $DIR 3l_SR_bins_notriggers_${signal}_met125_lowPt3l$type
# python susy-sos/sos_plots.py $DIR 3l_SR_bins_notriggers_${signal}_met125_lowPt3l$type | sh
# python susy-sos/sos_plots.py $DIR 3l_SR_bins_notriggers_${signal}_met125_highPt3l$type
# python susy-sos/sos_plots.py $DIR 3l_SR_bins_notriggers_${signal}_met125_highPt3l$type | sh
# python susy-sos/sos_plots.py $DIR 3l_SR_bins_notriggers_${signal}_met200$type
# python susy-sos/sos_plots.py $DIR 3l_SR_bins_notriggers_${signal}_met200$type | sh 


################## RUNNING COMBINE #############################################


exit 0

#if [ ls $DIR ]  
#then
#    echo "$DIR existing"
#else
mkdir $DIR
#fi

cd $DIR
mkdir $version
cd /afs/cern.ch/user/b/botta/CMGToolsGit/Combine/CMSSW_7_4_7/src 
eval `scramv1 runtime -sh`
cd -
echo pwd

#if [ ls $WWWDIR/$DIR ]  
#then
#echo "$WWWDIR/$DIR existing"
#else
#    echo "Creating $WWWDIR/$DIR combined_limits directory"
mkdir $WWWDIR/$DIR
#fi



#separate -- SKIP
#echo "Running on separate datacards..."
#if [ $type != "_unblind" ]  
#then
#    combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk20_met125_mm.txt
 ##   combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk20_met200.txt
 ##   combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk10_met125_mm.txt
 ##   combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk10_met200.txt
 ##   combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop20_met125_mm.txt
 ##   combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop20_met200.txt
 ##   combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop35_met125_mm.txt
 ##   combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop35_met200.txt
#else
#    echo " Running UNBLINDED..."
#    combine -M Asymptotic --datacard=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk20_met125_mm.txt
#    combine -M Asymptotic --datacard=TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk20_met200.txt    
   ## combine -M Asymptotic --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk10_met125_mm.txt
    ##combine -M Asymptotic --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_ewk10_met200.txt
   ## combine -M Asymptotic --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop20_met125_mm.txt
    ##combine -M Asymptotic --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop20_met200.txt 
   ## combine -M Asymptotic --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_met125_mm$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop35_met125_mm.txt
    ##combine -M Asymptotic --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_met200$type.card.txt > $version/Asymp_2los_SR_bins_notriggers_stop35_met200.txt
#fi


## combining
echo "Combining datacards..."

### 2lOS with CR
combineCards.py SR_MET125=${signalName}/2los_SR_bins_notriggers_${signal}_met125_mm$type.card.txt SR_MET200=${signalName}/2los_SR_bins_notriggers_${signal}_met200$type.card.txt SR_MET300=${signalName}/2los_SR_bins_notriggers_${signal}_met300$type.card.txt DYCR_MET125=${signalName}/2los_CR_DY_vars_data_${signal}_met125$type.card.txt DYCR_MET200=${signalName}/2los_CR_DY_vars_data_${signal}_met200$type.card.txt TTCR_MET125=${signalName}/2los_CR_TT_vars_dataMET_${signal}_met125$type.card.txt  TTCR_MET200=${signalName}/2los_CR_TT_vars_dataMET_${signal}_met200$type.card.txt SSCR_MET200=${signalName}/2los_CR_SS_bins_notriggers_${signal}_met200$type.card.txt > ${signalName}/2los_SR_bins_notriggers_${signal}_comb.card.txt


### 2lOS without CR
#combineCards.py SR_MET125=${signalName}/2los_SR_bins_notriggers_${signal}_met125_mm$type.card.txt SR_MET200=${signalName}/2los_SR_bins_notriggers_${signal}_met200$type.card.txt SR_MET300=${signalName}/2los_SR_bins_notriggers_${signal}_met300$type.card.txt > ${signalName}/2los_SR_bins_notriggers_${signal}_comb.card.txt


### 2lOS without CR + 3l
#combineCards.py SR_MET125=${signalName}/2los_SR_bins_notriggers_${signal}_met125_mm$type.card.txt SR_MET200=${signalName}/2los_SR_bins_notriggers_${signal}_met200$type.card.txt SR_MET300=${signalName}/2los_SR_bins_notriggers_${signal}_met300$type.card.txt SR_MET75_3lLow=${signalName}/3l_SR_bins_notriggers_${signal}_met75_lowPt3l$type.card.txt SR_MET75_3lHigh=${signalName}/3l_SR_bins_notriggers_${signal}_met75_highPt3l$type.card.txt SR_MET125_3lLow=${signalName}/3l_SR_bins_notriggers_${signal}_met125_lowPt3l$type.card.txt SR_MET125_3lHigh=${signalName}/3l_SR_bins_notriggers_${signal}_met125_highPt3l$type.card.txt SR_MET200_3l=${signalName}/3l_SR_bins_notriggers_${signal}_met200$type.card.txt > ${signalName}/2los_SR_bins_notriggers_${signal}_comb.card.txt


### 2lOS with CR + 3l
#combineCards.py SR_MET125=${signalName}/2los_SR_bins_notriggers_${signal}_met125_mm$type.card.txt SR_MET200=${signalName}/2los_SR_bins_notriggers_${signal}_met200$type.card.txt SR_MET300=${signalName}/2los_SR_bins_notriggers_${signal}_met300$type.card.txt DYCR_MET125=${signalName}/2los_CR_DY_vars_data_${signal}_met125$type.card.txt DYCR_MET200=${signalName}/2los_CR_DY_vars_data_${signal}_met200$type.card.txt TTCR_MET125=${signalName}/2los_CR_TT_vars_dataMET_${signal}_met125$type.card.txt  TTCR_MET200=${signalName}/2los_CR_TT_vars_dataMET_${signal}_met200$type.card.txt SSCR_MET200=${signalName}/2los_CR_SS_bins_notriggers_${signal}_met200$type.card.txt SR_MET75_3lLow=${signalName}/3l_SR_bins_notriggers_${signal}_met75_lowPt3l$type.card.txt SR_MET75_3lHigh=${signalName}/3l_SR_bins_notriggers_${signal}_met75_highPt3l$type.card.txt SR_MET125_3lLow=${signalName}/3l_SR_bins_notriggers_${signal}_met125_lowPt3l$type.card.txt SR_MET125_3lHigh=${signalName}/3l_SR_bins_notriggers_${signal}_met125_highPt3l$type.card.txt SR_MET200_3l=${signalName}/3l_SR_bins_notriggers_${signal}_met200$type.card.txt > ${signalName}/2los_SR_bins_notriggers_${signal}_comb.card.txt


#echo "Linking the associated root file.."
text2workspace.py ${signalName}/2los_SR_bins_notriggers_${signal}_comb.card.txt 



## -- checking the cards 
#echo "Checking the nuisance in the cards and printing on http://castello.web.cern.ch/castello/susy-sos/ichep/approval/limits/ "
#python ~/WorkArea/physics/limits/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/systematicsAnalyzer.py TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_comb.card.txt --all -m 125 -f html > $WWWDIR/test_all_benchmarks/2los_SR_bins_notriggers_ewk20_comb.card.html
#python ~/WorkArea/physics/limits/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/systematicsAnalyzer.py T2ttDeg_330/2los_SR_bins_notriggers_${signal}_comb.card.txt --all -m 125 -f html > $WWWDIR/test_all_benchmarks/2los_SR_bins_notriggers_${signal}_comb.card.html

#echo "Running on combined datacards..."
if [ $type != "_unblind" ]  
then
    echo " Running BLINDED..."
    echo "== Asymptotic"
    combine -M Asymptotic --run=blind -t -1 --datacard=${signalName}/2los_SR_bins_notriggers_${signal}_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_${signal}_combined.txt 

    
#    echo "== Likelihood"
#    combine -M MaxLikelihoodFit --setPhysicsModelParameterRanges r=-0,10 --setPhysicsModelParameters r=1  --customStartingPoint TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_comb.card.root
# python diffNuisances.py mlfit.root -g diffnuisances.root   
 #   combine -M Asymptotic --run=blind -t -1 --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_ewk10_combined.txt
 #   combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_stop20_combined.txt
 #   combine -M Asymptotic --run=blind -t -1 --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_stop35_combined.txt
else
    echo " Running UNBLINDED..."
    echo "== Asymptotic"
#    ##cd $asymptotic_dir

    combine -M Asymptotic --datacard=${signalName}/2los_SR_bins_notriggers_${signal}_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_${signal}_combined.txt

#    echo "== Likelihood"
#    combine -M MaxLikelihoodFit --setPhysicsModelParameterRanges r=-5,5 --setPhysicsModelParameters r=1 --customStartingPoint TChiNeuWZ_80/2los_SR_bins_notriggers_ewk20_comb.card.root -v 3 
#    python /afs/cern.ch/work/c/castello/physics/limits/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py mlfit.root -g diffnuisances.root

#   combine -M Asymptotic --datacard=TChiNeuWZ_90/2los_SR_bins_notriggers_ewk10_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_ewk10_combined.txt
#   combine -M Asymptotic --datacard=T2ttDeg_330/2los_SR_bins_notriggers_stop20_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_stop20_combined.txt
#   combine -M Asymptotic --datacard=T2ttDeg_315/2los_SR_bins_notriggers_stop35_comb.card.txt > $WWWDIR/$DIR/Asymp_2los_SR_bins_notriggers_stop35_combined.txt
fi

eval `scramv1 runtime -sh`
echo "I'm done. Bye."