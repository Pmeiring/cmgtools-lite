#include "TH2F.h"
#include "TMath.h"
#include "TGraphAsymmErrors.h"
#include "TFile.h"
#include "TSystem.h"
#include <iostream>

using namespace std;

TString CMSSW_BASE_SF = gSystem->ExpandPathName("${CMSSW_BASE}");
TString DATA_SF = CMSSW_BASE_SF+"/src/CMGTools/TTHAnalysis/data";

float getSF(TH2F* hist, float pt, float eta){
    int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(eta)));
    return hist->GetBinContent(xbin,ybin);
}

float getUnc(TH2F* hist, float pt, float eta){
    int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(eta)));
    return hist->GetBinError(xbin,ybin);
}


// TRIGGER SCALE FACTORS FULLSIM
// -------------------------------------------------------------


int lepton_permut(int pdgid1, int pdgid2, int  pdgid3) {
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

// files
TFile* f_trigSF_2l = new TFile(DATA_SF+"/sos_lepton_SF/triggerSF_36invfb.root","read");

// fullsim
TH2F* h_trigEff_mumuMET_l1_data      = (TH2F*) f_trigSF_2l->Get("hist2dnum_L1Mu__HLT_DoubleMu3_PFMET50pt");
TH2F* h_trigEff_mumuMET_l2_data      = (TH2F*) f_trigSF_2l->Get("hist2dnum_L2Mu__HLT_DoubleMu3_PFMET50pt");
TH2F* h_trigEff_mumuMET_l3_data      = (TH2F*) f_trigSF_2l->Get("hist2dnum_L3Mu__HLT_DoubleMu3_PFMET50pt");
TH2F* h_trigEff_mumuMET_l1_mc        = (TH2F*) f_trigSF_2l->Get("hist2dnum_MC_L1Mu__HLT_DoubleMu3_PFMET50pt");
TH2F* h_trigEff_mumuMET_l2_mc        = (TH2F*) f_trigSF_2l->Get("hist2dnum_MC_L2Mu__HLT_DoubleMu3_PFMET50pt");
TH2F* h_trigEff_mumuMET_l3_mc        = (TH2F*) f_trigSF_2l->Get("hist2dnum_MC_L3Mu__HLT_DoubleMu3_PFMET50pt");
TH2F* h_trigEff_mumuMET_met_num_data = (TH2F*) f_trigSF_2l->Get("hnummet"   );
TH2F* h_trigEff_mumuMET_met_den_data = (TH2F*) f_trigSF_2l->Get("hdenmet"   );
TH2F* h_trigEff_mumuMET_met_num_mc   = (TH2F*) f_trigSF_2l->Get("hnummet_mc");
TH2F* h_trigEff_mumuMET_met_den_mc   = (TH2F*) f_trigSF_2l->Get("hdenmet_mc");

// fullsim, additional for 3L
TH2F* h_trigEff_mumumu_l2_data       = (TH2F*) f_trigSF_2l->Get("hist2dnum_HLT_Mu5__HLT_TripleMu_12_10_5pt"   );
TH2F* h_trigEff_mumumu_l3_data       = (TH2F*) f_trigSF_2l->Get("hist2dnum_HLT_Mu3__HLT_TripleMu_5_3_3pt"     );
TH2F* h_trigEff_mumumu_l2_mc         = (TH2F*) f_trigSF_2l->Get("hist2dnum_MC_HLT_Mu5__HLT_TripleMu_12_10_5pt");
TH2F* h_trigEff_mumumu_l3_mc         = (TH2F*) f_trigSF_2l->Get("hist2dnum_MC_HLT_Mu3__HLT_TripleMu_5_3_3pt"  );

// 2l case
float triggerSFfullsim(float _pt1, float _eta1, float _pt2, float _eta2, float _met, float _met_corr, float var=0){

	// high-MET triggers
	if(_met>=200.0 && _met_corr>=200.0) return 0.97; // inclusive SF for MET>200 GeV

	// rest for double-Mu-plus-MET trigger

	// protection
	float eta1     = std::min(float(2.399), abs(_eta1));
	float eta2     = std::min(float(2.399), abs(_eta2));
	float met      = std::max(float(50.1) , _met      );
	float met_corr = std::max(float(50.1) , _met_corr );

	// first muon leg
	float mu1_l1_data = h_trigEff_mumuMET_l1_data -> GetBinContent(h_trigEff_mumuMET_l1_data -> GetXaxis() -> FindBin(_pt1),
	                                                               h_trigEff_mumuMET_l1_data -> GetYaxis() -> FindBin(eta1));
	float mu1_l1_mc   = h_trigEff_mumuMET_l1_mc   -> GetBinContent(h_trigEff_mumuMET_l1_mc   -> GetXaxis() -> FindBin(_pt1),
	                                                               h_trigEff_mumuMET_l1_data -> GetYaxis() -> FindBin(eta1));
	float mu1_l2_data = h_trigEff_mumuMET_l2_data -> GetBinContent(h_trigEff_mumuMET_l2_data -> GetXaxis() -> FindBin(_pt1),
	                                                               h_trigEff_mumuMET_l2_data -> GetYaxis() -> FindBin(eta1));
	float mu1_l2_mc   = h_trigEff_mumuMET_l2_mc   -> GetBinContent(h_trigEff_mumuMET_l2_mc   -> GetXaxis() -> FindBin(_pt1),
	                                                               h_trigEff_mumuMET_l2_data -> GetYaxis() -> FindBin(eta1));
	float mu1_l3_data = 1.0;
	float mu1_l3_mc   = 1.0; 

	// second muon leg
	float mu2_l1_data = h_trigEff_mumuMET_l1_data -> GetBinContent(h_trigEff_mumuMET_l1_data -> GetXaxis() -> FindBin(_pt2),
	                                                               h_trigEff_mumuMET_l1_data -> GetYaxis() -> FindBin(eta2));
	float mu2_l1_mc   = h_trigEff_mumuMET_l1_mc   -> GetBinContent(h_trigEff_mumuMET_l1_mc   -> GetXaxis() -> FindBin(_pt2),
	                                                               h_trigEff_mumuMET_l1_mc   -> GetYaxis() -> FindBin(eta2));
	float mu2_l2_data = h_trigEff_mumuMET_l2_data -> GetBinContent(h_trigEff_mumuMET_l2_data -> GetXaxis() -> FindBin(_pt2),
	                                                               h_trigEff_mumuMET_l2_data -> GetYaxis() -> FindBin(eta2));
	float mu2_l2_mc   = h_trigEff_mumuMET_l2_mc   -> GetBinContent(h_trigEff_mumuMET_l2_mc   -> GetXaxis() -> FindBin(_pt2),
	                                                               h_trigEff_mumuMET_l2_mc   -> GetYaxis() -> FindBin(eta2));
	float mu2_l3_data= 1.0;
	float mu2_l3_mc= 1.0;

	// dca leg
	float dca_data = 0.906; // DCA SF (inclusive) 
	float dca_mc   = 0.962; // DCA SF (inclusive)

	// met leg
	float met_data_num   = h_trigEff_mumuMET_met_num_data -> GetBinContent(h_trigEff_mumuMET_met_num_data -> GetXaxis() -> FindBin(met),
	                                                                       h_trigEff_mumuMET_met_num_data -> GetYaxis() -> FindBin(met_corr));
	float met_data_den   = h_trigEff_mumuMET_met_den_data -> GetBinContent(h_trigEff_mumuMET_met_den_data -> GetXaxis() -> FindBin(met),
	                                                                       h_trigEff_mumuMET_met_den_data -> GetYaxis() -> FindBin(met_corr));
	float met_mc_num     = h_trigEff_mumuMET_met_num_mc   -> GetBinContent(h_trigEff_mumuMET_met_num_mc   -> GetXaxis() -> FindBin(met),
	                                                                       h_trigEff_mumuMET_met_num_mc   -> GetYaxis() -> FindBin(met_corr));
	float met_mc_den     = h_trigEff_mumuMET_met_den_mc   -> GetBinContent(h_trigEff_mumuMET_met_den_mc   -> GetXaxis() -> FindBin(met),
	                                                                       h_trigEff_mumuMET_met_den_mc   -> GetYaxis() -> FindBin(met_corr));
	float met_data;
	float met_mc;
	met_data = (met_data_den == 0) ? 0 : met_data_num/met_data_den;
	met_mc   = (met_mc_den   == 0) ? 0 : met_mc_num  /met_mc_den  ;

	// putting everything together
	float res;
	if(mu1_l1_mc*mu2_l1_mc*mu1_l2_mc*mu2_l2_mc*mu1_l3_mc*mu2_l3_mc*dca_mc*met_mc==0 ) res=1.0;  // was 0!
	else res=(mu1_l1_data*mu2_l1_data*mu1_l2_data*mu2_l2_data*mu1_l3_data*mu2_l3_data*dca_data*met_data)/(mu1_l1_mc*mu2_l1_mc*mu1_l2_mc*mu2_l2_mc*mu1_l3_mc*mu2_l3_mc*dca_mc*met_mc);


	// variations: conservative 5% also for the SF 
	if(var>0) return res*(1+0.05);
	if(var<0) return res*(1-0.05);

	//if(res>2.2) std::cout<<res<<" "<<met_mc<<" "<<met_data<<" "<<mu1_l1_data<<" "<<mu1_l1_mc<<" "<<mu1_l2_data<<" "<<mu1_l2_mc<<" "<<mu2_l1_data<<" "<<mu2_l1_mc<<" "<<mu2_l2_data<<" "<<mu2_l2_mc<<std::endl;

    //std::cout << res << std::endl;

	assert (res>0 && "*** Warning we have a negative (or zero) Trigger SF ***");
	return res; 

}


float triggerSFfullsim3L(float _pt1, float _eta1, float _pt2, float _eta2, float _pt3, float _eta3, float _met, float _met_corr, int choose_leptons){


	// high-MET triggers
	if(_met>=200.0 && _met_corr>=200.0) return 0.97; // inclusive SF for MET>200 GeV

	// intermediate MET bin
	else if (_met>=125.0 && _met_corr>=125.0 && _met<200.0 ){

		if (choose_leptons == 12 ) return triggerSFfullsim(_pt1, _eta1, _pt2, _eta2, _met, _met_corr);
		if (choose_leptons == 13 ) return triggerSFfullsim(_pt1, _eta1, _pt3, _eta3, _met, _met_corr);
		if (choose_leptons == 23 ) return triggerSFfullsim(_pt2, _eta2, _pt3, _eta3, _met, _met_corr);

		if (choose_leptons == 123) { 

			// protection
			float met      = std::max(float(50.1), _met     );
			float met_corr = std::max(float(50.1), _met_corr);

			float met_data;       
			float met_data_num   = h_trigEff_mumuMET_met_num_data -> GetBinContent(h_trigEff_mumuMET_met_num_data -> GetXaxis() -> FindBin(met),
			                                                                       h_trigEff_mumuMET_met_num_data -> GetYaxis() -> FindBin(met_corr));
			float met_data_den   = h_trigEff_mumuMET_met_den_data -> GetBinContent(h_trigEff_mumuMET_met_den_data -> GetXaxis() -> FindBin(met),
			                                                                       h_trigEff_mumuMET_met_den_data -> GetYaxis() -> FindBin(met_corr));
			met_data = (met_data_den == 0) ? 0 : met_data_num/met_data_den;

			float mu_data  = 1.0;
			float mu_mc    = 1.0;
			float met_mc   = 1.0;
			float dca_data = 0.906; // DCA SF (inclusive)
			float dca_mc   = 0.962; // DCA SF (inclusive) 
			return (mu_data*dca_data*met_data)/(mu_mc*dca_mc*met_mc);
		}
  
		// else
		return 1;
	}

	// low MET bin
	else if(_met>=75.0 && _met<125.0 ){

		// protection
		float eta1 = std::min(float(2.399),abs(_eta1));
		float eta2 = std::min(float(2.399),abs(_eta2));
		float eta3 = std::min(float(2.399),abs(_eta3));
		
		float pt1_temp = std::max(float(5.0),_pt1); // protection as we don't have efficiencies below 5 GeV
		float pt2_temp = std::max(float(5.0),_pt2);
		float pt3_temp = std::max(float(5.0),_pt3);
		float pt1      = std::min(float(100.0),pt1_temp);
		float pt2      = std::min(float(100.0),pt2_temp);
		float pt3      = std::min(float(100.0),pt3_temp);

		// first muon leg
		float mu1_l1_data = h_trigEff_mumuMET_l1_data -> GetBinContent(h_trigEff_mumuMET_l1_data -> GetXaxis() -> FindBin(pt1 ),
		                                                               h_trigEff_mumuMET_l1_data -> GetYaxis() -> FindBin(eta1));
		float mu1_l2_data = h_trigEff_mumumu_l2_data  -> GetBinContent(h_trigEff_mumumu_l2_data  -> GetXaxis() -> FindBin(pt1 ),
		                                                               h_trigEff_mumumu_l2_data  -> GetYaxis() -> FindBin(eta1));
		float mu1_l1_mc   = h_trigEff_mumuMET_l1_mc   -> GetBinContent(h_trigEff_mumuMET_l1_mc   -> GetXaxis() -> FindBin(pt1 ),
		                                                               h_trigEff_mumuMET_l1_mc   -> GetYaxis() -> FindBin(eta1));
		float mu1_l2_mc   = h_trigEff_mumumu_l2_mc    -> GetBinContent(h_trigEff_mumumu_l2_mc    -> GetXaxis() -> FindBin(pt1 ),
		                                                               h_trigEff_mumumu_l2_mc    -> GetYaxis() -> FindBin(eta1));
 
		
		// second muon leg
		float mu2_l1_data = h_trigEff_mumuMET_l1_data -> GetBinContent(h_trigEff_mumuMET_l1_data -> GetXaxis() -> FindBin(pt2 ),
		                                                               h_trigEff_mumuMET_l1_data -> GetYaxis() -> FindBin(eta2));
		float mu2_l3_data = h_trigEff_mumumu_l3_data  -> GetBinContent(h_trigEff_mumumu_l3_data  -> GetXaxis() -> FindBin(pt2 ),
		                                                               h_trigEff_mumumu_l3_data  -> GetYaxis() -> FindBin(eta2));
		float mu2_l1_mc   = h_trigEff_mumuMET_l1_mc   -> GetBinContent(h_trigEff_mumuMET_l1_mc   -> GetXaxis() -> FindBin(pt2 ),
		                                                               h_trigEff_mumuMET_l1_mc   -> GetYaxis() -> FindBin(eta2));
		float mu2_l3_mc   = h_trigEff_mumumu_l3_mc    -> GetBinContent(h_trigEff_mumumu_l3_mc    -> GetXaxis() -> FindBin(pt2 ),
		                                                               h_trigEff_mumumu_l3_mc    -> GetYaxis() -> FindBin(eta2));
		
		// third muon leg
		float mu3_l1_data = h_trigEff_mumuMET_l1_data -> GetBinContent(h_trigEff_mumuMET_l1_data -> GetXaxis() -> FindBin(pt3 ),
		                                                               h_trigEff_mumuMET_l1_data -> GetYaxis() -> FindBin(eta3));
		float mu3_l3_data = h_trigEff_mumumu_l3_data  -> GetBinContent(h_trigEff_mumumu_l3_data  -> GetXaxis() -> FindBin(pt3 ),
		                                                               h_trigEff_mumumu_l3_data  -> GetYaxis() -> FindBin(eta3));
		float mu3_l1_mc   = h_trigEff_mumuMET_l1_mc   -> GetBinContent(h_trigEff_mumuMET_l1_mc   -> GetXaxis() -> FindBin(pt3 ),
		                                                               h_trigEff_mumuMET_l1_mc   -> GetYaxis() -> FindBin(eta3));
		float mu3_l3_mc   = h_trigEff_mumumu_l3_mc    -> GetBinContent(h_trigEff_mumumu_l3_mc    -> GetXaxis() -> FindBin(pt3 ),
		                                                               h_trigEff_mumumu_l3_mc    -> GetYaxis() -> FindBin(eta3));

		// DZ
		float dz_data   = 0.985; // DZ SF (inclusive) 

		// DCA
		float mass_data = 0.996; // Mass SF (inclusive) 
  
		// putting all together 
		float res;
		if(mu1_l1_mc*mu2_l1_mc*mu3_l1_mc*mu1_l2_mc*mu2_l3_mc*mu3_l3_mc==0) res=1.0;  // was 0!
		else res = (((mu1_l1_data*mu2_l1_data*mu3_l1_data*mu1_l2_data*mu2_l3_data*mu3_l3_data)*((7.401/(7.401+8.856))+((8.856/(8.856+7.401))*dz_data*mass_data)))/(mu1_l1_mc*mu2_l1_mc*mu3_l1_mc*mu1_l2_mc*mu2_l3_mc*mu3_l3_mc));
   

		if (res<=0) cout << "*** Warning we have a negative (or zero) Trigger SF ***"<< endl;
		return res;
	}

	// else
	return 1; // to be checked!
}


float triggerSFfullsimWZ(float _pt1, float _eta1, float _pt2, float _eta2, float _pt3, float _eta3, float _met, float _met_corr, int choose_leptons){
	return 1.0;
}



// TRIGGER EFFICIENCY FASTSIM
// -------------------------------------------------------------


// 2l
float triggerEff(float _pt1, float _eta1, float _pt2, float _eta2, float _met, float _met_corr, float var=0){
 
	// high-MET triggers
	if(_met>=200.0 && _met_corr>=200.0) return 0.95; // inclusive efficiency for MET>200 GeV

	// double-Mu-plut-MET trigger
	float eta1 = std::min(float(2.399), abs(_eta1));
	float eta2 = std::min(float(2.399), abs(_eta2));

	// first muon leg
	float mu1_l1_data = h_trigEff_mumuMET_l1_data -> GetBinContent(h_trigEff_mumuMET_l1_data->GetXaxis()->FindBin(_pt1), \
	                                                               h_trigEff_mumuMET_l1_data->GetYaxis()->FindBin(eta1));
	float mu1_l2_data = h_trigEff_mumuMET_l2_data -> GetBinContent(h_trigEff_mumuMET_l2_data->GetXaxis()->FindBin(_pt1), \
	                                                               h_trigEff_mumuMET_l2_data->GetYaxis()->FindBin(eta1));
	float mu1_l3_data = 1.0;

	// second muon leg
	float mu2_l1_data = h_trigEff_mumuMET_l1_data -> GetBinContent(h_trigEff_mumuMET_l1_data->GetXaxis()->FindBin(_pt2), \
	                                                               h_trigEff_mumuMET_l1_data->GetYaxis()->FindBin(eta2));
	float mu2_l2_data = h_trigEff_mumuMET_l2_data -> GetBinContent(h_trigEff_mumuMET_l2_data->GetXaxis()->FindBin(_pt2), \
	                                                               h_trigEff_mumuMET_l2_data->GetYaxis()->FindBin(eta2));
	float mu2_l3_data = 1.0;

	// DCA
	float dca_data = 0.906; 

	// MET
	float met      = std::max(float(50.1), _met     );
	float met_corr = std::max(float(50.1), _met_corr);

	float met_data_num = h_trigEff_mumuMET_met_num_data -> GetBinContent(h_trigEff_mumuMET_met_num_data -> GetXaxis() -> FindBin(met),
	                                                                     h_trigEff_mumuMET_met_num_data -> GetYaxis() -> FindBin(met_corr));
	float met_data_den = h_trigEff_mumuMET_met_den_data -> GetBinContent(h_trigEff_mumuMET_met_den_data -> GetXaxis() -> FindBin(met),
	                                                                     h_trigEff_mumuMET_met_den_data -> GetYaxis() -> FindBin(met_corr));
	float met_data;
	if(met_data_den == 0) met_data = 1.0;
	else met_data = met_data_num/met_data_den;
 
	float res = mu1_l1_data*mu2_l1_data*mu1_l2_data*mu2_l2_data*mu1_l3_data*mu2_l3_data*dca_data*met_data;

	assert (res>0 && "*** Warning we have a negative (or zero) Trigger efficiency ***");

	if(var > 0) return res*(1+0.05); // +5%
	if(var < 0) return res*(1-0.05); // -5%

	return res;
}


// 3l
float triggerEff3L(float _pt1, float _eta1, float _pt2, float _eta2, float _pt3, float _eta3, float _met, float _met_corr, float choose_leptons){
 
	// high-MET triggers
	if(_met>=200.0 && _met_corr>=200.0) return 0.95; // inclusive efficiency for MET>200 GeV

	// double-Mu-plut-MET trigger
	else if(_met>=125.0 && _met_corr>=125.0 && _met<=200.0){
		if (choose_leptons==12) return triggerEff(_pt1, _eta1, _pt2,  _eta2, _met, _met_corr, 0);
    	if (choose_leptons==23) return triggerEff(_pt2, _eta2, _pt3,  _eta3, _met, _met_corr, 0);
    	if (choose_leptons==13) return triggerEff(_pt1, _eta1, _pt3,  _eta3, _met, _met_corr, 0);              

		if (choose_leptons==123){
		  
			// MET
			float met      = std::max(float(50.1), _met     );
			float met_corr = std::max(float(50.1), _met_corr);
			
			float met_data_num = h_trigEff_mumuMET_met_num_data -> GetBinContent(h_trigEff_mumuMET_met_num_data->GetXaxis()->FindBin(met), \
			                                                                     h_trigEff_mumuMET_met_num_data->GetYaxis()->FindBin(met_corr));
			float met_data_den = h_trigEff_mumuMET_met_den_data -> GetBinContent(h_trigEff_mumuMET_met_den_data->GetXaxis()->FindBin(met), \
			                                                                     h_trigEff_mumuMET_met_den_data->GetYaxis()->FindBin(met_corr));

			float met_data;
			if(met_data_den == 0) met_data=0.; //was 0!
			else met_data=met_data_num/met_data_den;
			
			float mu_data  = 1.0 ;
			float dca_data = 0.906; 
			
			//float res;
			return (mu_data*dca_data*met_data);
		} 
		return 1; // to be checked!
	}

	// Low-MET bin
	else if (_met>=75.0 && _met<125.0){ 
	
		float eta1 = std::min(float(2.399), abs(_eta1));
		float eta2 = std::min(float(2.399), abs(_eta2));
		float eta3 = std::min(float(2.399), abs(_eta3));

		float pt1_temp = std::max(float(5.0)  , _pt1    ); // protection as we don't have efficiencies below 5 GeV
		float pt2_temp = std::max(float(5.0)  , _pt2    );
		float pt3_temp = std::max(float(5.0)  , _pt3    );
		float pt1      = std::min(float(100.0), pt1_temp); // protection as we don't have efficiencies below 5 GeV
		float pt2      = std::min(float(100.0), pt2_temp);
		float pt3      = std::min(float(100.0), pt3_temp);

		// first muon leg
		float mu1_l1_data = h_trigEff_mumuMET_l1_data -> GetBinContent(h_trigEff_mumuMET_l1_data -> GetXaxis() -> FindBin(pt1 ),
		                                                               h_trigEff_mumuMET_l1_data -> GetYaxis() -> FindBin(eta1));
		float mu1_l2_data = h_trigEff_mumumu_l2_data  -> GetBinContent(h_trigEff_mumumu_l2_data  -> GetXaxis() -> FindBin(pt1 ),
		                                                               h_trigEff_mumumu_l2_data  -> GetYaxis() -> FindBin(eta1));

		// second muon leg
		float mu2_l1_data = h_trigEff_mumuMET_l1_data -> GetBinContent(h_trigEff_mumuMET_l1_data -> GetXaxis() -> FindBin(pt2 ),
		                                                               h_trigEff_mumuMET_l1_data -> GetYaxis() -> FindBin(eta2));
		float mu2_l3_data = h_trigEff_mumumu_l3_data  -> GetBinContent(h_trigEff_mumumu_l3_data  -> GetXaxis() -> FindBin(pt2 ),
		                                                               h_trigEff_mumumu_l3_data  -> GetYaxis() -> FindBin(eta2));

		// third muon leg
		float mu3_l1_data = h_trigEff_mumuMET_l1_data -> GetBinContent(h_trigEff_mumuMET_l1_data -> GetXaxis() -> FindBin(pt3 ),
		                                                               h_trigEff_mumuMET_l1_data -> GetYaxis() -> FindBin(eta3));
		float mu3_l3_data = h_trigEff_mumumu_l3_data  -> GetBinContent(h_trigEff_mumumu_l3_data  -> GetXaxis() -> FindBin(pt3 ),
		                                                               h_trigEff_mumumu_l3_data  -> GetYaxis() -> FindBin(eta3));

		// DZ
		float dz_data   = 0.985; // DZ SF (inclusive) 

		// DCA
		float mass_data = 0.996; // Mass SF (inclusive) 

		
		float res = mu1_l1_data*mu2_l1_data*mu3_l1_data*mu1_l2_data*mu2_l3_data*mu3_l3_data*((7.401/(7.401+8.856))+((8.856/(8.856+7.401))*dz_data*mass_data));

		assert (res>0 && "*** Warning we have a negative (or zero) Trigger efficiency ***");
		return res;
	} 
	return 1;
} 









// LEPTON SCALE FACTORS FULLSIM
// -------------------------------------------------------------


// electrons
TFile* f_elSF_looseToTight_barrel             = new TFile(DATA_SF+"/sos_lepton_SF_2017/el_SOS_barrel.root" , "read");
TFile* f_elSF_looseToTight_endcap             = new TFile(DATA_SF+"/sos_lepton_SF_2017/el_SOS_endcap.root" , "read");
TFile* f_elSF_recoToLoose_lowPt               = new TFile(DATA_SF+"/sos_lepton_SF_2017/el_reco_lowpt.root" , "read");
TFile* f_elSF_recoToLoose_highPt              = new TFile(DATA_SF+"/sos_lepton_SF_2017/el_reco_highpt.root", "read");
TGraphAsymmErrors* h_elSF_looseToTight_barrel = (TGraphAsymmErrors*) f_elSF_looseToTight_barrel->Get("ratio");
TGraphAsymmErrors* h_elSF_looseToTight_endcap = (TGraphAsymmErrors*) f_elSF_looseToTight_endcap->Get("ratio");
TH2F* h_elSF_recoToLoose_lowPt                = (TH2F*) f_elSF_recoToLoose_lowPt ->Get("EGamma_SF2D");
TH2F* h_elSF_recoToLoose_highPt               = (TH2F*) f_elSF_recoToLoose_highPt->Get("EGamma_SF2D");


int getBinElectronLoose(float pt){
	// update this!
	if     (pt >  5.0 && pt <= 12.5) return 0;
	else if(pt > 12.5 && pt <= 16.0) return 1;
	else if(pt > 16.0 && pt <= 20.0) return 2;
	else if(pt > 20.0 && pt <= 25.0) return 3;
	else if(pt > 25.0              ) return 4;
	else {
		assert(0);
	}
}

float getElectronSFrecoToLoose(float _pt, float eta, int var = 0){
	float pt = std::min(float(499.9), _pt); //protection
	if(pt<20){
		Int_t binx = (h_elSF_recoToLoose_lowPt->GetXaxis())->FindBin(eta);
		Int_t biny = (h_elSF_recoToLoose_lowPt->GetYaxis())->FindBin(pt);
		if(var>0) return (h_elSF_recoToLoose_lowPt->GetBinContent(binx, biny) + 0.01);
		if(var<0) return (h_elSF_recoToLoose_lowPt->GetBinContent(binx, biny) - 0.01);
		return  h_elSF_recoToLoose_lowPt->GetBinContent(binx, biny);
	}
	else {
		Int_t binx = (h_elSF_recoToLoose_highPt->GetXaxis())->FindBin(eta);
		Int_t biny = (h_elSF_recoToLoose_highPt->GetYaxis())->FindBin(pt);
		if(var>0) return (h_elSF_recoToLoose_highPt->GetBinContent(binx, biny) + 0.01);
		if(var<0) return (h_elSF_recoToLoose_highPt->GetBinContent(binx, biny) - 0.01);
		return  h_elSF_recoToLoose_highPt->GetBinContent(binx, biny);
	}
}

float getElectronSFlooseToTight(float _pt, float eta, int var = 0){
	// update this!
	float pt = std::min(float(30.0), _pt); //protection
	
	if(abs(eta)<1.479){
		if(var>0) return (h_elSF_looseToTight_barrel->Eval(pt) + h_elSF_looseToTight_barrel->GetErrorYhigh(getBinElectronLoose(pt))) ;
		if(var<0) return (h_elSF_looseToTight_barrel->Eval(pt) - h_elSF_looseToTight_barrel->GetErrorYlow (getBinElectronLoose(pt))) ;
		return  h_elSF_looseToTight_barrel->Eval(pt);
	}
	else {
		if(var>0) return (h_elSF_looseToTight_endcap->Eval(pt) + h_elSF_looseToTight_endcap->GetErrorYhigh(getBinElectronLoose(pt))) ;
		if(var<0) return (h_elSF_looseToTight_endcap->Eval(pt) - h_elSF_looseToTight_endcap->GetErrorYlow (getBinElectronLoose(pt))) ;
		return h_elSF_looseToTight_endcap->Eval(pt);
	}
}

float getElectronSF(float pt, float eta, int var = 0){
	return getElectronSFrecoToLoose(pt, eta, var)*getElectronSFlooseToTight(pt, eta, var);
}




// muons
TFile* f_muSF_recoToLoose_lowPt        = new TFile(DATA_SF+"/sos_lepton_SF_2017/mu_tracking_lowpt.root" ,"read");
TFile* f_muSF_recoToLoose_highPt       = new TFile(DATA_SF+"/sos_lepton_SF_2017/mu_tracking_highpt.root","read");
TFile* f_muSF_id_lowPt                 = new TFile(DATA_SF+"/sos_lepton_SF_2017/mu_id_lowpt.root"       ,"read");
TFile* f_muSF_id_highPt                = new TFile(DATA_SF+"/sos_lepton_SF_2017/mu_id_highpt.root"      ,"read");
TFile* f_muSF_looseToTight_barrel      = new TFile(DATA_SF+"/sos_lepton_SF_2017/mu_SOS_comb_barrel.root","read");
TFile* f_muSF_looseToTight_endcap      = new TFile(DATA_SF+"/sos_lepton_SF_2017/mu_SOS_comb_endcap.root","read");
TGraphAsymmErrors* h_muSF_recoToLoose_lowPt   = (TGraphAsymmErrors*) f_muSF_recoToLoose_lowPt ->Get("ratio_eff_eta3_tk0_dr030e030_corr");
TGraphAsymmErrors* h_muSF_recoToLoose_highPt  = (TGraphAsymmErrors*) f_muSF_recoToLoose_highPt->Get("ratio_eff_eta3_dr030e030_corr");
TH2F* h_muSF_id_lowPt                         = (TH2F*) f_muSF_id_lowPt ->Get("NUM_SoftID_DEN_genTracks_pt_abseta");
TH2F* h_muSF_id_highPt                        = (TH2F*) f_muSF_id_highPt->Get("NUM_SoftID_DEN_genTracks_pt_abseta");
TGraphAsymmErrors* h_muSF_looseToTight_barrel = (TGraphAsymmErrors*) f_muSF_looseToTight_barrel->Get("ratio");
TGraphAsymmErrors* h_muSF_looseToTight_endcap = (TGraphAsymmErrors*) f_muSF_looseToTight_endcap->Get("ratio");

int getBinMuonTracking(float eta){
	if     (               eta < -2.1) return 0;
	else if(eta >= -2.1 && eta < -1.6) return 1;
	else if(eta >= -1.6 && eta < -1.1) return 2;
	else if(eta >= -1.1 && eta < -0.9) return 3;
	else if(eta >= -0.9 && eta < -0.6) return 4;
	else if(eta >= -0.6 && eta < -0.3) return 5;
	else if(eta >= -0.3 && eta < -0.2) return 6;
	else if(eta >= -0.2 && eta <  0.2) return 7;
	else if(eta >=  0.2 && eta <  0.3) return 8;
	else if(eta >=  0.3 && eta <  0.6) return 9;
	else if(eta >=  0.6 && eta <  0.9) return 10;
	else if(eta >=  0.9 && eta <  1.1) return 11;
	else if(eta >=  1.1 && eta <  1.6) return 12;
	else if(eta >=  1.6 && eta <  2.1) return 13;
	else if(eta >=  2.1              ) return 14;
	else {
	  	assert(0);
	}
	return -1;
}

int getBinMuonTight(float pt){
    // to be updated!!
	if     (pt >  3.5 && pt <=  7.5) return 0;
	else if(pt >  7.5 && pt <= 10.0) return 1;
	else if(pt > 10.0 && pt <= 15.0) return 2;
	else if(pt > 15.0 && pt <= 20.0) return 3;
	else if(pt > 20.0              ) return 4;
	else {
	  	assert(0);
	}
}

float getMuonSFtracking(float pt, float eta, int var = 0){
	if(pt<10){
		if(var>0) return (h_muSF_recoToLoose_lowPt->Eval(eta) + h_muSF_recoToLoose_lowPt->GetErrorYhigh(getBinMuonTracking(eta))) ;
		if(var<0) return (h_muSF_recoToLoose_lowPt->Eval(eta) - h_muSF_recoToLoose_lowPt->GetErrorYlow (getBinMuonTracking(eta))) ;
		return h_muSF_recoToLoose_lowPt->Eval(eta)
	}
	if(pt>10){
		if(var>0) return (h_muSF_recoToLoose_highPt->Eval(eta) + h_muSF_recoToLoose_highPt->GetErrorYhigh(getBinMuonTracking(eta))) ;
		if(var<0) return (h_muSF_recoToLoose_highPt->Eval(eta) - h_muSF_recoToLoose_higePt->GetErrorYlow (getBinMuonTracking(eta))) ;
		return h_muSF_recoToLoose_highPt->Eval(eta)
	}
	assert(0);
	return -999;
}


float getMuonSFrecoToLoose(float _pt, float eta, int var = 0){
	float pt = std::min(float(119.9),_pt);
	if (pt<15) {
		Int_t binx = (h_muSF_id_lowPt->GetXaxis())->FindBin(pt);
		Int_t biny = (h_muSF_id_lowPt->GetYaxis())->FindBin(abs(eta));
		if(var>0) return (h_muSF_id_lowPt->GetBinContent(binx, biny) + 0.01);
		if(var<0) return (h_muSF_id_lowPt->GetBinContent(binx, biny) - 0.01);
		return  h_muSF_id_lowPt->GetBinContent(binx, biny);
	}	
	else {
		Int_t binx = (h_muSF_id_highPt->GetXaxis())->FindBin(pt);
		Int_t biny = (h_muSF_id_highPt->GetYaxis())->FindBin(abs(eta));
		if(var>0) return (h_muSF_id_highPt->GetBinContent(binx, biny) + 0.01);
		if(var<0) return (h_muSF_id_highPt->GetBinContent(binx, biny) - 0.01);
		return  h_muSF_id_highPt->GetBinContent(binx, biny);
	}	
	assert(0);
	return -999;
}


float getMuonSFlooseToTight(float _pt, float eta, int var = 0){
	// update this!
	float pt = std::min(float(59.9),_pt); // protection
	if(abs(eta)<1.2){
		if(var>0) return (h_muSF_looseToTight_barrel->Eval(pt) + h_muSF_looseToTight_barrel->GetErrorYhigh(getBinMuonTight(pt))) ;
		if(var<0) return (h_muSF_looseToTight_barrel->Eval(pt) - h_muSF_looseToTight_barrel->GetErrorYlow (getBinMuonTight(pt))) ;
		return h_muSF_looseToTight_barrel->Eval(pt);
	}
	if(abs(eta)>1.2){
		if(var>0) return (h_muSF_looseToTight_endcap->Eval(pt) + h_muSF_looseToTight_endcap->GetErrorYhigh(getBinMuonTight(pt))) ;
		if(var<0) return (h_muSF_looseToTight_endcap->Eval(pt) - h_muSF_looseToTight_endcap->GetErrorYlow (getBinMuonTight(pt))) ;
		return h_muSF_looseToTight_endcap->Eval(pt);
	}
	assert(0);
	return -999;
}


float getMuonSF(float pt, float eta, int var = 0){
	return getMuonSFtracking(pt, eta, var)*getMuonSFrecoToLoose(pt, eta, var)*getMuonSFlooseToTight(pt, eta, var);
}


// leptons
float getLepSF(float pt, float eta, int pdgId, int var = 0){
	if(abs(pdgId)==11) return getElectronSF(pt, eta, var);
	return getMuonSF(pt, eta, var);
}


float leptonSF(float lepSF1, float lepSF2, float lepSF3 = 1, float lepSF4 = 1){
    return lepSF1*lepSF2*lepSF3*lepSF4;
}





//// LEPTON SCALE FACTORS FASTSIM
//// -------------------------------------------------------------
//
//// electrons
//TFile* f_elSF_FS = new TFile(DATA_SF+"/sos_lepton_SF/fastsim/sf_el_SOS.root", "read");
//TH2F* h_elSF_FS  = (TH2F*) f_elSF_FS->Get("histo2D");
//
//// muons
//TFile* f_muSF_FS = new TFile(DATA_SF+"/sos_lepton_SF/fastsim/sf_mu_SOS.root", "read");
//TH2F* h_muSF_FS  = (TH2F*) f_muSF_FS->Get("histo2D");
//
//
//float getElectronSFFS(float pt, float eta){
//    return getSF(h_elSF_FS, pt, abs(eta));
//}
//
//float getElectronUncFS(int var = 0){
//	return 0.02;
//}
//
//float getMuonSFFS(float pt, float eta){
//	if(pt<5) return 1.0;
//    return getSF(h_muSF_FS, pt, abs(eta));
//}
//
//float getMuonUncFS(float pt, int var = 0) {
//	return 0.02;
//}
//
//float getLepSFFS(float pt, float eta, int pdgId, int var = 0){
//    float sf  = 1.0; 
//    float err = 0.0;
//    if(abs(pdgId) == 11) { sf = getElectronSFFS(pt, eta); err = sf*getElectronUncFS(var); } // relative uncertainty
//    if(abs(pdgId) == 13) { sf = getMuonSFFS    (pt, eta); err = sf*getMuonUncFS    (var); } // relative uncertainty
//    return (var==0)?sf:(sf+var*err)/sf;
//}
//
//float leptonSFFS(float lepSF1, float lepSF2, float lepSF3 = 1.0, float lepSF4 = 1.0){
//    return lepSF1*lepSF2*lepSF3*lepSF4;
//}


void functionsSF17() {}
