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

float getSF(TH2F* hist, float pt, float eta){
    int xbin = max(1, min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    int ybin = max(1, min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(eta)));
    return hist->GetBinContent(xbin,ybin);
}

float getUnc(TH2F* hist, float pt, float eta){
    int xbin = max(1, min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    int ybin = max(1, min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(eta)));
    return hist->GetBinError(xbin,ybin);
}

int lepton_permut(int pdgId1, int pdgId2, int pdgId3){
  if 		(abs(pdgId1)==13 && abs(pdgId2)==13 && abs(pdgId3)!=13)	return 12; // if lep1 = muon and lep2 = muon and lep3 = not muon
  else if 	(abs(pdgId2)==13 && abs(pdgId3)==13 && abs(pdgId1)!=13)	return 23; // if lep2 = muon and lep3 = muon and lep1 = not muon
  else if 	(abs(pdgId1)==13 && abs(pdgId3)==13 && abs(pdgId2)!=13)	return 13; // if lep1 = muon and lep3 = muon and lep2 = not muon
  else if	(abs(pdgId1)==13 && abs(pdgId3)==13 && abs(pdgId2)==13)	return 123;// if lep1 = muon and lep2 = muon and lep3 = muon
  else		return 0;
} 


// TRIGGER SCALE FACTORS
// -------------------------------------------------------------

TFile* f_trigSF_2l = new TFile(DATA_SF+"/TriggerSF/triggereffcy_dimu3met50.root","read");

// Histo maps
unordered_map<int, TH2F*> h_trigEff_mumuMET_muleg_Data = {
	{ 2018, (TH2F*) f_trigSF_2l->Get("dimu3met50_muleg_2018_Data") },
	{ 2017, (TH2F*) f_trigSF_2l->Get("dimu3met50_muleg_2017_Data") },
	{ 2016, (TH2F*) f_trigSF_2l->Get("dimu3met50_muleg_2016_Data") }
};
unordered_map<int, TH2F*> h_trigEff_mumuMET_muleg_MC = {
	{ 2018, (TH2F*) f_trigSF_2l->Get("dimu3met50_muleg_2018_MC") },
	{ 2017, (TH2F*) f_trigSF_2l->Get("dimu3met50_muleg_2017_MC") },
	{ 2016, (TH2F*) f_trigSF_2l->Get("dimu3met50_muleg_2016_MC") }
};
unordered_map<int, TH2F*> h_trigEff_mumuMET_metleg_Data = {
	{ 2018, (TH2F*) f_trigSF_2l->Get("dimu3met50_metleg_2018_Data") },
	{ 2017, (TH2F*) f_trigSF_2l->Get("dimu3met50_metleg_2017_Data") },
	{ 2016, (TH2F*) f_trigSF_2l->Get("dimu3met50_metleg_2016_Data") }
};
unordered_map<int, TH2F*> h_trigEff_mumuMET_metleg_MC = {
	{ 2018, (TH2F*) f_trigSF_2l->Get("dimu3met50_metleg_2018_MC") },
	{ 2017, (TH2F*) f_trigSF_2l->Get("dimu3met50_metleg_2017_MC") },
	{ 2016, (TH2F*) f_trigSF_2l->Get("dimu3met50_metleg_2016_MC") }
};
TH2F* h_trigEff_mumuMET_dca16_Data = (TH2F*) f_trigSF_2l->Get("dimu3met50_dca_2016_Data");
TH2F* h_trigEff_mumuMET_dca16_MC = (TH2F*) f_trigSF_2l->Get("dimu3met50_dcaleg_2016_MC");

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
		else{ // Only electrons in the low MET bin => We should never go here.
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
		else{ // Only electrons in the low MET bin => We should never go here.
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
		cout << "=====================================" << endl;
		cout << "||             SF <= 0             ||" << endl;
		cout << "||    THIS SHOULD NEVER HAPPEN!    ||" << endl;
		cout << "||     Setting SF to 1 for now     ||" << endl;
		cout << "=====================================" << endl;
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
		cout << "=====================================" << endl;
		cout << "||           MC eff <= 0           ||" << endl;
		cout << "||    THIS SHOULD NEVER HAPPEN!    ||" << endl;
		cout << "||   Setting MC eff to 1 for now   ||" << endl;
		cout << "=====================================" << endl;
		MCEff = 1.0;
	}
	return MCEff; 
}

float triggerWZMCEff(float muDleg_MCEff, float _met, float _met_corr, int year){
	return 1.0;
}


//// LEPTON SCALE FACTORS FULLSIM
//// -------------------------------------------------------------
//
//// electrons
//TFile* f_elSF_looseToTight_barrel_16      = new TFile(DATA_SF+"/sos_lepton_SF/el_SOS_barrel_36invfb.root", "read");
//TFile* f_elSF_looseToTight_endcap_16      = new TFile(DATA_SF+"/sos_lepton_SF/el_SOS_endcap_36invfb.root", "read");
//TGraphAsymmErrors* h_elSF_looseToTight_barrel_16      = (TGraphAsymmErrors*) f_elSF_looseToTight_barrel_16->Get("ratio");
//TGraphAsymmErrors* h_elSF_looseToTight_endcap_16      = (TGraphAsymmErrors*) f_elSF_looseToTight_endcap_16->Get("ratio");
//
//int getBinElectronLoose_16(float pt){
//	if     (pt >  5.0 && pt <= 12.5) return 0;
//	else if(pt > 12.5 && pt <= 16.0) return 1;
//	else if(pt > 16.0 && pt <= 20.0) return 2;
//	else if(pt > 20.0 && pt <= 25.0) return 3;
//	else if(pt > 25.0              ) return 4;
//	else {
//		assert(0);
//	}
//}
//
//float getElectronSFlooseToTight_16(float _pt, float eta, int var = 0){
//	float pt = std::min(float(30.0), _pt); //protection
//	
//	if(abs(eta)<1.479){
//		if(var>0) return (h_elSF_looseToTight_barrel_16->Eval(pt) + h_elSF_looseToTight_barrel_16->GetErrorYhigh(getBinElectronLoose_16(pt))) ;
//		if(var<0) return (h_elSF_looseToTight_barrel_16->Eval(pt) - h_elSF_looseToTight_barrel_16->GetErrorYlow (getBinElectronLoose_16(pt))) ;
//		return  h_elSF_looseToTight_barrel_16->Eval(pt);
//	}
//
//	if(var>0) return (h_elSF_looseToTight_endcap_16->Eval(pt) + h_elSF_looseToTight_endcap_16->GetErrorYhigh(getBinElectronLoose_16(pt))) ;
//	if(var<0) return (h_elSF_looseToTight_endcap_16->Eval(pt) - h_elSF_looseToTight_endcap_16->GetErrorYlow (getBinElectronLoose_16(pt))) ;
//	return h_elSF_looseToTight_endcap_16->Eval(pt);
//}
//
//float getElectronSF_16(float pt, float eta, int var = 0){
//	return getElectronSFlooseToTight_16(pt, eta, var);
//}
//
//// muons
//TFile* f_muSF_recoToLoose_lowPt_barrel_16 = new TFile(DATA_SF+"/sos_lepton_SF/mu_JDGauss_bern3_Loose_barrel_7invfb.root","read");
//TFile* f_muSF_recoToLoose_lowPt_endcap_16 = new TFile(DATA_SF+"/sos_lepton_SF/mu_JDGauss_bern3_Loose_endcap_7invfb.root","read");
//TFile* f_muSF_recoToLoose_highPt_16       = new TFile(DATA_SF+"/sos_lepton_SF/MuonID_Z_RunBCD_prompt80X_7p65.root"      ,"read");
//TFile* f_muSF_looseToTight_barrel_16      = new TFile(DATA_SF+"/sos_lepton_SF/mu_SOS_comb_barrel_36invfb.root"          ,"read");
//TFile* f_muSF_looseToTight_endcap_16      = new TFile(DATA_SF+"/sos_lepton_SF/mu_SOS_comb_endcap_36invfb.root"          ,"read");
//TGraphAsymmErrors* h_muSF_recoToLoose_lowPt_barrel_16 = (TGraphAsymmErrors*) f_muSF_recoToLoose_lowPt_barrel_16->Get("mu_JDGauss_bern3_Loose_barrel_ratio");
//TGraphAsymmErrors* h_muSF_recoToLoose_lowPt_endcap_16 = (TGraphAsymmErrors*) f_muSF_recoToLoose_lowPt_endcap_16->Get("mu_JDGauss_bern3_Loose_endcap_ratio");
//TH1F* h_muSF_recoToLoose_highPt_16                    = (TH1F*) f_muSF_recoToLoose_highPt_16->Get("MC_NUM_LooseID_DEN_genTracks_PAR_pt_alleta_bin1/pt_ratio");
//TGraphAsymmErrors* h_muSF_looseToTight_barrel_16      = (TGraphAsymmErrors*) f_muSF_looseToTight_barrel_16->Get("ratio");
//TGraphAsymmErrors* h_muSF_looseToTight_endcap_16      = (TGraphAsymmErrors*) f_muSF_looseToTight_endcap_16->Get("ratio");
//
//int getBinMuonReco_16(float pt){
//	if     (pt >  3.0 && pt <=  3.5) return  0;
//	else if(pt >  3.5 && pt <=  4.0) return  1;
//	else if(pt >  4.0 && pt <=  4.5) return  2;
//	else if(pt >  4.5 && pt <=  5.0) return  3;
//	else if(pt >  5.0 && pt <=  6.0) return  4;
//	else if(pt >  6.0 && pt <=  7.0) return  5;
//	else if(pt >  7.0 && pt <=  8.0) return  6;
//	else if(pt >  8.0 && pt <= 10.0) return  7;
//	else if(pt > 10.0 && pt <= 12.0) return  8;
//	else if(pt > 12.0 && pt <= 18.0) return  9;
//	else if(pt > 18.               ) return 10;
//	else {
//		assert(0);
//	}
//}
//
//int getBinMuonLoose_16(float pt){
//	if     (pt >  3.5 && pt <=  7.5) return 0;
//	else if(pt >  7.5 && pt <= 10.0) return 1;
//	else if(pt > 10.0 && pt <= 15.0) return 2;
//	else if(pt > 15.0 && pt <= 20.0) return 3;
//	else if(pt > 20.0              ) return 4;
//	else {
//	  	assert(0);
//	}
//}
//
//float getMuonSFtracking_16(float pt, float eta, int var = 0){
//	//---pT>10 GeV-------
//	if(pt>10){
//		if     (abs(eta)>0.0  && abs(eta)<=0.20 ) return 0.9800;
//		else if(abs(eta)>0.20 && abs(eta)<=0.40 ) return 0.9862;
//		else if(abs(eta)>0.40 && abs(eta)<=0.60 ) return 0.9872;
//		else if(abs(eta)>0.60 && abs(eta)<=0.80 ) return 0.9845;
//		else if(abs(eta)>0.80 && abs(eta)<=1.00 ) return 0.9847;
//		else if(abs(eta)>1.00 && abs(eta)<=1.20 ) return 0.9801;
//		else if(abs(eta)>1.20 && abs(eta)<=1.40 ) return 0.9825;
//		else if(abs(eta)>1.40 && abs(eta)<=1.60 ) return 0.9754;
//		else if(abs(eta)>1.60 && abs(eta)<=1.80 ) return 0.9860;
//		else if(abs(eta)>1.80 && abs(eta)<=2.00 ) return 0.9810;
//		else if(abs(eta)>2.00 && abs(eta)<=2.20 ) return 0.9815;
//		else if(abs(eta)>2.20 && abs(eta)<=2.40 ) return 0.9687;
//		else return 1.0;
//	}
//
//	// --- pT<10 GeV ---
//	else{
//		if     (abs(eta)>0.0  && abs(eta)<=0.20 ) return 0.9968;
//		else if(abs(eta)>0.20 && abs(eta)<=0.40 ) return 0.9975;
//		else if(abs(eta)>0.40 && abs(eta)<=0.60 ) return 0.9979;
//		else if(abs(eta)>0.60 && abs(eta)<=0.80 ) return 0.9978;
//		else if(abs(eta)>0.80 && abs(eta)<=1.00 ) return 0.9980;
//		else if(abs(eta)>1.00 && abs(eta)<=1.20 ) return 0.9971;
//		else if(abs(eta)>1.20 && abs(eta)<=1.40 ) return 0.9961;
//		else if(abs(eta)>1.40 && abs(eta)<=1.60 ) return 0.9954;
//		else if(abs(eta)>1.60 && abs(eta)<=1.80 ) return 0.9955;
//		else if(abs(eta)>1.80 && abs(eta)<=2.00 ) return 0.9941;
//		else if(abs(eta)>2.00 && abs(eta)<=2.20 ) return 0.9925;
//		else if(abs(eta)>2.20 && abs(eta)<=2.40 ) return 0.9866;
//		else return 1.0;
//	}
//}
//
//float getMuonSFrecoToLoose_16(float _pt, float eta, int var = 0){
//	float pt = std::min(float(199.9),_pt);
//	if (pt<25){
//		if(abs(eta)<1.2){
//			if(var>0) return (h_muSF_recoToLoose_lowPt_barrel_16->Eval(pt) + h_muSF_recoToLoose_lowPt_barrel_16->GetErrorYhigh(getBinMuonReco_16(pt)));
//			if(var<0) return (h_muSF_recoToLoose_lowPt_barrel_16->Eval(pt) - h_muSF_recoToLoose_lowPt_barrel_16->GetErrorYlow (getBinMuonReco_16(pt)));
//			return h_muSF_recoToLoose_lowPt_barrel_16->Eval(pt);
//		}
//		else {
//			if(var>0) return (h_muSF_recoToLoose_lowPt_endcap_16->Eval(pt) + h_muSF_recoToLoose_lowPt_endcap_16->GetErrorYhigh(getBinMuonReco_16(pt)));
//			if(var<0) return (h_muSF_recoToLoose_lowPt_endcap_16->Eval(pt) - h_muSF_recoToLoose_lowPt_endcap_16->GetErrorYlow (getBinMuonReco_16(pt)));
//			return h_muSF_recoToLoose_lowPt_endcap_16->Eval(pt);
//		}
//	}
//	else{
//		Int_t binx = (h_muSF_recoToLoose_highPt_16->GetXaxis())->FindBin(pt);
//		if(var>0) return (h_muSF_recoToLoose_highPt_16->GetBinContent(binx) + 0.01);
//		if(var<0) return (h_muSF_recoToLoose_highPt_16->GetBinContent(binx) - 0.01);
//		return  h_muSF_recoToLoose_highPt_16->GetBinContent(binx);
//	}
//	assert(0);
//	return -999;
//}
//
//float getMuonSFlooseToTight_16(float _pt, float eta, int var = 0){
//	float pt = std::min(float(119.9),_pt);
//	if(abs(eta)<1.2){
//		if(var>0) return (h_muSF_looseToTight_barrel_16->Eval(pt) + h_muSF_looseToTight_barrel_16->GetErrorYhigh(getBinMuonLoose_16(pt))) ;
//		if(var<0) return (h_muSF_looseToTight_barrel_16->Eval(pt) - h_muSF_looseToTight_barrel_16->GetErrorYlow (getBinMuonLoose_16(pt))) ;
//		return h_muSF_looseToTight_barrel_16->Eval(pt);
//	}
//	if(abs(eta)>1.2){
//		if(var>0) return (h_muSF_looseToTight_endcap_16->Eval(pt) + h_muSF_looseToTight_endcap_16->GetErrorYhigh(getBinMuonLoose_16(pt))) ;
//		if(var<0) return (h_muSF_looseToTight_endcap_16->Eval(pt) - h_muSF_looseToTight_endcap_16->GetErrorYlow (getBinMuonLoose_16(pt))) ;
//		return h_muSF_looseToTight_endcap_16->Eval(pt);
//	}
//	assert(0);
//	return -999;
//}
//
//float getMuonSF_16(float pt, float eta, int var = 0){
//	return getMuonSFtracking_16(pt, eta, var)*getMuonSFrecoToLoose_16(pt, eta, var)*getMuonSFlooseToTight_16(pt, eta, var);
//}
//
//// leptons
//float getLepSF_16(float pt, float eta, int pdgId, int var = 0){
//	if(abs(pdgId)==11) return getElectronSF_16(pt, eta, var);
//	return getMuonSF_16(pt, eta, var);
//}
//
//float leptonSF_16(float lepSF1, float lepSF2, float lepSF3 = 1, float lepSF4 = 1){
//    return lepSF1*lepSF2*lepSF3*lepSF4;
//}
//
//
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
//
//
//// LEPTON SCALE FACTORS FULLSIM 17
//// -------------------------------------------------------------
//
//// electrons
//TFile* f_elSF_looseToTight_barrel_17             = new TFile(DATA_SF+"/sos_lepton_SF_2017/el_SOS_barrel.root" , "read");
//TFile* f_elSF_looseToTight_endcap_17             = new TFile(DATA_SF+"/sos_lepton_SF_2017/el_SOS_endcap.root" , "read");
//TFile* f_elSF_recoToLoose_lowPt_17               = new TFile(DATA_SF+"/sos_lepton_SF_2017/el_reco_lowpt.root" , "read");
//TFile* f_elSF_recoToLoose_highPt_17              = new TFile(DATA_SF+"/sos_lepton_SF_2017/el_reco_highpt.root", "read");
//TGraphAsymmErrors* h_elSF_looseToTight_barrel_17 = (TGraphAsymmErrors*) f_elSF_looseToTight_barrel_17->Get("ratio");
//TGraphAsymmErrors* h_elSF_looseToTight_endcap_17 = (TGraphAsymmErrors*) f_elSF_looseToTight_endcap_17->Get("ratio");
//TH2F* h_elSF_recoToLoose_lowPt_17                = (TH2F*) f_elSF_recoToLoose_lowPt_17 ->Get("EGamma_SF2D");
//TH2F* h_elSF_recoToLoose_highPt_17               = (TH2F*) f_elSF_recoToLoose_highPt_17->Get("EGamma_SF2D");
//
//int getBinElectronLoose_17(float pt){
//	if     (pt >  5.0 && pt <= 12.5) return 0;
//	else if(pt > 12.5 && pt <= 16.0) return 1;
//	else if(pt > 16.0 && pt <= 20.0) return 2;
//	else if(pt > 20.0 && pt <= 25.0) return 3;
//	else if(pt > 25.0 && pt <= 30.0) return 4;
//	else if(pt > 30.0 && pt <= 40.0) return 5;
//	else if(pt > 40.0 && pt <= 75.0) return 6;
//	else if(pt > 75.0 && pt <= 120.0) return 7;
//	else {
//		assert(0);
//	}
//}
//
//float getElectronSFrecoToLoose_17(float _pt, float eta, int var = 0){
//	float pt = std::min(float(499.9), _pt); //protection
//	if(pt<20){
//		Int_t binx = (h_elSF_recoToLoose_lowPt_17->GetXaxis())->FindBin(eta);
//		Int_t biny = (h_elSF_recoToLoose_lowPt_17->GetYaxis())->FindBin(pt);
//		if(var>0) return (h_elSF_recoToLoose_lowPt_17->GetBinContent(binx, biny) + 0.01);
//		if(var<0) return (h_elSF_recoToLoose_lowPt_17->GetBinContent(binx, biny) - 0.01);
//		return  h_elSF_recoToLoose_lowPt_17->GetBinContent(binx, biny);
//	}
//	else {
//		Int_t binx = (h_elSF_recoToLoose_highPt_17->GetXaxis())->FindBin(eta);
//		Int_t biny = (h_elSF_recoToLoose_highPt_17->GetYaxis())->FindBin(pt);
//		if(var>0) return (h_elSF_recoToLoose_highPt_17->GetBinContent(binx, biny) + 0.01);
//		if(var<0) return (h_elSF_recoToLoose_highPt_17->GetBinContent(binx, biny) - 0.01);
//		return  h_elSF_recoToLoose_highPt_17->GetBinContent(binx, biny);
//	}
//}
//
//float getElectronSFlooseToTight_17(float _pt, float eta, int var = 0){
//	// update this!
//	float pt = std::min(float(30.0), _pt); //protection
//	
//	if(abs(eta)<1.479){
//		if(var>0) return (h_elSF_looseToTight_barrel_17->Eval(pt) + h_elSF_looseToTight_barrel_17->GetErrorYhigh(getBinElectronLoose_17(pt))) ;
//		if(var<0) return (h_elSF_looseToTight_barrel_17->Eval(pt) - h_elSF_looseToTight_barrel_17->GetErrorYlow (getBinElectronLoose_17(pt))) ;
//		return  h_elSF_looseToTight_barrel_17->Eval(pt);
//	}
//	else {
//		if(var>0) return (h_elSF_looseToTight_endcap_17->Eval(pt) + h_elSF_looseToTight_endcap_17->GetErrorYhigh(getBinElectronLoose_17(pt))) ;
//		if(var<0) return (h_elSF_looseToTight_endcap_17->Eval(pt) - h_elSF_looseToTight_endcap_17->GetErrorYlow (getBinElectronLoose_17(pt))) ;
//		return h_elSF_looseToTight_endcap_17->Eval(pt);
//	}
//}
//
//float getElectronSF_17(float pt, float eta, int var = 0){
//	return getElectronSFrecoToLoose_17(pt, eta, var)*getElectronSFlooseToTight_17(pt, eta, var);
//}
//
//// muons
//TFile* f_muSF_recoToLoose_lowPt_17        = new TFile(DATA_SF+"/sos_lepton_SF_2017/mu_tracking_lowpt.root" ,"read");
//TFile* f_muSF_recoToLoose_highPt_17       = new TFile(DATA_SF+"/sos_lepton_SF_2017/mu_tracking_highpt.root","read");
//TFile* f_muSF_id_lowPt_17                 = new TFile(DATA_SF+"/sos_lepton_SF_2017/mu_id_lowpt.root"       ,"read");
//TFile* f_muSF_id_highPt_17                = new TFile(DATA_SF+"/sos_lepton_SF_2017/mu_id_highpt.root"      ,"read");
//TFile* f_muSF_looseToTight_barrel_17      = new TFile(DATA_SF+"/sos_lepton_SF_2017/mu_SOS_comb_barrel.root","read");
//TFile* f_muSF_looseToTight_endcap_17      = new TFile(DATA_SF+"/sos_lepton_SF_2017/mu_SOS_comb_endcap.root","read");
//TGraphAsymmErrors* h_muSF_recoToLoose_lowPt_17   = (TGraphAsymmErrors*) f_muSF_recoToLoose_lowPt_17 ->Get("ratio_eff_eta3_tk0_dr030e030_corr");
//TGraphAsymmErrors* h_muSF_recoToLoose_highPt_17  = (TGraphAsymmErrors*) f_muSF_recoToLoose_highPt_17->Get("ratio_eff_eta3_dr030e030_corr");
//TH2F* h_muSF_id_lowPt_17                         = (TH2F*) f_muSF_id_lowPt_17 ->Get("NUM_SoftID_DEN_genTracks_pt_abseta");
//TH2F* h_muSF_id_highPt_17                        = (TH2F*) f_muSF_id_highPt_17->Get("NUM_SoftID_DEN_genTracks_pt_abseta");
//TGraphAsymmErrors* h_muSF_looseToTight_barrel_17 = (TGraphAsymmErrors*) f_muSF_looseToTight_barrel_17->Get("ratio");
//TGraphAsymmErrors* h_muSF_looseToTight_endcap_17 = (TGraphAsymmErrors*) f_muSF_looseToTight_endcap_17->Get("ratio");
//
//int getBinMuonTracking_17(float eta){
//	if     (               eta < -2.1) return 0;
//	else if(eta >= -2.1 && eta < -1.6) return 1;
//	else if(eta >= -1.6 && eta < -1.1) return 2;
//	else if(eta >= -1.1 && eta < -0.9) return 3;
//	else if(eta >= -0.9 && eta < -0.6) return 4;
//	else if(eta >= -0.6 && eta < -0.3) return 5;
//	else if(eta >= -0.3 && eta < -0.2) return 6;
//	else if(eta >= -0.2 && eta <  0.2) return 7;
//	else if(eta >=  0.2 && eta <  0.3) return 8;
//	else if(eta >=  0.3 && eta <  0.6) return 9;
//	else if(eta >=  0.6 && eta <  0.9) return 10;
//	else if(eta >=  0.9 && eta <  1.1) return 11;
//	else if(eta >=  1.1 && eta <  1.6) return 12;
//	else if(eta >=  1.6 && eta <  2.1) return 13;
//	else if(eta >=  2.1              ) return 14;
//	else {
//	  	assert(0);
//	}
//	return -1;
//}
//
//int getBinMuonTight_17(float pt){
//	if     (pt >  3.5 && pt <=  7.5) return 0;
//	else if(pt >  7.5 && pt <= 10.0) return 1;
//	else if(pt > 10.0 && pt <= 15.0) return 2;
//	else if(pt > 15.0 && pt <= 20.0) return 3;
//	else if(pt > 20.0 && pt <= 30.0) return 4;
//	else if(pt > 30.0 && pt <= 40.0) return 5;
//	else if(pt > 40.0 && pt <= 60.0) return 6;
//	else {
//		assert(0);
//	}
//}
//
//float getMuonSFtracking_17(float pt, float eta, int var = 0){
//	if(pt<10){
//		if(var>0) return (h_muSF_recoToLoose_lowPt_17->Eval(eta) + h_muSF_recoToLoose_lowPt_17->GetErrorYhigh(getBinMuonTracking_17(eta))) ;
//		if(var<0) return (h_muSF_recoToLoose_lowPt_17->Eval(eta) - h_muSF_recoToLoose_lowPt_17->GetErrorYlow (getBinMuonTracking_17(eta))) ;
//		return h_muSF_recoToLoose_lowPt_17->Eval(eta);
//	}
//	if(pt>10){
//		if(var>0) return (h_muSF_recoToLoose_highPt_17->Eval(eta) + h_muSF_recoToLoose_highPt_17->GetErrorYhigh(getBinMuonTracking_17(eta))) ;
//		if(var<0) return (h_muSF_recoToLoose_highPt_17->Eval(eta) - h_muSF_recoToLoose_highPt_17->GetErrorYlow (getBinMuonTracking_17(eta))) ;
//		return h_muSF_recoToLoose_highPt_17->Eval(eta);
//	}
//	assert(0);
//	return -999;
//}
//
//float getMuonSFrecoToLoose_17(float _pt, float eta, int var = 0){
//	float pt = std::min(float(119.9),_pt);
//	if (pt<15) {
//		Int_t binx = (h_muSF_id_lowPt_17->GetXaxis())->FindBin(pt);
//		Int_t biny = (h_muSF_id_lowPt_17->GetYaxis())->FindBin(abs(eta));
//		if(var>0) return (h_muSF_id_lowPt_17->GetBinContent(binx, biny) + 0.01);
//		if(var<0) return (h_muSF_id_lowPt_17->GetBinContent(binx, biny) - 0.01);
//		return  h_muSF_id_lowPt_17->GetBinContent(binx, biny);
//	}	
//	else {
//		Int_t binx = (h_muSF_id_highPt_17->GetXaxis())->FindBin(pt);
//		Int_t biny = (h_muSF_id_highPt_17->GetYaxis())->FindBin(abs(eta));
//		if(var>0) return (h_muSF_id_highPt_17->GetBinContent(binx, biny) + 0.01);
//		if(var<0) return (h_muSF_id_highPt_17->GetBinContent(binx, biny) - 0.01);
//		return  h_muSF_id_highPt_17->GetBinContent(binx, biny);
//	}	
//	assert(0);
//	return -999;
//}
//
//float getMuonSFlooseToTight_17(float _pt, float eta, int var = 0){
//	float pt = std::min(float(59.9),_pt); // protection
//	if(abs(eta)<1.2){
//		if(var>0) return (h_muSF_looseToTight_barrel_17->Eval(pt) + h_muSF_looseToTight_barrel_17->GetErrorYhigh(getBinMuonTight_17(pt))) ;
//		if(var<0) return (h_muSF_looseToTight_barrel_17->Eval(pt) - h_muSF_looseToTight_barrel_17->GetErrorYlow (getBinMuonTight_17(pt))) ;
//		return h_muSF_looseToTight_barrel_17->Eval(pt);
//	}
//	if(abs(eta)>1.2){
//		if(var>0) return (h_muSF_looseToTight_endcap_17->Eval(pt) + h_muSF_looseToTight_endcap_17->GetErrorYhigh(getBinMuonTight_17(pt))) ;
//		if(var<0) return (h_muSF_looseToTight_endcap_17->Eval(pt) - h_muSF_looseToTight_endcap_17->GetErrorYlow (getBinMuonTight_17(pt))) ;
//		return h_muSF_looseToTight_endcap_17->Eval(pt);
//	}
//	assert(0);
//	return -999;
//}
//
//float getMuonSF_17(float pt, float eta, int var = 0){
//	return getMuonSFtracking_17(pt, eta, var)*getMuonSFrecoToLoose_17(pt, eta, var)*getMuonSFlooseToTight_17(pt, eta, var);
//}
//
//// leptons
//float getLepSF_17(float pt, float eta, int pdgId, int var = 0){
//	if(abs(pdgId)==11) return getElectronSF_17(pt, eta, var);
//	return getMuonSF_17(pt, eta, var);
//}
//
//float leptonSF_17(float lepSF1, float lepSF2, float lepSF3 = 1, float lepSF4 = 1){
//    return lepSF1*lepSF2*lepSF3*lepSF4;
//}

void functionsSF() {}
