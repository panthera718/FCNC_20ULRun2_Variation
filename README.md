# FCNC UL Run 2 variations

Required release: CMSSW_13_3_3.

Eras: 20UL16APV, 20UL16, 20UL17, 20UL18.
Variations: central, jerDown, jerUp, jetVar01.

From an empty CMSSW_13_3_3/src directory, run:

    git clone -b 20UL18_jetVar01 --single-branch https://github.com/panthera718/FCNC_20ULRun2_Variation.git .

## Produce the nominal and systematic-variation ntuples

This stage takes the ntuples produced by [FCNC_withtau_20ULRun2_RemakeNANOAOD](https://github.com/panthera718/FCNC_withtau_20ULRun2_RemakeNANOAOD) as input. Those ntuples already contain the TopLeptonMVA scores.

The instructions below use 2018 as an example. For nominal production, use `20UL18_central` in the clone command above. The `20UL18_jetVar01` branch shown in that command is used later for the jet energy scale variations. Follow the same workflow with the corresponding branches for the other eras.

After cloning, `TZWi/` should be directly under `CMSSW_13_3_3/src/`. From that `src/` directory, build the code:

```bash
cmsenv
scram b -j 4
```

### 1. Prepare the input file lists

Place the `ntuple_2018` directory from the RemakeNANOAOD step in a location accessible to the batch jobs. For this analysis, the files were stored under `/xrootd/store/user/...` on `cms-ui`.

Use [`gen_filelist_ExactlySameSamples_v16_withtau_xrootd.py`](https://github.com/panthera718/FCNC_20ULRun2_Variation/blob/20UL18_central/TZWi/TopAnalysis/data/datasets/NanoAOD/gen_filelist_ExactlySameSamples_v16_withtau_xrootd.py) to generate the dataset file lists. From `TZWi/TopAnalysis/data/datasets/NanoAOD/`, move aside or remove the existing `2018/` directory, then create a fresh one and copy the generator into it:

```bash
cd "$CMSSW_BASE/src/TZWi/TopAnalysis/data/datasets/NanoAOD"
mkdir 2018
cd 2018
cp ../gen_filelist_ExactlySameSamples_v16_withtau_xrootd.py .
```

Edit `dir_store` and `basedir` in the copied script so that `basedir` points to the directory containing the input datasets, for example `ntuple_2018/reco/NANOAOD/`. Then run:

```bash
python3 gen_filelist_ExactlySameSamples_v16_withtau_xrootd.py
```

The resulting dataset definitions and file lists are written under `TZWi/TopAnalysis/data/datasets/NanoAOD/2018/`.

Before submitting jobs, check which datasets are assigned to each process in [`grouping.yaml`](https://github.com/panthera718/FCNC_20ULRun2_Variation/blob/20UL18_central/TZWi/TopAnalysis/test/fcncTriLepton/config/grouping.yaml). Check the cross sections and normalization entries in [`crosssection.yaml`](https://github.com/panthera718/FCNC_20ULRun2_Variation/blob/20UL18_central/TZWi/TopAnalysis/test/fcncTriLepton/config/crosssection.yaml) against the sum of `nEventsGenWeighted` over the input ROOT files for each MC dataset.

### 2. Produce the nominal ntuples

The modules and their execution order are defined in [`01_prod_ntuple.sh`](https://github.com/panthera718/FCNC_20ULRun2_Variation/blob/20UL18_central/TZWi/TopAnalysis/test/fcncTriLepton/01_prod_ntuple.sh). From `TZWi/TopAnalysis/test/fcncTriLepton/`, run [`01.1_submit.py`](https://github.com/panthera718/FCNC_20ULRun2_Variation/blob/20UL18_central/TZWi/TopAnalysis/test/fcncTriLepton/01.1_submit.py) to submit the batch jobs:

```bash
cd "$CMSSW_BASE/src/TZWi/TopAnalysis/test/fcncTriLepton"
./01.1_submit.py
```

Once the batch jobs have finished, run [`01.2_checkFailed_2018.sh`](https://github.com/panthera718/FCNC_20ULRun2_Variation/blob/20UL18_central/TZWi/TopAnalysis/test/fcncTriLepton/01.2_checkFailed_2018.sh) from the same directory to check for reported failures:

```bash
./01.2_checkFailed_2018.sh
```

Enter `submit_2018/` and run [`makentuple2018`](https://github.com/panthera718/FCNC_20ULRun2_Variation/blob/20UL18_central/TZWi/TopAnalysis/scripts/makentuple2018) to extract the output ROOT files. Then move the extracted `ntuple_2018/` directory into `fcncTriLepton/`. Make sure that the destination does not already contain an `ntuple_2018/` from another production.

```bash
cd submit_2018
makentuple2018
cd ..
mv submit_2018/ntuple_2018 .
```

The resulting `ntuple_2018/` is the **nominal 2018 ntuple** used in the analysis. Once you have verified that the expected ROOT files are present in the new location, you can remove `submit_2018/` with `rm -rf submit_2018` to free disk space.

### 3. Make nominal histograms and plots

To make histograms and plots without systematic variations, run the following scripts in order from `TZWi/TopAnalysis/test/fcncTriLepton/`:

```bash
./02_make_histograms_2018.py
./03_scalemerge_2018.py
./04_drawPlots_2018.py
```

The first script [fills the histograms](https://github.com/panthera718/FCNC_20ULRun2_Variation/blob/20UL18_central/TZWi/TopAnalysis/test/fcncTriLepton/02_make_histograms_2018.py), the second [scales and merges them](https://github.com/panthera718/FCNC_20ULRun2_Variation/blob/20UL18_central/TZWi/TopAnalysis/test/fcncTriLepton/03_scalemerge_2018.py), and the third [draws the plots](https://github.com/panthera718/FCNC_20ULRun2_Variation/blob/20UL18_central/TZWi/TopAnalysis/test/fcncTriLepton/04_drawPlots_2018.py). The histogram definitions are in [`config/histogramming.yaml`](https://github.com/panthera718/FCNC_20ULRun2_Variation/blob/20UL18_central/TZWi/TopAnalysis/test/fcncTriLepton/config/histogramming.yaml).

### 4. Produce the jet energy resolution variations

Use the `20UL18_jerDown` and `20UL18_jerUp` branches for the jet energy resolution (JER) variations. Follow the same ntuple production procedure for each branch. These jobs process MC only, so remove the `RD.Run201*` data definitions and file lists from `TZWi/TopAnalysis/data/datasets/NanoAOD/2018/` **in each variation's working directory**. Keep the data inputs for nominal production.

The [`jerDown` event selection module](https://github.com/panthera718/FCNC_20ULRun2_Variation/blob/20UL18_jerDown/TZWi/TopAnalysis/python/postprocessing/fcncTriLepton_allmodes_unified_jetvar_only.py) reads the following inputs:

| Quantity | `jerDown` input branch | `jerUp` input branch |
|---|---|---|
| MET transverse momentum | `MET_T1_pt_jerDown` | `MET_T1_pt_jerUp` |
| MET azimuthal angle | `MET_T1_phi_jerDown` | `MET_T1_phi_jerUp` |
| Jet transverse momentum | `Jet_pt_jerDown` | `Jet_pt_jerUp` |
| Jet mass | `Jet_mass_jerDown` | `Jet_mass_jerUp` |

For example, the `jerDown` module initializes the MET readers with `tree.valueReader("MET_T1_pt_jerDown")` and `tree.valueReader("MET_T1_phi_jerDown")`. It reads the shifted jet `pt` and `mass` with `tree.arrayReader`. The `jerUp` branch uses the corresponding `jerUp` names.

### 5. Produce the jet energy scale variations

Use `20UL18_jetVar01` as the starting point for the jet energy scale (JES) variations. As with JER production, exclude the `RD.Run201*` data inputs from the variation's working directory.

Only `20UL18_jetVar01` is published in this repository. To produce the full set of JES variations, run nine configurations, `jetVar01` through `jetVar09`, using that branch. Each configuration processes three of the 27 JES uncertainty sources. I split the sources into nine groups after encountering a problem when processing all 27 in a single run.

The groups are defined by `jetUncert` in [`01_prod_ntuple.sh`](https://github.com/panthera718/FCNC_20ULRun2_Variation/blob/20UL18_jetVar01/TZWi/TopAnalysis/test/fcncTriLepton/01_prod_ntuple.sh):

```bash
jetUncert="AbsoluteStat AbsoluteScale AbsoluteMPFBias"
#jetUncert="Fragmentation SinglePionECAL SinglePionHCAL"
#jetUncert="FlavorQCD TimePtEta RelativeJEREC1"
#jetUncert="RelativeJEREC2 RelativeJERHF RelativePtBB"
#jetUncert="RelativePtEC1 RelativePtEC2 RelativePtHF"
#jetUncert="RelativeBal RelativeSample RelativeFSR"
#jetUncert="RelativeStatFSR RelativeStatEC RelativeStatHF"
#jetUncert="PileUpDataMC PileUpPtRef PileUpPtBB"
#jetUncert="PileUpPtEC1 PileUpPtEC2 PileUpPtHF"
```

Enable **exactly one** `jetUncert` line per run. Use the first line for `jetVar01`, the second for `jetVar02`, and so on through the ninth line for `jetVar09`. Each run produces the up and down variations for its three sources.

For each era, retain a separate output for `central`, `jerDown`, `jerUp`, and each of `jetVar01` through `jetVar09`. The production scripts reuse the same output directory name within an era, so keep the runs in separate working directories or archive each result under a distinct name such as `ntuple_2018_central`, `ntuple_2018_jerDown`, or `ntuple_2018_jetVar01`.
