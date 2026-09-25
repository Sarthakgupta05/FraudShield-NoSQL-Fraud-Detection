"""
Generate high-resolution architecture, data model, and workflow diagrams for Section 15
using Matplotlib with clean, modern styling.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_system_architecture_diagram(output_path):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Color palette
    bg_color = "#F8FAFC"
    border_color = "#334155"
    client_color = "#E0F2FE"
    api_color = "#FEF3C7"
    engine_color = "#DCFCE7"
    db_color = "#F3E8FF"
    alert_color = "#FFE4E6"

    # Background canvas
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    # Title
    ax.text(6, 7.6, "FraudShield: Real-Time NoSQL Fraud Detection System Architecture", 
            fontsize=15, fontweight='bold', ha='center', va='center', color="#0F172A")

    # Layer 1: Ingestion & Clients
    rect1 = patches.FancyBboxPatch((0.5, 5.0), 2.8, 2.0, boxstyle="round,pad=0.2", 
                                  edgecolor="#0284C7", facecolor=client_color, linewidth=1.5)
    ax.add_patch(rect1)
    ax.text(1.9, 6.7, "Data Ingestion & UI Layer", fontsize=11, fontweight='bold', ha='center', color="#0369A1")
    ax.text(1.9, 6.1, "• Payment Gateway APIs\n• Mobile/Web Banking\n• Stream Simulators\n• Fraud Analyst Dashboard", 
            fontsize=9, ha='center', va='center', color="#1E293B")

    # Layer 2: API Gateway & Orchestrator
    rect2 = patches.FancyBboxPatch((4.2, 5.0), 3.2, 2.0, boxstyle="round,pad=0.2", 
                                  edgecolor="#D97706", facecolor=api_color, linewidth=1.5)
    ax.add_patch(rect2)
    ax.text(5.8, 6.7, "FastAPI Service Layer", fontsize=11, fontweight='bold', ha='center', color="#B45309")
    ax.text(5.8, 6.1, "• Async REST & WebSocket API\n• Real-Time Event Dispatcher\n• Velocity Window Tracker\n• Authentication & Rate Limiting", 
            fontsize=9, ha='center', va='center', color="#1E293B")

    # Layer 3: Risk Scoring & Graph Intelligence Engine
    rect3 = patches.FancyBboxPatch((8.2, 5.0), 3.3, 2.0, boxstyle="round,pad=0.2", 
                                  edgecolor="#16A34A", facecolor=engine_color, linewidth=1.5)
    ax.add_patch(rect3)
    ax.text(9.85, 6.7, "Risk & Graph Engine", fontsize=11, fontweight='bold', ha='center', color="#15803D")
    ax.text(9.85, 6.1, "• Tarjan's Cycle Detection\n• Mule Ring Network Analyzer\n• Device Fingerprint Entropy\n• Multi-Factor Risk Scoring", 
            fontsize=9, ha='center', va='center', color="#1E293B")

    # Layer 4: NoSQL Hybrid Storage Layer
    # MongoDB Document Store
    rect4a = patches.FancyBboxPatch((1.5, 1.2), 4.0, 2.6, boxstyle="round,pad=0.2", 
                                   edgecolor="#9333EA", facecolor=db_color, linewidth=1.5)
    ax.add_patch(rect4a)
    ax.text(3.5, 3.4, "Document Store (MongoDB)", fontsize=11, fontweight='bold', ha='center', color="#7E22CE")
    ax.text(3.5, 2.4, "• Polymorphic Transaction Logs\n• Dynamic Customer Profiles\n• Device Metadata & Geolocation\n• Audit History & Alert Archives\n• Time-Series Aggregations", 
            fontsize=9, ha='center', va='center', color="#1E293B")

    # Graph NoSQL Store
    rect4b = patches.FancyBboxPatch((6.5, 1.2), 4.0, 2.6, boxstyle="round,pad=0.2", 
                                   edgecolor="#9333EA", facecolor=db_color, linewidth=1.5)
    ax.add_patch(rect4b)
    ax.text(8.5, 3.4, "Graph Store (Neo4j / Property Graph)", fontsize=11, fontweight='bold', ha='center', color="#7E22CE")
    ax.text(8.5, 2.4, "• Node: Account, Card, Device, IP\n• Edge: TRANSFERRED_TO, USED_DEVICE\n• Multi-hop Graph Traversal\n• Circular Path Identification\n• High-Density Fraud Rings", 
            fontsize=9, ha='center', va='center', color="#1E293B")

    # Connective Arrows
    ax.annotate('', xy=(4.2, 6.0), xytext=(3.3, 6.0),
                arrowprops=dict(facecolor='#475569', edgecolor='#475569', arrowstyle='->', lw=2))
    ax.annotate('', xy=(8.2, 6.0), xytext=(7.4, 6.0),
                arrowprops=dict(facecolor='#475569', edgecolor='#475569', arrowstyle='->', lw=2))

    # Dual writes / queries arrows
    ax.annotate('', xy=(3.5, 3.8), xytext=(5.2, 5.0),
                arrowprops=dict(facecolor='#9333EA', edgecolor='#9333EA', arrowstyle='<->', lw=1.8, linestyle='--'))
    ax.annotate('', xy=(8.5, 3.8), xytext=(6.5, 5.0),
                arrowprops=dict(facecolor='#9333EA', edgecolor='#9333EA', arrowstyle='<->', lw=1.8, linestyle='--'))
    ax.annotate('', xy=(8.5, 3.8), xytext=(9.8, 5.0),
                arrowprops=dict(facecolor='#16A34A', edgecolor='#16A34A', arrowstyle='<->', lw=1.8))

    # Arrow Labels
    ax.text(3.75, 6.2, "JSON", fontsize=8, ha='center', color="#64748B", fontweight='bold')
    ax.text(7.8, 6.2, "Events", fontsize=8, ha='center', color="#64748B", fontweight='bold')
    ax.text(3.8, 4.4, "CRUD & Aggregation", fontsize=8, ha='center', color="#7E22CE", rotation=25)
    ax.text(8.0, 4.4, "Graph Query / Sync", fontsize=8, ha='center', color="#7E22CE", rotation=-25)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_data_model_diagram(output_path):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F8FAFC")

    ax.text(6, 7.6, "FraudShield: Hybrid NoSQL Data Model (Document & Graph)", 
            fontsize=15, fontweight='bold', ha='center', va='center', color="#0F172A")

    # Document Collections (Left)
    doc_box = patches.FancyBboxPatch((0.5, 0.8), 4.8, 6.4, boxstyle="round,pad=0.2", 
                                    edgecolor="#0284C7", facecolor="#F0F9FF", linewidth=1.5)
    ax.add_patch(doc_box)
    ax.text(2.9, 6.8, "MongoDB Document Collections", fontsize=12, fontweight='bold', ha='center', color="#0369A1")

    # Schema Box 1: transactions
    t_box = patches.FancyBboxPatch((0.8, 3.8), 4.2, 2.6, boxstyle="round,pad=0.1", 
                                  edgecolor="#38BDF8", facecolor="#FFFFFF", linewidth=1)
    ax.add_patch(t_box)
    ax.text(1.0, 6.1, "Collection: 'transactions'", fontsize=10, fontweight='bold', color="#0F172A")
    t_text = """• _id: ObjectId
• transaction_id: String (Unique)
• sender_account: String (Indexed)
• receiver_account: String (Indexed)
• amount: Decimal128
• timestamp: ISODate (TTL / TimeSeries)
• device: { device_id, ip, os, fingerprint }
• location: { lat, lon, city, country }
• payment_type: 'P2P' | 'WIRE' | 'CARD'
• risk_evaluation: { score, flags, decision }"""
    ax.text(1.0, 4.8, t_text, fontsize=8.5, va='center', color="#334155", fontfamily='monospace')

    # Schema Box 2: accounts & alerts
    a_box = patches.FancyBboxPatch((0.8, 1.1), 4.2, 2.4, boxstyle="round,pad=0.1", 
                                  edgecolor="#38BDF8", facecolor="#FFFFFF", linewidth=1)
    ax.add_patch(a_box)
    ax.text(1.0, 3.2, "Collection: 'accounts' & 'alerts'", fontsize=10, fontweight='bold', color="#0F172A")
    a_text = """• account_id: String (Primary Key)
• customer_name: String
• kyc_level: 'TIER_1' | 'TIER_2' | 'TIER_3'
• risk_tier: 'LOW' | 'MEDIUM' | 'HIGH'
• linked_devices: Array<String>
• total_volume: Decimal128
• alerts: [{ alert_id, rule, timestamp }]"""
    ax.text(1.0, 2.1, a_text, fontsize=8.5, va='center', color="#334155", fontfamily='monospace')

    # Graph Entities (Right)
    graph_box = patches.FancyBboxPatch((6.7, 0.8), 4.8, 6.4, boxstyle="round,pad=0.2", 
                                      edgecolor="#16A34A", facecolor="#F0FDF4", linewidth=1.5)
    ax.add_patch(graph_box)
    ax.text(9.1, 6.8, "Neo4j / Property Graph Entities", fontsize=12, fontweight='bold', ha='center', color="#15803D")

    # Graph Nodes & Edges Visual
    # Account Node 1
    circle1 = patches.Circle((7.8, 5.2), 0.55, facecolor="#BBF7D0", edgecolor="#16A34A", linewidth=1.5)
    ax.add_patch(circle1)
    ax.text(7.8, 5.2, "Account A\n(Node)", fontsize=8, ha='center', va='center', fontweight='bold', color="#14532D")

    # Account Node 2
    circle2 = patches.Circle((10.4, 5.2), 0.55, facecolor="#BBF7D0", edgecolor="#16A34A", linewidth=1.5)
    ax.add_patch(circle2)
    ax.text(10.4, 5.2, "Account B\n(Node)", fontsize=8, ha='center', va='center', fontweight='bold', color="#14532D")

    # Device Node
    circle3 = patches.Circle((9.1, 3.8), 0.55, facecolor="#FEF08A", edgecolor="#CA8A04", linewidth=1.5)
    ax.add_patch(circle3)
    ax.text(9.1, 3.8, "Device D1\n(Shared)", fontsize=8, ha='center', va='center', fontweight='bold', color="#713F12")

    # Account Node 3
    circle4 = patches.Circle((9.1, 2.0), 0.55, facecolor="#BBF7D0", edgecolor="#16A34A", linewidth=1.5)
    ax.add_patch(circle4)
    ax.text(9.1, 2.0, "Account C\n(Mule)", fontsize=8, ha='center', va='center', fontweight='bold', color="#14532D")

    # Edges
    ax.annotate('', xy=(9.8, 5.2), xytext=(8.4, 5.2),
                arrowprops=dict(facecolor='#15803D', edgecolor='#15803D', arrowstyle='->', lw=1.8))
    ax.text(9.1, 5.4, "TRANSFERRED_TO\n{amount, time}", fontsize=7.5, ha='center', color="#15803D", fontweight='bold')

    ax.annotate('', xy=(8.0, 4.7), xytext=(8.7, 4.1),
                arrowprops=dict(facecolor='#CA8A04', edgecolor='#CA8A04', arrowstyle='<-', lw=1.5, linestyle='--'))
    ax.text(8.0, 4.2, "LOGGED_IN", fontsize=7, color="#713F12")

    ax.annotate('', xy=(10.2, 4.7), xytext=(9.5, 4.1),
                arrowprops=dict(facecolor='#CA8A04', edgecolor='#CA8A04', arrowstyle='<-', lw=1.5, linestyle='--'))
    ax.text(10.2, 4.2, "LOGGED_IN", fontsize=7, color="#713F12")

    ax.annotate('', xy=(9.1, 2.6), xytext=(9.1, 3.2),
                arrowprops=dict(facecolor='#CA8A04', edgecolor='#CA8A04', arrowstyle='->', lw=1.5, linestyle='--'))

    ax.annotate('', xy=(8.6, 2.2), xytext=(7.6, 4.6),
                arrowprops=dict(facecolor='#DC2626', edgecolor='#DC2626', arrowstyle='->', lw=1.8))
    ax.text(7.6, 3.2, "CYCLE_EDGE", fontsize=7.5, color="#DC2626", fontweight='bold', rotation=60)

    # Cross Link
    ax.annotate('', xy=(6.7, 4.5), xytext=(5.3, 4.5),
                arrowprops=dict(facecolor='#6366F1', edgecolor='#6366F1', arrowstyle='<->', lw=2))
    ax.text(6.0, 4.7, "Hybrid Sync", fontsize=8, ha='center', color="#4338CA", fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_workflow_flowchart(output_path):
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F8FAFC")

    ax.text(5, 9.6, "FraudShield: Transaction Processing & Risk Workflow", 
            fontsize=14, fontweight='bold', ha='center', va='center', color="#0F172A")

    steps = [
        ("1. Transaction Ingestion", "Incoming JSON payload via REST / WebSocket endpoint", "#E0F2FE", "#0284C7", 8.6),
        ("2. Schema Validation & Normalization", "FastAPI Pydantic validation & Device Fingerprinting", "#FEF3C7", "#D97706", 7.3),
        ("3. Dual NoSQL Storage & Sync", "Insert into MongoDB Document Store & update Graph Network", "#F3E8FF", "#9333EA", 6.0),
        ("4. Real-Time Risk Analysis", "Evaluate 4 Vectors: Velocity, Graph Cycles, Device Sharing, Amount", "#DCFCE7", "#16A34A", 4.7),
        ("5. Decision & Fraud Scoring Rule", "Calculate Aggregate Risk Score $S \in [0, 100]$", "#FCE7F3", "#DB2777", 3.4),
    ]

    for title, desc, f_color, b_color, y_pos in steps:
        rect = patches.FancyBboxPatch((1.5, y_pos - 0.45), 7.0, 0.9, boxstyle="round,pad=0.15", 
                                      edgecolor=b_color, facecolor=f_color, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(5.0, y_pos + 0.15, title, fontsize=10, fontweight='bold', ha='center', color="#0F172A")
        ax.text(5.0, y_pos - 0.18, desc, fontsize=8.5, ha='center', color="#334155")

    # Arrows between main steps
    for y_top in [8.15, 6.85, 5.55, 4.25]:
        ax.annotate('', xy=(5.0, y_top - 0.4), xytext=(5.0, y_top),
                    arrowprops=dict(facecolor='#475569', edgecolor='#475569', arrowstyle='->', lw=1.8))

    # Branching Outcomes
    # Decision Arrow split
    ax.annotate('', xy=(2.5, 2.0), xytext=(4.0, 2.95),
                arrowprops=dict(facecolor='#16A34A', edgecolor='#16A34A', arrowstyle='->', lw=1.8))
    ax.annotate('', xy=(5.0, 2.0), xytext=(5.0, 2.95),
                arrowprops=dict(facecolor='#D97706', edgecolor='#D97706', arrowstyle='->', lw=1.8))
    ax.annotate('', xy=(7.5, 2.0), xytext=(6.0, 2.95),
                arrowprops=dict(facecolor='#DC2626', edgecolor='#DC2626', arrowstyle='->', lw=1.8))

    # Outcome Boxes
    # Low Risk
    b1 = patches.FancyBboxPatch((1.0, 1.0), 2.4, 0.9, boxstyle="round,pad=0.1", 
                                edgecolor="#16A34A", facecolor="#DCFCE7", linewidth=1.5)
    ax.add_patch(b1)
    ax.text(2.2, 1.6, "SCORE < 40: APPROVE", fontsize=8.5, fontweight='bold', ha='center', color="#14532D")
    ax.text(2.2, 1.25, "Execute instantly\nLog to MongoDB", fontsize=7.5, ha='center', color="#1E293B")

    # Medium Risk
    b2 = patches.FancyBboxPatch((3.8, 1.0), 2.4, 0.9, boxstyle="round,pad=0.1", 
                                edgecolor="#D97706", facecolor="#FEF3C7", linewidth=1.5)
    ax.add_patch(b2)
    ax.text(5.0, 1.6, "40 ≤ SCORE < 75: 2FA / REVIEW", fontsize=8.2, fontweight='bold', ha='center', color="#78350F")
    ax.text(5.0, 1.25, "Trigger OTP / Challenge\nFlag for Analyst", fontsize=7.5, ha='center', color="#1E293B")

    # High Risk
    b3 = patches.FancyBboxPatch((6.6, 1.0), 2.4, 0.9, boxstyle="round,pad=0.1", 
                                edgecolor="#DC2626", facecolor="#FEE2E2", linewidth=1.5)
    ax.add_patch(b3)
    ax.text(7.8, 1.6, "SCORE ≥ 75: BLOCK & ALERT", fontsize=8.5, fontweight='bold', ha='center', color="#7F1D1D")
    ax.text(7.8, 1.25, "Freeze transaction\nBroadcast WebSocket alert", fontsize=7.5, ha='center', color="#1E293B")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    diagrams_dir = os.path.dirname(os.path.abspath(__file__)) + "/diagrams"
    os.makedirs(diagrams_dir, exist_ok=True)
    create_system_architecture_diagram(os.path.join(diagrams_dir, "system_architecture.png"))
    create_data_model_diagram(os.path.join(diagrams_dir, "database_data_model.png"))
    create_workflow_flowchart(os.path.join(diagrams_dir, "workflow_flowchart.png"))
    print("All 3 diagrams successfully generated in:", diagrams_dir)
