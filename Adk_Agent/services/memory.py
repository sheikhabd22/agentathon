import json
from pathlib import Path
from datetime import datetime

MEMORY_PATH = Path("data/memory.json")

def _load_memory():
    if MEMORY_PATH.exists():
        try:
            with open(MEMORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"preferences": {}, "insights": []}
    return {"preferences": {}, "insights": []}

def _save_memory(mem):
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(mem, f, indent=2, default=str)

def get_preferences():
    mem = _load_memory()
    return mem.get("preferences", {})

def set_preference(key: str, value):
    mem = _load_memory()
    prefs = mem.get("preferences", {})
    prefs[key] = value
    mem["preferences"] = prefs
    _save_memory(mem)
    return prefs

def log_insight(domain: str, payload: dict):
    mem = _load_memory()
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "domain": domain,
        "payload": payload,
    }
    mem.setdefault("insights", []).append(entry)
    # keep last 100
    mem["insights"] = mem["insights"][-100:]
    _save_memory(mem)
    return entry

def recent_insights(limit: int = 10):
    mem = _load_memory()
    return list(reversed(mem.get("insights", [])))[:limit]
