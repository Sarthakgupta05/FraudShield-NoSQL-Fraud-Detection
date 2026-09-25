"""
Integration tests for FastAPI REST Endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from src.backend.app import app

client = TestClient(app)

def test_get_metrics_endpoint():
    response = client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_transactions" in data
    assert "risk_breakdown" in data
    assert "graph_intelligence" in data

def test_get_topology_endpoint():
    response = client.get("/api/graph/topology")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data

def test_create_transaction_endpoint():
    payload = {
        "sender_account": "API_ACC_1",
        "receiver_account": "API_ACC_2",
        "amount": 12500.0,
        "currency": "INR",
        "payment_type": "UPI_INSTANT",
        "device_telemetry": {
            "device_id": "DEV_API_99",
            "ip_address": "103.20.10.5",
            "device_fingerprint": "fp_test_hash"
        },
        "geospatial": {
            "lat": 12.9716,
            "lon": 77.5946,
            "city": "Bengaluru"
        }
    }
    response = client.post("/api/transactions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "transaction_id" in data
    assert "risk_evaluation" in data
    assert data["risk_evaluation"]["risk_score"] >= 0

def test_simulator_generate_endpoint():
    response = client.post("/api/simulator/generate?scenario=normal&count=3")
    assert response.status_code == 200
    data = response.json()
    assert data["records_generated"] == 3
