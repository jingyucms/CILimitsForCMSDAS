import argparse
import subprocess
import time
import os
import sys
sys.path.append('cfgs/')
sys.path.append('input/')

def get_git_revision_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'])


def printProgress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '%' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()


##Data card for Zprime -> ll analysis, created on %(date)s at %(time)s using revision %(hash)s of the package

cardTemplate='''
##Data card for CI interpretation of the Zprime -> ll analysis, created on %(date)s at %(time)s
imax 1  number of channels
jmax %(nBkgs)s  number of backgrounds
kmax *  number of nuisance parameters (sources of systematical uncertainties)
------------
# we have just one channel, in which we observe 0 events
bin %(bin)s
observation %(data)s
------------
# now we list the expected events for signal and all backgrounds in that bin
# the second 'process' line must have a positive number for backgrounds, and 0 for signal
# then we list the independent sources of uncertainties, and give their effect (syst. error)
# on each process and bin
%(channels)s  
------------
%(systs)s
'''


def getChannelBlock(backgrounds,inputs,signalScale,chan):
	nBkgs = len(backgrounds)
	result = "bin %s"%chan
	for i in range(0,nBkgs):
		result += " %s "%chan
	result+="\n"
	result += "process      sig"
	for background in backgrounds:
		result+= " %s  "%background
	result +="\n"
	result +="process       0 "
	for i in range(0,nBkgs):
		result+=" %d"%(i+1)
	result +="\n"
	if inputs["sig"] >= 0:
		result += "rate         %.2f "%inputs["sig"]
	else:	
		result += "rate         0.0 "
	#result += "rate         1 "
	for background in backgrounds:
		result+= " %.2f"%inputs["bkg%s"%background]
	return result
 


def getUncert(uncert, value, backgrounds, mass,channel,correlate,yields,signif):
	if uncert == "xSecOther":
		result = "xSecOther lnN - "
	        for background in backgrounds:
			if background == "Other":
        			result += "  %.3f  "%value
			else:
        			result += " - "
		result += "\n"		

	if uncert == "jets":
		result = "jets lnN - "
	        for background in backgrounds:
			if background == "Jets":
        			result += "  %.3f  "%value
			else:
        			result += " - "
		result += "\n"		



	if uncert == "zPeak":
		result = "zPeak lnN %.3f"%value
	        for background in backgrounds:
			if background == "Jets":
        			result += "  -  "
			else:
        			result += "  %.3f"%value
		result += "\n"		



	if uncert == "trig":
		result = "trig lnN %.3f"%value
	        for background in backgrounds:
			if background == "Jets":
        			result += "  -  "
			else:
        			result += "  %.3f"%value
		result += "\n"		

	if uncert == "massScale":
		if correlate:
			name = "scale"
		else:
			name = "scale_%s"%channel
		result = "%s  lnN %.3f"%(name,yields["sigScale"])
	        for background in backgrounds:
			if background == "Jets":
        			result += "  -  "
			else:
        			result += "  %.3f  "%yields["bkg%sScale"%background]
	
		result += "\n"		

	if uncert == "stats":
		if correlate:
			name = "stats"
		else:
			name = "stats_%s"%channel
		result = "%s  lnN %.3f"%(name,yields["sigStats"])
	        for background in backgrounds:
			if background == "Jets":
        			result += "  -  "
       			else:
        			result += "  %.3f  "%yields["bkg%sStats"%background]
	
		result += "\n"		


	if uncert == "res":
		if correlate:
			name = "res"
		else:
			name = "res_%s"%channel
		result = "%s  lnN %.3f"%(name,yields["sigRes"])
	        for background in backgrounds:
			if background == "Jets":
        			result += "  -  "
       			else:
        			result += "  %.3f  "%yields["bkg%sRes"%background]
	
		result += "\n"		

	if uncert == "pdf":
		if correlate:
			name = "pdf"
		else:
			name = "pdf_%s"%channel
		result = "%s  lnN %.3f"%(name,yields["sigPDF"])
	        for background in backgrounds:
			if background == "Jets":
        			result += "  -  "	
        		else:
        			result += "  %.3f  "%yields["bkg%sPDF"%background]
		result += "\n"		
	if uncert == "ID":
		if correlate:
			name = "ID"
		else:
			name = "ID_%s"%channel
		result = "%s  lnN %.3f"%(name,yields["sigID"])
	        for background in backgrounds:
			if background == "Jets":
        			result += "  -  "	
        		else:
        			result += "  %.3f  "%yields["bkg%sID"%background]
		result += "\n"		

	if uncert == "lumi":
		name = "lumi"
		result = "lumi lnN %.3f"%value
	        for background in backgrounds:
			if background == "Jets":
        			result += "  -  "
        		else:	
				result += "  %.3f  "%value
		result += "\n"		



        return result
		
	


def writeCard(card,fileName):

	text_file = open("%s.txt" % (fileName), "w")
	text_file.write(card)
	text_file.close()
	

def main():

	parser = argparse.ArgumentParser(description='Data writer for Zprime -> ll analysis interpretation in combine')
	parser.add_argument("--expected", action="store_true", default=False, help="write datacards for expected limit mass binning")
	parser.add_argument("-i", "--inject", action="store_true", default=False, help="inject signal")
	parser.add_argument("-c", "--chan", dest = "chan", default="", help="name of the channel to use")
	parser.add_argument("-o", "--options", dest = "config", default="", help="name of config file")
	parser.add_argument("-t", "--tag", dest = "tag", default="", help="tag")
	parser.add_argument("-m", "--mass", dest = "mass", default=2000, help="tag")
	parser.add_argument("-s", "--signif", action="store_true", default=False, help="write card for significances")
        parser.add_argument( "--workDir", dest = "workDir", default = "", help="tells batch jobs where to put the datacards. Not for human use!")
				
	args = parser.parse_args()	
	tag = args.tag
	if not args.tag == "":
		tag = "_" + args.tag

        import glob
	from ROOT import gROOT
        for f in glob.glob("userfuncs/*.cxx"):
                gROOT.ProcessLine(".L "+f+"+")


	configName = "scanConfiguration_%s"%args.config
	config =  __import__(configName)

	moduleName = "channelConfig_%s"%args.chan
	module =  __import__(moduleName)

	from createInputs import createSingleBinCI
	from tools import getCardDir
	cardDir = getCardDir(args,config)	
	if not os.path.exists(cardDir):
    		os.makedirs(cardDir)

	lambdas = config.lambdas
	nPoints = len(config.lambdas)*len(config.interferences)
	

	index = 0
	for Lambda in config.lambdas:
		for interference in config.interferences:
			name = "%s/%s_%d_%s" % (cardDir,args.chan, Lambda, interference)
			if args.inject or "toy" in tag:	
				yields = createSingleBinCI(Lambda,interference, name,args.chan,args.config, args.mass ,dataFile=injectedFile)
			else:	
				yields = createSingleBinCI(Lambda,interference, name,args.chan,args.config, args.mass)
		
			backgrounds = config.backgrounds

			nBkg = len(backgrounds) 
	
						

			channelDict = {}

			channelDict["date"] = time.strftime("%d/%m/%Y")
			channelDict["time"] = time.strftime("%H:%M:%S")
			#channelDict["hash"] = get_git_revision_hash()	

			channelDict["bin"] = args.chan

			channelDict["nBkgs"] = nBkg
			scale = False
			res = False
			ID = False
			PDF = False

	
			channelDict["data"] = yields["data"]
		
			channelDict["channels"]	= getChannelBlock(backgrounds,yields,1,args.chan)		
			
			uncertBlock = ""
			uncerts = module.provideUncertaintiesCI(Lambda)
			for uncert in config.systematics:
				uncertBlock += getUncert(uncert,uncerts[uncert],backgrounds,Lambda,args.chan,config.correlate,yields,args.signif)
		
			channelDict["systs"] = uncertBlock

			writeCard(cardTemplate % channelDict, name)
			printProgress(index+1, nPoints, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
			index += 1	
main()
