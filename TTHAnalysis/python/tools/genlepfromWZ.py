from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput

class GenLepFromWZ(Module):
    def __init__(self, label="", recllabel='Recl', doSystJEC=True):
        self.namebranches = [ "GenLep_FromWZ_Leading_pt",
                              "GenLep_FromWZ_SubLeading_pt",
                              "GenLep_Leading_pt",
                              "GenLep_SubLeading_pt",
                              "GenLep_2LOS_Leading_pt",
                              "GenLep_2LOS_Subleading_pt",
                              "GenLep_2LOS_FromZ_Leading_pt",
                              "GenLep_2LOS_FromZ_Subleading_pt",
                              "GenLep_2LOS_NotFromTau_Leading_pt",
                              "GenLep_2LOS_NotFromTau_Subleading_pt",
                              "GenLep_2LOS_FromZNotFromTau_Leading_pt",
                              "GenLep_2LOS_FromZNotFromTau_Subleading_pt",
                              "has2LOS",
                              "has2LOSfromWZ",
                              "has2LOSfromZ",
                              "has2LOSfromWZnotfromTau",
                              "has2LOSfromZnotfromTau",
                              "has3LfromWZ",
                              "has3LfromWZnotfromTau"
                            ]
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.inputlabel = '_'+recllabel
        self.branches = []
        # for var in self.systsJEC: self.branches.extend([br+self.label+self.systsJEC[var] for br in self.namebranches])
        for name in self.namebranches: self.branches.extend([name])

    # old interface (CMG)
    def listBranches(self):
        return self.branches[:]
    def __call__(self,event):
        return self.run(event, CMGCollection, "genlep_fromwz")

    # new interface (nanoAOD-tools)
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.branches)

    def analyze(self, event):
        writeOutput(self, self.run(event, NanoAODCollection, "GenLep_FromWZ"))
        return True


#genlep_pt      : if3(GenPart_genPartIdxMother!=-1 && abs(GenPart_pdgId[GenPart_genPartIdxMother])==23 && (abs(GenPart_pdgId)>10 && abs(GenPart_pdgId)<19) , GenPart_pt , -100) : 120,0,30  ; XTitle="GenLepton p_{T} [GeV]"     , Legend='TR', IncludeOverflows=False

    # logic of the algorithm
    def run(self,event,Collection,genLepname):
        allret = {}

        all_genpart = [gp for gp in Collection(event,"GenPart")]

        genLep = filter(lambda x : (abs(x.pdgId)==11 or abs(x.pdgId)==13) and x.status==1, all_genpart)

        # prepare output
        ret = dict([(name,0.0) for name in self.namebranches])
        index=-1
        # print("Number of final state leptons: ", len(all_genpart))
        LepFromWZ = []
        Lep = []


        for gp in all_genpart:
            # if index==-1:
            #     print("\nEvent")
            index=index+1

            # Incoming partons
            if gp.status==21:
                # print("Incoming parton: ",gp.pdgId)
                continue;

            # If we cannot determine the mother, continue;
            if gp.genPartIdxMother==-1:
                continue

            # Cheat to see what are the daughters of the Z (to cross-check)
            # if abs(all_genpart[gp.genPartIdxMother].pdgId)==23:
            #     print("Daughter of a Z-boson:   ",gp.pdgId,"    |   status: ",gp.status)


            # For all final state particles, build the family tree and print
            if all_genpart[index].status==1:
                # print("Final state particle     %i  |   %i     |   pt: %f" %(index, gp.pdgId, gp.pt))
                # Continue as long as the ultimate mother is not yet found.

                MotherIndex = index
                OGParentFound=0
                FamilyTree = []
                while not OGParentFound:
                    # Build the familty tree
                    if all_genpart[MotherIndex].pdgId not in FamilyTree:
                        FamilyTree.append(all_genpart[MotherIndex].pdgId)

                    # print("Particle in family-tree: %i  |   %i     |   pt: %f" %(MotherIndex, all_genpart[MotherIndex].pdgId, all_genpart[MotherIndex].pt))
                    
                    # Cycle back through the family tree
                    MotherIndex = all_genpart[MotherIndex].genPartIdxMother

                    # Check if the mother has a mother
                    OGParentFound = MotherIndex==-1               

                # print FamilyTree, gp.pt

                # Save the index and pt of leptons from W/Z
                isFromZ = (23 in FamilyTree and 1000023 in FamilyTree) 
                isFromW = (24 in FamilyTree and 1000024 in FamilyTree) or (-24 in FamilyTree and -1000024 in FamilyTree)
                isFromWZ = isFromW or isFromZ
                isFromTau = (15 in FamilyTree or -15 in FamilyTree)

                if ((abs(gp.pdgId)==11 or abs(gp.pdgId)==13) and isFromWZ):
                    LepFromWZ.append((index,gp.pt))
                    
                if (abs(gp.pdgId)==11 or abs(gp.pdgId)==13):
                    Lep.append((index,gp.pt,gp.pdgId,isFromZ,isFromTau,isFromW))
                    # print FamilyTree

        # Loop over all final state leptons and make pairs
        has2LOS = 0
        has2LOSfromWZ = 0
        has2LOSfromZ = 0
        has2LOSfromWZnotfromTau = 0
        has2LOSfromZnotfromTau = 0
        has3LfromWZ = 0
        has3LfromWZnotfromTau =0

        # print len(Lep)
        if len(Lep)>1:
            for i in range(0,len(Lep)):
                for j in [j for j in range(0,len(Lep)-1) if j!=i]:
                    # print i,j
                    PairIs2LOS = abs(Lep[i][2]+Lep[j][2]) < 3
                    PairIs2LOSfromWZ = PairIs2LOS and ((Lep[i][3] or Lep[i][5]) and (Lep[j][3] or Lep[j][5]))
                    PairIs2LOSFromZ = PairIs2LOSfromWZ and (Lep[i][3] and Lep[j][3])
                    PairIs2LOSfromWZnotfromTau = PairIs2LOSfromWZ and not Lep[i][4] and not Lep[j][4]
                    PairIs2LOSfromZnotfromTau = PairIs2LOSFromZ and PairIs2LOSfromWZnotfromTau

                    has2LOS = has2LOS or PairIs2LOS
                    has2LOSfromWZ = has2LOSfromWZ or PairIs2LOSfromWZ
                    has2LOSfromZ = has2LOSfromZ or PairIs2LOSFromZ
                    has2LOSfromWZnotfromTau = has2LOSfromWZnotfromTau or PairIs2LOSfromWZnotfromTau
                    has2LOSfromZnotfromTau = has2LOSfromZnotfromTau or PairIs2LOSfromZnotfromTau

                    if len(Lep)>2:
                        for k in [k for k in range(0,len(Lep)-2) if (k!=j and k!=i)]:
                            TripleFromWZ = (Lep[i][3] or Lep[i][5]) and (Lep[j][3] or Lep[j][5]) and (Lep[k][3] or Lep[k][5])
                            TripleFromWZnotfromTau = TripleFromWZ and not Lep[i][4] and not Lep[j][4] and not Lep[k][4]

                            has3LfromWZ = has3LfromWZ or TripleFromWZ
                            has3LfromWZnotfromTau = has3LfromWZnotfromTau or TripleFromWZnotfromTau

        # print Lep
        # print has2LOS,has2LOSfromWZ,has2LOSfromZ,has2LOSfromWZnotfromTau,has2LOSfromZnotfromTau
        # print has3LfromWZ,has3LfromWZnotfromTau




        LepFromWZ.sort(key=lambda Particle: Particle[1], reverse=True)        
        ret["GenLep_FromWZ_Leading_pt"]    = LepFromWZ[0][1] if len(LepFromWZ) > 1 else -100
        ret["GenLep_FromWZ_SubLeading_pt"] = LepFromWZ[1][1] if len(LepFromWZ) > 1 else -100


        Lep.sort(key=lambda Particle: Particle[1], reverse=True)
        hasTwoFinalStateLeptons = len(Lep) > 1
        LSubl_OS = hasTwoFinalStateLeptons and abs(Lep[0][2]+Lep[1][2]) < 3  # f.e. abs(13+-11)=2
        LSubl_FromZ = hasTwoFinalStateLeptons and Lep[0][3] and Lep[1][3]
        LSubl_NotfromTau = hasTwoFinalStateLeptons and not Lep[0][4] and not Lep[1][4]


        ret["GenLep_Leading_pt"]    = Lep[0][1] if hasTwoFinalStateLeptons else -100
        ret["GenLep_SubLeading_pt"] = Lep[1][1] if hasTwoFinalStateLeptons else -100

        ret["GenLep_2LOS_Leading_pt"] = Lep[0][1] if (hasTwoFinalStateLeptons and LSubl_OS) else -100
        ret["GenLep_2LOS_Subleading_pt"] = Lep[1][1] if (hasTwoFinalStateLeptons and LSubl_OS) else -100
        
        ret["GenLep_2LOS_FromZ_Leading_pt"] = Lep[0][1] if (hasTwoFinalStateLeptons and LSubl_OS and LSubl_FromZ) else -100
        ret["GenLep_2LOS_FromZ_Subleading_pt"] = Lep[1][1] if (hasTwoFinalStateLeptons and LSubl_OS and LSubl_FromZ) else -100

        ret["GenLep_2LOS_NotFromTau_Leading_pt"] = Lep[0][1] if (hasTwoFinalStateLeptons and LSubl_OS  and LSubl_NotfromTau) else -100
        ret["GenLep_2LOS_NotFromTau_Subleading_pt"] = Lep[1][1] if (hasTwoFinalStateLeptons and LSubl_OS and LSubl_NotfromTau) else -100

        ret["GenLep_2LOS_FromZNotFromTau_Leading_pt"] = Lep[0][1] if (hasTwoFinalStateLeptons and LSubl_OS and LSubl_FromZ and LSubl_NotfromTau) else -100
        ret["GenLep_2LOS_FromZNotFromTau_Subleading_pt"] = Lep[1][1] if (hasTwoFinalStateLeptons and LSubl_OS and LSubl_FromZ and LSubl_NotfromTau) else -100

        ret["has2LOS"] = has2LOS
        ret["has2LOSfromWZ"] = has2LOSfromWZ
        ret["has2LOSfromZ"] = has2LOSfromZ
        ret["has2LOSfromWZnotfromTau"] = has2LOSfromWZnotfromTau
        ret["has2LOSfromZnotfromTau"] = has2LOSfromZnotfromTau
        ret["has3LfromWZ"] = has3LfromWZ
        ret["has3LfromWZnotfromTau"] = has3LfromWZnotfromTau
        # print Lep






        for br in self.namebranches:
            allret[br+self.label] = ret[br]
	 	
	return allret


if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    tree.AddFriend("sf/t",argv[2])
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = EventVars2LSS('','Recl')
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

        
