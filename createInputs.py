import ROOT,sys
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = 1 
from ROOT import *
from array import array
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


def createSignalDataset(massVal,name,channel,width,nEvents,CB,scale,tag=""):

	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)
	ROOT.RooRandom.randomGenerator().SetSeed(0)
	import glob
	for f in glob.glob("userfuncs/*.cxx"):
		ROOT.gSystem.Load(f)
        configName ="channelConfig_%s"%channel
        config =  __import__(configName)
	
	dataFile = config.dataFile
	ws = RooWorkspace("tempWS")

	peakName = "_%s"%channel 
	if 'electron' in channel:
		lowestMass = lowMass['ele']
	elif 'muon' in channel:
		lowestMass = lowMass['mu']

        mass = RooRealVar('massFullRange','massFullRange',massVal, lowestMass, 6000 )
        getattr(ws,'import')(mass,ROOT.RooCmdArg())


	peak = RooRealVar("peak","peak",massVal, lowestMass , 6000)
	peak.setConstant()
	getattr(ws,'import')(peak,ROOT.RooCmdArg())

	params = config.getResolution(massVal)
	if 'electron' in channel and massVal > 2300:
		res = RooRealVar("res%s"%peakName,"res%s"%peakName, massVal*params['res'])
		res.setConstant()
		getattr(ws,'import')(res,ROOT.RooCmdArg())

		alpha = RooRealVar("alpha_%s"%channel,"alpha_%s"%channel,params['alpha'])
		alpha.setConstant()
		getattr(ws,'import')(alpha,ROOT.RooCmdArg())
		n = RooRealVar("n_%s"%channel,"n_%s"%channel,params['n'])
		n.setConstant()
		getattr(ws,'import')(n,ROOT.RooCmdArg())



		beta_res = RooRealVar('beta_res%s'%peakName,'beta_res%s'%peakName,0,-5,5)
		getattr(ws,'import')(beta_res,ROOT.RooCmdArg())
		resUncert = 1. + config.provideUncertainties(massVal)["res"]
		res_kappa = RooRealVar('res%s_kappa'%peakName,'res%s_kappa'%peakName,resUncert)
		res_kappa.setConstant()
		getattr(ws,'import')(res_kappa,ROOT.RooCmdArg())
		ws.factory("PowFunc::res_nuis%s(res%s_kappa, beta_res%s)"%(peakName,peakName,peakName))
		ws.factory("prod::res_scaled%s(res%s, res_nuis%s)"%(peakName,peakName,peakName))
	elif 'dielectron_2017' in channel or 'dimuon_2017' in channel or 'dimuon_2018' in channel:
		res = RooRealVar("res%s"%peakName,"res%s"%peakName, massVal*params['res'])
		res.setConstant()
		getattr(ws,'import')(res,ROOT.RooCmdArg())

		mean = RooRealVar("mean%s"%peakName,"mean%s"%peakName, params['mean'])
		mean.setConstant()
		getattr(ws,'import')(mean,ROOT.RooCmdArg())

		alphaL = RooRealVar("alphaL_%s"%channel,"alphaL_%s"%channel,params['cutL'])
		alphaL.setConstant()
		getattr(ws,'import')(alphaL,ROOT.RooCmdArg())

		nL = RooRealVar("nL_%s"%channel,"nL_%s"%channel,params['powerL'])
		nL.setConstant()
		getattr(ws,'import')(nL,ROOT.RooCmdArg())

		alphaR = RooRealVar("alphaR_%s"%channel,"alphaR_%s"%channel,params['cutR'])
		alphaR.setConstant()
		getattr(ws,'import')(alphaR,ROOT.RooCmdArg())

		nR = RooRealVar("nR_%s"%channel,"nR_%s"%channel,params['powerR'])
		nR.setConstant()
		getattr(ws,'import')(nR,ROOT.RooCmdArg())




		beta_res = RooRealVar('beta_res%s'%peakName,'beta_res%s'%peakName,0,-5,5)
		getattr(ws,'import')(beta_res,ROOT.RooCmdArg())
		resUncert = 1. + config.provideUncertainties(massVal)["res"]
		res_kappa = RooRealVar('res%s_kappa'%peakName,'res%s_kappa'%peakName,resUncert)
		res_kappa.setConstant()
		getattr(ws,'import')(res_kappa,ROOT.RooCmdArg())
		ws.factory("PowFunc::res_nuis%s(res%s_kappa, beta_res%s)"%(peakName,peakName,peakName))
		ws.factory("prod::res_scaled%s(res%s, res_nuis%s)"%(peakName,peakName,peakName))




	else:
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
		ws.factory("BreitWigner::bw(massFullRange, peak, %.3f)"%(massVal*width))#	
		if 'dielectron_2017' in channel or 'dimuon_2017' or 'dimuon_2018':
			ws.factory("RooDCBShape::cb(mass_%s, mean[0.0], res_scaled%s, alphaL_%s, alphaR_%s, nL_%s, nR_%s)"%(channel,peakName,channel,channel,channel,channel))
		if 'dielectron_Moriond2017' in channel and massVal > 2300:
			ws.factory("RooCBShape::cb(mass_%s, mean[0.0], res_scaled%s, alpha_%s, n_%s)"%(channel,peakName,channel,channel))
		else:	
			ws.factory("RooCruijff::cb(massFullRange, mean[0.0], res_scaled%s, res_scaled%s, alphaL_%s, alphaR_%s)"%(peakName,peakName,channel,channel))
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

	useShapeUncert = False
	ws = config.loadBackgroundShape(ws,useShapeUncert)

        with open(dataFile) as f:
                masses = f.readlines()
	if config.nBkg == -1:
        	with open(dataFile) as f:
                	masses = f.readlines()
		nBkg = len(masses)
	else:
		nBkg = config.nBkg
	nBkg = nBkg*scale
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
		f = open("%s_%d_%.3f_%d_scale%d_CB%s.txt"%(name,massVal,width,nEvents,scale,tag), 'w')
	else:	
		f = open("%s_%d_%.3f_%d%s_scale%d.txt"%(name,massVal,width,nEvents,scale,tag), 'w')
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


	params = config.getResolution(massVal)
	effWidth = width + params['res']
	#else:	
	#	effWidth = width + config.getResolution(massVal)
	from tools import getMassRange
	massLow, massHigh = getMassRange(massVal,minNrEv,effWidth,dataFile,lowestMass)	
	#massLow = 120
	#massHigh = 400
	ws = RooWorkspace(channel)
	ws.autoImportClassCode(True)
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
	if 'dimuon_2017' in channel or 'dimuon_2018' in channel or 'dielectron' in channel:
		res = RooRealVar("res%s"%peakName,"res%s"%peakName, massVal*params['res'])
		res.setConstant()
		getattr(ws,'import')(res,ROOT.RooCmdArg())

		mean = RooRealVar("mean%s"%peakName,"mean%s"%peakName, params['scale'])
		mean.setConstant()
		getattr(ws,'import')(mean,ROOT.RooCmdArg())

		alphaL = RooRealVar("alphaL_%s"%channel,"alphaL_%s"%channel,params['alphaL'])
		alphaL.setConstant()
		getattr(ws,'import')(alphaL,ROOT.RooCmdArg())

		nL = RooRealVar("nL_%s"%channel,"nL_%s"%channel,params['nL'])
		nL.setConstant()
		getattr(ws,'import')(nL,ROOT.RooCmdArg())

		alphaR = RooRealVar("alphaR_%s"%channel,"alphaR_%s"%channel,params['alphaR'])
		alphaR.setConstant()
		getattr(ws,'import')(alphaR,ROOT.RooCmdArg())
		if params['nR'] < 0:
			params['nR'] = 0
		nR = RooRealVar("nR_%s"%channel,"nR_%s"%channel,params['nR'])
		nR.setConstant()
		getattr(ws,'import')(nR,ROOT.RooCmdArg())



		beta_res = RooRealVar('beta_res%s'%peakName,'beta_res%s'%peakName,0,-5,5)
		getattr(ws,'import')(beta_res,ROOT.RooCmdArg())
		resUncert = 1. + config.provideUncertainties(massVal)["res"]
		res_kappa = RooRealVar('res%s_kappa'%peakName,'res%s_kappa'%peakName,resUncert)
		res_kappa.setConstant()
		getattr(ws,'import')(res_kappa,ROOT.RooCmdArg())
		ws.factory("PowFunc::res_nuis%s(res%s_kappa, beta_res%s)"%(peakName,peakName,peakName))
		ws.factory("prod::res_scaled%s(res%s, res_nuis%s)"%(peakName,peakName,peakName))




	else:
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
		
		ws.factory("BreitWigner::bw_%s(mass_%s, peak_scaled%s, %.3f)"%(channel,channel,peakName,massVal*width))

		if 'dimuon_2017' in channel or 'dimuon_2018' in channel or 'dielectron' in channel:
			ws.factory("RooDCBShape::cb_%s(mass_%s, mean[0.0], res_scaled%s, alphaL_%s, alphaR_%s, nL_%s, nR_%s)"%(channel,channel,peakName,channel,channel,channel,channel))
		else:
			ws.factory("RooCruijff::cb_%s(mass_%s, mean[0.0], res_scaled%s, res_scaled%s, alphaL_%s, alphaR_%s)"%(channel,channel,peakName,peakName,channel,channel))
		bw = ws.pdf("bw_%s"%channel)
		cb = ws.pdf("cb_%s"%channel)
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
	ws.addClassDeclImportDir("userfuncs/")	
	#ws.importClassCode("userfuncs/ZPrimeEleBkgPdf3*")	
	#ws.Print()
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



def getRebinnedHistogram(hist,binning,name):
	#if "Jets" in name and "dielectron" in name:
	#	for i in range(0,hist.GetNbinsX()):
	#		hist.SetBinContent(i,hist.GetBinContent(i)*hist.GetBinWidth(i))
	#		hist.SetBinError(i,hist.GetBinError(i)*hist.GetBinWidth(i))		
	return hist.Rebin(len(binning) - 1, name, array('d', binning))

def getStatUncertHistogram(hist,name,up=False):
	uncertHist = hist.Clone(name)
	for i in range(0,hist.GetNbinsX()+1):
		if up:
			uncertHist.SetBinContent(i,hist.GetBinContent(i)+hist.GetBinError(i))	
		else:
			uncertHist.SetBinContent(i,max(0,hist.GetBinContent(i)-hist.GetBinError(i)))	
	return uncertHist 

def getPDFUncertHistogram(hist,name,pdf,up=False):
	uncertHist = hist.Clone(name)
	for i in range(1,hist.GetNbinsX()+1):
		if up:
			uncertHist.SetBinContent(i,hist.GetBinContent(i)+hist.GetBinContent(i)*pdf[i-1])	
		else:
			uncertHist.SetBinContent(i,max(0,hist.GetBinContent(i)-hist.GetBinContent(i)*pdf[i-1]))	
	return uncertHist


def createHistogramsCI(L,interference,name,channel,scanConfigName,dataFile="",truncation=False):
	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)


	configName ="channelConfig_%s"%channel
        config =  __import__(configName)
	
	scanConfigName ="scanConfiguration_%s"%scanConfigName
        scanConfig =  __import__(scanConfigName)
	
        binning = scanConfig.binning
	if "2016" in channel and "ADD" in scanConfigName:
	#if "ADD" in scanConfigName:
		binning = scanConfig.binning2016
	if dataFile == "":
		dataFile = config.dataFile
	with open(dataFile) as f:
    		events = f.readlines()

	if 'electron' in channel:
		lowestMass = 400
	elif 'muon' in channel:
		lowestMass = 400
        from array import array
 

	
	

	if 'ADD' in scanConfigName:
		model = 'ADD'
		lowestMass = 1800
		if "2016" in channel:
			lowestMass = 1900
	else: 
		model = 'CI'

	inputFileName = "input/inputsCI/inputsCI_%s.root"%(channel)
        inputFile = ROOT.TFile(inputFileName, "OPEN")
	truncationName=""
	if truncation:
		truncationName = "Truncation"
	import pickle 
	if "muon" in channel:
		pkl = open("input/inputsCI/%ssignalYields%s_default.pkl"%(model,truncationName), "r")
		signalYields_default = pickle.load(pkl)

		pkl = open("input/inputsCI/%ssignalYields%s_scaleDown.pkl"%(model,truncationName), "r")
		signalYields_scaleDown = pickle.load(pkl)

		pkl = open("input/inputsCI/%ssignalYields%s_pdfWeightsUp.pkl"%(model,truncationName), "r")
		signalYields_pdfWeightsUp = pickle.load(pkl)

		pkl = open("input/inputsCI/%ssignalYields%s_pdfWeightsDown.pkl"%(model,truncationName), "r")
		signalYields_pdfWeightsDown = pickle.load(pkl)

		pkl = open("input/inputsCI/%ssignalYields%s_resolution.pkl"%(model,truncationName), "r")
		signalYields_resolution = pickle.load(pkl)

		pkl = open("input/inputsCI/%ssignalYields%s_ID.pkl"%(model,truncationName), "r")
		signalYields_ID = pickle.load(pkl)
	elif "electron" in channel:
		pkl = open("input/inputsCI/%ssignalYieldsEle%s_default.pkl"%(model,truncationName), "r")
		signalYields_default = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsEle%s_scaleUp.pkl"%(model,truncationName), "r")
		signalYields_scaleUp = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsEle%s_scaleDown.pkl"%(model,truncationName), "r")
		signalYields_scaleDown = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsEle%s_piledown.pkl"%(model,truncationName), "r")
		signalYields_piledown = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsEle%s_pileup.pkl"%(model,truncationName), "r")
		signalYields_pileup = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsEle%s_pdfWeightsUp.pkl"%(model,truncationName), "r")
		signalYields_pdfWeightsUp = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsEle%s_pdfWeightsDown.pkl"%(model,truncationName), "r")
		signalYields_pdfWeightsDown = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsEle%s_prefireup.pkl"%(model,truncationName), "r")
		signalYields_prefireUp = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsEle%s_prefiredown.pkl"%(model,truncationName), "r")
		signalYields_prefireDown = pickle.load(pkl)

	histFile = ROOT.TFile("%s.root"%name, "RECREATE")	
	bkgHistDYTemp = inputFile.Get("bkgHistDY_%s"%channel)
	bkgHistDYScaleDownTemp = inputFile.Get("bkgHistDYScaleDown_%s"%channel)
	if "muon" in channel:
		bkgHistDYIDTemp = inputFile.Get("bkgHistDYWeighted_%s"%channel)
		bkgHistDYSmearTemp = inputFile.Get("bkgHistDYSmeared_%s"%channel)
	if "electron" in channel:
		bkgHistDYScaleUpTemp = inputFile.Get("bkgHistDYScaleUp_%s"%channel)
		bkgHistDYPUDownTemp = inputFile.Get("bkgHistDYPUDown_%s"%channel)
		bkgHistDYPUUpTemp = inputFile.Get("bkgHistDYPUUp_%s"%channel)
		bkgHistDYPrefireDownTemp = inputFile.Get("bkgHistDYPrefireDown_%s"%channel)
		bkgHistDYPrefireUpTemp = inputFile.Get("bkgHistDYPrefireUp_%s"%channel)

	bkgHistOtherTemp = inputFile.Get("bkgHistOther_%s"%channel)
	bkgHistOtherScaleDownTemp = inputFile.Get("bkgHistOtherScaleDown_%s"%channel)
	if "muon" in channel:
		bkgHistOtherIDTemp = inputFile.Get("bkgHistOtherWeighted_%s"%channel)
		bkgHistOtherSmearTemp = inputFile.Get("bkgHistOtherSmeared_%s"%channel)
	if "electron" in channel:
		bkgHistOtherPUDownTemp = inputFile.Get("bkgHistOtherPUDown_%s"%channel)
		bkgHistOtherPUUpTemp = inputFile.Get("bkgHistOtherPUUp_%s"%channel)
		bkgHistOtherScaleUpTemp = inputFile.Get("bkgHistOtherScaleUp_%s"%channel)
		bkgHistOtherPrefireDownTemp = inputFile.Get("bkgHistOtherPrefireDown_%s"%channel)
		bkgHistOtherPrefireUpTemp = inputFile.Get("bkgHistOtherPrefireUp_%s"%channel)

	bkgHistJetsTemp = inputFile.Get("bkgHistJets_%s"%channel)
	if "ADD" in scanConfigName:
		#if "2016" in channel:
			pdfUncert = [0.09650476077712875,0.11631416752423052,0.13116564710563733,0.14414683366902137,0.17666058539426496]	
			#pdfUncert = [0.001,0.001,0.001,0.001,0.001]	
			pdfUncertDY = [0.0335288129164533, 0.0429886021839947, 0.047645134519074, 0.069030181137942, 0.119036982092236]
			pdfUncertOther = [0.1655371996916466, 0.269902491201715, 0.2699234253751208, 0.2984407542188063, 0.3777961331626525]
		#else:
		#	pdfUncert = [0.029927732054534695,0.048888012380709035,0.08857090934916816,0.13602871909306424,0.17965523337854952]
		#	pdfUncertDY = [0.0138720301283295, 0.0190751831181522, 0.0305396967143887, 0.0516138991171715, 0.1230468160731701]
		#	pdfUncertOther = [0.0535456461585195, 0.1291420983058327, 0.1997479183784237, 0.283750816771433, 0.3565547632540647]
	else:
		pdfUncert = [0.029808675319316736,0.032492944178882606,0.046693632068081733,0.06985339137281024,0.11520346316811705,0.17965523337854952]
		pdfUncertDY = [0.0133126577202494, 0.0147788328624159, 0.01842209757115, 0.0243644300786998, 0.039572839847093, 0.1144248733154136]
		pdfUncertOther = [0.0358232181870253, 0.088892531404347, 0.1254268509362337, 0.1736824180528946, 0.2024257617076786, 0.3369525304968204]
	dataHistTemp = inputFile.Get("dataHist_%s"%channel)
	dataIntegral = dataHistTemp.Integral(dataHistTemp.FindBin(lowestMass),dataHistTemp.GetNbinsX())

        scaleName = "massScale"
        statName = "stats"
	smearName = "res"
	pdfName = "pdf"
	IDName = "ID"
	PUName = "PU"
	prefireName = "prefire"
	weightName = "PdfWeights"


	bkgHistDY = getRebinnedHistogram(bkgHistDYTemp,binning,"bkgHistDY_%s"%channel)

        bkgHistDYStatUp   = getStatUncertHistogram(bkgHistDY,"bkgHistDY_%s_%sUp"%(statName,channel),True)
        bkgHistDYStatDown = getStatUncertHistogram(bkgHistDY,"bkgHistDY_%s_%sDown"%(statName,channel))

        bkgHistDYScaleDown = getRebinnedHistogram(bkgHistDYScaleDownTemp,binning,"bkgHistDY_%s_%sDown"%(scaleName,channel))
	if "muon" in channel:
        	bkgHistDYScaleUp = getRebinnedHistogram(bkgHistDYScaleDownTemp,binning,"bkgHistDY_%s_%sUp"%(scaleName,channel))
        	bkgHistDYIDDown = getRebinnedHistogram(bkgHistDYIDTemp, binning, "bkgHistDY_%s_%sDown"%(IDName,channel))
        	bkgHistDYIDUp = getRebinnedHistogram(bkgHistDYIDTemp, binning, "bkgHistDY_%s_%sUp"%(IDName,channel))
	        bkgHistDYSmearUp = getRebinnedHistogram(bkgHistDYSmearTemp, binning, "bkgHistDY_%s_%sUp"%(smearName,channel))
        	bkgHistDYSmearDown = getRebinnedHistogram(bkgHistDYSmearTemp, binning, "bkgHistDY_%s_%sDown"%(smearName,channel))
	else:
 	        bkgHistDYPUDown = getRebinnedHistogram(bkgHistDYPUDownTemp, binning, "bkgHistDY_%sDown"%(PUName))
        	bkgHistDYPUUp = getRebinnedHistogram(bkgHistDYPUUpTemp, binning, "bkgHistDY_%sUp"%(PUName))
       		bkgHistDYScaleUp = getRebinnedHistogram(bkgHistDYScaleUpTemp,binning,"bkgHistDY_%s_%sUp"%(scaleName,channel))
 	        bkgHistDYPrefireDown = getRebinnedHistogram(bkgHistDYPrefireDownTemp, binning, "bkgHistDY_%sDown"%(prefireName))
        	bkgHistDYPrefireUp = getRebinnedHistogram(bkgHistDYPrefireUpTemp, binning, "bkgHistDY_%sUp"%(prefireName))

        bkgHistDYPDFDown = getPDFUncertHistogram(bkgHistDY,"bkgHistDY_%sDown"%(pdfName), pdfUncertDY)
        bkgHistDYPDFUp =   getPDFUncertHistogram(bkgHistDY,"bkgHistDY_%sUp"%(pdfName),   pdfUncertDY,True)

	bkgHistOther = getRebinnedHistogram(bkgHistOtherTemp,binning,"bkgHistOther_%s"%channel)

        bkgHistOtherStatUp   = getStatUncertHistogram(bkgHistOther,"bkgHistOther_%s_%sUp"%(statName,channel),True)
        bkgHistOtherStatDown = getStatUncertHistogram(bkgHistOther,"bkgHistOther_%s_%sDown"%(statName,channel))

        bkgHistOtherScaleDown = getRebinnedHistogram(bkgHistOtherScaleDownTemp,binning,"bkgHistOther_%s_%sDown"%(scaleName,channel))
	if "muon" in channel:
        	bkgHistOtherScaleUp = getRebinnedHistogram(bkgHistOtherScaleDownTemp,binning,"bkgHistOther_%s_%sUp"%(scaleName,channel))
        	bkgHistOtherIDDown = getRebinnedHistogram(bkgHistOtherIDTemp, binning, "bkgHistOther_%s_%sDown"%(IDName,channel))
        	bkgHistOtherIDUp = getRebinnedHistogram(bkgHistOtherIDTemp, binning, "bkgHistOther_%s_%sUp"%(IDName,channel))
	        bkgHistOtherSmearUp = getRebinnedHistogram(bkgHistOtherSmearTemp, binning, "bkgHistOther_%s_%sUp"%(smearName,channel))
        	bkgHistOtherSmearDown = getRebinnedHistogram(bkgHistOtherSmearTemp, binning, "bkgHistOther_%s_%sDown"%(smearName,channel))
	else:
 	        bkgHistOtherPUDown = getRebinnedHistogram(bkgHistOtherPUDownTemp, binning, "bkgHistOther_%sDown"%(PUName))
        	bkgHistOtherPUUp = getRebinnedHistogram(bkgHistOtherPUUpTemp, binning, "bkgHistOther_%sUp"%(PUName))
  	        bkgHistOtherPrefireDown = getRebinnedHistogram(bkgHistOtherPrefireDownTemp, binning, "bkgHistOther_%sDown"%(prefireName))
        	bkgHistOtherPrefireUp = getRebinnedHistogram(bkgHistOtherPrefireUpTemp, binning, "bkgHistOther_%sUp"%(prefireName))
       		bkgHistOtherScaleUp = getRebinnedHistogram(bkgHistOtherScaleUpTemp,binning,"bkgHistOther_%s_%sUp"%(scaleName,channel))
        bkgHistOtherPDFDown = getPDFUncertHistogram(bkgHistOther,"bkgHistOther_%sDown"%(pdfName), pdfUncertOther)
        bkgHistOtherPDFUp = getPDFUncertHistogram(bkgHistOther,"bkgHistOther_%sUp"%(pdfName), pdfUncertOther,True)

	
        bkgHistJets = getRebinnedHistogram(bkgHistJetsTemp,binning,"bkgHistJets_%s"%channel)
        #bkgHistJets = bkgHistJetsTemp

        sigHist = ROOT.TH1F("sigHist_%s"%channel,"sigHist_%s"%channel,len(binning)-1,array('f',binning))
        sigHistStatUp = ROOT.TH1F("sigHist_%s_%sUp"%(statName,channel),"sigHistStat_%s_%sUp"%(channel,statName),len(binning)-1,array('f',binning))
        sigHistStatDown = ROOT.TH1F("sigHist_%s_%sDown"%(statName,channel),"sigHistStat_%s_%sDown"%(channel,statName),len(binning)-1,array('f',binning))
        sigHistPdfWeightsUp = ROOT.TH1F("sigHist_%sUp"%(weightName),"sigHist_%sUp"%(weightName),len(binning)-1,array('f',binning))
        sigHistPdfWeightsDown = ROOT.TH1F("sigHist_%sDown"%(weightName),"sigHist_%sDown"%(weightName),len(binning)-1,array('f',binning))
        sigHistScaleDown = ROOT.TH1F("sigHist_%s_%sDown"%(scaleName,channel),"sigHistScaleDown_%s_%s"%(channel,scaleName),len(binning)-1,array('f',binning))
        sigHistPDFDown = ROOT.TH1F("sigHist_%sDown"%(pdfName),"sigHistPDFDown_%s_%s"%(channel,pdfName),len(binning)-1,array('f',binning))
        sigHistPDFUp = ROOT.TH1F("sigHist_%sUp"%(pdfName),"sigHistPDFUp_%s_%s"%(channel,pdfName),len(binning)-1,array('f',binning))
	if "muon" in channel:
        	sigHistIDDown = ROOT.TH1F("sigHist_%s_%sDown"%(IDName,channel),"sigHistIDDown_%s_%s"%(channel,IDName),len(binning)-1,array('f',binning))
        	sigHistIDUp = ROOT.TH1F("sigHist_%s_%sUp"%(IDName,channel),"sigHistIDUp_%s_%s"%(channel,IDName),len(binning)-1,array('f',binning))
	        sigHistSmearUp = ROOT.TH1F("sigHist_%s_%sUp"%(smearName,channel),"sigHistSmear_%s_%sUp"%(channel,smearName),len(binning)-1,array('f',binning))
        	sigHistSmearDown = ROOT.TH1F("sigHist_%s_%sDown"%(smearName,channel),"sigHistSmear_%s_%sDown"%(channel,smearName),len(binning)-1,array('f',binning))
	else:
	        sigHistPUDown = ROOT.TH1F("sigHist_%sDown"%(PUName),"sigHistPUDown_%s_%s"%(channel,PUName),len(binning)-1,array('f',binning))
        	sigHistPUUp = ROOT.TH1F("sigHist_%sUp"%(PUName),"sigHistPUUp_%s_%s"%(channel,PUName),len(binning)-1,array('f',binning))
	        sigHistPrefireDown = ROOT.TH1F("sigHist_%sDown"%(prefireName),"sigHistPUDown_%s_%s"%(channel,prefireName),len(binning)-1,array('f',binning))
        	sigHistPrefireUp = ROOT.TH1F("sigHist_%sUp"%(prefireName),"sigHistPUUp_%s_%s"%(channel,prefireName),len(binning)-1,array('f',binning))

        sigHistScaleUp = ROOT.TH1F("sigHist_%s_%sUp"%(scaleName,channel),"sigHistScaleUp_%s_%s"%(channel,scaleName),len(binning)-1,array('f',binning))

        dataHist = getRebinnedHistogram(dataHistTemp, binning, "dataHist_%s"%channel)

	

	for index, lower in enumerate(binning):	
		if index < len(binning)-1:
			label = "CITo2Mu_Lam%dTeV%s_%s"%(L,interference,channel)
			if "electron" in channel:
				label = "CITo2E_Lam%dTeV%s_%s"%(L,interference,channel)
			if "ADD" in scanConfigName:
				label = "ADDGravTo2Mu_Lam%d_%s"%(L,channel)
				if "electron" in channel:
					label = "ADDGravTo2E_Lam%d_%s"%(L,channel)
			val = max(0,signalYields_default[label][str(index)][0])
			err = signalYields_default[label][str(index)][1]
			sigHistPDFUp.SetBinContent(index+1,max(1e-9,val+val*pdfUncert[index]))
			sigHistPDFDown.SetBinContent(index+1,max(1e-9,val-val*pdfUncert[index]))
			sigHist.SetBinContent(index+1,max(1e-9,val))
			sigHistStatUp.SetBinContent(index+1,max(1e-9,val+val*err))
			sigHistStatDown.SetBinContent(index+1,max(1e-9,val-val*err))
			val = signalYields_scaleDown[label][str(index)][0]
			sigHistScaleDown.SetBinContent(index+1,max(1e-9,val))

			val = signalYields_pdfWeightsUp[label][str(index)][0]
			sigHistPdfWeightsUp.SetBinContent(index+1,max(1e-9,val))

			val = signalYields_pdfWeightsDown[label][str(index)][0]
			sigHistPdfWeightsDown.SetBinContent(index+1,max(1e-9,val))

			if "muon" in channel:
				val = signalYields_ID[label][str(index)][0]
				sigHistIDUp.SetBinContent(index+1,max(1e-9,val))
				sigHistIDDown.SetBinContent(index+1,max(1e-9,val))
				val = signalYields_resolution[label][str(index)][0]
				sigHistSmearDown.SetBinContent(index+1,max(1e-9,val))
				sigHistSmearUp.SetBinContent(index+1,max(1e-9,val))
				sigHistScaleUp.SetBinContent(index+1,sigHist.GetBinContent(index+1))
			if "electron" in channel:
				val = signalYields_scaleUp[label][str(index)][0]
				sigHistScaleUp.SetBinContent(index+1,max(1e-9,val))
				val = signalYields_piledown[label][str(index)][0]
				sigHistPUDown.SetBinContent(index+1,max(1e-9,val))
				val = signalYields_pileup[label][str(index)][0]
				sigHistPUUp.SetBinContent(index+1,max(1e-9,val))
				val = signalYields_prefireDown[label][str(index)][0]
				sigHistPrefireDown.SetBinContent(index+1,max(1e-9,val))
				val = signalYields_prefireUp[label][str(index)][0]
				sigHistPrefireUp.SetBinContent(index+1,max(1e-9,val))

	bkgIntegralDY = bkgHistDY.Integral()		
	bkgIntegralOther = bkgHistOther.Integral()		
	bkgIntegralJets = bkgHistJets.Integral()		
	sigIntegral = sigHist.Integral()

	histFile.Write()
	histFile.Close()


        return [bkgIntegralDY,bkgIntegralOther,bkgIntegralJets,sigIntegral]


	
def createHistogramsIntCI(L,interference,name,channel,scanConfigName,dataFile=""):
	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)


	configName ="channelConfig_%s"%channel
        config =  __import__(configName)
	
	scanConfigName ="scanConfiguration_%s"%scanConfigName
        scanConfig =  __import__(scanConfigName)
	
        binning = scanConfig.binning
	if dataFile == "":
		dataFile = config.dataFile
	with open(dataFile) as f:
    		events = f.readlines()

	if 'electron' in channel:
		lowestMass = 400
	elif 'muon' in channel:
		lowestMass = 400
        from array import array
 


	

	if 'ADD' in scanConfigName:
		model = 'ADD'
	else: 
		model = 'CI'


	inputFileName = "input/inputsCI/inputsCI_%s.root"%(channel)
        inputFile = ROOT.TFile(inputFileName, "OPEN")

	import pickle 
	if "muon" in channel:
		pkl = open("input/inputsCI/%ssignalYields_default.pkl"%model, "r")
		signalYields_default = pickle.load(pkl)

		pkl = open("input/inputsCI/%ssignalYields_scaleDown.pkl"%model, "r")
		signalYields_scaleDown = pickle.load(pkl)

		pkl = open("input/inputsCI/%ssignalYields_pdfWeightsUp.pkl"%model, "r")
		signalYields_pdfWeightsUp = pickle.load(pkl)

		pkl = open("input/inputsCI/%ssignalYields_pdfWeightsDown.pkl"%model, "r")
		signalYields_pdfWeightsDown = pickle.load(pkl)

		#pkl = open("input/inputsCI/signalYields_piledown.pkl", "r")
		#signalYields_piledown = pickle.load(pkl)

		#pkl = open("input/inputsCI/signalYields_pileup.pkl", "r")
		#signalYields_pileup = pickle.load(pkl)

		pkl = open("input/inputsCI/%ssignalYields_resolution.pkl"%model, "r")
		signalYields_resolution = pickle.load(pkl)

		pkl = open("input/inputsCI/%ssignalYields_ID.pkl"%model, "r")
		signalYields_ID = pickle.load(pkl)
	elif "electron" in channel:
		pkl = open("input/inputsCI/%ssignalYieldsEle_default.pkl"%model, "r")
		signalYields_default = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsEle_scaleUp.pkl"%model, "r")
		signalYields_scaleUp = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsEle_scaleDown.pkl"%model, "r")
		signalYields_scaleDown = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsEle_piledown.pkl"%model, "r")
		signalYields_piledown = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsEle_pileup.pkl"%model, "r")
		signalYields_pileup = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsEle_pdfWeightsUp.pkl"%model, "r")
		signalYields_pdfWeightsUp = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsEle_pdfWeightsDown.pkl"%model, "r")
		signalYields_pdfWeightsDown = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsEle_prefireup.pkl"%model, "r")
		signalYields_prefireup = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsEle_prefiredown.pkl"%model, "r")
		signalYields_prefiredown = pickle.load(pkl)




	histFile = ROOT.TFile("%s.root"%name, "RECREATE")	
	bkgHistDYTemp = inputFile.Get("bkgHistDY_%s"%channel)
	bkgHistDYScaleDownTemp = inputFile.Get("bkgHistDYScaleDown_%s"%channel)
	if "muon" in channel:
		bkgHistDYIDTemp = inputFile.Get("bkgHistDYWeighted_%s"%channel)
		bkgHistDYSmearTemp = inputFile.Get("bkgHistDYSmeared_%s"%channel)
	if "electron" in channel:
		bkgHistDYPUDownTemp = inputFile.Get("bkgHistDYPUDown_%s"%channel)
		bkgHistDYPUUpTemp = inputFile.Get("bkgHistDYPUUp_%s"%channel)
		bkgHistDYPrefireDownTemp = inputFile.Get("bkgHistDYPrefireDown_%s"%channel)
		bkgHistDYPrefireUpTemp = inputFile.Get("bkgHistDYPrefireUp_%s"%channel)
		bkgHistDYScaleUpTemp = inputFile.Get("bkgHistDYScaleUp_%s"%channel)

	bkgHistOtherTemp = inputFile.Get("bkgHistOther_%s"%channel)
	bkgHistOtherScaleDownTemp = inputFile.Get("bkgHistOtherScaleDown_%s"%channel)
	if "muon" in channel:
		bkgHistOtherIDTemp = inputFile.Get("bkgHistOtherWeighted_%s"%channel)
		bkgHistOtherSmearTemp = inputFile.Get("bkgHistOtherSmeared_%s"%channel)
	if "electron" in channel:
		bkgHistOtherScaleUpTemp = inputFile.Get("bkgHistOtherScaleUp_%s"%channel)
		bkgHistOtherPUDownTemp = inputFile.Get("bkgHistOtherPUDown_%s"%channel)
		bkgHistOtherPUUpTemp = inputFile.Get("bkgHistOtherPUUp_%s"%channel)
		bkgHistOtherPrefireDownTemp = inputFile.Get("bkgHistOtherPrefireDown_%s"%channel)
		bkgHistOtherPrefireUpTemp = inputFile.Get("bkgHistOtherPrefireUp_%s"%channel)

	bkgHistJetsTemp = inputFile.Get("bkgHistJets_%s"%channel)
	if "ADD" in scanConfigName:
		pdfUncert = [0.10312327041448502,0.11631416752423052,0.13116564710563733,0.14414683366902137,0.17666058539426496]	
		pdfUncertDY = [0.0365003172410037, 0.0429886021839947, 0.047645134519074, 0.069030181137942, 0.119036982092236]
		pdfUncertOther = [0.1789670634151592, 0.269902491201715, 0.2699234253751208, 0.2984407542188063, 0.3777961331626525]	
	else:
		pdfUncert = [0.029808675319316736,0.032492944178882606,0.046693632068081733,0.06985339137281024,0.11520346316811705,0.17965523337854952]
		pdfUncertDY = [0.0133126577202494, 0.0147788328624159, 0.01842209757115, 0.0243644300786998, 0.039572839847093, 0.1144248733154136]
		pdfUncertOther = [0.0358232181870253, 0.088892531404347, 0.1254268509362337, 0.1736824180528946, 0.2024257617076786, 0.3369525304968204]

	dataHistTemp = inputFile.Get("dataHist_%s"%channel)
	dataIntegral = dataHistTemp.Integral(dataHistTemp.FindBin(lowestMass),dataHistTemp.GetNbinsX())

        scaleName = "massScale"
        statName = "stats"
	smearName = "res"
	pdfName = "pdf"
	IDName = "ID"
	PUName = "PU"
	weightName = "PdfWeights"
	prefireName = "prefire"


	bkgHistDY = getRebinnedHistogram(bkgHistDYTemp,binning,"bkgHistDY_%s"%channel)

        bkgHistDYStatUp   = getStatUncertHistogram(bkgHistDY,"bkgHistDY_%s_%sUp"%(statName,channel),True)
        bkgHistDYStatDown = getStatUncertHistogram(bkgHistDY,"bkgHistDY_%s_%sDown"%(statName,channel))

        bkgHistDYScaleDown = getRebinnedHistogram(bkgHistDYScaleDownTemp,binning,"bkgHistDY_%s_%sDown"%(scaleName,channel))
	if "muon" in channel:
        	bkgHistDYScaleUp = getRebinnedHistogram(bkgHistDYScaleDownTemp,binning,"bkgHistDY_%s_%sUp"%(scaleName,channel))
        	bkgHistDYIDDown = getRebinnedHistogram(bkgHistDYIDTemp, binning, "bkgHistDY_%s_%sDown"%(IDName,channel))
        	bkgHistDYIDUp = getRebinnedHistogram(bkgHistDYIDTemp, binning, "bkgHistDY_%s_%sUp"%(IDName,channel))
	        bkgHistDYSmearUp = getRebinnedHistogram(bkgHistDYSmearTemp, binning, "bkgHistDY_%s_%sUp"%(smearName,channel))
        	bkgHistDYSmearDown = getRebinnedHistogram(bkgHistDYSmearTemp, binning, "bkgHistDY_%s_%sDown"%(smearName,channel))
	else:
        	bkgHistDYScaleUp = getRebinnedHistogram(bkgHistDYScaleUpTemp,binning,"bkgHistDY_%s_%sUp"%(scaleName,channel))
	        bkgHistDYPUDown = getRebinnedHistogram(bkgHistDYPUDownTemp, binning, "bkgHistDY_%sDown"%(PUName))
        	bkgHistDYPUUp = getRebinnedHistogram(bkgHistDYPUUpTemp, binning, "bkgHistDY_%sUp"%(PUName))
	        bkgHistDYPrefireDown = getRebinnedHistogram(bkgHistDYPrefireDownTemp, binning, "bkgHistDY_%sDown"%(prefireName))
        	bkgHistDYPrefireUp = getRebinnedHistogram(bkgHistDYPrefireUpTemp, binning, "bkgHistDY_%sUp"%(prefireName))

        bkgHistDYPDFDown = getPDFUncertHistogram(bkgHistDY,"bkgHistDY_%sDown"%(pdfName), pdfUncertDY)
        bkgHistDYPDFUp =   getPDFUncertHistogram(bkgHistDY,"bkgHistDY_%sUp"%(pdfName),   pdfUncertDY,True)

	bkgHistOther = getRebinnedHistogram(bkgHistOtherTemp,binning,"bkgHistOther_%s"%channel)

        bkgHistOtherStatUp   = getStatUncertHistogram(bkgHistOther,"bkgHistOther_%s_%sUp"%(statName,channel),True)
        bkgHistOtherStatDown = getStatUncertHistogram(bkgHistOther,"bkgHistOther_%s_%sDown"%(statName,channel))

        bkgHistOtherScaleDown = getRebinnedHistogram(bkgHistOtherScaleDownTemp,binning,"bkgHistOther_%s_%sDown"%(scaleName,channel))
	if "muon" in channel:
        	bkgHistOtherScaleUp = getRebinnedHistogram(bkgHistOtherScaleDownTemp,binning,"bkgHistOther_%s_%sUp"%(scaleName,channel))
        	bkgHistOtherIDDown = getRebinnedHistogram(bkgHistOtherIDTemp, binning, "bkgHistOther_%s_%sDown"%(IDName,channel))
        	bkgHistOtherIDUp = getRebinnedHistogram(bkgHistOtherIDTemp, binning, "bkgHistOther_%s_%sUp"%(IDName,channel))
	        bkgHistOtherSmearUp = getRebinnedHistogram(bkgHistOtherSmearTemp, binning, "bkgHistOther_%s_%sUp"%(smearName,channel))
        	bkgHistOtherSmearDown = getRebinnedHistogram(bkgHistOtherSmearTemp, binning, "bkgHistOther_%s_%sDown"%(smearName,channel))
	else:
        	bkgHistOtherScaleUp = getRebinnedHistogram(bkgHistOtherScaleUpTemp,binning,"bkgHistOther_%s_%sUp"%(scaleName,channel))
	        bkgHistOtherPUDown = getRebinnedHistogram(bkgHistOtherPUDownTemp, binning, "bkgHistOther_%sDown"%(PUName))
        	bkgHistOtherPUUp = getRebinnedHistogram(bkgHistOtherPUUpTemp, binning, "bkgHistOther_%sUp"%(PUName))
	        bkgHistOtherPrefireDown = getRebinnedHistogram(bkgHistOtherPrefireDownTemp, binning, "bkgHistOther_%sDown"%(prefireName))
        	bkgHistOtherPrefireUp = getRebinnedHistogram(bkgHistOtherPrefireUpTemp, binning, "bkgHistOther_%sUp"%(prefireName))

        bkgHistOtherPDFDown = getPDFUncertHistogram(bkgHistOther,"bkgHistOther_%sDown"%(pdfName), pdfUncertOther)
        bkgHistOtherPDFUp = getPDFUncertHistogram(bkgHistOther,"bkgHistOther_%sUp"%(pdfName), pdfUncertOther,True)

	
        bkgHistJets = getRebinnedHistogram(bkgHistJetsTemp,binning,"bkgHistJets_%s"%channel)

        sigHist = ROOT.TH1F("sigHist_%s"%channel,"sigHist_%s"%channel,len(binning)-1,array('f',binning))
        sigHistStatUp = ROOT.TH1F("sigHist_%s_%sUp"%(statName,channel),"sigHistStat_%s_%sUp"%(channel,statName),len(binning)-1,array('f',binning))
        sigHistStatDown = ROOT.TH1F("sigHist_%s_%sDown"%(statName,channel),"sigHistStat_%s_%sDown"%(channel,statName),len(binning)-1,array('f',binning))
        sigHistScaleDown = ROOT.TH1F("sigHist_%s_%sDown"%(scaleName,channel),"sigHistScaleDown_%s_%s"%(channel,scaleName),len(binning)-1,array('f',binning))
        sigHistPDFDown = ROOT.TH1F("sigHist_%sDown"%(pdfName),"sigHistPDFDown_%s_%s"%(channel,pdfName),len(binning)-1,array('f',binning))
        sigHistPDFUp = ROOT.TH1F("sigHist_%sUp"%(pdfName),"sigHistPDFUp_%s_%s"%(channel,pdfName),len(binning)-1,array('f',binning))
        sigHistPdfWeightsDown = ROOT.TH1F("sigHist_%sDown"%(weightName),"sigHistDown_%s_%s"%(channel,weightName),len(binning)-1,array('f',binning))
        sigHistPdfWeightsUp = ROOT.TH1F("sigHist_%sUp"%(weightName),"sigHistUp_%s_%s"%(channel,weightName),len(binning)-1,array('f',binning))
	if "muon" in channel:
        	sigHistIDDown = ROOT.TH1F("sigHist_%s_%sDown"%(IDName,channel),"sigHistIDDown_%s_%s"%(channel,IDName),len(binning)-1,array('f',binning))
        	sigHistIDUp = ROOT.TH1F("sigHist_%s_%sUp"%(IDName,channel),"sigHistIDUp_%s_%s"%(channel,IDName),len(binning)-1,array('f',binning))
	        sigHistSmearUp = ROOT.TH1F("sigHist_%s_%sUp"%(smearName,channel),"sigHistSmear_%s_%sUp"%(channel,smearName),len(binning)-1,array('f',binning))
        	sigHistSmearDown = ROOT.TH1F("sigHist_%s_%sDown"%(smearName,channel),"sigHistSmear_%s_%sDown"%(channel,smearName),len(binning)-1,array('f',binning))
	else:
	        sigHistPUDown = ROOT.TH1F("sigHist_%sDown"%(PUName),"sigHistPUDown_%s_%s"%(channel,PUName),len(binning)-1,array('f',binning))
        	sigHistPUUp = ROOT.TH1F("sigHist_%sUp"%(PUName),"sigHistPUUp_%s_%s"%(channel,PUName),len(binning)-1,array('f',binning))
	        sigHistPrefireDown = ROOT.TH1F("sigHist_%sDown"%(prefireName),"sigHistPrefireDown_%s_%s"%(channel,prefireName),len(binning)-1,array('f',binning))
        	sigHistPrefireUp = ROOT.TH1F("sigHist_%sUp"%(prefireName),"sigHistPrefireUp_%s_%s"%(channel,prefireName),len(binning)-1,array('f',binning))

        sigHistScaleUp = ROOT.TH1F("sigHist_%s_%sUp"%(scaleName,channel),"sigHistScaleUp_%s_%s"%(channel,scaleName),len(binning)-1,array('f',binning))

        intHist = ROOT.TH1F("intHist_%s"%channel,"intHist_%s"%channel,len(binning)-1,array('f',binning))
        intHistStatUp = ROOT.TH1F("intHist_%s_%sUp"%(statName,channel),"intHistStat_%s_%sUp"%(channel,statName),len(binning)-1,array('f',binning))
        intHistStatDown = ROOT.TH1F("intHist_%s_%sDown"%(statName,channel),"intHistStat_%s_%sDown"%(channel,statName),len(binning)-1,array('f',binning))
        intHistScaleDown = ROOT.TH1F("intHist_%s_%sDown"%(scaleName,channel),"intHistScaleDown_%s_%s"%(channel,scaleName),len(binning)-1,array('f',binning))
        intHistPDFDown = ROOT.TH1F("intHist_%sDown"%(pdfName),"intHistPDFDown_%s_%s"%(channel,pdfName),len(binning)-1,array('f',binning))
        intHistPDFUp = ROOT.TH1F("intHist_%sUp"%(pdfName),"intHistPDFUp_%s_%s"%(channel,pdfName),len(binning)-1,array('f',binning))
        intHistPdfWeightsDown = ROOT.TH1F("intHist_%sDown"%(weightName),"intHistDown_%s_%s"%(channel,weightName),len(binning)-1,array('f',binning))
        intHistPdfWeightsUp = ROOT.TH1F("intHist_%sUp"%(weightName),"intHistUp_%s_%s"%(channel,weightName),len(binning)-1,array('f',binning))
	
	if "muon" in channel:
        	intHistIDDown = ROOT.TH1F("intHist_%s_%sDown"%(IDName,channel),"intHistIDDown_%s_%s"%(channel,IDName),len(binning)-1,array('f',binning))
        	intHistIDUp = ROOT.TH1F("intHist_%s_%sUp"%(IDName,channel),"intHistIDUp_%s_%s"%(channel,IDName),len(binning)-1,array('f',binning))
	        intHistSmearUp = ROOT.TH1F("intHist_%s_%sUp"%(smearName,channel),"intHistSmear_%s_%sUp"%(channel,smearName),len(binning)-1,array('f',binning))
        	intHistSmearDown = ROOT.TH1F("intHist_%s_%sDown"%(smearName,channel),"intHistSmear_%s_%sDown"%(channel,smearName),len(binning)-1,array('f',binning))
	else:
	        intHistPUDown = ROOT.TH1F("intHist_%sDown"%(PUName),"intHistPUDown_%s_%s"%(channel,PUName),len(binning)-1,array('f',binning))
        	intHistPUUp = ROOT.TH1F("intHist_%sUp"%(PUName),"intHistPUUp_%s_%s"%(channel,PUName),len(binning)-1,array('f',binning))
	        intHistPrefireDown = ROOT.TH1F("intHist_%sDown"%(prefireName),"intHistprefireDown_%s_%s"%(channel,prefireName),len(binning)-1,array('f',binning))
        	intHistPrefireUp = ROOT.TH1F("intHist_%sUp"%(prefireName),"intHistPrefireUp_%s_%s"%(channel,prefireName),len(binning)-1,array('f',binning))

        intHistScaleUp = ROOT.TH1F("intHist_%s_%sUp"%(scaleName,channel),"intHistScaleUp_%s_%s"%(channel,scaleName),len(binning)-1,array('f',binning))




        dataHist = getRebinnedHistogram(dataHistTemp, binning, "dataHist_%s"%channel)

	if "LL" in interference:  hel = "LL"
	elif "LR" in interference: hel = "LR"
	elif "RL" in interference: hel = "RL"
	else:                     hel = "RR"
	for index, lower in enumerate(binning):	
		if index < len(binning)-1:
			label = "CITo2Mu_Lam%dTeV%s_%s"%(L,hel,channel)
			if "electron" in channel:
				label = "CITo2E_Lam%dTeV%s_%s"%(L,hel,channel)
			val = signalYields_default[label][str(index)][0]
			val = max(1e-9,val)
			err = signalYields_default[label][str(index)][1]
			sigHistPDFUp.SetBinContent(index+1,max(1e-9,val+val*pdfUncert[index]))
			sigHistPDFDown.SetBinContent(index+1,max(1e-9,val-val*pdfUncert[index]))
			sigHist.SetBinContent(index+1,max(1e-9,val))
			sigHistStatUp.SetBinContent(index+1,max(1e-9,val+val*err))
			sigHistStatDown.SetBinContent(index+1,max(1e-9,val-val*err))
			val = signalYields_scaleDown[label][str(index)][0]
			val = max(1e-9,val)
			sigHistScaleDown.SetBinContent(index+1,max(1e-9,val))

			val = signalYields_pdfWeightsDown[label][str(index)][0]
			val = max(1e-9,val)
			sigHistPdfWeightsDown.SetBinContent(index+1,max(1e-9,val))
			val = signalYields_pdfWeightsUp[label][str(index)][0]
			val = max(1e-9,val)
			sigHistPdfWeightsUp.SetBinContent(index+1,max(1e-9,val))

			if "muon" in channel:
				val = signalYields_ID[label][str(index)][0]
				val = max(1e-9,val)
				sigHistIDUp.SetBinContent(index+1,max(1e-9,val))
				sigHistIDDown.SetBinContent(index+1,max(1e-9,val))
				val = signalYields_resolution[label][str(index)][0]
				val = max(1e-9,val)
				sigHistSmearDown.SetBinContent(index+1,max(1e-9,val))
				sigHistSmearUp.SetBinContent(index+1,max(1e-9,val))
				sigHistScaleUp.SetBinContent(index+1,sigHist.GetBinContent(index+1))
			if "electron" in channel:
				val = signalYields_scaleUp[label][str(index)][0]
				val = max(1e-9,val)
				sigHistScaleUp.SetBinContent(index+1,max(1e-9,val))
				val = signalYields_piledown[label][str(index)][0]
				val = max(1e-9,val)
				sigHistPUDown.SetBinContent(index+1,max(1e-9,val))
				val = signalYields_pileup[label][str(index)][0]
				val = max(1e-9,val)
				sigHistPUUp.SetBinContent(index+1,max(1e-9,val))
				val = signalYields_prefiredown[label][str(index)][0]
				val = max(1e-9,val)
				sigHistPrefireDown.SetBinContent(index+1,max(1e-9,val))
				val = signalYields_prefireup[label][str(index)][0]
				val = max(1e-9,val)
				sigHistPrefireUp.SetBinContent(index+1,max(1e-9,val))

	for index, lower in enumerate(binning):	
		if index < len(binning)-1:
			label = "CITo2Mu_Lam%dTeV%s_%s"%(L,interference,channel)
			if "electron" in channel:
				label = "CITo2E_Lam%dTeV%s_%s"%(L,interference,channel)
			val = signalYields_default[label][str(index)][0]
			err = signalYields_default[label][str(index)][1]
			if err > 1.0:
				err = 0.5
			intHistPDFUp.SetBinContent(index+1,val+val*pdfUncert[index])
			intHistPDFDown.SetBinContent(index+1,val-val*pdfUncert[index])
			intHist.SetBinContent(index+1,val)
			intHistStatUp.SetBinContent(index+1,val+abs(val*err))
			intHistStatDown.SetBinContent(index+1,max(1e-9,val-abs(val*err)))
			#intHistStatDown.SetBinContent(index+1,val-val*err)
			val = signalYields_scaleDown[label][str(index)][0]
			#val = max(1e-9,val)
			intHistScaleDown.SetBinContent(index+1,val)

			val = signalYields_pdfWeightsDown[label][str(index)][0]
			#val = max(1e-9,val)
			intHistPdfWeightsDown.SetBinContent(index+1,max(1e-9,val))
			val = signalYields_pdfWeightsUp[label][str(index)][0]
			#val = max(1e-9,val)
			intHistPdfWeightsUp.SetBinContent(index+1,max(1e-9,val))

			if "muon" in channel:
				val = signalYields_ID[label][str(index)][0]
				#val = max(1e-9,val)
				intHistIDUp.SetBinContent(index+1,val)
				intHistIDDown.SetBinContent(index+1,val)
				val = signalYields_resolution[label][str(index)][0]
				#val = max(1e-9,val)
				intHistSmearDown.SetBinContent(index+1,val)
				intHistSmearUp.SetBinContent(index+1,val)
				intHistScaleUp.SetBinContent(index+1,intHist.GetBinContent(index+1))
			if "electron" in channel:
				val = signalYields_scaleUp[label][str(index)][0]
				#val = max(1e-9,val)
				intHistScaleUp.SetBinContent(index+1,val)
				val = signalYields_piledown[label][str(index)][0]
				#val = max(1e-9,val)
				intHistPUDown.SetBinContent(index+1,val)
				val = signalYields_pileup[label][str(index)][0]
				#val = max(1e-9,val)
				intHistPUUp.SetBinContent(index+1,val)
				val = signalYields_prefiredown[label][str(index)][0]
				#val = max(1e-9,val)
				intHistPrefireDown.SetBinContent(index+1,val)
				val = signalYields_prefireup[label][str(index)][0]
				#val = max(1e-9,val)
				intHistPrefireUp.SetBinContent(index+1,val)



        intHist.Add(bkgHistDY.Clone())
        intHistStatUp.Add(bkgHistDYStatUp.Clone())
        intHistStatDown.Add(bkgHistDYStatDown.Clone())
        intHistScaleDown.Add(bkgHistDYScaleDown.Clone())
        intHistPDFDown.Add(bkgHistDYPDFDown.Clone())
        intHistPDFUp.Add(bkgHistDYPDFUp.Clone())
        intHistPdfWeightsDown.Add(bkgHistDY.Clone())
        intHistPdfWeightsUp.Add(bkgHistDY.Clone())
	if "muon" in channel:
         	intHistIDDown.Add(bkgHistDYIDDown.Clone())
        	intHistIDUp.Add(bkgHistDYIDUp.Clone())
 	      	intHistSmearDown.Add(bkgHistDYSmearDown.Clone())
        	intHistSmearUp.Add(bkgHistDYSmearUp.Clone())
	else:
	        intHistPUDown.Add(bkgHistDYPUDown.Clone())
        	intHistPUUp.Add(bkgHistDYPUUp.Clone())
	        intHistPrefireDown.Add(bkgHistDYPrefireDown.Clone())
        	intHistPrefireUp.Add(bkgHistDYPrefireUp.Clone())

        intHistScaleUp.Add(bkgHistDYScaleUp.Clone())


	intIntegral = intHist.Integral()		
	bkgIntegralDY = bkgHistDY.Integral()		
	bkgIntegralOther = bkgHistOther.Integral()		
	bkgIntegralJets = bkgHistJets.Integral()		
	sigIntegral = sigHist.Integral()

	histFile.Write()
	histFile.Close()


        return [bkgIntegralDY,bkgIntegralOther,bkgIntegralJets,sigIntegral,intIntegral]




def createSingleBinCI(L,interference,name,channel,scanConfigName,mThresh,addSigDY,ADD,dataFile=""):
	ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

	binMap={'400':'0','500':'1','700':'2','1100':'3','1900':'4','3500':'5'}
	#mThreshList = binMap[mThresh]
	mThreshList = int(mThresh)
	mThreshList = mThresh

	configName ="channelConfig_%s"%channel
        config =  __import__(configName)
	
	scanConfigName ="scanConfiguration_%s"%scanConfigName
        scanConfig =  __import__(scanConfigName)
	
	#kaushal added
	for x in range(len(scanConfig.binning)-1):
		if (int(mThresh) == scanConfig.binning[x]):
			upperBound = scanConfig.binning[x+1]
	
	
	result = {}	
	

	import pickle
	
	#dummy instantiation
	fileBegin = "ADD" if ADD else "CI"
	if "muon" in channel:
		pkl = open("input/inputsCI/"+fileBegin+"signalYieldsSingleBin_default.pkl", "r")
		signalYields_default = pickle.load(pkl)
		pkl = open("input/inputsCI/"+fileBegin+"signalYieldsSingleBin_scaleDown.pkl", "r")
		signalYields_scaleDown = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsSingleBin_pdfWeightsUp.pkl"%fileBegin, "r")
		signalYields_pdfWeightsUp = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsSingleBin_pdfWeightsDown.pkl"%fileBegin, "r")
		signalYields_pdfWeightsDown = pickle.load(pkl)
		pkl = open("input/inputsCI/"+fileBegin+"signalYieldsSingleBin_resolution.pkl", "r")
		signalYields_resolution = pickle.load(pkl)
		pkl = open("input/inputsCI/"+fileBegin+"signalYieldsSingleBin_ID.pkl", "r")
		signalYields_ID = pickle.load(pkl)
	elif "electron" in channel:
		pkl = open("input/inputsCI/"+fileBegin+"signalYieldsSingleBinEle_default.pkl", "r")
		signalYields_default = pickle.load(pkl)
		pkl = open("input/inputsCI/"+fileBegin+"signalYieldsSingleBinEle_scaleUp.pkl", "r")
		signalYields_scaleUp = pickle.load(pkl)
		pkl = open("input/inputsCI/"+fileBegin+"signalYieldsSingleBinEle_scaleDown.pkl", "r")
		signalYields_scaleDown = pickle.load(pkl)
		pkl = open("input/inputsCI/"+fileBegin+"signalYieldsSingleBinEle_piledown.pkl", "r")
		signalYields_piledown = pickle.load(pkl)
		pkl = open("input/inputsCI/"+fileBegin+"signalYieldsSingleBinEle_pileup.pkl", "r")
		signalYields_pileup = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsSingleBinEle_pdfWeightsUp.pkl"%fileBegin, "r")
		signalYields_pdfWeightsUp = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsSingleBinEle_pdfWeightsDown.pkl"%fileBegin, "r")
		signalYields_pdfWeightsDown = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsSingleBinEle_prefireup.pkl"%fileBegin, "r")
		signalYields_prefireup = pickle.load(pkl)
		pkl = open("input/inputsCI/%ssignalYieldsSingleBinEle_prefiredown.pkl"%fileBegin, "r")
		signalYields_prefiredown = pickle.load(pkl)

	
	inputFileName = "input/inputsCI/inputsCI_%s.root"%(channel)
        inputFile = ROOT.TFile(inputFileName, "OPEN")

	bkgHistDY = inputFile.Get("bkgHistDY_%s"%channel)
	bkgHistDYSmear = inputFile.Get("bkgHistDYSmeared_%s"%channel)
	bkgHistDYScaleDown = inputFile.Get("bkgHistDYScaleDown_%s"%channel)
	bkgHistDYScaleUp = inputFile.Get("bkgHistDYScaleUp_%s"%channel)
	bkgHistDYPUDown = inputFile.Get("bkgHistDYPUDown_%s"%channel)
	bkgHistDYPUUp = inputFile.Get("bkgHistDYPUUp_%s"%channel)
	bkgHistDYID = inputFile.Get("bkgHistDYWeighted_%s"%channel)
	bkgHistDYPrefireDown = inputFile.Get("bkgHistDYPrefireDown_%s"%channel)
	bkgHistDYPrefireUp = inputFile.Get("bkgHistDYPrefireUp_%s"%channel)

	bkgHistOther = inputFile.Get("bkgHistOther_%s"%channel)
	bkgHistOtherSmear = inputFile.Get("bkgHistOtherSmeared_%s"%channel)
	bkgHistOtherScaleDown = inputFile.Get("bkgHistOtherScaleDown_%s"%channel)
	bkgHistOtherScaleUp = inputFile.Get("bkgHistOtherScaleUp_%s"%channel)
	bkgHistOtherPUDown = inputFile.Get("bkgHistOtherPUDown_%s"%channel)
	bkgHistOtherPUUp = inputFile.Get("bkgHistOtherPUUp_%s"%channel)
	bkgHistOtherID = inputFile.Get("bkgHistOtherWeighted_%s"%channel)
	bkgHistOtherPrefireDown = inputFile.Get("bkgHistOtherPrefireDown_%s"%channel)
	bkgHistOtherPrefireUp = inputFile.Get("bkgHistOtherPrefireUp_%s"%channel)

	bkgHistJets = inputFile.Get("bkgHistJets_%s"%channel)

	if "muon" in channel:
		if ADD:
			label = "ADDGravTo2Mu_Lam%d%s_%s"%(L,interference,channel)
		else:
			label = "CITo2Mu_Lam%dTeV%s_%s"%(L,interference,channel)
	elif "electron" in channel:
		if ADD:
			label = "ADDGravTo2E_Lam%d%s_%s"%(L,interference,channel)
		else:
			label = "CITo2E_Lam%dTeV%s_%s"%(L,interference,channel)
	val = signalYields_default[label][mThreshList][0]
	err = signalYields_default[label][mThreshList][1]
	
	valScaleDown = signalYields_scaleDown[label][mThreshList][0]
	if "electron" in channel:
		valScaleUp = signalYields_scaleUp[label][mThreshList][0]
		valPUDown = signalYields_piledown[label][mThreshList][0]
		valPUUp = signalYields_pileup[label][mThreshList][0]
		valPrefireDown = signalYields_prefiredown[label][mThreshList][0]
		valPrefireUp = signalYields_prefireup[label][mThreshList][0]

	if "muon" in channel:
		valID = signalYields_ID[label][mThreshList][0]
		valSmear = signalYields_resolution[label][mThreshList][0]

	result["sig"] = val 
	result["sigStats"] = 1. + err

	if "electron" in channel:
		if (val==0):
			result["sigScale"]=[0.0,0.0]
		else:
			result["sigScale"] = [abs(valScaleDown/val),abs(valScaleUp/val)]
		if (val==0):
			result["sigPU"]=[0.0,0.0]
		else:
			result["sigPU"] = [abs(valPUUp/val),abs(valPUDown/val)]
		if (val==0):
			result["sigPrefire"]=[0.0,0.0]
		else:
			result["sigPrefire"] = [abs(valPrefireUp/val),abs(valPrefireDown/val)]

	if "muon" in channel:
		result["sigScale"] = [abs(valScaleDown/val),1.]
		result["sigID"] = abs(1./(valID/val))
		result["sigRes"] = abs(valSmear/val) 
	result["sigPDF"] = 1.0 #dummy value to be replaced
	
	mThresh = float(mThresh)
	dataHist = inputFile.Get("dataHist_%s"%channel)
	result["data"] = dataHist.Integral(dataHist.FindBin(mThresh),dataHist.GetNbinsX()+1)	

 	err = ROOT.Double(0)	
	val = bkgHistDY.IntegralAndError(bkgHistDY.FindBin(mThresh),bkgHistDY.GetNbinsX()+1,err)
	result["bkgDY"] = val
	result["bkgDYStats"] = 1.+err/val

	if "electron" in channel:
			result["bkgDYScale"] =[ abs(bkgHistDYScaleDown.Integral(bkgHistDYScaleDown.FindBin(mThresh),bkgHistDYScaleDown.GetNbinsX()+1)/result["bkgDY"]) , abs(bkgHistDYScaleUp.Integral(bkgHistDYScaleUp.FindBin(mThresh),bkgHistDYScaleUp.GetNbinsX()+1)/result["bkgDY"])]
			result["bkgDYPU"] =[ abs(bkgHistDYPUUp.Integral(bkgHistDYPUUp.FindBin(mThresh),bkgHistDYPUUp.GetNbinsX()+1)/result["bkgDY"]) , abs(bkgHistDYPUDown.Integral(bkgHistDYPUDown.FindBin(mThresh),bkgHistDYPUDown.GetNbinsX()+1)/result["bkgDY"])]
			result["bkgDYPrefire"] =[ abs(bkgHistDYPrefireUp.Integral(bkgHistDYPrefireUp.FindBin(mThresh),bkgHistDYPrefireUp.GetNbinsX()+1)/result["bkgDY"]) , abs(bkgHistDYPrefireDown.Integral(bkgHistDYPrefireDown.FindBin(mThresh),bkgHistDYPrefireDown.GetNbinsX()+1)/result["bkgDY"])]
	if "muon" in channel:

		result["bkgDYScale"] =[ abs(bkgHistDYScaleDown.Integral(bkgHistDYScaleDown.FindBin(mThresh),bkgHistDYScaleDown.GetNbinsX()+1)/result["bkgDY"]) , 1.]
		if abs(bkgHistDYSmear.Integral(bkgHistDYSmear.FindBin(mThresh),bkgHistDYSmear.GetNbinsX()+1)/result["bkgDY"]) >=1:
			result["bkgDYRes"] = abs(bkgHistDYSmear.Integral(bkgHistDYSmear.FindBin(mThresh),bkgHistDYSmear.GetNbinsX()+1)/result["bkgDY"])
		else:
			result["bkgDYRes"] = 1./abs(bkgHistDYSmear.Integral(bkgHistDYSmear.FindBin(mThresh),bkgHistDYSmear.GetNbinsX()+1)/result["bkgDY"])
		if abs(bkgHistDYID.Integral(bkgHistDYID.FindBin(mThresh),bkgHistDYID.GetNbinsX()+1)/result["bkgDY"]) >=1:
			result["bkgDYID"] = abs(bkgHistDYID.Integral(bkgHistDYID.FindBin(mThresh),bkgHistDYID.GetNbinsX()+1)/result["bkgDY"])
		else:
			result["bkgDYID"] = 1./abs(bkgHistDYID.Integral(bkgHistDYID.FindBin(mThresh),bkgHistDYID.GetNbinsX()+1)/result["bkgDY"])
	result["bkgDYPDF"] = 1.057378696848 # from Markus's results
	val = bkgHistOther.IntegralAndError(bkgHistOther.FindBin(mThresh),bkgHistOther.GetNbinsX()+1,err)
	result["bkgOther"] = val
	if val > 0 and err > 0:
		result["bkgOtherStats"] = 1.+err/val
	else:
		result["bkgOtherStats"] = 1.

	result["bkgOther"] = abs(bkgHistOther.Integral(bkgHistOther.FindBin(mThresh),bkgHistOther.GetNbinsX()+1))
	
	if "electron" in channel:
		if result["bkgOther"] > 0:
			result["bkgOtherScale"] =[ abs(bkgHistOtherScaleDown.Integral(bkgHistOtherScaleDown.FindBin(mThresh),bkgHistOtherScaleDown.GetNbinsX()+1)/result["bkgOther"]) , abs(bkgHistOtherScaleUp.Integral(bkgHistOtherScaleUp.FindBin(mThresh),bkgHistOtherScaleUp.GetNbinsX()+1)/result["bkgOther"])]
			result["bkgOtherPU"] =[ abs(bkgHistOtherPUUp.Integral(bkgHistOtherPUUp.FindBin(mThresh),bkgHistOtherPUUp.GetNbinsX()+1)/result["bkgOther"]) , abs(bkgHistOtherPUDown.Integral(bkgHistOtherPUDown.FindBin(mThresh),bkgHistOtherPUDown.GetNbinsX()+1)/result["bkgOther"])]
			result["bkgOtherPrefire"] =[ abs(bkgHistOtherPrefireUp.Integral(bkgHistOtherPrefireUp.FindBin(mThresh),bkgHistOtherPrefireUp.GetNbinsX()+1)/result["bkgOther"]) , abs(bkgHistOtherPrefireDown.Integral(bkgHistOtherPrefireDown.FindBin(mThresh),bkgHistOtherPrefireDown.GetNbinsX()+1)/result["bkgOther"])]
		else:
			result["bkgOtherScale"] = 1.
			result["bkgOtherPU"] = 1.
			result["bkgOtherPrefire"] = 1.

	else:
		if result["bkgOther"] > 0:
			result["bkgOtherScale"] =[ abs(bkgHistOtherScaleDown.Integral(bkgHistOtherScaleDown.FindBin(mThresh),bkgHistOtherScaleDown.GetNbinsX()+1)/result["bkgOther"])]
			if  abs(bkgHistOtherSmear.Integral(bkgHistOtherSmear.FindBin(mThresh),bkgHistOtherSmear.GetNbinsX()+1)/result["bkgOther"]) >= 1:
				result["bkgOtherRes"] = abs(bkgHistOtherSmear.Integral(bkgHistOtherSmear.FindBin(mThresh),bkgHistOtherSmear.GetNbinsX()+1)/result["bkgOther"])	 
			else:
				result["bkgOtherRes"] = 1./abs(bkgHistOtherSmear.Integral(bkgHistOtherSmear.FindBin(mThresh),bkgHistOtherSmear.GetNbinsX()+1)/result["bkgOther"])

			if abs(bkgHistOtherID.Integral(bkgHistOtherID.FindBin(mThresh),bkgHistOtherID.GetNbinsX()+1)/result["bkgDY"]) >= 1:
				result["bkgOtherID"] = abs(bkgHistOtherID.Integral(bkgHistOtherID.FindBin(mThresh),bkgHistOtherID.GetNbinsX()+1)/result["bkgOther"])
			else:
				result["bkgOtherID"] = 1./abs(bkgHistOtherID.Integral(bkgHistOtherID.FindBin(mThresh),bkgHistOtherID.GetNbinsX()+1)/result["bkgOther"])
		else:
			result["bkgOtherRes"] = 1.
			result["bkgOtherID"] = 1.
			result["bkgOtherScale"] = 1.
 
	result["bkgOtherPDF"] = 1.170675011666 # form Markus's results 

	result["bkgJets"] = bkgHistJets.Integral(bkgHistJets.FindBin(mThresh),bkgHistJets.GetNbinsX()+1)

	#changed real quick by kaushal
	if addSigDY:
		result["sig"]+=result["bkgDY"]	
		result["sig"] = result["sig"]/result["sig"]

        return result
	
