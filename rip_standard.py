import copy
import time

def simulate_rip(G, max_iterations=50, verbose=False):
    """
    Simulates the standard RIP algorithm using hop count as the only metric.

    Parameters:
        G (networkx.Graph): Input graph with weighted edges
        max_iterations (int): Maximum iterations for convergence
        verbose (bool): Print convergence details

    Returns:
        routing_tables (dict): Final routing tables for all nodes
        iterations (int): Number of iterations until convergence
    """
    # Initialize routing tables
    routing_tables = {
        node: {n: (float('inf'), None) for n in G.nodes()} for node in G.nodes()
    }

    for node in G.nodes():
        routing_tables[node][node] = (0, node)
        for neighbor in G.neighbors(node):
            cost = G[node][neighbor]['weight']
            routing_tables[node][neighbor] = (cost, neighbor)

    history = []
    for iteration in range(max_iterations):
        changes = 0
        history.append(copy.deepcopy(routing_tables))

        for u in G.nodes():
            for v in G.nodes():
                if u == v:
                    continue
                for neighbor in G.neighbors(u):
                    cost_to_neighbor = routing_tables[u][neighbor][0]
                    cost_neighbor_to_v = routing_tables[neighbor][v][0]
                    total_cost = cost_to_neighbor + cost_neighbor_to_v

                    if total_cost < routing_tables[u][v][0]:
                        routing_tables[u][v] = (total_cost, neighbor)
                        changes += 1

        if verbose:
            print(f"Iteration {iteration + 1}: {changes} changes")

        if changes == 0:
            return routing_tables, iteration + 1

    return routing_tables, max_iterations


if __name__ == "__main__":
    import networkx as nx

    # Example graph
    G = nx.Graph()
    edges = [
        ('A', 'B', 1),
        ('A', 'C', 5),
        ('B', 'C', 2),
        ('B', 'D', 4),
        ('C', 'D', 1),
        ('C', 'E', 3),
        ('D', 'E', 1)
    ]
    G.add_weighted_edges_from(edges)

    start = time.time()
    final_routing, convergence_time = simulate_rip(G, verbose=True)
    end = time.time()

    print(f"\nRIP converged in {convergence_time} iterations (Time: {end - start:.4f} seconds)\n")

    # Pretty print routing table
    for node, table in final_routing.items():
        print(f"Routing table for {node}:")
        for dest, (cost, via) in table.items():
            print(f"  to {dest} via {via} cost {cost}")
        print()
