#/usr/bin/env python
import os
import sys
import copy
sys.path.append('cfgs/')

import numpy
import math
import ROOT
from ROOT import TCanvas,TGraphAsymmErrors,TFile,TH1D,TH1F,TGraph,TGraphErrors,gStyle,TLegend,TLine,TGraphSmooth,TPaveText,TGraphAsymmErrors,TPaveLabel,gROOT

ROOT.gROOT.SetBatch(True)

def printPlots(canvas,name):
    	canvas.Print('plots/'+name+".png","png")
    	canvas.Print('plots/'+name+".pdf","pdf")
    	canvas.SaveSource('plots/'+name+".C","cxx")
    	canvas.Print('plots/'+name+".root","root")
    	canvas.Print('plots/'+name+".eps","eps")

def createObsGraph(obs):

    	fileObs=open(obs,'r')

    	observedx=[]
    	observedy=[]
    	obsLimits={}
    	for entry in fileObs:
        	massPoint=float(entry.split()[0])
        	limitEntry=float(entry.split()[1])
        	if massPoint not in obsLimits: obsLimits[massPoint]=[]
        	obsLimits[massPoint].append(limitEntry)
    	for massPoint in sorted(obsLimits):
        	observedx.append(massPoint)
        	observedy.append(numpy.mean(obsLimits[massPoint]))
        	if (numpy.std(obsLimits[massPoint])/numpy.mean(obsLimits[massPoint])>0.05):
            		print massPoint," mean: ",numpy.mean(obsLimits[massPoint])," std dev: ",numpy.std(obsLimits[massPoint])," from: ",obsLimits[massPoint]




    	obsX=numpy.array(observedx)
    	obsY=numpy.array(observedy)

    	#if SMOOTH:
       # 	smooth_obs=TGraphSmooth("normal")
       # 	GraphObs_nonSmooth=TGraph(len(obsX),obsX,obsY)
       # 	GraphObs=smooth_obs.SmoothSuper(GraphObs_nonSmooth,"linear",0,0.005)
    #	else:
       	GraphObs=TGraph(len(obsX),obsX,obsY)
    
    	GraphObs.SetLineWidth(3)
	print GraphObs
	return GraphObs

def createExpGraph(exp):

   	fileExp=open(exp,'r')

    	limits={}
    	expectedx=[]
    	expectedy=[]
        for entry in fileExp:
        	massPoint=float(entry.split()[0])
        	limitEntry=float(entry.split()[1])
        	if massPoint not in limits: limits[massPoint]=[]
        	limits[massPoint].append(limitEntry)

    	for massPoint in sorted(limits):
        	limits[massPoint].sort()
        	numLimits=len(limits[massPoint])
        	nrExpts=len(limits[massPoint])
        	medianNr=int(nrExpts*0.5)
        	#get indexes:
    		#fill lists:
        	expectedx.append(massPoint)
        	expectedy.append(limits[massPoint][medianNr])
        
    	expX=numpy.array(expectedx)
    	expY=numpy.array(expectedy)
   	GraphExp=TGraph(len(expX),expX,expY)
    	GraphExp.SetLineWidth(3)
    	GraphExp.SetLineStyle(2)

	return GraphExp

def makeLimitPlot(output,obs,exp,chan,printStats=False):


	obsLimits = {}
	
	for obsFile in obs:
		if 'width' in obsFile:
			width = obsFile.split('width')[-1].split('_')[0]
		else:
			width = '0.006'
		obsLimits[width] = createObsGraph(obsFile)	

        if  SMOOTH:
		for width,obsGraph in obsLimits.iteritems():
                	smooth_obs=TGraphSmooth("normal")
                	GraphObs_nonSmooth=obsGraph
                	obsLimits[width]=copy.deepcopy(smooth_obs.SmoothSuper(GraphObs_nonSmooth,"linear",0,0.005))
                	obsLimits[width].SetLineWidth(3)


	expLimits = {}
	
	for expFile in exp:
		if 'width' in expFile:
			width = expFile.split('width')[-1].split('_')[0]
		else:
			width = '0.006'	
		expLimits[width] = createExpGraph(expFile)	


    	cCL=TCanvas("cCL", "cCL",0,0,800,500)
    	gStyle.SetOptStat(0)

    	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
    	plotPad.Draw()	
    	plotPad.cd()


     	smoother=TGraphSmooth("normal")
    	smoother2=TGraphSmooth("normal")
	   

    
    	zprimeX=[]
    	zprimeY=[]
    	fileZPrime=open('tools/xsec_ssm.txt','r')
    	for entries in fileZPrime:
        	entry=entries.split()
        	zprimeX.append(float(entry[0]))
        	zprimeY.append(float(entry[1])*1.3/1928)
    	zpX=numpy.array(zprimeX)
    	zpY=numpy.array(zprimeY)
    	GraphZPrime=TGraph(481,zpX,zpY)
    	GraphZPrimeSmooth=smoother2.SmoothSuper(GraphZPrime,"linear")
    	GraphZPrimeSmooth.SetLineWidth(3)
    	GraphZPrimeSmooth.SetLineColor(ROOT.kGreen+3)
    	GraphZPrimeSmooth.SetLineStyle(2)

    	zprimePsiX=[]
    	zprimePsiY=[]
    	fileZPrimePsi=open('tools/xsec_psi.txt','r')
    	for entries in fileZPrimePsi:
        	entry=entries.split()
        	zprimePsiX.append(float(entry[0]))
        	zprimePsiY.append(float(entry[1])*1.3/1928)
   	zpPsiX=numpy.array(zprimePsiX)
	zpPsiY=numpy.array(zprimePsiY)
    	GraphZPrimePsi=TGraph(481,zpPsiX,zpPsiY)
    	GraphZPrimePsiSmooth=smoother.SmoothSuper(GraphZPrimePsi,"linear")
   	GraphZPrimePsiSmooth.SetLineWidth(3)
    	GraphZPrimePsiSmooth.SetLineColor(ROOT.kBlue)

#Draw the graphs:
    	plotPad.SetLogy()
	if "Moriond" in output:
    		DummyGraph=TH1F("DummyGraph","",100,200,5500)
    	else:	
		DummyGraph=TH1F("DummyGraph","",100,400,4500)
    	DummyGraph.GetXaxis().SetTitle("M [GeV]")
    	if chan=="mumu":
        	DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowZ'+X#rightarrow#mu#mu+X) / #sigma(pp#rightarrowZ+X#rightarrow#mu#mu+X)")
    	elif chan=="elel":
        	DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowZ'+X#rightarrowee+X) / #sigma(pp#rightarrowZ+X#rightarrowee+X)")
    	elif chan=="elmu":
        	DummyGraph.GetYaxis().SetTitle("#sigma(pp#rightarrowZ'+X#rightarrow#font[12]{ll}+X) / #sigma(pp#rightarrowZ+X#rightarrow#font[12]{ll}+X)")

    	gStyle.SetOptStat(0)
	if "Moriond" in output:
    		DummyGraph.GetXaxis().SetRangeUser(200,5500)
    	else:	
		DummyGraph.GetXaxis().SetRangeUser(400,4500)

    	DummyGraph.SetMinimum(1e-8)
    	DummyGraph.SetMaximum(4e-4)
    	DummyGraph.GetXaxis().SetLabelSize(0.04)
    	DummyGraph.GetXaxis().SetTitleSize(0.045)
   	DummyGraph.GetXaxis().SetTitleOffset(1.)
    	DummyGraph.GetYaxis().SetLabelSize(0.04)
    	DummyGraph.GetYaxis().SetTitleSize(0.045)
    	DummyGraph.GetYaxis().SetTitleOffset(1.)
    	DummyGraph.Draw()

    	plCMS=TPaveLabel(.12,.81,.22,.88,"CMS","NBNDC")
#plCMS.SetTextSize(0.8)
    	plCMS.SetTextAlign(12)
    	plCMS.SetTextFont(62)
    	plCMS.SetFillColor(0)
    	plCMS.SetBorderSize(0)
    
    	plCMS.Draw()

    	plPrelim=TPaveLabel(.12,.76,.25,.82,"Preliminary","NBNDC")
    	plPrelim.SetTextSize(0.6)
    	plPrelim.SetTextAlign(12)
    	plPrelim.SetTextFont(52)
    	plPrelim.SetFillColor(0)
    	plPrelim.SetBorderSize(0)
    	plPrelim.Draw()

    	leg=TLegend(0.430517,0.623051,0.734885,0.878644,"","brNDC")   
#    	leg=TLegend(0.55,0.55,0.87,0.87,"","brNDC")   
    	leg.SetTextSize(0.032)
	colors = {'01':ROOT.kBlue,'03':ROOT.kRed,'05':ROOT.kGreen+3,'10':ROOT.kOrange}
	for width in sorted(obsLimits):
		obsGraph = obsLimits[width]
		if colors.has_key(width):
			obsGraph.SetLineColor(colors[width])
		obsGraph.Draw("lsame")
		if width == '0.006':
			leg.AddEntry(obsGraph,"Observed 95% CL limit width 0.6%","l")
		else:	
			leg.AddEntry(obsGraph,"Observed 95%% CL limit width %d%%"%int(width),"l")

	for width  in sorted(expLimits):
		expGraph = expLimits[width]
		if colors.has_key(width):
			expGraph.SetLineColor(colors[width])
		expGraph.Draw("lsame")
		if width == '0.006':
			leg.AddEntry(expGraph,"Expected 95% CL limit width 0.6%, median","l")
		else:	
			leg.AddEntry(expGraph,"Expected 95%% CL limit width %d%%, median"%(int(width)),"l")

#    	if not SPIN2:
#        	GraphZPrimeSmooth.Draw("lsame")
#        	GraphZPrimePsiSmooth.Draw("lsame")

    	cCL.SetTickx(1)
    	cCL.SetTicky(1)
    	cCL.RedrawAxis()
    	cCL.Update()
    
  	

	

    	leg.SetLineWidth(0)
    	leg.SetLineStyle(0)
    	leg.SetLineColor(0)
    	leg.Draw("hist")
	if "Moriond" in output:
         	if (chan=="mumu"): 
            		plLumi=TPaveLabel(.65,.905,.9,.99,"36.3 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
        	elif (chan=="elel"):
            		plLumi=TPaveLabel(.65,.905,.9,.99,"35.9 fb^{-1} (13 TeV, ee)","NBNDC")
        	elif (chan=="elmu"):
            		plLumi=TPaveLabel(.4,.905,.9,.99,"35.9 fb^{-1} (13 TeV, ee) + 36.3 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
	else:
 	      	if (chan=="mumu"): 
            		plLumi=TPaveLabel(.65,.905,.9,.99,"13.0 fb^{-1} (13 TeV, #mu#mu)","NBNDC")
        	elif (chan=="elel"):
            		plLumi=TPaveLabel(.65,.905,.9,.99,"2.7 fb^{-1} (13 TeV, ee)","NBNDC")
        	elif (chan=="elmu"):
            		plLumi=TPaveLabel(.4,.905,.9,.99,"12.4 fb^{-1} (13 TeV, ee) + 13.0 fb^{-1} (13 TeV, #mu#mu)","NBNDC")


    	plLumi.SetTextSize(0.5)
    	plLumi.SetTextFont(42)
    	plLumi.SetFillColor(0)
    	plLumi.SetBorderSize(0)
    	plLumi.Draw()
    


	


    
    	cCL.Update()
    	printPlots(cCL,output)
    

#### ========= MAIN =======================
SMOOTH=False
SPIN2=False
TWOENERGY=False

if __name__ == "__main__":
    	import argparse
    	parser = argparse.ArgumentParser(usage="makeLimitPlot.py [options] -o OUTPUTFILE --obs CARD1 --exp CARD2",description="Check if all the ascii files have been produced with the right number of iterations",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    	parser.add_argument("--obs",dest="obs", default=[], help='Observed datacards',action='append')
    	parser.add_argument("--exp",dest="exp", default=[], help='Expected datacards',action='append')
    	parser.add_argument("--stats",dest="stats", action="store_true", default=False, help='Print stats')
    	parser.add_argument("--smooth",dest="smooth",action="store_true",default=False, help="Smooth observed values")
    	parser.add_argument("--spin2",dest="spin2",action="store_true",default=False, help="Make Spin2 limits")
    	parser.add_argument("-c","--config",dest="config",default='', help="config name")
    	parser.add_argument("-t","--tag",dest="tag",default='', help="limit tag")
    	parser.add_argument("--ratioLabel",dest="ratioLabel",default='', help="label for ratio")
    	args = parser.parse_args()
    	SMOOTH=args.smooth
    	SPIN2=args.spin2
       
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
	
	outputfile = "limitPlotWidths_%s"%args.config
	if not args.tag == "":
		outputfile += "_"+args.tag        


    	print "Saving histograms in %s" %(outputfile)
    	if (SMOOTH):
        	print "                  "
        	print "Smoothing observed lines..." 
    	print "\n"


	
    	makeLimitPlot(outputfile,args.obs,args.exp,config.leptons,args.stats)
    
