import pathlib, sys, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from sre_incident_evidence_kit.loader import load_all
from sre_incident_evidence_kit.timeline import build_timeline
from sre_incident_evidence_kit.scorer import score_incident
from sre_incident_evidence_kit.baseline import heuristic_baseline
from sre_incident_evidence_kit.evals import evaluate
DATA=pathlib.Path(__file__).resolve().parent.parent/"data"/"incidents"
class TestKit(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.incs=load_all(DATA)
    def test_count(self): self.assertTrue(6 <= len(self.incs) <= 8)
    def test_four_source_types(self):
        for inc in self.incs:
            self.assertEqual(set(inc["sources"].keys()), {"logs","metrics","alerts","deploys"})
            for v in inc["sources"].values(): self.assertTrue(len(v)>=1)
    def test_candidates_include_truth(self):
        for inc in self.incs:
            ids=[c["id"] for c in inc["candidate_causes"]]
            self.assertIn(inc["ground_truth_cause_id"], ids)
    def test_timeline_sorted(self):
        for inc in self.incs:
            ts=[e["timestamp"] for e in build_timeline(inc)]
            self.assertEqual(ts, sorted(ts))
    def test_timeline_merges_all(self):
        for inc in self.incs:
            total=sum(len(v) for v in inc["sources"].values())
            self.assertEqual(len(build_timeline(inc)), total)
    def test_scorer_cites_evidence(self):
        r=score_incident(self.incs[0])
        self.assertTrue(r["ranked"][0]["supporting"])
    def test_red_herring_inc001(self):
        inc=[i for i in self.incs if i["incident_id"]=="inc-001"][0]
        self.assertEqual(score_incident(inc)["top1"], "db_pool_exhaustion")
        self.assertEqual(heuristic_baseline(inc), "deploy_regression")
        dep=[x for x in score_incident(inc)["ranked"] if x["cause_id"]=="deploy_regression"][0]
        self.assertTrue(dep["contradicted_by"], "scorer must cite contradicting evidence on red herring")
    def test_red_herring_cache_loudest_alert(self):
        inc=[i for i in self.incs if i["incident_id"]=="inc-003"][0]
        self.assertEqual(score_incident(inc)["top1"], "cache_failure")
        self.assertNotEqual(heuristic_baseline(inc), "cache_failure")
    def test_scorer_beats_baseline(self):
        rep=evaluate(self.incs)
        self.assertGreater(rep["scorer_top1_accuracy"], rep["baseline_top1_accuracy"])
    def test_eval_bounds(self):
        rep=evaluate(self.incs)
        for k in ("scorer_top1_accuracy","scorer_top3_accuracy","evidence_completeness","baseline_top1_accuracy"):
            self.assertTrue(0 <= rep[k] <= 1)
    def test_top3_contains_truth_most(self):
        rep=evaluate(self.incs)
        self.assertGreaterEqual(rep["scorer_top3_accuracy"], rep["scorer_top1_accuracy"])
    def test_no_personal_data_markers(self):
        for inc in self.incs:
            s=str(inc).lower()
            self.assertNotIn("akash", s); self.assertNotIn("@gmail", s)
if __name__=="__main__": unittest.main()
