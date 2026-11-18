import os
import glob
import ROOT

def sum_nEventsGenWeighted_pyroot(directory="."):
    total_sum = 0.0
    
    # Search for all .root files in the specified directory
    root_files = glob.glob(os.path.join(directory, "*.root"))
    
    if not root_files:
        print(f"No .root files found in the '{directory}' directory.")
        return

    print(f"Checking {len(root_files)} .root files...\n")

    for file_path in root_files:
        # Open the ROOT file
        f = ROOT.TFile.Open(file_path, "READ")
        
        # Skip if the file is corrupted or cannot be opened
        if not f or f.IsZombie():
            print(f"[{file_path}] Read error: File is corrupted or cannot be opened.")
            continue
            
        # Get the histogram object
        hist = f.Get("nEventsGenWeighted")
        
        if hist:
            # Calculate the sum using the Integral() method of TH1D
            file_sum = hist.Integral()
            total_sum += file_sum
            print(f"[{file_path}] Value: {file_sum}")
        else:
            print(f"[{file_path}] Warning: 'nEventsGenWeighted' key not found.")
            
        f.Close()

    print("-" * 40)
    print(f"Total sum of 'nEventsGenWeighted' across all files: {total_sum}")

if __name__ == "__main__":
    # Suppress unnecessary ROOT console output (e.g., info messages)
    ROOT.gErrorIgnoreLevel = ROOT.kWarning
    
    # Specify the target directory. (Default: current directory ".")
#    target_directory = "/cms/ldap_home/yhoonlee/FCNCforApproval/TopLeptonMVA/FCNC_RemakeNANOAOD/CMSSW_10_2_25/src/RunIISummer20UL16NanoAODAPVv9/reco/NANOAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8.RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1.NANOAODSIM/"
#    target_directory = "/cms/ldap_home/yhoonlee/FCNCforApproval/TopLeptonMVA/FCNC_RemakeNANOAOD/CMSSW_10_2_25/src/RunIISummer20UL16NanoAODAPVv9/reco/NANOAOD/TTToHadronic_TuneCP5_13TeV-powheg-pythia8.RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1.NANOAODSIM/"
#    target_directory = "/cms/ldap_home/yhoonlee/FCNCforApproval/TopLeptonMVA/FCNC_RemakeNANOAOD/CMSSW_10_2_25/src/RunIISummer20UL16NanoAODAPVv9/reco/NANOAOD/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8.RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1.NANOAODSIM/"
    sum_nEventsGenWeighted_pyroot(target_directory)
