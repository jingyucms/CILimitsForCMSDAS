import sys
import os
sys.path.append('cfgs/')
import argparse
import subprocess

supportedResources = ["Purdue"]


def getRange(mass,DM=False,CI=False):
	if DM:
		if 120 <= mass <= 200:
			return 0.1
		elif 200 <= mass <= 300:
			return 0.1
		elif 300 <= mass <= 400:
			return 0.1
		elif 400 <= mass <= 500:
			return 1
		elif 500 < mass <= 600:
			return 1
		elif 600 < mass <= 700:
			return 5
		elif 700 < mass <= 800:
			return 10
		elif 800 < mass <= 1000:
			return 10
		elif 1000 < mass <= 2000:
			return 20
		else:
			return 40


	elif CI:
		#return 20
		#if 0 <= mass <= 200:
		#	return 5
		if mass == 10:
			return 1
		if mass == 16:
			return 2
		if mass == 22:
			return 3
		if mass == 28:
			return 3
		if mass == 34:
			return 4
	else:
		if 120 <= mass <= 200:
			return 200000
		elif 200 <= mass <= 300:
			return 10000
		elif 300 <= mass <= 400:
			return 5000
		elif 400 <= mass <= 500:
			return 500
		elif 500 < mass <= 600:
			return 200
		elif 600 < mass <= 700:
			return 100
		elif 700 < mass <= 800:
			return 50
		elif 800 < mass <= 1000:
			return 50
		elif 1000 < mass <= 2000:
			return 20
		else:
			return 10


def runLocalLimits(args,config,outDir,cardDir,binned):

	if args.frequentist:
		algo = "HybridNew"
	else:
		algo = "MarkovChainMC"	

	if args.mass > 0 and not args.singlebin:
      		masses = [[5,args.mass,args.mass]]
        elif args.CI:
                masses = config.lambdas
  	else:
                masses = config.masses

	if args.CI:
		if args.Lambda > 0:
			Lambdas = [args.Lambda]
		else:
			Lambdas = config.lambdas
		for Lambda in Lambdas:
			for interference in config.interferences:
				print "calculate limit for Lambda %d and model %s"%(Lambda,interference)
				if len(config.channels) == 1:
					cardName = cardDir + "/" + config.channels[0] + "_%d_%s"%(Lambda,interference) + ".txt"
				else:
					cardName = cardDir + "/" + args.config + "_combined" + "_%d_%s"%(Lambda,interference) + ".txt"
		
				if args.usePhysicsModel:
					cardName = cardName.split(".")[0]+".root"

				numToys = config.numToys
				if args.expected:
					numToys = 1
	
				if not args.frequentist:
					subCommand = ["combine","-M","MarkovChainMC","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%Lambda, "-i", "%d"%config.numInt, "--tries", "%d"%numToys ,  "--prior","flat","--rMax","%d"%getRange(Lambda,args.DM,args.CI)]
				else:
					subCommand = ["combine","-M","HybridNew","--frequentist","--testStat","LHC","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%Lambda,"--rMax","%d"%getRange(Lambda,args.DM,args.CI), "--rMin", "-10"]
				if args.expected: 
					subCommand.append("-t")
					subCommand.append("%d"%config.exptToys)
		
				if args.lower:
					subCommand.append("--saveChain")
		
				subprocess.call(subCommand)

				if args.expected:	
					resultFile = "higgsCombine%s.%s.mH%d.123456.root"%(args.config,algo,Lambda)
				else:
					resultFile = "higgsCombine%s.%s.mH%d.root"%(args.config,algo,Lambda)
				
				subprocess.call(["mv","%s"%resultFile,"%s/higgsCombine%s.%s.mH%d_%s.root"%(outDir,args.config,algo,Lambda,interference)])
	
				if args.lower:
					from tools import convertToLowerLimit
					rName = "r"
					average = True
					if args.usePhysicsModel:
						rName = "Lambda"
					if args.expected:
						average = False
					limits = convertToLowerLimit(outDir+"/"+resultFile,getRange(Lambda,args.DM),rName,average)
					
					outFile = resultFile.split(".root")[0]+".txt"
					thefile = open(outDir+"/"+outFile, 'w')
					for limit in limits:
  						thefile.write("%.2f %.8f\n" % (Lambda,limit))	
	else:
		if args.mass > 0:
      			masses = [[5,args.mass,args.mass]]
  		else:
        	        masses = config.masses

		for mass in masses:
			for interference in config.interferences:
				print "calculate limit for mass %d"%mass
				if len(config.channels) == 1:
					cardName = cardDir + "/" + config.channels[0] + "_%d_%s"%(mass,interference) + ".txt"
				else:
					cardName = cardDir + "/" + args.config + "_combined" + "_%d_%s"%(mass,interference) + ".txt"
		
				if binned:
					cardName = cardName.split(".")[0] + "_binned.txt"
					numToys = config.numToys
				if args.expected:
					numToys = 1
	
				if not args.frequentist:
					subCommand = ["combine","-M","MarkovChainMC","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass, "-i", "%d"%config.numInt, "--tries", "%d"%numToys ,  "--prior","flat","--rMax","%d"%getRange(mass,args.DM,args.CI)]
				else:
					subCommand = ["combine","-M","HybridNew","--frequentist","--testStat","LHC","%s"%cardName, "-n" "%s"%args.config , "-m","%d"%mass,"--rMax","%d"%getRange(mass,args.DM,args.CI), "--rMin", "-10"]
				if args.expected: 
					subCommand.append("-t")
					subCommand.append("%d"%config.exptToys)
		
				if args.lower:
					subCommand.append("--saveChain")
		
				for library in config.libraries:		
					subCommand.append("--LoadLibrary")
					subCommand.append("userfuncs/%s"%library)
				subprocess.call(subCommand)

				if args.expected:	
					resultFile = "higgsCombine%s.%s.mH%d.123456.root"%(args.config,algo,mass)
				else:
					resultFile = "higgsCombine%s.%s.mH%d.root"%(args.config,algo,mass)
				
				subprocess.call(["mv","%s"%resultFile,"%s/higgsCombine%s.%s.mH%d_%s.root"%(outDir,args.config,algo,mass,interference)])

def runLocalSignificance(args,config,outDir,cardDir,binned):

	if args.hybrid or args.frequentist:
		algo = "HybridNew"
	else:
		algo = "ProfileLikelihood"	

	if args.mass > 0:
      		masses = [[5,args.mass,args.mass]]
        else:
                masses = config.masses
	for massRange in masses:
		mass = massRange[1]
		while mass <= massRange[2]:
			print "calculate significance for mass %d"%mass
                        if len(config.channels) == 1:
                                cardName = cardDir + "/" + config.channels[0] + "_%d"%mass + ".txt"
                        else:
                                cardName = cardDir + "/" + args.config + "_combined" + "_%d"%mass + ".txt"
                        if binned:
				cardName = cardName.split(".")[0]+"_binned.txt"
                        if args.frequentist:	
				subCommand = ["combine","-M","HybridNew","%s"%cardName, "-n" "%s"%(args.config) , "-m","%d"%mass, "--signif" , "--pvalue", "--frequentist", "--testStat","LHC","-T","10000"]
                       	elif args.hybrid:
				subCommand = ["combine","-M","HybridNew","%s"%cardName, "-n" "%s"%(args.config) , "-m","%d"%mass, "--signif" , "--pvalue","--testStat","LHC","-T","10000"]
			elif args.plc:	
				subCommand = ["combine","-M","ProfileLikelihood","%s"%cardName, "-n" "%s"%(args.config) , "-m","%d"%mass, "--signif" , "--pvalue", "--usePLC","--rMax","%d"%getRange(mass,args.DM)]
			else:
				subCommand = ["combine","-M","ProfileLikelihood","%s"%cardName, "-n" "%s"%(args.config) , "-m","%d"%mass, "--signif" , "--pvalue","--uncapped","1","--rMax","%d"%getRange(mass,args.DM)]
			for library in config.libraries:
                                subCommand.append("--LoadLibrary")
                                subCommand.append("userfuncs/%s"%library)


			subprocess.call(subCommand)
                        if args.expected:
                                resultFile = "higgsCombine%s.%s.mH%d.123456.root"%(args.config,algo,mass)
                        else:
                                resultFile = "higgsCombine%s.%s.mH%d.root"%(args.config,algo,mass)
                        subprocess.call(["mv","%s"%resultFile,"%s"%outDir])
                        mass += massRange[0]


def submitLimits(args,config,outDir,binned,tag):

	print "Job submission requested"
	if config.submitTo in supportedResources:
		print "%s resources will be used"%config.submitTo
	else:
		print "Computing resource not supported at the moment. Supported resources are:"
		for resource in supportedResources:
			print resource
		sys.exit()	
	if not os.path.exists("logFiles_%s"%args.config):
    		os.makedirs("logFiles_%s"%args.config)

	if not args.inject:
		srcDir = os.getcwd()
		os.chdir(srcDir+"/logFiles_%s"%args.config)
	else:
		srcDir = os.getcwd()
		if not os.path.exists("logFiles_%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"])):
    			os.makedirs("logFiles_%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]))
		os.chdir(srcDir+"/logFiles_%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]))
	
	Libs = ""
	for library in config.libraries:
        	Libs += "%s/userfuncs/%s "%(srcDir,library)

	name = "_"
	if args.inject:
		name += "_%d_%.4f_%d"%(config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]) + tag
	else:
		name += tag
	import time
	timestamp = time.strftime("%Y%m%d") + "_" + time.strftime("%H%M")
	if args.CI:

	        if args.Lambda > 0:
                	Lambdas = [args.Lambda]
      		else:
	                Lambdas = config.lambdas
	       	
		for Lambda in Lambdas:

                        print "submit limit for Lambda %d"%Lambda
			for interference in config.interferences:
                        	if len(config.channels) == 1:
       	                        	cardName = config.channels[0] + "_%d_%s"%(Lambda,interference) + ".txt"
               	        	else:
                       	        	cardName = args.config + "_combined" + "_%d_%s"%(Lambda,interference) + ".txt"
                       		if binned:
					cardName = cardName.split(".")[0] + "_binned.txt"
				if config.submitTo == "Purdue":
					if args.expected:
						numJobs = int(config.exptToys/10)
						for i in range(0,numJobs):
							subCommand = "qsub -l walltime=48:00:00 -q cms-express %s/submission/CILimits_PURDUE.job -F '%s %s %s %s %d %d %d %d %d %s %d %s'"%(srcDir,args.config,name+"_"+interference,srcDir,cardName,config.numInt,i,10,Lambda,getRange(Lambda),timestamp,args.spin2,Libs)
							subprocess.call(subCommand,shell=True)			
					else:
						#for i in range(0,config.numToys):
						subCommand = "qsub -l walltime=48:00:00 -q cms-express %s/submission/CILimits_PURDUE.job -F '%s %s %s %s %d %d %d %d %d %s %d %s'"%(srcDir,args.config,name+"_"+interference,srcDir,cardName,config.numInt,config.numToys,0,Lambda,getRange(Lambda),timestamp,args.spin2,Libs)
						subprocess.call(subCommand,shell=True)	
						import time
						time.sleep(0.1)		


	else:

		if args.mass > 0:
      			masses = [[5,args.mass,args.mass]]
		else:        
			masses = config.masses

        	for massRange in masses:
                	mass = massRange[1]
                	while mass <= massRange[2]:

	                        print "submit limit for mass %d"%mass
	                        if len(config.channels) == 1:
        	                        cardName = config.channels[0] + "_%d"%mass + ".txt"
                	        else:
                        	        cardName = args.config + "_combined" + "_%d"%mass + ".txt"
	                        if binned:
					cardName = cardName.split(".")[0] + "_binned.txt"
				if config.submitTo == "Purdue":
					if args.frequentist:
						if args.expected:
							subCommand = "qsub -l walltime=48:00:00 -q cms-express %s/submission/zPrimeLimitsFreq_PURDUE.job -F '%s %s %s %s %d %d %d %d %d %s %d %s '"%(srcDir,args.config,name,srcDir,cardName,config.numInt,config.numToys,config.exptToys,mass,getRange(mass),timestamp,args.spin2,Libs)
							subprocess.call(subCommand,shell=True)			
						else:
							for i in range(0,config.numToys):
								subCommand = "qsub -l walltime=48:00:00 -q cms-express %s/submission/zPrimeLimitsFreq_PURDUE.job -F '%s %s %s %s %d %d %d %d %d %s %d %s '"%(srcDir,args.config,name,srcDir,cardName,config.numInt,i,0,mass,getRange(mass),timestamp,args.spin2,Libs)
								subprocess.call(subCommand,shell=True)			

					else:
						if args.expected:
							subCommand = "qsub -l walltime=48:00:00 -q cms-express %s/submission/zPrimeLimits_PURDUE.job -F '%s %s %s %s %d %d %d %d %d %s %d %s'"%(srcDir,args.config,name,srcDir,cardName,config.numInt,config.numToys,config.exptToys,mass,getRange(mass),timestamp,args.spin2,Libs)
							subprocess.call(subCommand,shell=True)			
						else:
							#for i in range(0,config.numToys):
							subCommand = "qsub -l walltime=48:00:00 -q cms-express %s/submission/zPrimeLimits_PURDUE.job -F '%s %s %s %s %d %d %d %d %d %s %d  %s'"%(srcDir,args.config,name,srcDir,cardName,config.numInt,config.numToys,0,mass,getRange(mass),timestamp,args.spin2,Libs)
							subprocess.call(subCommand,shell=True)	
							import time
							time.sleep(0.1)		

			
				mass += massRange[0]

def submitPValues(args,config,outDir,binned,tag):

	if "toy" in tag:
		tag = "_"+tag

	print "Job submission requested"
	if config.submitTo in supportedResources:
		print "%s resources will be used"%config.submitTo
	else:
		print "Computing resource not supported at the moment. Supported resources are:"
		for resource in supportedResources:
			print resource
		sys.exit()	
        if args.mass > 0:
                masses = [[5,args.mass,args.mass]]
        else:
                masses = config.masses

	if not os.path.exists("logFiles_%s"%args.config):
    		os.makedirs("logFiles_%s"%args.config)

	if not args.inject:
		srcDir = os.getcwd()
		os.chdir(srcDir+"/logFiles_%s"%args.config)
	else:
		srcDir = os.getcwd()
		if not os.path.exists("logFiles_%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"])):
    			os.makedirs("logFiles_%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]))
		os.chdir(srcDir+"/logFiles_%s_%d_%.4f_%d"%(args.config,config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]))
	
	Libs = ""
	for library in config.libraries:
        	Libs += "%s/userfuncs/%s "%(srcDir,library)

	name = "_"
	if args.inject:
		name += "%d_%.4f_%d"%(config.signalInjection["mass"],config.signalInjection["width"],config.signalInjection["nEvents"]) + tag
	else:
		name += tag
	import time
	timestamp = time.strftime("%Y%m%d") + "_" + time.strftime("%H%M")
        for massRange in masses:
		print "submit p-value for mass range %d - %d GeV in %d GeV steps"%(massRange[1],massRange[2],massRange[0])
		if len(config.channels) == 1:
			cardName = config.channels[0] + "_"
		else:
			cardName = args.config + "_combined" + "_"
		if binned:
			cardName = cardName + "binned.txt"
		if config.submitTo == "Purdue":
			if args.hybrid:
		                mass = massRange[1]
                		while mass <= massRange[2]:
					subCommand = "qsub -l walltime=48:00:00 -q cms-express %s/submission/zPrimePValuesHybrid_PURDUE.job -F '%s %s %s %s %d %s %s'"%(srcDir,args.config,name,srcDir,cardName,mass,timestamp,Libs)
					mass += massRange[0]
					subprocess.call(subCommand,shell=True)			
			elif args.frequentist:	
		                mass = massRange[1]
                		while mass <= massRange[2]:
					subCommand = "qsub -l walltime=48:00:00 -q cms-express %s/submission/zPrimePValuesFreq_PURDUE.job -F '%s %s %s %s %d %s %s'"%(srcDir,args.config,name,srcDir,cardName,mass,timestamp,Libs)
					mass += massRange[0]
					subprocess.call(subCommand,shell=True)			
			elif args.plc:	
				subCommand = "qsub -l walltime=48:00:00 -q cms-express %s/submission/zPrimePValuesPLC_PURDUE.job -F '%s %s %s %s %d %d %d %s %s'"%(srcDir,args.config,name,srcDir,cardName,massRange[1],massRange[2],massRange[0],timestamp,Libs)
				subprocess.call(subCommand,shell=True)			
			else:
				subCommand = "qsub -l walltime=48:00:00 -q cms-express %s/submission/zPrimePValues_PURDUE.job -F '%s %s %s %s %d %d %d %s %s'"%(srcDir,args.config,name,srcDir,cardName,massRange[1],massRange[2],massRange[0],timestamp,Libs)
				subprocess.call(subCommand,shell=True)			
	os.chdir(srcDir)	


def submitLimitsToCrab(args,config,cardDir):

	if args.redo:
		createInputs(args,config,cardDir,CRAB=False)
	masses = config.masses
	if args.expected:
		masses = config.massesExp
	if args.mass > 0:
		if args.expected:
			for massRange in masses:
				if args.mass >= massRange[1] and args.mass < massRange[2]:
					masses = [massRange]
					masses[0][1] = args.mass
					masses[0][2] = args.mass+1
		else:
			masses = [[5,args.mass,args.mass+1]]
	workspaces = []
	i = 0
 	for massRange in masses:
		mass = massRange[1]
		while mass < massRange[2]:
			if len(config.channels) ==1:
				command = ["text2workspace.py","%s/%s_%d.txt"%(cardDir,config.channels[0],mass)]
				workspaces.append("%s/%s_%d.root"%(cardDir,config.channels[0],mass))
				print command
				for library in config.libraries:		
					command.append("--LoadLibrary")
					command.append("userfuncs/%s"%library)
				if args.redo:
					subprocess.call(command)	
				i += 1
				mass += massRange[0]			
			else:
				command = ["text2workspace.py","%s/%s_combined_%d.txt"%(cardDir,args.config,mass)]
				workspaces.append("%s/%s_combined_%d.root"%(cardDir,args.config,mass))
				for library in config.libraries:		
					command.append("--LoadLibrary")
					command.append("userfuncs/%s"%library)
	
				if args.redo:
					subprocess.call(command)	
				i += 1
				mass += massRange[0]			
	libPart = []
	for lib in config.libraries:
		libPart.append("userfuncs/"+lib)
		libPart.append("userfuncs/"+lib.split("_")[0]+".cxx")
		libPart.append("userfuncs/"+lib.split("_")[0]+".h")
		libPart.append("userfuncs/"+lib.split(".")[0]+".d")

	nrJobs = 1

    	script="submitLimitCrabJob.py"

	if args.expected:
 		for massRange in masses:
			mass = massRange[1]
			while mass < massRange[2]:
			
				nJobs = str(massRange[3])
				nToys = str(massRange[4])
				nIter = str(massRange[5])
			 	if len(config.channels) > 1:	
					workspace = "%s/%s_combined_%d.root"%(cardDir,args.config,mass)
				else:	
					workspace = "%s/%s_%d.root"%(cardDir,config.channels[0],mass)
				
				tarCommand = ['tar', '-cvf', 'gridPack.tar',"cfgs/","runInterpretation.py"] + [workspace] + libPart
				subprocess.call(tarCommand)

				mvCmd = ["mv gridPack.tar submission/"]
				subprocess.call(mvCmd,shell=True)

				os.chdir("submission/")

				scriptArgs=["python",script,"--mass",str(mass),"--nIter",nIter,"--nrJobs",nJobs,"--nToys",nToys,"--gridPack","gridPack.tar","--outputTag",args.tag.split("_")[-1],"--crabConfig","crab_base.py","--config",args.config,"--expected","1"]
				print scriptArgs
				result = subprocess.Popen(scriptArgs,stdout=subprocess.PIPE).communicate()[0].splitlines()
				for line in result:
    					print line

				mass += massRange[0]			
				os.chdir('../')
	else:
		nJobs = str(i)
		nToys = str(config.numToys)
		nIter = str(config.numInt)

		tarCommand = ['tar', '-cvf', 'gridPack.tar',"cfgs/","runInterpretation.py"] + workspaces + libPart
		subprocess.call(tarCommand)

		mvCmd = ["mv gridPack.tar submission/"]
		subprocess.call(mvCmd,shell=True)

		os.chdir("submission/")

		scriptArgs=["python",script,"--mass",str(mass),"--nIter",nIter,"--nrJobs",nJobs,"--nToys",nToys,"--gridPack","gridPack.tar","--outputTag",args.tag.split("_")[-1],"--crabConfig","crab_base.py","--config",args.config,"--expected","0"]
    		result = subprocess.Popen(scriptArgs,stdout=subprocess.PIPE).communicate()[0].splitlines()
		for line in result:
			print line




		

	sys.exit(0)	
def createInputs(args,config,cardDir,CRAB=False):
	for channel in config.channels:
		print "writing datacards and workspaces for channel %s ...."%channel
		call = ["python","writeDataCards.py","-c","%s"%channel,"-o","%s"%args.config,"-t","%s"%args.tag]
		if args.mass > 0:
			call.append("-m")
			call.append("%d"%args.mass)
		if args.inject:
			call.append("-i")
		if args.binned:
			call.append("-b")
		if args.DM:
			call.append("--DM")
		if args.expected:
			call.append("--expected")
		if args.signif:
			call.append("-s")
		if args.spin2:
			call.append("--spin2")
		if args.frequentist:
			if not "-s" in call:
				call.append("-s")
		if not args.workDir == '':
			call.append("--workDir")
			call.append(args.workDir)
		subprocess.call(call)

	print "done!"
	tag = args.tag
	if not args.tag == "":
		tag = "_" + args.tag

	if len(config.channels) > 1 or CRAB:
		print "writing combined channel datacards ...."
		if args.mass > 0:
			masses = [[5,args.mass,args.mass]]
		else:
			masses = config.masses
			if args.expected:
				masses = config.massesExp
		for massRange in masses:
			mass = massRange[1]
			while mass <= massRange[2]:
				command = ["combineCards.py"]	
				for channel in config.channels:
					if args.binned:
						command.append( "%s=%s_%d_binned.txt"%(channel,channel,mass))			
					else:	
						command.append( "%s=%s_%d.txt"%(channel,channel,mass))			
				outName = "%s/%s_combined_%d.txt"%(cardDir,args.config,mass)
				if args.binned:
					outName = outName.split(".")[0]+"_binned.txt"
				with open('%s'%outName, "w") as outfile:
					subprocess.call(command, stdout=outfile,cwd=cardDir)

				mass += massRange[0]			
		print "done!"

def createInputsCI(args,config,cardDir):
	for channel in config.channels:
		print "writing datacards and workspaces for channel %s ...."%channel
		if args.singlebin:
			mass = args.mass
			if args.mass == -1:
				mass = 2000
			call = ["python","writeDataCardsCISingleBin.py","-c","%s"%channel,"-o","%s"%args.config,"-t","%s"%args.tag, "-m","%d"%mass]
		else:	
			call = ["python","writeDataCardsCI.py","-c","%s"%channel,"-o","%s"%args.config,"-t","%s"%args.tag]
		if args.expected:
			call.append("--expected")
		if args.signif:
			call.append("-s")
		if args.frequentist:
			if not "-s" in call:
				call.append("-s")
		if not args.workDir == '':
			call.append("--workDir")
			call.append(args.workDir)
		subprocess.call(call)

	print "done!"
	tag = args.tag
	if not args.tag == "":
		tag = "_" + args.tag

	if len(config.channels) > 1:
		print "writing combined channel datacards ...."
		if int(args.Lambda) > 0:
			lambdas = [args.Lambda]
		else:
			lambdas = config.lambdas
			
		for Lambda in lambdas:
			for interference in config.interferences:
				command = ["combineCards.py"]	
				for channel in config.channels:
					command.append( "%s=%s_%d_%s.txt"%(channel,channel,Lambda,interference))			
				outName = "%s/%s_combined_%d_%s.txt"%(cardDir,args.config,Lambda,interference)
				with open('%s'%outName, "w") as outfile:
					subprocess.call(command, stdout=outfile,cwd=cardDir)

			        if args.usePhysicsModel:
					outFile = outName.split(".")[0]+".root"
					command = ["text2workspace.py", outName, "-o", outFile, "-P", "HiggsAnalysis.CombinedLimit.LambdaCI:CIlambda"]
					subprocess.call(command)
		print "done!"




def summarizeConfig(config,args,cardDir):
	print "      "
	print "Z' -> ll statistics tool based on Higgs Combine"
	print "               "
	print "------- Configuration Summary --------"
	if args.signif:
		print "Calculation of significances requested"
	else:
		print "Limit calculation requested"
		if args.expected:
			print "Calculating expected limits with %d toy datasets"%config.exptToys
		else:
			print "Calculating observed limits"
		print "MCMC configuration: iterations %d toys: %d"%(config.numInt,config.numToys)
	channelList = ""
	for channel in config.channels:
		channelList += " %s "%(channel)
	print "Consider channels: %s"%channelList
	systList = "" 
	for syst in config.systematics:
		systList += " %s "%(syst)
	print "Systematic uncertainties: %s"%systList
	if args.mass > 0:
		print "run for single mass point at %d GeV"%args.mass
	
	else:
		print "Mass scan configuration: "
		for massRange in config.masses:
			print "from %d to %d in %d GeV steps"%(massRange[1],massRange[2],massRange[0])
	print "data cards and workspaces are saved in %s"%cardDir	
	print "--------------------------------------"
	print "                                      "

def summarizeConfigCI(config,args,cardDir):
	print "      "
	print "Z' -> ll statistics tool based on Higgs Combine"
	print "               "
	print "------- Configuration Summary --------"
	if args.signif:
		print "Calculation of significances requested"
	else:
		print "Limit calculation requested"
		if args.expected:
			print "Calculating expected limits with %d toy datasets"%config.exptToys
		else:
			print "Calculating observed limits"
		print "MCMC configuration: iterations %d toys: %d"%(config.numInt,config.numToys)
	channelList = ""
	for channel in config.channels:
		channelList += " %s "%(channel)
	print "Consider channels: %s"%channelList
	systList = "" 
	for syst in config.systematics:
		systList += " %s "%(syst)
	print "Systematic uncertainties: %s"%systList
	
	print "Lambda scan configuration: "
	print "from %d to %d"%(config.lambdas[0],config.lambdas[-1])
	print "data cards and workspaces are saved in %s"%cardDir	
	if args.singlebin:
		if args.mass == -1:
			print "Use single bin counting with threshold 2000 GeV"
		else:	
			print "Use single bin counting with threshold %d GeV"%args.mass
	print "--------------------------------------"
	print "                                      "
		
if __name__ == "__main__":

        parser = argparse.ArgumentParser(description='Steering tool for Zprime -> ll analysis interpretation in combine')
        parser.add_argument("-r", "--redo", action="store_true", default=False, help="recreate datacards and workspaces for this configuration")
        parser.add_argument("-w", "--write", action="store_true", default=False, help="create datacards and workspaces for this configuration")
        parser.add_argument("-b", "--binned", action="store_true", default=False, help="use binned dataset")
        parser.add_argument("-s", "--submit", action="store_true", default=False, help="submit jobs to cluster")
        parser.add_argument( "--DM", action="store_true", default=False, help="run limits for DM interpretation")
        parser.add_argument("--signif", action="store_true", default=False, help="run significance instead of limits")
        parser.add_argument("--LEE", action="store_true", default=False, help="run significance on BG only toys to estimate LEE")
        parser.add_argument("--frequentist", action="store_true", default=False, help="use frequentist CLs limits")
        parser.add_argument("--hybrid", action="store_true", default=False, help="use frequenstist-bayesian hybrid methods")
        parser.add_argument("--plc", action="store_true", default=False, help="use PLC for signifcance calculation")
        parser.add_argument("-e", "--expected", action="store_true", default=False, help="expected limits")
        parser.add_argument("-i", "--inject", action="store_true", default=False, help="inject signal")
        parser.add_argument("--crab", action="store_true", default=False, help="submit to crab")
        parser.add_argument("-c", "--config", dest = "config", required=True, help="name of the congiguration to use")
        parser.add_argument("-t", "--tag", dest = "tag", default = "", help="tag to label output")
        parser.add_argument( "--workDir", dest = "workDir", default = "", help="tells batch jobs where to put the datacards. Not for human use!")
        parser.add_argument("-m", "--mass", dest = "mass", default = -1,type=int, help="mass point")
        parser.add_argument("-L", "--Lambda", dest = "Lambda", default = -1,type=int, help="Lambda values")
        parser.add_argument( "--CI", dest = "CI",action="store_true", default = False, help="calculate CI limits")
        parser.add_argument( "--usePhysicsModel", dest = "usePhysicsModel",action="store_true", default = False, help="use PhysicsModel to set limtsi of Lamda ")
        parser.add_argument( "--singlebin", dest = "singlebin",action="store_true", default = False, help="use single bin counting for CI. The mass parameter now designates the lower mass threshold")
        parser.add_argument( "--Lower", dest = "lower",action="store_true", default = False, help="calculate lower limits")
        parser.add_argument( "--spin2", dest = "spin2",action="store_true", default = False, help="calculate limits for spin2 resonances")

        args = parser.parse_args()
	
	if args.LEE:
		args.signif = True
		args.submit = True
        configName = "scanConfiguration_%s"%args.config

        config =  __import__(configName)
	tag = args.tag
	if not args.tag == "":
		args.tag = "_" + args.tag

	from tools import getCardDir, getOutDir
	cardDir = getCardDir(args,config)
		
	if args.CI:	
		summarizeConfigCI(config,args,cardDir)
	else:	
		summarizeConfig(config,args,cardDir)

	if args.crab:
		submitLimitsToCrab(args,config,cardDir)

	if (args.redo or args.write) and not args.LEE and not args.CI:
		createInputs(args,config,cardDir)
	elif (args.redo or args.write) and not args.LEE and args.CI:
		createInputsCI(args,config,cardDir)
	if args.write:
		sys.exit()

	outDir = getOutDir(args,config)
		
        if not os.path.exists(outDir):
                os.makedirs(outDir)
	
	if args.submit:
		if args.signif:
			if not args.LEE:
				submitPValues(args,config,outDir,args.binned,args.tag)
			else:
				for i in range(0,1000):
					args.tag = args.tag+"toy%d"%i
					if args.redo:
						createInputs(args,config,cardDir)
					submitPValues(args,config,outDir,args.binned,args.tag)						
					i += 1						
		else:
			submitLimits(args,config,outDir,args.binned,args.tag)
	else:
		print "no submisson requested - running locally"
		if args.signif:
			runLocalSignificance(args,config,outDir,cardDir,args.binned)
		else:
			runLocalLimits(args,config,outDir,cardDir,args.binned)	

