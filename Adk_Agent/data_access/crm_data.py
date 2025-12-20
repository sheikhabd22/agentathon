import pandas as pd
from datetime import datetime
from collections import Counter
from ..services.path_utils import get_data_dir

DATA_DIR = get_data_dir()


def _load_customers():
    path = DATA_DIR / "crm_customers_20000.xlsx"
    if not path.exists():
        raise FileNotFoundError(f"Missing data file: {path}")
    df = pd.read_excel(path)
    df["last_order_date"] = pd.to_datetime(df.get("last_order_date"), errors="coerce")
    df["signup_date"] = pd.to_datetime(df.get("signup_date"), errors="coerce")
    df["lifetime_value"] = pd.to_numeric(df.get("lifetime_value"), errors="coerce").fillna(0)
    df = df.dropna(subset=["customer_id", "customer_name"])
    return df


def inactive_customers(days=30):
    customers_df = _load_customers()
    cutoff = datetime.now() - pd.Timedelta(days=days)
    inactive = customers_df[customers_df["last_order_date"] < cutoff]
    return inactive.to_dict("records")


def segment_summary(customers):
    return dict(Counter(c.get("segment", "Unknown") for c in customers))


def top_customers(n=5):
    df = _load_customers()
    return df.sort_values("lifetime_value", ascending=False).head(n).to_dict("records")
