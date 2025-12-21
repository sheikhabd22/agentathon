# FastAPI Backend - API Documentation

## Quick Start

### Install Dependencies
```bash
pip install fastapi uvicorn pydantic
```

### Run the Server
```bash
cd F:/Agentathon
python Adk_Agent/api/fastapi_backend.py
```

Server will start on **http://localhost:8001**

### Access Interactive Docs
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

---

## Primary Endpoints (Frontend-Facing)

### 1. Agent Conversation
**Endpoint**: `POST /agent/query`

**Purpose**: Interactive chat with the AI agent

**Request**:
```json
{
  "question": "How is our revenue performing?",
  "session_id": "optional-session-id"
}
```

**Response**:
```json
{
  "text": "Revenue is up 103.23% compared to last period...",
  "visuals": [
    {
      "type": "KPI",
      "title": "Revenue",
      "data": {
        "value": 108836.0,
        "unit": "$",
        "change_pct": 103.23
      },
      "status": "positive"
    }
  ]
}
```

**Test with cURL**:
```bash
curl -X POST http://localhost:8001/agent/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me our business health"}'
```

---

### 2. Monitoring Dashboard
**Endpoint**: `GET /monitoring/overview`

**Purpose**: Real-time business health for dashboards (non-chat)

**Response**:
```json
{
  "summary": {
    "timestamp": "2025-12-21T...",
    "revenue": {
      "current_revenue": 108836.0,
      "revenue_change_pct": 103.23,
      "alert": false
    },
    "customers": {
      "total_customers": 20000,
      "churn_rate_pct": 100.0,
      "alert": true
    },
    "overall_health": "CRITICAL"
  },
  "signals": {
    "high_churn": true,
    "cash_crunch": true,
    "inventory_crisis": false,
    "revenue_alert": false
  }
}
```

**Test**:
```bash
curl http://localhost:8001/monitoring/overview | python -m json.tool
```

---

### 3. Risks Overview
**Endpoint**: `GET /risks`

**Purpose**: Active and historical business risks

**Response**:
```json
{
  "active_risks": [
    {
      "risk_id": "CUSTOMER_2025-12-21...",
      "risk_type": "CUSTOMER",
      "description": "100% of customers are inactive...",
      "severity": "HIGH",
      "status": "ACTIVE",
      "timestamp": "2025-12-21T..."
    }
  ],
  "historical_risks": []
}
```

**Test**:
```bash
curl http://localhost:8001/risks | python -m json.tool
```

---

## Legacy Endpoints (Backward Compatibility)

All previous Flask endpoints are preserved under `/api/*`:

- `GET /api/monitoring` - Full monitoring snapshot
- `GET /api/risks/active` - Active risks
- `GET /api/risks/historical` - Historical risks
- `POST /api/risks/generate` - Generate new risks
- `POST /api/risks/resolve/:id` - Resolve a risk
- `GET /api/health` - Health check

---

## Visualization Specs

### Supported Visual Types

#### 1. KPI
Single metric with status indicator
```json
{
  "type": "KPI",
  "title": "Revenue",
  "data": {
    "value": 108836.0,
    "unit": "$",
    "change_pct": 103.23
  },
  "status": "positive"
}
```

#### 2. BAR
Category comparisons
```json
{
  "type": "BAR",
  "title": "Revenue by Segment",
  "data": {
    "categories": ["Enterprise", "SMB", "Mid-Market"],
    "values": [50000, 30000, 20000],
    "unit": "$"
  }
}
```

#### 3. TREND
Time-based changes
```json
{
  "type": "TREND",
  "title": "Revenue Over Time",
  "data": {
    "dates": ["2025-12-01", "2025-12-08", "2025-12-15"],
    "values": [95000, 102000, 108836],
    "unit": "$"
  }
}
```

#### 4. RISK_LIST
Risk summaries
```json
{
  "type": "RISK_LIST",
  "title": "Active Risks",
  "data": {
    "risks": [
      {
        "description": "High customer churn detected",
        "severity": "HIGH",
        "type": "CUSTOMER",
        "timestamp": "2025-12-21T..."
      }
    ]
  }
}
```

---

## Architecture

```
Frontend
    ↓
FastAPI Backend (Port 8001)
    ↓
├─→ Agent (Gemini LLM + Tools)
├─→ Monitoring Engine (Deterministic)
├─→ Risk Engine (Generation + Storage)
└─→ Memory System (Persistent)
    ↓
Data Access Layer
    ↓
XLSX Datasets (70K+ records)
```

---

## Integration Example (JavaScript)

```javascript
// Agent conversation
async function askAgent(question) {
  const response = await fetch('http://localhost:8001/agent/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  });
  const data = await response.json();
  
  // Display text
  console.log(data.text);
  
  // Render visuals
  if (data.visuals) {
    data.visuals.forEach(visual => {
      renderVisualization(visual);
    });
  }
}

// Monitoring dashboard
async function loadDashboard() {
  const response = await fetch('http://localhost:8001/monitoring/overview');
  const data = await response.json();
  
  updateDashboard(data.summary);
  showAlerts(data.signals);
}

// Risks page
async function loadRisks() {
  const response = await fetch('http://localhost:8001/risks');
  const data = await response.json();
  
  displayRisks(data.active_risks, 'active');
  displayRisks(data.historical_risks, 'historical');
}
```

---

## Environment Setup

Ensure `.env` file has API key:
```
GOOGLE_API_KEY=your-gemini-api-key
```

---

## Comparison: Flask vs FastAPI

| Feature | Flask (Port 5000) | FastAPI (Port 8001) |
|---------|-------------------|---------------------|
| Agent Conversation | ❌ No | ✅ `/agent/query` |
| Monitoring | ✅ `/api/monitoring` | ✅ `/monitoring/overview` |
| Risks | ✅ `/api/risks/*` | ✅ `/risks` |
| Visualization Specs | ❌ No | ✅ Yes |
| Interactive Docs | ❌ No | ✅ `/docs` |
| Type Safety | ❌ No | ✅ Pydantic models |

**Recommendation**: Use **FastAPI (8001)** for new frontends. Flask endpoints remain for backward compatibility.
