import pandas as pd
from datetime import datetime
from collections import Counter

customers_df = pd.read_excel("data/crm_customers_20000.xlsx")
orders_df = pd.read_excel("data/orders_25000.xlsx")
invoices_df = pd.read_excel("data/erp_invoices_22000.xlsx")
products_df = pd.read_excel("data/inventory_products_3000.xlsx")


# -------- REVENUE --------

def compute_revenue_kpis():
    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])

    last_week = orders_df["order_date"].max() - pd.Timedelta(days=7)
    prev_week = last_week - pd.Timedelta(days=7)

    current = orders_df[orders_df["order_date"] >= last_week]["order_value"].sum()
    previous = orders_df[
        (orders_df["order_date"] >= prev_week) &
        (orders_df["order_date"] < last_week)
    ]["order_value"].sum()

    change_pct = ((current - previous) / previous) * 100 if previous else 0

    return {
        "current_revenue": round(current, 2),
        "previous_revenue": round(previous, 2),
        "revenue_change_pct": round(change_pct, 2)
    }


def detect_revenue_anomaly(kpis):
    return {
        "is_anomaly": kpis["revenue_change_pct"] < -10,
        "severity": "HIGH" if kpis["revenue_change_pct"] < -15 else "MEDIUM"
    }


# -------- CRM --------

def inactive_customers(days=30):
    customers_df["last_order_date"] = pd.to_datetime(customers_df["last_order_date"])
    cutoff = datetime.now() - pd.Timedelta(days=days)
    inactive = customers_df[customers_df["last_order_date"] < cutoff]
    return inactive[["customer_id", "segment", "lifetime_value"]].to_dict("records")


def customer_segment_summary(customers):
    return dict(Counter(c["segment"] for c in customers))


# -------- ERP --------

def overdue_invoice_summary():
    invoices_df["due_date"] = pd.to_datetime(invoices_df["due_date"])
    overdue = invoices_df[
        (invoices_df["payment_status"] != "PAID") &
        (invoices_df["due_date"] < datetime.now())
    ]
    return {
        "overdue_count": len(overdue),
        "overdue_amount": round(overdue["invoice_amount"].sum(), 2)
    }


# -------- INVENTORY --------

def inventory_risk_summary():
    low = products_df[
        products_df["stock_level"] < products_df["reorder_threshold"]
    ]
    return {
        "low_stock_products": len(low),
        "critical_categories": low["category"].value_counts().head(3).to_dict()
    }
