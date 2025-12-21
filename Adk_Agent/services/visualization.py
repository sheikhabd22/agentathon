"""
Visualization Specification Generator
Provides structured visualization instructions for frontend rendering.
Agent generates specs, frontend renders actual visuals.
"""
from typing import Dict, List, Any, Optional, Literal

VisualType = Literal["KPI", "BAR", "TREND", "RISK_LIST"]
Status = Literal["positive", "warning", "negative"]


def create_kpi_visual(
    title: str,
    value: float,
    status: Status,
    unit: str = "",
    change_pct: Optional[float] = None
) -> Dict[str, Any]:
    """
    Create a KPI visualization spec for single metrics.
    
    Args:
        title: Metric name (e.g., "Revenue")
        value: Current value
        status: positive | warning | negative
        unit: Optional unit (e.g., "$", "%")
        change_pct: Optional percentage change
    """
    visual = {
        "type": "KPI",
        "title": title,
        "data": {
            "value": value,
            "unit": unit
        },
        "status": status
    }
    
    if change_pct is not None:
        visual["data"]["change_pct"] = change_pct
    
    return visual


def create_bar_visual(
    title: str,
    categories: List[str],
    values: List[float],
    unit: str = ""
) -> Dict[str, Any]:
    """
    Create a BAR chart spec for category comparisons.
    
    Args:
        title: Chart title
        categories: Category labels
        values: Corresponding values
        unit: Optional unit
    """
    return {
        "type": "BAR",
        "title": title,
        "data": {
            "categories": categories,
            "values": values,
            "unit": unit
        }
    }


def create_trend_visual(
    title: str,
    dates: List[str],
    values: List[float],
    unit: str = ""
) -> Dict[str, Any]:
    """
    Create a TREND visualization spec for time-based changes.
    
    Args:
        title: Chart title
        dates: Date labels (ISO format or simple labels)
        values: Corresponding values
        unit: Optional unit
    """
    return {
        "type": "TREND",
        "title": title,
        "data": {
            "dates": dates,
            "values": values,
            "unit": unit
        }
    }


def create_risk_list_visual(
    title: str,
    risks: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Create a RISK_LIST visualization spec for risk summaries.
    
    Args:
        title: List title
        risks: List of risk objects with description, severity, timestamp
    """
    return {
        "type": "RISK_LIST",
        "title": title,
        "data": {
            "risks": [
                {
                    "description": r.get("description", ""),
                    "severity": r.get("severity", "MEDIUM"),
                    "timestamp": r.get("timestamp", ""),
                    "type": r.get("risk_type", "UNKNOWN")
                }
                for r in risks
            ]
        }
    }


def create_agent_response(
    text: str,
    visuals: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Create a structured agent response with optional visualizations.
    
    Args:
        text: Natural language explanation
        visuals: Optional list of visualization specs
    
    Returns:
        Structured response for frontend consumption
    """
    response = {"text": text}
    
    if visuals and len(visuals) > 0:
        response["visuals"] = visuals
    
    return response


def should_visualize(question: str) -> bool:
    """
    Heuristic to determine if a question warrants visualization.
    
    Returns True if question asks about metrics, trends, comparisons, or risks.
    """
    question_lower = question.lower()
    
    visual_keywords = [
        "revenue", "sales", "customer", "churn", "trend", "change",
        "compare", "performance", "metrics", "risk", "health",
        "inventory", "finance", "overdue", "growth", "decline"
    ]
    
    return any(keyword in question_lower for keyword in visual_keywords)
