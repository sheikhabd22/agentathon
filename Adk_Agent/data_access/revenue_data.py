import pandas as pd
from ..services.path_utils import get_data_dir

DATA_DIR = get_data_dir()


def _load_invoices():
    path = DATA_DIR / "erp_invoices_22000.xlsx"
    if not path.exists():
        return pd.DataFrame({"invoice_date": [], "invoice_amount": []})
    df = pd.read_excel(path)
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
    df["invoice_amount"] = pd.to_numeric(df["invoice_amount"], errors="coerce").fillna(0)
    df = df.dropna(subset=["invoice_date"])
    return df


def _load_orders():
    path = DATA_DIR / "orders_25000.xlsx"
    if not path.exists():
        return pd.DataFrame({"order_date": [], "order_count": []})
    df = pd.read_excel(path)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])
    # Aggregate to daily order counts
    grouped = df.groupby(df["order_date"].dt.date).size().reset_index(name="order_count")
    grouped.rename(columns={"order_date": "date"}, inplace=True)
    grouped["date"] = pd.to_datetime(grouped["date"])
    return grouped.sort_values("date")


def _daily_revenue():
    invoices = _load_invoices()
    if invoices.empty:
        return pd.DataFrame({"date": [], "revenue": []})
    daily = (
        invoices
        .groupby(invoices["invoice_date"].dt.date)["invoice_amount"]
        .sum()
        .reset_index(name="revenue")
    )
    daily.rename(columns={"invoice_date": "date"}, inplace=True)
    daily["date"] = pd.to_datetime(daily["date"])
    return daily.sort_values("date")


def compute_revenue_kpis():
    revenue_df = _daily_revenue()

    if len(revenue_df) < 2:
        return {
            "current_revenue": 0.0,
            "previous_revenue": 0.0,
            "revenue_change_pct": 0.0,
        }

    current_row = revenue_df.iloc[-1]
    previous_row = revenue_df.iloc[-2]

    current = float(current_row["revenue"])
    previous = float(previous_row["revenue"]) if previous_row["revenue"] else 0.0
    change_pct = ((current - previous) / previous) * 100 if previous else 0.0

    return {
        "current_revenue": round(current, 2),
        "previous_revenue": round(previous, 2),
        "revenue_change_pct": round(change_pct, 2),
    }


def detect_revenue_anomaly(kpis):
    change = kpis.get("revenue_change_pct", 0.0)
    is_drop = change < -5  # flag moderate drop
    severity = (
        "HIGH" if change <= -15 else
        "MEDIUM" if change <= -8 else
        "LOW"
    )
    return {"is_anomaly": is_drop, "severity": severity}


def supporting_signals():
    """Return additional signals to aid causal analysis (e.g., order count)."""
    orders_df = _load_orders()
    if len(orders_df) < 2:
        return {"order_change_pct": 0.0}
    curr = float(orders_df.iloc[-1]["order_count"])
    prev = float(orders_df.iloc[-2]["order_count"]) if orders_df.iloc[-2]["order_count"] else 0.0
    change_pct = ((curr - prev) / prev) * 100 if prev else 0.0
    return {"order_change_pct": round(change_pct, 2)}
