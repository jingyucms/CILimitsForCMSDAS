leptons = "mumu"
systematics = ["sigEff","bkgUncert","massScale",'res',"bkgParams","reco"]
correlate = False
masses = [[5,200,1000], [10,1000,2000], [20,2000,5500]]
#masses = [[5,375,620]]
massesExp = [[100,200,600,250,4,500000], [100,600,1000,250,8,500000], [250,1000,2000,100,20,50000], [250,2000,5600,100,20,500000]]
#massesExp = [[100,700,1000,250,8,500000], [250,1000,2300,100,20,50000]]


libraries = ["ZPrimeMuonBkgPdf2_cxx.so","PowFunc_cxx.so",'RooCruijff_cxx.so',"RooDCBShape_cxx.so"]

channels = ["dimuon_Moriond2017_BB","dimuon_Moriond2017_BE","dimuon_2017_BB","dimuon_2017_BE","dimuon_2018_BB","dimuon_2018_BE"]

numInt = 500000
numToys = 10
exptToys = 250
width = 0.006
submitTo = "Purdue"

binWidth = 10
CB = True
signalInjection = {"mass":2000,"width":0.006,"nEvents":10,"CB":True}
		
