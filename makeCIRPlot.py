from ROOT import * 
from setTDRStyle import setTDRStyle
import sys
sys.path.append('cfgs/')
import numpy
from copy import deepcopy

lineColors = {"ConLL":kRed,"ConLR":kRed,"ConRR":kRed,"DesLL":kBlue,"DesLR":kBlue,"DesRR":kBlue}
lineStyles = {"ConLL":1,"ConLR":2,"ConRR":4,"DesLL":1,"DesLR":2,"DesRR":4}
def main():

	import argparse
    	parser = argparse.ArgumentParser(usage="makeLimitPlot.py [options] -o OUTPUTFILE --obs CARD1 --exp CARD2",description="Check if all the ascii files have been produced with the right number of iterations",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    	parser.add_argument("--obs",dest="obs", default='', help='Observed datacard')
    	parser.add_argument("--obs2",dest="obs2", default='', help='2nd Observed datacard')
    	parser.add_argument("--exp",dest="exp", default='', help='Expected datacard')
    	parser.add_argument("--expOnly",dest="expOnly",action="store_true",default=False, help="plot only expected")
    	parser.add_argument("-c","--config",dest="config",default='', help="config name")
    	parser.add_argument("-t","--tag",dest="tag",default='', help="limit tag")
    	parser.add_argument("--input",dest="input",default='', help="where is the stuff?")
    	args = parser.parse_args()
	configName = "scanConfiguration_%s"%args.config

        config =  __import__(configName)
	outDir =  "results_" + args.config + "_" +  args.tag
	if args.input is not "":
		outDir = args.input
	canv = TCanvas("c1","c1",800,800)
	plotPad = TPad("plotPad","plotPad",0,0,1,1)
	style = setTDRStyle()
	gStyle.SetTitleYOffset(1.15)
	gStyle.SetOptStat(0)
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()
	plotPad.DrawFrame(8,0,36,10,";#Lambda [TeV]; limit on signal strength")
	
	leg = TLegend(0.52, 0.751, 0.89, 0.92,"","brNDC")
	leg.SetFillColor(10)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)		
		
	graphs = []
		
	lambdas = [10.,16.,22.,28.,34.]
	#interferences = ["ConLL"]
	interferences = ["ConLL","ConLR","ConRR","DesLL","DesLR","DesRR"]
	for index,interference in enumerate(interferences):
		limits = []
		for L in config.lambdas:
			fileName = "%s/higgsCombine%s.%s.mH%d_%s.root"%(outDir,args.config,"MarkovChainMC",L,interference)
                        limitTree = TChain()
                        limitTree.Add(fileName+"/limit")
                        for entry in limitTree:
				limits.append(entry.limit)
		graphs.append( deepcopy(TGraph(len(lambdas),numpy.array(lambdas),numpy.array(limits))))
		graphs[index].SetLineColor(lineColors[interference])
		graphs[index].SetLineStyle(lineStyles[interference])
		leg.AddEntry(graphs[index],interference,"l")			
		graphs[index].Draw("Lsame")	
		graphs[index].SetLineWidth(2)
	
	fConLL = TF1("fConLL","([0]*x^2 + [1]*x^4)",10,34)	
#	graphs[0].Fit("fConLL","R")	

	fConLR = TF1("fConLR"," [0]*x^2 + [1]*x^4",10,34)	
#	graphs[1].Fit("fConLR","R")	
#
	fConRR = TF1("fConRR"," [0]*x^2 + [1]*x^4",10,34)
#	graphs[2].Fit("fConRR","R")	
	fDesLL = TF1("fDesLL"," [0]*x^2 + [1]*x^4",10,22)	
#	graphs[3].Fit("fDesLL","R")	
	fDesRR = TF1("fDesLR"," [0]*x^2 + [1]*x^4",10,34)	
#	graphs[4].Fit("fDesLR","R")	
	fDesRR = TF1("fDesRR"," [0]*x^2 + [1]*x^4",10,34)	
#	graphs[5].Fit("fDesRR","R")	

	leg.Draw()

	latex = TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.03)
	latex.SetNDC(True)
	latexCMS = TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.055)
	latexCMS.SetNDC(True)
	latexCMSExtra = TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(0.03)
	latexCMSExtra.SetNDC(True) 

	chan = config.leptons

	if chan == "elmu":	
		latex.DrawLatex(0.95, 0.96, "35.9 fb^{-1} (13 TeV, ee) + 36.3 fb^{-1} (13 TeV, #mu#mu )")
	elif chan == "elel":
		latex.DrawLatex(0.95, 0.96, "35.9 fb^{-1} (13 TeV, ee)")
	elif chan ==  "mumu":
		latex.DrawLatex(0.95, 0.96, "36.3 fb^{-1} (13 TeV, #mu#mu )")


	cmsExtra = "Preliminary"
	latexCMS.DrawLatex(0.19,0.88,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.81	
	else:
		yLabelPos = 0.84	
	
	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))			
	line = TLine(8,1,36,1)
	line.Draw("same")

	canv.Print("CILimits_%s_%s.pdf"%(args.config,args.tag))	
main()
