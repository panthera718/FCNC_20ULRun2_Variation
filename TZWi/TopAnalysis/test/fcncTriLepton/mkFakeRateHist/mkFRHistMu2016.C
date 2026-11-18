void mkFRHistMu2016() {
  const Int_t XBINS = 3;
  const Int_t YBINS = 5;
  Double_t xEdges[XBINS + 1] = {0.0, 1.2, 2.1, 2.4};
  Double_t yEdges[YBINS + 1] = {10.0, 15.0, 32.0, 45.0, 60.0, 100.0};
  TH2* h_fakeratesMRmu = new TH2D("fakeratesMRmu", "Fake rates form QCD - muons", XBINS, xEdges, YBINS, yEdges);
  TH2* h_staterr = new TH2D("staterr", "staterr", XBINS, xEdges, YBINS, yEdges);

  Double_t fakerate[3][5] = { {0.196196, 0.0563383, 0.0582372, 0.06527, 0.0646016},
                              {0.161408, 0.0418446, 0.0310639, 0.0354109, 0.0342838},
                              {0.153195, 0.0369929, 0.0261514, 0.0316471, 0.0360789} };

  Double_t fakerateerr[3][5] = { {0.00178105, 0.000605338, 0.00240676, 0.00489598, 0.00250303},
                                 {0.00213548, 0.00061992, 0.00179273, 0.00396781, 0.00183414},
                                 {0.00435142, 0.0009455, 0.00170873, 0.00398312, 0.0034294} };

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
      h_fakeratesMRmu->SetBinContent(xbin, ybin, fakerate[i][j]);
      h_staterr->SetBinContent(xbin, ybin, fakerateerr[i][j]);
    }
  }

  TFile *fakeratemufile = new TFile("2016APVpreVFP_fakerates_MR_mu_LowVersion.root", "recreate");
  h_fakeratesMRmu->Write();
  h_staterr->Write();
  fakeratemufile->Close();
}
