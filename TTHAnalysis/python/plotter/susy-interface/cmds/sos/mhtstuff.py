import ROOT

class Histogram1D:
	def __init__(self, signals, name, expr, label, xnbins, xmin, xmax):
		self.expr    = expr
		self.signals = signals
		self.bins    = str(xnbins)+","+str(xmin)+","+str(xmax)
		self.objs    = []
		for signal in signals:
			self.objs.append(ROOT.TH1F(signal+"_"+name, "", xnbins, xmin, xmax))
			self.objs[-1].GetXaxis().SetTitle(label)
	def draw(self, tree, signal, weight="1"):
		theObj = filter(lambda x: signal in x.GetName(), self.objs)
		print theObj, [x.GetName() for x in self.objs]
		if len(theObj)!=1: return
		if ROOT.gROOT.FindObject("dummy") != None: ROOT.gROOT.FindObject("dummy").Delete()
		print tree.Draw(self.expr+">>dummy("+self.bins+")","xsec*(Sum$(abs(Jet_eta)<2.5 && Jet_chHEF<0.1 && Jet_mcPt<8)==0)*"+weight)
		theObj[0].Add(ROOT.gROOT.FindObject("dummy"))	
		print theObj[0].GetEntries()

class Histogram2D:
	def __init__(self, signals, name, expr, xlabel, ylabel, xnbins, xmin, xmax, ynbins, ymin, ymax):
		self.expr    = expr
		self.signals = signals
		self.bins    = str(xnbins)+","+str(xmin)+","+str(xmax)+","+str(ynbins)+","+str(ymin)+","+str(ymax) 
		self.objs    = []
		for signal in signals:
			self.objs.append(ROOT.TH2F(signal+"_"+name, "", xnbins, xmin, xmax, ynbins, ymin, ymax))
			self.objs[-1].GetXaxis().SetTitle(xlabel)
			self.objs[-1].GetYaxis().SetTitle(ylabel)
	def draw(self, tree, signal, weight="1"):
		theObj = filter(lambda x: signal in x.GetName(), self.objs)
		if len(theObj)!=1: return
		if ROOT.gROOT.FindObject("dummy") != None: ROOT.gROOT.FindObject("dummy").Delete()
		print tree.Draw(self.expr+">>dummy("+self.bins+")","xsec*(Sum$(abs(Jet_eta)<2.5 && Jet_chHEF<0.1 && Jet_mcPt<8)==0)*"+weight)
		theObj[0].Add(ROOT.gROOT.FindObject("dummy"))	
	

tpath   = "/data1/botta/trees_SOS_010217"

friends = ["/data1/cheidegg/trees_SOS_010217_mht/0_both3dlooseClean_v2"]
signals = ["TChiWZ_200_180"  , "TChiWZ_175_165"  , "TChiWZ_125_95"   ]
weights = ["1807.39/1000*0.1", "2953.28/1000*0.1", "10034.8/1000*0.1"]

hists = [
         Histogram1D(signals, "met"       , "met_pt"     , "p_{T}^{miss} [GeV]", 18, 0, 450), 
         Histogram1D(signals, "mht"       , "mhtJet25Sel", "H_{T}^{miss} [GeV]", 18, 0, 450), 
         Histogram2D(signals, "metvsmht"  , "mhtJet25Sel:met_pt", "p_{T}^{miss} [GeV]", "H_{T}^{miss} [GeV]", 18, 0, 450, 18, 0, 450), 
         Histogram1D(signals, "met_lowMET", "met_pt"     , "p_{T}^{miss} [GeV]", 18, 0, 450), 
         Histogram1D(signals, "met_higMET", "met_pt"     , "p_{T}^{miss} [GeV]", 18, 0, 450), 
         Histogram1D(signals, "mht_lowMET", "mhtJet25Sel", "H_{T}^{miss} [GeV]", 18, 0, 450), 
         Histogram1D(signals, "mht_higMET", "mhtJet25Sel", "H_{T}^{miss} [GeV]", 18, 0, 450), 
        ]

lowMET = "HLT_BIT_HLT_DoubleMu3_PFMET50_v"
higMET = "(HLT_BIT_HLT_PFMET90_PFMHT90_IDTight_v || HLT_BIT_HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v || HLT_BIT_HLT_PFMET100_PFMHT100_IDTight_v || HLT_BIT_HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v || HLT_BIT_HLT_PFMET110_PFMHT110_IDTight_v || HLT_BIT_HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v || HLT_BIT_HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v || HLT_BIT_HLT_PFMET120_PFMHT120_IDTight_v)"

for i,sample in enumerate(signals):
	spath = tpath+"/"+sample+"/treeProducerSusyMultilepton/tree.root"
	rfile = ROOT.TFile.Open(spath,"read")
	rtree = rfile.Get("tree")
	for friend in friends:
		rtree.AddFriend("sf/t",friend+"/evVarFriend_"+sample+".root")
		###rtree.AddFriend("sf/t",tpath+"/"+friend+"/evVarFriend_"+sample+".root")
	for hist in hists[0:3]:
		hist.draw(rtree, sample, weights[i])

	lowMETweight = weights[i]+"*"+lowMET
	hists[3].draw(rtree, sample, lowMETweight)
	hists[5].draw(rtree, sample, lowMETweight)

	higMETweight = weights[i]+"*"+higMET
	hists[4].draw(rtree, sample, higMETweight)
	hists[6].draw(rtree, sample, higMETweight)

	rfile.Close()


rfile = ROOT.TFile.Open("/afs/cern.ch/user/c/cheidegg/ec/CMSSW_8_0_25/src/CMGTools/TTHAnalysis/python/plotter/susy-interface/cmds/sos/mht.root","recreate")
rfile.cd()
for hist in hists:
	for obj in hist.objs:
		obj.Write()
rfile.Close() 


