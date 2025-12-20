"""
Causal inference and what-if scenario engine.
Provides simple causal reasoning for business metrics.
"""

def infer_causal_relationships(metrics_snapshot: dict) -> dict:
    """
    Simple causal graph: revenue -> order count, customer activity -> spend.
    Returns likely causal chains for observed changes.
    """
    causal_chains = []

    # Revenue and order correlation
    if "revenue_change" in metrics_snapshot and "order_change" in metrics_snapshot:
        rev_change = metrics_snapshot["revenue_change"]
        ord_change = metrics_snapshot["order_change"]

        if rev_change < -5 and ord_change < -3:
            causal_chains.append({
                "cause": "Lower order volume",
                "effect": "Revenue decline",
                "confidence": 0.85,
            })
        elif rev_change < -5 and ord_change >= -3:
            causal_chains.append({
                "cause": "Price reduction or margin compression",
                "effect": "Revenue decline",
                "confidence": 0.70,
            })

    # Customer activity and spend
    if "inactive_customer_change" in metrics_snapshot:
        inactive_change = metrics_snapshot["inactive_customer_change"]
        if inactive_change > 10:
            causal_chains.append({
                "cause": "Increasing customer inactivity",
                "effect": "Future revenue risk",
                "confidence": 0.75,
            })

    return {"causal_chains": causal_chains}

def simulate_what_if(base_metrics: dict, intervention: str) -> dict:
    """
    Simple what-if scenario simulator.
    Example: "What if we reduce prices by 10%?"
    """
    scenarios = {}

    if "reduce_prices" in intervention.lower():
        pct = 0.1
        scenarios["scenario"] = f"Reduce prices by {pct*100}%"
        scenarios["estimated_order_lift"] = f"+{pct*20:.0f}%"  # simple elasticity
        scenarios["estimated_revenue_impact"] = f"-{pct*5:.1f}%"
        scenarios["recommendation"] = "Net negative; use selective discounting instead."

    elif "increase_prices" in intervention.lower():
        pct = 0.05
        scenarios["scenario"] = f"Increase prices by {pct*100}%"
        scenarios["estimated_order_decline"] = f"-{pct*15:.0f}%"
        scenarios["estimated_revenue_impact"] = f"+{pct*2:.1f}%"
        scenarios["recommendation"] = "Minimal revenue uplift; risk losing price-sensitive customers."

    elif "expand" in intervention.lower() or "marketing" in intervention.lower():
        scenarios["scenario"] = "Increase marketing spend by 20%"
        scenarios["estimated_customer_acquisition"] = "+15% new customers"
        scenarios["estimated_revenue_impact"] = "+12%"
        scenarios["payback_period_months"] = 4.5
        scenarios["recommendation"] = "Strong ROI; recommend proceeding with phased rollout."

    else:
        scenarios["scenario"] = "Unknown intervention"
        scenarios["recommendation"] = "Please specify an intervention (e.g., price change, marketing spend)."

    return scenarios

def recommend_next_actions(insights: list) -> list:
    """
    Synthesize insights across domains to generate prioritized, actionable recommendations.
    """
    actions = []
    domains_with_anomalies = [i for i in insights if i.get("anomaly", {}).get("is_anomaly")]

    if not domains_with_anomalies:
        return ["All metrics appear healthy. Continue monitoring."]

    # Sort by severity
    critical = [i for i in domains_with_anomalies if i.get("anomaly", {}).get("severity") == "HIGH"]
    medium = [i for i in domains_with_anomalies if i.get("anomaly", {}).get("severity") == "MEDIUM"]

    if critical:
        for insight in critical:
            domain = insight.get("domain", "unknown")
            recs = insight.get("recommendations", [])
            if recs:
                actions.append(f"[URGENT - {domain.upper()}] {recs[0]}")

    if medium:
        for insight in medium:
            domain = insight.get("domain", "unknown")
            recs = insight.get("recommendations", [])
            if recs:
                actions.append(f"[ACTION - {domain.upper()}] {recs[0]}")

    return actions if actions else ["Monitor metrics closely."]
