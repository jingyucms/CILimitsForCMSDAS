leptons = "elel"
systematics = ['res','massScale',"zPeak","trig","jets","xSecOther","pdf","stats","PU","prefire","PdfWeights","ID"]
#systematics = ["lumi",'res','massScale',"zPeak","trig","jets","xSecOther","pdf","ID","stats","PU"]
#systematics = []
backgrounds = ['DY','Other','Jets']

correlate = True

lambdas = [10,16,22,28,34,40,46,52]
interferences = ["ConLL","ConLR","ConRL","ConRR"]
#interferences = ["ConLL","ConLR","ConRR"]

binning = [400,500,700,1100,1900,3500,10000]

libraries = []

channels = ["cspos_dielectron_2016_BB","cspos_dielectron_2016_BE","cspos_dielectron_2017_BB","cspos_dielectron_2017_BE","cspos_dielectron_2018_BB","cspos_dielectron_2018_BE","csneg_dielectron_2016_BB","csneg_dielectron_2016_BE","csneg_dielectron_2017_BB","csneg_dielectron_2017_BE","csneg_dielectron_2018_BB","csneg_dielectron_2018_BE"]
numInt = 500000
numToys = 10
exptToys = 1000
submitTo = "FNAL"
LPCUsername = "jschulte"
		
