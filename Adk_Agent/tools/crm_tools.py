from google.adk.tools.function_tool import FunctionTool
from ..data_access.crm_data import inactive_customers, segment_summary, top_customers
from ..services.memory import log_insight

def _customer_health(days: int = 30):
    """
    Returns customer inactivity and segment distribution, plus top customers.
    """
    customers = inactive_customers(days=days)
    segments = segment_summary(customers)
    top = top_customers(5)

    insight = {
        "inactive_count": len(customers),
        "segment_distribution": segments,
        "top_customers": top,
    }

    log_insight("customers", insight)
    return insight

customer_health = FunctionTool(_customer_health)
