/**
 * FraudShield Frontend Application Logic
 * Integrates Vis.js Network Graph, WebSockets stream, and NoSQL Inspector
 */

let network = null;
let networkData = { nodes: new vis.DataSet([]), edges: new vis.DataSet([]) };
let websocket = null;

document.addEventListener("DOMContentLoaded", () => {
    initGraph();
    fetchMetrics();
    fetchTransactions();
    fetchFraudInsights();
    initWebSocket();
});

// Initialize Vis.js Network Graph
function initGraph() {
    const container = document.getElementById("graph-network-view");
    
    const options = {
        nodes: {
            shape: "dot",
            font: { color: "#F9FAFB", size: 12, face: "system-ui" },
            borderWidth: 2,
            shadow: true
        },
        edges: {
            arrows: { to: { enabled: true, scaleFactor: 0.8 } },
            font: { color: "#94A3B8", size: 10, align: "middle" },
            smooth: { type: "continuous" },
            shadow: false
        },
        groups: {
            account: { color: { background: "#0284C7", border: "#38BDF8" } },
            device: { color: { background: "#EAB308", border: "#FEF08A" }, shape: "square" },
            ip: { color: { background: "#8B5CF6", border: "#C4B5FD" }, shape: "triangle" }
        },
        physics: {
            stabilization: { iterations: 100 },
            barnesHut: { gravitationalConstant: -3000, springLength: 95 }
        },
        interaction: { hover: true, tooltipDelay: 200 }
    };

    network = new vis.Network(container, networkData, options);

    network.on("click", function(params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            fetchNodeDetails(nodeId);
        }
    });

    refreshGraph();
}

// Fetch Graph Topology from NoSQL Backend
async function refreshGraph() {
    try {
        const res = await fetch("/api/graph/topology?max_nodes=60");
        const data = await res.json();

        networkData.nodes.clear();
        networkData.edges.clear();

        networkData.nodes.add(data.nodes);
        networkData.edges.add(data.edges);

        document.getElementById("graph-node-count").innerText = 
            `Nodes: ${data.total_nodes} | Edges: ${data.total_edges}`;
        
        network.fit();
    } catch (e) {
        console.error("Error refreshing graph:", e);
    }
}

// Fetch Metrics & KPI Cards
async function fetchMetrics() {
    try {
        const res = await fetch("/api/metrics");
        const data = await res.json();

        document.getElementById("total-txs-val").innerText = data.total_transactions;
        document.getElementById("total-vol-val").innerText = `Volume: ₹${data.total_volume.toLocaleString()}`;

        document.getElementById("blocked-txs-val").innerText = data.risk_breakdown.high_risk_blocked;
        const blockedPct = data.total_transactions > 0 
            ? ((data.risk_breakdown.high_risk_blocked / data.total_transactions) * 100).toFixed(1) 
            : 0;
        document.getElementById("blocked-rate-val").innerText = `${blockedPct}% interception rate`;

        document.getElementById("fraud-rings-val").innerText = data.graph_intelligence.active_fraud_rings;
        document.getElementById("mules-val").innerText = `${data.graph_intelligence.detected_mules} Mule Accounts Detected`;

        document.getElementById("latency-val").innerText = `${data.performance_latency.risk_inference_total_avg_ms} ms`;
        document.getElementById("db-status-text").innerText = `${data.database_status.engine} Active`;
    } catch (e) {
        console.error("Error fetching metrics:", e);
    }
}

// Fetch Recent Transactions Table
async function fetchTransactions() {
    try {
        const res = await fetch("/api/transactions?limit=25");
        const data = await res.json();
        const tbody = document.getElementById("tx-table-body");
        tbody.innerHTML = "";

        data.transactions.forEach(tx => renderTransactionRow(tx, false));
    } catch (e) {
        console.error("Error fetching transactions:", e);
    }
}

function renderTransactionRow(tx, prepend = true) {
    const tbody = document.getElementById("tx-table-body");
    const tr = document.createElement("tr");

    const evalData = tx.risk_evaluation || { risk_score: 0, classification: "LOW_RISK_APPROVE" };
    let badgeClass = "approve";
    let badgeText = "Approved";

    if (evalData.classification === "HIGH_RISK_BLOCK") {
        badgeClass = "block";
        badgeText = "Blocked";
    } else if (evalData.classification === "MEDIUM_RISK_CHALLENGE_2FA") {
        badgeClass = "challenge";
        badgeText = "2FA Required";
    }

    tr.innerHTML = `
        <td style="font-family: var(--font-mono); font-weight: bold; color: var(--accent-blue-light);">${tx.transaction_id || tx.id}</td>
        <td>${tx.sender_account} &rarr; ${tx.receiver_account}</td>
        <td style="font-weight: 600;">₹${Number(tx.amount).toLocaleString()}</td>
        <td><span class="risk-pill" style="color: ${evalData.risk_score > 70 ? '#EF4444' : (evalData.risk_score > 35 ? '#F59E0B' : '#10B981')}">${evalData.risk_score} / 100</span></td>
        <td><span class="badge-status ${badgeClass}">${badgeText}</span></td>
    `;

    tr.onclick = () => {
        document.getElementById("json-preview").innerText = JSON.stringify(tx, null, 2);
    };

    if (prepend && tbody.firstChild) {
        tbody.insertBefore(tr, tbody.firstChild);
        // Keep max 35 rows in view
        if (tbody.children.length > 35) {
            tbody.removeChild(tbody.lastChild);
        }
    } else {
        tbody.appendChild(tr);
    }
}

// Fetch Fraud Rings & Mule Networks
async function fetchFraudInsights() {
    try {
        const resRings = await fetch("/api/graph/fraud-rings");
        const dataRings = await resRings.json();

        const container = document.getElementById("fraud-rings-container");
        container.innerHTML = "";

        if (dataRings.fraud_rings && dataRings.fraud_rings.length > 0) {
            dataRings.fraud_rings.forEach((ring, idx) => {
                const card = document.createElement("div");
                card.className = "fraud-ring-card";
                card.innerHTML = `
                    <div class="ring-header">
                        <span><i data-lucide="shield-alert"></i> Circular Ring #${idx + 1} (${ring.ring_length} Hops)</span>
                        <span>Total Volume: ₹${ring.total_volume.toLocaleString()}</span>
                    </div>
                    <div class="ring-nodes">${ring.ring_nodes.join(" &rarr; ")} &rarr; ${ring.ring_nodes[0]}</div>
                `;
                container.appendChild(card);
            });
        } else {
            container.innerHTML = `<div class="empty-state">No circular loops detected in current graph topology.</div>`;
        }

        if (window.lucide) {
            lucide.createIcons();
        }
    } catch (e) {
        console.error("Error fetching fraud insights:", e);
    }
}

// Trigger Synthetic Fraud Scenario
async function injectScenario(scenario, count) {
    try {
        const res = await fetch(`/api/simulator/generate?scenario=${scenario}&count=${count}`, {
            method: "POST"
        });
        const result = await res.json();
        console.log("Injected scenario:", result);
        
        await refreshGraph();
        await fetchMetrics();
        await fetchFraudInsights();
    } catch (e) {
        console.error("Error triggering scenario:", e);
    }
}

// Reset Database & Graph State
async function resetDatabase() {
    if (confirm("Reset all MongoDB collections and Neo4j graph nodes?")) {
        try {
            await fetch("/api/reset", { method: "POST" });
            networkData.nodes.clear();
            networkData.edges.clear();
            document.getElementById("tx-table-body").innerHTML = "";
            document.getElementById("json-preview").innerText = "// Database reset complete.";
            await fetchMetrics();
            await fetchFraudInsights();
        } catch (e) {
            console.error("Error resetting database:", e);
        }
    }
}

// WebSocket Stream Connection
function initWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/ws/stream`;

    try {
        websocket = new WebSocket(wsUrl);

        websocket.onopen = () => {
            console.log("Connected to FraudShield live stream.");
        };

        websocket.onmessage = (event) => {
            const msg = JSON.parse(event.data);
            if (msg.event === "NEW_TRANSACTION") {
                renderTransactionRow(msg.data, true);
                fetchMetrics();
            }
        };

        websocket.onclose = () => {
            console.log("WebSocket closed. Reconnecting in 3s...");
            setTimeout(initWebSocket, 3000);
        };
    } catch (e) {
        console.error("WebSocket init error:", e);
    }
}

function triggerSimModal() {
    injectScenario('normal', 3);
}
