# tools.py
from google.adk import tool
from data_access import (
    compute_revenue_kpis,
    detect_revenue_anomaly,
    inactive_customers,
    customer_segment_summary,
    overdue_invoice_summary,
    inventory_risk_summary
)


@tool
def revenue_health():
    """
    Returns revenue KPIs and anomaly signals.
    """
    kpis = compute_revenue_kpis()
    anomaly = detect_revenue_anomaly(kpis)
    return {"kpis": kpis, "anomaly": anomaly}


@tool
def customer_health():
    """
    Returns inactive customer summary and segment distribution.
    """
    customers = inactive_customers()
    segments = customer_segment_summary(customers)
    return {
        "inactive_count": len(customers),
        "segment_distribution": segments
    }


@tool
def finance_health():
    """
    Returns overdue invoice risk summary.
    """
    return overdue_invoice_summary()


@tool
def inventory_health():
    """
    Returns inventory shortage risk.
    """
    return inventory_risk_summary()
