void mkFRHistEl2016() {
  const Int_t XBINS = 3;
  const Int_t YBINS = 5;
  Double_t xEdges[XBINS + 1] = {0.0, 0.8, 1.48, 2.5};
  Double_t yEdges[YBINS + 1] = {10.0, 15.0, 25.0, 45.0, 60.0, 100.0};
  TH2* h_fakeratesMRele = new TH2D("fakeratesMRele", "Fake rates form QCD - electrons", XBINS, xEdges, YBINS, yEdges);
  TH2* h_staterr = new TH2D("staterr", "staterr", XBINS, xEdges, YBINS, yEdges);

  Double_t fakerate[3][5] = { {0.900533, 0.70539, 0.584609, 0.541874, 0.488086},
                              {0.874624, 0.6779, 0.510465, 0.413573, 0.446702},
                              {0.728995, 0.535154, 0.321767, 0.242839, 0.219501} };

  Double_t fakerateerr[3][5] = { {0.0137195, 0.0218346, 0.0276053, 0.0457201, 0.0298636},
                                 {0.0191756, 0.0243932, 0.0244496, 0.0348721, 0.0275402},
                                 {0.0260039, 0.0205134, 0.0120131, 0.0139127, 0.00791445} };

  for (Int_t i=0; i<3; ++i) {
    for (Int_t j=0; j<5; ++j) {
      std::cout<<fakerate[i][j];
      if (j<4) { std::cout<<", "; }
    }
  std::cout<<std::endl;
  }

  for (Int_t i=0; i<3; ++i) {
    for (Int_t j=0; j<5; ++j) {
      std::cout<<fakerateerr[i][j];
      if (j<4) { std::cout<<", "; }
    }
  std::cout<<std::endl;
  }

  for (Int_t i=0; i<3; ++i) {
    for (Int_t j=0; j<5; ++j) {
      Int_t xbin = i+1;
      Int_t ybin = j+1;
      h_fakeratesMRele->SetBinContent(xbin, ybin, fakerate[i][j]);
      h_staterr->SetBinContent(xbin, ybin, fakerateerr[i][j]);
    }
  }

  TFile *fakerateelefile = new TFile("2016APVpreVFP_fakerates_MR_ele_LowVersion.root", "recreate");
  h_fakeratesMRele->Write();
  h_staterr->Write();
  fakerateelefile->Close();
}
