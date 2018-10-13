import re

theTest ="""
for sample in $(samples):
	print sample
    #if not "dy" in sample.datasets: continue
    #frstring = ", FakeRate=\""+",".join(sample.samplesfrs)+"\""
    #print sample.datasets +":"+ "+".join(sample.samplescomponent) +":"+ sample.samplesnorm +"; Label=\""+sample.samplelegend+"\", FillColor=\""+sample.samplescolor+"\", "+ frstring
"""

samples = ["a", "list", "of", "string", "entries"]
theList = ["samples", "datasets", "otherstuff"]

print any(["$("+elm+")" in theTest for elm in theList])

for elm in theList:
	theTest = theTest.replace("$("+elm+")", elm)
theTest = theTest.replace("print ", "theBuffer += ")
print theTest
print "-"*25
theBuffer = ""
exec(theTest)
print theBuffer
