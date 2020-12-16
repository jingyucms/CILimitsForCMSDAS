leptons = "elmu"
systematics = ['res','massScale',"zPeak","trig","jets","xSecOther","pdf","ID","stats","PU","PdfWeights"]
#systematics = []
backgrounds = ['DY','Other','Jets']

correlate = True

lambdas = [10,16,22,28,34,40,46]
interferences = ["ConLL","ConLR","ConRL","ConRR","DesLL","DesLR","DesRL","DesRR"]
#interferences = ["ConLL","ConLR","ConRR"]

binning = [400,500,700,1100,1900,3500,10000]

libraries = []

channels = ["dielectron_2016_BB","dielectron_2016_BE","dimuon_2016_BB","dimuon_2016_BE"]
numInt = 100000
numToys = 6
exptToys = 500
submitTo = "FNAL"
LPCUsername = "jschulte"
		
