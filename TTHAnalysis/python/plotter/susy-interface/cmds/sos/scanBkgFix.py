import ROOT, os


cardbase = "/afs/cern.ch/work/c/cheidegg/scratch/2018-05-21_sos16_fullstatus"
#cardbase = "/afs/cern.ch/work/c/cheidegg/scratch/2018-05-21_sos16_fullstatus_sDD"


for region in os.listdir(cardbase+"/scan/SR"):
	for lumi in os.listdir(cardbase+"/scan/SR/"+region):
		orig = cardbase+"/scan/SR/"+region+"/"+lumi+"/bkg/common/SR.original.root"
		inpt = cardbase+"/scan/SR/"+region+"/"+lumi+"/bkg/common/SR.input.root"
		if not (os.path.exists(orig) and os.path.exists(inpt)): continue
		print "processing",orig
		h = []
		fakes = None
		f = ROOT.TFile.Open(orig,"read")
		for key in f.GetListOfKeys():
			hist = f.Get(key.GetName())
			hist.SetDirectory(0)
			if   hist.GetName()=="x_rares_btagLF_Up"  : hist.SetName("x_rares_bTagLF_Up");
			elif hist.GetName()=="x_rares_btagLF_Down": hist.SetName("x_rares_bTagLF_Dn");
			elif hist.GetName()=="x_rares_btagHF_Up"  : hist.SetName("x_rares_bTagHF_Up");
			elif hist.GetName()=="x_rares_btagHF_Down": hist.SetName("x_rares_bTagHF_Dn");
			elif hist.GetName()[-4:]=="Down": hist.SetName(hist.GetName()[0:-4]+"Dn")
			h.append(hist)
		f.Close()
		f = ROOT.TFile.Open(inpt,"recreate")
		f.cd()
		for hist in h: hist.Write()
		f.Close()


