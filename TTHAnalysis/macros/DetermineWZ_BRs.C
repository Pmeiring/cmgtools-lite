#include "TROOT.h"
#include "TFile.h"
#include "TTree.h"
#include "TBrowser.h"
#include "TH2.h"
#include "TRandom.h"

int StringToMassPoint(std::string mp){
	std::string mN2 = mp.substr(0, mp.find("_", 0));
	// std::string mN1 = mp.substr(1, mp.find("_", 0));
	std::string mN1 = mp.erase (0,mN2.length()+1);

	int MN2 = std::stoi(mN2);
	int MN1 = std::stoi(mN1);

	return MN2-MN1;
}

void DetermineWZ_BRs(){
	
	
	ROOT::EnableImplicitMT();

	std::string filename = "/eos/user/p/pmeiring/www/SUSY_SOS/GenLep_TChiWZ_categorization/BranchingRatios/N2_100GeV_BR_xsec/2los_3l_plots_PETER.root";
	const char *fileName = filename.c_str();
	TFile *RootFile= TFile::Open(fileName);


	TKey *key1;	TObject* obj1; int i=0;
	TIter next(RootFile->GetListOfKeys());

	std::vector<std::string> MassPointsZ = {};
	std::vector<std::string> MassPointsW = {};
	std::vector<std::string> MassPointsZtau = {};
	std::vector<std::string> MassPointsWtau = {};

	int nMassPoints = 9;

	// Bins filled depending on decay modes (Z->ee = 1111)
	float Zbins [3] = {1111,1313,1515};
	float Wbins [12] = {65,63,61,45,43,41,25,23,21,1516,1314,1112};

	float Ztaubins [3] = {1500,1501,1502};
	float Wtaubins [2] = {1500,1501};

	// Number of times the boson decayed with a specified mode				
	//  tb,ts,td,cb,cs,cd,ub,us,ud,tauv,muv ,ev
	float yieldsZ[9][3];
	float yieldsW[9][12];
	// Integers to keep track of which masspoint the plot corresponds to
	int indexMasspointZ=0;
	int indexMasspointW=0;

	// Yields for specific Boson->tau decays
	float yieldsZtau[9][3];
	float yieldsWtau[9][2];
	int indexMasspointZtau=0;
	int indexMasspointWtau=0;


	while ((key1=(TKey*)next())){

		obj1 = key1->ReadObj();
		if (obj1->InheritsFrom(TH1D::Class())){
			TH1D *h = (TH1D*)obj1;
			string name = h->GetName();

			std::size_t found = name.find("Z_decays_signal_TChiWZ_");
			if(found!=std::string::npos){
				name.replace(found,23,"");
				MassPointsZ.push_back(name);
				// std::cout<<name<<"\tZ"<<std::endl;

				for (int b=0; b<3; b++){
					float binc = h->GetBinContent(Zbins[b]+1);
					yieldsZ[indexMasspointZ][b]=binc;
					// std::cout<<indexMasspointZ<<"\t"<<yieldsZ[indexMasspointZ][b]<<std::endl;
					// std::cout<<binc<<std::endl;
				}
				indexMasspointZ++;
			}

			found = name.find("W_decays_signal_TChiWZ_");
			if(found!=std::string::npos){
				name.replace(found,23,"");
				MassPointsW.push_back(name);
				// std::cout<<name<<"\tW"<<std::endl;

				for (int b=0; b<12; b++){
					float binc = h->GetBinContent(Wbins[b]+1);
					yieldsW[indexMasspointW][b]=binc;
					// std::cout<<binc<<std::endl;
				}
				indexMasspointW++;
			}

			found = name.find("Ztau_decays_signal_TChiWZ_");
			if(found!=std::string::npos){
				name.replace(found,26,"");
				MassPointsZtau.push_back(name);
				// std::cout<<name<<"\tZ"<<std::endl;

				for (int b=0; b<3; b++){
					float binc = h->GetBinContent(Ztaubins[b]+1);
					yieldsZtau[indexMasspointZtau][b]=binc;
				}
				indexMasspointZtau++;
			}

			found = name.find("Wtau_decays_signal_TChiWZ_");
			if(found!=std::string::npos){
				name.replace(found,26,"");
				MassPointsWtau.push_back(name);
				// std::cout<<name<<"\tW"<<std::endl;

				for (int b=0; b<2; b++){
					float binc = h->GetBinContent(Wtaubins[b]+1);
					yieldsWtau[indexMasspointWtau][b]=binc;
					// std::cout<<binc<<std::endl;
				}
				indexMasspointWtau++;
			}			
		}
	}


	float dmz[9];
	float dmw[9];
	float dmztau[9];
	float dmwtau[9];

	float z_ee[9];
	float z_mm[9];
	float z_tt[9];
	float z_ll[9];
	float z_tltl[9];
	float z_thtl[9];
	float z_thth[9];

	float w_ev[9];
	float w_mv[9];
	float w_tv[9];
	float w_lv[9];
	float w_tlv[9];
	float w_thv[9];

	float w_tb[9];
	float w_ts[9];
	float w_td[9];
	float w_cb[9];
	float w_cd[9];
	float w_cs[9];
	float w_ub[9];
	float w_us[9];
	float w_ud[9];
	float w_qq[9];
					

	for (int mp=0; mp<nMassPoints; mp++){
		float yieldsZnorm = (yieldsZ[mp][0]+yieldsZ[mp][1]+yieldsZ[mp][2]);
		float yieldsZtaunorm= (yieldsZ[mp][0]+yieldsZ[mp][1]+yieldsZtau[mp][0]+yieldsZtau[mp][1]+yieldsZtau[mp][2]);
		float yieldsWnorm = (yieldsW[mp][0]+yieldsW[mp][1]+yieldsW[mp][2]+yieldsW[mp][3]+yieldsW[mp][4]+yieldsW[mp][5]+yieldsW[mp][6]+yieldsW[mp][7]+yieldsW[mp][8]+yieldsW[mp][9]+yieldsW[mp][10]+yieldsW[mp][11]);
		float yieldsWtaunorm= (yieldsW[mp][0]+yieldsW[mp][1]+yieldsW[mp][2]+yieldsW[mp][3]+yieldsW[mp][4]+yieldsW[mp][5]+yieldsW[mp][6]+yieldsW[mp][7]+yieldsW[mp][8]+yieldsWtau[mp][0]+yieldsWtau[mp][1]+yieldsW[mp][10]+yieldsW[mp][11]);

		dmz[mp] = (float)StringToMassPoint(MassPointsZ[mp]);		
		z_ee[mp] = yieldsZ[mp][0] / yieldsZnorm;
		z_mm[mp] = yieldsZ[mp][1] / yieldsZnorm;
		z_tt[mp] = yieldsZ[mp][2] / yieldsZnorm;
		z_ll[mp] = z_ee[mp] + z_mm[mp] / yieldsZnorm;

		dmztau[mp] = (float)StringToMassPoint(MassPointsZtau[mp]);		
		z_tltl[mp] = yieldsZtau[mp][0] /yieldsZtaunorm;
		z_thtl[mp] = yieldsZtau[mp][1] /yieldsZtaunorm;
		z_thth[mp] = yieldsZtau[mp][2] /yieldsZtaunorm;

		//  tb,ts,td,cb,cs,cd,ub,us,ud,tauv,muv ,ev
		dmw[mp] = (float)StringToMassPoint(MassPointsW[mp]);
		w_ev[mp] = yieldsW[mp][11] / yieldsWnorm;
		w_mv[mp] = yieldsW[mp][10] / yieldsWnorm;
		w_tv[mp] = yieldsW[mp][9] / yieldsWnorm;
		// w_lv[mp] = (w_mv[mp] + w_ev[mp]) / yieldsWnorm;

		w_tb[mp] = yieldsW[mp][0] / yieldsWnorm;
		w_ts[mp] = yieldsW[mp][1] / yieldsWnorm;
		w_td[mp] = yieldsW[mp][2] / yieldsWnorm;
		w_cb[mp] = yieldsW[mp][3] / yieldsWnorm;
		w_cs[mp] = yieldsW[mp][4] / yieldsWnorm;
		w_cd[mp] = yieldsW[mp][5] / yieldsWnorm;
		w_ub[mp] = yieldsW[mp][6] / yieldsWnorm;
		w_us[mp] = yieldsW[mp][7] / yieldsWnorm;
		w_ud[mp] = yieldsW[mp][8] / yieldsWnorm;
		w_qq[mp] = (w_tb[mp] + w_ts[mp] + w_td[mp] + w_cb[mp] + w_cs[mp] + w_cd[mp] + w_ub[mp] + w_us[mp] + w_ud[mp]);

		dmwtau[mp] = (float)StringToMassPoint(MassPointsWtau[mp]);
		w_tlv[mp] = yieldsWtau[mp][0] / yieldsWtaunorm;
		w_thv[mp] = yieldsWtau[mp][1] / yieldsWtaunorm;

	}

	TGraph *Z_ll = new TGraph(nMassPoints, dmz, z_ll); Z_ll->Sort(); Z_ll->SetLineColor(kAzure+7); Z_ll->SetLineWidth(3);
	TGraph *Z_ee = new TGraph(nMassPoints, dmz, z_ee); Z_ee->Sort(); Z_ee->SetLineColor(kBlue);  Z_ee->SetLineWidth(3);
	TGraph *Z_mm = new TGraph(nMassPoints, dmz, z_mm); Z_mm->Sort(); Z_mm->SetLineColor(kRed);   Z_mm->SetLineWidth(3);	
	TGraph *Z_tt = new TGraph(nMassPoints, dmz, z_tt); Z_tt->Sort(); Z_tt->SetLineColor(kGreen); Z_tt->SetLineWidth(3);

	TGraph *Z_tltl = new TGraph(nMassPoints, dmztau, z_tltl); Z_tltl->Sort(); Z_tltl->SetLineColor(kGreen); Z_tltl->SetLineWidth(3);
	TGraph *Z_thtl = new TGraph(nMassPoints, dmztau, z_thtl); Z_thtl->Sort(); Z_thtl->SetLineColor(kMagenta); Z_thtl->SetLineWidth(3);
	TGraph *Z_thth = new TGraph(nMassPoints, dmztau, z_thth); Z_thth->Sort(); Z_thth->SetLineColor(kCyan); Z_thth->SetLineWidth(3);
	
	// Z->LL (ee/mumu/tautau)
	TMultiGraph *mgz = new TMultiGraph(); 
	mgz->Add(Z_ee);mgz->Add(Z_mm);mgz->Add(Z_tt);

	// Z->ll (ee/mumu)
	TMultiGraph *mgz2 = new TMultiGraph(); 
	mgz2->Add(Z_ee); mgz2->Add(Z_mm); mgz2->Add(Z_tltl); mgz2->Add(Z_thtl); mgz2->Add(Z_thth);

	// W->lv
	TGraph *W_lv = new TGraph(nMassPoints, dmw, w_lv); W_lv->Sort(); W_lv->SetLineColor(kBlue); W_lv->SetLineWidth(3);
	TGraph *W_ev = new TGraph(nMassPoints, dmw, w_ev); W_ev->Sort(); W_ev->SetLineColor(kBlue); W_ev->SetLineWidth(3);
	TGraph *W_mv = new TGraph(nMassPoints, dmw, w_mv); W_mv->Sort(); W_mv->SetLineColor(kRed); W_mv->SetLineWidth(3);
	TGraph *W_tv = new TGraph(nMassPoints, dmw, w_tv); W_tv->Sort(); W_tv->SetLineColor(kGreen); W_tv->SetLineWidth(3);

	TGraph *W_tlv = new TGraph(nMassPoints, dmwtau, w_tlv); W_tlv->Sort(); W_tlv->SetLineColor(kGreen); W_tlv->SetLineWidth(3);
	TGraph *W_thv = new TGraph(nMassPoints, dmwtau, w_thv); W_thv->Sort(); W_thv->SetLineColor(kMagenta); W_thv->SetLineWidth(3);

	// W->qq
	TGraph *W_qq = new TGraph(nMassPoints, dmw, w_qq); W_qq->Sort(); W_qq->SetLineColor(kCyan); W_qq->SetLineWidth(3);
	TGraph *W_tb = new TGraph(nMassPoints, dmw, w_tb); W_tb->Sort(); W_tb->SetLineColor(kAzure+7);
	TGraph *W_ts = new TGraph(nMassPoints, dmw, w_ts); W_ts->Sort(); W_ts->SetLineColor(kMagenta);
	TGraph *W_td = new TGraph(nMassPoints, dmw, w_td); W_td->Sort(); W_td->SetLineColor(kRed-7);
	TGraph *W_cb = new TGraph(nMassPoints, dmw, w_cb); W_cb->Sort(); W_cb->SetLineColor(kOrange-3); W_cb->SetLineWidth(3);
	TGraph *W_cs = new TGraph(nMassPoints, dmw, w_cs); W_cs->Sort(); W_cs->SetLineColor(kYellow+2); W_cs->SetLineWidth(3);
	TGraph *W_cd = new TGraph(nMassPoints, dmw, w_cd); W_cd->Sort(); W_cd->SetLineColor(kSpring-6); W_cd->SetLineWidth(3);
	TGraph *W_ub = new TGraph(nMassPoints, dmw, w_ub); W_ub->Sort(); W_ub->SetLineColor(kGreen+4); W_ub->SetLineWidth(3);
	TGraph *W_us = new TGraph(nMassPoints, dmw, w_us); W_us->Sort(); W_us->SetLineColor(kGray); W_us->SetLineWidth(3);
	TGraph *W_ud = new TGraph(nMassPoints, dmw, w_ud); W_ud->Sort(); W_ud->SetLineColor(kBlack); W_ud->SetLineWidth(3);




	TMultiGraph *mgw = new TMultiGraph();  
	mgw->Add(W_ev);
	mgw->Add(W_mv);
	mgw->Add(W_tv);
	mgw->Add(W_cs);
	mgw->Add(W_cd);
	mgw->Add(W_us);
	mgw->Add(W_ud);

	TMultiGraph *mgw2 = new TMultiGraph(); 
	mgw2->Add(W_tlv); mgw2->Add(W_thv); mgw2->Add(W_ev); mgw2->Add(W_mv); mgw2->Add(W_qq); 

	std::cout<<"all done, printing..."<<std::endl;







gStyle->SetOptStat(0);
    TCanvas *c1 = new TCanvas("c1","Canvas",900,900);
	c1->SetFillStyle(4000); //will be transparent
	// c1->Divide(1,2);

	c1->cd();	
		mgz->Draw("AC*");
		mgz->GetXaxis()->SetTitle("Mass-splitting #Delta M (GeV)"); 
		mgz->GetYaxis()->SetTitle("Branching Ratio"); 
		auto legend1 = new TLegend(.6,.75,.9,.9);
		legend1->SetNColumns(2);
		legend1->AddEntry(Z_ee,"Z->ee","l");
		legend1->AddEntry(Z_mm,"Z->#mu#mu","l");
		legend1->AddEntry(Z_tt,"Z->#tau#tau","l");
		legend1->Draw("same");
	c1->Update();

TCanvas *c2 = new TCanvas("c2","Canvas",900,900);
	c2->SetFillStyle(4000); //will be transparent
	c2->cd(2);	
		mgw->Draw("AC*");
		mgw->GetXaxis()->SetTitle("Mass-splitting #Delta M (GeV)"); 
		mgw->GetYaxis()->SetTitle("Branching Ratio"); 
		auto legend2 = new TLegend(.6,.65,.9,.9);
		legend2->SetNColumns(2);
		legend2->AddEntry(W_ev,"W->e#nu","l");
		legend2->AddEntry(W_mv,"W->#mu#nu","l");
		legend2->AddEntry(W_tv,"W->#tau#nu","l");
		// legend2->AddEntry(W_tb,"W->tb","l");
		// legend2->AddEntry(W_ts,"W->ts","l");
		// legend2->AddEntry(W_td,"W->td","l");
		// legend2->AddEntry(W_cb,"W->cb","l");
		legend2->AddEntry(W_cs,"W->cs","l");
		legend2->AddEntry(W_cd,"W->cd","l");
		// legend2->AddEntry(W_ub,"W->ub","l");
		legend2->AddEntry(W_us,"W->us","l");
		legend2->AddEntry(W_ud,"W->ud","l");
		legend2->Draw("same");		
	c2->Update();

    TCanvas *c3 = new TCanvas("c3","Canvas",900,900);
	c3->SetFillStyle(4000); //will be transparent
	c3->cd();	
		mgz2->Draw("AC*");
		mgz2->GetXaxis()->SetTitle("Mass-splitting #Delta M (GeV)"); 
		mgz2->GetYaxis()->SetTitle("Branching Ratio"); 
		auto legend3 = new TLegend(.6,.75,.9,.9);
		legend3->SetNColumns(2);
		legend3->AddEntry(Z_ee,"Z->ee","l");
		legend3->AddEntry(Z_thtl,"Z->#tau_{h}#tau_{l}","l");
		legend3->AddEntry(Z_mm,"Z->#mu#mu","l");
		legend3->AddEntry(Z_thth,"Z->#tau_{h}#tau_{h}","l");
		legend3->AddEntry(Z_tltl,"Z->#tau_{l}#tau_{l}","l");
		legend3->Draw("same");
	c3->Update();

    TCanvas *c4 = new TCanvas("c4","Canvas",900,900);
	c4->SetFillStyle(4000); //will be transparent
	c4->cd();	
		mgw2->Draw("AC*");
		mgw2->GetXaxis()->SetTitle("Mass-splitting #Delta M (GeV)"); 
		mgw2->GetYaxis()->SetTitle("Branching Ratio"); 
		auto legend4 = new TLegend(.6,.75,.9,.9);
		legend4->SetNColumns(2);
		legend4->AddEntry(W_tlv,"W->#tau_{l}#nu","l");
		legend4->AddEntry(W_thv,"W->#tau_{h}#nu","l");
		legend4->AddEntry(W_ev,"W->e#nu","l");
		legend4->AddEntry(W_qq,"W->qq","l");
		legend4->AddEntry(W_mv,"W->#mu#nu","l");
		legend4->Draw("same");
	c4->Update();

	gPad->WaitPrimitive();

	c1->SaveAs("/eos/user/p/pmeiring/www/SUSY_SOS/GenLep_TChiWZ_categorization/BranchingRatios/N2_100GeV_BR_xsec/BRs_Z_v1.png");
	c2->SaveAs("/eos/user/p/pmeiring/www/SUSY_SOS/GenLep_TChiWZ_categorization/BranchingRatios/N2_100GeV_BR_xsec/BRs_W_v1.png");
	c3->SaveAs("/eos/user/p/pmeiring/www/SUSY_SOS/GenLep_TChiWZ_categorization/BranchingRatios/N2_100GeV_BR_xsec/BRs_Z_v2.png");
	c4->SaveAs("/eos/user/p/pmeiring/www/SUSY_SOS/GenLep_TChiWZ_categorization/BranchingRatios/N2_100GeV_BR_xsec/BRs_W_v2.png");
	// c1->Print("/eos/user/p/pmeiring/www/SUSY_SOS/PlayGround/BRs.pdf","PDF"); 

	c1->Close();	

	gApplication->Terminate();
}