from optparse import OptionParser
import subprocess

parser = OptionParser(usage="%prog [options] <pathtotrees> ")
# common options, independent of the flavour chosen
parser.add_option("-d", "--dataset", dest="pathtotrees",  type="string", default=[], action="append", help="Count the entries in this directory");
(options, args) = parser.parse_args()

if args:
	print(options.pathtotrees)

	bashCommand = "grep -rnw " + args[0] + "/SMS_*/condor_job_0.out -e \"Finally selected\" > preselected.txt"
	process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE)
	output = process.communicate()

	# print output

	f = open('preselected.txt','r')

	totalpreselect=0
	totaltotal=0
	totalfinalselect=0
	for l in f:
		print(l)
		res = l.split()
		# print res
		# print res[6]
		total = int(res[6].replace('(',''))
		preselect = int(res[1])
		finalselect=int(res[10])
		totaltotal=totaltotal+total
		totalpreselect=totalpreselect+preselect
		totalfinalselect=totalfinalselect+finalselect

	print('Pre-selected entries: %s' %totalpreselect)
	print('Total amount of entries: %s' %totaltotal)
	print('Final amount of entries: %s' %totalfinalselect)
	
	# print bashCommand

else:
	print("No path specified")