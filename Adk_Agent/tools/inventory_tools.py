from google.adk.tools.function_tool import FunctionTool
from ..data_access.inventory_data import (
    compute_inventory_kpis,
    detect_inventory_anomaly,
    low_stock_alerts,
)
from ..services.memory import log_insight

def _inventory_health():
    """
    Provides inventory health metrics and alerts.
    - Inventory turnover rate
    - Days inventory outstanding
    - Low stock warnings for critical SKUs
    """
    kpis = compute_inventory_kpis()
    anomaly = detect_inventory_anomaly(kpis)
    low_stock = low_stock_alerts()

    explanation = []
    explanation.append(
        f"Inventory turnover: {kpis['inventory_turnover_rate']} times/year. "
        f"Days inventory: {kpis['days_inventory']} days."
    )
    if low_stock:
        sku_list = ", ".join(s["sku"] for s in low_stock)
        explanation.append(f"Low stock alerts for: {sku_list}")

    recs = []
    if low_stock:
        recs.append("Immediately reorder low-stock SKUs to prevent stockouts.")
        recs.append("Review demand forecasts to adjust safety stock levels.")
    else:
        recs.append("Inventory levels appear adequate; maintain monitoring.")

    insight = {
        "kpis": kpis,
        "anomaly": anomaly,
        "low_stock_skus": low_stock,
        "explanation": " ".join(explanation),
        "recommendations": recs,
    }

    log_insight("inventory", insight)
    return insight

inventory_health = FunctionTool(_inventory_health)
