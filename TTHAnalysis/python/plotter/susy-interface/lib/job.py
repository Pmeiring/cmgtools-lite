import os
from functions import *
import time

class Job():
	def __init__(self, master, name, commands, options, forceLocal = False, work = None, src = None):
		self.master     = master
		self.id         = "job"+timestamp(False)
		self.name       = name
		self.commands   = commands
		self.options    = options
		self.forceLocal = forceLocal
#		testqueue       = ["8nm", "1nh", "8nh", "1nd", "2nd", "1nw", "2nw"]
#		self.template   = "lxbatch_runner.sh"
		testqueue = ["espresso", "microcentury", "longlunch", "workday", "tomorrow", "testmatch", "nextweek"]
		self.template   = "htcondor_runner.sh"
		if "t3ui" in os.environ["HOSTNAME"]:
			testqueue = ["short.q", "all.q", "long.q"]
			self.template = "psibatch_runner.sh"
		elif "uniovi" in os.environ["HOSTNAME"]:
			testqueue = ["batch"]
			self.template = "oviedobatch_runner.sh"
		self.script     = self.master.srcpath +"/submitJob_"+name+".sh"
		self.HTCsub     = self.master.srcpath +"/HTCsub_"+name+".sh"
		if self.options.queue and not any([t in self.options.queue for t in testqueue]):
		#if self.options.queue and not self.options.queue in testqueue:
			self.master.error("Cannot find queue '"+self.options.queue+"' on this system.")
		self.prepare(work, src)
	def addCommands(self, commands):
		self.commands += commands
	def batchRuns(self):
		if hasattr(self, "batchDone"): return self.batchDone
#		if self.batchId==-1 or not self.options.queue: return False
		if not self.options.queue: return False
		if any([t in self.options.queue for t in ["all.q", "long.q", "short.q"]]):
		#if self.options.queue in ["all.q", "long.q", "short.q", "all.q@t3wn59.psi.ch"]:
			jobLine = bash("qstat -j "+str(self.batchId))
			toReturn = not(jobLine=="" or "Following jobs do not exist" in jobLine)
		elif any([t in self.options.queue for t in ["batch"]]):
		#elif self.options.queue in ["batch"]:
			jobLine = bash("qstat "+str(self.batchId))
			toReturn = not(jobLine=="" or "Unknown Job Id Error" in jobLine)
		elif any([t in self.options.queue for t in ["espresso", "microcentury", "longlunch", "workday", "tomorrow", "testmatch", "nextweek"]]):
			jobLine = bash("condor_q "+str(self.batchId)+" -af JobStatus")
			toReturn = not(jobLine=="" or jobLine=="3" or jobLine=="4") #jobStatus is not Removed (3) or Completed (4). Sumbission_error (6)?
		else:
			jobLine = bash("bjobs "+str(self.batchId))
			toReturn = not(jobLine=="" or "Job <"+str(self.batchId)+"> is not found" in jobLine)
		if toReturn: self.batchDone = True
		return toReturn
	def isDone(self):
		return os.path.exists(self.master.jobpath+"/"+self.id)
	def isError(self):
		stillRunning = self.batchRuns() # will be False for local job
		if stillRunning: return False
		if not os.path.exists(self.master.jobpath+"/"+self.id): return True
		return os.path.exists(self.master.jobpath+"/err_"+self.id)
	def prepare(self, work = None, src = None):
		## PLACEHOLDER is replaced later
		template = [l.strip("\n") for l in open("susy-interface/scripts/"+self.template).readlines()]
		f = open(self.script, "w")
		for line in template:
			line = line.replace("[WORK]"       , work if work else self.master.workdir     )
			line = line.replace("[SRC]"        , src  if src  else self.master.cmssw+"/src")
			line = line.replace("[INST]"       , self.master.instance                      )
			line = line.replace("[JOBDIR]"     , self.master.jobpath                       )
			line = line.replace("[JOBID]"      , self.id                                   )
			line = line.replace("[EMAIL]"      , self.master.options.email                 )
			f.write(line+"\n")
		f.close()
	def prepareCommands(self):
		replaceInFile(self.script, "[PLACEHOLDER]", "\n".join([b for b in self.commands]))
		cmd("chmod 755 "+self.script)
		cmd("chmod 755 "+self.master.jobpath)
	def run(self):
		self.prepareCommands() # here, because of the add commands method
		if self.options.queue and not self.forceLocal:
			print "submitting to queue"
			super = "bsub -q {queue} -J SPM_{name} "
			if any([t in self.options.queue for t in ["all.q", "long.q", "short.q"]]):
			#if self.options.queue in ["all.q", "long.q", "short.q", "all.q@t3wn59.psi.ch"]:
				super = "qsub -q {queue} -N SPM_{name} "
				super += "-o {dir}/submitJob_{name}.out -e {dir}/submitJob_{name}.err "
				super = super.format(queue=self.options.queue, name=self.name, dir=self.master.logpath)
				self.batchId = self.runCmd(super + self.script)
			elif any([t in self.options.queue for t in ["batch"]]):
			#elif self.options.queue in ["batch"] and os.path.isdir('/pool/ciencias/'):
				super = "qsub -q {queue} -N SPM_{name} "
				super += "-o {dir}/submitJob_{name}.out -e {dir}/submitJob_{name}.err "
				super = super.format(queue=self.options.queue, name=self.name, dir=self.master.logpath)
				self.batchId = self.runCmd(super + self.script)
			elif any([t in self.options.queue for t in ["espresso", "microcentury", "longlunch", "workday", "tomorrow", "testmatch", "nextweek"]]):
				template = [l.strip("\n") for l in open("susy-interface/scripts/htcondor_submitter.sh").readlines()]
				f = open(self.HTCsub, "w")
				for line in template:
					line = line.replace("[SCRIPT]"       , self.script   )
					line = line.replace("[NAME]"       , self.name   )
					line = line.replace("[QUEUE]"       , '"'+self.options.queue+'"'   )
					line = line.replace("[DIR]"       , self.master.logpath   )
					f.write(line+"\n")
				f.close()
				super = "condor_submit "+str(self.HTCsub)
				self.runCmd(super)
				##to be fixed for monitoring htcondor jobs
				jobIdCmd = "condor_wait %s/job.%s.log -status -wait 0.01" % (self.master.logpath, self.name)
				jobIdOut = bash(jobIdCmd)
				print "wait out ",jobIdOut
				if jobIdOut == "":
					print "jobIdOut is empty"
					ntry=0
					while(ntry<5 and jobIdOut==""):
						print "sleeping 1 and trying again for the %s time"%ntry
						time.sleep(1)
						jobIdOut = bash(jobIdCmd)
						ntry=ntry+1
						print "now jobIdOut is", jobIdOut
					
				if jobIdOut == "":
					print "Could not set job Id for this job, setting to 0"
					self.batchId = 0
				else:
					self.batchId = jobIdOut.split()[0][:-2]
				print "condor jobId ",self.batchId
				
		else:
			print "running locally, sourcing"
			super = "source "
			self.batchId = self.runCmd(super + self.script)
	def runCmd(self, theCmd):
		print "running command ",theCmd
###		jobLine = bash(theCmd)
		jobLine = cmd(theCmd)
		theId   = -1
		if not self.options.queue or self.forceLocal: return theId
		if   any([t in self.options.queue for t in ["all.q", "long.q", "short.q"]]): theId=int(jobLine.split()[2])
		elif any([t in self.options.queue for t in ["batch"]                     ]): theId=int(jobLine.split('.')[0])
		#if   self.options.queue in ["all.q", "long.q", "short.q"]                : theId=int(jobLine.split()[2])
		#elif self.options.queue in ["batch"] and os.path.isdir('/pool/ciencias/'): theId=int(jobLine.split('.')[0])
		###else: theId = int(jobLine.split()[1].strip("<").strip(">"))
		else: theId = 0
		return theId




