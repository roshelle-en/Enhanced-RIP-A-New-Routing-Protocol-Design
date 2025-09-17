import networkx as nx
import matplotlib.pyplot as plt

# Create a sample undirected graph
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

# Draw the network
pos = nx.spring_layout(G, seed=42)
edge_labels = nx.get_edge_attributes(G, 'weight')

plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_color='skyblue',
        node_size=1500, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Initial Network Topology")
plt.show()
