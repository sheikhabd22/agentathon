"""
Tool for the agent to access monitoring snapshot and active risks.
This allows the LLM to reason about current business health + risks.
"""
from google.adk.tools.function_tool import FunctionTool
from ..services.monitoring_engine import compute_monitoring_snapshot
from ..services.risk_engine import get_active_risks, generate_risks_from_monitoring, store_risks
from ..services.memory import log_risk_reference
from ..services.visualization import create_kpi_visual, create_risk_list_visual


def _get_monitoring_snapshot():
    """
    Retrieve the current business health snapshot from the monitoring engine.
    Shows revenue, customer, finance, and inventory metrics + alerts.
    Includes visualization specs for dashboard rendering.
    """
    snapshot = compute_monitoring_snapshot()
    
    # Add visualization specs for key metrics
    metrics = snapshot.get("metrics", {})
    visuals = []
    
    # Revenue KPI visual
    if "revenue" in metrics:
        rev = metrics["revenue"]
        status = "negative" if rev.get("alert") else "positive" if rev.get("revenue_change_pct", 0) > 0 else "warning"
        visuals.append(create_kpi_visual(
            title="Revenue",
            value=rev.get("current_revenue", 0),
            status=status,
            unit="$",
            change_pct=rev.get("revenue_change_pct", 0)
        ))
    
    # Customer churn KPI visual
    if "customers" in metrics:
        cust = metrics["customers"]
        status = "negative" if cust.get("alert") else "positive"
        visuals.append(create_kpi_visual(
            title="Customer Churn",
            value=cust.get("churn_rate_pct", 0),
            status=status,
            unit="%"
        ))
    
    snapshot["visuals"] = visuals
    return snapshot


def _get_active_risks():
    """
    Retrieve all currently active business risks.
    Each risk includes type, description, severity, and timestamp.
    Includes visualization spec for risk list rendering.
    """
    risks = get_active_risks()
    
    # Add risk list visualization
    if risks:
        visual = create_risk_list_visual(
            title="Active Business Risks",
            risks=risks
        )
        return {
            "risks": risks,
            "count": len(risks),
            "visual": visual
        }
    
    return {"risks": risks, "count": 0}


def _check_and_generate_risks():
    """
    Generate new risks from current monitoring state if conditions warrant.
    Stores generated risks for future reference.
    """
    snapshot = compute_monitoring_snapshot()
    new_risks = generate_risks_from_monitoring(snapshot)
    
    if new_risks:
        store_risks(new_risks)
        # Log to agent memory
        for risk in new_risks:
            log_risk_reference(
                risk["risk_id"],
                f"Generated: {risk['description']}"
            )
    
    return {
        "generated_count": len(new_risks),
        "risks": new_risks
    }


monitoring_snapshot_tool = FunctionTool(_get_monitoring_snapshot)
active_risks_tool = FunctionTool(_get_active_risks)
check_risks_tool = FunctionTool(_check_and_generate_risks)
