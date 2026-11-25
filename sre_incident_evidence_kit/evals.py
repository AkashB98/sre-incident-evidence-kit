from .timeline import build_timeline, decisive_items
from .scorer import score_incident, cited_evidence
from .baseline import heuristic_baseline
def evaluate(incidents):
    per=[]; t1=t3=base=0; comp_sum=0.0
    for inc in incidents:
        r=score_incident(inc); truth=inc["ground_truth_cause_id"]
        is1=r["top1"]==truth; is3=truth in r["top3"]
        b=heuristic_baseline(inc); b_ok=b==truth
        t1+=is1; t3+=is3; base+=b_ok
        dec=decisive_items(build_timeline(inc))
        cited=cited_evidence(r)
        # decisive surfaced if cited for/against any ranked cause
        surfaced=[e for e in dec if e["id"] in cited]
        comp=(len(surfaced)/len(dec)) if dec else 1.0; comp_sum+=comp
        per.append({"incident_id":inc["incident_id"],"ground_truth":truth,"scorer_top1":r["top1"],"scorer_top3":r["top3"],
                    "top1_correct":is1,"top3_correct":is3,"baseline_pick":b,"baseline_correct":b_ok,
                    "evidence_completeness":round(comp,4),"decisive_total":len(dec),"decisive_surfaced":len(surfaced),
                    "ranked":[{"cause_id":x["cause_id"],"score":x["score"],"supporting":x["supporting"],"contradicted_by":x["contradicted_by"]} for x in r["ranked"]]})
    n=len(incidents) or 1
    return {"n_incidents":len(incidents),"scorer_top1_accuracy":round(t1/n,4),"scorer_top3_accuracy":round(t3/n,4),
            "evidence_completeness":round(comp_sum/n,4),"baseline_top1_accuracy":round(base/n,4),
            "baseline_label":"latest deploy within 15 min, else loudest alert","per_incident":per}
