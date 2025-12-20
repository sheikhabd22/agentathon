import pandas as pd
from datetime import datetime
from ..services.path_utils import get_data_dir

DATA_DIR = get_data_dir()


def _load_orders():
    """Load order history from the larger orders XLSX."""
    path = DATA_DIR / "orders_25000.xlsx"
    if not path.exists():
        return pd.DataFrame({"date": [], "order_count": []})
    df = pd.read_excel(path)
    df["order_date"] = pd.to_datetime(df.get("order_date"), errors="coerce")
    df = df.dropna(subset=["order_date"])
    daily = df.groupby(df["order_date"].dt.date).size().reset_index(name="order_count")
    daily.rename(columns={"order_date": "date"}, inplace=True)
    daily["date"] = pd.to_datetime(daily["date"])
    return daily.sort_values("date")


def _load_products():
    path = DATA_DIR / "inventory_products_3000.xlsx"
    if not path.exists():
        return pd.DataFrame({"product_id": [], "stock_level": [], "reorder_threshold": []})
    df = pd.read_excel(path)
    df["stock_level"] = pd.to_numeric(df.get("stock_level"), errors="coerce").fillna(0)
    df["reorder_threshold"] = pd.to_numeric(df.get("reorder_threshold"), errors="coerce").fillna(0)
    return df


def compute_inventory_kpis():
    """
    Compute inventory health metrics from order velocity and current stock.
    """
    orders_df = _load_orders()
    products_df = _load_products()

    if len(orders_df) < 2 or products_df.empty:
        return {
            "avg_order_count": 0.0,
            "inventory_turnover_rate": 0.0,
            "days_inventory": 0.0,
        }

    avg_orders = orders_df["order_count"].mean()
    avg_stock = products_df["stock_level"].mean() or 0.0
    # Estimate days of cover assuming avg_orders per day demand
    days_inventory = (avg_stock / avg_orders) if avg_orders > 0 else float("inf")
    # Approximate annual turnover using demand vs. stock
    turnover_rate = ((avg_orders * 365) / avg_stock) if avg_stock > 0 else 0.0

    return {
        "avg_order_count": float(round(avg_orders, 2)),
        "inventory_turnover_rate": float(round(turnover_rate, 2)),
        "days_inventory": float(round(days_inventory if days_inventory != float("inf") else 0.0, 2)),
    }


def detect_inventory_anomaly(kpis):
    """Flag inventory anomalies based on days of cover."""
    days = kpis["days_inventory"]
    is_anomaly = days > 30  # stock sitting too long
    severity = "HIGH" if days > 45 else "MEDIUM" if days > 30 else "LOW"
    return {"is_anomaly": is_anomaly, "severity": severity}


def low_stock_alerts():
    """Return low-stock products based on reorder thresholds from the XLSX."""
    products_df = _load_products()
    if products_df.empty:
        return []

    low = products_df[products_df["stock_level"] <= products_df["reorder_threshold"]]
    if low.empty:
        return []

    alerts = []
    for _, row in low.head(10).iterrows():  # cap to keep response concise
        alerts.append({
            "sku": row.get("product_id"),
            "current_qty": float(row.get("stock_level", 0)),
            "reorder_point": float(row.get("reorder_threshold", 0)),
        })
    return alerts
