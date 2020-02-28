import ROOT
from array import array
from collections import OrderedDict

DM = {
    "100_99" : 1,
    "100_97" : 3,
    "100_95" : 5,
    "100_92" : 8,
    "100_90" : 10,
    "100_85" : 15,
    "100_80" : 20,
    "100_70" : 30,
    "100_60" : 40,
}

W_channels = [0,65,63,61,45,43,41,25,23,21,1516,1314,1112]

def GetIdx(d,channel):
    for i,x in enumerate(d):
        if x == channel:
            return i


def GetKeyNames( self, dir = "" ):
        self.cd(dir)
        return [key.GetName() for key in ROOT.gDirectory.GetListOfKeys()]
ROOT.TFile.GetKeyNames = GetKeyNames

def GetRatio(d1,d2):
    for i,d in enumerate(d1):   # d is the ith value in list d1
        d[1] = d[1] / d2[i]     # normalize d[1] (the yields) to the total yields (at the ith masspoint)
    return d1                   # return the normalized list


def GetGraph(d, name=None):
    x = array('f', [dm[0] for dm in d])
    y = array('f', [dy[1] for dy in d])
    g = ROOT.TGraph(len(x), x, y)
    g.Sort()
    if name: g.SetName(name)
    return g

def GetLabel(x):
    if 'ev' in x: return 'W*#rightarrow e #nu'
    if 'mv' in x: return 'W*#rightarrow #mu #nu'
    if 'tv' in x: return 'W*#rightarrow #tau #nu'
    if 'cs' in x: return 'W*#rightarrow cs'
    if 'ud' in x: return 'W*#rightarrow ud'
    if 'ff' in x: return 'W*#rightarrow f#bar{f}'
    return x

def MultiPlot(gs, outname="dummy", 
              ytitle="dummy", yrange=(0,0.1),
              log=False):
    ROOT.gStyle.SetOptStat(0)
    c = ROOT.TCanvas("canv","",750,750)
    pad = ROOT.TPad("pad", "pad", .005, .01, .995, .995)
    pad.Draw()
    pad.cd()
    if log: pad.SetLogy()

    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetRightMargin(0.05)
    ROOT.gPad.SetBottomMargin(0.1)
    ROOT.gPad.SetTopMargin(0.05)

    # pad2.cd()
    leg = ROOT.TLegend(.65,0.65,0.95,0.95);
    leg.SetTextFont(42);
    leg.SetHeader("");
    leg.SetNColumns(1);

    mg = ROOT.TMultiGraph()
    for g in gs:
        mg.Add(g)
        g.SetLineWidth(2)
        g.SetMarkerStyle(20)
        if "mm" in g.GetName(): g.SetLineStyle(ROOT.kDashed)
        leg.AddEntry(g, GetLabel(g.GetName()),"lp")
    mg.Draw("ACP PLC PMC")
    mg.SetTitle(";dM(C_{1},N_{1}) [GeV];"+ytitle)
    mg.GetXaxis().SetLimits(-1,41);
    mg.SetMinimum(0.);
    mg.SetMaximum(0.7);

    t = ROOT.TLatex((.2,.87,"#splitline{BRs determined by counting the}{W-decays in the TChiWZ samples}"))
    t.SetTextSize(.03)
    t.SetNDC(1)
    t.Draw()

    c.Modified()

    leg.SetFillStyle(0);
    leg.SetFillColor(0);
    leg.SetBorderSize(0);
    leg.Draw();

    c.SaveAs(outname+".png") 


# Define input file, from which to read the number of decays
inFileName = "/eos/user/p/pmeiring/www/SUSY_SOS/GenLep_TChiWZ_categorization/BranchingRatios_REMOVE/N2_100GeV_BR_xsec/2los_3l_plots_PETER.root";
inFile = ROOT.TFile.Open(inFileName ,"READ")

y_W_decay = [[] for c in W_channels]

# Loop over all keys in the file
keyList = inFile.GetKeyNames(inFileName)
for key in keyList:
    if key.startswith("W_decays_signal_TChiWZ"): 
        dM = DM.get(key[-6:])       
        hist = inFile.Get(key)
        # nentries = hist.GetEntries()
        # sumw = hist.Integral()
        # inv_weight = nentries/sumw
        for ic,c in enumerate(W_channels):
            y_W_decay[ic].append([dM,hist.GetBinContent(c+1)])


# total yields for W decays per mass point
y_W_all = []
for m in range(len(y_W_decay[0])):
    total=0
    for c in range(len(W_channels)):
        total+=y_W_decay[c][m][1]
    y_W_all.append(total)


# Extract the yields per mass point for each decay channel of choice
y_W_ev = [y_W_decay[GetIdx(W_channels,1112)][m] for m in range(len(y_W_decay[GetIdx(W_channels,1112)]))]
y_W_mv = [y_W_decay[GetIdx(W_channels,1314)][m] for m in range(len(y_W_decay[GetIdx(W_channels,1314)]))]
y_W_tv = [y_W_decay[GetIdx(W_channels,1516)][m] for m in range(len(y_W_decay[GetIdx(W_channels,1516)]))]
y_W_ud = [y_W_decay[GetIdx(W_channels,21)][m]   for m in range(len(y_W_decay[GetIdx(W_channels,21)]))]
y_W_cs = [y_W_decay[GetIdx(W_channels,43)][m]   for m in range(len(y_W_decay[GetIdx(W_channels,43)]))]

# Make the graphs and normalize them to the total number of events to get the actual BRs
g_W_ev = GetGraph( GetRatio(y_W_ev,y_W_all) ,"BR_Wev")
g_W_mv = GetGraph( GetRatio(y_W_mv,y_W_all) ,"BR_Wmv")
g_W_tv = GetGraph( GetRatio(y_W_tv,y_W_all) ,"BR_Wtv")
g_W_cs = GetGraph( GetRatio(y_W_cs,y_W_all) ,"BR_Wcs")
g_W_ud = GetGraph( GetRatio(y_W_ud,y_W_all) ,"BR_Wud")

# Make the multigraph plot
brs = [g_W_ev,g_W_mv,g_W_tv,g_W_cs,g_W_ud]
MultiPlot(brs,ytitle="BR(C_{1}#rightarrowN_{1}+(W*#rightarrowf#bar{f}))",outname="/eos/user/p/pmeiring/www/SUSY_SOS/GenLep_TChiWZ_categorization/BranchingRatios_REMOVE/N2_100GeV_BR_xsec/BR_W_Counting")

