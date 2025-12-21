"""
FastAPI Backend for Agentic BI Copilot
Orchestration and delivery layer for frontend consumption.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from Adk_Agent.services.monitoring_engine import compute_monitoring_snapshot, get_average_order_value
from Adk_Agent.services.risk_engine import (
    generate_risks_from_monitoring,
    store_risks,
    get_active_risks,
    get_historical_risks,
    get_all_risks,
    resolve_risk,
    auto_resolve_stale_risks
)
from Adk_Agent.services.memory import log_insight, recent_insights, get_preferences
from Adk_Agent.services.visualization import create_agent_response


app = FastAPI(
    title="Agentic BI Copilot API",
    description="FastAPI backend for Business Intelligence Copilot with AI agent",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================
# REQUEST/RESPONSE MODELS
# ========================

class AgentQueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None


class AgentQueryResponse(BaseModel):
    text: str
    visuals: Optional[List[Dict[str, Any]]] = None


class MonitoringOverviewResponse(BaseModel):
    summary: Dict[str, Any]
    signals: Dict[str, Any]


class RisksResponse(BaseModel):
    active_risks: List[Dict[str, Any]]
    historical_risks: List[Dict[str, Any]]


# ========================
# AGENT CONVERSATION ENDPOINT
# ========================

@app.post("/agent/query", response_model=AgentQueryResponse)
async def agent_query(request: AgentQueryRequest):
    """
    Handle conversational agent interaction.
    
    Passes user question to the agent, which invokes tools and generates
    natural language response with optional visualization specs.
    """
    try:
        # Lazy import to avoid circular dependencies
        from Adk_Agent.agent.agent import root_agent
        from Adk_Agent.services.visualization import should_visualize
        
        question = request.question
        
        # Invoke the agent
        # Note: ADK agent returns response via its run method
        # For now, we'll provide a wrapper that calls the agent
        # and formats the response appropriately
        
        # Call the agent (this will use tools internally)
        response = root_agent.run(question)
        
        # Extract text response
        if hasattr(response, 'text'):
            text_response = response.text
        elif isinstance(response, str):
            text_response = response
        else:
            text_response = str(response)
        
        # For MVP, we'll return text-only response
        # Advanced: Parse agent's tool usage to generate visualization specs
        result = create_agent_response(text=text_response)
        
        # Log the interaction to memory
        log_insight("conversation", {
            "question": question,
            "response_preview": text_response[:200] if len(text_response) > 200 else text_response
        })
        
        return AgentQueryResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent query failed: {str(e)}")


# ========================
# MONITORING DASHBOARD ENDPOINT
# ========================

@app.get("/monitoring/overview", response_model=MonitoringOverviewResponse)
async def monitoring_overview():
    """
    Retrieve current business health snapshot for dashboard.
    
    Non-chat endpoint - pure monitoring data without LLM involvement.
    Designed for periodic refresh in frontend.
    """
    try:
        snapshot = compute_monitoring_snapshot()
        
        # Extract summary metrics
        summary = {
            "timestamp": snapshot.get("timestamp"),
            "revenue": snapshot["metrics"]["revenue"],
            "customers": snapshot["metrics"]["customers"],
            "finance": snapshot["metrics"]["finance"],
            "inventory": snapshot["metrics"]["inventory"],
            "overall_health": snapshot["status"]["overall_health"]
        }
        
        # Extract health signals/flags
        signals = snapshot["status"]
        
        return MonitoringOverviewResponse(
            summary=summary,
            signals=signals
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Monitoring failed: {str(e)}")


# ========================
# RISKS ENDPOINT
# ========================

@app.get("/risks", response_model=RisksResponse)
async def get_risks():
    """
    Retrieve active and historical business risks.
    
    Powers the Risks page with severity, timestamps, and status.
    """
    try:
        active = get_active_risks()
        historical = get_historical_risks()
        
        return RisksResponse(
            active_risks=active,
            historical_risks=historical
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risks retrieval failed: {str(e)}")


# ========================
# ADDITIONAL ENDPOINTS (Legacy/Admin)
# ========================

@app.get("/api/monitoring")
async def legacy_monitoring():
    """Legacy endpoint - full monitoring snapshot."""
    try:
        return compute_monitoring_snapshot()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/risks/active")
async def legacy_active_risks():
    """Legacy endpoint - active risks only."""
    try:
        risks = get_active_risks()
        return {"risks": risks, "count": len(risks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/risks/historical")
async def legacy_historical_risks():
    """Legacy endpoint - historical risks."""
    try:
        risks = get_historical_risks()
        return {"risks": risks, "count": len(risks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/risks/all")
async def legacy_all_risks():
    """Legacy endpoint - all risks."""
    try:
        risks = get_all_risks()
        return {"risks": risks, "count": len(risks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/risks/generate")
async def legacy_generate_risks():
    """Legacy endpoint - generate risks from monitoring."""
    try:
        snapshot = compute_monitoring_snapshot()
        new_risks = generate_risks_from_monitoring(snapshot)
        store_risks(new_risks)
        return {
            "message": f"Generated {len(new_risks)} new risks",
            "risks": new_risks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/risks/resolve/{risk_id}")
async def legacy_resolve_risk(risk_id: str):
    """Legacy endpoint - resolve a risk."""
    try:
        resolve_risk(risk_id)
        return {"message": f"Risk {risk_id} resolved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/risks/auto-resolve")
async def legacy_auto_resolve():
    """Legacy endpoint - auto-resolve stale risks."""
    try:
        auto_resolve_stale_risks()
        return {"message": "Stale risks auto-resolved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics/aov")
async def legacy_aov():
    """Legacy endpoint - average order value."""
    try:
        aov = get_average_order_value()
        return {"average_order_value": round(aov, 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Agentic BI Copilot",
        "version": "1.0.0",
        "backend": "FastAPI"
    }


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "service": "Agentic BI Copilot API",
        "version": "1.0.0",
        "endpoints": {
            "agent": "POST /agent/query",
            "monitoring": "GET /monitoring/overview",
            "risks": "GET /risks",
            "health": "GET /api/health"
        },
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Agentic BI Copilot FastAPI Backend")
    print("📊 Endpoints:")
    print("   POST /agent/query          - Conversational agent interaction")
    print("   GET  /monitoring/overview  - Business health dashboard")
    print("   GET  /risks                - Active and historical risks")
    print("   GET  /api/health           - Health check")
    print("   GET  /docs                 - Interactive API documentation")
    print("\n🌐 Server running on http://localhost:8001")
    
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
