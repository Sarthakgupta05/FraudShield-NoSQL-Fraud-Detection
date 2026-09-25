# FraudShield: Real-Time Multi-Model NoSQL Fraud Detection System

FraudShield is a high-throughput, real-time financial fraud detection and risk scoring platform architected on a **Multi-Model NoSQL** paradigm:
- **Document NoSQL (MongoDB):** Flexible BSON schemaless storage for polymorphic transaction telemetry, customer KYC profiles, and sliding-window velocity aggregations.
- **Graph NoSQL (Neo4j / Property Graph Model):** Index-free adjacency and sub-second graph traversal for real-time circular fraud ring discovery, money mule identification, and shared-device cluster detection.

---

## 📁 Repository Structure

```
.
├── NoSQL_Project_Formate.pdf            # Original assignment template
├── message.txt                          # Instructor guidelines & requirements
├── assignment/
│   ├── NoSQL_Project_Analysis_Assignment.md    # Full 16-section assignment proposal
│   ├── NoSQL_Project_Analysis_Assignment.docx  # Formatted Word Document with diagrams
│   ├── NoSQL_Project_Analysis_Assignment.pdf   # Formatted PDF document ready for submission
│   ├── generate_assignment_docs.py             # Docx & PDF generator script
│   ├── generate_diagrams.py                    # Matplotlib diagram generator
│   └── diagrams/                               # High-res diagrams (System Arch, Data Model, Flowchart)
├── src/
│   ├── backend/
│   │   ├── app.py                       # FastAPI REST & WebSocket streaming server
│   │   ├── config.py                    # System settings
│   │   ├── database/
│   │   │   ├── mongo_client.py          # MongoDB client with in-memory fallback
│   │   │   └── graph_engine.py          # Graph NoSQL engine & cycle detection
│   │   ├── models/
│   │   │   └── schemas.py               # Pydantic & BSON schemas
│   │   └── services/
│   │       ├── risk_analyzer.py         # Multi-factor real-time scoring engine
│   │       └── data_generator.py        # Realistic financial stream & fraud simulator
│   └── frontend/
│       ├── index.html                   # Dark-themed FinTech dashboard
│       ├── styles.css                   # Modern styling & UI components
│       └── app.js                       # Vis.js graph rendering & live WebSocket updates
├── tests/
│   ├── test_graph_detection.py          # Unit tests for cycle detection & mule networks
│   ├── test_mongo_storage.py            # Unit tests for Document NoSQL CRUD & queries
│   ├── test_risk_analyzer.py            # Unit tests for multi-vector risk heuristics
│   └── test_api_endpoints.py            # Integration tests for FastAPI endpoints
├── requirements.txt                     # Python dependencies
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Installation

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Launch the Application

Run the FastAPI backend server:
```bash
python3 -m uvicorn src.backend.app:app --host 0.0.0.0 --port 8000 --reload
```

Open your web browser and navigate to:
👉 **`http://localhost:8000`**

---

## 🔬 Key Features & Demonstrations

### 1. Interactive Graph Explorer (Vis.js)
- Displays dynamic account nodes (blue) and shared device nodes (yellow).
- Visualizes directed payment flows and circular money laundering loops in real time.

### 2. Synthetic Scenario Injection
Use the dashboard control buttons to inject live test scenarios:
- **+5 Normal Transactions:** Standard P2P and merchant payments.
- **+3-Hop Circular Fraud Ring:** Closed cycle ($A \rightarrow B \rightarrow C \rightarrow A$) triggering automatic graph cycle alerts.
- **+Mule Smurfing Network:** Fan-out to multiple disposable mule accounts aggregating into a central collector.
- **+Velocity Burst Attack:** Rapid carding attempts from a single device.

### 3. NoSQL Inspection Console
Click on any transaction in the live table to inspect its raw BSON Document representation stored in MongoDB.

---

## 🧪 Running Automated Tests

Run the complete test suite with PyTest:
```bash
pytest tests/ -v
```

---

## 📄 Assignment Deliverables

The assignment document answering **all 16 sections** from `NoSQL_Project_Formate.pdf` is available in three formats:
1. **Markdown:** `assignment/NoSQL_Project_Analysis_Assignment.md`
2. **Microsoft Word:** `assignment/NoSQL_Project_Analysis_Assignment.docx`
3. **PDF Document:** `assignment/NoSQL_Project_Analysis_Assignment.pdf`

To recompile the document files and diagrams at any time:
```bash
python3 assignment/generate_diagrams.py
python3 assignment/generate_assignment_docs.py
```
