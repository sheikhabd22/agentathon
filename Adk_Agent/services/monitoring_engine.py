"""
Deterministic Monitoring Engine (NON-LLM)
Computes business health KPIs for dashboard consumption.
Returns compact, structured JSON suitable for frontend visualizations.
"""
import pandas as pd
from datetime import datetime, timedelta
from ..data_access.revenue_data import compute_revenue_kpis, supporting_signals
from ..data_access.crm_data import _load_customers
from ..data_access.erp_data import compute_finance_kpis, payment_cycle_health
from ..data_access.inventory_data import compute_inventory_kpis, low_stock_alerts


def compute_monitoring_snapshot():
    """
    Compute all dashboard KPIs in one call.
    Returns a structured dict with metrics and status flags.
    """
    # Revenue
    revenue_kpis = compute_revenue_kpis()
    revenue_change_pct = revenue_kpis.get("revenue_change_pct", 0.0)
    current_revenue = revenue_kpis.get("current_revenue", 0.0)
    
    # Customer health
    customers_df = _load_customers()
    total_customers = len(customers_df)
    cutoff = datetime.now() - timedelta(days=30)
    inactive_count = len(customers_df[customers_df["last_order_date"] < cutoff])
    inactive_pct = (inactive_count / total_customers * 100) if total_customers > 0 else 0.0
    churn_rate_pct = inactive_pct  # proxy for churn
    
    # Finance
    finance_kpis = compute_finance_kpis()
    payment_health = payment_cycle_health()
    outstanding_cash = payment_health.get("overdue_amount", 0.0)
    overdue_invoices = payment_health.get("overdue_invoices", 0)
    total_spend = finance_kpis.get("total_spend", 0.0)
    overdue_pct = (outstanding_cash / total_spend * 100) if total_spend > 0 else 0.0
    
    # Inventory
    inventory_kpis = compute_inventory_kpis()
    low_stock = low_stock_alerts()
    low_stock_count = len(low_stock)
    days_inventory = inventory_kpis.get("days_inventory", 0.0)
    
    # Status flags (business stress indicators)
    high_churn = churn_rate_pct > 50  # more than half inactive
    cash_crunch = overdue_pct > 15 or outstanding_cash > 10_000_000
    inventory_crisis = low_stock_count > 10 or days_inventory > 45
    revenue_alert = revenue_change_pct < -10  # >10% drop
    
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "metrics": {
            "revenue": {
                "current_revenue": round(current_revenue, 2),
                "revenue_change_pct": round(revenue_change_pct, 2),
                "alert": revenue_alert
            },
            "customers": {
                "total_customers": total_customers,
                "inactive_count": inactive_count,
                "churn_rate_pct": round(churn_rate_pct, 2),
                "alert": high_churn
            },
            "finance": {
                "outstanding_cash_amount": round(outstanding_cash, 2),
                "overdue_invoices": overdue_invoices,
                "overdue_pct": round(overdue_pct, 2),
                "alert": cash_crunch
            },
            "inventory": {
                "low_stock_item_count": low_stock_count,
                "days_inventory": round(days_inventory, 2),
                "alert": inventory_crisis
            }
        },
        "status": {
            "high_churn": high_churn,
            "cash_crunch": cash_crunch,
            "inventory_crisis": inventory_crisis,
            "revenue_alert": revenue_alert,
            "overall_health": "CRITICAL" if (high_churn or cash_crunch or revenue_alert) else "WARNING" if inventory_crisis else "HEALTHY"
        }
    }


def get_average_order_value():
    """Compute AOV from invoice data."""
    from ..data_access.erp_data import _load_invoices
    invoices = _load_invoices()
    if invoices.empty:
        return 0.0
    return float(invoices["invoice_amount"].mean())
