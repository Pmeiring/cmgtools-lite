#include "TStyle.h"
#include "TFile.h"
#include "TH2D.h"
#include "TColor.h"

void draw()
{
  //gStyle->SetPalette(1,0); //55
  
  UInt_t Number = 3;
  Double_t Red[3]   = { 0.0, 1.0, 1.0 };
  Double_t Green[3] = { 0.0, 1.0, 0.0 };
  Double_t Blue[3]  = { 1.0, 1.0, 0.0 };
  Double_t Stops[3] = { 0.0, 0.5, 1.0 };
  Int_t nb=900;
  TColor::CreateGradientColorTable(Number,Stops,Red,Green,Blue,nb);
  //gStyle->SetNumberContours(nb); 
 

  TFile *f = new TFile("../makeExclusionPlot/config/SUS16025/TChiNeuWZ_significance_results.root");
  //TFile *f = new TFile("../makeExclusionPlot/config/SUS16025/T2tt_significance_results.root");
  TH2D * h2 = (TH2D*)f->Get("ul_histo"); 
  h2->SetContour(nb); 
 
  // TChiWZ =============
  h2->GetXaxis()->SetTitle("m#kern[0.1]{_{#lower[-0.12]{#tilde{#chi}^{0}_{2}, #tilde{#chi_{1}}^{#pm}   }}} [GeV]");
  h2->GetXaxis()->SetTitleOffset(1.2);
  h2->GetXaxis()->SetRangeUser(100, 260);
 
  h2->GetYaxis()->SetTitle("#Delta m ( #tilde{#chi}^{0}_{2},#tilde{#chi}^{0}_{1} ) [GeV]");
  h2->GetYaxis()->SetRangeUser(7.5, 40);
  h2->GetYaxis()->SetTitleOffset(1.1);

  //pp #rightarrow #tilde{#chi}_{2}^{0} #tilde{#chi}_{1}^{#pm}, #tilde{#chi}_{2}^{0} #rightarrow Z* #tilde{#chi}^{0}_{1}, #tilde{#chi}_{1}^{#pm} #rightarrow W* #tilde{#chi}^{0}_{1}  

  // T2tt =============                                                                                                                                                                                                                                                                                                     
  //h2->GetXaxis()->SetTitle("m#kern[0.1]{_{#lower[-0.12]{ #tilde{t}}}} [GeV]");
  //h2->GetXaxis()->SetTitleOffset(1.2);
  //h2->GetXaxis()->SetRangeUser(300, 520);

  //h2->GetYaxis()->SetTitle("#Delta m ( #tilde{t}, #tilde{#chi}^{0}_{1} ) [GeV]");
  //h2->GetYaxis()->SetRangeUser(10.5, 80);
  //h2->GetYaxis()->SetTitleOffset(1.1);
  
  //pp #rightarrow #tilde{t} #tilde{t}, #tilde{t} #rightarrow #tilde{#chi}^{+}_{1} b, #tilde{#chi}^{+}_{1} #rightarrow #tilde{#chi}^{0}_{1} W^{+}

  

  //=====================

  h2->GetZaxis()->SetRangeUser(-3, 3);
  h2->GetZaxis()->SetTitle("Observed significance");
  h2->Draw("COLZ"); 
  h2->Smooth(1,"k3a"); 


  TPaveLabel *pl = new TPaveLabel(0.1920863,0.8567134,0.5920863,0.9809619,"CMS #font[50]{Preliminary}","brNDC");
  pl->SetBorderSize(0);
  pl->SetFillColor(0);
  pl->SetFillStyle(0);
  pl->SetTextAlign(12);
  pl->SetTextSize(0.2790178);
  pl->Draw();
  
  pl = new TPaveLabel(0.6906475,0.8391784,0.9431655,0.998497,"33.2-35.9 fb^{-1} (13 TeV)","brNDC");
  pl->SetBorderSize(0);
  pl->SetFillColor(0);
  pl->SetFillStyle(0);
  pl->SetTextAlign(12);
  pl->SetTextFont(42);
  pl->SetTextSize(0.22);
  pl->Draw();
  
}
