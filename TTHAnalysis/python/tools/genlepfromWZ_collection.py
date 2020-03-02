from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput

class GenLepFromWZ_Collection(Module):
    def __init__(self, label=""):
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
                            ]
        self.label = "" if (label in ["",None]) else ("_"+label)
        # self.inputlabel = '_'+recllabel
        self.branches = []
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

        self.out.branch("GenTauFromZ_pt", "F", 2)
        self.out.branch("GenTauFromZ_eta", "F", 2)
        self.out.branch("GenTauFromZ_phi", "F", 2)

        declareOutput(self, wrappedOutputTree, self.branches)
        self.inputTree = inputTree

    def analyze(self, event):
        writeOutput(self, self.run(event, NanoAODCollection, "GenLep_FromWZ"))
        return True

    # Function to determine what to print
    def Log(self,message,v):
        verbosity = 0 #0:nothing, 1:event info, 2:specific particles, 3:all particles
        if v<=verbosity:
            print(message)

    # Function to determine if particle is prompt, based on its family tree. 
    def IsPrompt(self, FamilyTree):
        if len(FamilyTree)<2:
            print "WARNING: Found particle that has no family:", FamilyTree
            return 0
        if abs(FamilyTree[1]) in {23,24}:       # Final state lepton is direct daughter of Z or W
            return 1
        elif abs(FamilyTree[1]) == 15:          # If Final state lepton is daughter of tau
            if len(FamilyTree)<3:
                print "WARNING: Found particle from tau that has no family:", FamilyTree
                return 0
            if abs(FamilyTree[2]) in {23,24}:   # If the tau is direct daughter of Z or W, the lepton is still prompt
                return 1
            else:
                return 0
        else:
            return 0 

    # Function that loops back through the gen-particle family tree and makes the list of corresponding ids
    def BuildFamilyTree(self, i, allgenpart):
        MotherIndex = i
        OGParentFound=0
        family_tree = []

        # Continue as long as the ultimate mother is not yet found.
        while not OGParentFound:
            # Build the familty tree
            if allgenpart[MotherIndex].pdgId not in family_tree:
                family_tree.append(allgenpart[MotherIndex].pdgId)
                self.Log("Particle in family-tree:\t %d \t|\tid: %d   \t|\tpt: %f" % (MotherIndex, allgenpart[MotherIndex].pdgId, allgenpart[MotherIndex].pt), 3)

            # Cycle back through the family tree
            MotherIndex = allgenpart[MotherIndex].genPartIdxMother

            # Check if the mother has a mother
            OGParentFound = MotherIndex==-1         

        return family_tree


    # Function to categorize the events, see:
    # https://indico.cern.ch/event/870087/contributions/3669284/attachments/1959791/3256711/MCsignal_study_lowDM.pdf 
    def Prepare_2l3l_categories_returns(self, ret, GenLepFromWZ_id, GenLepFromWZ_charge, GenLepFromWZ_isFromZ, GenLepFromWZ_isFromTau):
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

        return ret           


    def Prepare_WZtoTau_decays_returns(self, ret, nTauFromZ, nTauFromW, LepFromWZ):
        nTauFromW_h=0
        nTauFromW_l=0
        nTauFromZ_h=0
        nTauFromZ_l=0 

        if (nTauFromZ>0 or nTauFromW>0):
            for l in range(3):
                if (LepFromWZ[l][3]==1 and LepFromWZ[l][4]==1):         #lepton is from Z and from tau (Z->tau->l)
                    nTauFromZ_l+=1
                elif (LepFromWZ[l][3]==1 and LepFromWZ[l][4]!=1):       #lepton is from Z but not from tau (Z->l), we don't care
                    continue 
                elif (LepFromWZ[l][3]!=1 and LepFromWZ[l][4]==1):       #lepton is not from Z, but is from tau (W->tau->l)
                    nTauFromW_l+=1
                else:                                                   #lepton is not from Z and not from tau (W->l), we don't care
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
            # print("Found unkown decay for Z->tautau",nTauFromZ,nTauFromZ_h,nTauFromZ_l,LepFromWZ_FamilyTrees)
            ret["Ztau_decays"]=0

        if (nTauFromW_h==1 and nTauFromW_l==0):
            ret["Wtau_decays"]=1501     #1 hadronic taus from W 
        elif (nTauFromW_h==0 and nTauFromW_l==1):
            ret["Wtau_decays"]=1500     #0 hadronic taus from W
        elif (nTauFromW_h==0 and nTauFromW_l==0):
            ret["Wtau_decays"]=0     #0 no taus from W
        else:
            # print("Found unkown decay for W->tauv",nTauFromW,nTauFromW_h,nTauFromW_l,LepFromWZ_FamilyTrees)
            ret["Wtau_decays"]=0

        return ret


    def Prepare_WZ_decays_returns(self, ret, Z_daughters, W_daughters):

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

        return ret



    # logic of the algorithm
    def run(self,event,Collection,genLepname):

        # Put the generator particles in a list so we can loop over it
        all_genpart = [gp for gp in Collection(event,"GenPart")]

        # EventsTree = self.inputTree 
        # # genmodel = [gm for gm in Collection(event,"GenModel"+self.systsJEC[_var],"nJet"+self.systsJEC[_var])]
        # genmodels = ["GenModel_TChiWZ_ZToLL_100_80"]
        
        # # print listBranches
        # isgm = 0
        # for gm in genmodels:
        #     print "here"
        #     print EventsTree.Scan(gm)
        #     # gmBranch = EventsTree.GetBranch(gm)
        #     # EventsTree.SetBranchAddress(gm, isgm)
        #     # EventsTree.GetEntry()
        #     # if isgm==1: print isgm
        #     # isgenmodel = getattr(event,gmBranch)
        # #     print gm, isgenmodel

        # # objarray = ROOT.TObjArray(self.inputTree)

        # prepare output
        ret = dict([(name,0.0) for name in self.namebranches])
        
        LepFromWZ = []
        # LepFromWZ_FamilyTrees = []

        Z_daughters = []
        W_daughters = []

        # Track the tau decays from W and Z
        nTauFromZ=0
        TauFromZ = []    
        nTauFromW=0

        # Loop over all generator particles
        for index,gp in enumerate(all_genpart):

            # Incoming partons have status 21; We don't care about these particles
            if gp.status==21:
                continue;

            # If we cannot determine the mother, continue;
            if gp.genPartIdxMother==-1:
                continue

            # Z-Boson daughters
            if abs(all_genpart[gp.genPartIdxMother].pdgId)==23:
                self.Log("Daughter of a Z-boson:\t %d \t|\tid: %d   \t|\tstatus: %d" % (index, gp.pdgId, gp.status),2)
                Z_daughters.append(gp.pdgId)
                if (abs(gp.pdgId)==15):
                    TauFromZ.append((gp.pt,gp.eta,gp.phi))
                    nTauFromZ+=1

            # W-Boson daughters
            if abs(all_genpart[gp.genPartIdxMother].pdgId)==24:
                self.Log("Daughter of a W-boson:\t %d \t|\tid: %d   \t|\tstatus: %d" % (index, gp.pdgId, gp.status),2)
                W_daughters.append(gp.pdgId)
                if (abs(gp.pdgId)==15):
                    nTauFromW+=1

            # For all final state particles, build the family tree and print
            if all_genpart[index].status==1:
                self.Log("Final state particle:\t %d \t|\tid: %d   \t|\tpt: %f" % (index, gp.pdgId, gp.pt), 3)

                # Determine the familytree
                FamilyTree = self.BuildFamilyTree(index,all_genpart)
    
                # Determine some properties regarding origin
                isFromZ = (23 in FamilyTree and 1000023 in FamilyTree) 
                isFromW = (24 in FamilyTree and 1000024 in FamilyTree) or (-24 in FamilyTree and -1000024 in FamilyTree)
                isFromWZ = isFromW or isFromZ
                isFromTau = (15 in FamilyTree or -15 in FamilyTree)
                isPrompt = self.IsPrompt(FamilyTree)

                # Build the LepFromWZ list, which contains only electrons/muons that are from W/Z and prompt
                if ((abs(gp.pdgId)==11 or abs(gp.pdgId)==13) and isFromWZ and isPrompt):
                    LepFromWZ.append((index,gp.pt,gp.pdgId,isFromZ,isFromTau,gp.eta,gp.phi))
                    # LepFromWZ_FamilyTrees.append((FamilyTree))
        
        # END of for loop over all generator particles
        # Prepare the output to fill the branches
       
        # Sort based on the particle pt
        LepFromWZ.sort(key=lambda Particle: Particle[1], reverse=True)        

        # DEBUG: events with > 3 prompt leptons in the final state (happens if event has e.g. Z->e+e-e+). | Unphysical -> overwrite if this is the case..
        if len(LepFromWZ)>3:
            self.Log("WARNING: Found event with >3 f.s. leptons", 1)
            LepFromWZ = []


        ret["nGenLepFromWZ"] = len(LepFromWZ)

        # If there are less than 3 f.s. LepFromWZ, fill this list with dummy values
        for i in range(3-len(LepFromWZ)):
            LepFromWZ.append((-100,-100,-100,-100,-100,-100,-100,-100))

        for i in range(2-len(TauFromZ)):
            TauFromZ.append((-100,-100,-100,-100,-100,-100,-100,-100))


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

        self.out.fillBranch("GenTauFromZ_pt",          list(TauFromZ[l][0] for l in range(len(TauFromZ))))
        self.out.fillBranch("GenTauFromZ_eta",         list(TauFromZ[l][1] for l in range(len(TauFromZ))))
        self.out.fillBranch("GenTauFromZ_phi",         list(TauFromZ[l][2] for l in range(len(TauFromZ))))

        ret = self.Prepare_2l3l_categories_returns(ret, GenLepFromWZ_id, GenLepFromWZ_charge, GenLepFromWZ_isFromZ, GenLepFromWZ_isFromTau)
        ret = self.Prepare_WZtoTau_decays_returns(ret, nTauFromZ, nTauFromW, LepFromWZ)
        ret = self.Prepare_WZ_decays_returns(ret, Z_daughters, W_daughters)
    

        # Put all ret branches together
        allret = {}
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

        
