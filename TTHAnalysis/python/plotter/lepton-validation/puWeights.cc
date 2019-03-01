// Run2016 E+F+G up to 279931, calculated with minBias xsec = 69 mbxs
float _puw2016_nTrueInt_EF[60] = {0.0002476692378524667, 0.014821369430223724, 0.01908474123097549, 0.018774416942744378, 0.027731029726566526, 0.022766323438142735, 0.02112794605705192, 0.015627067131392624, 0.013027012984949482, 0.02664421891070537, 0.105951322567897, 0.2282219493320249, 0.3198539045796174, 0.4472658025206919, 0.6588805154724832, 0.7954191125076755, 0.7971828693076433, 0.8476493223752923, 0.828823661825391, 0.9020575899440882, 0.8251811240056177, 0.8088819151700594, 0.898945222693826, 1.0499718952630142, 1.1569874762934436, 1.4559615822558385, 1.5258279117119538, 1.8409115119643453, 1.8896981359803084, 2.140209911977273, 2.3304811410048387, 2.558753854290941, 3.6974162747530404, 4.798085511876458, 5.7327747190694405, 5.7327747190694405, 5.7327747190694405, 5.7327747190694405, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993, 1.0318994494324993};
float _puw2016_nTrueInt_G_upto279931[60] = {0.0030664708563046326, 0.01123794331581895, 0.016465056588825536, 0.024602832177926543, 0.026107749406095258, 0.019050503081821886, 0.02110161688725923, 0.017694605650846847, 0.016290999589588673, 0.03017245306638949, 0.062201175397462435, 0.21783085244166905, 0.5552753191757233, 0.7214955162768668, 0.7324485837208575, 0.7293440437992165, 0.7146681538266634, 0.7527382158346893, 0.7180480259007131, 0.7910622869835229, 0.7597422022206722, 0.7786794509943739, 0.8873764384591624, 1.0499884204081869, 1.1665585452761693, 1.482186697601494, 1.579761549660652, 1.9529819332323881, 2.053483793295554, 2.356853951860021, 2.5540748462771266, 2.7323308232944745, 3.76828118550158, 4.585241234971839, 5.680781421298886, 5.680781421298886, 5.680781421298886, 5.680781421298886, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995, 1.0225406558337995};
float _puw2016_nTrueInt_EFG_upto279931[60] = {0.0012466094493921048, 0.013160935994534766, 0.01768708902983447, 0.021285749046576714, 0.02682365314703701, 0.020855099389744048, 0.020605061123741098, 0.016225941568981307, 0.014048132697170798, 0.02723810756281671, 0.08766748594327597, 0.2188586889136281, 0.3959226446275465, 0.53375637601322, 0.668298874408685, 0.7522202102811592, 0.7512257707056236, 0.8045384529297095, 0.790321346838139, 0.8694715549669896, 0.80985012101077, 0.8077764909536846, 0.9071025263393598, 1.0638089303658826, 1.17351814974311, 1.478754892106334, 1.5559650574410981, 1.8900984223481412, 1.9531327854179075, 2.2173732038373344, 2.402868150348858, 2.6038209490463284, 3.685234828496249, 4.657038942103952, 5.7091311002033045, 5.7091311002033045, 5.7091311002033045, 5.7091311002033045, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948, 1.0276435980365948};
float puw2016_nTrueInt_EF(int nTrueInt) { if (nTrueInt<60) return _puw2016_nTrueInt_EF[nTrueInt]; else return 0; }
float puw2016_nTrueInt_G_upto279931(int nTrueInt) { if (nTrueInt<60) return _puw2016_nTrueInt_G_upto279931[nTrueInt]; else return 0; }
float puw2016_nTrueInt_EFG_upto279931(int nTrueInt) { if (nTrueInt<60) return _puw2016_nTrueInt_EFG_upto279931[nTrueInt]; else return 0; }