leptons = "elel"
systematics = ['res','massScale',"zPeak","trig","jets","xSecOther","pdf","stats","PU","prefire"]
#systematics = ["lumi",'res','massScale',"zPeak","trig","jets","xSecOther","pdf","ID","stats","PU"]
#systematics = []
backgrounds = ['DY','Other','Jets']

correlate = True

lambdas = [10,16,22,28,34,40,46,52]
interferences = ["ConLL","ConLR","ConRL","ConRR","DesLL","DesLR","DesRL","DesRR"]
#interferences = ["ConLL","ConLR","ConRR"]

binning = [400,500,700,1100,1900,3500,10000]

libraries = []

channels = ["dielectron_2016_BB","dielectron_2016_BE","dielectron_2017_BB","dielectron_2017_BE","dielectron_2018_BB","dielectron_2018_BE"]
numInt = 100000
numToys = 6
exptToys = 500
submitTo = "FNAL"
LPCUsername = "jschulte"
		
