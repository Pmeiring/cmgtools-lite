
## flags (queue, select samples, etc.)
##F="--direct --nosplit -q all.q"
F="-q workday --direct --nosplit"
##F="--direct --finalize"
#="--direct --nosplit"
#F="-F --direct --nosplit -q all.q --accept WZTo --exclude amcatnlo --exclude ext"
#F="-F --direct --nosplit -q all.q --accept TChiWZ_200_100 --accept TChiWZ_350_250"
#F="--nosplit --direct -q all.q --accept TChiWZ --accept TChiWH --accept TChiHH --accept TChiHZ --accept TChiZZ4L"


## tree directory
##T="/afs/cern.ch/user/v/vtavolar/SusySOS/cleanTest/CMSSW_8_0_25/src/CMGTools/TTHAnalysis/python/plotter/data1/botta/trees_SOS_010217"
##T="/eos/user/v/vtavolar/SusySOS/trees_SOS_010217/"
T="/afs/cern.ch/user/p/peruzzi/work/sostrees/trees_SOS_010217/"

##lib for module import
I="CMGTools.TTHAnalysis.tools.susySosReCleaner"

## output directory
O=$PWD

echo $O

## setups
python susy-interface/friendmaker.py sos2l16 2losEwkLow16 $T $O --bk --pretend --log $F --modules "both3dloose;ipjets" 
#python susy-interface/friendmaker.py sos2l16 2losEwkLow16 $T $O --bk -I $I --log $F --modules "both3dloose;ipjets" --accept "MET_Run2016H-PromptReco-v2_runs_281207_284035;T_tch_powheg;TTJets_DiLepton_ext;TTJets_DiLepton;tZq_ll_ext"


