from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput

class GenLepFromWZ_Collection(Module):
    def __init__(self, label="", recllabel='Recl', doSystJEC=True):
        self.namebranches = [   "nGenLepFromWZ",
                                "EvHas_OSSFpair",
                                "EvHas2LOSSF_FromZ_tau",
                                "EvHas2LOS_notSF_FromZ_tau",
                                "EvHas2LOSSF_FromZ_notau",
                                "EvHas2LOSSF_FromWZ_tau",
                                "EvHas2L_notOSSF_FromWZ_tau",
                                "EvHas3L_FromWZ_notau",
                                "EvHas3L_FromWZ_tau",
                                "EvHas3L_notOSSF_FromWZ_tau",
                                "Z_decays",
                                "Ztau_decays",
                                "W_decays",
                                "Wtau_decays"
                                # "nTauFromZ",
                                # "nTauFromZ_l",
                                # "nTauFromZ_h",
                                # "nTauFromW",
                                # "nTauFromW_l",
                                # "nTauFromW_h"                                
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
        self.out = wrappedOutputTree
        self.out.branch("GenLepFromWZ_pt", "F", 3)
        self.out.branch("GenLepFromWZ_eta", "F", 3)
        self.out.branch("GenLepFromWZ_phi", "F", 3)
        self.out.branch("GenLepFromWZ_id", "I", 3)
        self.out.branch("GenLepFromWZ_charge", "I", 3)
        self.out.branch("GenLepFromWZ_isFromZ", "I", 3)
        self.out.branch("GenLepFromWZ_isFromTau", "I", 3)

        declareOutput(self, wrappedOutputTree, self.branches)

    def analyze(self, event):
        writeOutput(self, self.run(event, NanoAODCollection, "GenLep_FromWZ"))
        return True

    # def HadronInWdecay(self, FamilyTree):
    #     counter = 0
    #     IndexOfBoson=-1
    #     for l in FamilyTree:
    #         if abs(l)==24:
    #             IndexOfW=counter
    #             if (FamilyTree[IndexOfW-1]) in {11, 13, 15}:
    #                 #W decays to e/mu/tau, now check if tau decays leptonically
    #                 return 0 
    #         counter=counter+1
    #     return 1

    def IsPrompt(self, FamilyTree):
        if len(FamilyTree)<2:
            print FamilyTree
            return 0
        if abs(FamilyTree[1]) in {23,24}:       # Final state lepton is direct daughter of Z or W
            return 1
        elif abs(FamilyTree[1]) == 15:          # If Final state lepton is dauchter of tau
            if len(FamilyTree)<3:
                print FamilyTree
                return 0

            if abs(FamilyTree[2]) in {23,24}:   # If the tau is direct daughter of Z or W, the lepton is still prompt
                return 1
            else:
                return 0
        else:
            return 0 

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
        LepFromWZ_FamilyTrees = []

        Z_daughters = []
        W_daughters = []

        # Track the tau decays from W and Z
        nTauFromZ=0
        nTauFromZ_h=0
        nTauFromZ_l=0        
        nTauFromW=0
        nTauFromW_h=0
        nTauFromW_l=0

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
            if abs(all_genpart[gp.genPartIdxMother].pdgId)==23:
                # print("Daughter of a Z-boson:   ",gp.pdgId,"    |   status: ",gp.status,"    |   index: ",index)
                Z_daughters.append(gp.pdgId)
                if (abs(gp.pdgId)==15):
                    nTauFromZ+=1

            
            if abs(all_genpart[gp.genPartIdxMother].pdgId)==24:
                # print("Daughter of a W-boson:   ",gp.pdgId,"    |   status: ",gp.status)
                W_daughters.append(gp.pdgId)
                if (abs(gp.pdgId)==15):
                    nTauFromW+=1

            # print("Particle     %i  |   %i     |   pt: %f" %(index, gp.pdgId, gp.pt))

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

                isFromZ = (23 in FamilyTree and 1000023 in FamilyTree) 
                isFromW = (24 in FamilyTree and 1000024 in FamilyTree) or (-24 in FamilyTree and -1000024 in FamilyTree)
                isFromWZ = isFromW or isFromZ
                isFromTau = (15 in FamilyTree or -15 in FamilyTree)
                isPrompt = self.IsPrompt(FamilyTree)


                # if ((abs(gp.pdgId)==11 or abs(gp.pdgId)==13)):
                #     print "f.s. lep: ",isPrompt, FamilyTree, (index,gp.pt,gp.pdgId,isFromZ,isFromTau)
              
                if ((abs(gp.pdgId)==11 or abs(gp.pdgId)==13) and isFromWZ and isPrompt):
                    LepFromWZ.append((index,gp.pt,gp.pdgId,isFromZ,isFromTau,gp.eta,gp.phi))
                    LepFromWZ_FamilyTrees.append((FamilyTree))
                    # print "f.s. lep: ",isPrompt, FamilyTree, (index,gp.pt,gp.pdgId,isFromZ,isFromTau)

        # Sort based on the particle pt
        LepFromWZ.sort(key=lambda Particle: Particle[1], reverse=True)        

        # DEBUG: events with > 3 prompt leptons in fs. | Overwrite if this is the case..
        if len(LepFromWZ)>3:
            print "Event with >3 f.s. leptons"
            # print LepFromWZ
            LepFromWZ = []


        ret["nGenLepFromWZ"] = len(LepFromWZ)

        for i in range(3-len(LepFromWZ)):
            # print "Length = ",len(LepFromWZ),", appending dummy..."
            LepFromWZ.append((-100,-100,-100,-100,-100,-100,-100,-100))


        GenLepFromWZ_id =       list(LepFromWZ[l][2] for l in range(len(LepFromWZ)))
        GenLepFromWZ_charge =   list(1 if LepFromWZ[l][2]>0 else -1 for l in range(len(LepFromWZ)))
        GenLepFromWZ_isFromZ =  list(LepFromWZ[l][3] for l in range(len(LepFromWZ)))
        GenLepFromWZ_isFromTau =list(LepFromWZ[l][4] for l in range(len(LepFromWZ)))

        self.out.fillBranch("GenLepFromWZ_pt",          list(LepFromWZ[l][1] for l in range(len(LepFromWZ))))
        self.out.fillBranch("GenLepFromWZ_eta",         list(LepFromWZ[l][5] for l in range(len(LepFromWZ))))
        self.out.fillBranch("GenLepFromWZ_phi",         list(LepFromWZ[l][6] for l in range(len(LepFromWZ))))
        self.out.fillBranch("GenLepFromWZ_id",          list(LepFromWZ[l][2] for l in range(len(LepFromWZ))))
        self.out.fillBranch("GenLepFromWZ_charge",      list(1 if LepFromWZ[l][2]>0 else -1 for l in range(len(LepFromWZ))))
        self.out.fillBranch("GenLepFromWZ_isFromZ",     list(LepFromWZ[l][3] for l in range(len(LepFromWZ))))
        self.out.fillBranch("GenLepFromWZ_isFromTau",   list(LepFromWZ[l][4] for l in range(len(LepFromWZ))))

        ret["EvHas_OSSFpair"]=0
        ret["EvHas2LOS_FromZ_tau"]=0
        ret["EvHas2LOS_FromZ_notau"]=0
        ret["EvHas2LOS_FromWZ_tau"]=0
        ret["EvHas3L_FromWZ_notau"]=0
        ret["EvHas3L_FromWZ_tau"]=0

        ret["EvHas2LOS_notSF_FromZ_tau"]=0
        ret["EvHas2L_notOSSF_FromWZ_tau"]=0
        ret["EvHas3L_notOSSF_FromWZ_tau"]=0

        # Case of 2L
        if GenLepFromWZ_id[1]!=-100 and GenLepFromWZ_id[2]==-100:
            # Require opposite sign
            if GenLepFromWZ_charge[0]+GenLepFromWZ_charge[1]==0:
                #Require same flavor
                if abs(GenLepFromWZ_id[0])==abs(GenLepFromWZ_id[1]):
                    # print "2LOSSF!"
                    ret["EvHas_OSSFpair"]=1
                    if GenLepFromWZ_isFromZ[0]==1 and GenLepFromWZ_isFromZ[1]==1:
                        if 1 in GenLepFromWZ_isFromTau:
                            ret["EvHas2LOSSF_FromZ_tau"]=1
                        else:
                            ret["EvHas2LOSSF_FromZ_notau"]=1
                    else:
                        ret["EvHas2LOSSF_FromWZ_tau"]=1
                
                else:
                    if GenLepFromWZ_isFromZ[0]==1 and GenLepFromWZ_isFromZ[1]==1:
                        if 1 in GenLepFromWZ_isFromTau:
                            ret["EvHas2LOS_notSF_FromZ_tau"]=1    # <- blue   (Z->tautau->l+l, W->(tau->)h) 
                    else:
                        if 1 in GenLepFromWZ_isFromTau:
                            ret["EvHas2L_notOSSF_FromWZ_tau"]=1   # <- purple   (Z->tautau->l+h, W->(tau->)l) 
            else:
                ret["EvHas2L_notOSSF_FromWZ_tau"]=1    # <- purple   (Z->tautau->l+h, W->(tau->)l)         


        # Case of 3L
        if GenLepFromWZ_id[1]!=-100 and GenLepFromWZ_id[2]!=-100:
            # Require a pair with OSSF
            if (GenLepFromWZ_id[0]+GenLepFromWZ_id[1]==0) or (GenLepFromWZ_id[1]+GenLepFromWZ_id[2]==0) or (GenLepFromWZ_id[0]+GenLepFromWZ_id[2]==0):
                # print "3L with OSSF-pair!"
                ret["EvHas_OSSFpair"]=1
                if 1 in GenLepFromWZ_isFromTau:
                    ret["EvHas3L_FromWZ_tau"]=1
                else:
                    ret["EvHas3L_FromWZ_notau"]=1
            else:
                ret["EvHas3L_notOSSF_FromWZ_tau"]=1     # <- orange   (Z->tautau->l+l, W->(tau->)l)



        if (nTauFromZ>0 or nTauFromW>0):
            for l in range(3):
                # print(LepFromWZ[l][3],LepFromWZ[l][4])
                if (LepFromWZ[l][3]==1 and LepFromWZ[l][4]==1):         #lepton is from Z and from tau (Z->tau->l)
                    nTauFromZ_l+=1
                    # print("Z->tau->l")
                elif (LepFromWZ[l][3]==1 and LepFromWZ[l][4]!=1):       #lepton is from Z but not from tau (Z->l), we don't care
                    # print("Z->l")
                    continue 
                elif (LepFromWZ[l][3]!=1 and LepFromWZ[l][4]==1):   #lepton is not from Z, but is from tau (W->tau->l)
                    nTauFromW_l+=1
                    # print("W->tau->l")                    
                else:                                           #lepton is not from Z and not from tau (W->l), we don't care
                    # print("W->l")
                    continue
            nTauFromZ_h = nTauFromZ - nTauFromZ_l
            nTauFromW_h = nTauFromW - nTauFromW_l


        if (nTauFromZ_h==2 and nTauFromZ_l==0):
            ret["Ztau_decays"]=1502     #2 hadronic taus from Z
        elif (nTauFromZ_h==1 and nTauFromZ_l==1):
            ret["Ztau_decays"]=1501     #1 hadronic taus from Z
        elif (nTauFromZ_h==0 and nTauFromZ_l==2):
            ret["Ztau_decays"]=1500     #0 hadronic taus from Z
        elif (nTauFromZ_h==0 and nTauFromZ_l==0):
            ret["Ztau_decays"]=0        # no taus from Z
        else:
            print("Found unkown decay for Z->tautau",nTauFromZ,nTauFromZ_h,nTauFromZ_l,LepFromWZ_FamilyTrees)
            ret["Ztau_decays"]=0

        if (nTauFromW_h==1 and nTauFromW_l==0):
            ret["Wtau_decays"]=1501     #1 hadronic taus from W 
        elif (nTauFromW_h==0 and nTauFromW_l==1):
            ret["Wtau_decays"]=1500     #0 hadronic taus from W
        elif (nTauFromW_h==0 and nTauFromW_l==0):
            ret["Wtau_decays"]=0     #0 no taus from W
        else:
            print("Found unkown decay for W->tauv",nTauFromW,nTauFromW_h,nTauFromW_l,LepFromWZ_FamilyTrees)
            ret["Wtau_decays"]=0




        if (11 in Z_daughters and -11 in Z_daughters):
            ret["Z_decays"]=1111
        elif (13 in Z_daughters and -13 in Z_daughters):
            ret["Z_decays"]=1313
        elif (15 in Z_daughters and -15 in Z_daughters):
            ret["Z_decays"]=1515
        else:
            print("Found unknown Z decay!")
            ret["Z_decays"]=0

        if   ((6 in W_daughters and -5 in W_daughters) or (-6 in W_daughters and 5 in W_daughters)):
            ret["W_decays"]=65
        elif ((6 in W_daughters and -3 in W_daughters) or (-6 in W_daughters and 3 in W_daughters)):
            ret["W_decays"]=63    
        elif ((6 in W_daughters and -1 in W_daughters) or (-6 in W_daughters and 1 in W_daughters)):
            ret["W_decays"]=61
        elif ((4 in W_daughters and -5 in W_daughters) or (-4 in W_daughters and 5 in W_daughters)):
            ret["W_decays"]=45    
        elif ((4 in W_daughters and -3 in W_daughters) or (-4 in W_daughters and 3 in W_daughters)):
            ret["W_decays"]=43        
        elif ((4 in W_daughters and -1 in W_daughters) or (-4 in W_daughters and 1 in W_daughters)):
            ret["W_decays"]=41    
        elif ((2 in W_daughters and -5 in W_daughters) or (-2 in W_daughters and 5 in W_daughters)):
            ret["W_decays"]=25
        elif ((2 in W_daughters and -3 in W_daughters) or (-2 in W_daughters and 3 in W_daughters)):
            ret["W_decays"]=23
        elif ((2 in W_daughters and -1 in W_daughters) or (-2 in W_daughters and 1 in W_daughters)):
            ret["W_decays"]=21
        elif ((15 in W_daughters and -16 in W_daughters) or (-15 in W_daughters and 16 in W_daughters)):
            ret["W_decays"]=1516
        elif ((13 in W_daughters and -14 in W_daughters) or (-13 in W_daughters and 14 in W_daughters)):
            ret["W_decays"]=1314
        elif ((11 in W_daughters and -12 in W_daughters) or (-11 in W_daughters and 12 in W_daughters)):
            ret["W_decays"]=1112            
        else:
            print("Found unknown W decay! ",W_daughters)
            ret["W_decays"]=0
       
        # ret["nTauFromZ"]  =nTauFromZ
        # ret["nTauFromZ_l"]=nTauFromZ_l
        # ret["nTauFromZ_h"]=nTauFromZ_h
        # ret["nTauFromW"]  =nTauFromW
        # ret["nTauFromW_l"]=nTauFromW_l
        # ret["nTauFromW_h"]=nTauFromW_h

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

        
