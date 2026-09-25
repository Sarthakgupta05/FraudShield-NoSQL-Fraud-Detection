"""
Multi-Vector Real-Time Risk Analysis Engine for FraudShield.
Combines Graph NoSQL Topological Heuristics with Document NoSQL Velocity Aggregations.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple
from ..models.schemas import TransactionCreate, RiskEvaluation
from ..database.mongo_client import doc_store
from ..database.graph_engine import graph_engine
import logging

logger = logging.getLogger("fraudshield.risk")

class RealTimeRiskAnalyzer:
    def __init__(self):
        self.cycle_weight = 45.0
        self.device_share_weight = 30.0
        self.velocity_burst_weight = 25.0
        self.amount_outlier_weight = 15.0

    def evaluate_transaction(self, tx: TransactionCreate, tx_id: str) -> RiskEvaluation:
        now = datetime.now(timezone.utc)
        score = 0.0
        reasons: List[str] = []
        cycle_detected = False
        cycle_path: List[str] = None

        # 1. Graph Vector: Cycle / Ring Detection
        # Check if this transaction completes a circular flow in the graph
        cycles = graph_engine.find_cycles_involving_transaction(
            sender=tx.sender_account, 
            receiver=tx.receiver_account, 
            max_depth=5
        )
        if cycles:
            cycle_detected = True
            cycle_path = cycles[0]
            score += self.cycle_weight
            reasons.append(f"Circular fraud ring detected (Length: {len(cycle_path)} nodes): {' -> '.join(cycle_path)}")

        # 2. Graph Vector: Shared Device & Mule Cluster Check
        shared_accounts = graph_engine.get_shared_device_accounts(tx.device_telemetry.device_id)
        # If current sender is not in shared yet, add 1 to count
        effective_device_users = set(shared_accounts)
        effective_device_users.add(tx.sender_account)
        shared_count = len(effective_device_users)

        if shared_count >= 3:
            score += self.device_share_weight
            reasons.append(f"High-risk device sharing: Device {tx.device_telemetry.device_id[:8]} used by {shared_count} distinct KYC accounts")
        elif shared_count == 2:
            score += 15.0
            reasons.append(f"Moderate device sharing: Device used across 2 accounts")

        # 3. Document Store Vector: Short-Window Velocity Aggregation (Last 5 minutes)
        five_min_ago = now - timedelta(minutes=5)
        recent_tx_count = doc_store.transactions.count_documents({
            "sender_account": tx.sender_account,
            "timestamp": {"$gte": five_min_ago}
        })
        
        if recent_tx_count >= 5:
            score += self.velocity_burst_weight
            reasons.append(f"Burst velocity spike: {recent_tx_count + 1} transactions initiated in under 5 minutes")
        elif recent_tx_count >= 3:
            score += 12.0
            reasons.append(f"Elevated transaction frequency ({recent_tx_count + 1} txs in 5m)")

        # 4. Monetary Outlier Check
        if tx.amount >= 100000.0:
            score += self.amount_outlier_weight
            reasons.append(f"High-value transfer alert (₹{tx.amount:,.2f})")
        elif tx.amount >= 50000.0:
            score += 8.0
            reasons.append(f"Above-average transfer amount (₹{tx.amount:,.2f})")

        # Cap score at 100
        final_score = min(100.0, round(score, 1))

        # Decision classification
        if final_score >= 75.0:
            classification = "HIGH_RISK_BLOCK"
        elif final_score >= 40.0:
            classification = "MEDIUM_RISK_CHALLENGE_2FA"
        else:
            classification = "LOW_RISK_APPROVE"
            if not reasons:
                reasons.append("Standard transaction profile verified")

        return RiskEvaluation(
            risk_score=final_score,
            classification=classification,
            anomaly_reasons=reasons,
            graph_cycle_detected=cycle_detected,
            cycle_path=cycle_path,
            shared_device_count=shared_count,
            velocity_5m_count=recent_tx_count + 1,
            evaluated_at=now
        )

# Global singleton
risk_analyzer = RealTimeRiskAnalyzer()
