import ROOT,sys
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = 1 
from ROOT import *
sys.path.append('cfgs/')
sys.path.append('input/')

lowMass = {'ele':150,'mu':150}

def setIntegrator(ws,name):
	config = RooNumIntConfig(ws.pdf(name).getIntegratorConfig())
	config.method1D().setLabel("RooAdaptiveGaussKronrodIntegrator1D")
	config.getConfigSection("RooAdaptiveGaussKronrodIntegrator1D").setCatLabel("method","61Points")
	config.getConfigSection("RooAdaptiveGaussKronrodIntegrator1D").setRealValue("maxSeg",1000)
	config.method1D().setLabel("RooAdaptiveGaussKronrodIntegrator1D")
	config.getConfigSection("RooAdaptiveGaussKronrodIntegrator1D").setCatLabel("method","61Points")
	config.getConfigSection("RooAdaptiveGaussKronrodIntegrator1D").setRealValue("maxSeg",1000)
	ws.pdf(name).setIntegratorConfig(config)


def createSignalDataset(massVal,name,channel,width,nEvents,CB,tag=""):

	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)
	ROOT.RooRandom.randomGenerator().SetSeed(0)
	import glob
	for f in glob.glob("userfuncs/*.cxx"):
		ROOT.gSystem.Load(f)
        configName ="channelConfig_%s"%channel
        config =  __import__(configName)
	
	dataFile = config.dataFile
	ws = RooWorkspace("tempWS")

	if 'electron' in channel:
		lowestMass = lowMass['ele']
	elif 'muon' in channel:
		lowestMass = lowMass['mu']

        mass = RooRealVar('massFullRange','massFullRange',massVal, lowestMass, 6000 )
        getattr(ws,'import')(mass,ROOT.RooCmdArg())


	peak = RooRealVar("peak","peak",massVal, lowestMass , 6000)
	peak.setConstant()
	getattr(ws,'import')(peak,ROOT.RooCmdArg())


	### define signal shape
	if CB:

		ws.factory("BreitWigner::bw(massFullRange, peak, %.3f)"%(massVal*width))
		
		#if 'electron' in name:
	


		params = config.getResolution(massVal)
		ws.factory("RooCruijff::cb(massFullRange, mean[0.0], %f, %f, %f, %f)"%(massVal*params['res'],massval*params['res'],params['alphaL'],params['alphaR']))
		#else:
		#	ws.factory("RooCBShape::cb(massFullRange, mean[0.0], %.3f, alpha[1.43], n[3])"%(massVal*config.getResolution(massVal)))
		
	

		bw = ws.pdf("bw")
		cb = ws.pdf("cb")
		
		mass.setBins(20000,"cache")
		mass.setMin("cache",0)
		mass.setMax("cache",12500); ## need to be adjusted to be higher than limit setting
		
		sigpdf = RooFFTConvPdf("sig_pdf","sig_pdf",mass,bw,cb)
		getattr(ws,'import')(sigpdf,ROOT.RooCmdArg())



	else:
		#if 'elextron' in name:
		params = config.getResolution(massVal)
		ws.factory("Voigtian::sig_pdf(massFullRange,peak,%.3f, %.3f)"%(massVal*width,massVal*config.params['res']))
		#else:	
		#	ws.factory("Voigtian::sig_pdf(massFullRange,peak,%.3f, %.3f)"%(massVal*width,massVal*config.getResolution(massVal)))
	useShapeUncert = False
	if "bkgParams" in config.systematics:
		useShapeUncert=True
	ws = config.loadBackgroundShape(ws,useShapeUncert)

        with open(dataFile) as f:
                masses = f.readlines()
        nBkg = len(masses)
	dataSet = ws.pdf("bkgpdf_fullRange").generate(ROOT.RooArgSet(ws.var("massFullRange")),nBkg)
	if nEvents > 0:
		nSignal = int(round(nEvents*config.signalEff(massVal)))
		dataSet.append(ws.pdf("sig_pdf").generate(ROOT.RooArgSet(ws.var("massFullRange")),nSignal))

	masses = []
	for i in range(0,dataSet.numEntries()):
		masses.append(dataSet.get(i).getRealValue("massFullRange"))
	if "toy" in tag:
		f = open("%s%s.txt"%(name,tag), 'w')
 	elif CB:
		f = open("%s_%d_%.3f_%d_CB%s.txt"%(name,massVal,width,nEvents,tag), 'w')
	else:	
		f = open("%s_%d_%.3f_%d%s.txt"%(name,massVal,width,nEvents,tag), 'w')
	for mass in masses:
		f.write("%.4f\n" % mass)
	f.close()

def createWS(massVal,minNrEv,name,channel,width,correlateMass,dataFile="",CB=True,write=True,useShapeUncert=False):
	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)
	import glob
	for f in glob.glob("userfuncs/*.cxx"):
		ROOT.gSystem.Load(f)
                configName ="channelConfig_%s"%channel
        config =  __import__(configName)
	
	if dataFile == "":
		dataFile = config.dataFile

	if not correlateMass:
		peakName = "_%s"%channel 
	else:
		peakName = ""
	#if "electron" in name:
	if 'electron' in channel:
		lowestMass = lowMass['ele']
	elif 'muon' in channel:
		lowestMass = lowMass['mu']


	effWidth = width + config.getResolution(massVal)['res']
	#else:	
	#	effWidth = width + config.getResolution(massVal)
	from tools import getMassRange
	massLow, massHigh = getMassRange(massVal,minNrEv,effWidth,dataFile,lowestMass)	
	#massLow = 120
	#massHigh = 400	
	ws = RooWorkspace(channel)
        massFullRange = RooRealVar('massFullRange','massFullRange',massVal, lowestMass, 6000 )
        getattr(ws,'import')(massFullRange,ROOT.RooCmdArg())

	mass = RooRealVar('mass_%s'%channel,'mass_%s'%channel,massVal, massLow, massHigh )
	getattr(ws,'import')(mass,ROOT.RooCmdArg())
	
	peak = RooRealVar("peak%s"%peakName,"peak%s"%peakName,massVal, massVal, massVal)
	peak.setConstant()
	getattr(ws,'import')(peak,ROOT.RooCmdArg())
	
	### mass scale uncertainty defined on peak position
	beta_peak = RooRealVar('beta_peak%s'%peakName,'beta_peak%s'%peakName,0,-5,5)
	getattr(ws,'import')(beta_peak,ROOT.RooCmdArg())
	scaleUncert = 1. + config.provideUncertainties(massVal)["massScale"]
	peak_kappa = RooRealVar('peak%s_kappa'%peakName,'peak%s_kappa'%peakName,scaleUncert)
	peak_kappa.setConstant()
	getattr(ws,'import')(peak_kappa,ROOT.RooCmdArg())
	ws.factory("PowFunc::peak_nuis%s(peak%s_kappa, beta_peak%s)"%(peakName,peakName,peakName))
	ws.factory("prod::peak_scaled%s(peak%s, peak_nuis%s)"%(peakName,peakName,peakName))


	### load resolution parameters and set up log normal for systematic on core resolution
	params = config.getResolution(massVal)
	res = RooRealVar("res%s"%peakName,"res%s"%peakName, massVal*params['res'])
        if params['alphaR'] < 0:
        	params['alphaR'] = 0
	res.setConstant()
	getattr(ws,'import')(res,ROOT.RooCmdArg())

	alphaL = RooRealVar("alphaL_%s"%channel,"alphaL_%s"%channel,params['alphaL'])
	alphaL.setConstant()
	getattr(ws,'import')(alphaL,ROOT.RooCmdArg())

	alphaR = RooRealVar("alphaR_%s"%channel,"alphaR_%s"%channel, params['alphaR'])
	alphaR.setConstant()
	getattr(ws,'import')(alphaR,ROOT.RooCmdArg())

	beta_res = RooRealVar('beta_res%s'%peakName,'beta_res%s'%peakName,0,-5,5)
	getattr(ws,'import')(beta_res,ROOT.RooCmdArg())
	resUncert = 1. + config.provideUncertainties(massVal)["res"]
	res_kappa = RooRealVar('res%s_kappa'%peakName,'res%s_kappa'%peakName,resUncert)
	res_kappa.setConstant()
	getattr(ws,'import')(res_kappa,ROOT.RooCmdArg())
	ws.factory("PowFunc::res_nuis%s(res%s_kappa, beta_res%s)"%(peakName,peakName,peakName))
	ws.factory("prod::res_scaled%s(res%s, res_nuis%s)"%(peakName,peakName,peakName))

	if CB:
		
		ws.factory("BreitWigner::bw(mass_%s, peak_scaled%s, %.3f)"%(channel,peakName,massVal*width))


		ws.factory("RooCruijff::cb(mass_%s, mean[0.0], res_scaled%s, res_scaled%s, alphaL_%s, alphaR_%s)"%(channel,peakName,peakName,channel,channel))
		bw = ws.pdf("bw")
		cb = ws.pdf("cb")
		mass.setBins(20000,"cache")
		mass.setMin("cache",0)
		mass.setMax("cache",12500); ## need to be adjusted to be higher than limit setting
		
		sigpdf = RooFFTConvPdf("sig_pdf_%s"%channel,"sig_pdf_%s"%channel,mass,bw,cb)
		getattr(ws,'import')(sigpdf,ROOT.RooCmdArg())

	else:
		params = config.getResolution(massVal)
		ws.factory("Voigtian::sig_pdf_%s(mass_%s, peak_scaled%s,  %.3f, res_scaled%s)"%(channel,channel,peakName,massVal*width,peakName))
	setIntegrator(ws,'sig_pdf_%s'%channel)

	ws = config.loadBackgroundShape(ws,useShapeUncert)


	setIntegrator(ws,'bkgpdf_fullRange')
	setIntegrator(ws,'bkgpdf_%s'%channel)

	ds = RooDataSet.read(dataFile,RooArgList(mass))
	ds.SetName('data_%s'%channel)
	ds.SetTitle('data_%s'%channel)
	getattr(ws,'import')(ds,ROOT.RooCmdArg())
	ws.addClassDeclImportDir("shapes/")	
	ws.importClassCode()	
	if config.nBkg == -1:
        	with open(dataFile) as f:
                	masses = f.readlines()
		nBkgTotal = len(masses)
	else:
		nBkgTotal = config.nBkg
	if write:
		ws.writeToFile("%s.root"%name,True)
        	from tools import getBkgEstInWindow
        	return getBkgEstInWindow(ws,massLow,massHigh,nBkgTotal)
	else:
		return ws


def getBinning(mass):


	if mass < 700:
		return [1,1000000]
	if mass < 1000:
		return [1,1000000]
	elif mass < 2000:
		return [2,1000000]
	else:
		return [5,500000]

def createHistograms(massVal,minNrEv,name,channel,width,correlateMass,binWidth,dataFile="",CB=True):
	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)


	

	configName ="channelConfig_%s"%channel
        config =  __import__(configName)
	
	if dataFile == "":
		dataFile = config.dataFile
	effWidth = width + config.getResolution(massVal)['res']
	if config.nBkg == -1:
        	with open(dataFile) as f:
                	masses = f.readlines()
		nBkgTotal = len(masses)
	else:
		nBkgTotal = config.nBkg


	if 'electron' in channel:
		lowestMass = lowMass['ele']
	elif 'muon' in channel:
		lowestMass = lowMass['mu']


	from tools import getMassRange
	massLow, massHigh = getMassRange(massVal,minNrEv,effWidth,dataFile,lowestMass)	
	if not correlateMass:
		peakName = "_%s"%channel 
	else:
		peakName = ""


	ws = createWS(massVal,minNrEv,name,channel,width,correlateMass,dataFile=dataFile,CB=CB,write=False)
        
	from tools import getBkgEstInWindow
	nBackground = getBkgEstInWindow(ws,massLow,massHigh,nBkgTotal)
	binWidth = getBinning(massVal)[0]
	numEvents = getBinning(massVal)[1]
	nBins = int((massHigh - massLow)/binWidth) 
	ws.var("mass_%s"%channel).setBins(nBins)
	histFile = ROOT.TFile("%s.root"%name, "RECREATE")	

        scaleName = "scale"
        if not correlateMass:
                scaleName +="_%s"%channel

	scaleUncert = config.provideUncertainties(massVal)["massScale"]
        sigShape = ws.pdf("sig_pdf_%s"%channel).generate(ROOT.RooArgSet(ws.var("mass_%s"%channel)),numEvents)
	ws.var("peak%s"%peakName).setVal(massVal*(1+scaleUncert))
        sigShapeUp = ws.pdf("sig_pdf_%s"%channel).generate(ROOT.RooArgSet(ws.var("mass_%s"%channel)),numEvents)
	ws.var("peak%s"%peakName).setVal(massVal*(1-scaleUncert))
        sigShapeDown = ws.pdf("sig_pdf_%s"%channel).generate(ROOT.RooArgSet(ws.var("mass_%s"%channel)),numEvents)

	sigHistRooFit = ROOT.RooDataHist("sigHist_%s"%channel, "sigHist_%s"%channel, ROOT.RooArgSet(ws.var('mass_%s'%channel)), sigShape)	
	sigHist = sigHistRooFit.createHistogram("sigHist_%s"%channel,ws.var("mass_%s"%channel))
	sigHist.SetName("sigHist_%s"%channel)

	sigHistRooFitUp = ROOT.RooDataHist("sigHist_%s_%sUp"%(channel,scaleName), "sigHist_%s_%sUp"%(channel,scaleName), ROOT.RooArgSet(ws.var('mass_%s'%channel)), sigShapeUp)	
	sigHistUp = sigHistRooFitUp.createHistogram("sigHist_%s_%sUp"%(channel,scaleName),ws.var("mass_%s"%channel))
	sigHistUp.SetName("sigHist_%s_%sUp"%(channel,scaleName))

	sigHistRooFitDown = ROOT.RooDataHist("sigHist_%s_%sDown"%(channel,scaleName), "sigHist_%s_%sDown"%(channel,scaleName), ROOT.RooArgSet(ws.var('mass_%s'%channel)), sigShapeDown)	
	sigHistDown = sigHistRooFitDown.createHistogram("sigHist_%s_%sDown"%(channel,scaleName),ws.var("mass_%s"%channel))
	sigHistDown.SetName("sigHist_%s_%sDown"%(channel,scaleName))
	
	sigHist.Scale(1./(sigHist.Integral())*config.provideSignalScaling(massVal)*1e-7)
	sigHistUp.Scale(1./(sigHistUp.Integral())*config.provideSignalScaling(massVal)*1e-7)
	sigHistDown.Scale(1./(sigHistDown.Integral())*config.provideSignalScaling(massVal)*1e-7)

	bkgShape = ws.pdf("bkgpdf_%s"%channel).generate(ROOT.RooArgSet(ws.var("mass_%s"%channel)),numEvents)
	bkgHistRooFit = ROOT.RooDataHist("bkgHist_%s"%channel, "bkgHist_%s"%channel, ROOT.RooArgSet(ws.var('mass_%s'%channel)), bkgShape)	
	bkgHist = bkgHistRooFit.createHistogram("bkgHist_%s"%channel,ws.var("mass_%s"%channel))
	bkgHist.SetName("bkgHist_%s"%channel)

	bkgHist.Scale(1./(bkgHist.Integral())*nBackground)

	dataHist = ROOT.TH1F("data_%s"%channel,"data_%s"%channel,nBins,massLow,massHigh)
	
	
        with open(dataFile) as f:
                masses = f.readlines()
	for mass in masses:
		mass = float(mass)
		if (mass >= massLow and mass <= massHigh):
			dataHist.Fill(mass)
	histFile.Write()
	histFile.Close()


        return nBackground
	
def createHistogramsCI(L,interference,name,channel,scanConfigName,dataFile=""):
	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)


	configName ="channelConfig_%s"%channel
        config =  __import__(configName)
	
	scanConfigName ="scanConfiguration_%s"%scanConfigName
        scanConfig =  __import__(scanConfigName)
	
        binning = scanConfig.binning

	if 'electron' in channel:
		lowestMass = 400
	elif 'muon' in channel:
		lowestMass = 400
        from array import array
 

	ws = RooWorkspace(channel)

	mass = RooRealVar('massFullRange','massFullRange',1000, lowestMass, 3500 )
	getattr(ws,'import')(mass,ROOT.RooCmdArg())
	
	
	ws = config.loadBackgroundShape(ws,useShapeUncert=False)
	setIntegrator(ws,'bkgpdf_fullRange')

	inputFileName = "input/inputsCI/inputsCI_%s_%dTeV_%s.root"%(channel,L,interference)
        inputFile = ROOT.TFile(inputFileName, "OPEN")

	import pickle 
	pkl = open("input/inputsCI/signalYields_default.pkl", "r")
	signalYields_default = pickle.load(pkl)
	pkl = open("input/inputsCI/signalYields_scale.pkl", "r")
	signalYields_scale = pickle.load(pkl)

	pkl = open("input/inputsCI/signalYields_resolution.pkl", "r")
	signalYields_resolution = pickle.load(pkl)

	pkl = open("input/inputsCI/signalYields_ID.pkl", "r")
	signalYields_ID = pickle.load(pkl)



	histFile = ROOT.TFile("%s.root"%name, "RECREATE")	
#	sigHistTemp = inputFile.Get("sigHist_%s"%channel)
#	sigHistSmearTemp = inputFile.Get("sigHistSmeared_%s"%channel)
##	sigHistScaleDownTemp = inputFile.Get("sigHistScaleDown_%s"%channel)
#	sigHistScaleUpTemp = inputFile.Get("sigHistScaleUp_%s"%channel)
#	sigHistIDTemp = inputFile.Get("sigHistWeighted_%s"%channel)

	bkgHistDYTemp = inputFile.Get("bkgHistDY_%s"%channel)
	bkgHistDYSmearTemp = inputFile.Get("bkgHistDYSmeared_%s"%channel)
	bkgHistDYScaleDownTemp = inputFile.Get("bkgHistDYScaleDown_%s"%channel)
	bkgHistDYScaleUpTemp = inputFile.Get("bkgHistDYScaleUp_%s"%channel)
	bkgHistDYIDTemp = inputFile.Get("bkgHistDYWeighted_%s"%channel)
	
	bkgHistOtherTemp = inputFile.Get("bkgHistOther_%s"%channel)
	bkgHistOtherSmearTemp = inputFile.Get("bkgHistOtherSmeared_%s"%channel)
	bkgHistOtherScaleDownTemp = inputFile.Get("bkgHistOtherScaleDown_%s"%channel)
	bkgHistOtherScaleUpTemp = inputFile.Get("bkgHistOtherScaleUp_%s"%channel)
	bkgHistOtherIDTemp = inputFile.Get("bkgHistOtherWeighted_%s"%channel)

	bkgHistJetsTemp = inputFile.Get("bkgHistJets_%s"%channel)
	
	pdfUncert = [0.01,0.0125,0.02,0.035,0.065]

	dataHistTemp = inputFile.Get("dataHist_%s"%channel)
	dataIntegral = dataHistTemp.Integral(dataHistTemp.FindBin(lowestMass),dataHistTemp.GetNbinsX())

        scaleName = "scale"
        statName = "stats"
	smearName = "res"
	pdfName = "pdf"
	IDName = "ID"


        bkgHistDY = ROOT.TH1F("bkgHistDY_%s"%channel,"bkgHistDY_%s"%channel,len(binning)-1,array('f',binning))
        bkgHistDYStatUp = ROOT.TH1F("bkgHistDY_%s_%sUp"%(statName,channel),"bkgHistDYStat_%s_%sUp"%(channel,statName),len(binning)-1,array('f',binning))
        bkgHistDYStatDown = ROOT.TH1F("bkgHistDY_%s_%sDown"%(statName,channel),"bkgHistDYStat_%s_%sDown"%(channel,statName),len(binning)-1,array('f',binning))
        bkgHistDYSmearUp = ROOT.TH1F("bkgHistDY_%s_%sUp"%(smearName,channel),"bkgHistDYSmear_%s_%sUp"%(channel,smearName),len(binning)-1,array('f',binning))
        bkgHistDYSmearDown = ROOT.TH1F("bkgHistDY_%s_%sDown"%(smearName,channel),"bkgHistDYSmear_%s_%sDown"%(channel,smearName),len(binning)-1,array('f',binning))
        bkgHistDYScaleDown = ROOT.TH1F("bkgHistDY_%s_%sDown"%(scaleName,channel),"bkgHistDYScaleDown_%s_%s"%(channel,scaleName),len(binning)-1,array('f',binning))
        bkgHistDYScaleUp = ROOT.TH1F("bkgHistDY_%s_%sUp"%(scaleName,channel),"bkgHistDYScaleUp_%s_%s"%(channel,scaleName),len(binning)-1,array('f',binning))
        bkgHistDYPDFDown = ROOT.TH1F("bkgHistDY_%s_%sDown"%(pdfName,channel),"bkgHistDYPDFDown_%s_%s"%(channel,pdfName),len(binning)-1,array('f',binning))
        bkgHistDYPDFUp = ROOT.TH1F("bkgHistDY_%s_%sUp"%(pdfName,channel),"bkgHistDYPDFUp_%s_%s"%(channel,pdfName),len(binning)-1,array('f',binning))
        bkgHistDYIDDown = ROOT.TH1F("bkgHistDY_%s_%sDown"%(IDName,channel),"bkgHistDYIDDown_%s_%s"%(channel,IDName),len(binning)-1,array('f',binning))
        bkgHistDYIDUp = ROOT.TH1F("bkgHistDY_%s_%sUp"%(IDName,channel),"bkgHistDYIDUp_%s_%s"%(channel,IDName),len(binning)-1,array('f',binning))

        bkgHistOther = ROOT.TH1F("bkgHistOther_%s"%channel,"bkgHistOther_%s"%channel,len(binning)-1,array('f',binning))
        bkgHistOtherStatUp = ROOT.TH1F("bkgHistOther_%s_%sUp"%(statName,channel),"bkgHistOtherStat_%s_%sUp"%(channel,statName),len(binning)-1,array('f',binning))
        bkgHistOtherStatDown = ROOT.TH1F("bkgHistOther_%s_%sDown"%(statName,channel),"bkgHistOtherStat_%s_%sDown"%(channel,statName),len(binning)-1,array('f',binning))
        bkgHistOtherSmearUp = ROOT.TH1F("bkgHistOther_%s_%sUp"%(smearName,channel),"bkgHistOtherSmear_%s_%sUp"%(channel,smearName),len(binning)-1,array('f',binning))
        bkgHistOtherSmearDown = ROOT.TH1F("bkgHistOther_%s_%sDown"%(smearName,channel),"bkgHistOtherSmear_%s_%sDown"%(channel,smearName),len(binning)-1,array('f',binning))
        bkgHistOtherScaleDown = ROOT.TH1F("bkgHistOther_%s_%sDown"%(scaleName,channel),"bkgHistOtherScaleDown_%s_%s"%(channel,scaleName),len(binning)-1,array('f',binning))
        bkgHistOtherScaleUp = ROOT.TH1F("bkgHistOther_%s_%sUp"%(scaleName,channel),"bkgHistOtherScaleUp_%s_%s"%(channel,scaleName),len(binning)-1,array('f',binning))
        bkgHistOtherPDFDown = ROOT.TH1F("bkgHistOther_%s_%sDown"%(pdfName,channel),"bkgHistOtherPDFDown_%s_%s"%(channel,pdfName),len(binning)-1,array('f',binning))
        bkgHistOtherPDFUp = ROOT.TH1F("bkgHistOther_%s_%sUp"%(pdfName,channel),"bkgHistOtherPDFUp_%s_%s"%(channel,pdfName),len(binning)-1,array('f',binning))
        bkgHistOtherIDDown = ROOT.TH1F("bkgHistOther_%s_%sDown"%(IDName,channel),"bkgHistOtherIDDown_%s_%s"%(channel,IDName),len(binning)-1,array('f',binning))
        bkgHistOtherIDUp = ROOT.TH1F("bkgHistOther_%s_%sUp"%(IDName,channel),"bkgHistOtherIDUp_%s_%s"%(channel,IDName),len(binning)-1,array('f',binning))

        bkgHistJets = ROOT.TH1F("bkgHistJets_%s"%channel,"bkgHistJets_%s"%channel,len(binning)-1,array('f',binning))

        sigHist = ROOT.TH1F("sigHist_%s"%channel,"sigHist_%s"%channel,len(binning)-1,array('f',binning))
        sigHistStatUp = ROOT.TH1F("sigHist_%s_%sUp"%(statName,channel),"sigHistStat_%s_%sUp"%(channel,statName),len(binning)-1,array('f',binning))
        sigHistStatDown = ROOT.TH1F("sigHist_%s_%sDown"%(statName,channel),"sigHistStat_%s_%sDown"%(channel,statName),len(binning)-1,array('f',binning))
        sigHistSmearUp = ROOT.TH1F("sigHist_%s_%sUp"%(smearName,channel),"sigHistSmear_%s_%sUp"%(channel,smearName),len(binning)-1,array('f',binning))
        sigHistSmearDown = ROOT.TH1F("sigHist_%s_%sDown"%(smearName,channel),"sigHistSmear_%s_%sDown"%(channel,smearName),len(binning)-1,array('f',binning))
        sigHistScaleDown = ROOT.TH1F("sigHist_%s_%sDown"%(scaleName,channel),"sigHistScaleDown_%s_%s"%(channel,scaleName),len(binning)-1,array('f',binning))
        sigHistScaleUp = ROOT.TH1F("sigHist_%s_%sUp"%(scaleName,channel),"sigHistScaleUp_%s_%s"%(channel,scaleName),len(binning)-1,array('f',binning))
        sigHistPDFDown = ROOT.TH1F("sigHist_%s_%sDown"%(pdfName,channel),"sigHistPDFDown_%s_%s"%(channel,pdfName),len(binning)-1,array('f',binning))
        sigHistPDFUp = ROOT.TH1F("sigHist_%s_%sUp"%(pdfName,channel),"sigHistPDFUp_%s_%s"%(channel,pdfName),len(binning)-1,array('f',binning))
        sigHistIDDown = ROOT.TH1F("sigHist_%s_%sDown"%(IDName,channel),"sigHistIDDown_%s_%s"%(channel,IDName),len(binning)-1,array('f',binning))
        sigHistIDUp = ROOT.TH1F("sigHist_%s_%sUp"%(IDName,channel),"sigHistIDUp_%s_%s"%(channel,IDName),len(binning)-1,array('f',binning))

        dataHist = ROOT.TH1F("dataHist_%s"%channel,"dataHist_%s"%channel,len(binning)-1,array('f',binning))

	for index, lower in enumerate(binning):	
		if index < len(binning)-1:
			#ws.var("massFullRange").setRange("window",lower,binning[index+1])
			#argSet = ROOT.RooArgSet(ws.var("massFullRange"))
			#integral = ws.pdf("bkgpdf_fullRange").createIntegral(argSet,ROOT.RooFit.NormSet(argSet), ROOT.RooFit.Range("window"))
			#bkgHist.SetBinContent(index+1,dataIntegral*integral.getVal())

	#	 	err = ROOT.Double(0)	
	#		val = sigHistTemp.IntegralAndError(sigHistTemp.FindBin(lower),sigHistTemp.FindBin(binning[index+1]-0.001),err)

	#		sigHist.SetBinContent(index+1,max(0,val))
	#		sigHistStatUp.SetBinContent(index+1,max(0,val+err))
	#		sigHistStatDown.SetBinContent(index+1,max(0,val-err))
	#		sigHistSmearDown.SetBinContent(index+1,max(0,sigHistSmearTemp.Integral(sigHistSmearTemp.FindBin(lower),sigHistSmearTemp.FindBin(binning[index+1]-0.001))))
	#		sigHistSmearUp.SetBinContent(index+1,max(0,sigHistSmearTemp.Integral(sigHistSmearTemp.FindBin(lower),sigHistSmearTemp.FindBin(binning[index+1]-0.001))))
	#		sigHistScaleDown.SetBinContent(index+1,max(0,sigHistScaleDownTemp.Integral(sigHistScaleDownTemp.FindBin(lower),sigHistScaleDownTemp.FindBin(binning[index+1]-0.001))))
	#		sigHistIDUp.SetBinContent(index+1,max(0,sigHistIDTemp.Integral(sigHistIDTemp.FindBin(lower),sigHistIDTemp.FindBin(binning[index+1]-0.001))))
	#		sigHistIDDown.SetBinContent(index+1,max(0,sigHistIDTemp.Integral(sigHistIDTemp.FindBin(lower),sigHistIDTemp.FindBin(binning[index+1]-0.001))))
	#		sigHistScaleUp.SetBinContent(index+1,max(0,sigHistScaleUpTemp.Integral(sigHistScaleUpTemp.FindBin(lower),sigHistScaleUpTemp.FindBin(binning[index+1]-0.001))))
	#		sigHistPDFDown.SetBinContent(index+1,max(0,val-val*pdfUncert[index]))
	#		sigHistPDFUp.SetBinContent(index+1,max(0,val+val*pdfUncert[index]))
			label = "CITo2Mu_Lam%dTeV%s_%s"%(L,interference,channel)
			val = signalYields_default[label][str(index)][0]
			err = signalYields_default[label][str(index)][1]
#			sigHistPDFDown.SetBinContent(index+1,val-val*pdfUncert[index])
#			sigHistPDFUp.SetBinContent(index+1,val+val*pdfUncert[index])
#			sigHist.SetBinContent(index+1,val)
#			sigHistStatUp.SetBinContent(index+1,val+err)
#			sigHistStatDown.SetBinContent(index+1,val-err)
#			val = signalYields_resolution[label][str(index)][0]
#			sigHistSmearDown.SetBinContent(index+1,val)
#			sigHistSmearUp.SetBinContent(index+1,val)
#			val = signalYields_scale[label][str(index)][0]
#			sigHistScaleDown.SetBinContent(index+1,val)
#			sigHistScaleUp.SetBinContent(index+1,sigHist.GetBinContent(index+1))
#			val = signalYields_ID[label][str(index)][0]
#			sigHistIDUp.SetBinContent(index+1,sigHist.GetBinContent(index+1))
#			sigHistIDDown.SetBinContent(index+1,val)
			sigHistPDFDown.SetBinContent(index+1,max(0,val-val*pdfUncert[index]))
			sigHistPDFUp.SetBinContent(index+1,max(0,val+val*pdfUncert[index]))
			sigHist.SetBinContent(index+1,max(0,val))
			sigHistStatUp.SetBinContent(index+1,max(0,val+err))
			sigHistStatDown.SetBinContent(index+1,max(0,val-err))
			val = signalYields_resolution[label][str(index)][0]
			sigHistSmearDown.SetBinContent(index+1,max(0,val))
			sigHistSmearUp.SetBinContent(index+1,max(0,val))
			val = signalYields_scale[label][str(index)][0]
			sigHistScaleDown.SetBinContent(index+1,max(0,val))
			sigHistScaleUp.SetBinContent(index+1,max(0,val))
			val = signalYields_ID[label][str(index)][0]
			sigHistIDUp.SetBinContent(index+1,max(0,val))
			sigHistIDDown.SetBinContent(index+1,max(0,val))


		 	err = ROOT.Double(0)	
			val = bkgHistDYTemp.IntegralAndError(bkgHistDYTemp.FindBin(lower),bkgHistDYTemp.FindBin(binning[index+1]-0.001),err)
			bkgHistDY.SetBinContent(index+1,max(0,val))
			bkgHistDYStatUp.SetBinContent(index+1,max(0,val+err))
			bkgHistDYStatDown.SetBinContent(index+1,max(0,val-err))
			bkgHistDYSmearDown.SetBinContent(index+1,max(0,bkgHistDYSmearTemp.Integral(bkgHistDYSmearTemp.FindBin(lower),bkgHistDYSmearTemp.FindBin(binning[index+1]-0.001))))
			bkgHistDYSmearUp.SetBinContent(index+1,max(0,bkgHistDYSmearTemp.Integral(bkgHistDYSmearTemp.FindBin(lower),bkgHistDYSmearTemp.FindBin(binning[index+1]-0.001))))
			bkgHistDYScaleDown.SetBinContent(index+1,max(0,bkgHistDYScaleDownTemp.Integral(bkgHistDYScaleDownTemp.FindBin(lower),bkgHistDYScaleDownTemp.FindBin(binning[index+1]-0.001))))
			bkgHistDYIDUp.SetBinContent(index+1,max(0,bkgHistDYIDTemp.Integral(bkgHistDYIDTemp.FindBin(lower),bkgHistDYIDTemp.FindBin(binning[index+1]-0.001))))
			bkgHistDYIDDown.SetBinContent(index+1,max(0,bkgHistDYIDTemp.Integral(bkgHistDYIDTemp.FindBin(lower),bkgHistDYIDTemp.FindBin(binning[index+1]-0.001))))
			bkgHistDYScaleUp.SetBinContent(index+1,max(0,bkgHistDYScaleUpTemp.Integral(bkgHistDYScaleUpTemp.FindBin(lower),bkgHistDYScaleUpTemp.FindBin(binning[index+1]-0.001))))
			bkgHistDYPDFDown.SetBinContent(index+1,max(0,val-val*pdfUncert[index]))
			bkgHistDYPDFUp.SetBinContent(index+1,max(0,val+val*pdfUncert[index]))

		 	err = ROOT.Double(0)	
			val = bkgHistOtherTemp.IntegralAndError(bkgHistOtherTemp.FindBin(lower),bkgHistOtherTemp.FindBin(binning[index+1]-0.001),err)
			bkgHistOther.SetBinContent(index+1,max(0,val))
			bkgHistOtherStatUp.SetBinContent(index+1,max(0,val+err))
			bkgHistOtherStatDown.SetBinContent(index+1,max(0,val-err))
			bkgHistOtherSmearDown.SetBinContent(index+1,max(0,bkgHistOtherSmearTemp.Integral(bkgHistOtherSmearTemp.FindBin(lower),bkgHistOtherSmearTemp.FindBin(binning[index+1]-0.001))))
			bkgHistOtherSmearUp.SetBinContent(index+1,max(0,bkgHistOtherSmearTemp.Integral(bkgHistOtherSmearTemp.FindBin(lower),bkgHistOtherSmearTemp.FindBin(binning[index+1]-0.001))))
			bkgHistOtherScaleDown.SetBinContent(index+1,max(0,bkgHistOtherScaleDownTemp.Integral(bkgHistOtherScaleDownTemp.FindBin(lower),bkgHistOtherScaleDownTemp.FindBin(binning[index+1]-0.001))))
			bkgHistOtherScaleUp.SetBinContent(index+1,max(0,bkgHistOtherScaleUpTemp.Integral(bkgHistOtherScaleUpTemp.FindBin(lower),bkgHistOtherScaleUpTemp.FindBin(binning[index+1]-0.001))))
			bkgHistOtherIDDown.SetBinContent(index+1,max(0,bkgHistOtherIDTemp.Integral(bkgHistOtherIDTemp.FindBin(lower),bkgHistOtherIDTemp.FindBin(binning[index+1]-0.001))))
			bkgHistOtherIDUp.SetBinContent(index+1,max(0,bkgHistOtherIDTemp.Integral(bkgHistOtherIDTemp.FindBin(lower),bkgHistOtherIDTemp.FindBin(binning[index+1]-0.001))))
			bkgHistOtherPDFDown.SetBinContent(index+1,max(0,val-val*pdfUncert[index]))
			bkgHistOtherPDFUp.SetBinContent(index+1,max(0,val+val*pdfUncert[index]))
	
			val = bkgHistJetsTemp.IntegralAndError(bkgHistJetsTemp.FindBin(lower),bkgHistJetsTemp.FindBin(binning[index+1]-0.001),err)
			bkgHistJets.SetBinContent(index+1,max(0,val))
		
			dataHist.SetBinContent(index+1,dataHistTemp.Integral(dataHistTemp.FindBin(lower),dataHistTemp.FindBin(binning[index+1]-0.001)))
			#dataHist.SetBinContent(index+1,dataYields[index])
	
	bkgIntegralDY = bkgHistDY.Integral()		
	bkgIntegralOther = bkgHistOther.Integral()		
	bkgIntegralJets = bkgHistJets.Integral()		
	sigIntegral = sigHist.Integral()

	histFile.Write()
	histFile.Close()


        return [bkgIntegralDY,bkgIntegralOther,bkgIntegralJets,sigIntegral]


def createSingleBinCI(L,interference,name,channel,scanConfigName,mThresh,dataFile=""):
	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

	mThresh = float(mThresh)

	configName ="channelConfig_%s"%channel
        config =  __import__(configName)
	
	scanConfigName ="scanConfiguration_%s"%scanConfigName
        scanConfig =  __import__(scanConfigName)
	
	
	result = {}	
	

	import pickle 
	pkl = open("input/inputsCI/signalYieldsSingleBin_default.pkl", "r")
	signalYields_default = pickle.load(pkl)
	pkl = open("input/inputsCI/signalYieldsSingleBin_scale.pkl", "r")
	signalYields_scale = pickle.load(pkl)
	pkl = open("input/inputsCI/signalYieldsSingleBin_resolution.pkl", "r")
	signalYields_resolution = pickle.load(pkl)

	pkl = open("input/inputsCI/signalYieldsSingleBin_ID.pkl", "r")
	signalYields_ID = pickle.load(pkl)


	inputFileName = "input/inputsCI/inputsCI_%s_%dTeV_%s.root"%(channel,L,interference)
        inputFile = ROOT.TFile(inputFileName, "OPEN")

	bkgHistDY = inputFile.Get("bkgHistDY_%s"%channel)
	bkgHistDYSmear = inputFile.Get("bkgHistDYSmeared_%s"%channel)
	bkgHistDYScaleDown = inputFile.Get("bkgHistDYScaleDown_%s"%channel)
	bkgHistDYScaleUp = inputFile.Get("bkgHistDYScaleUp_%s"%channel)
	bkgHistDYID = inputFile.Get("bkgHistDYWeighted_%s"%channel)
	
	bkgHistOther = inputFile.Get("bkgHistOther_%s"%channel)
	bkgHistOtherSmear = inputFile.Get("bkgHistOtherSmeared_%s"%channel)
	bkgHistOtherScaleDown = inputFile.Get("bkgHistOtherScaleDown_%s"%channel)
	bkgHistOtherScaleUp = inputFile.Get("bkgHistOtherScaleUp_%s"%channel)
	bkgHistOtherID = inputFile.Get("bkgHistOtherWeighted_%s"%channel)

	bkgHistJets = inputFile.Get("bkgHistJets_%s"%channel)

	
	label = "CITo2Mu_Lam%dTeV%s_%s"%(L,interference,channel)
	val = signalYields_default[label][str(int(mThresh))][0]
	err = signalYields_default[label][str(int(mThresh))][1]

	valSmear = signalYields_resolution[label][str(int(mThresh))][0]
	valScale = signalYields_scale[label][str(int(mThresh))][0]
	valID = signalYields_ID[label][str(int(mThresh))][0]


	result["sig"] = val 
	result["sigStats"] = abs(1+err/val)
	result["sigRes"] = abs(valSmear/val) 
	result["sigScale"] = abs(valScale/val)
	result["sigID"] = abs(valID/val)
	result["sigPDF"] = 1.05 #dummy value for now
	

	dataHist = inputFile.Get("dataHist_%s"%channel)
	result["data"] = dataHist.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)	

 	err = ROOT.Double(0)	
	val = bkgHistDY.IntegralAndError(bkgHistDY.FindBin(mThresh),bkgHistDY.GetNbinsX()+1,err)
	result["bkgDY"] = val
	result["bkgDYStats"] = 1.+err/val
	if abs(bkgHistDYSmear.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) >=1:
		result["bkgDYRes"] = abs(bkgHistDYSmear.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])
	else:	
		result["bkgDYRes"] = 1./abs(bkgHistDYSmear.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])
	if abs(bkgHistDYScaleUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) >=1: 
		result["bkgDYScale"] = abs(bkgHistDYScaleUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) 
	else:
		result["bkgDYScale"] =1./abs(bkgHistDYScaleUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) 
	if abs(bkgHistDYID.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) >=1:
		result["bkgDYID"] = abs(bkgHistDYID.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])
	else:
		result["bkgDYID"] = 1./abs(bkgHistDYID.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])
	result["bkgDYPDF"] = 1.05 #dummy value for now 
	
	val = bkgHistOther.IntegralAndError(bkgHistOther.FindBin(mThresh),bkgHistOther.GetNbinsX()+1,err)
	result["bkgOther"] = val
	result["bkgOtherStats"] = 1.+val/err
	result["bkgOther"] = abs(bkgHistOther.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)) 
	if  abs(bkgHistOtherSmear.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) >= 1:
		result["bkgOtherRes"] = abs(bkgHistOtherSmear.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])	 
	else:
		result["bkgOtherRes"] = 1./abs(bkgHistOtherSmear.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])
	if abs(bkgHistOtherScaleUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) >=1:
		result["bkgOtherScale"] = abs(bkgHistOtherScaleUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])
	else:	
		result["bkgOtherScale"] = 1./abs(bkgHistOtherScaleUp.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])
	if abs(bkgHistOtherID.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"]) >= 1:
		result["bkgOtherID"] = abs(bkgHistOtherID.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])
	else:
		result["bkgOtherID"] = 1./abs(bkgHistOtherID.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)/result["bkgDY"])
	result["bkgOtherPDF"] = 1.05 #dummy value for now 


	result["bkgJets"] = bkgHistJets.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)


        return result
	
