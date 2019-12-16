#include "TROOT.h"
#include "TFile.h"
#include "TTree.h"
#include "TBrowser.h"
#include "TH2.h"
#include "TRandom.h"

// void FillMultiGraph(TMultiGraph *mg, TLegend *legend, TFile *RootFile_ee, TFile *RootFile_mm){

// 	Color_t color[10] = {};
// 	color[0] 	 = kCyan;
// 	color[1] 	 = kAzure+7;
// 	color[2]	 = kMagenta;
// 	color[3] 	 = kRed-7;
// 	color[4] 	 = kOrange-3;
// 	color[5] 	 = kYellow+2;
// 	color[6] 	 = kSpring-6;
// 	color[7] 	 = kGreen+4;
// 	color[8] 	 = kBlack;
// 	color[9] 	 = kGray;

// 	TKey *key1;	TObject* obj1;
// 	TIter next_ee(RootFile_ee->GetListOfKeys());
// 	TIter next_mm(RootFile_mm->GetListOfKeys());

// 	int counter=0;
// 	while ((key1=(TKey*)next_ee())){

// 		obj1 = key1->ReadObj();
// 		if (obj1->InheritsFrom(TGraphErrors::Class())){
// 			TGraphErrors *h = (TGraphErrors*)obj1;
// 			string name = h->GetName();
// 			if (name=="TChiWZ_100_85") continue;
// 			if (name=="TChiWZ_100_80") continue;
// 			if (name=="TChiWZ_100_70") continue;
// 			if (name=="TChiWZ_100_60") continue;


// 			h->SetLineColor(color[counter]);
// 			h->SetLineWidth(3);
// 			counter++;
// 			legend->AddEntry(h,name.c_str(),"l");

// 			mg->Add(h);
// 			std::cout<<name<<std::endl;
// 		}
// 	}		
// }

void FillMultiGraph(TMultiGraph *mg, TMultiGraph *mg_eff, TLegend *legend, TLegend *legend_eff, TFile *RootFile){

	Color_t color[10] = {};
	color[0] 	 = kGreen;
	color[1] 	 = kRed;
	color[2]	 = kGray;
	color[3]	 = kYellow;
	color[4] 	 = kCyan;
	color[5] 	 = kOrange+1;
	color[6] 	 = kBlue;
	color[7] 	 = kMagenta;
	color[8] 	 = kBlack;

	TKey *key1;	TObject* obj1;
	TIter next(RootFile->GetListOfKeys());

	int counter=0;
	while ((key1=(TKey*)next())){

		obj1 = key1->ReadObj();
		if (obj1->InheritsFrom(TGraphErrors::Class())){
			TGraphErrors *h = (TGraphErrors*)obj1;
			string name = h->GetName();
			// if (name=="TChiWZ_100_85") continue;
			// if (name=="TChiWZ_100_80") continue;
			// if (name=="TChiWZ_100_70") continue;
			// if (name=="TChiWZ_100_60") continue;


			h->SetLineColor(color[counter]);
			h->SetLineWidth(3);

			if(name.find("TChi")==0){
				legend->AddEntry(h,name.c_str(),"l");
				legend_eff->AddEntry(h,name.c_str(),"l");
				mg->Add(h);
				std::cout<<name<<std::endl;
			}
			else{
				mg_eff->Add(h);
				std::cout<<name<<std::endl;
				counter++;
			}
		}
	}
}














// void PlotCutflow(std::string Path1, std::string Path2){


// 	std::string RootFile1 = Path1+"/Trial_CutFlow.root";
// 	std::string RootFile2 = Path2+"/Trial_CutFlow.root";
// 	const char *cPath1 = RootFile1.c_str();
// 	const char *cPath2 = RootFile2.c_str();


//     TFile *RootFile_ee= TFile::Open(cPath1);
//     TFile *RootFile_mm= TFile::Open(cPath1);


//     // Read the text file containing the cuts
//     TMacro *ma = (TMacro*)RootFile_ee->Get("Cuts");
//     TList *Cuts = ma->GetListOfLines();
//     std::vector<std::string> cuts;
// 	TIter nextcut(Cuts);
// 	while (TObject *obj = nextcut()){
// 		cuts.push_back(obj->GetName());
// 	}


// 	TMultiGraph *mg = new TMultiGraph(); 
// 	auto legend = new TLegend(.7,.65,.9,.9);

// 	FillMultiGraph(mg, legend, RootFile_ee, RootFile_mm);


// 	gStyle->SetOptStat(0);
//     TCanvas *c1 = new TCanvas("c1","Canvas",900,1000);
// 	c1->SetFillStyle(4000); //will be transparent
// 	// c1->Divide(1,2);

// 	c1->cd();	
// 	c1->SetLogy();

// 		int nSel=18;

// 		TH1F *h = new TH1F("h","CutFlow m_{N1}=100GeV, ee",nSel,0.5,nSel+0.5);
//    		for (int i=1;i<=nSel;i++) {
//    			h->GetXaxis()->SetBinLabel(i,cuts[i-1].c_str());
//    		}
//    		h->GetXaxis()->SetLabelSize(0.03);
//    		h->GetXaxis()->LabelsOption("v");
// 		h->GetYaxis()->SetTitle("Event yields");
//    		h->GetYaxis()->SetRangeUser(1e0,1e6);
//    		h->Draw();

// 		mg->Draw("P");

// 		// auto legend = new TLegend(.6,.75,.9,.9);
// 		legend->Draw("same");
// 		c1->SetBottomMargin(0.3);
// 	c1->Update();

// 	string outputPath = Path1 + "/CutFlowPlot.png";
// 	const char *coutputPath = outputPath.c_str();

// 	c1->SaveAs(coutputPath);


// 	c1->Close();
// 	gApplication->Terminate();

// }


void PlotCutflow(std::string Path1, std::string plotTitle){


	std::string RootFile1 = Path1+"/Trial_CutFlow.root";
	const char *cPath1 = RootFile1.c_str();

    TFile *RootFile= TFile::Open(cPath1);


    // Read the text file containing the cuts
    TMacro *ma = (TMacro*)RootFile->Get("Cuts");
    TList *Cuts = ma->GetListOfLines();
    int ncuts=0;
    std::vector<std::string> cuts;
	TIter nextcut(Cuts);
	while (TObject *obj = nextcut()){
		cuts.push_back(obj->GetName());
		ncuts++;
	}


	TMultiGraph *mg = new TMultiGraph(); 
	TMultiGraph *mg_eff = new TMultiGraph(); 
	auto legend = new TLegend(.7,.65,.9,.9);
	auto legend_eff = new TLegend(.11,.45,.27,.65);
	// auto legend_eff = new TLegend(.51,.4,.67,.6);



	FillMultiGraph(mg, mg_eff, legend, legend_eff, RootFile);




	gStyle->SetOptStat(0);
    TCanvas *c1 = new TCanvas("c1","Canvas",900,1000);
	c1->SetFillStyle(4000); //will be transparent
	// c1->Divide(1,2);

	c1->cd();	
	c1->SetLogy();

		const char *title = plotTitle.c_str();
		TH1F *h = new TH1F("h", title, ncuts,0.5,ncuts+0.5);
   		for (int i=1;i<=ncuts;i++) {
   			h->GetXaxis()->SetBinLabel(i,cuts[i-1].c_str());
   		}
   		h->GetXaxis()->SetLabelSize(0.03);
   		h->GetXaxis()->LabelsOption("v");
		h->GetYaxis()->SetTitle("Event yields");
   		h->GetYaxis()->SetRangeUser(1e0,1e6);
   		h->Draw();

		mg->Draw("P");

		// auto legend = new TLegend(.6,.75,.9,.9);
		legend->Draw("same");
		c1->SetBottomMargin(0.3);
	c1->Update();

	string outputPath = Path1 + "/CutFlowPlot.png";
	const char *coutputPath = outputPath.c_str();
	c1->SaveAs(coutputPath);

	outputPath = Path1 + "/CutFlowPlot.pdf";
	coutputPath = outputPath.c_str();
	c1->SaveAs(coutputPath);



    TCanvas *c2 = new TCanvas("c2","Canvas",900,1000);
	c2->SetFillStyle(4000); //will be transparent
	// c1->Divide(1,2);

	c2->cd();	

		const char *title2 = plotTitle.c_str();
		TH1F *g = new TH1F("g", title, ncuts,0.5,ncuts+0.5);
   		for (int i=1;i<=ncuts;i++) {
   			g->GetXaxis()->SetBinLabel(i,cuts[i-1].c_str());
   		}
   		g->GetXaxis()->SetLabelSize(0.03);
   		g->GetXaxis()->LabelsOption("v");
		g->GetYaxis()->SetTitle("Cut efficiency");
   		g->GetYaxis()->SetRangeUser(0,1.1);
   		g->Draw();

		mg_eff->Draw("P");

		// auto legend = new TLegend(.6,.75,.9,.9);
		legend_eff->Draw("same");
		c2->SetBottomMargin(0.4);
	c2->Update();


	outputPath = Path1 + "/CutEffPlot.png";
	coutputPath = outputPath.c_str();
	c2->SaveAs(coutputPath);

	outputPath = Path1 + "/CutEffPlot.pdf";
	coutputPath = outputPath.c_str();
	c2->SaveAs(coutputPath);









	c1->Close();
	gApplication->Terminate();

}