from google.adk.tools.function_tool import FunctionTool
from ..data_access.erp_data import (
    compute_finance_kpis,
    detect_finance_anomaly,
    payment_cycle_health,
)
from ..services.memory import log_insight

def _finance_health():
    """
    Provides finance and payment cycle health.
    - Total spend, average spend per customer
    - Revenue trends
    - Payment cycle anomalies and overdue invoices
    """
    kpis = compute_finance_kpis()
    anomaly = detect_finance_anomaly(kpis)
    payment = payment_cycle_health()

    explanation = []
    if anomaly["is_anomaly"]:
        explanation.append(
            f"Weekly revenue is {kpis['revenue_last_week']} (below target)."
        )
    if payment["overdue_invoices"] > 0:
        explanation.append(
            f"{payment['overdue_invoices']} overdue invoices totaling ${payment['overdue_amount']:,.2f}."
        )

    recs = []
    if payment["overdue_invoices"] > 0:
        recs.append("Send dunning notices for overdue invoices.")
        recs.append("Review payment terms and discount structures.")
    else:
        recs.append("Maintain current payment terms; no immediate action needed.")

    insight = {
        "kpis": kpis,
        "anomaly": anomaly,
        "payment_cycle": payment,
        "explanation": " ".join(explanation) if explanation else "Finance metrics appear healthy.",
        "recommendations": recs,
    }

    log_insight("finance", insight)
    return insight

finance_health = FunctionTool(_finance_health)
