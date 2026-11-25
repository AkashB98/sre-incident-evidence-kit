from .timeline import build_timeline
SEV={"P1":3,"P2":2,"P3":1}
def heuristic_baseline(incident):
    """Latest deploy within 15 min wins; otherwise loudest alert's implied cause."""
    from datetime import datetime
    def parse(s): return datetime.fromisoformat(s.replace("Z","+00:00"))
    start=parse(incident["start_time"])
    timeline=build_timeline(incident)
    deploys=[e for e in timeline if e["source_type"]=="deploy" and e.get("implies_cause")]
    recent=[e for e in deploys if abs((parse(e["timestamp"])-start).total_seconds())<=900]
    if recent:
        recent.sort(key=lambda x: x["timestamp"])
        return recent[-1]["implies_cause"]
    alerts=[e for e in timeline if e["source_type"]=="alert" and e.get("implies_cause")]
    if alerts:
        alerts.sort(key=lambda x: SEV.get(x.get("severity","P3"),0), reverse=True)
        return alerts[0]["implies_cause"]
    return None
