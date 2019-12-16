#!/usr/bin/python
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F, TGraph, TGraphErrors, TMacro
from ROOT import gROOT, gBenchmark, gRandom, gSystem, Double

from array import array
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
staterror=[]

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

	# Open the input text file on cernbox, containing the yields
	with open(yieldstxt) as yt:
		# Loop over the lines
		for line in yt:
			# print line
			# Only treat lines that actually contain yields per mass point
			if line.startswith("TChiWZ_"):
				masspoint=line.split(" ")[0]

				# Only for the very first cut ("allways true" probably), add the title/masspoint in the first column (first cell of each row)
				if cutcount=="00":
					yields.append([masspoint])
					staterror.append([masspoint])
					nMassPoints=+1

				# Loop over the lines already in the output matrix, to see in which line we should append yields
				for j,yieldsline in enumerate(yields):
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
						staterror[j].append(splitline[len(splitline)-2])


	for i,yieldsline in enumerate(yields):
		if i>0:
			if len(yieldsline)!=len(yields[i-1]):
				yieldsline.append("0.00")
				staterror[i].append("0.00")

# print yields
# print staterror

for i,yieldsline in enumerate(yields):
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
			yieldsline[ic] = "{:.2f}".format(yieldsline[ic]) + " +- " + staterror[i][ic]
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

# ax.table(cellText=df.values, colLabels=df.columns, loc='center')
# fig.tight_layout()
# plt.savefig("plt.pdf")

pathtosavecvs=sys.argv[1]+"/CutFlow.csv"
export_csv = df.to_csv(pathtosavecvs, index = None, header=True) #Don't forget to add '.csv' at the end of the path




hfile = TFile(sys.argv[1]+"/Trial_CutFlow.root", 'RECREATE')

ma = TMacro()
for cut in cuts:
	ma.AddLine(cut)
ma.SetName("Cuts")
ma.Write()

y=[]
x=[]
dy=[]
dx=[]
eff=[]
dy_eff=[]

name = "dummyname"
for x_index, row in df.iterrows():
	for y_index in range(len(row)):
		value = df.iat[x_index,y_index]

		if value.startswith("TChiWZ_"):
			name = value
		else:
			# print value.split(" ")
			y.append(float(value.split(" ")[0]))
			dy.append(float(value.split(" ")[2]))
			x.append(y_index)
			dx.append(0.5)

			dy_eff.append(0.001)

			if y_index==1:
				eff.append(1)
			else:
				# print x_index, y_index
				cut_eff = value.split(" ")[3]
				cut_eff = cut_eff.replace('(','')
				cut_eff = cut_eff.replace(')','')
				eff.append(float(cut_eff))

		if y_index==ncuts:
			gr = TGraphErrors( ncuts, array( 'f',x), array( 'f',y), array( 'f',dx), array( 'f',dy) )
			gr.SetTitle("CutFlow " + name)
			gr.SetName(name)
			# gr.Draw()
			gr.Write()
			# print eff
			gr_eff = TGraphErrors( ncuts, array( 'f',x), array( 'f',eff), array( 'f',dx), array( 'f',dy_eff) )
			gr_eff.SetTitle("Cut-Eff. " + name)
			gr_eff.SetName("Eff_" + name)
			# gr_eff.Draw()
			gr_eff.Write()

			y=[]
			x=[]
			dy=[]
			dx=[]
			eff=[]

hfile.Write()
hfile.Close()

