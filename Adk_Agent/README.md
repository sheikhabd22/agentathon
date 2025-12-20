# AI-Powered Digital Business Analyst (Google ADK)

An intelligent business copilot that integrates fragmented data systems (CRM, ERP, inventory, revenue) and provides **real-time KPI monitoring, anomaly detection, causal reasoning, and actionable recommendations**.

## Features

✅ **Data Integration**: CSV connectors (extensible to Salesforce, Shopify, SAP, Odoo via REST/GraphQL adapters)

✅ **KPI Monitoring**: Real-time computation of revenue trends, customer metrics, inventory health, payment cycles

✅ **Anomaly Detection**: Flags deviations automatically (revenue drops, payment delays, low stock, churn signals)

✅ **Causal Reasoning**: Explains "why" metrics changed, not just "what"—e.g., "Revenue dropped 15% because orders fell 18% week-over-week"

✅ **Natural Language Interface**: Ask questions like *"Why did sales fall last week?"* and get data-backed explanations

✅ **Persistent Memory**: Stores insights, user preferences, and learns priorities over time

✅ **What-If Scenarios**: Simulates business interventions (pricing changes, marketing spend) to forecast impact

✅ **Explainability**: Natural language summaries with confidence levels and prioritized recommendations

## Project Structure

```
Adk-Agent/
├── agent/                 # Root agent and conversation logic
│   └── agent.py          # Main ADK agent with tools registry
├── tools/                # ADK tools for each domain
│   ├── revenue_tools.py  # Revenue & sales analytics
│   ├── crm_tools.py      # Customer insights
│   ├── erp_tools.py      # Finance & payment cycles
│   ├── inventory_tools.py # Stock & supply chain
│   ├── preferences_tools.py # User preferences
│   └── insights_tools.py # Memory retrieval
├── data_access/          # Data layer (CSV to unified models)
│   ├── revenue_data.py
│   ├── crm_data.py
│   ├── erp_data.py
│   └── inventory_data.py
├── services/             # Business logic & integrations
│   ├── memory.py         # Persistent insights & preferences
│   ├── connectors.py     # API adapters (CSV, Salesforce, Shopify, SAP, Odoo)
│   ├── models.py         # Unified semantic models (Customer360, Order360, etc.)
│   ├── causal_inference.py # Causal graphs & what-if simulator
├── data/                 # Sample CSV data
│   ├── customers.csv
│   ├── orders.csv
│   └── sales.csv
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Setup

### Prerequisites
- Python 3.9+
- Google ADK framework
- Pandas, Requests

### Installation

1. **Clone and navigate:**
   ```bash
   cd F:\Agentathon\Adk-Agent
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Agent

### Interactive Chat Mode

```bash
adk web
```

Then open your browser to `http://localhost:8080` and chat with the agent.

### Direct Testing

```bash
python -c "
from agent.agent import root_agent
response = root_agent.run('Why did revenue decline last week?')
print(response)
"
```

## Example Queries

- **Revenue Analysis**: *"What's our revenue trend? Any anomalies?"*
- **Customer Health**: *"Which customer segments are inactive?"*
- **Finance Check**: *"How many overdue invoices do we have?"*
- **Inventory**: *"Are we low on any critical products?"*
- **Causal Reasoning**: *"Revenue dropped 15%—what's the root cause?"*
- **What-If**: *"What if we reduce prices by 10%?"*
- **Memory**: *"Show me recent insights on revenue"*

## Architecture Highlights

### 1. **Data Connectors** (`services/connectors.py`)
- **CSVConnector**: Local CSV files (default for demo)
- **SalesforceConnector**: Placeholder for Salesforce CRM API
- **ShopifyConnector**: Placeholder for Shopify e-commerce API
- **SchemaMapper**: Normalizes heterogeneous data into unified models

### 2. **Unified Models** (`services/models.py`)
- `Customer360`: Full customer profile with lifecycle status, LTV, engagement scores
- `Order360`: Complete order context (customer, items, payment, fulfillment status)
- `Invoice360`: Payment tracking and aging
- `Product360`: Inventory and sales performance

### 3. **Memory System** (`services/memory.py`)
- Persistent JSON store (`data/memory.json`) for insights and preferences
- Adaptive learning: system learns user priorities (e.g., "focus on cash flow on Fridays")
- Historical insight retrieval for trend analysis

### 4. **Causal Inference** (`services/causal_inference.py`)
- Simple causal graphs: revenue ← order count, spend ← customer activity
- What-if scenario simulator with elasticity models
- Prioritized action recommender across domains

### 5. **ADK Tools Integration**
- Each domain (revenue, CRM, ERP, inventory) exposes an ADK `@tool`
- Tools compute KPIs, detect anomalies, attach natural-language explanations, and persist insights to memory
- Agent orchestrates tools via LLM-powered reasoning

## Extensibility

### Add a New Connector
1. Subclass `DataConnector` in `services/connectors.py`
2. Implement `fetch_customers()`, `fetch_orders()`, etc.
3. Call `set_connector()` in agent initialization

**Example: Odoo ERP**
```python
class OdooConnector(DataConnector):
    def __init__(self, api_url: str, api_token: str):
        self.api_url = api_url
        self.api_token = api_token
    
    def fetch_customers(self):
        # Call Odoo REST API
        response = requests.get(
            f"{self.api_url}/res.partner",
            headers={"Authorization": f"Bearer {self.api_token}"}
        )
        return [SchemaMapper.normalize_customer(c) for c in response.json()]
```

### Add a New KPI or Metric
1. Add logic to `data_access/<domain>_data.py`
2. Create or extend a tool in `tools/<domain>_tools.py`
3. Register tool in `agent/agent.py`

## Future Enhancements

- [ ] Real-time streaming ingestion (Kafka, Pub/Sub)
- [ ] Advanced causal inference (causal forests, graphical models)
- [ ] Multi-step reinforcement learning for optimal recommendations
- [ ] Fine-tuned LLM for finance & business terminology
- [ ] Role-based alerts (CEO vs. inventory manager)
- [ ] Export insights to Tableau, Power BI dashboards
- [ ] Scheduled reports and bulk recommendations

## Support & Development

For questions or improvements, extend `services/` modules and register new tools in the agent. Maintain data integrity by validating all connector outputs against unified models.

---

**Status**: MVP with CSV data; ready for Salesforce/Shopify/SAP integration.
