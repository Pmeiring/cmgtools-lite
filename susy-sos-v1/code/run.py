from optparse import OptionParser
import os

def rm(path):
	if not os.path.exists(path): return
	os.system("rm "+path)

def write(path, content):
	f = open(path,"w")
	f.write(content)
	f.close()

class Statement:
	def __init__(self, scope, raw, options):
		self.raw    = raw.strip()
		self.parsed = ""
		self.parse()
	def parse(self):
		if not self.raw or len(self.raw)==0: return
		self.raw 

class Parameter:
	def __init__(self, module, name, value, options=[]):
		self.module  = module
		self.name    = name
		self.value   = value
		self.options = options
	def process(self):
		## how to evaluate statements as values in parameters?
		return Statement(self.module, self.value, self.options)

class Cfg:
	def __init__(self, cfgpath):
		self.path   = cfgpath
		self.params = []
		self.load()
	def __getattr__(self, key):
		param = filter(lambda x: x.name==kye, self.params)
		if len(param)==1: return param[0]
		return None
	def load(self):
		if not os.path.exists(self.path): return
		for line in [l.strip().rstrip("\n").strip() for l in open(self.path).readlines()]:
			if line[0:1]=="#": continue
			if len(line)==0: continue
			sl = [s.strip() for s in line.split(":")]
			self.params.append(Parameter(sl[0], sl[1], self.parseOpts(sl[2] if len(sl)>2 else "")))
#parsing of + and = symbols
					   

	def parseOpts(self, string):
		if len(string)==0: return []
		opts = {}
		for entry in [ss.strip() for ss in string.split(";")]:
			if len(entry)==0: continue
			if "=" in entry:
				opts[entry.split("=")[0].strip()] = entry.split("=")[1].strip()
			else:
				opts[entry                      ] = True
		return opts


class QuasiModuleParameter: 
	## basically dynamic parameters for the mode
	## one can define at runtime what is a relevant parameter for the execution of the quasi module
	def __init__(self, module, cfgparam):
		self.module  = module
		self.name    = cfgparam.value
		self.load(cfgparam.options)
	def load(self, options):
		## linkages and allowed values and stuff
		self.default = []
		self.value   = []
		self.allowed = []
		self.alrange = []
		self.depends = None
		for optkey, optval in options.iteritems():
			if   optkey == "depends": self.depends = self.module.getQuasiModuleParam(optval)
			elif optkey == "default": self.value   = optval; self.default = optval


class QuasiModule:
	def __init__(self, cfg):
		self.cfg = cfg
		self.load()
	def load(self):
		if not self.cfg: return
		self.containers = []
		self.parameters = []
		for container in self.cfg.containers:
			self.containers.append(Container(self, container.key, container.value, "builds/"+container.key))
		for parameter in self.cfg.parameters:
			self.parameters.append(QuasiModuleParameter(self, parameter))

#	def loadMode(self):


	def getParam(self, name):
		pnames = [p.name for p in self.parameters]
		if name in pnames: return self.parameters[self.parameters.index(pname)]
		return None


class Build:
	def __init__(self, container, code):
		self.container = container
		self.module    = container.module
		self.raw       = code
	def prepare(self):
		self.prepared = self.raw
		for pname in [p.name for p in self.module.parameters]:
			self.prepared = self.prepared.replace("$("+pname+")", "self.module.getParam(\""+pname+"\")")
		self.prepared = self.prepared.replace("print ", "theBuffer += ")
	def build(self):
		theBuffer = ""
		exec(self.prepared)
		self.out = theBuffer

class Container:
	def __init__(self, module, name, path, build):
		self.module = module
		self.name   = name
		self.path   = path
		self.build  = Build(module, "".join(open(build).readlines()))
	def build(self):
		self.build.prepare()
		self.build.build  ()
		self.write()
	def write(self):
		rm(self.path)
		write(self.path, self.build.out)

class Scheme:
	def __init__(self, module):
		self.module = module

	def run(self):
		self.mode.build()
		self.build()
		cmd(self.cmd)

#	def build(self):
		## building the scheme (sequence of general commands + mode commands)


class Mode:
	def __init__(self, module, name):
		self.module = module
		self.name   = name
	def load(self):
		self.cfg = Cfg("modes/"+name)
	def build(self):
		for container in self.containers:
			container.build()
		self.cmd = self.cfg.cmd






## cfg format:
## parameter name [: parameter value [: options]]

## need in quasi module
## * general info (name, module type)
## * a list of parameters, allowed values, possible values (if any)
## * a list of containers and prescriptions of how to build them
## * a list of schemes (= bundles of execution commands), in python plotter its only one
## * a list of modes (how to use the schemes or build the ingredients of the schemes) = individual commands




	






tdrawer = Cfg("config/pythonplotter") # would come from DB
plotter = QuasiModule(tdrawer)

run     = ModuleRunner(plotter, args, options)
run.execute()

## internal cfg => determines what the code should do, and how the containers are written
## 


## how to run the plotter script?

## ingredients
###   => plotter command

## generate the plotter 


		

## group : name [: value [; options ]]
## process : tw 
## sample  : 2los
## morecut : 


class Cfg:
	def __init__(self, filepath=None):
		self.path   = filepath
		self.groups = []
		self.params = []
		self.load()
	def __getattr__(self, key):
		param = filter(lambda x: x.name==kye, self.params)
		if len(param)==1: return param[0]
		return None

##	def load(self):
## 324         if not self.path: return
## 325         classes        = listClasses()
## 326         self.objects   = []
## 327         self.variables = []
## 328         for line in open(self.path,"r"):
## 329             line = line.strip().strip("\n").strip()
## 330             if line[0:1]=="#" or len(line)==0: continue
## 331             sl   = [ss .strip() for ss  in line.split(":")]
## 332             ss   = [sss.strip() for sss in sl[1].split(";")]
## 333             if sl[0] in classes:
## 334                 varr = []; raw = []
## 335                 if len(ss)>1: raw = [ssss.strip() for ssss in ss[1].replace("\\,",";").split(",")]
## 336                 for opt in raw:
## 337                     ssl = opt.split("=")
## 338                     if len(ssl)==1: print "adding True to", ssl[0]; ssl.append("True")
## 339                     isList = (ssl[0][-1:]=="+")
## 340                     isDict = (ssl[0][-1:]=="#")




##class TreeDrawer:
##	def __init__(self, cfg, options):




	
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
	mm.iterateRegion()

	mccs    = mm.collectMCCs  ()
	macros  = mm.collectMacros()	
	flags   = mm.collectFlags (["flagsPlots"])
	ratio   = "--showRatio" if options.ratio else ""
	
	makes    = collectMakes(mm.region, options.make)
	plots    = collectPlots(mm.region, options.plots, options.customPlots)
	scenario = mm.getScenario(True)
	
	for p in plots:
		for m in makes:
			output = mm.outdir +"/plot/"+ scenario +"/"+ sl +"fb/"+ p +"/"+ m
			func.mkdir(output)
	
			procs   = collectProcesses(mm, m)
			pplots  = collectPPlots   (mm, p, options.customPlots)

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




