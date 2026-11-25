import json, pathlib
def load_incident(path):
    return json.loads(pathlib.Path(path).read_text())
def load_all(data_dir):
    d=pathlib.Path(data_dir)
    return [load_incident(p) for p in sorted(d.glob("*.json"))]
