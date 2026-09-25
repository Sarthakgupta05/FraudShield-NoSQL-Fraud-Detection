"""
Synthetic Financial Data Generator & Fraud Simulator for FraudShield.
Produces realistic normal transactions as well as complex fraud topology patterns.
"""

import random
import uuid
import hashlib
from typing import List, Dict, Any
from datetime import datetime, timezone
from ..models.schemas import TransactionCreate, DeviceTelemetry, GeospatialLocation

CITIES = [
    {"city": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"city": "New Delhi", "lat": 28.6139, "lon": 77.2090},
    {"city": "Bengaluru", "lat": 12.9716, "lon": 77.5946},
    {"city": "Hyderabad", "lat": 17.3850, "lon": 78.4867},
    {"city": "Chennai", "lat": 13.0827, "lon": 80.2707},
    {"city": "Pune", "lat": 18.5204, "lon": 73.8567},
    {"city": "Kolkata", "lat": 22.5726, "lon": 88.3639}
]

PAYMENT_TYPES = ["UPI_INSTANT", "IMPS", "NEFT", "DEBIT_CARD", "CREDIT_CARD", "NET_BANKING"]
OS_LIST = ["Android 14", "iOS 17.5", "Windows 11", "macOS Sonoma", "Ubuntu Linux"]

def _generate_device(device_id: str = None) -> DeviceTelemetry:
    dev_id = device_id or f"DEV_{uuid.uuid4().hex[:6].upper()}"
    ip = f"{random.randint(45, 185)}.{random.randint(10, 250)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
    fingerprint = hashlib.sha256(f"{dev_id}-{ip}".encode()).hexdigest()
    return DeviceTelemetry(
        device_id=dev_id,
        ip_address=ip,
        user_agent="Mozilla/5.0 FraudShieldClient/2.0",
        device_fingerprint=fingerprint,
        os=random.choice(OS_LIST)
    )

def generate_normal_transaction(sender: str = None, receiver: str = None) -> TransactionCreate:
    s = sender or f"ACC_{random.randint(1000, 4999)}"
    r = receiver or f"ACC_{random.randint(5000, 9999)}"
    loc = random.choice(CITIES)
    amount = round(random.uniform(150.0, 4500.0), 2)

    return TransactionCreate(
        sender_account=s,
        receiver_account=r,
        amount=amount,
        currency="INR",
        payment_type=random.choice(PAYMENT_TYPES),
        device_telemetry=_generate_device(),
        geospatial=GeospatialLocation(
            lat=loc["lat"] + random.uniform(-0.05, 0.05),
            lon=loc["lon"] + random.uniform(-0.05, 0.05),
            city=loc["city"],
            country="India"
        ),
        metadata={"category": "Retail / P2P Transfer", "simulation": "Normal"}
    )

def generate_circular_fraud_ring(ring_size: int = 4, base_amount: float = 75000.0) -> List[TransactionCreate]:
    """Generates a closed loop: A -> B -> C -> D -> A to trigger graph cycle detection."""
    accounts = [f"RING_ACC_{uuid.uuid4().hex[:4].upper()}" for _ in range(ring_size)]
    transactions = []
    loc = random.choice(CITIES)
    shared_device_id = f"SHARED_DEV_{uuid.uuid4().hex[:4].upper()}"

    for i in range(ring_size):
        sender = accounts[i]
        receiver = accounts[(i + 1) % ring_size]
        # Slight variation in amount to simulate fee deductions
        amount = round(base_amount * random.uniform(0.92, 0.98), 2)
        
        tx = TransactionCreate(
            sender_account=sender,
            receiver_account=receiver,
            amount=amount,
            currency="INR",
            payment_type="UPI_INSTANT",
            device_telemetry=_generate_device(shared_device_id if i % 2 == 0 else None),
            geospatial=GeospatialLocation(lat=loc["lat"], lon=loc["lon"], city=loc["city"]),
            metadata={"simulation": "Circular Fraud Ring", "ring_order": i + 1}
        )
        transactions.append(tx)
    return transactions

def generate_mule_smurfing_network(mule_count: int = 5, total_illicit_amount: float = 120000.0) -> List[TransactionCreate]:
    """1 Source Account -> Multiple Mule Accounts -> 1 Master Collector Account."""
    source_acc = f"ILLICIT_SRC_{uuid.uuid4().hex[:4].upper()}"
    collector_acc = f"COLLECTOR_{uuid.uuid4().hex[:4].upper()}"
    mules = [f"MULE_ACC_{uuid.uuid4().hex[:4].upper()}" for _ in range(mule_count)]
    
    transactions = []
    split_amount = round(total_illicit_amount / mule_count, 2)
    loc = random.choice(CITIES)

    # Step 1: Disperse to mules (Fan-Out)
    for mule in mules:
        transactions.append(TransactionCreate(
            sender_account=source_acc,
            receiver_account=mule,
            amount=split_amount,
            currency="INR",
            payment_type="IMPS",
            device_telemetry=_generate_device(),
            geospatial=GeospatialLocation(lat=loc["lat"], lon=loc["lon"], city=loc["city"]),
            metadata={"simulation": "Smurfing - Dispersion Phase"}
        ))

    # Step 2: Mules aggregate to Collector (Fan-In)
    for mule in mules:
        transactions.append(TransactionCreate(
            sender_account=mule,
            receiver_account=collector_acc,
            amount=round(split_amount * 0.95, 2),
            currency="INR",
            payment_type="IMPS",
            device_telemetry=_generate_device(),
            geospatial=GeospatialLocation(lat=loc["lat"], lon=loc["lon"], city=loc["city"]),
            metadata={"simulation": "Smurfing - Collection Phase"}
        ))

    return transactions

def generate_velocity_burst_attack(burst_count: int = 6) -> List[TransactionCreate]:
    """Single sender rapidly sending high volume transactions from one device."""
    attacker_acc = f"ATTACKER_{uuid.uuid4().hex[:4].upper()}"
    shared_device = f"DEV_BOTNET_{uuid.uuid4().hex[:4].upper()}"
    loc = random.choice(CITIES)
    transactions = []

    for _ in range(burst_count):
        victim = f"VICTIM_{random.randint(1000, 9999)}"
        transactions.append(TransactionCreate(
            sender_account=attacker_acc,
            receiver_account=victim,
            amount=round(random.uniform(25000.0, 60000.0), 2),
            currency="INR",
            payment_type="CREDIT_CARD",
            device_telemetry=_generate_device(shared_device),
            geospatial=GeospatialLocation(lat=loc["lat"], lon=loc["lon"], city=loc["city"]),
            metadata={"simulation": "Velocity Burst Attack"}
        ))
    return transactions
