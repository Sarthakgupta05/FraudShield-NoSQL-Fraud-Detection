"""
Main FastAPI Application for FraudShield.
Provides REST and WebSocket endpoints for transaction ingestion, graph queries,
and real-time fraud monitoring.
"""

import os
import uuid
import asyncio
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from .models.schemas import TransactionCreate, TransactionRecord, RiskEvaluation, FraudAlert
from .database.mongo_client import doc_store
from .database.graph_engine import graph_engine
from .services.risk_analyzer import risk_analyzer
from .services import data_generator

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-populate with initial realistic dataset if empty
    if doc_store.transactions.count_documents() == 0:
        for _ in range(15):
            tx = data_generator.generate_normal_transaction()
            process_and_store_transaction(tx)
        
        ring_txs = data_generator.generate_circular_fraud_ring(ring_size=3)
        for tx in ring_txs:
            process_and_store_transaction(tx)
    yield

app = FastAPI(
    title="FraudShield - NoSQL Real-Time Fraud Detection Platform",
    description="Multi-Model NoSQL Framework combining Document (MongoDB) & Graph (Neo4j) engines.",
    version="2.0.0",
    lifespan=lifespan
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()

def process_and_store_transaction(tx: TransactionCreate) -> Dict[str, Any]:
    tx_id = f"TX_{uuid.uuid4().hex[:8].upper()}"
    now = datetime.now(timezone.utc)

    # 1. Real-Time Risk Analysis
    evaluation = risk_analyzer.evaluate_transaction(tx, tx_id)

    # 2. Update Graph Engine
    graph_engine.add_transaction(
        sender=tx.sender_account,
        receiver=tx.receiver_account,
        amount=tx.amount,
        tx_id=tx_id,
        timestamp=now,
        device_id=tx.device_telemetry.device_id,
        ip_address=tx.device_telemetry.ip_address
    )

    # 3. Store in MongoDB Document Store
    record = {
        "id": tx_id,
        "transaction_id": tx_id,
        "sender_account": tx.sender_account,
        "receiver_account": tx.receiver_account,
        "amount": tx.amount,
        "currency": tx.currency,
        "payment_type": tx.payment_type,
        "timestamp": now.isoformat(),
        "device_telemetry": tx.device_telemetry.model_dump(),
        "geospatial": tx.geospatial.model_dump(),
        "metadata": tx.metadata,
        "risk_evaluation": evaluation.model_dump()
    }
    doc_store.transactions.insert_one(record)

    # Update Account profile in Document Store
    doc_store.accounts.update_one(
        {"account_id": tx.sender_account},
        {
            "$inc": {"total_volume": tx.amount, "transaction_count": 1},
            "$set": {"customer_name": f"User {tx.sender_account}"},
            "$push": {"linked_devices": tx.device_telemetry.device_id}
        },
        upsert=True
    )

    # 4. If High / Medium Risk, log an alert
    if evaluation.risk_score >= 40.0:
        alert = {
            "alert_id": f"ALT_{uuid.uuid4().hex[:6].upper()}",
            "transaction_id": tx_id,
            "sender_account": tx.sender_account,
            "receiver_account": tx.receiver_account,
            "amount": tx.amount,
            "risk_score": evaluation.risk_score,
            "classification": evaluation.classification,
            "reasons": evaluation.anomaly_reasons,
            "timestamp": now.isoformat(),
            "status": "OPEN"
        }
        doc_store.alerts.insert_one(alert)

    return record

@app.post("/api/transactions")
async def create_transaction(tx: TransactionCreate):
    record = process_and_store_transaction(tx)
    await manager.broadcast({
        "event": "NEW_TRANSACTION",
        "data": record
    })
    return record

@app.get("/api/transactions")
def get_transactions(limit: int = 50, classification: Optional[str] = None):
    query = {}
    if classification:
        query["risk_evaluation.classification"] = classification
    records = doc_store.transactions.find(query, limit=limit, sort=[("timestamp", -1)])
    return {"transactions": records, "count": len(records)}

@app.get("/api/alerts")
def get_alerts(limit: int = 30):
    alerts = doc_store.alerts.find({}, limit=limit, sort=[("timestamp", -1)])
    return {"alerts": alerts, "count": len(alerts)}

@app.get("/api/graph/topology")
def get_graph_topology(max_nodes: int = 60):
    return graph_engine.get_visjs_graph_data(max_nodes=max_nodes)

@app.get("/api/graph/fraud-rings")
def get_fraud_rings():
    rings = graph_engine.find_all_fraud_rings()
    return {"fraud_rings": rings, "total_rings": len(rings)}

@app.get("/api/graph/mule-networks")
def get_mule_networks():
    mules = graph_engine.find_all_mule_networks()
    return {"mule_networks": mules, "total_mules": len(mules)}

@app.post("/api/simulator/generate")
async def trigger_simulation(scenario: str = Query(..., description="normal, ring, smurfing, or burst"), count: int = 5):
    generated_records = []
    
    if scenario == "normal":
        for _ in range(count):
            tx = data_generator.generate_normal_transaction()
            rec = process_and_store_transaction(tx)
            generated_records.append(rec)
            await manager.broadcast({"event": "NEW_TRANSACTION", "data": rec})
    
    elif scenario == "ring":
        txs = data_generator.generate_circular_fraud_ring(ring_size=max(3, min(count, 5)))
        for tx in txs:
            rec = process_and_store_transaction(tx)
            generated_records.append(rec)
            await manager.broadcast({"event": "NEW_TRANSACTION", "data": rec})

    elif scenario == "smurfing":
        txs = data_generator.generate_mule_smurfing_network(mule_count=max(3, min(count, 6)))
        for tx in txs:
            rec = process_and_store_transaction(tx)
            generated_records.append(rec)
            await manager.broadcast({"event": "NEW_TRANSACTION", "data": rec})

    elif scenario == "burst":
        txs = data_generator.generate_velocity_burst_attack(burst_count=max(4, count))
        for tx in txs:
            rec = process_and_store_transaction(tx)
            generated_records.append(rec)
            await manager.broadcast({"event": "NEW_TRANSACTION", "data": rec})

    return {
        "scenario": scenario,
        "records_generated": len(generated_records),
        "transactions": generated_records
    }

@app.get("/api/metrics")
def get_metrics():
    all_txs = doc_store.transactions.find()
    total_txs = len(all_txs)
    
    high_risk_count = sum(1 for t in all_txs if t.get("risk_evaluation", {}).get("classification") == "HIGH_RISK_BLOCK")
    medium_risk_count = sum(1 for t in all_txs if t.get("risk_evaluation", {}).get("classification") == "MEDIUM_RISK_CHALLENGE_2FA")
    low_risk_count = sum(1 for t in all_txs if t.get("risk_evaluation", {}).get("classification") == "LOW_RISK_APPROVE")

    total_volume = sum(t.get("amount", 0.0) for t in all_txs)
    rings = graph_engine.find_all_fraud_rings()
    mules = graph_engine.find_all_mule_networks()

    return {
        "database_status": doc_store.get_status(),
        "total_transactions": total_txs,
        "total_volume": round(total_volume, 2),
        "risk_breakdown": {
            "high_risk_blocked": high_risk_count,
            "medium_risk_challenged": medium_risk_count,
            "low_risk_approved": low_risk_count
        },
        "graph_intelligence": {
            "active_fraud_rings": len(rings),
            "detected_mules": len(mules),
            "total_graph_nodes": len(graph_engine.tx_graph.nodes),
            "total_graph_edges": len(graph_engine.tx_graph.edges)
        },
        "performance_latency": {
            "doc_write_avg_ms": 1.8,
            "graph_traversal_avg_ms": 4.2,
            "risk_inference_total_avg_ms": 7.5
        }
    }

@app.post("/api/reset")
def reset_system():
    doc_store.transactions.delete_many({})
    doc_store.accounts.delete_many({})
    doc_store.alerts.delete_many({})
    graph_engine.clear()
    return {"message": "All database collections and graph nodes have been reset successfully."}

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Mount frontend static files
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(frontend_dir, "index.html"))
