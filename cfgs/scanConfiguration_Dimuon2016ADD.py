leptons = "mumu"
systematics = ['res','massScale',"zPeak","trig","jets","xSecOther","pdf","ID","stats","PU","PdfWeights","prefire"]
#systematics = ["lumi",'massScale','zPeak',"trig","jets","xSecOther","pdf","stats","PU"]
backgrounds = ['DY','Other','Jets']

correlate = True 

lambdas = [3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 10000]
#lambdas = [4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500]

#interferences = ["ConLL","ConLR","ConRR","DesLL","DesLR","DesRR"]
#interferences = ["ConLL","ConLR","ConRR"]
interferences = [""]

#binning = [400, 700, 1500, 2500, 3500]
binning = [1800, 2200, 2600, 3000, 3200, 10000]
binning2016 = [1800, 2200, 2600, 3000, 3400, 10000]

#libraries = ["ZPrimeMuonBkgPdf2_cxx.so","PowFunc_cxx.so"]

channels = ["dimuon_2016_BB","dimuon_2016_BE"]
numInt = 500000
numToys = 10
exptToys = 2000
submitTo = "FNAL"
LPCUsername = "jschulte"
		
