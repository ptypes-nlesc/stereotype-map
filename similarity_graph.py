import networkx as nx

# Create a graph
G = nx.Graph()

tags = t
stereotypes = s

# Add nodes for tags and stereotypes
G.add_nodes_from(tags, bipartite=0)
G.add_nodes_from(stereotypes, bipartite=1)

# Add edges with weights based on similarity
for i, tag in enumerate(tags):
    for j, stereotype in enumerate(stereotypes):
        weight = similarities[i, j]
        if weight > 0.3:  # Only add edges with significant similarity
            G.add_edge(tag, stereotype, weight=weight)

# Position nodes using bipartite layout
pos = nx.spring_layout(G, k=0.5, iterations=50)

# Draw the graph
plt.figure(figsize=(12, 8))
edges = G.edges(data=True)
weights = [edge[2]["weight"] for edge in edges]
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=3000,
    node_color="skyblue",
    font_size=10,
    font_weight="bold",
)
nx.draw_networkx_edges(G, pos, edge_color=weights, edge_cmap=plt.cm.Blues, width=2)
plt.title("Network Graph of Cosine Similarity between Tags and Stereotypes")
plt.show()
