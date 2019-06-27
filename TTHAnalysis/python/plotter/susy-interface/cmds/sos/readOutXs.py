import ROOT, sys, os

rpath = sys.argv[1]
opath = os.path.basename(rpath)

tf = ROOT.TFile.Open(rpath,"read")
rh = tf.Get("xs")

values = []

for b in range(1,rh.GetXaxis().GetNbins()):
	values.append([rh.GetBinCenter(b)-0.5*rh.GetBinWidth(b), 1000*rh.GetBinContent(b)/0.105, 1000*rh.GetBinError(b)/0.105])

tf.Close()

f = open(opath.replace(".root", ".txt"), "w")
for entry in values:
	f.write(" : ".join([str(e) for e in entry])+"\n")
f.close()
