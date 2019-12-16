import csv
import sys
import pandas
import numpy as np
import pandas as pd


df_ee = pandas.read_csv(sys.argv[1]+"/CutFlow.csv")
df_mm = pandas.read_csv(sys.argv[2]+"/CutFlow.csv")

dummy = []

print df_ee
print df_mm

ncolumns=0
nrows=0
for x_index, row in df_ee.iterrows():
	for y_index in range(len(row)):
		ee_value = df_ee.iat[x_index,y_index]
		mm_value = df_mm.iat[x_index,y_index]

		if ee_value!=mm_value:
			dummy.append(ee_value+"\n"+mm_value)
		else:
			dummy.append(ee_value)
		# print df_ee.iat[x_index,y_index]
		# print df_mm.iat[x_index,y_index]
		# if dummy.append[]

# print dummy
eemm = np.array(dummy)
eemm = eemm.reshape(df_ee.shape[0],df_ee.shape[1])
# print eemm

ColumnNames = [i for i in range(df_ee.shape[1])]
df = pd.DataFrame(eemm, columns=ColumnNames)

pathtosavecvs=sys.argv[1]+"/CutFlowMerged.csv"
export_csv = df.to_csv(pathtosavecvs, index = None, header=True) #Don't forget to add '.csv' at the end of the path

print df
