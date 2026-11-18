import sys, os, fnmatch

central = {
"MC2016.TTZToLLNuNu": "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
"MC2016.TTZToLL_M-1to10": "TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",

"MC2016.tZq_ll": "tZq_ll_4f",

#"MC2016.ST_tW_top_5f_NoFullyHadronicDecays": "ST_tW_top_5f_NoFullyHadronicDecays",
#"MC2016.ST_tW_antitop_5f_NoFullyHadronicDecays": "ST_tW_antitop_5f_NoFullyHadronicDecays",

"MC2016.WZTo3LNu": "WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8",

"MC2016.ZZ_TuneCP5": "ZZ_TuneCP5_13TeV-pythia8",

"MC2016.WW_TuneCP5": "WW_TuneCP5_13TeV-pythia8",
"MC2016.GluGluToContinToZZTo2e2mu": "GluGluToContinToZZTo2e2mu",
"MC2016.GluGluToContinToZZTo2e2tau": "GluGluToContinToZZTo2e2tau",
"MC2016.GluGluToContinToZZTo2mu2tau": "GluGluToContinToZZTo2mu2tau",
"MC2016.GluGluToContinToZZTo4e": "GluGluToContinToZZTo4e",
"MC2016.GluGluToContinToZZTo4mu": "GluGluToContinToZZTo4mu",
"MC2016.GluGluToContinToZZTo4tau": "GluGluToContinToZZTo4tau",

"MC2016.WWW_4F_TuneCP5": "WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8",
"MC2016.WWZ_4F_TuneCP5": "WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8",
"MC2016.WZZ_TuneCP5": "WZZ_TuneCP5_13TeV-amcatnlo-pythia8",
"MC2016.ZZZ_TuneCP5": "ZZZ_TuneCP5_13TeV-amcatnlo-pythia8",

"MC2016.TTWJetsToLNu": "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
"MC2016.TTWW": "TTWW_TuneCP5_13TeV-madgraph-pythia8",
"MC2016.TTWZ": "TTWZ_TuneCP5_13TeV-madgraph-pythia8",
"MC2016.TTZZ": "TTZZ_TuneCP5_13TeV-madgraph-pythia8",
"MC2016.TTGamma_Dilept": "TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8",
"MC2016.ttHToNonbb": "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",

"MC2016.ZGToLLG_01J": "ZGToLLG_01J_5f",
"MC2016.WGToLNuG_01J": "WGToLNuG_01J_5f",

"MC2016.TWZToLL_thad_Wlept": "TWZToLL_thad_Wlept_5f",
"MC2016.TWZToLL_tlept_Whad": "TWZToLL_tlept_Whad_5f",
"MC2016.TWZToLL_tlept_Wlept": "TWZToLL_tlept_Wlept_5f",

#"MC2016.TTTo2L2Nu": "TTTo2L2Nu",
#"MC2016.TTToHadronic": "TTToHadronic",
#"MC2016.TTToSemiLeptonic": "TTToSemiLeptonic"
}
rareprocess = {
"MC2016.ST_FCNC-TLL_zct": "ST_FCNC-TLL_Tleptonic_kappa_zct",
"MC2016.ST_FCNC-TLL_zut": "ST_FCNC-TLL_Tleptonic_kappa_zut",
"MC2016.TT_FCNC-T2ZJ_zct": "TT_FCNC-T2ZJ_aTleptonic_ZToll_kappa_zct",
"MC2016.TT_FCNC-aT2ZJ_zct": "TT_FCNC-aT2ZJ_Tleptonic_ZToll_kappa_zct",
"MC2016.TT_FCNC-T2ZJ_zut": "TT_FCNC-T2ZJ_aTleptonic_ZToll_kappa_zut",
"MC2016.TT_FCNC-aT2ZJ_zut": "TT_FCNC-aT2ZJ_Tleptonic_ZToll_kappa_zut"
}
data = {
"Run2016.DoubleEG": "DoubleEG",
"Run2016.SingleElectron": "SingleElectron",
"Run2016.DoubleMuon": "DoubleMuon",
"Run2016.SingleMuon": "SingleMuon",
"Run2016.MuonEG": "MuonEG",
"Run2016.Tau": "Tau"
}

Run2016 = {"MC.RunIISummer16.central": central, "MC.RunIISummer16.rareprocess": rareprocess, "RD.Run2016": data}

dir_store = "/cms/ldap_home/yhoonlee/FCNCforApproval/TopLeptonMVA/FCNC_RemakeNANOAOD/CMSSW_10_2_25/src/"
basedir = dir_store + "RunIISummer20UL16NanoAODAPVv9/reco/NANOAOD"

for i in os.listdir(basedir):
    for process in list(Run2016.values()):
        process_key = list(Run2016.keys())[list(Run2016.values()).index(process)]
        if not os.path.exists(process_key):
            os.system("mkdir %s"%process_key)
        for sub_process in list(process.values()):
            sub_process_key = list(process.keys())[list(process.values()).index(sub_process)]
            if sub_process in i:
                if not os.path.exists("%s/%s"%(process_key,sub_process_key)):
                    os.system("mkdir %s/%s"%(process_key,sub_process_key))
                os.system("ls %s/%s/*.root > %s/%s/%s.txt"%(basedir,i,process_key,sub_process_key,i))

for process in list(Run2016.values()):
    process_key = list(Run2016.keys())[list(Run2016.values()).index(process)]
    process_key_yaml = process_key + ".yaml"
    f = open(process_key_yaml, "w")
    f.write("dataset:\n")
    for sub_process in list(process.values()):
        sub_process_key = list(process.keys())[list(process.values()).index(sub_process)]
        sub_process_key_str = "    " + sub_process_key + ":\n"
        f.write(sub_process_key_str)
        for i in os.listdir(basedir):
            if sub_process in i:
                filekey = "        /" + i + ":\n"
                filekey_mod = filekey.replace(".","/")
                f.write(filekey_mod)
                filedir = "        - " + basedir + "/" + i + "\n"
                f.write(filedir)
    f.close()
