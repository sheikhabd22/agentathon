import pandas as pd
from datetime import datetime, timedelta
from ..services.path_utils import get_data_dir

DATA_DIR = get_data_dir()


def _load_customers():
    path = DATA_DIR / "crm_customers_20000.xlsx"
    if not path.exists():
        return pd.DataFrame({"customer_id": [], "customer_name": [], "segment": [], "last_order_date": [], "lifetime_value": []})
    df = pd.read_excel(path)
    df["last_order_date"] = pd.to_datetime(df.get("last_order_date"), errors="coerce")
    df["lifetime_value"] = pd.to_numeric(df.get("lifetime_value"), errors="coerce").fillna(0)
    return df


def _load_invoices():
    path = DATA_DIR / "erp_invoices_22000.xlsx"
    if not path.exists():
        return pd.DataFrame({"invoice_date": [], "invoice_amount": [], "payment_status": [], "due_date": []})
    df = pd.read_excel(path)
    df["invoice_date"] = pd.to_datetime(df.get("invoice_date"), errors="coerce")
    df["due_date"] = pd.to_datetime(df.get("due_date"), errors="coerce")
    df["invoice_amount"] = pd.to_numeric(df.get("invoice_amount"), errors="coerce").fillna(0)
    df = df.dropna(subset=["invoice_date"])
    return df


def compute_finance_kpis():
    """Compute finance and payment health metrics using invoice data."""
    customers_df = _load_customers()
    invoices_df = _load_invoices()

    if invoices_df.empty:
        return {
            "total_spend": 0.0,
            "avg_spend_per_customer": 0.0,
            "revenue_last_week": 0.0,
            "weekly_cash_flow_avg": 0.0,
        }

    total_invoice_amount = invoices_df["invoice_amount"].sum()
    spend_per_customer = invoices_df.groupby("customer_id")["invoice_amount"].sum()
    avg_spend_per_customer = spend_per_customer.mean() if not spend_per_customer.empty else 0.0

    most_recent_date = invoices_df["invoice_date"].max()
    week_start = most_recent_date - timedelta(days=7)
    last_week_revenue = invoices_df[invoices_df["invoice_date"] >= week_start]["invoice_amount"].sum()

    recent_window = invoices_df[invoices_df["invoice_date"] >= week_start]
    if recent_window.empty:
        weekly_avg = last_week_revenue
    else:
        daily_avg = (
            recent_window
            .groupby(recent_window["invoice_date"].dt.date)["invoice_amount"]
            .sum()
            .mean()
        )
        weekly_avg = daily_avg * 7

    return {
        "total_spend": float(round(total_invoice_amount, 2)),
        "avg_spend_per_customer": float(round(avg_spend_per_customer, 2)),
        "revenue_last_week": float(round(last_week_revenue, 2)),
        "weekly_cash_flow_avg": float(round(weekly_avg, 2)),
    }


def detect_finance_anomaly(kpis):
    """Flag finance anomalies relative to weekly average."""
    baseline = kpis.get("weekly_cash_flow_avg", 0) or 0
    last_week = kpis.get("revenue_last_week", 0)
    is_anomaly = baseline > 0 and last_week < 0.8 * baseline
    severity = "HIGH" if baseline > 0 and last_week < 0.6 * baseline else "MEDIUM" if is_anomaly else "LOW"
    return {"is_anomaly": is_anomaly, "severity": severity}


def payment_cycle_health():
    """Return payment cycle metrics derived from invoice terms."""
    invoices_df = _load_invoices()
    if invoices_df.empty:
        return {"avg_days_to_payment": 0.0, "overdue_invoices": 0, "overdue_amount": 0.0}

    term_days = (invoices_df["due_date"] - invoices_df["invoice_date"]).dt.days
    avg_days = term_days[term_days >= 0].mean() if not term_days.empty else 0.0

    overdue_mask = invoices_df["payment_status"].str.contains("Overdue", case=False, na=False)
    overdue_df = invoices_df[overdue_mask]
    overdue_amount = overdue_df["invoice_amount"].sum() if not overdue_df.empty else 0.0

    return {
        "avg_days_to_payment": float(round(avg_days or 0.0, 2)),
        "overdue_invoices": int(len(overdue_df)),
        "overdue_amount": float(round(overdue_amount, 2)),
    }
