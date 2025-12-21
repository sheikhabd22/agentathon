# BI Copilot Backend API

## Quick Test Commands

### 1. Test monitoring snapshot
```bash
curl http://localhost:5000/api/monitoring | python -m json.tool
```

### 2. Generate risks from current state
```bash
curl -X POST http://localhost:5000/api/risks/generate | python -m json.tool
```

### 3. View active risks
```bash
curl http://localhost:5000/api/risks/active | python -m json.tool
```

### 4. View all risks
```bash
curl http://localhost:5000/api/risks/all | python -m json.tool
```

### 5. Auto-resolve stale risks
```bash
curl -X POST -H "Content-Type: application/json" -d "{\"max_age_hours\": 24}" http://localhost:5000/api/risks/auto-resolve | python -m json.tool
```

### 6. Get average order value
```bash
curl http://localhost:5000/api/metrics/aov | python -m json.tool
```

### 7. Health check
```bash
curl http://localhost:5000/api/health | python -m json.tool
```

## Running the Backend

```bash
cd F:/Agentathon
python Adk_Agent/api/backend.py
```

The backend will start on http://localhost:5000

## Architecture

- **Monitoring Engine**: Computes KPIs without LLM (deterministic)
- **Risk Engine**: Generates/stores/retrieves business risks
- **API Layer**: Flask endpoints for frontend consumption
- **Agent Tools**: LLM can access monitoring + risks for reasoning
