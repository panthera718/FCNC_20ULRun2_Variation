import ROOT
import os
import math
import copy
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


class _HistogramLookup2D(object):
    def __init__(self, hist):
        self.hist = hist

    def get_weight(self, x, y):
        if self.hist is None:
            print("ERROR! The weights input histogram is not loaded. Returning weight 0!")
            return 0.0
        binx = max(1, min(self.hist.GetNbinsX(), self.hist.GetXaxis().FindBin(float(x))))
        biny = max(1, min(self.hist.GetNbinsY(), self.hist.GetYaxis().FindBin(float(y))))
        return float(self.hist.GetBinContent(binx, biny))


class _FakeRateCorrectorPy(object):
    def __init__(self, files, histos):
        self.effmaps_ = []
        if len(files) != len(histos):
            print("ERROR! There should be one histogram per input file! Returning 0 as SF.")
            return

        for i in range(len(files)):
            filename = str(files[i])
            histname = str(histos[i])
            tf = ROOT.TFile.Open(filename, "read")
            if not tf or tf.IsZombie():
                print("WARNING! File %s cannot be opened. Skipping this scale factor " % filename)
                continue

            obj = tf.Get(histname)
            if not obj:
                print("ERROR! Histogram %s not in file %s. Not considering this SF. " % (histname, filename))
                tf.Close()
                continue

            hist = obj.Clone(("eff_" + histname))
            hist.SetDirectory(0)
            print("Loading histogram %s from file %s... " % (histname, filename))
            self.effmaps_.append(hist)
            tf.Close()

    def getFR(self, pTcone, abs_eta):
        out = 1.0

        pTcone = float(pTcone)
        abs_eta = float(abs_eta)
        if pTcone >= 100.0:
            pTcone = 99.0
        elif pTcone <= 10.0:
            pTcone = 11.0

        x = abs_eta
        y = pTcone
        for hist in self.effmaps_:
            wc = _HistogramLookup2D(hist)
            out *= wc.get_weight(x, y)
        return float(out)


class FakeRateProducer(Module):
    TAU_FR = {
        "pt_bins_motherjet_approx_GeV": [
            (20, 30),
            (30, 40),
            (40, 50),
            (50, 100),
            (100, 300),
        ],
        "2016postVFP": {
            "prong1": {
                "absEta_0p0_0p8": {
                    "fr":  [0.255000, 0.145444, 0.121453, 0.159962, 0.138307],
                    "err": [0.043462, 0.020221, 0.023732, 0.024955, 0.058605],
                },
                "absEta_0p8_1p5": {
                    "fr":  [0.247223, 0.179972, 0.095790, 0.078256, 0.206505],
                    "err": [0.058178, 0.025956, 0.021645, 0.018140, 0.078847],
                },
                "absEta_1p5_2p4": {
                    "fr":  [0.371148, 0.133069, 0.144136, 0.099639, 0.131985],
                    "err": [0.128756, 0.025918, 0.026873, 0.020452, 0.064875],
                },
            },
            "prong23": {
                "absEta_0p0_2p4": {
                    "fr":  [0.110029, 0.070958, 0.076250, 0.094021, 0.137775],
                    "err": [0.028320, 0.011698, 0.014264, 0.013678, 0.035100],
                },
            },
        },
    }

    def __init__(self, era=None):

        mu_fN = ["2016postVFP_fakerates_MR_mu_LowVersion.root"]
        mu_h = ["fakeratesMRmu"]
        mu_err_h = ["staterr"]

        el_fN = ["2016postVFP_fakerates_MR_ele_LowVersion.root"]
        el_h = ["fakeratesMRele"]
        el_err_h = ["staterr"]

        self.mu_f = ["%s/src/TZWi/TopAnalysis/data/FakeRate/" % os.environ['CMSSW_BASE'] + f for f in mu_fN]
        self.mu_h = list(mu_h)
        self.mu_err_h = list(mu_err_h)

        self.el_f = ["%s/src/TZWi/TopAnalysis/data/FakeRate/" % os.environ['CMSSW_BASE'] + f for f in el_fN]
        self.el_h = list(el_h)
        self.el_err_h = list(el_err_h)

        self.explicit_era = era if era is not None else os.environ.get("FAKERATE_ERA", None)
        self.inputFileName = ""
        self._resolved_era = None
        self._warned_ambiguous_2016 = False
        self._warned_unknown_era = False
        self._warned_tau_no_matched_jet = False

    def beginJob(self):
        self._worker_mu = _FakeRateCorrectorPy(self.mu_f, self.mu_h)
        self._worker_mu_err = _FakeRateCorrectorPy(self.mu_f, self.mu_err_h)
        self._worker_el = _FakeRateCorrectorPy(self.el_f, self.el_h)
        self._worker_el_err = _FakeRateCorrectorPy(self.el_f, self.el_err_h)

    def endJob(self):
        if hasattr(self, '_worker_mu'):
            del self._worker_mu
        if hasattr(self, '_worker_mu_err'):
            del self._worker_mu_err
        if hasattr(self, '_worker_el'):
            del self._worker_el
        if hasattr(self, '_worker_el_err'):
            del self._worker_el_err

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.inputFileName = inputFile.GetName() if inputFile and hasattr(inputFile, "GetName") else ""
        self._resolved_era = self._resolve_tau_era()

        self.out.branch("Lepton1_FR", "F")
        self.out.branch("Lepton1_FRerr", "F")
        self.out.branch("Lepton2_FR", "F")
        self.out.branch("Lepton2_FRerr", "F")
        self.out.branch("Lepton3_FR", "F")
        self.out.branch("Lepton3_FRerr", "F")
        self.out.branch("FakeRateWeight", "F")
        self.out.branch("FakeRateWeightError", "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def _resolve_tau_era(self):
        if self.explicit_era in self.TAU_FR:
            return self.explicit_era

        name = self.inputFileName.lower()
        if "2016" in name:
            return "2016"
        if "2016" in name:
            return "2016"

        pre_tokens = [
            "2016apv", "prevfp", "pre-vfp", "hipm",
            "run2016b", "run2016c", "run2016d", "run2016e", "run2016f-hipm",
        ]
        post_tokens = [
            "2016postvfp", "postvfp", "post-vfp",
            "run2016g", "run2016h", "run2016f-ul2016",
        ]

        for tok in pre_tokens:
            if tok in name:
                return "2016preVFP"
        for tok in post_tokens:
            if tok in name and "hipm" not in name:
                return "2016postVFP"

        if "2016" in name:
            if not self._warned_ambiguous_2016:
                print("[FakeRateProducer] Warning: could not distinguish 2016preVFP and 2016postVFP from input file '%s'. Defaulting tau fake rate era to 2016preVFP. Set FAKERATE_ERA or instantiate FakeRateProducer(era='2016postVFP') to override." % self.inputFileName)
                self._warned_ambiguous_2016 = True
            return "2016preVFP"

        if not self._warned_unknown_era:
            print("[FakeRateProducer] Warning: could not infer tau fake rate era from input file '%s'. Defaulting to 2016." % self.inputFileName)
            self._warned_unknown_era = True
        return "2016"

    @staticmethod
    def _get_tau_prong_group(decay_mode):
        dm = int(decay_mode)
        if dm in (0, 1, 2):
            return "prong1"
        if dm in (10, 11):
            return "prong23"
        if dm >= 10:
            return "prong23"
        return "prong1"

    @staticmethod
    def _get_tau_eta_key(abs_eta, prong_group):
        if prong_group == "prong23":
            return "absEta_0p0_2p4"
        if abs_eta < 0.8:
            return "absEta_0p0_0p8"
        if abs_eta < 1.5:
            return "absEta_0p8_1p5"
        return "absEta_1p5_2p4"

    def _get_tau_pt_bin_index(self, mother_jet_pt):
        bins = self.TAU_FR["pt_bins_motherjet_approx_GeV"]
        pt = float(mother_jet_pt)
        if pt < bins[0][0]:
            return 0
        for i, (ptmin, ptmax) in enumerate(bins):
            if pt >= ptmin and pt < ptmax:
                return i
        return len(bins) - 1

    def _get_tau_fr(self, era, mother_jet_pt, abs_eta, decay_mode):
        prong_group = self._get_tau_prong_group(decay_mode)
        eta_key = self._get_tau_eta_key(abs_eta, prong_group)
        ibin = self._get_tau_pt_bin_index(mother_jet_pt)
        fr_map = self.TAU_FR[era][prong_group][eta_key]
        return float(fr_map["fr"][ibin]), float(fr_map["err"][ibin])

    @staticmethod
    def _get_ptcone_from_tree(tree, idx):
        is_tight = getattr(tree, "b_out_Lepton%d_isTight" % idx)
        lep_pt = getattr(tree, "b_out_Lepton%d_pt" % idx)
        jet_pt = getattr(tree, "b_out_Lepton%d_Jet_pt" % idx)
        lep_pfiso = getattr(tree, "b_out_Lepton%d_PFIso" % idx)
        if is_tight:
            return lep_pt
        if jet_pt > 0:
            return 0.7 * jet_pt
        return 0.7 * lep_pt * (1.0 + lep_pfiso)

    def _get_tau_inputs_from_tree(self, tree, idx):
        tau_decay_attr = "b_out_Lepton%d_tauDecayMode" % idx
        if not hasattr(tree, tau_decay_attr):
            raise RuntimeError(
                "Tau fake rate requires Lepton%d_tauDecayMode, but this branch is missing. "
                "Update fcncTriLepton_allmodes_unified to store tau decayMode/prong information before running FakeRateProducer." % idx
            )
        decay_mode = int(getattr(tree, tau_decay_attr))
        mother_jet_pt = getattr(tree, "b_out_Lepton%d_Jet_pt" % idx)
        if mother_jet_pt <= 0.0:
            if not self._warned_tau_no_matched_jet:
                print("[FakeRateProducer] Warning: tau candidate without matched jet encountered. Falling back to tau pT for tau fake-rate lookup.")
                self._warned_tau_no_matched_jet = True
            mother_jet_pt = getattr(tree, "b_out_Lepton%d_pt" % idx)
        abs_eta = abs(getattr(tree, "b_out_Lepton%d_eta" % idx))
        return float(mother_jet_pt), float(abs_eta), decay_mode

    def _get_lepton_fr(self, tree, idx):
        pdgid = abs(getattr(tree, "b_out_Lepton%d_pdgId" % idx))

        if pdgid == 11:
            ptcone = self._get_ptcone_from_tree(tree, idx)
            eta = abs(getattr(tree, "b_out_Lepton%d_eta" % idx))
            return float(self._worker_el.getFR(ptcone, eta)), float(self._worker_el_err.getFR(ptcone, eta))

        if pdgid == 13:
            ptcone = self._get_ptcone_from_tree(tree, idx)
            eta = abs(getattr(tree, "b_out_Lepton%d_eta" % idx))
            return float(self._worker_mu.getFR(ptcone, eta)), float(self._worker_mu_err.getFR(ptcone, eta))

        if pdgid == 15:
            mother_jet_pt, abs_eta, decay_mode = self._get_tau_inputs_from_tree(tree, idx)
            return self._get_tau_fr(self._resolved_era, mother_jet_pt, abs_eta, decay_mode)

        return 0.0, 0.0

    @staticmethod
    def _fr_to_factor(fr):
        fr = float(fr)
        if fr >= 1.0:
            fr = 1.0 - 1.0e-6
        if fr <= -1.0:
            fr = -1.0 + 1.0e-6
        return -fr / (1.0 - fr)

    @staticmethod
    def _frerr_to_factorerr(fr, fr_err):
        fr = float(fr)
        fr_err = abs(float(fr_err))
        if fr >= 1.0:
            fr = 1.0 - 1.0e-6
        if fr <= -1.0:
            fr = -1.0 + 1.0e-6
        return fr_err / ((1.0 - fr) ** 2)

    @staticmethod
    def _event_has_selected_tau(tree):
        return any(
            abs(int(getattr(tree, "b_out_Lepton%d_pdgId" % idx))) == 15
            for idx in (1, 2, 3)
        )

    @staticmethod
    def _event_has_prompt_selected_tau(tree):
        for idx in (1, 2, 3):
            if abs(int(getattr(tree, "b_out_Lepton%d_pdgId" % idx))) != 15:
                continue

            tau_genpartflav_attr = "b_out_Lepton%d_tauGenPartFlav" % idx
            if not hasattr(tree, tau_genpartflav_attr):
                raise RuntimeError(
                    "Tau prompt-subtraction requires Lepton%d_tauGenPartFlav, but this branch is missing. "
                    "Update fcncTriLepton_allmodes_unified.py before running FakeRateProducer." % idx
                )

            if int(getattr(tree, tau_genpartflav_attr)) == 5:
                return True
        return False

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        tree = event._tree

        fr_lepton1, fr_lepton1_err = self._get_lepton_fr(tree, 1)
        fr_lepton2, fr_lepton2_err = self._get_lepton_fr(tree, 2)
        fr_lepton3, fr_lepton3_err = self._get_lepton_fr(tree, 3)

        fake_terms = []
        for is_fake, fr, fr_err in [
            (tree.b_out_Lepton1_isFake, fr_lepton1, fr_lepton1_err),
            (tree.b_out_Lepton2_isFake, fr_lepton2, fr_lepton2_err),
            (tree.b_out_Lepton3_isFake, fr_lepton3, fr_lepton3_err),
        ]:
            if is_fake:
                fake_terms.append((self._fr_to_factor(fr), self._frerr_to_factorerr(fr, fr_err)))

        if not fake_terms:
            FRweight = 0.0
            FRweightErr = 0.0
        else:
            FRweight = -1.0
            for factor, _ in fake_terms:
                FRweight *= factor

            FRweightErr2 = 0.0
            for i, (_, factor_err) in enumerate(fake_terms):
                other_prod = -1.0
                for j, (other_factor, _) in enumerate(fake_terms):
                    if i == j:
                        continue
                    other_prod *= other_factor
                FRweightErr2 += (other_prod * factor_err) ** 2
            FRweightErr = math.sqrt(FRweightErr2)

        self.out.fillBranch("Lepton1_FR", fr_lepton1)
        self.out.fillBranch("Lepton1_FRerr", fr_lepton1_err)
        self.out.fillBranch("Lepton2_FR", fr_lepton2)
        self.out.fillBranch("Lepton2_FRerr", fr_lepton2_err)
        self.out.fillBranch("Lepton3_FR", fr_lepton3)
        self.out.fillBranch("Lepton3_FRerr", fr_lepton3_err)
        self.out.fillBranch("FakeRateWeight", FRweight)
        self.out.fillBranch("FakeRateWeightError", FRweightErr)

        return True


#FRProducer = lambda: FakeRateProducer()
FRProducer_2016postVFP = lambda: FakeRateProducer(era="2016postVFP")
