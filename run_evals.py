#!/usr/bin/env python3
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from sre_incident_evidence_kit.loader import load_all
from sre_incident_evidence_kit.evals import evaluate
def main():
    root=pathlib.Path(__file__).parent
    report=evaluate(load_all(root/"data"/"incidents"))
    (root/"eval_report.json").write_text(json.dumps(report,indent=2))
    print(json.dumps({k:report[k] for k in ("n_incidents","scorer_top1_accuracy","scorer_top3_accuracy","evidence_completeness","baseline_top1_accuracy")},indent=2))
    return 0
if __name__=="__main__": raise SystemExit(main())
