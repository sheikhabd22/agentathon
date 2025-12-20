from google.adk import Agent
from config import MODEL_NAME
from tools import (
    revenue_health,
    customer_health,
    finance_health,
    inventory_health
)

bi_agent = Agent(
    name="AgenticBusinessIntelligenceCopilot",
    model=MODEL_NAME,
    tools=[
        revenue_health,
        customer_health,
        finance_health,
        inventory_health
    ],
    system_prompt="""
You are a senior Business Intelligence Analyst AI.

Behave like a human analyst:
- Speak naturally
- Explain insights clearly
- Avoid rigid templates
- Be honest when data is insufficient
"""
)
