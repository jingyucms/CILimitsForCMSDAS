leptons = "elel"
systematics = ['res','massScale',"zPeak","trig","jets","xSecOther","pdf","ID","stats","PU","PdfWeights","prefire"]
backgrounds = ['DY','Other','Jets']

correlate = True

lambdas = [3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 10000]
#lambdas = [4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500]

#interferences = ["ConLL","ConLR","ConRR","DesLL","DesLR","DesRR"]
#interferences = ["ConLL","ConLR","ConRR"]
interferences = [""]

#binning = [400,500,700,1100,1900,3500,10000]
binning = [1800, 2200, 2600, 3000, 3400, 10000]
binning2016 = [1900, 2200, 2600, 3000, 3400, 10000]


channels = ["cspos_dielectron_2016_BB","cspos_dielectron_2016_BE","cspos_dielectron_2017_BB","cspos_dielectron_2017_BE","cspos_dielectron_2018_BB","cspos_dielectron_2018_BE","csneg_dielectron_2016_BB","csneg_dielectron_2016_BE","csneg_dielectron_2017_BB","csneg_dielectron_2017_BE","csneg_dielectron_2018_BB","csneg_dielectron_2018_BE"]

numInt = 500000
numToys = 10
exptToys = 2000
submitTo = "FNAL"
LPCUsername = "jschulte"
		
