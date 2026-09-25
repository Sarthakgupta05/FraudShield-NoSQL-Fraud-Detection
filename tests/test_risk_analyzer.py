"""
Unit tests for Real-Time Multi-Factor Risk Analyzer.
"""

import pytest
from src.backend.models.schemas import TransactionCreate, DeviceTelemetry, GeospatialLocation
from src.backend.services.risk_analyzer import RealTimeRiskAnalyzer
from src.backend.database.graph_engine import graph_engine
from src.backend.database.mongo_client import doc_store

def test_normal_transaction_scoring():
    graph_engine.clear()
    doc_store.transactions.delete_many({})
    analyzer = RealTimeRiskAnalyzer()

    tx = TransactionCreate(
        sender_account="NORMAL_01",
        receiver_account="NORMAL_02",
        amount=500.0,
        currency="INR",
        payment_type="UPI_INSTANT",
        device_telemetry=DeviceTelemetry(
            device_id="DEV_SAFE_01",
            ip_address="192.168.1.1",
            device_fingerprint="fp_safe"
        ),
        geospatial=GeospatialLocation(lat=19.0760, lon=72.8777, city="Mumbai")
    )

    evaluation = analyzer.evaluate_transaction(tx, "TX_SAFE_101")
    assert evaluation.risk_score < 40.0
    assert evaluation.classification == "LOW_RISK_APPROVE"
    assert evaluation.graph_cycle_detected is False

def test_circular_ring_high_risk_trigger():
    graph_engine.clear()
    doc_store.transactions.delete_many({})
    analyzer = RealTimeRiskAnalyzer()

    # Create 2 legs of a loop
    graph_engine.add_transaction("ACC_RING_A", "ACC_RING_B", 60000.0, "TX_L1")
    graph_engine.add_transaction("ACC_RING_B", "ACC_RING_C", 59000.0, "TX_L2")

    # Closing leg: C -> A
    tx_closing = TransactionCreate(
        sender_account="ACC_RING_C",
        receiver_account="ACC_RING_A",
        amount=58000.0,
        currency="INR",
        payment_type="UPI_INSTANT",
        device_telemetry=DeviceTelemetry(
            device_id="DEV_RING_01",
            ip_address="103.21.14.88",
            device_fingerprint="fp_ring"
        ),
        geospatial=GeospatialLocation(lat=28.6139, lon=77.2090, city="New Delhi")
    )

    evaluation = analyzer.evaluate_transaction(tx_closing, "TX_RING_CLOSE")
    assert evaluation.graph_cycle_detected is True
    assert evaluation.risk_score >= 45.0 # At least cycle weight + high amount
