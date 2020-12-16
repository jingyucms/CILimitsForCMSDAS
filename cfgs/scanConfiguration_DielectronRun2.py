
leptons = "elel"
systematics = ["sigEff","bkgUncert","massScale","res","bkgParams","reco"]
correlate = False
#systematics = ["massScale","sigEff"]
masses = [[5,200,1000], [10,1000,2000], [20,2000,5500]]
#masses = [ [20,2300,5500]]
massesExp = [[100,200,600,250,4,250000], [100,600,1000,250,8,250000], [250,1000,2000,100,20,250000], [250,2000,5600,100,20,250000]]
#massesExp = [[250,2750,5600,50,20,500000]]


libraries = ["ZPrimeEleBkgPdf3_cxx.so","PowFunc_cxx.so","RooDCBShape_cxx.so"]

#channels = ["dimuon_BB","dimuon_BEpos","dimuon_BEneg"]
channels = ["dielectron_2016_EBEB","dielectron_2016_EBEE","dielectron_2017_EBEB","dielectron_2017_EBEE","dielectron_2018_EBEB","dielectron_2018_EBEE"]
#channels = ["dielectron_2016_EBEB","dielectron_2016_EBEE"]
numInt = 500000
numToys = 10
exptToys = 500
width = 0.006
submitTo = "Purdue"

binWidth = 10
CB = True
signalInjection = {"mass":750,"width":0.1000,"nEvents":0,"CB":True,"scale":1}
		
