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


def getChannelBlock(backgrounds,inputs,signalScale,chan,args):
        if args.combineSigDY:
            beginIndex = 1
        else:
            beginIndex = 0
	result = "bin %s_%s"%(chan, args.mass)
	for i in range(beginIndex,len(backgrounds)):
		result += " %s_%s "%(chan,args.mass)
	result+="\n"
	result += "process      sig"
	for i in range(beginIndex, len(backgrounds)):
		result+= " %s  "%backgrounds[i]
	result +="\n"
	result +="process       0 "
	for i in range(beginIndex, len(backgrounds)):
                if args.combineSigDY:
                    result+=" %d"%(i)
                else:
                    result+=" %d"%(i+1)
	result +="\n"
	if inputs["sig"] > 0.01:
		result += "rate         %.2f "%inputs["sig"]
	else:	
		result += "rate         1e-9 "
	#result += "rate         1 "
	for i in range(beginIndex, len(backgrounds)):
                if inputs["bkg%s"%backgrounds[i]] > 0.01:
                    result+= " %.2f"%inputs["bkg%s"%backgrounds[i]]
                else:
                    result+= " 1e-9"
	return result
 
correlations = {
"xSecOther":2,
"jets":2,
"zPeak":1,
"trig":1,
"massScale":0,
"stats":0,
"res":0,
"pdf":2,
"ID":0,
"lumi":2,
"PU":2,
"PdfWeights":2,
"prefire":2
}



def getUncert(uncert, value, backgrounds, mass,channel,correlate,yields,signif,args):
        if args.combineSigDY:
            beginIndex = 1
        else:
            beginIndex = 0
	result = ""
	if correlate:
		if correlations[uncert] == 0:
			name = "%s_%s"%(uncert,channel)
		elif correlations[uncert] == 1:
			if "dimuon" in channel:
				name = "%s_dimuon"%uncert
			else:
				name = "%s_dielectron"%uncert
		elif correlations[uncert] == 2:
			name = uncert	
	else:
		name = "%s_%s"%(uncert,channel)

	if uncert == "xSecOther":
		result = "%s lnN - "%name
	        for i in range(beginIndex,len(backgrounds)):
			if backgrounds[i] == "Other":
        			result += "  %.3f  "%value
			else:
        			result += " - "
		result += "\n"		


	if uncert == "jets":
		result = "%s lnN - "%name
	        for i in range(beginIndex, len(backgrounds)):
			if backgrounds[i] == "Jets":
        			result += "  %.3f  "%value
			else:
        			result += " - "
		result += "\n"		



	if uncert == "zPeak":
		result = "%s lnN -"%name
	        for i in range(beginIndex, len(backgrounds)):
			if backgrounds[i] == "Jets":
        			result += "  -  "
			else:
        			result += "  %.3f"%value
		result += "\n"		



	if uncert == "trig":
		result = "%s lnN %.3f"%(name,value)
	        for i in range(beginIndex, len(backgrounds)):
			if backgrounds[i] == "Jets":
        			result += "  -  "
			else:
        			result += "  %.3f"%value
		result += "\n"		

	if uncert == "massScale":
		if yields["sigScale"][1] > 1.:
			result = "%s  lnN %.3f/%.3f"%(name,yields["sigScale"][0],yields["sigScale"][1])
		else:
			result = "%s  lnN %.3f"%(name,yields["sigScale"][0])
	        for i in range(beginIndex, len(backgrounds)):
			if backgrounds[i] == "Jets":
        			result += "  -  "
			else:
				if "dimuon" in channel: 
					if yields["bkg%sScale"%backgrounds[i]][0] > 1.: 
        					result += "  %.3f  "%(yields["bkg%sScale"%backgrounds[i]][0])
        				else:	
						result += "  %.3f  "%(1./yields["bkg%sScale"%backgrounds[i]][0])
        			else:	
					result += "  %.3f/%.3f  "%(yields["bkg%sScale"%backgrounds[i]][0],yields["bkg%sScale"%backgrounds[i]][1])
	
		result += "\n"		

	if uncert == "stats":
		result = "%s  lnN %.3f"%(name,yields["sigStats"])
	        for i in range(beginIndex, len(backgrounds)):
			if backgrounds[i] == "Jets":
        			result += "  -  "
       			else:
        			result += "  %.3f  "%yields["bkg%sStats"%backgrounds[i]]
	
		result += "\n"		



	if uncert == "pdf":
		result = "%s  lnN %.3f"%(name,yields["sigPDF"])
	        for i in range(beginIndex, len(backgrounds)):
			if backgrounds[i] == "Jets":
        			result += "  -  "	
        		else:
        			result += "  %.3f  "%yields["bkg%sPDF"%backgrounds[i]]
		result += "\n"	

	if uncert == "PU" and "electron" in channel:
		result = "%s  lnN %.3f/%.3f"%(name,yields["sigPU"][0],yields["sigPU"][1])
	        for i in range(beginIndex, len(backgrounds)):
			if backgrounds[i] == "Jets":
        			result += "  -  "	
        		else:
				result += "  %.3f/%.3f  "%(yields["bkg%sPU"%backgrounds[i]][0],yields["bkg%sPU"%backgrounds[i]][1])
		result += "\n"		
	if uncert == "prefire" and "electron" in channel:
		result = "%s  lnN %.3f/%.3f"%(name,yields["sigPrefire"][0],yields["sigPrefire"][1])
	        for i in range(beginIndex, len(backgrounds)):
			if backgrounds[i] == "Jets":
        			result += "  -  "	
        		else:
				result += "  %.3f/%.3f  "%(yields["bkg%sPrefire"%backgrounds[i]][0],yields["bkg%sPrefire"%backgrounds[i]][1])
		result += "\n"		

	if "muon" in channel:
		if uncert == "ID":
			result = "%s  lnN %.3f"%(name,yields["sigID"])
		        for i in range(beginIndex, len(backgrounds)):
				if backgrounds[i] == "Jets":
        				result += "  -  "	
        			else:
        				result += "  %.3f  "%yields["bkg%sID"%backgrounds[i]]
			result += "\n"		
		if uncert == "res":
			result = "%s  lnN %.3f"%(name,yields["sigRes"])
		        for i in range(beginIndex, len(backgrounds)):
				if backgrounds[i] == "Jets":
        				result += "  -  "
       				else:
        				result += "  %.3f  "%yields["bkg%sRes"%backgrounds[i]]
	
			result += "\n"		

	if uncert == "lumi":
		result = "%s lnN %.3f"%(name,value)
	        for i in range(beginIndex, len(backgrounds)):
			if backgrounds[i] == "Jets":
        			result += "  -  "
        		else:	
				result += "  -  "
		result += "\n"			

	if uncert == "pdfWeights":
		result = "%s lnN %.3f"%(name,value)
	        for background in backgrounds:
        		result += "  -  "
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
        parser.add_argument("-L", "--Lambda", dest = "Lambda", default = -1,type=int, help="Lambda values")
	parser.add_argument("-t", "--tag", dest = "tag", default="", help="tag")
	parser.add_argument("-m", "--mass", dest = "mass", default=2000, help="tag")
	parser.add_argument("-s", "--signif", action="store_true", default=False, help="write card for significances")
        parser.add_argument( "--workDir", dest = "workDir", default = "", help="tells batch jobs where to put the datacards. Not for human use!")
        parser.add_argument("--combineSigDY", dest = "combineSigDY", action = "store_true", default = False, help="Combines Signal and DY Histograms")
        parser.add_argument('--ADD', action= "store_true", default = False, help="ADD")
				
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
	Lambdas = config.lambdas
	if args.Lambda > 0:
		Lambdas = [args.Lambda]	

	for Lambda in Lambdas:
		for interference in config.interferences:
                        name = "%s/%s_%d_%s" % (cardDir,args.chan, Lambda, interference)
                        if args.inject or "toy" in tag:	
                            yields = createSingleBinCI(Lambda,interference, name,args.chan,args.config,args.mass,args.combineSigDY,args.ADD,dataFile=injectedFile)
                        else:	
                            yields = createSingleBinCI(Lambda,interference, name,args.chan,args.config,args.mass, args.combineSigDY,args.ADD)

			backgrounds = config.backgrounds

                        if args.combineSigDY:
                            nBkg = len(backgrounds)-1 
                        else:
                            nBkg = len(backgrounds)
						
	
						

			channelDict = {}

			channelDict["date"] = time.strftime("%d/%m/%Y")
			channelDict["time"] = time.strftime("%H:%M:%S")
			#channelDict["hash"] = get_git_revision_hash()	

			channelDict["bin"] = args.chan+"_"+args.mass

			channelDict["nBkgs"] = nBkg
			scale = False
			res = False
			ID = False
			PDF = False

	
			channelDict["data"] = yields["data"]
		
			channelDict["channels"]	= getChannelBlock(backgrounds,yields,1,args.chan,args)		
			
			uncertBlock = ""
			uncerts = module.provideUncertaintiesCI(Lambda)
			for uncert in config.systematics:
				uncertBlock += getUncert(uncert,uncerts[uncert],backgrounds,Lambda,args.chan,config.correlate,yields,args.signif,args)
		
			channelDict["systs"] = uncertBlock

			writeCard(cardTemplate % channelDict, name)
			printProgress(index+1, nPoints, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
			index += 1	
main()
