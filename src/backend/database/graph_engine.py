"""
Graph NoSQL Engine for FraudShield.
Implements Index-Free Adjacency property graph traversal, cycle detection for laundering loops,
shared device clusters, and mule network identification.
"""

import networkx as nx
from typing import List, Dict, Any, Optional, Set, Tuple
from datetime import datetime, timezone, timedelta
import logging

logger = logging.getLogger("fraudshield.graph")

class FraudGraphEngine:
    def __init__(self):
        # DiGraph for directed payment flows
        self.tx_graph = nx.MultiDiGraph()
        # Heterogeneous Graph for Account <-> Device <-> IP relationships
        self.entity_graph = nx.Graph()

    def clear(self):
        self.tx_graph.clear()
        self.entity_graph.clear()

    def add_transaction(self, sender: str, receiver: str, amount: float, tx_id: str, 
                        timestamp: Optional[datetime] = None, device_id: Optional[str] = None, 
                        ip_address: Optional[str] = None):
        ts = timestamp or datetime.now(timezone.utc)
        
        # Ensure Nodes exist in Transaction Graph
        if not self.tx_graph.has_node(sender):
            self.tx_graph.add_node(sender, type="account", total_sent=0.0, total_received=0.0, tx_count=0)
        if not self.tx_graph.has_node(receiver):
            self.tx_graph.add_node(receiver, type="account", total_sent=0.0, total_received=0.0, tx_count=0)

        # Update node statistics
        self.tx_graph.nodes[sender]["total_sent"] += amount
        self.tx_graph.nodes[sender]["tx_count"] += 1
        self.tx_graph.nodes[receiver]["total_received"] += amount
        self.tx_graph.nodes[receiver]["tx_count"] += 1

        # Add directed payment edge
        self.tx_graph.add_edge(sender, receiver, key=tx_id, amount=amount, timestamp=ts, tx_id=tx_id)

        # Entity Graph (Heterogeneous relationships)
        self.entity_graph.add_node(sender, type="account")
        self.entity_graph.add_node(receiver, type="account")

        if device_id:
            self.entity_graph.add_node(device_id, type="device")
            self.entity_graph.add_edge(sender, device_id, relation="LOGGED_IN", last_seen=ts)
        
        if ip_address:
            self.entity_graph.add_node(ip_address, type="ip")
            self.entity_graph.add_edge(sender, ip_address, relation="CONNECTED_FROM", last_seen=ts)

    def find_cycles_involving_transaction(self, sender: str, receiver: str, max_depth: int = 5) -> List[List[str]]:
        """
        Detects if adding an edge from sender -> receiver completes a circular flow:
        receiver -> ... -> sender.
        Uses depth-bounded traversal to guarantee millisecond latency.
        """
        if not self.tx_graph.has_node(receiver) or not self.tx_graph.has_node(sender):
            return []

        cycles = []
        try:
            # Look for paths from receiver back to sender
            for path in nx.all_simple_paths(self.tx_graph, source=receiver, target=sender, cutoff=max_depth - 1):
                full_cycle = [sender] + path
                cycles.append(full_cycle)
                if len(cycles) >= 5: # Limit returned cycles for performance
                    break
        except Exception as e:
            logger.error("Error finding cycles: %s", e)
        return cycles

    def find_all_fraud_rings(self, min_length: int = 3, max_length: int = 6) -> List[Dict[str, Any]]:
        """Finds all circular payment rings in the current graph."""
        detected_rings = []
        try:
            simple_cycles = list(nx.simple_cycles(self.tx_graph))
            for cycle in simple_cycles:
                if min_length <= len(cycle) <= max_length:
                    # Calculate total transaction volume within cycle
                    total_amount = 0.0
                    for i in range(len(cycle)):
                        u = cycle[i]
                        v = cycle[(i + 1) % len(cycle)]
                        edge_data = self.tx_graph.get_edge_data(u, v)
                        if edge_data:
                            for k, attrs in edge_data.items():
                                total_amount += attrs.get("amount", 0.0)

                    detected_rings.append({
                        "ring_nodes": cycle,
                        "ring_length": len(cycle),
                        "total_volume": round(total_amount, 2),
                        "severity": "CRITICAL" if total_amount > 50000 else "HIGH"
                    })
        except Exception as e:
            logger.error("Error detecting fraud rings: %s", e)
        return detected_rings

    def get_shared_device_accounts(self, device_id: str) -> List[str]:
        """Finds all accounts that have logged in from a specific device."""
        if not self.entity_graph.has_node(device_id):
            return []
        neighbors = self.entity_graph.neighbors(device_id)
        return [n for n in neighbors if self.entity_graph.nodes[n].get("type") == "account"]

    def find_all_mule_networks(self, fan_in_threshold: int = 3, fan_out_threshold: int = 3) -> List[Dict[str, Any]]:
        """
        Identifies money mules: Accounts receiving funds from multiple distinct sources
        and rapidly routing them out to multiple targets or collectors.
        """
        mules = []
        for node, data in self.tx_graph.nodes(data=True):
            in_degree = self.tx_graph.in_degree(node)
            out_degree = self.tx_graph.out_degree(node)
            
            if in_degree >= fan_in_threshold or (in_degree >= 2 and out_degree >= 2):
                sources = list(self.tx_graph.predecessors(node))
                destinations = list(self.tx_graph.successors(node))
                mules.append({
                    "mule_account": node,
                    "in_degree": in_degree,
                    "out_degree": out_degree,
                    "incoming_sources": sources,
                    "outgoing_destinations": destinations,
                    "total_received": round(data.get("total_received", 0.0), 2),
                    "total_sent": round(data.get("total_sent", 0.0), 2)
                })
        return mules

    def get_visjs_graph_data(self, max_nodes: int = 80) -> Dict[str, Any]:
        """Exports graph data formatted for Vis.js interactive frontend canvas."""
        nodes = []
        edges = []
        node_set = set()

        # Add most active transaction nodes
        sorted_nodes = sorted(
            self.tx_graph.nodes(data=True), 
            key=lambda x: x[1].get("tx_count", 0), 
            reverse=True
        )[:max_nodes]

        for node_id, data in sorted_nodes:
            node_set.add(node_id)
            nodes.append({
                "id": node_id,
                "label": node_id,
                "group": "account",
                "title": f"Account: {node_id}<br/>Sent: ₹{data.get('total_sent', 0):,.2f}<br/>Recv: ₹{data.get('total_received', 0):,.2f}",
                "value": data.get("tx_count", 1) + 5
            })

        # Add connected device nodes
        for u, v, d in self.entity_graph.edges(data=True):
            if u in node_set and self.entity_graph.nodes[v].get("type") == "device":
                if v not in node_set:
                    node_set.add(v)
                    nodes.append({
                        "id": v,
                        "label": f"📱 {v[:8]}",
                        "group": "device",
                        "title": f"Device: {v}",
                        "value": 4
                    })
                edges.append({
                    "from": u,
                    "to": v,
                    "dashes": True,
                    "color": {"color": "#EAB308"},
                    "title": "LOGGED_IN"
                })

        # Add transaction edges
        for u, v, key, data in self.tx_graph.edges(keys=True, data=True):
            if u in node_set and v in node_set:
                edges.append({
                    "from": u,
                    "to": v,
                    "label": f"₹{data.get('amount', 0):,.0f}",
                    "arrows": "to",
                    "color": {"color": "#0284C7"},
                    "title": f"TxID: {data.get('tx_id')}<br/>Amount: ₹{data.get('amount', 0)}"
                })

        return {"nodes": nodes, "edges": edges, "total_nodes": len(self.tx_graph.nodes), "total_edges": len(self.tx_graph.edges)}

# Global singleton instance
graph_engine = FraudGraphEngine()
