leptons = "mumu"
systematics = ["lumi",'res','massScale',"zPeak","trig","jets","xSecOther","pdf","ID","stats"]
backgrounds = ['DY','Other','Jets']

correlate = False

lambdas = [10,16,22,28,34]
interferences = ["ConLL","ConLR","ConRR"]

binning = [400,500,700,1100,1900,3500]

libraries = []

channels = ["dimuon_BB","dimuon_BE"]
numInt = 1000000
numToys = 6
exptToys = 500
submitTo = "FNAL"

		
