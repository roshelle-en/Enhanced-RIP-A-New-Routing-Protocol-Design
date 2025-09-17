import heapq
import time

# ------------------ Compound Cost Calculation ------------------ #
def calculate_compound_cost(hop_count, bandwidth, delay, jitter=0, packet_loss=0,
                            a0=1, a1=1, a2=1, a3=0, a4=0):
    """
    Calculate the compound cost metric.

    Metric = a0 * HopCount + a1 * (1 / Bandwidth) + a2 * Delay + a3 * Jitter + a4 * PacketLoss
    """
    inv_bandwidth = 1 / bandwidth if bandwidth > 0 else float("inf")
    return (a0 * hop_count) + (a1 * inv_bandwidth) + (a2 * delay) + (a3 * jitter) + (a4 * packet_loss)


# ------------------ Build Enhanced Routing Table ------------------ #
def build_routing_table(G, k=3, weights=(1, 1, 1, 0, 0)):
    """
    Build routing tables using compound cost.
    Each entry contains:
      - Primary next hop
      - Secondary next hop set (min-heap)

    Args:
        G: Graph with attributes (hop, bandwidth, delay, jitter, loss)
        k: Max number of secondary nodes to store
        weights: Tuple of (a0, a1, a2, a3, a4)

    Returns:
        dict: Routing tables with primary and secondary entries
    """
    a0, a1, a2, a3, a4 = weights
    tables = {}

    for node in G.nodes():
        tables[node] = {}
        for target in G.nodes():
            if node == target:
                continue

            candidates = []
            for neighbor in G.neighbors(node):
                edge = G[node][neighbor]
                comp_cost = calculate_compound_cost(
                    edge.get("hop", 1),
                    edge.get("bandwidth", 1),
                    edge.get("delay", 1),
                    edge.get("jitter", 0),
                    edge.get("loss", 0),
                    a0, a1, a2, a3, a4
                )
                heapq.heappush(candidates, (comp_cost, neighbor))

            if candidates:
                primary = heapq.heappop(candidates)
                secondary = candidates[:k]  # limit secondary nodes
                tables[node][target] = {
                    "primary": primary,
                    "secondary": secondary
                }
            else:
                tables[node][target] = {
                    "primary": None,
                    "secondary": []
                }

    return tables


# ------------------ Memory Optimization: Pruning ------------------ #
def prune_secondary_nodes(routing_table, timeout=90, current_time=None):
    """
    Removes secondary nodes that have not been used within timeout.

    Args:
        routing_table: Routing table with secondary node sets
        timeout: Time (seconds) after which unused entries are pruned
        current_time: Current timestamp (default = time.time())
    """
    if current_time is None:
        current_time = time.time()

    for node, entries in routing_table.items():
        for dest, entry in entries.items():
            if "secondary" in entry:
                entry["secondary"] = [
                    (cost, neighbor, ts) for cost, neighbor, ts in entry.get("secondary", [])
                    if current_time - ts <= timeout
                ]


# ------------------ Example Run ------------------ #
if __name__ == "__main__":
    import networkx as nx

    # Create sample graph
    G = nx.Graph()
    G.add_node("A")
    G.add_node("B")
    G.add_node("C")
    edges = [
        ("A", "B", {"hop": 1, "bandwidth": 10, "delay": 5}),
        ("A", "C", {"hop": 1, "bandwidth": 5, "delay": 10}),
        ("B", "C", {"hop": 1, "bandwidth": 20, "delay": 2}),
    ]
    G.add_edges_from(edges)

    # Build routing tables
    routing_tables = build_routing_table(G, k=2, weights=(1, 1, 1, 0, 0))

    # Print results
    for node, table in routing_tables.items():
        print(f"Router {node} routing table:")
        for dest, entry in table.items():
            print(f"  To {dest} - Primary: {entry['primary']}, Secondary: {entry['secondary']}")
        print()
