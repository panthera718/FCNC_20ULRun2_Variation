import sys, os, fnmatch

central = {
"MC2016.DYJetsToLL_M-10to50": "DYJetsToLL_M-10to50",
"MC2016.DYJetsToLL_M-50": "DYJetsToLL_M-50",
"MC2016.ST_s-channel_4f_leptonDecays": "ST_s-channel_4f_leptonDecays",
"MC2016.ST_tW_top_5f_inclusiveDecays": "ST_tW_top_5f_inclusiveDecays",
"MC2016.ST_tW_antitop_5f_inclusiveDecays": "ST_tW_antitop_5f_inclusiveDecays",
"MC2016.TTToSemiLeptonic": "TTToSemiLeptonic",
"MC2016.TTTo2L2Nu": "TTTo2L2Nu"
}
rareprocess = {
"MC2016.TTWJetsToQQ": "TTWJetsToQQ",
"MC2016.TTZToQQ": "TTZToQQ",
"MC2016.WJetsToLNu": "WJetsToLNu"
}

Run2016 = {"MC.RunIISummer16.central": central, "MC.RunIISummer16.rareprocess": rareprocess}

dir_xrd = "root://cms-xrdr.private.lo:2094//xrd/"
dir_xrootd = "/xrootd"
dir_store = "/store/user/yhoonlee/20ULRun2NanoAODv9_-xvf/"
basedir = dir_xrootd + dir_store + "RunIISummer20UL16NanoAODAPVv9/reco/NANOAOD"

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

path = os.path.dirname(os.path.realpath(__file__))
find_str = dir_xrootd
replace_str = dir_xrd
filePattern = "*.txt"

for path, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
    for filename in fnmatch.filter(files, filePattern):
        filepath = os.path.join(path, filename)
        with open(filepath) as f:
            s = f.read()
        if s.find(find_str) != -1:
            s = s.replace(find_str, replace_str)
            with open(filepath, 'w') as f:
                f.write(s)

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
