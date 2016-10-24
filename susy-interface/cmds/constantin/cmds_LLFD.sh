#!/bin/bash
# syntax: python susy-scanmaker/run.py config model outdir [options]

python susy-scanmaker/run.py crwz TChiNeuSlepSneu_FD /mnt/t3nfs01/data01/shome/cheidegg/o/2016-08-01_ewk80X_scan12p9final_full  --s2v --tree treeProducerSusyMultilepton -P /mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X -F sf/t {P}/leptonJetReCleanerSusyEWK2L/evVarFriend_{cname}.root -F sf/t {P}/leptonBuilderEWK/evVarFriend_{cname}.root -F sf/t {P}/eventBTagWeight/evVarFriend_{cname}.root --mcc susy-ewkino/crwz/lepchoice-crwz-FO.txt --mcc susy-ewkino/mcc_triggerdefs.txt -f -j 4 -L susy-ewkino/3l/functionsEWK.cc -L FastSimleptonSF.cc --plotgroup fakes_appldata+=promptsub --plotgroup fakes_appldata_ewk_Up+=promptsub_ewk_Up --plotgroup fakes_appldata_ewk_Dn+=promptsub_ewk_Dn --ignore promptsub --ignore promptsub_ewk_Up --ignore promptsub_ewk_Dn --neglist promptsub --neglist promptsub_ewk_Up --neglist promptsub_ewk_Dn -W 'puw2016_nInt_12p9fb(nTrueInt)*triggerSF(3,LepGood_pt[0], LepGood_pdgId[0], LepGood_pt[1], LepGood_pdgId[1], LepGood_pt[2], LepGood_pdgId[2])*leptonSF_2lss_ewk(LepGood1_pdgId,LepGood1_conePt,LepGood1_eta)*leptonSF_2lss_ewk(LepGood2_pdgId,LepGood2_conePt,LepGood2_eta)*leptonSF_2lss_ewk(LepGood3_pdgId,LepGood3_conePt,LepGood3_eta)*eventBTagSF' --WFS '(leptonSF_2lss_ewk_FS(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,0)*leptonSF_2lss_ewk_FS(LepGood2_pdgId,LepGood2_pt,LepGood2_eta,0))' -l 12.9 --q2acc '' --noNegVar --hardZero --sigOnly -q all.q
python susy-scanmaker/run.py 3l TChiNeuSlepSneu_FD /mnt/t3nfs01/data01/shome/cheidegg/o/2016-08-01_ewk80X_scan12p9final_full  --s2v --tree treeProducerSusyMultilepton -P /mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X -F sf/t {P}/leptonJetReCleanerSusyEWK3L/evVarFriend_{cname}.root -F sf/t {P}/leptonBuilderEWK/evVarFriend_{cname}.root -F sf/t {P}/eventBTagWeight/evVarFriend_{cname}.root --mcc susy-ewkino/3l/mcc_ewkino.txt -f -j 4 -L susy-ewkino/3l/functionsEWK.cc --plotgroup fakes_appldata+=promptsub --plotgroup fakes_appldata_ewk_Up+=promptsub_ewk_Up --plotgroup fakes_appldata_ewk_Dn+=promptsub_ewk_Dn --ignore promptsub --ignore promptsub_ewk_Up --ignore promptsub_ewk_Dn --neglist promptsub --neglist promptsub_ewk_Up --neglist promptsub_ewk_Dn -X blinding -W 'puw2016_nInt_12p9fb(nTrueInt)*triggerSF(BR, LepSel_pt[0], LepSel_pdgId[0], LepSel_pt[1], LepSel_pdgId[1], LepSel_pt[2], LepSel_pdgId[2])*eventBTagSF*leptonSF(getLeptonSF(LepSel_pt[0], LepSel_eta[0], LepSel_pdgId[0]), getLeptonSF(LepSel_pt[1], LepSel_eta[1], LepSel_pdgId[1]), getLeptonSF(LepSel_pt[2], LepSel_eta[2], LepSel_pdgId[2]))' --WFS 'leptonSFFS(getLeptonSFFS(LepSel_pt[0], LepSel_eta[0], LepSel_pdgId[0]), getLeptonSFFS(LepSel_pt[1], LepSel_eta[1], LepSel_pdgId[1]), getLeptonSFFS(LepSel_pt[2], LepSel_eta[2], LepSel_pdgId[2]))' -l 12.9 --bins "12,0.5,12.5" --out 3lA1 --noNegVar --hardZero -q all.q --sigOnly
python susy-scanmaker/run.py 3l TChiNeuSlepSneu_FD /mnt/t3nfs01/data01/shome/cheidegg/o/2016-08-01_ewk80X_scan12p9final_full  --s2v --tree treeProducerSusyMultilepton -P /mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X -F sf/t {P}/leptonJetReCleanerSusyEWK3L/evVarFriend_{cname}.root -F sf/t {P}/leptonBuilderEWK/evVarFriend_{cname}.root -F sf/t {P}/eventBTagWeight/evVarFriend_{cname}.root --mcc susy-ewkino/3l/mcc_ewkino.txt -f -j 4 -L susy-ewkino/3l/functionsEWK.cc --plotgroup fakes_appldata+=promptsub --plotgroup fakes_appldata_ewk_Up+=promptsub_ewk_Up --plotgroup fakes_appldata_ewk_Dn+=promptsub_ewk_Dn --ignore promptsub --ignore promptsub_ewk_Up --ignore promptsub_ewk_Dn --neglist promptsub --neglist promptsub_ewk_Up --neglist promptsub_ewk_Dn -X blinding -W 'puw2016_nInt_12p9fb(nTrueInt)*triggerSF(BR, LepSel_pt[0], LepSel_pdgId[0], LepSel_pt[1], LepSel_pdgId[1], LepSel_pt[2], LepSel_pdgId[2])*eventBTagSF*leptonSF(getLeptonSF(LepSel_pt[0], LepSel_eta[0], LepSel_pdgId[0]), getLeptonSF(LepSel_pt[1], LepSel_eta[1], LepSel_pdgId[1]), getLeptonSF(LepSel_pt[2], LepSel_eta[2], LepSel_pdgId[2]))' --WFS 'leptonSFFS(getLeptonSFFS(LepSel_pt[0], LepSel_eta[0], LepSel_pdgId[0]), getLeptonSFFS(LepSel_pt[1], LepSel_eta[1], LepSel_pdgId[1]), getLeptonSFFS(LepSel_pt[2], LepSel_eta[2], LepSel_pdgId[2]))' -l 12.9 --out 3lA2 --expr "SR-13" --bins "23,0.5,23.5" --noNegVar --hardZero -q all.q --sigOnly