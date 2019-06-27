import os

keep = []
for line in open("TChiWZ.txt","r").readlines():
	sl = [ss.strip() for ss in line.split(":")]
	if os.path.exists("/data1/botta/trees_SOS_010217/0_eventShapeWeight_v2/evVarFriend_"+sl[2].rstrip("\n").strip()+".root"):
		keep.append(line)

f = open("TChiWZ_pruned.txt","w")
for line in keep:
	f.write(line)
f.close()
