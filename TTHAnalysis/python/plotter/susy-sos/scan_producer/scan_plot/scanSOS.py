import sys, copy
import ROOT as r
from array import array
#import array
import math


class binning:
    def __init__(self, mi, ma, w):
        self._min = mi
        self._max = ma
        self.w  = w 
        self.n  = int(abs(ma-mi)/w)

def interpolateByHand(th2, startx, starty, binx):
    while startx+binx <= th2.GetXaxis().GetXmax():
        v1 = th2.GetBinContent(th2.FindBin(startx, starty))
        v2 = th2.GetBinContent(th2.FindBin(startx+binx, starty+binx))
        th2.Fill(startx+binx/2., starty+binx/2, (v1+v2)/2.)
        startx = startx+binx
        starty = starty+binx
    

class Scan(object):
    def __init__(self, name):
        self.cuts_norm = '1'
        self.name  = name
        self.zminUL  = 1e-3; self.zmaxUL = 1e3
        self.xbins = binning(100,100,1000); self.ybins = binning(100,100,1000)
        self.xtitle = 'mother'; self.ytitle = 'daughter'
        self.xsecFile = 0
        self.xsecFile2 = None
        self.zmaxEff = 0.5
        self.extraSmoothes = 2
        self.paper = 'SUS7'
        self.xvar = 'GenSusyMScan1_Edge'
        self.yvar = 'GenSusyMScan2_Edge'
        self.loadData()
        self.loadXsecs()
       # self.xtran=Transpose(h_orig)

    def __getstate__(self): 
        return self.__dict__
    def __setstate__(self, d): 
        self.__dict__.update(d)

    def loadData(self):
        if self.name == 'T2tt':
            self.makeMCDatacards = True
            self.paper = 'SUS16025'
            self.xbinsize = 1. 
            self.ybinsize = 1.
            self.xbins = binning(300,550, self.xbinsize)
            self.ybins = binning(  0,120, self.ybinsize)
            self.yx = r.TH2F('histo_'+self.name, 'histo_'+self.name, self.xbins.n, self.xbins._min, self.xbins._max, self.ybins.n, self.ybins._min, self.ybins._max)
            self.zminUL = 1e-3; self.zmaxUL = 1e3
            self.zmaxEff = 0.30
            self.xsecFile = 'xs_T2tt.root'
            self.xtitle = 'm_{stop}'; self.ytitle = 'm_{LSP}'
            self.limitfile = 'limits/scan_T2tt_Moriond_FINAL.root'

        if self.name == 'TChiNeuWZ':
            self.makeMCDatacards = True
            self.paper = 'SUS16025'
            self.xbinsize = 1.
            self.ybinsize = 1.
            self.xbins = binning(100,330, self.xbinsize)
            self.ybins = binning(  0, 60, self.ybinsize)#50
            self.yx = r.TH2F('histo_'+self.name, 'histo_'+self.name, self.xbins.n, self.xbins._min, self.xbins._max, self.ybins.n, self.ybins._min, self.ybins._max)
            self.zminUL = 1e-3; self.zmaxUL = 1e3 
            self.zmaxEff = 0.30
            self.xsecFile = 'xs_TChiNeuWZ.root'
            self.xtitle = 'm_{Chargino=Neutralino2}'; self.ytitle = 'm_{LSP}'
            self.limitfile = 'limits/scan_TChiWZ_Moriond_FINAL.root' 

        if self.name == 'TN2C1':
            self.makeMCDatacards = True
            self.paper = 'SUS16025'
            self.xbinsize = 1.
            self.ybinsize = 1.
            self.xbins = binning(100,330, self.xbinsize)
            self.ybins = binning(  0, 60, self.ybinsize)#50                                                                                                                                                       
            self.yx = r.TH2F('histo_'+self.name, 'histo_'+self.name, self.xbins.n, self.xbins._min, self.xbins._max, self.ybins.n, self.ybins._min, self.ybins._max)
            self.zminUL = 1e-3; self.zmaxUL = 1e3
            self.zmaxEff = 0.30
            self.xsecFile = 'xs_TN2C1.root' 
            self.xtitle = 'm_{Chargino=Neutralino2}'; self.ytitle = 'm_{LSP}'
            self.limitfile = 'limits/scan_TN2C1_Moriond_FINAL.root'

        if self.name == 'TN2N1':
            self.makeMCDatacards = True
            self.paper = 'SUS16025'
            self.xbinsize = 1.
            self.ybinsize = 1.
            self.xbins = binning(100,330, self.xbinsize)
            self.ybins = binning(  0, 60, self.ybinsize)#50                                                                                                                                                       
            self.yx = r.TH2F('histo_'+self.name, 'histo_'+self.name, self.xbins.n, self.xbins._min, self.xbins._max, self.ybins.n, self.ybins._min, self.ybins._max)
            self.zminUL = 1e-3; self.zmaxUL = 1e3
            self.zmaxEff = 0.30
            self.xsecFile = 'xs_TN2N1.root'
            self.xtitle = 'm_{Chargino=Neutralino2}'; self.ytitle = 'm_{LSP}'
            self.limitfile = 'limits/scan_TN2N1_Moriond_FINAL.root' 

        if self.name == 'TN2N1_TN2C1_comb':
            self.makeMCDatacards = True
            self.paper = 'SUS16025'
            self.xbinsize = 1.
            self.ybinsize = 1.
            self.xbins = binning(100,330, self.xbinsize)
            self.ybins = binning(  0, 60, self.ybinsize)#50                                                                                                                                                                                                                                                                  
            self.yx = r.TH2F('histo_'+self.name, 'histo_'+self.name, self.xbins.n, self.xbins._min, self.xbins._max, self.ybins.n, self.ybins._min, self.ybins._max)
            self.zminUL = 1e-3; self.zmaxUL = 1e3
            self.zmaxEff = 0.30
            self.xsecFile  = 'xs_TN2N1.root'
            self.xsecFile2 = 'xs_TN2C1.root'
            self.xtitle = 'm_{Chargino=Neutralino2}'; self.ytitle = 'm_{LSP}'
            self.limitfile = 'limits/scan_TN2N1_TN2C1_combination_Moriond_FINAL.root'


        if self.name == 'TN2N1_pheno':
            self.makeMCDatacards = True
            self.paper = 'SUS16025'
            self.xbinsize = 1.
            self.ybinsize = 1.
            self.xbins = binning(100,330, self.xbinsize)
            self.ybins = binning(  0, 60, self.ybinsize)#50                                                                           
            self.yx = r.TH2F('histo_'+self.name, 'histo_'+self.name, self.xbins.n, self.xbins._min, self.xbins._max, self.ybins.n, self.ybins._min, self.ybins._max)
            self.zminUL = 1e-3; self.zmaxUL = 1e3
            self.zmaxEff = 0.30
            self.xsecFile = 'xs_TN2N1_pheno.root'                                                                              
            self.xtitle = 'm_{Chargino=Neutralino2}'; self.ytitle = 'm_{LSP}'
            self.limitfile = 'limits/scan_TN2N1_pheno_Moriond_FINAL.root'

        if self.name == 'TN2C1_pheno':
            self.makeMCDatacards = True
            self.paper = 'SUS16025'
            self.xbinsize = 1.
            self.ybinsize = 1.
            self.xbins = binning(100,330, self.xbinsize)
            self.ybins = binning(  0, 60, self.ybinsize)#50                                                                             
            self.yx = r.TH2F('histo_'+self.name, 'histo_'+self.name, self.xbins.n, self.xbins._min, self.xbins._max, self.ybins.n, self.ybins._min, self.ybins._max)
            self.zminUL = 1e-3; self.zmaxUL = 1e3
            self.zmaxEff = 0.30
            self.xsecFile = 'xs_TN2C1_pheno.root'
            self.xtitle = 'm_{Chargino=Neutralino2}'; self.ytitle = 'm_{LSP}'
            self.limitfile = 'limits/scan_TN2C1_pheno_Moriond_FINAL.root'

        if self.name == 'TN2N1_TN2C1_pheno_comb':
            self.makeMCDatacards = True
            self.paper = 'SUS16025'
            self.xbinsize = 1.
            self.ybinsize = 1.
            self.xbins = binning(100,330, self.xbinsize)
            self.ybins = binning(  0, 60, self.ybinsize)#50                                                                                                                                                                                                                                                                   
            self.yx = r.TH2F('histo_'+self.name, 'histo_'+self.name, self.xbins.n, self.xbins._min, self.xbins._max, self.ybins.n, self.ybins._min, self.ybins._max)
            self.zminUL = 1e-3; self.zmaxUL = 1e3
            self.zmaxEff = 0.30
            self.xsecFile = 'xs_TN2N1_pheno2.root'
            self.xsecFile2 = 'xs_TN2C1_pheno2.root'
            self.xtitle = 'm_{Chargino=Neutralino2}'; self.ytitle = 'm_{LSP}'
            self.limitfile = 'limits/scan_TN2N1_TN2C1_phenoFinal_combination_Moriond_FINAL.root'

        if self.name == 'pMSSM':
            self.makeMCDatacards = True
            self.paper = 'SUS16025'
            self.xbinsize = 1.
            self.ybinsize = 1.
            self.xbins = binning(100,240, self.xbinsize)
            self.ybins = binning(200,1000, self.ybinsize)#50                                                                                                                                                       
            self.yx = r.TH2F('histo_'+self.name, 'histo_'+self.name, self.xbins.n, self.xbins._min, self.xbins._max, self.ybins.n, self.ybins._min, self.ybins._max)
            self.zminUL = 1e-3; self.zmaxUL = 1e3
            self.zmaxEff = 0.30
            self.xsecFile = 'xs_pMSSM.root'
            self.xtitle = 'm_{Chargino=Neutralino2}'; self.ytitle = 'm_{LSP}'
            self.limitfile = 'limits/scan_pMSSM_Moriond_FINAL_highStat.root'


    def loadXsecs(self):
        if not self.xsecFile:
            estring = 'ERROR: no xsec file specified for scan {name}!!!\nExiting...'.format(name=self.name)
            sys.exit(estring)
        xsecf = r.TFile(self.xsecFile,'READ')
        self.xsec_histo = copy.deepcopy(xsecf.Get('xs'))
        if self.xsecFile2:
            xsecf2 = r.TFile(self.xsecFile2,'READ')
            self.xsec2_histo = copy.deepcopy(xsecf2.Get('xs'))

    def makeExclusion(self):
        print 'making the exclusions!!'
        limitfile = r.TFile(self.limitfile,'READ')
        limittree = limitfile.Get('limit')
        ## observed limit
        self.ex_obs = copy.deepcopy(self.yx)
        self.ex_obs.SetTitle("nominal exclusion plot observed"); self.ex_obs.SetName('ex_obs')
        self.ex_obs.Reset()
        ## observed + 1 sigma xsec limit
        self.ex_obs_p1s = copy.deepcopy(self.yx)
        self.ex_obs_p1s.SetTitle("nominal exclusion plot observed + 1 sig xsec"); self.ex_obs_p1s.SetName('ex_obs_p1s')
        self.ex_obs_p1s.Reset()
        ## observed - 1 sigma xsec limit
        self.ex_obs_m1s = copy.deepcopy(self.yx)
        self.ex_obs_m1s.SetTitle("nominal exclusion plot observed - 1 sig xsec"); self.ex_obs_m1s.SetName('ex_obs_m1s')
        self.ex_obs_m1s.Reset()
        ## expected limit
        self.ex_exp = copy.deepcopy(self.yx)
        self.ex_exp.SetTitle("nominal exclusion plot expected"); self.ex_exp.SetName('ex_exp')
        self.ex_exp.Reset()
        ## expected limit +1 sigma(exp)
        self.ex_exp_p1s = copy.deepcopy(self.yx)
        self.ex_exp_p1s.SetTitle("nominal exclusion plot expected + 1 sigma exp"); self.ex_exp_p1s.SetName('ex_exp_p1s')
        self.ex_exp_p1s.Reset()
        ## expected limit +1 sigma(exp)
        self.ex_exp_m1s = copy.deepcopy(self.yx)
        self.ex_exp_m1s.SetTitle("nominal exclusion plot expected - 1 sigma exp"); self.ex_exp_m1s.SetName('ex_exp_m1s')
        self.ex_exp_m1s.Reset()
    
        self.ex_exp_p2s = copy.deepcopy(self.yx)
        self.ex_exp_p2s.SetTitle("nominal exclusion plot expected + 2 sigma exp"); self.ex_exp_p2s.SetName('ex_exp_p2s')
        self.ex_exp_p2s.Reset()

        self.ex_exp_m2s = copy.deepcopy(self.yx)
        self.ex_exp_m2s.SetTitle("nominal exclusion plot expected - 2 sigma exp"); self.ex_exp_m2s.SetName('ex_exp_m2s')
        self.ex_exp_m2s.Reset()
    

        for point in limittree:
            massx = point.mh
            massy = point.iSeed
            limit = point.limit
            if self.name != 'pMSSM':
                massy = (massx - massy)
            j=massy
            cor=1
            if j<7.5:
               cor=cor*0.6
            elif j<10:
               cor=cor*0.77
            elif j<15:
               cor=cor*0.9
            elif j<20:
               cor=cor*0.94
            elif j<30:
               cor=cor*0.98
            elif j<40:
               cor=cor*0.99
            #limit=limit/cor ## george?
            if point.quantileExpected <  0.:
                self.ex_obs.Fill(massx, massy, limit)
                ## R.C. modified here for adapting to the different scans
                if self.name == 'TN2N1':
                    mass_mu = (massx+(massx-massy))/2
                    xsec   = self.xsec_histo.GetBinContent(self.xsec_histo.FindBin(mass_mu))
                    xsec_e = self.xsec_histo.GetBinError  (self.xsec_histo.FindBin(mass_mu))
                elif self.name == 'TN2C1':
                    mass_mu = (0.75*massx)+(0.25*(massx-massy))
                    xsec   = self.xsec_histo.GetBinContent(self.xsec_histo.FindBin(mass_mu))
                    xsec_e = self.xsec_histo.GetBinError  (self.xsec_histo.FindBin(mass_mu))
                elif self.name == 'TN2N1_TN2C1_comb':    
                    mass_mu_n2n1 = (massx+(massx-massy))/2
                    mass_mu_n2c1 = (0.75*massx)+(0.25*(massx-massy))
                    xsec   = self.xsec_histo.GetBinContent(self.xsec_histo.FindBin(mass_mu_n2n1)) + self.xsec2_histo.GetBinContent(self.xsec2_histo.FindBin(mass_mu_n2c1))
                    xsec_e = math.sqrt(math.pow(self.xsec_histo.GetBinError(self.xsec_histo.FindBin(mass_mu_n2n1)),2) + math.pow(self.xsec2_histo.GetBinError(self.xsec2_histo.FindBin(mass_mu_n2c1)),2))
                elif (self.name == 'pMSSM' or self.name == 'TN2N1_pheno' or self.name == 'TN2C1_pheno') :
                    xsec   = self.xsec_histo.GetBinContent(self.xsec_histo.FindBin(massx,massy))
                    xsec_e = self.xsec_histo.GetBinError  (self.xsec_histo.FindBin(massx,massy))
                elif self.name == 'TN2N1_TN2C1_pheno_comb':
                    xsec   = self.xsec_histo.GetBinContent(self.xsec_histo.FindBin(massx,massy)) + self.xsec2_histo.GetBinContent(self.xsec2_histo.FindBin(massx,massy))
                    xsec_e = math.sqrt( math.pow(self.xsec_histo.GetBinError(self.xsec_histo.FindBin(massx,massy)),2) + math.pow(self.xsec2_histo.GetBinError(self.xsec2_histo.FindBin(massx,massy)),2))
                else:
                    xsec   = self.xsec_histo.GetBinContent(self.xsec_histo.FindBin(massx))
                    xsec_e = self.xsec_histo.GetBinError  (self.xsec_histo.FindBin(massx))
                
                self.ex_obs_p1s.Fill(massx, massy, limit*((xsec+xsec_e)/xsec))
                self.ex_obs_m1s.Fill(massx, massy, limit*((xsec-xsec_e)/xsec))

            elif 0.49 < point.quantileExpected < 0.51:
                self.ex_exp.Fill(massx, massy, limit)
            elif 0.15 < point.quantileExpected < 0.17:
                self.ex_exp_p1s.Fill(massx, massy, limit)
            elif 0.83 < point.quantileExpected < 0.85:
                self.ex_exp_m1s.Fill(massx, massy, limit)
            elif 0.02 < point.quantileExpected < 0.04:
                self.ex_exp_p2s.Fill(massx, massy, limit)
            elif 0.96 < point.quantileExpected < 0.99:
                self.ex_exp_m2s.Fill(massx, massy, limit)

        #if self.name == 'T2tt':
        #    for step in [25, 12.5]:
        #        for (x,y) in [(250, 240), (250, 230), (250, 220), (250, 210), (250, 200), (275, 205), (275, 215), (275, 220) ]:
        #            interpolateByHand(self.ex_obs    , x, y, step)
        #            interpolateByHand(self.ex_obs_p1s, x, y, step)
        #            interpolateByHand(self.ex_obs_m1s, x, y, step)
        #            interpolateByHand(self.ex_exp    , x, y, step)
        #            interpolateByHand(self.ex_exp_p1s, x, y, step)
        #            interpolateByHand(self.ex_exp_m1s, x, y, step)
        zmax = self.ex_obs.GetMaximum()
        self.ex_obs    .GetZaxis().SetRangeUser(0.,10.)
        self.ex_obs_p1s.GetZaxis().SetRangeUser(0.,10.)
        self.ex_obs_m1s.GetZaxis().SetRangeUser(0.,10.)
        self.ex_exp_p2s.GetZaxis().SetRangeUser(0.,10.)
        self.ex_exp_m2s.GetZaxis().SetRangeUser(0.,10.)
        self.ex_exp    .GetZaxis().SetRangeUser(0.,10.)
        self.ex_exp_p1s.GetZaxis().SetRangeUser(0.,10.)
        self.ex_exp_m1s.GetZaxis().SetRangeUser(0.,10.)
    
    def getSmoothedGraph(self,h_orig):
        print h_orig.GetName()
        tmp_name       = (h_orig.GetName()+'_smoothed').replace('Graph2D_from_','')
        tmp_name_graph = tmp_name+'_graph'
        global h_smoothed, smoothed_2dg, smoothed_gl, smoothed_g
        setattr(self, tmp_name.replace('smoothed','presmoothed'), copy.deepcopy(h_orig) )
        h_smoothed = h_orig.Clone(tmp_name)
        smoothedbins = []
        for i in range(h_smoothed.GetNbinsX()+1):
            for j in range(h_smoothed.GetNbinsY()+1):
                if j > 0 and not h_smoothed.GetBinContent(i,j):
                    h_smoothed.SetBinContent(i,j,h_smoothed.GetBinContent(i-1,j))
                    smoothedbins.append((i,j))
                    break
        h_smoothed.Smooth(1, 'k3a')#'k5a')
        for i in range(self.extraSmoothes):
            h_smoothed.Smooth(1, 'kba')
        for i,j in smoothedbins:
            h_smoothed.SetBinContent(i,j,0.)
        smcopy = copy.deepcopy(h_smoothed)
        smoothed_2dg = r.TGraph2D(smcopy)
        smoothed_2dg.SetNpx( int((smoothed_2dg.GetXmax() - smoothed_2dg.GetXmin())/ (self.xbinsize/2.) ) )
        smoothed_2dg.SetNpy( int((smoothed_2dg.GetYmax() - smoothed_2dg.GetYmin())/ (self.ybinsize/2.) ) )
        foobar = smoothed_2dg.GetHistogram() ## have to call this, otherwise root will freak out
        c = smoothed_2dg.GetContourList(1.0)
        #c = smoothed_2dg.GetContourList(2.51)
        smoothed_g   = c[max( (i.GetN(),j) for j,i in enumerate( c )  )[1]]
        setattr(self, 'c', c)
        smoothed_g.SetName(tmp_name_graph)
        setattr(self, tmp_name      , copy.deepcopy(h_smoothed) )
        setattr(self, tmp_name_graph, copy.deepcopy(smoothed_g) )#copy.deepcopy(graph[0][1]) )
    
    def makeULPlot(self):
        print 'making the UL histo with holes filled etc.'
        h_rhisto = copy.deepcopy(self.ex_obs)
        for i in range(h_rhisto.GetNbinsX()+1):
            for j in range(h_rhisto.GetNbinsY()+1):
                if self.name == 'TN2N1':
                    delta_m=h_rhisto.GetYaxis().GetBinCenter(j)
                    m_x=h_rhisto.GetXaxis().GetBinCenter(i)
                    m_mu = (0.5*m_x)+(0.5*(m_x-delta_m))
                    xs = self.xsec_histo.GetBinContent(self.xsec_histo.FindBin(int(m_mu)))
                    xs=xs*10 # unfolding the leptonic BR (0.10)
                elif self.name == 'TN2C1':
                    delta_m=h_rhisto.GetYaxis().GetBinCenter(j)
                    m_x=h_rhisto.GetXaxis().GetBinCenter(i)
                    m_mu = (0.75*m_x)+(0.25*(m_x-delta_m))                
                    xs = self.xsec_histo.GetBinContent(self.xsec_histo.FindBin(int(m_mu)))
                    xs=xs*10 # unfolding the leptonic BR (0.10) 
                elif self.name == 'TN2N1_TN2C1_comb':
                    delta_m=h_rhisto.GetYaxis().GetBinCenter(j)
                    m_x=h_rhisto.GetXaxis().GetBinCenter(i)
                    m_mu_n2n1 = (0.5*m_x)+(0.5*(m_x-delta_m))
                    m_mu_n2c1 = (0.75*m_x)+(0.25*(m_x-delta_m))                     
                    xs = self.xsec_histo.GetBinContent(self.xsec_histo.FindBin(int(m_mu_n2n1))) + self.xsec2_histo.GetBinContent(self.xsec_histo.FindBin(int(m_mu_n2c1)))
                    xs=xs*10 # unfolding the leptonic BR (0.10) 
                elif self.name == 'pMSSM':
                    xs = self.xsec_histo.GetBinContent( self.xsec_histo.FindBin(int(h_rhisto.GetXaxis().GetBinCenter(i)),int(h_rhisto.GetYaxis().GetBinCenter(j))))
                    xs = xs*14.3 ## NB: approximated efficiency from p.122 of Basil's Higgsino booklet
                elif (self.name == 'TN2N1_pheno' or self.name == 'TN2C1_pheno') :
                    xs = self.xsec_histo.GetBinContent( self.xsec_histo.FindBin(int(h_rhisto.GetXaxis().GetBinCenter(i)),int(h_rhisto.GetYaxis().GetBinCenter(j))))
                    xs = xs*10 # unfolding the leptonic BR (0.10) 
                elif self.name == 'TN2N1_TN2C1_pheno_comb':
                  xs = self.xsec_histo.GetBinContent( self.xsec_histo.FindBin(int(h_rhisto.GetXaxis().GetBinCenter(i)),int(h_rhisto.GetYaxis().GetBinCenter(j)))) + self.xsec2_histo.GetBinContent( self.xsec2_histo.FindBin(int(h_rhisto.GetXaxis().GetBinCenter(i)),int(h_rhisto.GetYaxis().GetBinCenter(j))))
                  xs = xs*10 # unfolding the leptonic BR (0.10) 
                elif self.name == 'TChiNeuWZ':
                    xs = self.xsec_histo.GetBinContent( self.xsec_histo.FindBin(int(h_rhisto.GetXaxis().GetBinCenter(i))))
                    xs=xs*10 # unfolding the leptonic BR (0.10) 
                elif self.name == 'T2tt':
                    xs = self.xsec_histo.GetBinContent( self.xsec_histo.FindBin(int(h_rhisto.GetXaxis().GetBinCenter(i))))
                    xs=xs*10000

                h_rhisto.SetBinContent(i,j,h_rhisto.GetBinContent(i,j)*xs )
        gr2d = r.TGraph2D(h_rhisto)
        gr2d.SetNpx( int((gr2d.GetXmax() - gr2d.GetXmin())/ (self.xbinsize/2.) ) )
        gr2d.SetNpy( int((gr2d.GetYmax() - gr2d.GetYmin())/ (self.ybinsize/2.) ) )
        tmp_2d_histo = gr2d.GetHistogram()
        tmp_2d_histo.SetName('ul_histo')
        setattr(self, 'ul_histo', copy.deepcopy(tmp_2d_histo))
        print '... done making the UL histo'
                
    def saveULGraphsInFile(self):
        print 'saving the UL histo and graphs in a file'
        f = r.TFile('makeExclusionPlot/config/%s/%s_results.root'%(self.paper,self.name),'RECREATE')
        f.cd()        
        self.ul_histo.Write()
        self.ex_exp_smoothed_graph    .Write()
        self.ex_exp_p1s_smoothed_graph.Write()
        if(self.name == 'TChiNeuWZ' or self.name == 'T2tt' or self.name == 'pMSSM' or self.name == 'TN2N1_TN2C1_comb' or self.name == 'TN2N1_TN2C1_pheno_comb'):
            self.ex_exp_m1s_smoothed_graph.Write() 
        self.ex_obs_smoothed_graph    .Write()
        self.ex_obs_p1s_smoothed_graph.Write()
        self.ex_obs_m1s_smoothed_graph.Write()
        self.ex_exp_p2s_smoothed_graph.Write()
        if(self.name == 'TChiNeuWZ' or self.name == 'T2tt' ):
            self.ex_exp_m2s_smoothed_graph.Write()
        #self.xtran(ex_obs_smoothed_graph).Write()

        f.Close()
        print '... done saving the results file'
  
    def transposeHist(self,inHist):
        outName = inHist.GetName()        
        binWidthX = 2*(inHist.GetXaxis().GetBinCenter(1)-inHist.GetXaxis().GetBinLowEdge(1))
        binWidthY = 2*(inHist.GetYaxis().GetBinCenter(1)-inHist.GetYaxis().GetBinLowEdge(1))
        xMass = [inHist.GetXaxis().GetBinCenter(x) for x in range(1,inHist.GetXaxis().GetNbins()+1)]
        yMass = [inHist.GetYaxis().GetBinCenter(y) for y in range(1,inHist.GetYaxis().GetNbins()+1)]
        xLow = [inHist.GetXaxis().GetBinLowEdge(x) for x in range(1,inHist.GetXaxis().GetNbins()+1)]
        yAxisTranspose = []
        for x in xMass:
            for y in yMass:
                if x+y >= binWidthY/2.:
                    yAxisTranspose.append(x+y-binWidthY/2.)
        minY = max(0,min(yAxisTranspose))
        maxY = max(yAxisTranspose)
        xAxis = array('d',xLow)
        yValue = minY
        print "ok"
        yAxisTranspose = []
        while yValue <= maxY+binWidthY:
            yAxisTranspose.append(yValue)
            yValue += binWidthY
        yAxisTranspose = array('d',yAxisTranspose)
        outHist = r.TH2D(outName+"_transpose","",len(xAxis)-1,xAxis,len(yAxisTranspose)-1,yAxisTranspose)
        outHist.SetDirectory(0)
        for x in range(1,outHist.GetXaxis().GetNbins()+1):
            for y in range(1,outHist.GetYaxis().GetNbins()+1):
                value = inHist.GetBinContent(x,y)
                xValue,yValue = self.getBinCenter2D(x,y,inHist)
                newMass = xValue - yValue
                outHist.Fill(xValue,newMass,value)
        outHist.SetName(inHist.GetName())
        if inHist.GetName() is outName:
            print 'ok2'    
        print outName
        return outHist

    def transposeGraph(self,graph):
        outputGraph = graph.Clone()
        outputSize = graph.GetN()
        outputX,outputY = array('d',[0.]*outputSize),array('d',[0.]*outputSize)
        tempX,tempY = r.Double(0.),r.Double(0.)
        for i in range(outputSize):
            graph.GetPoint(i,tempX,tempY)
            outputX[i],outputY[i] = tempX,tempX-tempY
        outputGraph = r.TGraph(outputSize,outputX,outputY)
        outputGraph.SetName(graph.GetName())
        return outputGraph

    def getBinCenter2D(self,x,y,hist):
        xValue = hist.GetXaxis().GetBinCenter(x)
        yValue = hist.GetYaxis().GetBinCenter(y)
        return xValue,yValue   
    def makePrettyPlots(self):
        print 'starting to make pretty plots'
        #for t in ['_obs', '_obs_p1s', '_obs_m1s', '_exp', '_exp_p1s', '_exp_m1s','_exp_p2s', '_exp_m2s' ]: # Only for TChiWZ and T2tt
        #for t in ['_obs', '_obs_p1s', '_obs_m1s', '_exp', '_exp_p1s','_exp_p2s' ]: # Only for TN2N1 and C1N1 (full Higgsino)
        for t in ['_obs', '_obs_p1s', '_obs_m1s', '_exp', '_exp_p1s', '_exp_m1s','_exp_p2s' ]: # Only for combination
        #for t in ['_obs', '_obs_p1s', '_obs_m1s', '_exp', '_exp_m1s', '_exp_p1s','_exp_p2s' ]:
            tmp_2d_graph = r.TGraph2D(getattr(self, 'ex%s'%t))
            #tmp_2d_graph=transposeGraph(getattr(self,'ex%s'%t))
            tmp_2d_graph.SetNpx( int((tmp_2d_graph.GetXmax() - tmp_2d_graph.GetXmin())/ (self.xbinsize) ) )
            tmp_2d_graph.SetNpy( int((tmp_2d_graph.GetYmax() - tmp_2d_graph.GetYmin())/ (self.ybinsize) ) )
            tmp_2d_histo = tmp_2d_graph.GetHistogram()
            tmp_graph_list = tmp_2d_graph.GetContourList(1.01) 
            #tmp_graph_list = tmp_2d_graph.GetContourList(2.61)
            tmp_graph = tmp_graph_list[max( (i.GetN(),j) for j,i in enumerate( tmp_graph_list )  )[1]]
            setattr(self, 'ex%s_graph'%t, copy.deepcopy(tmp_graph    ) )
            setattr(self, 'ex%s_2dg'  %t, copy.deepcopy(tmp_2d_graph ) )
            setattr(self, 'ex%s_2dh'  %t, copy.deepcopy(tmp_2d_histo ) )
            self.getSmoothedGraph(getattr(self,'ex%s_2dh'%t))
           # self.transposeHist(getattr(self,'ex%s_2dh'%t))
            self.transposeGraph(getattr(self,'ex%s_graph'%t))
            self.getSmoothedGraph(getattr(self,'ex%s_2dh'%t))
            #self.transposeGraph(getattr(self,'ex%s_2dh'%t))
        self.makeULPlot()
        self.saveULGraphsInFile()
        print '... done making pretty plots'

#scan = Scan('TChiNeuWZ')
#scan.makeExclusion()
#scan.makePrettyPlots()

#scan = Scan('T2tt')
#scan.makeExclusion()
#scan.makePrettyPlots()

#scan = Scan('TN2N1')
#scan.makeExclusion()
#scan.makePrettyPlots()

#scan = Scan('TN2C1')
#scan.makeExclusion()
#scan.makePrettyPlots()

#scan = Scan('TN2N1_TN2C1_comb')
#scan.makeExclusion()                                                                                                                                                                                            
#scan.makePrettyPlots()    

scan = Scan('TN2N1_TN2C1_pheno_comb')
scan.makeExclusion()
scan.makePrettyPlots()

#scan = Scan('TN2N1_pheno')
#scan.makeExclusion()
#scan.makePrettyPlots()

#scan = Scan('TN2C1_pheno')
#scan.makeExclusion()
#scan.makePrettyPlots()

#scan = Scan('pMSSM')
#scan.makeExclusion()
#scan.makePrettyPlots()
