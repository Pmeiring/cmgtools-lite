from optparse import OptionParser
from lib import maker
from lib import functions as func

def collectMakes(region, make):
	available = ["data", "datasig", "sigs", "bkgs", "mix"]
	mix       = ["all", "both"]
	if not make in available and not make in mix: return []
	if make in mix:
		if make=="all" : return available
		if make=="both": return ["sigs", "bkgs"]
	if make in available: return [make]
	return []

def collectPlots(region, plotsname, custom):
	if len(custom)>0: return ["custom"]
	available = [k for k,v in region.plots.iteritems()]
	if len(available)==0 or (plotsname!="all" and not plotsname in available): return []
	#if plotsname=="all": return available
	return [plotsname]

def collectPPlots(mm, plotsname, custom):
	if plotsname=="all": return ""
	if len(custom)>0: 
		return " ".join("--sP "+p for p in func.splitList(custom))
	if not plotsname in mm.region.plots.keys(): return ""
	return " ".join("--sP "+v for v in mm.region.plots[plotsname])

def collectProcesses(mm, make):
	if len(mm.options.procs)>0: 
		procs = " ".join(["-p "+b for b in mm.getProcs()])
		add = ""
		if make in ["sigs", "mix", "datasig"]: add="--showIndivSigs --noStackSig "
		if make=="sigs": add="--empytStack -p dummy "+add
		return add + procs
	bkgs = " ".join(["-p "+b for b in mm.getBkgs()])
	sigs = " ".join(["-p "+s for s in mm.getSigs()])
	if make=="data"   : return "-p data "+bkgs
	if make=="datasig": return "-p data "+bkgs+" --showIndivSigs --noStackSig "+sigs
	if make=="mix"    : return "--showIndivSigs --noStackSig "+sigs+" "+bkgs
	if make=="sigs"   : return "--emptyStack -p dummy --showIndivSigs --noStackSig "+sigs
	if make=="bkgs"   : return bkgs
	return ""
	
parser = OptionParser(usage="%prog cfg regions treedir outdir [options]")
parser = maker.addMakerOptions(parser)
parser.add_option("--make",  dest="make",   type="string", default="data", help="Give info what to plot, either 'data' (data vs bkg), 'bkg' (for bkg only), 'sig' (for signal only), 'mix' (for bkg and signal together), 'both' (for running once 'sig' and once 'bkg')");
parser.add_option("--plots",  dest="plots",   type="string", default="all", help="Give the name of the plot collection you want to run");
parser.add_option("--selPlots", dest="customPlots", action="append", default=[], help="Bypass --plots option and give directly the name of the plots in the plotsfile")
parser.add_option("--lspam", dest="lspam", type="string", default="Preliminary", help="Left-spam for CMS_lumi in mcPlots, either Preliminary, Simulation, Internal or nothing")
parser.add_option("--noRatio", dest="ratio", action="store_false", default=True, help="Do NOT plot the ratio (i.e. give flag --showRatio)")
parser.add_option("--dcc", dest="dcc", action="store_true", default=False, help="Run the double-count-checker after you have run all the plots.")

base = "python mcPlots.py {MCA} {CUTS} {PLOTFILE} {T} --s2v --tree {TREENAME} -f --cmsprel '{LSPAM}' --legendWidth 0.20 --legendFontSize 0.035 {MCCS} {MACROS} {RATIO} -l {LUMI} --pdir {O} {FRIENDS} {PROCS} {PLOTS} {FLAGS}"
baseDcc = "python mcDump.py {MCA} {CUTS} '{run:1d} {lumi:9d} {evt:12d}' {T} --tree {TREENAME} {MCCS} {MACROS} {FRIENDS} {PROCS} {FLAGS}" 
(options, args) = parser.parse_args()
options = maker.splitLists(options)
mm      = maker.Maker("plotmaker", base, args, options, parser.defaults)

friends = mm.collectFriends()	
sl      = mm.getVariable("lumi","12.9").replace(".","p")

for r in range(len(mm.regions)):
	print "region ",r
	mm.iterateRegion()

	mccs    = mm.collectMCCs  ()
	macros  = mm.collectMacros()	
	flags   = mm.collectFlags (["flagsPlots"])
	ratio   = "--showRatio" if options.ratio else ""
	
	makes    = collectMakes(mm.region, options.make)
	plots    = collectPlots(mm.region, options.plots, options.customPlots)
	scenario = mm.getScenario(True)

	for p in plots:
		print "p ",p
		for m in makes:
			print "m, ",m
			output = mm.outdir +"/plot/"+ scenario +"/"+ sl +"fb/"+ p +"/"+ m
			func.mkdir(output)
			procs   = collectProcesses(mm, m)
			print "procs ",procs
			pplots  = collectPPlots   (mm, p, options.customPlots)
			print "pplots ",pplots


			mm.submit([mm.getVariable("mcafile",""), mm.getVariable("cutfile",""), mm.getVariable("plotfile",""), mm.treedirs, mm.getVariable("treename","treeProducerSusyMultilepton"), options.lspam, mccs, macros, ratio, mm.getVariable("lumi","12.9"), output, friends, procs, pplots, flags],mm.region.name+"_"+p+"_"+m,False)

mm.runJobs()
mm.clearJobs()

if options.dcc:
	flags = mm.collectFlags ([])
	mm.reloadBase(baseDcc)
	base = mm.makeCmd([mm.getVariable("mcafile",""), mm.getVariable("cutfile",""), mm.treedirs, mm.getVariable("treename", "treeProducerSusyMultilepton"), mccs, macros, friends, procs, flags])
	evtlist = sorted(filter(lambda x: x[0:1].isdigit(), filter(None, func.bashML(base))))
	preceeding = ""
	for entry in evtlist:
		if entry == preceeding:
			print "DOUBLE COUNTED: "+entry
			continue
		preceeding = entry

