import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict

import src.utils.helpers as helpers

def create_network_graph(
    tags: Dict[str, str],
    stereotypes: Dict[str, str],
    df: pd.DataFrame,
    file_name: str,
    model_name: str,
):
    """
    Create and plot a network graph based on similarity scores between tags and stereotypes.

    Parameters:
    - tags (Dict[str, str]): A dictionary where keys are tag names and values are their descriptions.
    - stereotypes (Dict[str, str]): A dictionary where keys are stereotype names and values are their descriptions.
    - sim (pd.DataFrame): A DataFrame containing the cosine similarity scores between tags and stereotypes.
    - file_name (str): The name of the file to save the network graph plot.

    The function generates a network graph where nodes represent tags and stereotypes, and edges represent the similarity scores between them. Nodes are grouped by type (tag or stereotype), and edge thickness is proportional to the similarity score.
    """
    helpers.ensure_directory_exists("plots")
    G = nx.Graph()
    G.add_nodes_from(tags.keys(), bipartite=0)
    G.add_nodes_from(stereotypes.keys(), bipartite=1)
    for i, tag in enumerate(tags.keys()):
        for j, stereotype in enumerate(stereotypes.keys()):
            weight = df.iloc[i, j]
            if weight > 0.3:
                G.add_edge(tag, stereotype, weight=weight)
    pos = nx.spring_layout(G, k=0.5, iterations=50)
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
    
    nx.draw_networkx_edges(
        G, pos, edge_color=weights, edge_cmap=plt.get_cmap("Blues"), width=2
    )
    plt.title("Network Graph of Cosine Similarity between Tags and Stereotypes")
    plt.savefig(f"plots/{file_name}_{model_name}")
    plt.show()