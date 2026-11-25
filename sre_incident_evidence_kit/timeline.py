def build_timeline(incident):
    items=[]
    for stype, lst in incident.get("sources",{}).items():
        for it in lst:
            e=dict(it); e.setdefault("source_type", stype); items.append(e)
    return sorted(items, key=lambda x: x["timestamp"])
def decisive_items(timeline):
    return [e for e in timeline if e.get("decisive")]
