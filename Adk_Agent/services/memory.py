import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

MEMORY_PATH = Path("data/memory.json")

def _load_memory():
    if MEMORY_PATH.exists():
        try:
            with open(MEMORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"preferences": {}, "insights": [], "risk_references": []}
    return {"preferences": {}, "insights": [], "risk_references": []}

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


def log_risk_reference(risk_id: str, context: str):
    """Store a reference to a risk the agent mentioned or generated."""
    mem = _load_memory()
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "risk_id": risk_id,
        "context": context,
    }
    mem.setdefault("risk_references", []).append(entry)
    mem["risk_references"] = mem["risk_references"][-50:]  # keep last 50
    _save_memory(mem)
    return entry


def recent_risk_references(limit: int = 10) -> List[Dict]:
    """Retrieve recent risk references from agent memory."""
    mem = _load_memory()
    return list(reversed(mem.get("risk_references", [])))[:limit]
