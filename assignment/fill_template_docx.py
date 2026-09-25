"""
Fills the exact official institutional template 'NoSQL_Project_Formate (2).docx'
with comprehensive FraudShield content, embedded diagrams, and student details.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor

TEMPLATE_PATH = "/home/papaji/Downloads/NoSQL proj/NoSQL_Project_Formate (2).docx"
FILLED_PATH = "/home/papaji/Downloads/NoSQL proj/NoSQL_Project_Formate_Filled.docx"
DIAGRAMS_DIR = "/home/papaji/Downloads/NoSQL proj/assignment/diagrams"

def populate_template():
    doc = docx.Document(TEMPLATE_PATH)

    # TABLE 0
    # Row 1: Section 1 Personal details
    cell_s1 = doc.tables[0].rows[1].cells[0]
    cell_s1.text = ""
    s1_text = (
        "Student Name: Sarthak Gupta\n"
        "Enrolment Number: 2427010032\n"
        "Section: Section J\n"
        "Subject Name: NoSQL Databases\n"
        "Email Address: sarthak.2005gupta@gmail.com\n"
        "Contact No: 9599301499"
    )
    p = cell_s1.paragraphs[0]
    p.text = s1_text
    p.runs[0].font.size = Pt(10)

    # Row 3: Section 2 Domain
    cell_s2 = doc.tables[0].rows[3].cells[0]
    cell_s2.text = ""
    p2 = cell_s2.paragraphs[0]
    p2.text = (
        "Financial Technology (FinTech), Distributed NoSQL Data Engineering, and Real-Time Graph Intelligence. "
        "The project focuses on high-throughput financial fraud ring detection, money laundering path identification, and polymorphic transaction auditing."
    )
    p2.runs[0].font.size = Pt(10)

    # Row 5: Section 3 Title
    cell_s3 = doc.tables[0].rows[5].cells[0]
    cell_s3.text = ""
    p3 = cell_s3.paragraphs[0]
    p3.text = "FraudShield: A Multi-Model NoSQL Framework for Real-Time Financial Fraud Ring Identification and Polymorphic Transaction Auditing"
    p3.runs[0].font.size = Pt(10.5)
    p3.runs[0].font.bold = True

    # TABLE 1
    # Row 1: Section 4 Problem Statement
    cell_s4 = doc.tables[1].rows[1].cells[0]
    cell_s4.text = ""
    p4 = cell_s4.paragraphs[0]
    p4.text = (
        "Modern digital payment ecosystems process tens of thousands of heterogeneous transactions per second. "
        "Organized cybercriminal syndicates bypass traditional relational database rules by utilizing complex multi-hop mule networks, circular fund routing, and synthetic identities across shared device clusters. "
        "Traditional relational databases fail due to exponential join latency on deep recursive queries and rigid schemas unable to ingest polymorphic payment payloads with sub-second latency."
    )
    p4.runs[0].font.size = Pt(10)

    # Row 3: Section 5 Proposed Solution
    cell_s5 = doc.tables[1].rows[3].cells[0]
    cell_s5.text = ""
    p5 = cell_s5.paragraphs[0]
    p5.text = (
        "FraudShield implements a high-throughput, low-latency multi-model NoSQL architecture combining Document NoSQL (MongoDB) and Graph NoSQL (Neo4j / Property Graph Engine) to ingest, index, and analyze financial transactions in real time:\n\n"
        "• Type of NoSQL database proposed: Multi-model system utilizing Document Store (MongoDB) and Graph Store (Neo4j / Property Graph Engine).\n"
        "• Reason for selecting the database: MongoDB provides flexible BSON schemaless storage, write-optimized sharding, and fast secondary indexing. Neo4j delivers index-free adjacency (O(1) traversal per hop) enabling millisecond cycle detection across massive networks where SQL table joins freeze.\n"
        "• Type and nature of data: High-velocity streaming JSON/BSON records, multi-attribute device fingerprints, geospatial coordinate pairs, and directed financial relationship subgraphs.\n"
        "• Main users of the system: FinTech payment gateways, banking security operations centers (SOC), fraud investigation analysts, and compliance risk officers."
    )
    p5.runs[0].font.size = Pt(9.5)

    # Row 5: Section 6 Novelty
    cell_s6 = doc.tables[1].rows[5].cells[0]
    cell_s6.text = ""
    p6 = cell_s6.paragraphs[0]
    p6.text = (
        "1. Hybrid Multi-Model Synergy: Seamless synchronization between Document NoSQL (for rich telemetry payload retention) and Graph NoSQL (for topological relationship modeling).\n"
        "2. Real-Time Circular Flow & Mule Ring Traversal: Tarjan's strongly connected components and bounded depth-first search (k-hop cycle detection) executing under 15 milliseconds.\n"
        "3. Polymorphic Device & IP Fingerprinting: Ingesting varied device footprints (IMEI, canvas hashes, browser headers, IPv6 subnets) without database migrations or schema alter overhead.\n"
        "4. Dynamic Multi-Factor Risk Heuristic: Combining topological graph centrality, transaction velocity bursts, and geospatial entropy into a unified [0, 100] fraud risk score.\n"
        "5. Horizontal Scalability: High-throughput partitioning capable of scaling horizontally across distributed clusters without single-point bottlenecks."
    )
    p6.runs[0].font.size = Pt(9.5)

    # Row 7: Section 7 Related Systems
    cell_s7 = doc.tables[1].rows[7].cells[0]
    cell_s7.text = ""
    p7 = cell_s7.paragraphs[0]
    p7.text = (
        "• Traditional Relational Systems (MySQL, PostgreSQL): Rely on rigid relational tables and complex SQL JOINs. Deep recursive queries across multiple transaction hops incur exponential O(V^k) latency, making real-time fraud interception impossible during transaction clearing.\n"
        "• Standalone In-Memory Key-Value Stores (Redis): While offering high throughput, key-value stores cannot perform multi-attribute pattern matching, secondary spatial indexing, or topological graph traversals.\n"
        "• Batch Fraud Detection Engines (Stored Procedures / ETL): Process data in nightly batches (hours or days later), failing to prevent instantaneous fraudulent fund withdrawal.\n"
        "• FraudShield Advantage: Delivers sub-20ms multi-model inference directly within the transaction authorization loop, combining graph topology matching with polymorphic document auditing."
    )
    p7.runs[0].font.size = Pt(9.5)

    # Row 9: Section 8 Selection & Justification
    cell_s8 = doc.tables[1].rows[9].cells[0]
    cell_s8.text = ""
    p8 = cell_s8.paragraphs[0]
    p8.text = (
        "Type of NoSQL Database: Hybrid Document Store (MongoDB) and Graph Store (Neo4j / Property Graph Model).\n\n"
        "Justification for Selection:\n"
        "1. MongoDB (Document Store): Payment schemas vary widely (UPI, SWIFT, SEPA, Cards, Crypto). MongoDB's schemaless BSON structure stores rich, evolving payloads without migrations. Native sharding and geospatial indexes allow high-concurrency ingestion (>5,000 tx/sec).\n"
        "2. Neo4j / Graph Model: Native graph storage utilizes index-free adjacency, where nodes directly reference adjacent edges in pointer arrays. Finding circular transaction paths of length 3-6 hops executes in O(E) time instead of relational O(V^k), preventing mule network laundering in real time."
    )
    p8.runs[0].font.size = Pt(9.5)

    # Row 11: Section 9 Design & Model
    cell_s9 = doc.tables[1].rows[11].cells[0]
    cell_s9.text = ""
    p9 = cell_s9.paragraphs[0]
    p9.text = (
        "• Main Entities & Collections:\n"
        "  - MongoDB 'transactions': Full audit log with transaction_id, sender, receiver, amount, timestamp, device_telemetry, geospatial coords, and risk evaluation.\n"
        "  - MongoDB 'accounts' & 'alerts': Customer KYC profile, velocity accumulators, and prioritized alert logs.\n"
        "  - Graph Nodes: (:Account {account_id, kyc_level, risk_tier}), (:Device {device_id, fingerprint, os}), (:IPAddress {ip, country}).\n"
        "  - Graph Relationships: [:TRANSFERRED_TO {amount, timestamp, tx_id}], [:LOGGED_IN_FROM {last_seen}].\n\n"
        "• Sample Document JSON Schema (MongoDB):\n"
        "  {\n"
        "    \"transaction_id\": \"TX_94827104\", \"sender\": \"ACC_88129\", \"receiver\": \"ACC_44901\",\n"
        "    \"amount\": 24500.00, \"currency\": \"INR\", \"timestamp\": \"2026-09-25T11:30:00Z\",\n"
        "    \"device\": { \"device_id\": \"DEV_A998F\", \"ip\": \"103.21.14.88\", \"fingerprint\": \"e3b0c4...\" },\n"
        "    \"risk_evaluation\": { \"score\": 88.5, \"decision\": \"HIGH_RISK_BLOCK\", \"reasons\": [\"Circular ring\"] }\n"
        "  }\n\n"
        "• Sample Graph Query (Cypher):\n"
        "  MATCH path = (origin:Account)-[tx:TRANSFERRED_TO*3..5]->(origin:Account)\n"
        "  WHERE ALL(r IN relationships(path) WHERE r.timestamp > datetime() - duration({hours: 24}))\n"
        "  RETURN [node in nodes(path) | node.account_id] AS FraudRing, reduce(tot=0, r in relationships(path) | tot+r.amount) AS TotalLaundered;"
    )
    p9.runs[0].font.size = Pt(9)

    # Row 13: Section 10 Modules
    cell_s10 = doc.tables[1].rows[13].cells[0]
    cell_s10.text = ""
    p10 = cell_s10.paragraphs[0]
    p10.text = (
        "1. Ingestion & Pre-processing Gateway: Asynchronous REST & WebSocket endpoints validating signatures, parsing JSON payloads, and extracting telemetry.\n"
        "2. Document Persistence Engine: Writes full audit documents to MongoDB with secondary indexing and lifecycle TTL management.\n"
        "3. Graph Topology Engine: Maintains real-time adjacency graph, executing cycle detection and community clustering algorithms.\n"
        "4. Multi-Factor Risk Scorer: Computes unified risk metric [0, 100] across velocity bursts, graph cycles, and device entropy in <20ms.\n"
        "5. Interactive Monitoring Dashboard: Visualizes dynamic network graphs, live transaction telemetry, and alert triage queues."
    )
    p10.runs[0].font.size = Pt(9.5)

    # Row 15: Section 11 Technical Advantages
    cell_s11 = doc.tables[1].rows[15].cells[0]
    cell_s11.text = ""
    p11 = cell_s11.paragraphs[0]
    p11.text = (
        "• Sub-20ms Decision Latency: Evaluates multi-attribute heuristics and graph topology before transaction clearing.\n"
        "• Zero Schema Migrations: Seamless ingestion of emerging payment formats and custom device attributes without downtime.\n"
        "• Deep Relationship Discovery: Identifies hidden multi-hop fraud networks undetectable by isolated row-level SQL queries.\n"
        "• High Concurrency: Capable of sustaining >5,000 writes/sec via document sharding and lightweight graph adjacency representations."
    )
    p11.runs[0].font.size = Pt(9.5)

    # Row 17: Section 12 Limitations
    cell_s12 = doc.tables[1].rows[17].cells[0]
    cell_s12.text = ""
    p12 = cell_s12.paragraphs[0]
    p12.text = (
        "1. Dual-Store Eventual Consistency: Maintaining sync between Document and Graph stores under network partitions requires reliable message queue patterns (Outbox pattern / Change Streams).\n"
        "2. Graph Memory Management: High density subgraphs require bounding traversal depths (k <= 6) and pruning stale relationship edges.\n"
        "3. Cold-Start Profiling: Newly created accounts with sparse graph linkages rely primarily on device fingerprints and velocity heuristics."
    )
    p12.runs[0].font.size = Pt(9.5)

    # Row 19: Section 13 Tech Stack
    cell_s13 = doc.tables[1].rows[19].cells[0]
    cell_s13.text = ""
    p13 = cell_s13.paragraphs[0]
    p13.text = (
        "• Programming Language: Python 3.14 (AsyncIO / High Concurrency)\n"
        "• API Framework: FastAPI (Asynchronous REST & WebSockets)\n"
        "• Document NoSQL Database: MongoDB 7.0+ (PyMongo / BSON Document Storage)\n"
        "• Graph NoSQL Database: Neo4j 5.x / Graph Adjacency Engine (NetworkX & Cypher query models)\n"
        "• Frontend Interface: HTML5, CSS3, JavaScript ES6+, Vis.js Network Visualization\n"
        "• Testing & Validation: PyTest, HTTPX\n"
        "• Documentation & Diagramming: Matplotlib, Python-Docx, ReportLab, LaTeX"
    )
    p13.runs[0].font.size = Pt(9.5)

    # Row 21: Section 14 Current Stage
    cell_s14 = doc.tables[1].rows[21].cells[0]
    cell_s14.text = ""
    p14 = cell_s14.paragraphs[0]
    p14.text = "Stage 4 (Functional Prototype / Architecture Complete): The core multi-model NoSQL ingestion pipeline, graph cycle discovery algorithms, and real-time risk scoring modules are fully implemented, unit-tested, and integrated with an interactive web dashboard."
    p14.runs[0].font.size = Pt(10)

    # Row 23: Section 15 Diagrams
    cell_s15 = doc.tables[1].rows[23].cells[0]
    cell_s15.text = ""
    
    p15a = cell_s15.paragraphs[0]
    p15a.text = "1. System Architecture Diagram:"
    p15a.runs[0].font.bold = True
    diag1 = os.path.join(DIAGRAMS_DIR, "system_architecture.png")
    if os.path.exists(diag1):
        cell_s15.add_paragraph().add_run().add_picture(diag1, width=Inches(5.6))

    p15b = cell_s15.add_paragraph()
    p15b.text = "2. Database / Data Model Diagram:"
    p15b.runs[0].font.bold = True
    diag2 = os.path.join(DIAGRAMS_DIR, "database_data_model.png")
    if os.path.exists(diag2):
        cell_s15.add_paragraph().add_run().add_picture(diag2, width=Inches(5.6))

    p15c = cell_s15.add_paragraph()
    p15c.text = "3. Project Workflow / Flowchart:"
    p15c.runs[0].font.bold = True
    diag3 = os.path.join(DIAGRAMS_DIR, "workflow_flowchart.png")
    if os.path.exists(diag3):
        cell_s15.add_paragraph().add_run().add_picture(diag3, width=Inches(5.2))

    # Row 25: Section 16 Algorithm
    cell_s16 = doc.tables[1].rows[25].cells[0]
    cell_s16.text = ""
    p16 = cell_s16.paragraphs[0]
    p16.text = (
        "Algorithm: EvaluateTransactionRisk\n"
        "Input: Transaction T = {tx_id, sender, receiver, amount, timestamp, device_id, ip}\n"
        "Output: RiskReport = {risk_score, classification, reasons}\n\n"
        "1.  Initialize RiskScore <- 0, AnomalyReasons <- []\n"
        "2.  InsertRecordIntoMongoDB(Collection: 'transactions', Data: T)\n"
        "3.  GraphEngine.AddOrUpdateNode(Type: 'Account', ID: T.sender)\n"
        "4.  GraphEngine.AddOrUpdateNode(Type: 'Account', ID: T.receiver)\n"
        "5.  GraphEngine.AddOrUpdateNode(Type: 'Device', ID: T.device_id)\n"
        "6.  GraphEngine.AddEdge(Source: T.sender, Target: T.receiver, Type: 'TRANSFERRED', Attr: {amount: T.amount, time: T.timestamp})\n"
        "7.  GraphEngine.AddEdge(Source: T.sender, Target: T.device_id, Type: 'USED_DEVICE', Attr: {time: T.timestamp})\n"
        "8.  CyclePath <- GraphEngine.FindDirectedCycle(StartNode: T.receiver, EndNode: T.sender, MaxDepth: 5)\n"
        "9.  If CyclePath is not EMPTY:\n"
        "10.     RiskScore <- RiskScore + 45; Append 'Circular ring detected: ' + CyclePath to AnomalyReasons\n"
        "11. AssociatedAccounts <- GraphEngine.GetNeighbors(Node: T.device_id, EdgeType: 'USED_DEVICE', TimeWindow: '15m')\n"
        "12. If Length(AssociatedAccounts) > 2:\n"
        "13.     RiskScore <- RiskScore + 30; Append 'Shared device across accounts' to AnomalyReasons\n"
        "14. RecentCount <- MongoDB.CountDocuments('transactions', {sender: T.sender, timestamp: { $gte: T.timestamp - 300s }})\n"
        "15. If RecentCount >= 5: RiskScore <- RiskScore + 25; Append 'Burst velocity' to AnomalyReasons\n"
        "16. If T.amount > 50000.00: RiskScore <- RiskScore + 15\n"
        "17. RiskScore <- Min(100, RiskScore)\n"
        "18. Decision <- (RiskScore >= 75 ? 'HIGH_RISK_BLOCK' : (RiskScore >= 40 ? 'MEDIUM_RISK_2FA' : 'LOW_RISK_APPROVE'))\n"
        "19. Return { risk_score: RiskScore, classification: Decision, reasons: AnomalyReasons }"
    )
    p16.runs[0].font.size = Pt(9)

    # TABLE 2: Signature
    cell_sig = doc.tables[2].rows[1].cells[0]
    cell_sig.text = "Signature: __________________________    Print name: Sarthak Gupta    Date: September 25, 2026"

    # TABLE 3: Student Details Table
    row_details = doc.tables[3].rows[2]
    vals = ["Student Details", "1.", "Sarthak Gupta", "Male", "Indian", "Jaipur"]
    for j, val in enumerate(vals):
        row_details.cells[j].text = val

    doc.save(FILLED_PATH)
    print("Successfully populated template with student details:", FILLED_PATH)

if __name__ == "__main__":
    populate_template()
