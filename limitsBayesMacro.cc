///centralLimit.cc
#include "RooConstVar.h"
#include "RooWorkspace.h"
#include "RooCategory.h"
#include "RooStats/ModelConfig.h"
#include "RooStats/FrequentistCalculator.h"
#include "RooStats/HybridCalculator.h"
#include "RooStats/HypoTestInverter.h"
#include "RooStats/ProfileLikelihoodTestStat.h"
#include "RooStats/RatioOfProfiledLikelihoodsTestStat.h"
#include "RooStats/SimpleLikelihoodRatioTestStat.h"
#include "RooStats/MCMCInterval.h"
#include "RooStats/MCMCCalculator.h"
using namespace std;

using namespace RooFit;
using namespace RooStats;




void limitsBayesMacro()
{
   
      //Simple Poisson cut & count using RooStats
      
      
      //First create the model, very similar to what we have done in RooFit last week
      
      int nobs = 13;   // number of observed events
      double b = 10; // number of background events
      double sigmab = 0.2;   // relative uncertainty in b

      RooWorkspace *w = new RooWorkspace("w");

      // make Poisson model * Gaussian constraint
      w->factory("sum:nexp(s[3,0,15],b[1,0,10])");
      // Poisson of (n | s+b)
      w->factory("Poisson:pdf(nobs[0,50],nexp)");
      w->factory("Gaussian:constraint(b0[0,10],b,sigmab[1])");
      w->factory("PROD:model(pdf,constraint)");   
      
      RooRealVar * obs = w->var("nobs");
      w->var("b0")->setVal(b);
      w->var("b0")->setConstant(true); // needed for being treated as global observables
      w->var("sigmab")->setVal(sigmab*b);  

      // use this to avoid too large ranges 
      w->var("b")->setMax(b+5*b*sigmab);
      //~ w->var("s")->setMax(b+5*b*sigmab);
      
      //set value of observed events
      obs->setVal(nobs);         
      

      // make data set with the namber of observed events
      RooDataSet * data = new RooDataSet("data","", *obs );
      data->add(*obs );
      w->import(*data);

      ModelConfig * sbModel = new ModelConfig("sbModel",w);
      sbModel->SetPdf(*w->pdf("model"));
      sbModel->SetParametersOfInterest(*w->var("s"));
      sbModel->SetObservables(*w->var("nobs"));
      sbModel->SetNuisanceParameters(*w->var("b"));

      // these are needed for the hypothesis tests
      sbModel->SetSnapshot(*w->var("s"));
      sbModel->SetGlobalObservables(*w->var("b0"));

      sbModel->Print();
   
      
      
      RooRealVar* poi = (RooRealVar*) sbModel->GetParametersOfInterest()->first();
      ModelConfig * bModel = (ModelConfig*) sbModel->Clone("bModel");
      double oldval = poi->getVal();
      poi->setVal(0);
      bModel->SetSnapshot( *poi  );
      poi->setVal(oldval);   
           
     MCMCCalculator mc(*data, *sbModel);
     mc.SetNumIters(200000); // steps to propose in the chain
     mc.SetTestSize(.05); // 95% CL
     mc.SetNumBurnInSteps(400); // ignore first N steps in chain as "burn in"
     mc.SetLeftSideTailFraction(0.5);  // find a "central" interval
     MCMCInterval* r = (MCMCInterval*)mc.GetInterval();
     

      
      
      double upperLimit = r->UpperLimit(*w->var("s"));
      double ulError = 0;
      std::cout << "The computed upper limit is: " << upperLimit << " +/- " << ulError << std::endl;

     TCanvas * c1 = new TCanvas("IntervalPlot");
     MCMCIntervalPlot plot(*r);
     plot.Draw();  
     c1->Print("post.pdf");     
   
}
