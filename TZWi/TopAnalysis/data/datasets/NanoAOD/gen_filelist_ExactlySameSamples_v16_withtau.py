import sys, os, fnmatch

central = {
"MC2017.TTZToLLNuNu": "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
"MC2017.TTZToLL_M-1to10": "TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",

"MC2017.tZq_ll": "tZq_ll_4f",

#"MC2017.ST_tW_top_5f_NoFullyHadronicDecays": "ST_tW_top_5f_NoFullyHadronicDecays",
#"MC2017.ST_tW_antitop_5f_NoFullyHadronicDecays": "ST_tW_antitop_5f_NoFullyHadronicDecays",

"MC2017.WZTo3LNu": "WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8",

"MC2017.ZZ_TuneCP5": "ZZ_TuneCP5_13TeV-pythia8",

"MC2017.WW_TuneCP5": "WW_TuneCP5_13TeV-pythia8",
"MC2017.GluGluToContinToZZTo2e2mu": "GluGluToContinToZZTo2e2mu",
"MC2017.GluGluToContinToZZTo2e2tau": "GluGluToContinToZZTo2e2tau",
"MC2017.GluGluToContinToZZTo2mu2tau": "GluGluToContinToZZTo2mu2tau",
"MC2017.GluGluToContinToZZTo4e": "GluGluToContinToZZTo4e",
"MC2017.GluGluToContinToZZTo4mu": "GluGluToContinToZZTo4mu",
"MC2017.GluGluToContinToZZTo4tau": "GluGluToContinToZZTo4tau",

"MC2017.WWW_4F_TuneCP5": "WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8",
"MC2017.WWZ_4F_TuneCP5": "WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8",
"MC2017.WZZ_TuneCP5": "WZZ_TuneCP5_13TeV-amcatnlo-pythia8",
"MC2017.ZZZ_TuneCP5": "ZZZ_TuneCP5_13TeV-amcatnlo-pythia8",

"MC2017.TTWJetsToLNu": "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
"MC2017.TTWW": "TTWW_TuneCP5_13TeV-madgraph-pythia8",
"MC2017.TTWZ": "TTWZ_TuneCP5_13TeV-madgraph-pythia8",
"MC2017.TTZZ": "TTZZ_TuneCP5_13TeV-madgraph-pythia8",
"MC2017.TTGamma_Dilept": "TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8",
"MC2017.ttHToNonbb": "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",

"MC2017.ZGToLLG_01J": "ZGToLLG_01J_5f",
"MC2017.WGToLNuG_01J": "WGToLNuG_01J_5f",

"MC2017.TWZToLL_thad_Wlept": "TWZToLL_thad_Wlept_5f",
"MC2017.TWZToLL_tlept_Whad": "TWZToLL_tlept_Whad_5f",
"MC2017.TWZToLL_tlept_Wlept": "TWZToLL_tlept_Wlept_5f",

#"MC2017.TTTo2L2Nu": "TTTo2L2Nu",
#"MC2017.TTToHadronic": "TTToHadronic",
#"MC2017.TTToSemiLeptonic": "TTToSemiLeptonic"
}
rareprocess = {
"MC2017.ST_FCNC-TLL_zct": "ST_FCNC-TLL_Tleptonic_kappa_zct",
"MC2017.ST_FCNC-TLL_zut": "ST_FCNC-TLL_Tleptonic_kappa_zut",
"MC2017.TT_FCNC-T2ZJ_zct": "TT_FCNC-T2ZJ_aTleptonic_ZToll_kappa_zct",
"MC2017.TT_FCNC-aT2ZJ_zct": "TT_FCNC-aT2ZJ_Tleptonic_ZToll_kappa_zct",
"MC2017.TT_FCNC-T2ZJ_zut": "TT_FCNC-T2ZJ_aTleptonic_ZToll_kappa_zut",
"MC2017.TT_FCNC-aT2ZJ_zut": "TT_FCNC-aT2ZJ_Tleptonic_ZToll_kappa_zut"
}
data = {
"Run2017.DoubleEG": "DoubleEG",
"Run2017.SingleElectron": "SingleElectron",
"Run2017.DoubleMuon": "DoubleMuon",
"Run2017.SingleMuon": "SingleMuon",
"Run2017.MuonEG": "MuonEG",
"Run2017.Tau": "Tau"
}

Run2017 = {"MC.RunIISummer17.central": central, "MC.RunIISummer17.rareprocess": rareprocess, "RD.Run2017": data}

dir_store = "/cms/ldap_home/yhoonlee/FCNCforApproval/TopLeptonMVA/FCNC_RemakeNANOAOD/CMSSW_10_2_25/src/"
basedir = dir_store + "RunIISummer20UL17NanoAODv9/reco/NANOAOD"

for i in os.listdir(basedir):
    for process in list(Run2017.values()):
        process_key = list(Run2017.keys())[list(Run2017.values()).index(process)]
        if not os.path.exists(process_key):
            os.system("mkdir %s"%process_key)
        for sub_process in list(process.values()):
            sub_process_key = list(process.keys())[list(process.values()).index(sub_process)]
            if sub_process in i:
                if not os.path.exists("%s/%s"%(process_key,sub_process_key)):
                    os.system("mkdir %s/%s"%(process_key,sub_process_key))
                os.system("ls %s/%s/*.root > %s/%s/%s.txt"%(basedir,i,process_key,sub_process_key,i))

for process in list(Run2017.values()):
    process_key = list(Run2017.keys())[list(Run2017.values()).index(process)]
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
