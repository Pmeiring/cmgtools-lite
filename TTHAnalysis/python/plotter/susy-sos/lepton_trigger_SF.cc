#include <cmath>
#include <assert.h>
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "Math/GenVector/PxPyPzM4D.h"
#include "Math/GenVector/Boost.h"
#include "TLorentzVector.h"
#include "TGraphAsymmErrors.h"
#include "TH2F.h"
#include "TFile.h"

TFile *_file_recoToLoose_leptonSF_mu_sos_barrel = NULL;
TGraphAsymmErrors *_histo_recoToLoose_leptonSF_mu_sos_barrel = NULL;
TFile *_file_recoToLoose_leptonSF_mu_sos_endcap = NULL;
TGraphAsymmErrors *_histo_recoToLoose_leptonSF_mu_sos_endcap = NULL;

TFile *_file_recoToLoose_leptonSF_mu_sos_all_highpt = NULL;
//TGraphAsymmErrors *_histo_recoToLoose_leptonSF_mu_sos_barrel_highpt = NULL;
TH1F *_histo_recoToLoose_leptonSF_mu_sos_all_highpt = NULL;

TFile *_file_recoToLoose_leptonSF_mu_sos_endcap_highpt = NULL;
//TGraphAsymmErrors *_histo_recoToLoose_leptonSF_mu_sos_endcap_highpt = NULL;


//float deltaPhi(float phi1, float phi2) {
//  float result = phi1 - phi2;
//  while (result > float(M_PI)) result -= float(2*M_PI);
//  while (result <= -float(M_PI)) result += float(2*M_PI);
//  return result;
//}

int get_bin_recoToLoose(float pt){
  if(pt> 3.0 && pt<=3.5) return 0;
  else if(pt>3.5  && pt<=4.0) return 1;
  else if(pt>4.0  && pt<=4.5) return 2;
  else if(pt>4.5  && pt<=5.0) return 3;
  else if(pt>5.0  && pt<=6.0) return 4;
  else if(pt>6.0  && pt<=7.0) return 5;
  else if(pt>7.0  && pt<=8.0) return 6;
  else if(pt> 8.0 && pt<=10.0) return 7;
  else if(pt> 10.0 && pt<=12.0) return 8;
  else if(pt> 12.0 && pt<=18.0) return 9;
  else if(pt>18.) return 10;
  else {
    //cout << "Error in get_bin_recoToLoose" << endl;
    assert(0);
  }
}

int get_bin_looseToTight_mu(float pt){
  if(pt> 3.5 && pt<=7.5) return 0;
  else if(pt>7.5  && pt<=10.0) return 1;
  else if(pt>10.0  && pt<=15.0) return 2;
  else if(pt>15.0  && pt<=20.0) return 3;
  else if(pt>20.0) return 4;
  else {
    //cout << "Error in get_bin_looseToTight_mu" << endl;
    assert(0);
  }
}

int get_bin_looseToTight_el(float pt){
  if(pt> 5.0 && pt<=12.5) return 0;
  else if(pt>12.5  && pt<=16.0) return 1;
  else if(pt>16.0  && pt<=20.0) return 2;
  else if(pt>20.0  && pt<=25.0) return 3;
  else if(pt>25.0) return 4;
  else {
    //cout << "Error in get_bin_looseToTight_el" << endl;
    assert(0);
  }
}


float _get_recoToLoose_leptonSF_SOS(int pdgid, float _pt, float eta, float var){
  
  float pt = std::min(float(199.9),_pt);

  if (abs(pdgid)!=13) return 1.0; // not needed for electrons

  if (!_histo_recoToLoose_leptonSF_mu_sos_barrel) {
    _file_recoToLoose_leptonSF_mu_sos_barrel = new TFile("../../data/sos_lepton_SF/mu_JDGauss_bern3_Loose_barrel_7invfb.root","read");//RECOtoLOOSE -low pT
    _histo_recoToLoose_leptonSF_mu_sos_barrel = ( TGraphAsymmErrors*)(_file_recoToLoose_leptonSF_mu_sos_barrel->Get("mu_JDGauss_bern3_Loose_barrel_ratio"));
  }
  
  if (!_histo_recoToLoose_leptonSF_mu_sos_endcap) {
    _file_recoToLoose_leptonSF_mu_sos_endcap = new TFile("../../data/sos_lepton_SF/mu_JDGauss_bern3_Loose_endcap_7invfb.root","read");//RECOtoLOOSE -low pT
    _histo_recoToLoose_leptonSF_mu_sos_endcap = ( TGraphAsymmErrors*)(_file_recoToLoose_leptonSF_mu_sos_endcap->Get("mu_JDGauss_bern3_Loose_endcap_ratio"));
  }

  if (!_histo_recoToLoose_leptonSF_mu_sos_all_highpt) {
    _file_recoToLoose_leptonSF_mu_sos_all_highpt = new TFile("../../data/sos_lepton_SF/MuonID_Z_RunBCD_prompt80X_7p65.root","read");
    _histo_recoToLoose_leptonSF_mu_sos_all_highpt = ( TH1F*)(_file_recoToLoose_leptonSF_mu_sos_all_highpt->Get("MC_NUM_LooseID_DEN_genTracks_PAR_pt_alleta_bin1/pt_ratio"));
  }
 
  TGraphAsymmErrors *hist_barrel = _histo_recoToLoose_leptonSF_mu_sos_barrel;
  TGraphAsymmErrors *hist_endcap = _histo_recoToLoose_leptonSF_mu_sos_endcap;
  TH1F *hist_all_highpt = _histo_recoToLoose_leptonSF_mu_sos_all_highpt;

  if (pt<25){
    if(abs(eta)<1.2){
      if(var>0) return (hist_barrel->Eval(pt)+hist_barrel->GetErrorYhigh(get_bin_recoToLoose(pt)));
      if(var<0) return (hist_barrel->Eval(pt)-hist_barrel->GetErrorYlow(get_bin_recoToLoose(pt)));
      return  hist_barrel->Eval(pt);
     
    }
    else {
      if(var>0) return (hist_endcap->Eval(pt)+hist_endcap->GetErrorYhigh(get_bin_recoToLoose(pt)));
      if(var<0) return (hist_endcap->Eval(pt)-hist_endcap->GetErrorYlow(get_bin_recoToLoose(pt)));
      return hist_endcap->Eval(pt);
    }
  }
  else{
    Int_t binx = (hist_all_highpt->GetXaxis())->FindBin(pt);
    if(var>0) return (hist_all_highpt->GetBinContent(binx) + 0.01);
    if(var<0) return (hist_all_highpt->GetBinContent(binx) - 0.01);
    return  hist_all_highpt->GetBinContent(binx);
  }

  assert(0);
  return -999;

}

TFile *_file_looseToTight_leptonSF_mu_sos_barrel = NULL;
TGraphAsymmErrors *_histo_looseToTight_leptonSF_mu_sos_barrel = NULL;
TFile *_file_looseToTight_leptonSF_mu_sos_endcap = NULL;
TGraphAsymmErrors *_histo_looseToTight_leptonSF_mu_sos_endcap = NULL;

TFile *_file_looseToTight_leptonSF_el_sos_barrel = NULL;
TGraphAsymmErrors *_histo_looseToTight_leptonSF_el_sos_barrel = NULL;
TFile *_file_looseToTight_leptonSF_el_sos_endcap = NULL;
TGraphAsymmErrors *_histo_looseToTight_leptonSF_el_sos_endcap = NULL;



float _get_looseToTight_leptonSF_SOS(int pdgid, float _pt, float eta, float var){

 
  if (!_histo_looseToTight_leptonSF_mu_sos_barrel) {
    _file_looseToTight_leptonSF_mu_sos_barrel = new TFile("../../data/sos_lepton_SF/mu_SOS_comb_barrel_36invfb.root","read");
    _histo_looseToTight_leptonSF_mu_sos_barrel = (TGraphAsymmErrors*)(_file_looseToTight_leptonSF_mu_sos_barrel->Get("ratio"));
  }
  if (!_histo_looseToTight_leptonSF_mu_sos_endcap) {
    _file_looseToTight_leptonSF_mu_sos_endcap = new TFile("../../data/sos_lepton_SF/mu_SOS_comb_endcap_36invfb.root","read");
    _histo_looseToTight_leptonSF_mu_sos_endcap = (TGraphAsymmErrors*)(_file_looseToTight_leptonSF_mu_sos_endcap->Get("ratio"));
  }
  
  if (!_histo_looseToTight_leptonSF_el_sos_barrel) {
    _file_looseToTight_leptonSF_el_sos_barrel = new TFile("../../data/sos_lepton_SF/el_SOS_barrel_36invfb.root","read");
    _histo_looseToTight_leptonSF_el_sos_barrel = (TGraphAsymmErrors*)(_file_looseToTight_leptonSF_el_sos_barrel->Get("ratio"));
  }
  if (!_histo_looseToTight_leptonSF_el_sos_endcap) {
    _file_looseToTight_leptonSF_el_sos_endcap = new TFile("../../data/sos_lepton_SF/el_SOS_endcap_36invfb.root","read");
    _histo_looseToTight_leptonSF_el_sos_endcap = (TGraphAsymmErrors*)(_file_looseToTight_leptonSF_el_sos_endcap->Get("ratio"));
  }

  if (abs(pdgid)==13){
    float pt= std::min(float(119.9),_pt); //protection
    TGraphAsymmErrors *hist_mu_barrel = _histo_looseToTight_leptonSF_mu_sos_barrel;
    TGraphAsymmErrors *hist_mu_endcap = _histo_looseToTight_leptonSF_mu_sos_endcap;
    
    if(abs(eta)<1.2){
      if(var>0) return (hist_mu_barrel->Eval(pt) + hist_mu_barrel->GetErrorYhigh(get_bin_looseToTight_mu(pt))) ;
      if(var<0) return (hist_mu_barrel->Eval(pt) - hist_mu_barrel->GetErrorYlow(get_bin_looseToTight_mu(pt))) ;
      return hist_mu_barrel->Eval(pt);
    }
    if(abs(eta)>1.2){
      if(var>0) return (hist_mu_endcap->Eval(pt) + hist_mu_endcap->GetErrorYhigh(get_bin_looseToTight_mu(pt))) ;
      if(var<0) return (hist_mu_endcap->Eval(pt) - hist_mu_endcap->GetErrorYlow(get_bin_looseToTight_mu(pt))) ;
      return hist_mu_endcap->Eval(pt);
    }
  }
 
  if(abs(pdgid)==11){
    float pt= std::min(float(30.0),_pt); //protection
    TGraphAsymmErrors *hist_el_barrel = _histo_looseToTight_leptonSF_el_sos_barrel;
    TGraphAsymmErrors *hist_el_endcap = _histo_looseToTight_leptonSF_el_sos_endcap;
    
    if(abs(eta)<1.479){
      if(var>0) return (hist_el_barrel->Eval(pt) + hist_el_barrel->GetErrorYhigh(get_bin_looseToTight_el(pt))) ;
      if(var<0) return (hist_el_barrel->Eval(pt) - hist_el_barrel->GetErrorYlow(get_bin_looseToTight_el(pt))) ;
      return  hist_el_barrel->Eval(pt);
    }
    if(abs(eta)>1.479){
      if(var>0) return (hist_el_endcap->Eval(pt) + hist_el_endcap->GetErrorYhigh(get_bin_looseToTight_el(pt))) ;
      if(var<0) return (hist_el_endcap->Eval(pt) - hist_el_endcap->GetErrorYlow(get_bin_looseToTight_el(pt))) ;
      return hist_el_endcap->Eval(pt);
    }
  }
  
  assert(0);
  return -999;
}

// ---- Tracking (hard-coded so far)  ---------------------------

TH2F  *_histo_reco_ele_sf = NULL;
TFile *_file_trackingSF = NULL;

float _get_tracking_SF(int pdgid, float pt, float eta, float var){

 if (var!=0) assert(0); // NOT IMPLEMENTED

 if (abs(pdgid)==11){
   //// ---- electrons
   if (!_file_trackingSF){
     _file_trackingSF  = new TFile("../../data/sos_lepton_SF/egammaReco_eff_36invfb.root","read");
     _histo_reco_ele_sf = (TH2F*)(_file_trackingSF->Get("EGamma_SF2D"));
   }

   return 1.0;
   // --- commented due to a bug in the original Egamma file
   // return _histo_reco_ele_sf->GetBinContent(((_histo_reco_ele_sf->GetXaxis())->FindBin(eta)),((_histo_reco_ele_sf->GetYaxis())->FindBin(pt_min)));
 }
 else{
   // Tracking efficiency for muons is 1. according to MuonPOG
   // ---  muons, from: http://ebrondol.web.cern.ch/ebrondol/TrackingTnP_Zmumu/80_20/all2016Runs_vs_/tk0_dr030e030/ and http://ebrondol.web.cern.ch/ebrondol/TrackingTnP_Zmumu/80_20/all2016Runs_vs_/
   return 1.0;
 }
 
}

// ------------------------------------------

float leptonSF_SOS(int pdgid, float pt, float eta, float var=0){

  // For e + mu
  float tracking = _get_tracking_SF(pdgid,pt,eta,var);
  // For mu
  float recoToLoose = _get_recoToLoose_leptonSF_SOS(pdgid,pt,eta,var);
  // For e + mu
  float looseToTight = _get_looseToTight_leptonSF_SOS(pdgid,pt,eta,var);

  float res = tracking*recoToLoose*looseToTight; 

  assert (res>0 && "*** Warning we have a negative (or zero) Lepton SF ***");
  return res;
}

// Trigger ---------------------------

TFile *_file_triggerSF = NULL;

TH2F  *_histo_l1_data_DoubleMu_MET = NULL;
TH2F  *_histo_l2_data_DoubleMu_MET = NULL;
TH2F  *_histo_l3_data_DoubleMu_MET = NULL;
TH2F  *_histo_l1_mc_DoubleMu_MET = NULL;
TH2F  *_histo_l2_mc_DoubleMu_MET = NULL;
TH2F  *_histo_l3_mc_DoubleMu_MET = NULL;
TH2F  *_histo_met_num_data = NULL;
TH2F  *_histo_met_denom_data = NULL;
TH2F  *_histo_met_num_mc = NULL;
TH2F  *_histo_met_denom_mc = NULL;
TH2F *_histo_l2_data_TripleMu_12_10_5= NULL;
TH2F *_histo_l3_data_TripleMu_5_3_3= NULL;
TH2F *_histo_l2_mc_TripleMu_12_10_5= NULL;
TH2F *_histo_l3_mc_TripleMu_5_3_3= NULL;

void init_triggerSF_SOS(){
    _file_triggerSF  = new TFile("../../data/sos_lepton_SF/triggerSF_36invfb.root","read");
    _histo_l1_data_DoubleMu_MET = (TH2F*)(_file_triggerSF->Get("hist2dnum_L1Mu__HLT_DoubleMu3_PFMET50pt"));
    _histo_l2_data_DoubleMu_MET = (TH2F*)(_file_triggerSF->Get("hist2dnum_L2Mu__HLT_DoubleMu3_PFMET50pt"));
    _histo_l3_data_DoubleMu_MET = (TH2F*)(_file_triggerSF->Get("hist2dnum_L3Mu__HLT_DoubleMu3_PFMET50pt"));
    _histo_l2_data_TripleMu_12_10_5 = (TH2F*)(_file_triggerSF->Get("hist2dnum_HLT_Mu5__HLT_TripleMu_12_10_5pt"));
    _histo_l3_data_TripleMu_5_3_3 = (TH2F*)(_file_triggerSF->Get("hist2dnum_HLT_Mu3__HLT_TripleMu_5_3_3pt"));
    _histo_met_num_data = (TH2F*)(_file_triggerSF->Get("hnummet"));
    _histo_met_denom_data = (TH2F*)(_file_triggerSF->Get("hdenmet"));
    _histo_met_num_mc = (TH2F*)(_file_triggerSF->Get("hnummet_mc"));
    _histo_met_denom_mc = (TH2F*)(_file_triggerSF->Get("hdenmet_mc"));
    _histo_l1_mc_DoubleMu_MET = (TH2F*)(_file_triggerSF->Get("hist2dnum_MC_L1Mu__HLT_DoubleMu3_PFMET50pt"));
    _histo_l2_mc_DoubleMu_MET = (TH2F*)(_file_triggerSF->Get("hist2dnum_MC_L2Mu__HLT_DoubleMu3_PFMET50pt"));
    _histo_l3_mc_DoubleMu_MET = (TH2F*)(_file_triggerSF->Get("hist2dnum_MC_L3Mu__HLT_DoubleMu3_PFMET50pt"));
    _histo_l2_mc_TripleMu_12_10_5= (TH2F*)(_file_triggerSF->Get("hist2dnum_MC_HLT_Mu5__HLT_TripleMu_12_10_5pt"));
    _histo_l3_mc_TripleMu_5_3_3= (TH2F*)(_file_triggerSF->Get("hist2dnum_MC_HLT_Mu3__HLT_TripleMu_5_3_3pt"));
  }   




int lepton_permut(int pdgid1, int pdgid2 ,int  pdgid3)
{
  if ((abs(pdgid1)==13 && (abs(pdgid2)) == 13) && (abs(pdgid3)!=13)){
    return 12 ; // if lep1 = muon and lep2 = muon and lep3 = not muon
  }
  else  if ((abs(pdgid2)== 13 && abs(pdgid3) == 13) && (abs(pdgid1)!=13)){
    return 23; // if lep3 = muon and lep2 = muon and lep1 = not muon
  }
  else  if ((abs(pdgid1)== 13 && abs(pdgid3) == 13) && (abs(pdgid2)!=13)){            
    return 13; //if lep1 = muon and lep3 = muon and lep2 = not muon
  }
  else if (abs(pdgid1)== 13 && abs(pdgid3) == 13 && abs(pdgid2)==13){  
    return 123; //if lep1 = muon and lep2 = muon and lep3 =  muon
  }
  else return 1;
} 


 
float triggerSF_SOS(float _pt1, float _eta1, float _pt2, float _eta2, float _met, float _met_corr, float var=0){
 
  if (_met>=200.0 && _met_corr>=200.0)return 0.97; // inclusive SF for MET>200 GeV
  if (!_file_triggerSF) init_triggerSF_SOS();

  float eta1 = std::min(float(2.399),abs(_eta1));
  float eta2 = std::min(float(2.399),abs(_eta2));
  ///////// first leg muon
  float mu1_l1_data= _histo_l1_data_DoubleMu_MET->GetBinContent(((_histo_l1_data_DoubleMu_MET->GetXaxis())->FindBin(_pt1)),((_histo_l1_data_DoubleMu_MET->GetYaxis())->FindBin(eta1)));
  float mu1_l1_mc= _histo_l1_mc_DoubleMu_MET->GetBinContent(((_histo_l1_mc_DoubleMu_MET->GetXaxis())->FindBin(_pt1)),((_histo_l1_mc_DoubleMu_MET->GetYaxis())->FindBin(eta1)));
  float mu1_l2_data= _histo_l2_data_DoubleMu_MET->GetBinContent(((_histo_l2_data_DoubleMu_MET->GetXaxis())->FindBin(_pt1)),((_histo_l2_data_DoubleMu_MET->GetYaxis())->FindBin(eta1)));
  float mu1_l2_mc= _histo_l2_mc_DoubleMu_MET->GetBinContent(((_histo_l2_mc_DoubleMu_MET->GetXaxis())->FindBin(_pt1)),((_histo_l2_mc_DoubleMu_MET->GetYaxis())->FindBin(eta1)));
  float mu1_l3_data= 1.0;
  float mu1_l3_mc= 1.0; 

  //////// second leg muon
  float mu2_l1_data= _histo_l1_data_DoubleMu_MET->GetBinContent(((_histo_l1_data_DoubleMu_MET->GetXaxis())->FindBin(_pt2)),((_histo_l1_data_DoubleMu_MET->GetYaxis())->FindBin(eta2)));
  float mu2_l1_mc= _histo_l1_mc_DoubleMu_MET->GetBinContent(((_histo_l1_mc_DoubleMu_MET->GetXaxis())->FindBin(_pt2)),((_histo_l1_mc_DoubleMu_MET->GetYaxis())->FindBin(eta2)));
  float mu2_l2_data= _histo_l2_data_DoubleMu_MET->GetBinContent(((_histo_l2_data_DoubleMu_MET->GetXaxis())->FindBin(_pt2)),((_histo_l2_data_DoubleMu_MET->GetYaxis())->FindBin(eta2)));
  float mu2_l2_mc= _histo_l2_mc_DoubleMu_MET->GetBinContent(((_histo_l2_mc_DoubleMu_MET->GetXaxis())->FindBin(_pt2)),((_histo_l2_mc_DoubleMu_MET->GetYaxis())->FindBin(eta2)));
  float mu2_l3_data= 1.0;
  float mu2_l3_mc= 1.0;

  /////// DCA
  float dca_data= 0.906; // DCA SF (inclusive) 
  float dca_mc= 0.962; // DCA SF (inclusive)

  ////// MET
  //-- protection
  float met = std::max(float(50.1),_met);
  float met_corr = std::max(float(50.1),_met_corr);
  // ----
  float met_data;
  float met_mc;
  float met_data_num= _histo_met_num_data->GetBinContent(((_histo_met_num_data->GetXaxis())->FindBin(met)),((_histo_met_num_data->GetYaxis())->FindBin(met_corr)));
  float met_data_denom=_histo_met_denom_data->GetBinContent(((_histo_met_denom_data->GetXaxis())->FindBin(met)),((_histo_met_denom_data->GetYaxis())->FindBin(met_corr)));
  float met_mc_num=_histo_met_num_mc->GetBinContent(((_histo_met_num_mc->GetXaxis())->FindBin(met)),((_histo_met_num_mc->GetYaxis())->FindBin(met_corr)));
  float met_mc_denom=_histo_met_denom_mc->GetBinContent(((_histo_met_denom_mc->GetXaxis())->FindBin(met)),((_histo_met_denom_mc->GetYaxis())->FindBin(met_corr)));
    
  if(met_data_denom == 0) met_data=0.; //was 0!
  else met_data=met_data_num/met_data_denom;
  
  if(met_mc_denom == 0) met_mc=0.; // was 0!
  else met_mc=met_mc_num/met_mc_denom;
  
  float res;
  if(mu1_l1_mc*mu2_l1_mc*mu1_l2_mc*mu2_l2_mc*mu1_l3_mc*mu2_l3_mc*dca_mc*met_mc==0 ) res=1.0;  // was 0!
  else res=(mu1_l1_data*mu2_l1_data*mu1_l2_data*mu2_l2_data*mu1_l3_data*mu2_l3_data*dca_data*met_data)/(mu1_l1_mc*mu2_l1_mc*mu1_l2_mc*mu2_l2_mc*mu1_l3_mc*mu2_l3_mc*dca_mc*met_mc);

  assert (res>0 && "*** Warning we have a negative (or zero) Trigger SF ***");
  
  // ==== Variations conservative 5% also for the SF 
  if(var>0)return res+0.05;
  if(var<0)return res-0.05;
  // ===== CENTRAL VALUE ==========
  return res; 

}



float triggerSF_3l(float _pt1, float _eta1, float _pt2, float _eta2, float _pt3, float _eta3, float _met, float _met_corr, int choose_leptons){
   
  ////   High MET
  if(_met>=200.0 && _met_corr>=200.0)
  {
    return 0.97;
   }
  ///// Intermediate MET
  else if (_met>=125.0 && _met_corr>=125.0 && _met<200.0 ){
    if (choose_leptons == 12){
      return triggerSF_SOS(_pt1, _eta1, _pt2, _eta2, _met, _met_corr);   
    }
    if (choose_leptons ==13){
      return triggerSF_SOS(_pt1, _eta1, _pt3, _eta3, _met, _met_corr);
    }
    if (choose_leptons == 23){
      return triggerSF_SOS(_pt2, _eta2, _pt3, _eta3, _met, _met_corr);
    }
    if (choose_leptons == 123){
      if (!_file_triggerSF) init_triggerSF_SOS();

      //// MET
      //-- protection
      float met = std::max(float(50.1),_met);
      float met_corr = std::max(float(50.1),_met_corr);
      // ----
      float met_data;       
      float met_data_num= _histo_met_num_data->GetBinContent(((_histo_met_num_data->GetXaxis())->FindBin(met)),((_histo_met_num_data->GetYaxis())->FindBin(met_corr)));
      float met_data_denom=_histo_met_denom_data->GetBinContent(((_histo_met_denom_data->GetXaxis())->FindBin(met)),((_histo_met_denom_data->GetYaxis())->FindBin(met_corr)));
      if(met_data_denom == 0) met_data=0.; //was 0!
      else met_data=met_data_num/met_data_denom;

      float mu_data = 1.0 ;
      float mu_mc = 1.0;
      float met_mc = 1.0;
      float dca_data= 0.906; // DCA SF (inclusive)
      float dca_mc= 0.962; // DCA SF (inclusive) 
      return (mu_data*dca_data*met_data)/(mu_mc*dca_mc*met_mc);
    }
    return 1; // to be checked!
    //cout << "Error in triggerSF_3l " << choose_leptons << endl;
    //return -99999;

  }
   ///// Low MET
  else if(_met>=75.0 && _met<125.0 ){
    if (!_file_triggerSF) init_triggerSF_SOS();
    float eta1 = std::min(float(2.399),abs(_eta1));
    float eta2 = std::min(float(2.399),abs(_eta2));
    float eta3 = std::min(float(2.399),abs(_eta3));
    float pt1_temp= std::max(float(5.0),_pt1); // protection as we don't have efficiencies below 5 GeV
    float pt2_temp= std::max(float(5.0),_pt2);
    float pt3_temp= std::max(float(5.0),_pt3);
    float pt1= std::min(float(100.0),pt1_temp); // protection as we don't have efficiencies below 5 GeV                                                                                                           
    float pt2= std::min(float(100.0),pt2_temp);
    float pt3= std::min(float(100.0),pt3_temp);

    ///////first leg muon
    float mu1_l1_data= _histo_l1_data_DoubleMu_MET->GetBinContent(((_histo_l1_data_DoubleMu_MET->GetXaxis())->FindBin(pt1)),((_histo_l1_data_DoubleMu_MET->GetYaxis())->FindBin(eta1)));
    float mu1_l2_data= _histo_l2_data_TripleMu_12_10_5->GetBinContent(((_histo_l2_data_TripleMu_12_10_5->GetXaxis())->FindBin(pt1)),((_histo_l2_data_TripleMu_12_10_5->GetYaxis())->FindBin(eta1)));


   //////// second leg muon
   float mu2_l1_data= _histo_l1_data_DoubleMu_MET->GetBinContent(((_histo_l1_data_DoubleMu_MET->GetXaxis())->FindBin(pt2)),((_histo_l1_data_DoubleMu_MET->GetYaxis())->FindBin(eta2)));
   float mu2_l3_data = _histo_l3_data_TripleMu_5_3_3->GetBinContent(((_histo_l3_data_TripleMu_5_3_3->GetXaxis())->FindBin(pt2)),((_histo_l3_data_TripleMu_5_3_3->GetYaxis())->FindBin(eta2)));

   //////// third leg muon
   float mu3_l1_data = _histo_l1_data_DoubleMu_MET->GetBinContent(((_histo_l1_data_DoubleMu_MET->GetXaxis())->FindBin(pt3)),((_histo_l1_data_DoubleMu_MET->GetYaxis())->FindBin(eta3)));
   float mu3_l3_data = _histo_l3_data_TripleMu_5_3_3->GetBinContent(((_histo_l3_data_TripleMu_5_3_3->GetXaxis())->FindBin(pt3)),((_histo_l3_data_TripleMu_5_3_3->GetYaxis())->FindBin(eta3)));
 
   /////// DZ
   float dz_data= 0.985; // DZ SF (inclusive) 
   /////// DCA
   float mass_data= 0.996; // Mass SF (inclusive) 
  
   //////// first leg muon
   float mu1_l1_mc= _histo_l1_mc_DoubleMu_MET->GetBinContent(((_histo_l1_mc_DoubleMu_MET->GetXaxis())->FindBin(pt1)),((_histo_l1_mc_DoubleMu_MET->GetYaxis())->FindBin(eta1)));
   float mu1_l2_mc= _histo_l2_mc_TripleMu_12_10_5->GetBinContent(((_histo_l2_mc_TripleMu_12_10_5->GetXaxis())->FindBin(pt1)),((_histo_l2_mc_TripleMu_12_10_5->GetYaxis())->FindBin(eta1)));

   //////// second leg muon
   float mu2_l1_mc= _histo_l1_mc_DoubleMu_MET->GetBinContent(((_histo_l1_mc_DoubleMu_MET->GetXaxis())->FindBin(pt2)),((_histo_l1_mc_DoubleMu_MET->GetYaxis())->FindBin(eta2)));
   float mu2_l3_mc = _histo_l3_mc_TripleMu_5_3_3->GetBinContent(((_histo_l3_mc_TripleMu_5_3_3->GetXaxis())->FindBin(pt2)),((_histo_l3_mc_TripleMu_5_3_3->GetYaxis())->FindBin(eta2)));

   //////// third leg muon
   float mu3_l1_mc = _histo_l1_mc_DoubleMu_MET->GetBinContent(((_histo_l1_mc_DoubleMu_MET->GetXaxis())->FindBin(pt3)),((_histo_l1_mc_DoubleMu_MET->GetYaxis())->FindBin(eta3)));
   float mu3_l3_mc = _histo_l3_mc_TripleMu_5_3_3->GetBinContent(((_histo_l3_mc_TripleMu_5_3_3->GetXaxis())->FindBin(pt3)),((_histo_l3_mc_TripleMu_5_3_3->GetYaxis())->FindBin(eta3)));
 
      
   float res;
   if(mu1_l1_mc*mu2_l1_mc*mu3_l1_mc*mu1_l2_mc*mu2_l3_mc*mu3_l3_mc==0) res=1.0;  // was 0!
   else res=(((mu1_l1_data*mu2_l1_data*mu3_l1_data*mu1_l2_data*mu2_l3_data*mu3_l3_data)*((7.401/(7.401+8.856))+((8.856/(8.856+7.401))*dz_data*mass_data)))/(mu1_l1_mc*mu2_l1_mc*mu3_l1_mc*mu1_l2_mc*mu2_l3_mc*mu3_l3_mc));
   
   if (res<=0) cout << "*** Warning we have a negative (or zero) Trigger SF ***"<< endl;
   //  if(var>0) return res+0.05; // +5%
   //  if(var<0) return res-0.05; // -5%
  return res;
  }

  return 1; // to be checked!
  //cout << "Error in triggerSF_3l " << _met << " " << _met_corr << endl;
  //return -99999;
 }



float triggereff_SOS(float _pt1, float _eta1, float _pt2, float _eta2, float _met, float _met_corr, float var=0){
 
  //  if (var_ee!=0) assert(0); // NOT IMPLEMENTED

  if (_met>=200.0 && _met_corr>=200.0){
    return 0.95; // inclusive efficiency for MET>200 GeV
  }
  if (!_file_triggerSF) init_triggerSF_SOS();

  float eta1 = std::min(float(2.399),abs(_eta1));
  float eta2 = std::min(float(2.399),abs(_eta2));

  ///////// first leg muon
  float mu1_l1_data= _histo_l1_data_DoubleMu_MET->GetBinContent(((_histo_l1_data_DoubleMu_MET->GetXaxis())->FindBin(_pt1)),((_histo_l1_data_DoubleMu_MET->GetYaxis())->FindBin(eta1)));
  float mu1_l2_data= _histo_l2_data_DoubleMu_MET->GetBinContent(((_histo_l2_data_DoubleMu_MET->GetXaxis())->FindBin(_pt1)),((_histo_l2_data_DoubleMu_MET->GetYaxis())->FindBin(eta1)));
  float mu1_l3_data= 1.0;

  //////// second leg muon
  float mu2_l1_data= _histo_l1_data_DoubleMu_MET->GetBinContent(((_histo_l1_data_DoubleMu_MET->GetXaxis())->FindBin(_pt2)),((_histo_l1_data_DoubleMu_MET->GetYaxis())->FindBin(eta2)));
  float mu2_l2_data= _histo_l2_data_DoubleMu_MET->GetBinContent(((_histo_l2_data_DoubleMu_MET->GetXaxis())->FindBin(_pt2)),((_histo_l2_data_DoubleMu_MET->GetYaxis())->FindBin(eta2)));
  float mu2_l3_data= 1.0;
 
  /////// DCA
  float dca_data= 0.906; // DCA SF (inclusive) 
  ////// MET
  //-- protection
  float met = std::max(float(50.1),_met);
  float met_corr = std::max(float(50.1),_met_corr);
  //----

  float met_data;
  float met_data_num= _histo_met_num_data->GetBinContent(((_histo_met_num_data->GetXaxis())->FindBin(met)),((_histo_met_num_data->GetYaxis())->FindBin(met_corr)));
  float met_data_denom=_histo_met_denom_data->GetBinContent(((_histo_met_denom_data->GetXaxis())->FindBin(met)),((_histo_met_denom_data->GetYaxis())->FindBin(met_corr)));
    
  if(met_data_denom == 0) met_data=1.0; // was 0!
  else met_data=met_data_num/met_data_denom;
 
  float res= mu1_l1_data*mu2_l1_data*mu1_l2_data*mu2_l2_data*mu1_l3_data*mu2_l3_data*dca_data*met_data;
  assert (res>0 && "*** Warning we have a negative (or zero) Trigger efficiency ***");
  if(var>0) return res+0.05; // +5%
  if(var<0) return res-0.05; // -5%
  return res;
}

float triggereff_3l(float _pt1, float _eta1, float _pt2, float _eta2, float _pt3, float _eta3, float _met, float _met_corr, float choose_leptons){ 
  /////// High MET bin 
  if (_met>=200.0 && _met_corr>=200.0) return 0.95;

  ///// Intermediate MET
  else if(_met>=125.0 && _met_corr>=125.0 && _met<=200.0){
    if (choose_leptons==12){
      return triggereff_SOS( _pt1, _eta1, _pt2,  _eta2, _met, _met_corr, 0);
    }
    if (choose_leptons==23){
      return triggereff_SOS (_pt2, _eta2, _pt3,  _eta3, _met, _met_corr, 0);
    }
    if (choose_leptons==13) {
      return triggereff_SOS( _pt1, _eta1, _pt3,  _eta3, _met, _met_corr, 0);              
    }                                                                                                                                    
    if (choose_leptons==123){
      if (!_file_triggerSF) init_triggerSF_SOS();
      
      //// MET
      //-- protection
      float met = std::max(float(50.1),_met);
      float met_corr = std::max(float(50.1),_met_corr);
      // ----
      float met_data;
    
      float met_data_num= _histo_met_num_data->GetBinContent(((_histo_met_num_data->GetXaxis())->FindBin(met)),((_histo_met_num_data->GetYaxis())->FindBin(met_corr)));
      float met_data_denom=_histo_met_denom_data->GetBinContent(((_histo_met_denom_data->GetXaxis())->FindBin(met)),((_histo_met_denom_data->GetYaxis())->FindBin(met_corr)));
      if(met_data_denom == 0) met_data=0.; //was 0!
      else met_data=met_data_num/met_data_denom;
      
      float mu_data = 1.0 ;
      //float mu_mc = 1.0;
      //float met_mc = 1.0;
      float dca_data= 0.906; // DCA SF (inclusive) 
      
      //float res;
      return (mu_data*dca_data*met_data);
    } 
    return 1; // to be checked!
    //cout << "Error in triggereff_3l" << endl;
    //return -99999;
  }

  /////// Low MET bin
  else if (_met>=75.0 && _met<125.0){ 
    if (!_file_triggerSF) init_triggerSF_SOS();

  float eta1 = std::min(float(2.399),abs(_eta1));
  float eta2 = std::min(float(2.399),abs(_eta2));
  float eta3 = std::min(float(2.399),abs(_eta3));
  float pt1_temp= std::max(float(5.0),_pt1); // protection as we don't have efficiencies below 5 GeV                                                                                                             
  float pt2_temp= std::max(float(5.0),_pt2);
  float pt3_temp= std::max(float(5.0),_pt3);
  float pt1= std::min(float(100.0),pt1_temp); // protection as we don't have efficiencies below 5 GeV                                                                                                           
  float pt2= std::min(float(100.0),pt2_temp);
  float pt3= std::min(float(100.0),pt3_temp);

  ///////// first leg muon
  float mu1_l1_data= _histo_l1_data_DoubleMu_MET->GetBinContent(((_histo_l1_data_DoubleMu_MET->GetXaxis())->FindBin(pt1)),((_histo_l1_data_DoubleMu_MET->GetYaxis())->FindBin(eta1)));
  float mu1_l2_data= _histo_l2_data_TripleMu_12_10_5->GetBinContent(((_histo_l2_data_TripleMu_12_10_5->GetXaxis())->FindBin(pt1)),((_histo_l2_data_TripleMu_12_10_5->GetYaxis())->FindBin(eta1)));  
  //////// second leg muon
  float mu2_l1_data = _histo_l1_data_DoubleMu_MET->GetBinContent(((_histo_l1_data_DoubleMu_MET->GetXaxis())->FindBin(pt2)),((_histo_l1_data_DoubleMu_MET->GetYaxis())->FindBin(eta2)));
  float mu2_l3_data = _histo_l3_data_TripleMu_5_3_3->GetBinContent(((_histo_l3_data_TripleMu_5_3_3->GetXaxis())->FindBin(pt2)),((_histo_l3_data_TripleMu_5_3_3->GetYaxis())->FindBin(eta2)));
  //////// third leg muon
  float mu3_l1_data = _histo_l1_data_DoubleMu_MET->GetBinContent(((_histo_l1_data_DoubleMu_MET->GetXaxis())->FindBin(pt3)),((_histo_l1_data_DoubleMu_MET->GetYaxis())->FindBin(eta3)));
  float mu3_l3_data= _histo_l3_data_TripleMu_5_3_3->GetBinContent(((_histo_l3_data_TripleMu_5_3_3->GetXaxis())->FindBin(pt3)),((_histo_l3_data_TripleMu_5_3_3->GetYaxis())->FindBin(eta3)));
 
  /////// DZ
  float dz_data= 0.985; // DZ SF (inclusive) 
  /////// DCA
  float mass_data= 0.996; // Mass SF (inclusive) 
 
  float res= mu1_l1_data*mu2_l1_data*mu3_l1_data*mu1_l2_data*mu2_l3_data*mu3_l3_data*((7.401/(7.401+8.856))+((8.856/(8.856+7.401))*dz_data*mass_data));
  //if(_met>=75.0 && _met<125.0 && pt1<30 && pt2<30 && pt3<30 && pt1>5 && pt2>3.5 && pt3>3.5 && choose_leptons==123) {
  //    cout <<"The total efficiency is : " << res <<endl;
  //    cout << "pT1/pT2/pT3 = " << pt1 <<"/"<< pt2 <<"/"<< pt3<< endl;  
  //    cout << "eta1/eta2/eta3 = " << eta1 <<"/"<< eta2 <<"/"<< eta3<< endl;
  //    cout << "mu1_l2_data/mu2_l3_data/mu3_l3_data = " << mu1_l2_data <<"/"<< mu2_l3_data <<"/"<< mu3_l3_data<< endl;
  //    cout << "the rest = " << ((7.401/(7.401+8.856))+((8.856/(8.856+7.401))*dz_data*mass_data))<< endl;
  //    cout << "L1 values= " << mu1_l1_data*mu2_l1_data*mu3_l1_data <<endl;  
  //    cout << "================" << endl; 
  //  }
  assert (res>0 && "*** Warning we have a negative (or zero) Trigger efficiency ***");
  //  if(var>0) return res+0.05; // +5%
  //  if(var<0) return res-0.05; // -5%
  return res;
  } 
  return 1; // to be checked!
  //cout << "Error in triggereff_3l" << endl;
  //return -99999;
} 
 
 
void lepton_trigger_SF() {}
