from google.adk.tools.function_tool import FunctionTool
from ..data_access.revenue_data import (
    compute_revenue_kpis,
    detect_revenue_anomaly,
    supporting_signals,
)
from ..data_access.crm_data import top_customers
from ..services.memory import log_insight
from ..services.visualization import create_kpi_visual, create_trend_visual

def _revenue_health():
    """
    REQUIRED for answering questions about:
    - revenue increase or decline
    - revenue trends
    - recent revenue performance
    - business growth or slowdown

    Returns KPIs, anomaly flags, causal hints, recommendations, and optional visualization specs.
    """
    kpis = compute_revenue_kpis()
    anomaly = detect_revenue_anomaly(kpis)
    signals = supporting_signals()

    # Simple causal reasoning
    explanation = []
    if anomaly["is_anomaly"]:
        explanation.append(
            f"Revenue changed {kpis['revenue_change_pct']}% week-over-week."
        )
        if signals["order_change_pct"] < -5:
            explanation.append(
                f"Orders fell {signals['order_change_pct']}%, likely contributing to revenue drop."
            )
        else:
            explanation.append("Order volume was stable; investigate pricing or discounts.")

    # Actionable recommendations
    recs = []
    if anomaly["is_anomaly"]:
        tc = top_customers(3)
        names = ", ".join(c["customer_name"] for c in tc)
        recs.append(f"Engage top customers ({names}) to probe deferred orders.")
        recs.append("Offer targeted promotions to at-risk segments.")
        recs.append("Audit recent pricing or invoice terms that may affect conversions.")
    else:
        recs.append("Maintain current campaigns; monitor segments for emerging changes.")

    # Generate visualization spec
    status = "negative" if anomaly["is_anomaly"] else "positive" if kpis["revenue_change_pct"] > 0 else "warning"
    visual = create_kpi_visual(
        title="Revenue",
        value=kpis["current_revenue"],
        status=status,
        unit="$",
        change_pct=kpis["revenue_change_pct"]
    )

    insight = {
        "kpis": kpis,
        "anomaly": anomaly,
        "signals": signals,
        "explanation": " ".join(explanation) if explanation else "Revenue appears stable.",
        "recommendations": recs,
        "visual": visual  # Include visualization spec
    }

    # Persist insight to memory
    log_insight("revenue", insight)

    return insight

revenue_health = FunctionTool(_revenue_health)
