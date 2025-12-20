from google.adk.tools.function_tool import FunctionTool
from ..services.memory import recent_insights

def _recent_insights_tool(limit: int = 10):
    """Fetch recent insights logged by the agent across domains."""
    return recent_insights(limit)

recent_insights_tool = FunctionTool(_recent_insights_tool)
