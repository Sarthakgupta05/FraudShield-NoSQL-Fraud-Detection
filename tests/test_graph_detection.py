"""
Unit tests for FraudShield Graph Engine.
Tests cyclic path detection, mule detection, and shared device clustering.
"""

import pytest
from src.backend.database.graph_engine import FraudGraphEngine

def test_circular_ring_detection():
    engine = FraudGraphEngine()
    
    # Create a 3-node ring: ACC_A -> ACC_B -> ACC_C -> ACC_A
    engine.add_transaction("ACC_A", "ACC_B", 10000.0, "TX_1")
    engine.add_transaction("ACC_B", "ACC_C", 9800.0, "TX_2")
    
    # Before closing the loop
    rings_before = engine.find_all_fraud_rings()
    assert len(rings_before) == 0

    # Add the closing transaction: ACC_C -> ACC_A
    cycles = engine.find_cycles_involving_transaction("ACC_C", "ACC_A", max_depth=5)
    assert len(cycles) > 0
    assert cycles[0] == ["ACC_C", "ACC_A", "ACC_B", "ACC_C"]

    engine.add_transaction("ACC_C", "ACC_A", 9500.0, "TX_3")
    rings_after = engine.find_all_fraud_rings()
    assert len(rings_after) == 1
    assert rings_after[0]["ring_length"] == 3
    assert rings_after[0]["total_volume"] == 29300.0

def test_shared_device_clustering():
    engine = FraudGraphEngine()
    
    dev_id = "DEV_SUSPICIOUS_01"
    engine.add_transaction("ACC_X", "ACC_Y", 5000.0, "TX_10", device_id=dev_id)
    engine.add_transaction("ACC_Z", "ACC_W", 4000.0, "TX_11", device_id=dev_id)
    engine.add_transaction("ACC_M", "ACC_N", 3000.0, "TX_12", device_id=dev_id)

    accounts = engine.get_shared_device_accounts(dev_id)
    assert len(accounts) == 3
    assert set(accounts) == {"ACC_X", "ACC_Z", "ACC_M"}

def test_mule_network_detection():
    engine = FraudGraphEngine()
    
    mule = "ACC_MULE"
    # 4 distinct sources send money to MULE
    for i in range(4):
        engine.add_transaction(f"SRC_{i}", mule, 10000.0, f"TX_IN_{i}")
    
    # MULE forwards money to 2 collectors
    engine.add_transaction(mule, "COLL_1", 19000.0, "TX_OUT_1")
    engine.add_transaction(mule, "COLL_2", 19000.0, "TX_OUT_2")

    mules = engine.find_all_mule_networks(fan_in_threshold=3)
    assert len(mules) >= 1
    mule_record = next(m for m in mules if m["mule_account"] == mule)
    assert mule_record["in_degree"] == 4
    assert mule_record["out_degree"] == 2
    assert mule_record["total_received"] == 40000.0
