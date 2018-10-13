import os, sys, ROOT

plotbase = "/afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos16_fullstatus"
plotbase = "/afs/cern.ch/user/c/cheidegg/www/heppy/2018-05-21_sos17_fullstatus"



def scale(plot):
	f = ROOT.TFile.Open(plot,"read")
	htot = f.Get("yields_total") 
	hdat = f.Get("yields_data" ) 
	if not htot or not hdat: f.Close(); return 1
	tot=htot.GetBinContent(1)
	dat=hdat.GetBinContent(1)
	npr = 0
	for key in f.GetListOfKeys():
		keyn = key.GetName()
		if "yields" in keyn and "fakes" in keyn: 
			npr += f.Get(keyn).GetBinContent(1)
	f.Close()
	if npr==0: return 1.0
	others = tot-npr
	return float(dat-others)/npr

for selection in ["AR1F", "AR2F", "AR3F"]:
	if not os.path.isdir(plotbase+"/plot/"+selection): continue
	for region in os.listdir(plotbase+"/plot/"+selection):
		for lumi in os.listdir(plotbase+"/plot/"+selection+"/"+region):
			rpath = plotbase+"/plot/"+selection+"/"+region+"/"+lumi+"/all/datasig/plots_sos.root"
			print 
			print selection, region, lumi
			print scale(rpath)


