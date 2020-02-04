#!/bin/bash

echo Will run mcPlots.py for the 2l and/or 3l case, using mN2=100GeV and/or mN2=200GeV

pwd=$PWD
TTHpath=/afs/cern.ch/work/p/pmeiring/private/CMS/CMSSW_10_4_0/src/CMGTools/TTHAnalysis
CERNboxpath=/eos/user/p/pmeiring/www/SUSY_SOS/GenLep_TChiWZ_categorization/RemoveMe/CutFlow/
PSIWorkpath=/work/pmeiring/PlayGroundAuto
Samplepath=/eos/cms/store/user/pmeiring

cuts_2l=susy-sos/2los_cuts_PETER.txt
cuts_2l_ee=susy-sos/2los_ee_cuts_PETER.txt
cuts_2l_mm=susy-sos/2los_mm_cuts_PETER.txt

cuts_3l=susy-sos/3l_cuts_PETER.txt
cuts_3l_ee=susy-sos/3l_ee_cuts_PETER.txt
cuts_3l_mm=susy-sos/3l_mm_cuts_PETER.txt

mca_mN2_100GeV=susy-sos/mca-includes/2018/mca-2los-signal_PETER_mN2_100GeV.txt
mca_mN2_200GeV=susy-sos/mca-includes/2018/mca-2los-signal_PETER_mN2_200GeV.txt

mca_mN2_100GeV_xsec=susy-sos/mca-includes/2018/mca-2los-signal_PETER_mN2_100GeV_xsec.txt
mca_mN2_200GeV_xsec=susy-sos/mca-includes/2018/mca-2los-signal_PETER_mN2_200GeV_xsec.txt

# insert folder inside CERNbox, mca, cuts, plots
Run_mcPlots() {
	echo -e "\n...\nUsing input from\n$2\n$3\n$4\n..."
	rm -rf $CERNboxpath/"$1"
	
	python mcPlots.py 	--pdir $CERNboxpath/"$1" \
						--Fs $Samplepath/NanoTrees_SOS_291019_NoSkimNoTrigger/2018/genlep_SMS_TChiWZ/ \
						--Fs $Samplepath/NanoTrees_SOS_291019_NoSkimNoTrigger/2018/recleaner/ \
						"$2" "$3" "$4" \
						-P $Samplepath/NanoTrees_SOS_291019_NoSkimNoTrigger/2018/ \
						-j 8 --year 2018 -l 137.1 --tree NanoAOD --s2v --noCms --lspam '#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}' --rspam '137.1 fb^{-1} [13 TeV]' \
						--xp data --xp prompt_tt --xp prompt_dy --xp prompt_vv --xp Fakes_Wj --xp Fakes_tt --xp Fakes_t --xp Fakes_vv --xp Rares --xp Convs \
						--legendWidth 0.52 --legendFontSize 0.042 --plotmode nostack -L susy-sos/functionsSOS.cc ;
}



	#	2l 100GeV 
# cd $TTHpath/python/plotter
# Run_mcPlots N2_100GeV_2L "$mca_mN2_100GeV" "$cuts_2l" susy-sos/2los_plots_PETER.txt
# Run_mcPlots N2_100GeV_2L_ee "$mca_mN2_100GeV" "$cuts_2l_ee" susy-sos/2los_plots_PETER.txt
# Run_mcPlots N2_100GeV_2L_mumu "$mca_mN2_100GeV" "$cuts_2l_mm" susy-sos/2los_plots_PETER.txt
# cd $pwd
# python DetermineCutFlow.py $CERNboxpath/N2_100GeV_2L $TTHpath/python/plotter/$cuts_2l 
# python DetermineCutFlow.py $CERNboxpath/N2_100GeV_2L_ee $TTHpath/python/plotter/$cuts_2l_ee 
# python DetermineCutFlow.py $CERNboxpath/N2_100GeV_2L_mumu $TTHpath/python/plotter/$cuts_2l_mm 
# python MergeCutFlow_eemm.py $CERNboxpath/N2_100GeV_2L_ee $CERNboxpath/N2_100GeV_2L_mumu


	#	2l 200GeV
# cd $TTHpath/python/plotter
# Run_mcPlots N2_200GeV_2L "$mca_mN2_200GeV" "$cuts_2l" susy-sos/2los_plots_PETER.txt
# Run_mcPlots N2_200GeV_2L_ee "$mca_mN2_200GeV" "$cuts_2l_ee" susy-sos/2los_plots_PETER.txt
# Run_mcPlots N2_200GeV_2L_mumu "$mca_mN2_200GeV" "$cuts_2l_mm" susy-sos/2los_plots_PETER.txt
# cd $pwd
# python DetermineCutFlow.py $CERNboxpath/N2_200GeV_2L $TTHpath/python/plotter/$cuts_2l 
# python DetermineCutFlow.py $CERNboxpath/N2_200GeV_2L_ee $TTHpath/python/plotter/$cuts_2l_ee 
# python DetermineCutFlow.py $CERNboxpath/N2_200GeV_2L_mumu $TTHpath/python/plotter/$cuts_2l_mm 
# python MergeCutFlow_eemm.py $CERNboxpath/N2_200GeV_2L_ee $CERNboxpath/N2_200GeV_2L_mumu


	#	2l 100GeV with correct xsec
cd $TTHpath/python/plotter
Run_mcPlots N2_100GeV_2L_xsec "$mca_mN2_100GeV_xsec" "$cuts_2l" susy-sos/2los_plots_PETER.txt
# # Run_mcPlots N2_100GeV_2L_ee_xsec "$mca_mN2_100GeV_xsec" "$cuts_2l_ee" susy-sos/2los_plots_PETER.txt
# # Run_mcPlots N2_100GeV_2L_mumu_xsec "$mca_mN2_100GeV_xsec" "$cuts_2l_mm" susy-sos/2los_plots_PETER.txt
cd $pwd
python DetermineCutFlow_withStatError.py $CERNboxpath/N2_100GeV_2L_xsec $TTHpath/python/plotter/$cuts_2l
# python DetermineCutFlow_withStatError.py $CERNboxpath/N2_100GeV_2L_ee_xsec $TTHpath/python/plotter/$cuts_2l_ee 
# python DetermineCutFlow_withStatError.py $CERNboxpath/N2_100GeV_2L_mumu_xsec $TTHpath/python/plotter/$cuts_2l_mm
# python MergeCutFlow_eemm.py $CERNboxpath/N2_100GeV_2L_ee_xsec $CERNboxpath/N2_100GeV_2L_mumu_xsec





	#	2l 200GeV with correct xsec
# cd $TTHpath/python/plotter
# Run_mcPlots N2_200GeV_2L_xsec "$mca_mN2_200GeV_xsec" "$cuts_2l" susy-sos/2los_plots_PETER.txt
# Run_mcPlots N2_200GeV_2L_ee_xsec "$mca_mN2_200GeV_xsec" "$cuts_2l_ee" susy-sos/2los_plots_PETER.txt
# Run_mcPlots N2_200GeV_2L_mumu_xsec "$mca_mN2_200GeV_xsec" "$cuts_2l_mm" susy-sos/2los_plots_PETER.txt
cd $pwd
# python DetermineCutFlow_withStatError.py $CERNboxpath/N2_200GeV_2L_xsec $TTHpath/python/plotter/$cuts_2l 
# python DetermineCutFlow_withStatError.py $CERNboxpath/N2_200GeV_2L_ee_xsec $TTHpath/python/plotter/$cuts_2l_ee 
# python DetermineCutFlow_withStatError.py $CERNboxpath/N2_200GeV_2L_mumu_xsec $TTHpath/python/plotter/$cuts_2l_mm 
# python MergeCutFlow_eemm.py $CERNboxpath/N2_200GeV_2L_ee_xsec $CERNboxpath/N2_200GeV_2L_mumu_xsec




#	2l 100GeV with correct xsec
cd $pwd
# root -l -b "PlotCutflow.C(\"$CERNboxpath/N2_100GeV_2L_ee_xsec\", \"CutFlow m_{N2}=100GeV, ee\")"
# root -l -b "PlotCutflow.C(\"$CERNboxpath/N2_100GeV_2L_mumu_xsec\", \"CutFlow m_{N2}=100GeV, mumu\")"
root -l -b "PlotCutflow.C(\"$CERNboxpath/N2_100GeV_2L_xsec\", \"CutFlow m_{N2}=100GeV, 2l (ee,mumu)\")"

#	2l 200GeV with correct xsec
cd $pwd
# root -l -b "PlotCutflow.C(\"$CERNboxpath/N2_200GeV_2L_ee_xsec\", \"CutFlow m_{N2}=200GeV, ee\")"
# root -l -b "PlotCutflow.C(\"$CERNboxpath/N2_200GeV_2L_mumu_xsec\", \"CutFlow m_{N2}=200GeV, mumu\")"
# root -l -b "PlotCutflow.C(\"$CERNboxpath/N2_200GeV_2L_xsec\", \"CutFlow m_{N2}=200GeV, 2l (ee,mumu)\")"
