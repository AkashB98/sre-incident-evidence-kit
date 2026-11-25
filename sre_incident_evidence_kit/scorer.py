from .timeline import build_timeline
def score_incident(incident):
    timeline=build_timeline(incident)
    scores={}
    for c in incident["candidate_causes"]:
        scores[c["id"]]={"cause_id":c["id"],"label":c["label"],"score":0,"supporting":[],"contradicting":[],"contradicted_by":[]}
    for e in timeline:
        w=2 if e.get("decisive") else 1
        for cid in e.get("supports",[]):
            if cid in scores:
                scores[cid]["score"]+=w; scores[cid]["supporting"].append(e["id"])
        for cid in e.get("contradicts",[]):
            if cid in scores:
                scores[cid]["score"]-=w; scores[cid]["contradicted_by"].append(e["id"])
                # also record this evidence as contradicting evidence cited against that cause
    ranked=sorted(scores.values(), key=lambda x: (-x["score"], x["cause_id"]))
    return {"incident_id":incident["incident_id"],"timeline":timeline,"ranked":ranked,
            "top1":ranked[0]["cause_id"] if ranked else None,
            "top3":[r["cause_id"] for r in ranked[:3]]}
def cited_evidence(result):
    ids=set()
    for r in result["ranked"]:
        ids.update(r["supporting"]); ids.update(r["contradicted_by"])
    return ids
