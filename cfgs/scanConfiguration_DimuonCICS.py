leptons = "mumu"
systematics = ["lumi",'res','massScale',"zPeak","trig","jets","xSecOther","pdf","ID","stats"]
backgrounds = ['DY','Other','Jets']

correlate = False

lambdas = [10,16,22,28,34]
interferences = ["ConLR"]

binning = [400,500,700,1100,1900,3500,5000]

libraries = []

channels = ["dimuon_BBCSPos","dimuon_BBCSNeg","dimuon_BECSPos","dimuon_BECSNeg"]
numInt = 100000
numToys = 6
exptToys = 100
submitTo = "FNAL"

		
