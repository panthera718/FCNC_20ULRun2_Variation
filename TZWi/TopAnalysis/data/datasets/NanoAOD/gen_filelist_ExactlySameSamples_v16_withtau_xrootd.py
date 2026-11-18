import sys, os, fnmatch

central = {
"MC2018.TTZToLLNuNu": "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
"MC2018.TTZToLL_M-1to10": "TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",

"MC2018.tZq_ll": "tZq_ll_4f",

#"MC2018.ST_tW_top_5f_NoFullyHadronicDecays": "ST_tW_top_5f_NoFullyHadronicDecays",
#"MC2018.ST_tW_antitop_5f_NoFullyHadronicDecays": "ST_tW_antitop_5f_NoFullyHadronicDecays",

"MC2018.WZTo3LNu": "WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8",

"MC2018.ZZ_TuneCP5": "ZZ_TuneCP5_13TeV-pythia8",

"MC2018.WW_TuneCP5": "WW_TuneCP5_13TeV-pythia8",
"MC2018.GluGluToContinToZZTo2e2mu": "GluGluToContinToZZTo2e2mu",
"MC2018.GluGluToContinToZZTo2e2tau": "GluGluToContinToZZTo2e2tau",
"MC2018.GluGluToContinToZZTo2mu2tau": "GluGluToContinToZZTo2mu2tau",
"MC2018.GluGluToContinToZZTo4e": "GluGluToContinToZZTo4e",
"MC2018.GluGluToContinToZZTo4mu": "GluGluToContinToZZTo4mu",
"MC2018.GluGluToContinToZZTo4tau": "GluGluToContinToZZTo4tau",

"MC2018.WWW_4F_TuneCP5": "WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8",
"MC2018.WWZ_4F_TuneCP5": "WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8",
"MC2018.WZZ_TuneCP5": "WZZ_TuneCP5_13TeV-amcatnlo-pythia8",
"MC2018.ZZZ_TuneCP5": "ZZZ_TuneCP5_13TeV-amcatnlo-pythia8",

"MC2018.TTWJetsToLNu": "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
"MC2018.TTWW": "TTWW_TuneCP5_13TeV-madgraph-pythia8",
"MC2018.TTWZ": "TTWZ_TuneCP5_13TeV-madgraph-pythia8",
"MC2018.TTZZ": "TTZZ_TuneCP5_13TeV-madgraph-pythia8",
"MC2018.TTGamma_Dilept": "TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8",
"MC2018.ttHToNonbb": "ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8",

"MC2018.ZGToLLG_01J": "ZGToLLG_01J_5f",
"MC2018.WGToLNuG_01J": "WGToLNuG_01J_5f",

"MC2018.TWZToLL_thad_Wlept": "TWZToLL_thad_Wlept_5f",
"MC2018.TWZToLL_tlept_Whad": "TWZToLL_tlept_Whad_5f",
"MC2018.TWZToLL_tlept_Wlept": "TWZToLL_tlept_Wlept_5f",

"MC2018.TTTo2L2Nu": "TTTo2L2Nu",
"MC2018.TTToHadronic": "TTToHadronic",
"MC2018.TTToSemiLeptonic": "TTToSemiLeptonic"
}
rareprocess = {
"MC2018.ST_FCNC-TLL_zct": "ST_FCNC-TLL_Tleptonic_kappa_zct",
"MC2018.ST_FCNC-TLL_zut": "ST_FCNC-TLL_Tleptonic_kappa_zut",
"MC2018.TT_FCNC-T2ZJ_zct": "TT_FCNC-T2ZJ_aTleptonic_ZToll_kappa_zct",
"MC2018.TT_FCNC-aT2ZJ_zct": "TT_FCNC-aT2ZJ_Tleptonic_ZToll_kappa_zct",
"MC2018.TT_FCNC-T2ZJ_zut": "TT_FCNC-T2ZJ_aTleptonic_ZToll_kappa_zut",
"MC2018.TT_FCNC-aT2ZJ_zut": "TT_FCNC-aT2ZJ_Tleptonic_ZToll_kappa_zut"
}
data = {
"Run2018.EGamma": "EGamma",
"Run2018.DoubleMuon": "DoubleMuon",
"Run2018.SingleMuon": "SingleMuon",
"Run2018.MuonEG": "MuonEG",
"Run2018.Tau": "Tau"
}

Run2018 = {"MC.RunIISummer18.central": central, "MC.RunIISummer18.rareprocess": rareprocess, "RD.Run2018": data}

dir_store = "/xrootd/store/user/yhoonlee/20ULRun2NanoAODv9_2026Apr_-xvf/"
basedir = dir_store + "RunIISummer20UL18NanoAODv9/reco/NANOAOD"

for i in os.listdir(basedir):
    for process in list(Run2018.values()):
        process_key = list(Run2018.keys())[list(Run2018.values()).index(process)]
        if not os.path.exists(process_key):
            os.system("mkdir %s"%process_key)
        for sub_process in list(process.values()):
            sub_process_key = list(process.keys())[list(process.values()).index(sub_process)]
            if sub_process in i:
                if not os.path.exists("%s/%s"%(process_key,sub_process_key)):
                    os.system("mkdir %s/%s"%(process_key,sub_process_key))
                #os.system("ls %s/%s/*.root > %s/%s/%s.txt"%(basedir,i,process_key,sub_process_key,i))
                #os.system("ls %s/%s/*.root | sed 's|^/xrootd|root://cms-xrdr.private.lo:2094//xrd/|' > %s/%s/%s.txt" % (basedir, i, process_key, sub_process_key, i))
                os.system("ls %s/%s/*.root | sed 's|^/xrootd|root://cms-xrdr.sdfarm.kr:2094//xrd/|' > %s/%s/%s.txt" % (basedir, i, process_key, sub_process_key, i))

for process in list(Run2018.values()):
    process_key = list(Run2018.keys())[list(Run2018.values()).index(process)]
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
                
                # Create the full original path
                original_path = basedir + "/" + i
                
                # Replace /xrootd with the correct redirector URL
                modified_path = original_path.replace("/xrootd", "root://cms-xrdr.private.lo:2094//xrd/")
                
                filedir = "        - " + modified_path + "\n"
                f.write(filedir)
    f.close()
