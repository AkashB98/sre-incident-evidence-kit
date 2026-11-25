#!/usr/bin/env python3
"""Demo: score all seeded incidents and show the red-herring contrast on inc-001."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from sre_incident_evidence_kit.loader import load_all
from sre_incident_evidence_kit.scorer import score_incident
from sre_incident_evidence_kit.baseline import heuristic_baseline
def main():
    data=pathlib.Path(__file__).parent/"data"/"incidents"
    for inc in load_all(data):
        r=score_incident(inc)
        print(f"{inc['incident_id']} truth={inc['ground_truth_cause_id']} scorer_top1={r['top1']} baseline={heuristic_baseline(inc)}")
        for rank in r["ranked"]:
            print(f"  - {rank['cause_id']}: {rank['score']} support={rank['supporting']} contradicted_by={rank['contradicted_by']}")
    # Red-herring spotlight
    inc=[i for i in load_all(data) if i["incident_id"]=="inc-001"][0]
    r=score_incident(inc)
    dep=[x for x in r["ranked"] if x["cause_id"]=="deploy_regression"][0]
    print("\nRed-herring spotlight (inc-001): deploy at incident time is NOT the cause.")
    print(f"  deploy_regression contradicted_by={dep['contradicted_by']} — inc001-met-01/inc001-met-02 show pool saturation began 20 min before the deploy.")
    return 0
if __name__=="__main__": raise SystemExit(main())
