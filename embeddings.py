import json
import logging
from typing import Dict, List

import matplotlib.pyplot as plt
import networkx as nx
import nltk
import pandas as pd
import seaborn as sns
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Constants for file paths
STEREOTYPES_JSON_PATH = "stereotypes.json"
TAGS_JSON_PATH = "tags.json"
PLOTS_PATH = "plots/"

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def download_nltk_data():
    """Download necessary NLTK data if not already present."""
    nltk_data = ["stopwords", "punkt"]
    for data in nltk_data:
        try:
            nltk.data.find(f"tokenizers/{data}")
        except LookupError:
            nltk.download(data)


def preprocess(text: str) -> str:
    """Tokenize and clean the text by removing stopwords and non-alphabetic tokens."""
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text.lower())
    return " ".join(
        [word for word in tokens if word.isalpha() and word not in stop_words]
    )


def load_and_preprocess_data(file_path: str) -> Dict[str, str]:
    """Load and preprocess data from a JSON file."""
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return {key: preprocess(text) for key, text in data.items()}
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        return {}


def generate_embeddings(texts: Dict[str, str]) -> Dict[str, List[float]]:
    """Generate embeddings for preprocessed texts."""
    model = SentenceTransformer("bert-base-nli-mean-tokens")
    return {key: model.encode([text])[0] for key, text in texts.items()}


def calculate_similarity(
    tags_emb: Dict[str, List[float]], stereotypes_emb: Dict[str, List[float]]
) -> pd.DataFrame:
    """Calculate cosine similarity between tags and stereotypes embeddings."""
    tags_keys, tags_values = zip(*tags_emb.items())
    stereotypes_keys, stereotypes_values = zip(*stereotypes_emb.items())
    sim_matrix = cosine_similarity(list(tags_values), list(stereotypes_values))
    return pd.DataFrame(sim_matrix, index=tags_keys, columns=stereotypes_keys)


def plot_heatmap(sim_df: pd.DataFrame):
    """Plot a heatmap based on the similarity DataFrame."""
    plt.figure(figsize=(10, 8))
    sns.heatmap(sim_df, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Cosine Similarity between Videos and Stereotypes")
    plt.xlabel("Stereotypes")
    plt.ylabel("Videos")
    plt.savefig(f"{PLOTS_PATH}video_stereotype_heatmap.png")
    plt.show()


def create_network_graph(
    tags: Dict[str, str], stereotypes: Dict[str, str], sim: pd.DataFrame
):
    """Create and plot a network graph based on similarity scores."""
    G = nx.Graph()
    G.add_nodes_from(tags.keys(), bipartite=0)
    G.add_nodes_from(stereotypes.keys(), bipartite=1)
    for i, tag in enumerate(tags.keys()):
        for j, stereotype in enumerate(stereotypes.keys()):
            weight = sim.iloc[i, j]
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
    nx.draw_networkx_edges(G, pos, edge_color=weights, edge_cmap=plt.cm.Blues, width=2)
    plt.title("Network Graph of Cosine Similarity between Tags and Stereotypes")
    plt.savefig(f"{PLOTS_PATH}video_stereotype_graph.png")
    plt.show()


if __name__ == "__main__":
    download_nltk_data()
    stereotypes = load_and_preprocess_data(STEREOTYPES_JSON_PATH)
    tags = load_and_preprocess_data(TAGS_JSON_PATH)
    stereotypes_emb = generate_embeddings(stereotypes)
    tags_emb = generate_embeddings(tags)
    sim_df = calculate_similarity(tags_emb, stereotypes_emb)
    plot_heatmap(sim_df)
    create_network_graph(tags, stereotypes, sim_df)
