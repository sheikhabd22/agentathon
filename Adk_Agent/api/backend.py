"""
Backend API Layer for Monitoring Dashboard and Risks
Exposes HTTP endpoints independent of the chat agent.
Uses Flask for simplicity.
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
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

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend


@app.route("/api/monitoring", methods=["GET"])
def monitoring_endpoint():
    """
    Returns current business health snapshot for dashboard.
    No LLM involved - pure deterministic KPIs.
    """
    try:
        snapshot = compute_monitoring_snapshot()
        return jsonify(snapshot), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/risks/active", methods=["GET"])
def active_risks_endpoint():
    """Returns all active risks."""
    try:
        risks = get_active_risks()
        return jsonify({"risks": risks, "count": len(risks)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/risks/historical", methods=["GET"])
def historical_risks_endpoint():
    """Returns all resolved/historical risks."""
    try:
        risks = get_historical_risks()
        return jsonify({"risks": risks, "count": len(risks)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/risks/all", methods=["GET"])
def all_risks_endpoint():
    """Returns all risks (active + historical)."""
    try:
        risks = get_all_risks()
        return jsonify({"risks": risks, "count": len(risks)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/risks/generate", methods=["POST"])
def generate_risks_endpoint():
    """
    Manually trigger risk generation from current monitoring snapshot.
    Stores generated risks.
    """
    try:
        snapshot = compute_monitoring_snapshot()
        new_risks = generate_risks_from_monitoring(snapshot)
        store_risks(new_risks)
        return jsonify({
            "message": f"Generated {len(new_risks)} new risks",
            "risks": new_risks
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/risks/resolve/<risk_id>", methods=["POST"])
def resolve_risk_endpoint(risk_id):
    """Mark a specific risk as resolved."""
    try:
        resolve_risk(risk_id)
        return jsonify({"message": f"Risk {risk_id} resolved"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/risks/auto-resolve", methods=["POST"])
def auto_resolve_endpoint():
    """Auto-resolve stale risks based on monitoring state."""
    try:
        max_age = request.json.get("max_age_hours", 48) if request.json else 48
        auto_resolve_stale_risks(max_age_hours=max_age)
        return jsonify({"message": "Stale risks auto-resolved"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/metrics/aov", methods=["GET"])
def aov_endpoint():
    """Returns average order value."""
    try:
        aov = get_average_order_value()
        return jsonify({"average_order_value": round(aov, 2)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "healthy", "service": "BI Copilot Backend"}), 200


if __name__ == "__main__":
    print("Starting BI Copilot Backend API on http://localhost:5000")
    print("Endpoints:")
    print("  GET  /api/monitoring        - Dashboard KPIs")
    print("  GET  /api/risks/active      - Active risks")
    print("  GET  /api/risks/historical  - Historical risks")
    print("  GET  /api/risks/all         - All risks")
    print("  POST /api/risks/generate    - Generate risks from current state")
    print("  POST /api/risks/resolve/:id - Resolve a risk")
    print("  POST /api/risks/auto-resolve- Auto-resolve stale risks")
    print("  GET  /api/metrics/aov       - Average order value")
    print("  GET  /api/health            - Health check")
    app.run(host="0.0.0.0", port=5000, debug=True)
