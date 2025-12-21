"""
Risk Generation and Persistence Engine
Generates structured risk objects based on monitoring signals.
Stores historical risks for review.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


RISKS_PATH = Path("data/risks.json")


def _load_risks() -> List[Dict]:
    """Load all risks from persistent storage."""
    if RISKS_PATH.exists():
        try:
            with open(RISKS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def _save_risks(risks: List[Dict]):
    """Persist risks to storage."""
    RISKS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RISKS_PATH, "w", encoding="utf-8") as f:
        json.dump(risks, f, indent=2, default=str)


def generate_risks_from_monitoring(monitoring_snapshot: Dict) -> List[Dict]:
    """
    Generate structured risk objects from monitoring data.
    Each risk has: risk_type, description, severity, timestamp, status.
    """
    risks = []
    ts = datetime.utcnow().isoformat() + "Z"
    
    metrics = monitoring_snapshot.get("metrics", {})
    
    # Revenue risk
    revenue = metrics.get("revenue", {})
    if revenue.get("alert"):
        change_pct = revenue.get("revenue_change_pct", 0)
        severity = "HIGH" if change_pct <= -15 else "MEDIUM"
        risks.append({
            "risk_id": f"REVENUE_{ts}",
            "risk_type": "REVENUE",
            "description": f"Revenue declined {change_pct}% compared to previous period. Investigate pricing, customer activity, or market conditions.",
            "severity": severity,
            "timestamp": ts,
            "status": "ACTIVE",
            "metrics": {"revenue_change_pct": change_pct}
        })
    
    # Customer churn risk
    customers = metrics.get("customers", {})
    if customers.get("alert"):
        churn = customers.get("churn_rate_pct", 0)
        risks.append({
            "risk_id": f"CUSTOMER_{ts}",
            "risk_type": "CUSTOMER",
            "description": f"{churn:.1f}% of customers are inactive (>30 days). High churn may signal service or engagement issues.",
            "severity": "HIGH" if churn > 60 else "MEDIUM",
            "timestamp": ts,
            "status": "ACTIVE",
            "metrics": {"churn_rate_pct": churn, "inactive_count": customers.get("inactive_count")}
        })
    
    # Cash flow risk
    finance = metrics.get("finance", {})
    if finance.get("alert"):
        overdue_amount = finance.get("outstanding_cash_amount", 0)
        overdue_count = finance.get("overdue_invoices", 0)
        risks.append({
            "risk_id": f"CASH_FLOW_{ts}",
            "risk_type": "CASH_FLOW",
            "description": f"{overdue_count} overdue invoices totaling ${overdue_amount:,.2f}. Immediate collection action required to maintain cash flow.",
            "severity": "HIGH" if overdue_amount > 20_000_000 else "MEDIUM",
            "timestamp": ts,
            "status": "ACTIVE",
            "metrics": {"overdue_amount": overdue_amount, "overdue_invoices": overdue_count}
        })
    
    # Inventory risk
    inventory = metrics.get("inventory", {})
    if inventory.get("alert"):
        low_stock_count = inventory.get("low_stock_item_count", 0)
        days_inv = inventory.get("days_inventory", 0)
        desc = f"{low_stock_count} SKUs below reorder threshold." if low_stock_count > 10 else f"Inventory sitting for {days_inv:.1f} days (high holding cost)."
        risks.append({
            "risk_id": f"INVENTORY_{ts}",
            "risk_type": "INVENTORY",
            "description": desc,
            "severity": "MEDIUM" if low_stock_count > 10 else "LOW",
            "timestamp": ts,
            "status": "ACTIVE",
            "metrics": {"low_stock_count": low_stock_count, "days_inventory": days_inv}
        })
    
    return risks


def store_risks(new_risks: List[Dict]):
    """Append new risks to persistent storage."""
    existing = _load_risks()
    existing.extend(new_risks)
    _save_risks(existing)


def get_active_risks() -> List[Dict]:
    """Retrieve all active risks."""
    all_risks = _load_risks()
    return [r for r in all_risks if r.get("status") == "ACTIVE"]


def get_historical_risks() -> List[Dict]:
    """Retrieve all historical (resolved) risks."""
    all_risks = _load_risks()
    return [r for r in all_risks if r.get("status") == "RESOLVED"]


def get_all_risks() -> List[Dict]:
    """Retrieve all risks (active + resolved)."""
    return _load_risks()


def resolve_risk(risk_id: str):
    """Mark a risk as resolved."""
    all_risks = _load_risks()
    for risk in all_risks:
        if risk.get("risk_id") == risk_id:
            risk["status"] = "RESOLVED"
            risk["resolved_at"] = datetime.utcnow().isoformat() + "Z"
    _save_risks(all_risks)


def auto_resolve_stale_risks(max_age_hours: int = 48):
    """
    Auto-resolve risks older than max_age_hours if monitoring no longer flags them.
    Simple heuristic: if risk type is no longer in active alerts, mark resolved.
    """
    from .monitoring_engine import compute_monitoring_snapshot
    
    snapshot = compute_monitoring_snapshot()
    alerts = snapshot.get("status", {})
    
    active_types = set()
    if alerts.get("revenue_alert"):
        active_types.add("REVENUE")
    if alerts.get("high_churn"):
        active_types.add("CUSTOMER")
    if alerts.get("cash_crunch"):
        active_types.add("CASH_FLOW")
    if alerts.get("inventory_crisis"):
        active_types.add("INVENTORY")
    
    all_risks = _load_risks()
    now = datetime.utcnow()
    
    for risk in all_risks:
        if risk.get("status") != "ACTIVE":
            continue
        
        risk_type = risk.get("risk_type")
        risk_ts = datetime.fromisoformat(risk.get("timestamp", "").replace("Z", ""))
        age_hours = (now - risk_ts).total_seconds() / 3600
        
        # Auto-resolve if type not in active alerts and older than threshold
        if risk_type not in active_types and age_hours > max_age_hours:
            risk["status"] = "RESOLVED"
            risk["resolved_at"] = datetime.utcnow().isoformat() + "Z"
            risk["resolution_reason"] = "Auto-resolved: monitoring no longer flags this issue"
    
    _save_risks(all_risks)
