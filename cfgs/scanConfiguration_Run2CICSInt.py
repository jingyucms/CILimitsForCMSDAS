leptons = "elmu"
systematics = ['res','massScale',"zPeak","trig","jets","xSecOther","pdf","stats","PU","prefire","PdfWeights","ID"]
#systematics = ["lumi",'res','massScale',"zPeak","trig","jets","xSecOther","pdf","ID","stats","PU"]
#systematics = []
backgrounds = ['DY','Other','Jets']

correlate = True

lambdas = [10,13,16,19,22,25,28,31,34]
interferences = ["DesLL","DesLR","DesRL","DesRR"]
#interferences = ["ConLL","ConLR","ConRR"]

binning = [400,500,700,1100,1900,3500,10000]

libraries = []

channels = ["cspos_dielectron_2016_BB","cspos_dielectron_2016_BE","cspos_dimuon_2016_BB","cspos_dimuon_2016_BE","cspos_dielectron_2017_BB","cspos_dielectron_2017_BE","cspos_dimuon_2017_BB","cspos_dimuon_2017_BE","cspos_dielectron_2018_BB","cspos_dielectron_2018_BE","cspos_dimuon_2018_BB","cspos_dimuon_2018_BE","csneg_dielectron_2016_BB","csneg_dielectron_2016_BE","csneg_dimuon_2016_BB","csneg_dimuon_2016_BE","csneg_dielectron_2017_BB","csneg_dielectron_2017_BE","csneg_dimuon_2017_BB","csneg_dimuon_2017_BE","csneg_dielectron_2018_BB","csneg_dielectron_2018_BE","csneg_dimuon_2018_BB","csneg_dimuon_2018_BE"]
#channels = ["cspos_dimuon_2017_BB"]
numInt = 500000
numToys = 10
exptToys = 1000
submitTo = "FNAL"
LPCUsername = "jschulte"
		
