import ROOT, os


cardbase = "/afs/cern.ch/work/c/cheidegg/scratch/2018-05-21_sos16_fullstatus"
cardbase = "/afs/cern.ch/work/c/cheidegg/scratch/2018-05-21_sos16_fullstatus_sDD"


for region in os.listdir(cardbase+"/scan/SR"):
	for lumi in os.listdir(cardbase+"/scan/SR/"+region):
		orig = cardbase+"/scan/SR/"+region+"/"+lumi+"/bkg/common/SR.original.root"
		inpt = cardbase+"/scan/SR/"+region+"/"+lumi+"/bkg/common/SR.input.root"
		if os.path.exists(orig) and os.path.exists(inpt): continue
		if not os.path.exists(inpt): continue
		print "processing",inpt
		os.system("mv "+inpt+" "+orig)
		h = []
		fakes = None
		f = ROOT.TFile.Open(orig,"read")
		for key in f.GetListOfKeys():
			hist = f.Get(key.GetName())
			hist.SetDirectory(0)
			if "fakes" in hist.GetName():
				if not fakes: fakes = hist; fakes.SetName(fakes.GetName().replace("appldata","applany").replace("applmcBoth","applany").replace("matched_wj","applany").replace("matched_tt","applany").replace("matched_t","applany").replace("matched_dy","applany").replace("matched_tw","applany").replace("matched_vv","applany")) ## this won't work if there are systematic variations of the fakes !!!!!!!
				else        : fakes.Add(hist)
				continue
			h.append(hist)
		f.Close()
		f = ROOT.TFile.Open(inpt,"recreate")
		f.cd()
		for hist in h: hist.Write()
		fakes.Write()
		f.Close()


