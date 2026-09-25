from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid

class DeviceTelemetry(BaseModel):
    device_id: str
    ip_address: str
    user_agent: str = "Mozilla/5.0"
    device_fingerprint: str
    os: str = "Android"

class GeospatialLocation(BaseModel):
    lat: float
    lon: float
    city: str
    country: str = "India"

class TransactionCreate(BaseModel):
    sender_account: str
    receiver_account: str
    amount: float = Field(gt=0, description="Amount must be positive")
    currency: str = "INR"
    payment_type: str = "UPI_INSTANT"
    device_telemetry: DeviceTelemetry
    geospatial: GeospatialLocation
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RiskEvaluation(BaseModel):
    risk_score: float = Field(ge=0, le=100)
    classification: str # LOW_RISK_APPROVE, MEDIUM_RISK_CHALLENGE_2FA, HIGH_RISK_BLOCK
    anomaly_reasons: List[str]
    graph_cycle_detected: bool = False
    cycle_path: Optional[List[str]] = None
    shared_device_count: int = 0
    velocity_5m_count: int = 0
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TransactionRecord(BaseModel):
    id: str = Field(default_factory=lambda: f"TX_{uuid.uuid4().hex[:8].upper()}")
    sender_account: str
    receiver_account: str
    amount: float
    currency: str
    payment_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    device_telemetry: DeviceTelemetry
    geospatial: GeospatialLocation
    metadata: Dict[str, Any] = Field(default_factory=dict)
    risk_evaluation: Optional[RiskEvaluation] = None

class AccountProfile(BaseModel):
    account_id: str
    customer_name: str
    kyc_level: str = "TIER_2" # TIER_1, TIER_2, TIER_3
    risk_tier: str = "LOW"
    total_volume: float = 0.0
    transaction_count: int = 0
    linked_devices: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class FraudAlert(BaseModel):
    alert_id: str = Field(default_factory=lambda: f"ALT_{uuid.uuid4().hex[:6].upper()}")
    transaction_id: str
    sender_account: str
    receiver_account: str
    amount: float
    risk_score: float
    reasons: List[str]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "OPEN" # OPEN, UNDER_INVESTIGATION, RESOLVED
