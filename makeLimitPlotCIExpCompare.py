#/usr/bin/env python
import os
import sys
sys.path.append('cfgs/')
from copy import deepcopy
import numpy
import math
import ROOT
from ROOT import TCanvas,TGraphAsymmErrors,TFile,TH1D,TH1F,TGraph,TGraphErrors,gStyle,TLegend,TLine,TGraphSmooth,TPaveText,TGraphAsymmErrors,TPaveLabel,gROOT

ROOT.gROOT.SetBatch(True)

def getXSecCurve(name,kFac):
   	smoother=TGraphSmooth("normal")
    	X=[]
    	Y=[]
    	file=open('tools/xsec_%s.txt'%name,'r')
    	for entries in file:
        	entry=entries.split()
        	X.append(float(entry[0]))
        	Y.append(float(entry[1])*kFac)
   	aX=numpy.array(X)
	aY=numpy.array(Y)
    	Graph=TGraph(len(X),aX,aY)
   	Graph.SetLineWidth(3)
    	Graph.SetLineColor(lineColors[name.split("_")[-1]])
	#GraphSmooth=smoother.SmoothSuper(Graph,"linear")
   	#GraphSmooth.SetLineWidth(3)
    	#GraphSmooth.SetLineColor(lineColors[name.split("_")[-1]])
	
	#if SPIN2:
    #		Graph.SetLineColor(colors[name])
   #		Graph.SetLineWidth(3)
#		return deepcopy(Graph)
#	else:	
	#return deepcopy(GraphSmooth)
	return deepcopy(Graph)
def getXSecs(name,kFac):
   	smoother=TGraphSmooth("normal")
    	
    	Y={}
    	file=open('tools/xsec_%s.txt'%name,'r')
    	for entries in file:
        	entry=entries.split()
        	X = int(float(entry[0]))
        	Y[X] = float(entry[1])*kFac
	return Y


lineColors = {"ConLL":ROOT.kRed,"ConLR":ROOT.kRed,"ConRR":ROOT.kRed,"DesLL":ROOT.kBlue,"DesLR":ROOT.kBlue,"DesRR":ROOT.kBlue}
lineStyles = {"ConLL":1,"ConLR":2,"ConRR":4,"DesLL":1,"DesLR":2,"DesRR":4}
labels = {"ConLL":"constructive left-left","ConLR":"constructive left-right","ConRR":"constructive right-right","DesLL":"destructive left-left","DesLR":"destructive left-right","DesRR":"destructive right-right"}



def printPlots(canvas,name):
    	canvas.Print('plots/'+name+".png","png")
    	canvas.Print('plots/'+name+".pdf","pdf")
    	canvas.SaveSource('plots/'+name+".C","cxx")
    	canvas.Print('plots/'+name+".root","root")
    	canvas.Print('plots/'+name+".eps","eps")



def makeLimitPlot(output,exp,exp2,chan,interference,printStats=False):

    	fileExp=open(exp,'r')
   	fileExp2=open(exp2,'r')

	xSecs = getXSecs("CI_%s"%interference,1.3)
    
    	limits={}
    	expectedx=[]
    	expectedy=[]
    	expected1SigLow=[]
   	expected1SigHigh=[]
    	expected2SigLow=[]
    	expected2SigHigh=[]
    	for entry in fileExp:
        	massPoint=float(entry.split()[0])
        	limitEntry=float(entry.split()[1])*xSecs[int(float(entry.split()[0]))]
        	if massPoint not in limits: limits[massPoint]=[]
        	limits[massPoint].append(limitEntry)

    	if printStats: print "len limits:", len(limits)
    	for massPoint in sorted(limits):
        	limits[massPoint].sort()
        	numLimits=len(limits[massPoint])
        	nrExpts=len(limits[massPoint])
        	medianNr=int(nrExpts*0.5)
        	#get indexes:
        	upper1Sig=int(nrExpts*(1-(1-0.68)*0.5))
        	lower1Sig=int(nrExpts*(1-0.68)*0.5)
        	upper2Sig=int(nrExpts*(1-(1-0.95)*0.5))
        	lower2Sig=int(nrExpts*(1-0.95)*0.5)
        	if printStats: print massPoint,":",limits[massPoint][lower2Sig],limits[massPoint][lower1Sig],limits[massPoint][medianNr],limits[massPoint][upper1Sig],limits[massPoint][upper2Sig]
    		#fill lists:
        	expectedx.append(massPoint)
		print massPoint, limits[massPoint][medianNr]
        	expectedy.append(limits[massPoint][medianNr])
        	expected1SigLow.append(limits[massPoint][lower1Sig])
        	expected1SigHigh.append(limits[massPoint][upper1Sig])
        	expected2SigLow.append(limits[massPoint][lower2Sig])
        	expected2SigHigh.append(limits[massPoint][upper2Sig])
        
    	expX=numpy.array(expectedx)
    	expY=numpy.array(expectedy)


    	limits2={}
    	expectedx2=[]
    	expectedy2=[]
    	expected1SigLow2=[]
   	expected1SigHigh2=[]
    	expected2SigLow2=[]
    	expected2SigHigh2=[]
    	for entry in fileExp2:
        	massPoint=float(entry.split()[0])
        	limitEntry=float(entry.split()[1])*xSecs[int(float(entry.split()[0]))]
        	if massPoint not in limits2: limits2[massPoint]=[]
        	limits2[massPoint].append(limitEntry)

    	if printStats: print "len limits:", len(limits2)
    	for massPoint in sorted(limits2):
        	limits2[massPoint].sort()
        	numLimits=len(limits2[massPoint])
        	nrExpts=len(limits2[massPoint])
        	medianNr=int(nrExpts*0.5)
        	#get indexes:
        	upper1Sig=int(nrExpts*(1-(1-0.68)*0.5))
        	lower1Sig=int(nrExpts*(1-0.68)*0.5)
        	upper2Sig=int(nrExpts*(1-(1-0.95)*0.5))
        	lower2Sig=int(nrExpts*(1-0.95)*0.5)
        	if printStats: print massPoint,":",limits2[massPoint][lower2Sig],limits2[massPoint][lower1Sig],limits2[massPoint][medianNr],limits2[massPoint][upper1Sig],limits2[massPoint][upper2Sig]
    		#fill lists:
        	expectedx2.append(massPoint)
		print massPoint, limits2[massPoint][medianNr]
        	expectedy2.append(limits2[massPoint][medianNr])
        	expected1SigLow2.append(limits2[massPoint][lower1Sig])
        	expected1SigHigh2.append(limits2[massPoint][upper1Sig])
        	expected2SigLow2.append(limits2[massPoint][lower2Sig])
        	expected2SigHigh2.append(limits2[massPoint][upper2Sig])
        
    	expX2=numpy.array(expectedx2)
    	expY2=numpy.array(expectedy2)




    	values2=[]
    	xPointsForValues2=[]
    	values=[]
    	xPointsForValues=[]
    	if printStats: print "length of expectedx: ", len(expectedx)
    	if printStats: print "length of expected1SigLow: ", len(expected1SigLow)
    	if printStats: print "length of expected1SigHigh: ", len(expected1SigHigh)

	#Here is some Voodoo via Sam:
    	for x in range (0,len(expectedx)):
        	values2.append(expected2SigLow[x])
        	xPointsForValues2.append(expectedx[x])
    	for x in range (len(expectedx)-1,0-1,-1):
        	values2.append(expected2SigHigh[x])
        	xPointsForValues2.append(expectedx[x])
    	if printStats: print "length of values2: ", len(values2)

    	for x in range (0,len(expectedx)):
        	values.append(expected1SigLow[x])
        	xPointsForValues.append(expectedx[x])
    	for x in range (len(expectedx)-1,0-1,-1):
        	values.append(expected1SigHigh[x])
        	xPointsForValues.append(expectedx[x])
    	if printStats: print "length of values: ", len(values)

    	exp2Sig=numpy.array(values2)
    	xPoints2=numpy.array(xPointsForValues2)
    	exp1Sig=numpy.array(values)
    	xPoints=numpy.array(xPointsForValues)
    	if printStats: print "xPoints2: ",xPoints2
    	if printStats: print "exp2Sig: ",exp2Sig
    	if printStats: print "xPoints: ",xPoints
    	if printStats: print "exp1Sig: ",exp1Sig
    	GraphErr2Sig=TGraphAsymmErrors(len(xPoints),xPoints2,exp2Sig)
    	GraphErr2Sig.SetFillColor(ROOT.kYellow+1)
    	GraphErr1Sig=TGraphAsymmErrors(len(xPoints),xPoints,exp1Sig)
    	GraphErr1Sig.SetFillColor(ROOT.kGreen)

    	cCL=TCanvas("cCL", "cCL",0,0,800,500)
    	gStyle.SetOptStat(0)

    	plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
    	ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
    	plotPad.Draw()	
    	ratioPad.Draw()	
    	plotPad.cd()


    

    	expX=numpy.array(expectedx)
    	expY=numpy.array(expectedy)
    	GraphExp=TGraph(len(expX),expX,expY)
    	GraphExp.SetLineWidth(3)
    	GraphExp.SetLineStyle(2)
    	GraphExp.SetLineColor(ROOT.kBlue)
    	expX2=numpy.array(expectedx2)
    	expY2=numpy.array(expectedy2)
    	GraphExp2=TGraph(len(expX2),expX2,expY2)
    	GraphExp2.SetLineWidth(3)
    	GraphExp2.SetLineStyle(2)
    	GraphExp2.SetLineColor(ROOT.kRed)


 
	xSecCurves = []
	xSecCurves.append(getXSecCurve("CI_%s"%interference,1.3)) 

	#Draw the graphs:
	plotPad.SetLogy()
	DummyGraph=TH1F("DummyGraph","",100,10,34)
    	DummyGraph.GetXaxis().SetTitle("#Lambda [TeV]")
    	if chan=="mumu":
        	DummyGraph.GetYaxis().SetTitle("95% CL limit on #sigma(pp#rightarrow CI+X#rightarrow#mu#mu +X) [pb]")
    	elif chan=="elel":
        	DummyGraph.GetYaxis().SetTitle("95% CL limit on #sigma(pp#rightarrow CI+X#rightarrowee +X) [pb]")
    	elif chan=="elmu":
        	DummyGraph.GetYaxis().SetTitle("95% CL limit on #sigma(pp#rightarrow CI+X#rightarrowfont[12]{ll}) [pb]")

    	gStyle.SetOptStat(0)
	DummyGraph.GetXaxis().SetRangeUser(10,34)

    	DummyGraph.SetMinimum(1e-3)
    	DummyGraph.SetMaximum(5)
    	DummyGraph.GetXaxis().SetLabelSize(0.04)
    	DummyGraph.GetXaxis().SetTitleSize(0.045)
   	DummyGraph.GetXaxis().SetTitleOffset(1.)
    	DummyGraph.GetYaxis().SetLabelSize(0.04)
    	DummyGraph.GetYaxis().SetTitleSize(0.045)
    	DummyGraph.GetYaxis().SetTitleOffset(1.)
    	DummyGraph.Draw()
        GraphExp.Draw("lp")
        GraphExp2.Draw("lp")
    	for curve in xSecCurves:
        	curve.Draw("lsame")
        	#curve.Draw("ALP")


    	plCMS=TPaveLabel(.12,.81,.22,.88,"CMS","NBNDC")
#plCMS.SetTextSize(0.8)
    	plCMS.SetTextAlign(12)
    	plCMS.SetTextFont(62)
    	plCMS.SetFillColor(0)
    	plCMS.SetFillStyle(0)
    	plCMS.SetBorderSize(0)
    
    	plCMS.Draw()

    	plPrelim=TPaveLabel(.12,.76,.25,.82,"Preliminary","NBNDC")
    	plPrelim.SetTextSize(0.6)
    	plPrelim.SetTextAlign(12)
    	plPrelim.SetTextFont(52)
    	plPrelim.SetFillColor(0)
    	plPrelim.SetFillStyle(0)
    	plPrelim.SetBorderSize(0)
    	plPrelim.Draw()


    	cCL.SetTickx(1)
    	cCL.SetTicky(1)
    	cCL.RedrawAxis()
    	cCL.Update()
    
    	#leg=TLegend(0.65,0.65,0.87,0.87,"","brNDC")   
    	leg=TLegend(0.540517,0.623051,0.834885,0.878644,"","brNDC")   
#    	leg=TLegend(0.55,0.55,0.87,0.87,"","brNDC")   
    	leg.SetTextSize(0.032)
	ratioLabel = "Default / Angular"
	ratioLabels = ratioLabel.split("/")
	leg.AddEntry(GraphExp, "Default Expected 95%% CL limit","l")
    	leg.AddEntry(GraphExp2,"Angular Expected 95%% CL limit","l")
    	
    	leg1=TLegend(0.665517,0.483051,0.834885,0.623051,"","brNDC")
	leg1.SetTextSize(0.032)
	
        leg1.AddEntry(xSecCurves[0],labels[interference],"l")

    	leg.SetLineWidth(0)
    	leg.SetLineStyle(0)
    	leg.SetFillStyle(0)
    	leg.SetLineColor(0)
    	leg.Draw("hist")

    	leg1.SetLineWidth(0)
    	leg1.SetLineStyle(0)
    	leg1.SetFillStyle(0)
    	leg1.SetLineColor(0)
    	leg1.Draw("hist")
        if (chan=="mumu"): 
           	plLumi=TPaveLabel(.65,.905,.9,.99,"36.3 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
        elif (chan=="elel"):
            	plLumi=TPaveLabel(.65,.905,.9,.99,"35.9 fb^{-1} (13 TeV, ee)","NBNDC")
        elif (chan=="elmu"):
            	plLumi=TPaveLabel(.4,.905,.9,.99,"35.9 fb^{-1} (13 TeV, ee) + 36.3 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
    	plLumi.SetTextSize(0.5)
    	plLumi.SetTextFont(42)
    	plLumi.SetFillColor(0)
    	plLumi.SetBorderSize(0)
    	plLumi.Draw()
    

	plotPad.RedrawAxis()
	

    	ratioPad.cd()

    	line = ROOT.TLine(200,1,5500,1)
    	line.SetLineStyle(ROOT.kDashed)

    	ROOT.gStyle.SetTitleSize(0.12, "Y")
    	ROOT.gStyle.SetTitleYOffset(0.35) 
    	ROOT.gStyle.SetNdivisions(000, "Y")
    	ROOT.gStyle.SetNdivisions(408, "Y")
    	ratioPad.DrawFrame(10,0.8,34,1.7, "; ; %s"%ratioLabel)

    	line.Draw("same")

	ratio = []
	ratiox = []
	for index,val in enumerate(expectedy):
		mass = expectedx[index]
		foundIndex = -1
		for index2, mass2 in enumerate(expectedx2):
			if mass == mass2:
				foundIndex = index2

		if foundIndex >= 0:
			ratio.append(val/expectedy2[foundIndex])
			ratiox.append(mass)
	ratioA = numpy.array(ratio)
	ratioX = numpy.array(ratiox)
	ratioGraph = TGraph(len(ratioX),ratioX,ratioA)
	ratioGraph.SetMarkerSize(4)


    	ratioGraph.Draw("sameP")




    
    	cCL.Update()
    	printPlots(cCL,output)
    

#### ========= MAIN =======================
SMOOTH=False
FULL=False
EXPONLY = False
TWOENERGY=False
if __name__ == "__main__":
    	import argparse
    	parser = argparse.ArgumentParser(usage="makeLimitPlot.py [options] -o OUTPUTFILE --obs CARD1 --exp CARD2",description="Check if all the ascii files have been produced with the right number of iterations",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    	parser.add_argument("--exp",dest="exp", default='', help='Expected datacard')
    	parser.add_argument("--exp2",dest="exp2", default='', help='Expected datacard 2')
    	parser.add_argument("--stats",dest="stats", action="store_true", default=False, help='Print stats')
    	parser.add_argument("--smooth",dest="smooth",action="store_true",default=False, help="Smooth observed values")
    	parser.add_argument("--full",dest="full",action="store_true",default=False, help="Draw 2sigma bands")
    	parser.add_argument("--expOnly",dest="expOnly",action="store_true",default=False, help="plot only expected")
    	parser.add_argument("-c","--config",dest="config",default='', help="config name")
    	parser.add_argument("-t","--tag",dest="tag",default='', help="limit tag")
    	parser.add_argument("-t2","--tag2",dest="tag2",default='', help="limit tag2")
    	parser.add_argument("--ratioLabel",dest="ratioLabel",default='', help="label for ratio")
    	args = parser.parse_args()
    	SMOOTH=args.smooth
    	FULL=args.full
        EXPONLY = args.expOnly
	configName = "scanConfiguration_%s"%args.config

        config =  __import__(configName)

    	if ("mumu" in config.leptons):  
        	print "Running Limts for dimuon channel"
    	elif ("elel" in config.leptons):
        	print "Running Limts for dielectron channel"
    	elif ("elmu" in config.leptons):
        	print "Running Limts for Combination of dielectron and dimuon channel"
    	else: 
        	print "ERROR, --chan must be mumu, elel or elmu"
        	exit
	
	outputfile = "limitPlotCI_ExpCompare_%s"%args.config
	if not args.tag == "":
		outputfile += "_"+args.tag        
	exp = "cards/limitCard_%s_Exp"%args.config 
	exp2 = "cards/limitCard_%s_Exp"%args.config 
	if not args.tag == "":
		exp += "_" + args.tag
	if not args.tag2 == "":
		exp2 += "_" + args.tag2
    	print "Saving histograms in %s" %(outputfile)
    	print " - Exp file: %s" %(exp)
    	if (SMOOTH):
        	print "                  "
        	print "Smoothing observed lines..." 
    	print "\n"

	for interference in config.interferences:
		expFile = exp + "_" + interference
		expFile += ".txt"
		expFile2 = exp2 + "_" + interference
		expFile2 += ".txt"


		outName = outputfile+"_"+interference
	    	makeLimitPlot(outName,expFile,expFile2,config.leptons,interference,args.stats)
		
    
