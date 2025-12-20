from google.adk.tools.function_tool import FunctionTool
from ..services.memory import get_preferences, set_preference

def _get_preferences_tool():
    """Return current user/business preferences stored in memory."""
    return get_preferences()

def _set_preferences_tool(key: str, value: str):
    """Update a preference (e.g., focus area, alert cadence)."""
    return set_preference(key, value)
get_preferences_tool = FunctionTool(_get_preferences_tool)
set_preferences_tool = FunctionTool(_set_preferences_tool)
