#include "TH2F.h"
#include "TMath.h"
#include "TGraphAsymmErrors.h"
#include "TFile.h"
#include "TSystem.h"
#include <iostream>
#include <unordered_map>

using namespace std;

TString CMSSW_BASE_SF = gSystem->ExpandPathName("${CMSSW_BASE}");
TString DATA_SF = CMSSW_BASE_SF+"/src/CMGTools/TTHAnalysis/data/susySosSF";

int lepton_permut(int pdgId1, int pdgId2, int pdgId3){
  if 		(abs(pdgId1)==13 && abs(pdgId2)==13 && abs(pdgId3)!=13)	return 12; // if lep1 = muon and lep2 = muon and lep3 = not muon
  else if 	(abs(pdgId2)==13 && abs(pdgId3)==13 && abs(pdgId1)!=13)	return 23; // if lep2 = muon and lep3 = muon and lep1 = not muon
  else if 	(abs(pdgId1)==13 && abs(pdgId3)==13 && abs(pdgId2)!=13)	return 13; // if lep1 = muon and lep3 = muon and lep2 = not muon
  else if	(abs(pdgId1)==13 && abs(pdgId3)==13 && abs(pdgId2)==13)	return 123;// if lep1 = muon and lep2 = muon and lep3 = muon
  else		return 0;
} 


// TRIGGER SCALE FACTORS
// -------------------------------------------------------------

TFile* f_trigSF = new TFile(DATA_SF+"/TriggerSF/triggereffcy_dimu3met50.root","read");

// Histo maps
unordered_map<int, TH2F*> h_trigEff_mumuMET_muleg_Data = {
	{ 2018, (TH2F*) f_trigSF->Get("dimu3met50_muleg_2018_Data") },
	{ 2017, (TH2F*) f_trigSF->Get("dimu3met50_muleg_2017_Data") },
	{ 2016, (TH2F*) f_trigSF->Get("dimu3met50_muleg_2016_Data") }
};
unordered_map<int, TH2F*> h_trigEff_mumuMET_muleg_MC = {
	{ 2018, (TH2F*) f_trigSF->Get("dimu3met50_muleg_2018_MC") },
	{ 2017, (TH2F*) f_trigSF->Get("dimu3met50_muleg_2017_MC") },
	{ 2016, (TH2F*) f_trigSF->Get("dimu3met50_muleg_2016_MC") }
};
unordered_map<int, TH2F*> h_trigEff_mumuMET_metleg_Data = {
	{ 2018, (TH2F*) f_trigSF->Get("dimu3met50_metleg_2018_Data") },
	{ 2017, (TH2F*) f_trigSF->Get("dimu3met50_metleg_2017_Data") },
	{ 2016, (TH2F*) f_trigSF->Get("dimu3met50_metleg_2016_Data") }
};
unordered_map<int, TH2F*> h_trigEff_mumuMET_metleg_MC = {
	{ 2018, (TH2F*) f_trigSF->Get("dimu3met50_metleg_2018_MC") },
	{ 2017, (TH2F*) f_trigSF->Get("dimu3met50_metleg_2017_MC") },
	{ 2016, (TH2F*) f_trigSF->Get("dimu3met50_metleg_2016_MC") }
};
TH2F* h_trigEff_mumuMET_dca16_Data = (TH2F*) f_trigSF->Get("dimu3met50_dca_2016_Data");
TH2F* h_trigEff_mumuMET_dca16_MC = (TH2F*) f_trigSF->Get("dimu3met50_dcaleg_2016_MC");

// Numerical maps
float mass_Data = 1.00, mass_MC = 1.00;
unordered_map<int, float> dcaDz_Data = {
	{ 2018, 0.998 },
	{ 2017, 0.995 },
	{ 2016, 0.907 }
};
unordered_map<int, float> dcaDz_MC = {
	{ 2018, 0.999 },
	{ 2017, 0.990 },
	{ 2016, 0.966 }
};
unordered_map<int, float> epsilonInf_Data = {
	{ 2018, 0.979 },
	{ 2017, 0.984 },
	{ 2016, 0.973 }
};
unordered_map<int, float> epsilonInf_MC = {
	{ 2018, 0.981 },
	{ 2017, 0.983 },
	{ 2016, 0.972 }
};
unordered_map<int, float> mean_Data = {
	{ 2018, 169.660 },
	{ 2017, 165.982 },
	{ 2016, 142.266 }
};
unordered_map<int, float> mean_MC = {
	{ 2018, 154.271 },
	{ 2017, 146.144 },
	{ 2016, 118.905 }
};
unordered_map<int, float> sigma_Data = {
	{ 2018, 63.147 },
	{ 2017, 65.089 },
	{ 2016, 77.482 }
};
unordered_map<int, float> sigma_MC = {
	{ 2018, 59.513 },
	{ 2017, 67.424 },
	{ 2016, 84.284 }
};


// TFormula bug => Functions cannot have more than 9 arguments => Factorize SF computation by using functions
float dcaDzleg_Data(int year, float _eta1, float _eta2){
	
	// Definitions and Protection
	float d_Data;
	float etaMax = max(_eta1,_eta2);
	float etaMin = min(_eta1,_eta2);
	float maxBin = h_trigEff_mumuMET_dca16_Data->GetXaxis()->FindBin(etaMax);
	float minBin = h_trigEff_mumuMET_dca16_Data->GetYaxis()->FindBin(etaMin);

	if(year==2016 &&  (maxBin - minBin) < 5){
		d_Data = h_trigEff_mumuMET_dca16_Data->GetBinContent(maxBin, minBin);
	}
	else d_Data = dcaDz_Data[year];

	return d_Data;
}
float dcaDzleg_MC(int year, float _eta1, float _eta2){
	
	// Definitions and Protection
	float d_MC;
	float etaMax = max(_eta1,_eta2);
	float etaMin = min(_eta1,_eta2);
	float maxBin = h_trigEff_mumuMET_dca16_MC->GetXaxis()->FindBin(etaMax);
	float minBin = h_trigEff_mumuMET_dca16_MC->GetYaxis()->FindBin(etaMin);

	if(year==2016 &&  (maxBin - minBin) < 5){
		d_MC = h_trigEff_mumuMET_dca16_MC->GetBinContent(maxBin, minBin);
	}
	else d_MC = dcaDz_MC[year];

	return d_MC;
}


// d factors also include the mass efficiency. Since this efficiency is 1.0, it is omitted.
float muDleg_SF(int year, float _pt1, float _eta1, float _pt2, float _eta2, float _pt3 = -100.0, float _eta3 = -100.0, int choose_leptons = 12){ // "choose_leptons" determines 2l or 3l case
	
	// Definitions and Protection
	float mu1_Data, mu1_MC, mu2_Data, mu2_MC, mu3_Data, mu3_MC;
	float d12_Data, d12_MC, d13_Data, d13_MC, d23_Data, d23_MC;
	float SF;
	float pt1 = max(float(3.501), min(float(499.999), _pt1));
	float pt2 = max(float(3.501), min(float(499.999), _pt2));
	float pt3 = max(float(3.501), min(float(499.999), _pt3));
	float eta1	= min(float(2.399), abs(_eta1)); // eta -> Absolute eta
	float eta2	= min(float(2.399), abs(_eta2)); // eta -> Absolute eta
	float eta3	= min(float(2.399), abs(_eta3)); // eta -> Absolute eta
	
	// First 2 muon efficiency
	mu1_Data	= h_trigEff_mumuMET_muleg_Data[year]->GetBinContent(h_trigEff_mumuMET_muleg_Data[year]->GetXaxis()->FindBin(pt1), h_trigEff_mumuMET_muleg_Data[year]->GetYaxis()->FindBin(eta1));
	mu1_MC		= h_trigEff_mumuMET_muleg_MC[year]->GetBinContent(h_trigEff_mumuMET_muleg_MC[year]->GetXaxis()->FindBin(pt1), h_trigEff_mumuMET_muleg_MC[year]->GetYaxis()->FindBin(eta1));
	mu2_Data	= h_trigEff_mumuMET_muleg_Data[year]->GetBinContent(h_trigEff_mumuMET_muleg_Data[year]->GetXaxis()->FindBin(pt2), h_trigEff_mumuMET_muleg_Data[year]->GetYaxis()->FindBin(eta2));
	mu2_MC		= h_trigEff_mumuMET_muleg_MC[year]->GetBinContent(h_trigEff_mumuMET_muleg_MC[year]->GetXaxis()->FindBin(pt2), h_trigEff_mumuMET_muleg_MC[year]->GetYaxis()->FindBin(eta2));
	if(mu1_Data==0) {mu1_Data=1.0;}; if(mu1_MC==0) {mu1_MC=1.0;}; if(mu2_Data==0) {mu2_Data=1.0;}; if(mu2_MC==0) {mu2_MC=1.0;}; //Fix empty bins in histos
	if(year == 2016){ //Eliminate the DCA efficiency within the muleg
		mu1_Data /= dcaDz_Data[year]; mu2_Data /= dcaDz_Data[year];
		mu1_MC /= dcaDz_MC[year]; mu2_MC /= dcaDz_MC[year];
		if(mu1_Data>1.0) {mu1_Data=1.0;}; if(mu1_MC>1.0) {mu1_MC=1.0;}; if(mu2_Data>1.0) {mu2_Data=1.0;}; if(mu2_MC>1.0) {mu2_MC=1.0;}; //Fix upward stat. fluctuations in maps leading to eff > 1
	}

	if(choose_leptons==12){
		d12_Data = dcaDzleg_Data(year, _eta1, _eta2);
		d12_MC = dcaDzleg_MC(year, _eta1, _eta2);
		SF = (mu1_MC*mu2_MC*d12_MC == 0.0) ? 0.0 : (mu1_Data*mu2_Data*d12_Data) / (mu1_MC*mu2_MC*d12_MC);
	}
	else{
		// Third muon efficiency
		mu3_Data = h_trigEff_mumuMET_muleg_Data[year]->GetBinContent(h_trigEff_mumuMET_muleg_Data[year]->GetXaxis()->FindBin(pt3), h_trigEff_mumuMET_muleg_Data[year]->GetYaxis()->FindBin(eta3));
		mu3_MC = h_trigEff_mumuMET_muleg_MC[year]->GetBinContent(h_trigEff_mumuMET_muleg_MC[year]->GetXaxis()->FindBin(pt3), h_trigEff_mumuMET_muleg_MC[year]->GetYaxis()->FindBin(eta3));
		if(mu3_Data==0) {mu3_Data=1.0;}; if(mu3_MC==0) {mu3_MC=1.0;}; //Fix empty bins in histos
		if(year == 2016){ //Eliminate the DCA efficiency within the muleg
			mu3_Data /= dcaDz_Data[year];
			mu3_MC /= dcaDz_MC[year];
			if(mu3_Data>1.0) {mu3_Data=1.0;}; if(mu3_MC>1.0) {mu3_MC=1.0;}; //Fix upward stat. fluctuations in maps leading to eff > 1
		}

		if(choose_leptons==13){
			d13_Data = dcaDzleg_Data(year, _eta1, _eta3);
			d13_MC = dcaDzleg_MC(year, _eta1, _eta3);
			SF = (mu1_MC*mu3_MC*d13_MC == 0.0) ? 0.0 : (mu1_Data*mu3_Data*d13_Data) / (mu1_MC*mu3_MC*d13_MC);
		}
		else if(choose_leptons==23){
			d23_Data = dcaDzleg_Data(year, _eta2, _eta3);
			d23_MC = dcaDzleg_MC(year, _eta2, _eta3);
			SF = (mu2_MC*mu3_MC*d23_MC == 0.0) ? 0.0 : (mu2_Data*mu3_Data*d23_Data) / (mu2_MC*mu3_MC*d23_MC);
		}
		else if(choose_leptons==123){
			d12_Data = dcaDzleg_Data(year, _eta1, _eta2);	d13_Data = dcaDzleg_Data(year, _eta1, _eta3);	d23_Data = dcaDzleg_Data(year, _eta2, _eta3);
			d12_MC = dcaDzleg_MC(year, _eta1, _eta2);		d13_MC = dcaDzleg_MC(year, _eta1, _eta3);		d23_MC = dcaDzleg_MC(year, _eta2, _eta3);

			float ProbAnyPairFired_Data = mu1_Data*mu2_Data*d12_Data + mu1_Data*mu3_Data*d13_Data + mu2_Data*mu3_Data*d23_Data - mu1_Data*mu2_Data*mu3_Data * (d12_Data*d13_Data + d12_Data*d23_Data + d13_Data*d23_Data - d12_Data*d13_Data*d23_Data);
			float ProbAnyPairFired_MC = mu1_MC*mu2_MC*d12_MC + mu1_MC*mu3_MC*d13_MC + mu2_MC*mu3_MC*d23_MC - mu1_MC*mu2_MC*mu3_MC * (d12_MC*d13_MC + d12_MC*d23_MC + d13_MC*d23_MC - d12_MC*d13_MC*d23_MC);

			SF = (ProbAnyPairFired_MC == 0.0) ? 0.0 : ProbAnyPairFired_Data / ProbAnyPairFired_MC;
		}
		else{ // Only electrons in the low MET bin
			SF = 0.0;
		}
	}

	return SF;
}

float muDleg_MCEff(int year, float _pt1, float _eta1, float _pt2, float _eta2, float _pt3 = -100.0, float _eta3 = -100.0, int choose_leptons = 12){ // "choose_leptons" determines 2l or 3l case
	
	// Definitions and Protection
	float mu1_MC, mu2_MC, mu3_MC;
	float d12_MC, d13_MC, d23_MC;
	float MCEff;
	float pt1 = max(float(3.501), min(float(499.999), _pt1));
	float pt2 = max(float(3.501), min(float(499.999), _pt2));
	float pt3 = max(float(3.501), min(float(499.999), _pt3));
	float eta1	= min(float(2.399), abs(_eta1)); // eta -> Absolute eta
	float eta2	= min(float(2.399), abs(_eta2)); // eta -> Absolute eta
	float eta3	= min(float(2.399), abs(_eta3)); // eta -> Absolute eta
	
	// First 2 muon efficiency
	mu1_MC	= h_trigEff_mumuMET_muleg_MC[year]->GetBinContent(h_trigEff_mumuMET_muleg_MC[year]->GetXaxis()->FindBin(pt1), h_trigEff_mumuMET_muleg_MC[year]->GetYaxis()->FindBin(eta1));
	mu2_MC	= h_trigEff_mumuMET_muleg_MC[year]->GetBinContent(h_trigEff_mumuMET_muleg_MC[year]->GetXaxis()->FindBin(pt2), h_trigEff_mumuMET_muleg_MC[year]->GetYaxis()->FindBin(eta2));
	if(mu1_MC==0) {mu1_MC=1.0;}; if(mu2_MC==0) {mu2_MC=1.0;}; //Fix empty bins in histos
	if(year == 2016){ //Eliminate the DCA efficiency within the muleg
		mu1_MC /= dcaDz_MC[year]; mu2_MC /= dcaDz_MC[year];
		if(mu1_MC>1.0) {mu1_MC=1.0;}; if(mu2_MC>1.0) {mu2_MC=1.0;}; //Fix upward stat. fluctuations in maps leading to eff > 1
	}

	if(choose_leptons==12){
		d12_MC = dcaDzleg_MC(year, _eta1, _eta2);
		MCEff = (mu1_MC*mu2_MC*d12_MC);
	}
	else{
		// Third muon efficiency
		mu3_MC = h_trigEff_mumuMET_muleg_MC[year]->GetBinContent(h_trigEff_mumuMET_muleg_MC[year]->GetXaxis()->FindBin(pt3), h_trigEff_mumuMET_muleg_MC[year]->GetYaxis()->FindBin(eta3));
		if(mu3_MC==0) {mu3_MC=1.0;}; //Fix empty bins in histos
		if(year == 2016){ //Eliminate the DCA efficiency within the muleg
			mu3_MC /= dcaDz_MC[year];
			if(mu3_MC>1.0) {mu3_MC=1.0;}; //Fix upward stat. fluctuations in maps leading to eff > 1
		}

		if(choose_leptons==13){
			d13_MC = dcaDzleg_MC(year, _eta1, _eta3);
			MCEff = (mu1_MC*mu3_MC*d13_MC);
		}
		else if(choose_leptons==23){
			d23_MC = dcaDzleg_MC(year, _eta2, _eta3);
			MCEff = (mu2_MC*mu3_MC*d23_MC);
		}
		else if(choose_leptons==123){
			d12_MC = dcaDzleg_MC(year, _eta1, _eta2);	d13_MC = dcaDzleg_MC(year, _eta1, _eta3);	d23_MC = dcaDzleg_MC(year, _eta2, _eta3);
			float ProbAnyPairFired_MC = mu1_MC*mu2_MC*d12_MC + mu1_MC*mu3_MC*d13_MC + mu2_MC*mu3_MC*d23_MC - mu1_MC*mu2_MC*mu3_MC * (d12_MC*d13_MC + d12_MC*d23_MC + d13_MC*d23_MC - d12_MC*d13_MC*d23_MC);

			MCEff = ProbAnyPairFired_MC;
		}
		else{ // Only electrons in the low MET bin
			MCEff = 0.0;
		}
	}

	return MCEff;
}


// Fullsim
float triggerSF(float muDleg_SF, float _met, float _met_corr, int year){

	// Definitions and Protection
	float eff_Data, eff_MC, SF;
	float met      = max(float(50.1) , min(float(499.999), _met));
	float met_corr = max(float(50.1) , min(float(499.999), _met_corr));

	// High MET triggers
	if(met_corr>=200.0){
		eff_Data	= 0.5 * epsilonInf_Data[year] * ( TMath::Erf( (met_corr - mean_Data[year]) / sigma_Data[year] ) + 1 );
		eff_MC		= 0.5 * epsilonInf_MC[year] * ( TMath::Erf( (met_corr - mean_MC[year]) / sigma_MC[year] ) + 1 );
		SF			= (eff_MC == 0.0) ? 0.0 : eff_Data / eff_MC;
	}
	// Low MET triggers
	else{
		// Mu + Dca/Dz legs computed in muDleg_SF function
		// Met leg
		float met_Data	= h_trigEff_mumuMET_metleg_Data[year]->GetBinContent(h_trigEff_mumuMET_metleg_Data[year]->GetXaxis() ->FindBin(met), h_trigEff_mumuMET_metleg_Data[year]->GetYaxis()->FindBin(met_corr));
		float met_MC	= h_trigEff_mumuMET_metleg_MC[year]->GetBinContent(h_trigEff_mumuMET_metleg_MC[year]->GetXaxis() ->FindBin(met), h_trigEff_mumuMET_metleg_MC[year]->GetYaxis()->FindBin(met_corr));
		if(met_Data==0) {met_Data=1.0;}; if(met_MC==0) {met_MC=1.0;} //Fix empty bins in histos

		// Putting everything together
		eff_Data	= mass_Data * met_Data;
		eff_MC		= mass_MC * met_MC;
		SF = (eff_MC == 0.0) ? 0.0 : muDleg_SF * eff_Data / eff_MC;
	}

	if(SF<=0.0){
		//cout << "=====================================" << endl;
		//cout << "||             SF <= 0             ||" << endl;
		//cout << "||    THIS SHOULD NEVER HAPPEN!    ||" << endl;
		//cout << "||     Setting SF to 1 for now     ||" << endl;
		//cout << "=====================================" << endl;
		SF = 1.0;
	}
	return SF; 
}

float triggerWZSF(float muDleg_SF, float _met, float _met_corr, int year){
	return 1.0;
}


// Fastsim: MCEff to multiply fastsim samples so that SF * MCEff = DataEff
float triggerMCEff(float muDleg_MCEff, float _met, float _met_corr, int year){

	// Definitions and Protection
	float MCEff;
	float met      = max(float(50.1) , min(float(499.999), _met));
	float met_corr = max(float(50.1) , min(float(499.999), _met_corr));

	// High MET triggers
	if(met_corr>=200.0) MCEff	= 0.5 * epsilonInf_MC[year] * ( TMath::Erf( (met_corr - mean_MC[year]) / sigma_MC[year] ) + 1 );
	// Low MET triggers
	else{
		// Mu + Dca/Dz legs computed in muDleg_MCEff function
		// Met leg
		float met_MC	= h_trigEff_mumuMET_metleg_MC[year]->GetBinContent(h_trigEff_mumuMET_metleg_MC[year]->GetXaxis() ->FindBin(met), h_trigEff_mumuMET_metleg_MC[year]->GetYaxis()->FindBin(met_corr));
		if(met_MC==0) {met_MC=1.0;} //Fix empty bins in histos

		// Putting everything together
		MCEff	= muDleg_MCEff * mass_MC * met_MC;
	}

	if(MCEff<=0.0){
		//cout << "=====================================" << endl;
		//cout << "||           MC eff <= 0           ||" << endl;
		//cout << "||    THIS SHOULD NEVER HAPPEN!    ||" << endl;
		//cout << "||   Setting MC eff to 1 for now   ||" << endl;
		//cout << "=====================================" << endl;
		MCEff = 1.0;
	}
	return MCEff; 
}

float triggerWZMCEff(float muDleg_MCEff, float _met, float _met_corr, int year){
	return 1.0;
}


// LEPTON SCALE FACTORS
// -------------------------------------------------------------

// Electron Reconstruction SF
TFile* f_recoSF_Electron_2018 = new TFile(DATA_SF+"/LeptonSF/Electron2018_RecoSFMap.root","read");
TFile* f_recoSFHighPt_Electron_2017 = new TFile(DATA_SF+"/LeptonSF/Electron2017_RecoHighPtSFMap.root","read");
TFile* f_recoSFLowPt_Electron_2017 = new TFile(DATA_SF+"/LeptonSF/Electron2017_RecoLowPtSFMap.root","read");
TFile* f_recoSFHighPt_Electron_2016 = new TFile(DATA_SF+"/LeptonSF/Electron2016_RecoHighPtSFMap.root","read");
TFile* f_recoSFLowPt_Electron_2016 = new TFile(DATA_SF+"/LeptonSF/Electron2016_RecoLowPtSFMap.root","read");

unordered_map<string, TH2F*> h_recoSF_Electron_SF = {
	{ "2018",		(TH2F*) f_recoSF_Electron_2018->Get("EGamma_SF2D") },
	{ "2017High",	(TH2F*) f_recoSFHighPt_Electron_2017->Get("EGamma_SF2D") },
	{ "2017Low",	(TH2F*) f_recoSFLowPt_Electron_2017->Get("EGamma_SF2D") },
	{ "2016High",	(TH2F*) f_recoSFHighPt_Electron_2016->Get("EGamma_SF2D") },
	{ "2016Low",	(TH2F*) f_recoSFLowPt_Electron_2016->Get("EGamma_SF2D") }
};

// To be revised
//unordered_map<string, TH2F*> h_recoSF_Electron_MCEff = {
//	{ "2018",		(TH2F*) f_recoSF_Electron_2018->Get("EGamma_EffMC2D") },
//	{ "2017High",	(TH2F*) f_recoSFHighPt_Electron_2017->Get("EGamma_EffMC2D") },
//	{ "2017Low",	(TH2F*) f_recoSFLowPt_Electron_2017->Get("EGamma_EffMC2D") },
//	{ "2016High",	(TH2F*) f_recoSFHighPt_Electron_2016->Get("EGamma_EffMC2D") },
//	{ "2016Low",	(TH2F*) f_recoSFLowPt_Electron_2016->Get("EGamma_EffMC2D") }
//};

// Muon Tracking SF = 1.0 (Muon POG)
// Muon Loose ID SF
TFile* f_looseIDSF_Muon_2018 = new TFile(DATA_SF+"/LeptonSF/Muon2018_LooseIDSFMap.root","read");
TFile* f_looseIDSF_Muon_2017 = new TFile(DATA_SF+"/LeptonSF/Muon2017_LooseIDSFMap.root","read");
TFile* f_looseIDSF_Muon_2016 = new TFile(DATA_SF+"/LeptonSF/Muon2016_LooseIDSFMap.root","read"); // ErasBCDEF

unordered_map<int, TH2D*> h_looseIDSF_Muon_SF = {
	{ 2018, (TH2D*) f_looseIDSF_Muon_2018->Get("NUM_LooseID_DEN_genTracks_pt_abseta") },
	{ 2017, (TH2D*) f_looseIDSF_Muon_2017->Get("NUM_LooseID_DEN_genTracks_pt_abseta") },
	{ 2016, (TH2D*) f_looseIDSF_Muon_2016->Get("NUM_LooseID_DEN_genTracks_pt_abseta") } // ErasBCDEF
};

// To be revised
// Muon Loose ID SF for 2016ErasGH missing (even from POG) --> Small correction 
// Muon Loose ID MCEff missing (even from POG in 2016)

// SOS Tight ID SF
TFile* f_lepSF_Electron_2018 = new TFile(DATA_SF+"/LeptonSF/Electron2018_LeptonSFMap.root","read");
TFile* f_lepSF_Electron_2017 = new TFile(DATA_SF+"/LeptonSF/Electron2017_LeptonSFMap.root","read");
TFile* f_lepSF_Electron_2016 = new TFile(DATA_SF+"/LeptonSF/Electron2016_LeptonSFMap.root","read");
TFile* f_lepSF_Muon_2018 = new TFile(DATA_SF+"/LeptonSF/Muon2018_LeptonSFMap.root","read");
TFile* f_lepSF_Muon_2017 = new TFile(DATA_SF+"/LeptonSF/Muon2017_LeptonSFMap.root","read");
TFile* f_lepSF_Muon_2016 = new TFile(DATA_SF+"/LeptonSF/Muon2016_LeptonSFMap.root","read");

unordered_map<int, TH2F*> h_lepSF_Electron_SF = {
	{ 2018, (TH2F*) f_lepSF_Electron_2018->Get("EGamma_SF2D") },
	{ 2017, (TH2F*) f_lepSF_Electron_2017->Get("EGamma_SF2D") },
	{ 2016, (TH2F*) f_lepSF_Electron_2016->Get("EGamma_SF2D") }
};
unordered_map<int, TH2F*> h_lepSF_Muon_SF = {
	{ 2018, (TH2F*) f_lepSF_Muon_2018->Get("EGamma_SF2D") },
	{ 2017, (TH2F*) f_lepSF_Muon_2017->Get("EGamma_SF2D") },
	{ 2016, (TH2F*) f_lepSF_Muon_2016->Get("EGamma_SF2D") }
};

// To be revised
//unordered_map<int, TH2F*> h_lepSF_Electron_MCEff = {
//	{ 2018, (TH2F*) f_lepSF_Electron_2018->Get("EGamma_EffMC2D") },
//	{ 2017, (TH2F*) f_lepSF_Electron_2017->Get("EGamma_EffMC2D") },
//	{ 2016, (TH2F*) f_lepSF_Electron_2016->Get("EGamma_EffMC2D") }
//};
//unordered_map<int, TH2F*> h_lepSF_Muon_MCEff = {
//	{ 2018, (TH2F*) f_lepSF_Muon_2018->Get("EGamma_EffMC2D") },
//	{ 2017, (TH2F*) f_lepSF_Muon_2017->Get("EGamma_EffMC2D") },
//	{ 2016, (TH2F*) f_lepSF_Muon_2016->Get("EGamma_EffMC2D") }
//};

// Fullsim
float lepSF_recoToTight(float _pt, float _eta, int pdgId, int year) {
	
	// Definitions
	float SF, pt, eta;

	if(abs(pdgId)==11) { // Electrons
		// Protection
		pt = max(float(5.001), min(float(999.999), _pt));
		eta = min(float(2.499), abs(_eta)); // eta -> Absolute eta

		SF = h_lepSF_Electron_SF[year]->GetBinContent(h_lepSF_Electron_SF[year]->GetXaxis()->FindBin(eta), h_lepSF_Electron_SF[year]->GetYaxis()->FindBin(pt));
	}
	else if(abs(pdgId)==13) { // Muons
		// Protection
		pt = max(float(3.501), min(float(999.999), _pt));
		eta = min(float(2.399), abs(_eta)); // eta -> Absolute eta

		SF = h_lepSF_Muon_SF[year]->GetBinContent(h_lepSF_Muon_SF[year]->GetXaxis()->FindBin(eta), h_lepSF_Muon_SF[year]->GetYaxis()->FindBin(pt));
	}
	else { // Other => We should never end up here.
		SF = 0.0;
	}
	
	if(SF<=0.0){
        //cout << "=====================================" << endl;
        //cout << "||             SF <= 0             ||" << endl;
        //cout << "||    THIS SHOULD NEVER HAPPEN!    ||" << endl;
        //cout << "||     Setting SF to 1 for now     ||" << endl;
        //cout << "=====================================" << endl;
        SF = 1.0;
    }
	return SF;
}

float lepSF_toReco(float _pt, float _eta, int pdgId, int year) {

	// Definitions
	float SF, pt, eta;
	string ptString, yearString;

	if(abs(pdgId)==11) { // Electrons
		// Protection
		pt = max(float(10.001), min(float(499.999), _pt));
		eta = max(float(-2.499), min(float(2.499), _eta));

		yearString = to_string(year);
		if(pt > 20.0) ptString = "High";
		else ptString = "Low";
		if(year!=2018) yearString = yearString+ptString;

		SF = h_recoSF_Electron_SF[yearString]->GetBinContent(h_recoSF_Electron_SF[yearString]->GetXaxis()->FindBin(eta), h_recoSF_Electron_SF[yearString]->GetYaxis()->FindBin(pt)); // reco
	}
	else if(abs(pdgId)==13) { // Muons
		// Protection
		pt = max(float(3.501), min(float(29.999), _pt)); // Use last bin to cover SFs in higher pT as well
		eta = min(float(2.399), abs(_eta)); // eta -> Absolute eta

		// tracking SF = 1.0 (Muon POG Recommendations)
		SF = h_looseIDSF_Muon_SF[year]->GetBinContent(h_looseIDSF_Muon_SF[year]->GetXaxis()->FindBin(pt), h_looseIDSF_Muon_SF[year]->GetYaxis()->FindBin(eta)); // loose ID
	}
	else { // Other => We should never end up here.
		SF = 0.0;
	}
	
	if(SF<=0.0){
        //cout << "=====================================" << endl;
        //cout << "||             SF <= 0             ||" << endl;
        //cout << "||    THIS SHOULD NEVER HAPPEN!    ||" << endl;
        //cout << "||     Setting SF to 1 for now     ||" << endl;
        //cout << "=====================================" << endl;
        SF = 1.0;
    }
	return SF;
}

float lepSF(float _pt, float _eta, int pdgId, int year) {
	return lepSF_toReco(_pt,_eta,pdgId,year) * lepSF_recoToTight(_pt,_eta,pdgId,year);
}


// Fastsim: MCEff to multiply fastsim samples so that SF * MCEff = DataEff
// To be revised
//float lepMCEff_recoToTight(float _pt, float _eta, int pdgId, int year) {
//	
//	// Definitions
//	float MCEff, pt, eta;
//
//	if(abs(pdgId)==11) { // Electrons
//		// Protection
//		pt = max(float(5.001), min(float(999.999), _pt));
//		eta = min(float(2.499), abs(_eta)); // eta -> Absolute eta
//
//		MCEff = h_lepSF_Electron_MCEff[year]->GetBinContent(h_lepSF_Electron_MCEff[year]->GetXaxis()->FindBin(eta), h_lepSF_Electron_MCEff[year]->GetYaxis()->FindBin(pt));
//	}
//	else if(abs(pdgId)==13) { // Muons
//		// Protection
//		pt = max(float(3.501), min(float(999.999), _pt));
//		eta = min(float(2.399), abs(_eta)); // eta -> Absolute eta
//
//		MCEff = h_lepSF_Muon_MCEff[year]->GetBinContent(h_lepSF_Muon_MCEff[year]->GetXaxis()->FindBin(eta), h_lepSF_Muon_MCEff[year]->GetYaxis()->FindBin(pt));
//	}
//	else { // Other => We should never end up here.
//		MCEff = 0.0;
//	}
//	
//	if(MCEff<=0.0){
//		//cout << "=====================================" << endl;
//		//cout << "||           MC eff <= 0           ||" << endl;
//		//cout << "||    THIS SHOULD NEVER HAPPEN!    ||" << endl;
//		//cout << "||   Setting MC eff to 1 for now   ||" << endl;
//		//cout << "=====================================" << endl;
//		MCEff = 1.0;
//	}
//	return MCEff; 
//}
//
//float lepMCEff_toReco(float _pt, float _eta, int pdgId, int year) {
//	
//	// Definitions
//	float MCEff, pt, eta;
//	string ptString, yearString;
//
//	if(abs(pdgId)==11) { // Electrons
//		// Protection
//		pt = max(float(10.001), min(float(499.999), _pt));
//		eta = max(float(-2.499), min(float(2.499), _eta));
//
//		yearString = to_string(year);
//		if(pt > 20.0) ptString = "High";
//		else ptString = "Low";
//		if(year!=2018) yearString = yearString+ptString;
//
//		MCEff = h_recoSF_Electron_MCEff[yearString]->GetBinContent(h_recoSF_Electron_MCEff[yearString]->GetXaxis()->FindBin(eta), h_recoSF_Electron_MCEff[yearString]->GetYaxis()->FindBin(pt)); // reco
//	}
//	else if(abs(pdgId)==13) { // Muons
//		// Protection
//		//pt = max(float(3.501), min(float(999.999), _pt));
//		//eta = min(float(2.399), abs(_eta)); // eta -> Absolute eta
//
//		// tracking SF = 1.0 (Muon POG Recommendations)
//		// MCEff missing for 2016 from the POG and 2017 and 2018 are left be implemented together with that
//		// MCEff = h_lepSF_Muon_MCEff[year]->GetBinContent(h_lepSF_Muon_MCEff[year]->GetXaxis()->FindBin(eta), h_lepSF_Muon_MCEff[year]->GetYaxis()->FindBin(pt)); // loose ID
//		MCEff = 1.0;
//	}
//	else { // Other => We should never end up here.
//		MCEff = 0.0;
//	}
//	
//	if(MCEff<=0.0){
//		//cout << "=====================================" << endl;
//		//cout << "||           MC eff <= 0           ||" << endl;
//		//cout << "||    THIS SHOULD NEVER HAPPEN!    ||" << endl;
//		//cout << "||   Setting MC eff to 1 for now   ||" << endl;
//		//cout << "=====================================" << endl;
//		MCEff = 1.0;
//	}
//	return MCEff; 
//}

float lepMCEff(float _pt, float _eta, int pdgId, int year) {
	// To be revised
	return 1.0; //lepMCEff_toReco(_pt,_eta,pdgId,year) * lepMCEff_recoToTight(_pt,_eta,pdgId,year);
}

void functionsSF() {}
