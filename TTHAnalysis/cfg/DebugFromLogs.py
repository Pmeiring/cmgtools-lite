from optparse import OptionParser
import subprocess


# bashCommand = "grep -rnw ./SkimsRemoved_191029/LepFromWZselection/logs/out.2853797.SMS_TChiWZ.* -e 'Event with\|Pre-select' > Debug.txt"
# process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE)
# output = process.communicate()

f = open('Debug.txt','r')

nEventsWith_3plus_FS_leptons=0
nTotalEvents = 0

for l in f:
	# print(l)
	res = l.split()
	# print res
	# print res[0]

	if res[0].endswith('Pre-select'):
		# print "here!"
		nTotalEvents = nTotalEvents + int(res[1])
	else:
		nEventsWith_3plus_FS_leptons = nEventsWith_3plus_FS_leptons+1

print('nEventsWith_3plus_FS_leptons: %s' %nEventsWith_3plus_FS_leptons)
print('nTotalEvents: %s'				 %nTotalEvents)

print('Fraction: %f' %(float(nEventsWith_3plus_FS_leptons)/float(nTotalEvents)))
