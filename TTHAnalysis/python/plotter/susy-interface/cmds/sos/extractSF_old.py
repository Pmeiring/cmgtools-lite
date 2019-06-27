import os, sys, ROOT

## lumis
red   = 33.2
full  = 35.9

## tree dir
treedir = "/data1/botta/trees_SOS_010217"


## FUNCTIONS AND CLASSES BELOW
def scale(plot):
	f = ROOT.TFile.Open(plot,"read")
	tot = f.Get("yields_total").GetBinContent(1)
	dat = f.Get("yields_data" ).GetBinContent(1)
	npr = 0
	for key in f.GetListOfKeys():
		keyn = key.GetName()
		if "yields" in keyn and "fakes" in keyn: 
			npr += f.Get(keyn).GetBinContent(1)
	f.Close()
	if npr==0: return 1.0
	others = tot-npr
	return float(dat-others)/npr

def mkdir(basedir):
	if os.path.isdir(basedir): return
	os.system("mkdir -p "+basedir)

class Region:
	def __init__(self, config, region, lumi):
		self.config = config
		self.nleps  = 3 if config=="sos3l" else 2
		self.region = region
		self.lumi   = lumi
		self.slumi  = str(lumi)
	def getARs(self):
		return ["AR"+str(i)+"F" for i in range(1,self.nleps+1)]
	def getCut(self, ar):
		if ar=="AR1F": return "oneLNT"
		if ar=="AR2F": return "twoLNT"
		if ar=="AR3F": return "threeLNT"
		return ""
	def runARplots(self, treedir, basedir):
		templates = []
		for AR in self.getARs():
			template = "python susy-interface/plotmaker.py {C} {R} {T} {O} -l {L} --make data --plots yields -o {A} -p \"data;prompt_.*;rares;fakes_matched_.*\" --flags \"-X twoTight -E {CA} --perBin\"".format(C=self.config, R=self.region, T=treedir, O=basedir, L=self.slumi, A=AR, CA=self.getCut(AR)) 
			print template
			os.system(template)
	def runSF(self, basedir):
		self.sfAR = []
		for AR in self.getARs():
			theDir = basedir+"/plot/{A}/{R}/{L}/yields/data/plots_sos.root".format(A=AR, R=self.region, L=self.slumi.replace(".","p")+"fb")
			self.sfAR.append(scale(theDir))



## format (config, region, lumi)
theRegions = [
              #Region("sos2l", "2losEwkLow", red ),
              #Region("sos2l", "2losEwkMed", full),
              #Region("sos2l", "2losEwkHig", full),
              #Region("sos2l", "2losColLow", red ),
              #Region("sos2l", "2losColMed", full),
              #Region("sos2l", "2losColHig", full),
              Region("sos2l", "2lss"      , full),
              #Region("sos3l", "3lLow"     , red ),
              #Region("sos3l", "3lMed"     , full),
              #Region("sos2l", "dyLow"     , red ),
              #Region("sos2l", "dyMed"     , full),
              #Region("sos2l", "ttLow"     , red ),
              #Region("sos2l", "ttMed"     , full),
              #Region("sos2l", "vvLow"     , red ),
              #Region("sos2l", "vvMed"     , full),
              #Region("sos2l", "wzMin"     , full),
              #Region("sos2l", "wzLow"     , full),
              #Region("sos2l", "wzMed"     , full),
             ]

## MAIN STORY

basedir = sys.argv[1] if len(sys.argv)>1 else None
if not basedir:
	print "Need to give a path"
	sys.exit()

what = None
if not os.path.isdir(basedir):
	print "Please give the basedir of the directory where you want to compute the SF from"
	print "Alternatively, type 'y' to create it and the plots on the fly"
	what = raw_input(">> ").strip()
	if what!="y": sys.exit()

## run all plots
if what=="y":
	mkdir(basedir)
	for region in theRegions:
		region.runARplots(treedir, basedir)

## run the SF extraction
for region in theRegions:
	region.runSF(basedir)
	print region.region,":",region.sfAR



