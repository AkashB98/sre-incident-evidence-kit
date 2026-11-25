import argparse, json, pathlib
from .loader import load_all, load_incident
from .scorer import score_incident
def main(argv=None):
    ap=argparse.ArgumentParser(prog="sre-incident-evidence-kit")
    ap.add_argument("--data", default=str(pathlib.Path(__file__).resolve().parent.parent/"data"/"incidents"))
    ap.add_argument("--incident", default=None)
    a=ap.parse_args(argv)
    incs=[load_incident(a.incident)] if a.incident else load_all(a.data)
    for inc in incs:
        r=score_incident(inc)
        print(f"{inc['incident_id']}: {inc['title']}")
        print(f"  timeline: {len(r['timeline'])} evidence items")
        for rank in r["ranked"]:
            print(f"  {rank['cause_id']}: score={rank['score']} supporting={rank['supporting']} contradicted_by={rank['contradicted_by']}")
        print(f"  top-1: {r['top1']} (truth: {inc['ground_truth_cause_id']})")
    return 0
if __name__=="__main__": raise SystemExit(main())
