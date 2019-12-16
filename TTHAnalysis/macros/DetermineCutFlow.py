#!/usr/bin/python

import sys
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

# Read the cuts file so that we know which directories to check (and in which order) for yields.
cuts = []
ncuts=0
with open(str(sys.argv[2])) as fp:
	print '\nCuts:'
   	for line in fp:
   		line.strip()
		if line[:1]=="#":
			continue
		if line=="\n":
			continue
		else:
			cut = line.split(' ', 1)[0]
			print "\t"+str(ncuts+1)+" "+cut
			cuts.append(cut)
			ncuts=len(cuts)
print '\n'

# Build paths to the yields files
yields=[]
count=0
for cut in cuts:
	if count<10:
		cutcount="0"+str(count)
	else:
		cutcount=str(count)
	count+=1

	# build the path to text file with the yields. The last file to use is the final yields (one dir up)
	if count==len(cuts):
		yieldstxt=str(sys.argv[1])+"/yields.txt"
	else:
		yieldstxt=str(sys.argv[1])+"/cut_"+cutcount+"_"+cut+"/yields.txt"

	# Determine what masspoints were used
	masspoints=[]
	nMassPoints=0
	nAppended=0

	with open(yieldstxt) as yt:
		for line in yt:
			# print line
			if line.startswith("TChiWZ_"):
				masspoint=line.split(" ")[0]


				if cutcount=="00":
					yields.append([masspoint])
					nMassPoints=+1

				for yieldsline in yields:
					# print yieldsline
					if yieldsline[0]==masspoint:
						splitline = line.split(" ")
						# print splitline
						for i in range(len(splitline)):
							if splitline[i]==masspoint:
								continue
							elif splitline[i]=='':
								continue
							else:
								yieldsline.append(splitline[i])
								nAppended=+1
								break

	for i,yieldsline in enumerate(yields):
		if i>0:
			if len(yieldsline)!=len(yields[i-1]):
				yieldsline.append("0.00")



for yieldsline in yields:
	cuteffs = []
	for ic in range(len(cuts)+1):
		if ic>1:
			if float(yieldsline[ic-1])==0:
				cuteff=0
			else:
				cuteff=float(yieldsline[ic])/float(yieldsline[ic-1])
			cuteffs.append("{:.2f}".format(cuteff))
			# cuteff = str(1-round(cuteff,2))
	for ic in range(len(cuts)+1):
		if ic>0:
			yieldsline[ic] = float(yieldsline[ic])#/100
			yieldsline[ic] = "{:.2f}".format(yieldsline[ic])
		if ic>1:
			yieldsline[ic]=yieldsline[ic] + " (" + cuteffs[ic-2] + ")"

b = np.array(yields)

fig, ax = plt.subplots()
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')


ColumnNames = [i for i in range(ncuts+1)]
df = pd.DataFrame(b, columns=ColumnNames)
print df

ax.table(cellText=df.values, colLabels=df.columns, loc='center')
fig.tight_layout()
plt.savefig("plt.pdf")

pathtosavecvs=sys.argv[1]+"/CutFlow.csv"
export_csv = df.to_csv(pathtosavecvs, index = None, header=True) #Don't forget to add '.csv' at the end of the path