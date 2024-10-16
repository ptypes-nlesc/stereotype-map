"""
Determine the similarity between video tags and predefined stereotypes by leveraging word embeddings
"""

import json
import logging
import os
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

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def ensure_directory_exists(directory: str):
    """Ensure that a directory exists; if not, create it."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def download_nltk_data():
    """Download necessary NLTK data if not already present."""
    nltk_data = ["stopwords", "punkt"]
    for data in nltk_data:
        try:
            nltk.data.find(f"tokenizers/{data}")
        except LookupError:
            nltk.download(data)


def preprocess(text: str) -> str:
    """
    Tokenize and clean the input text by removing stopwords and non-alphabetic tokens.

    Parameters:
    - text (str): The input text to be preprocessed.

    Returns:
    - str: The preprocessed text, with stopwords and non-alphabetic tokens removed.
    """
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text.lower())
    return " ".join(
        [word for word in tokens if word.isalpha() and word not in stop_words]
    )


def load_and_preprocess_data(file_path: str) -> Dict[str, str]:
    """Load and preprocess data from a JSON file.

    Parameters:
    - file_path (str): The path to the JSON file to be loaded and processed.

    Returns:
    - Dict[str, str]: A dictionary containing the original keys from the JSON
    file and their associated preprocessed text values.
    If the file is not found, an empty dictionary is returned.

    Raises:
    - FileNotFoundError: If the specified file does not exist, a logging error
    is recorded, and an empty dictionary is returned.
    """
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            data = json.load(file)
        return {key: preprocess(text) for key, text in data.items()}
    except FileNotFoundError:
        logging.error("File %s not found.", file_path)
        return {}


def generate_embeddings(
    texts: Dict[str, str], model_name: str
) -> Dict[str, List[float]]:
    """Generate embeddings for a dictionary of texts."""
    try:
        model = SentenceTransformer(model_name)
        return {
            key: model.encode(text, show_progress_bar=False).tolist()
            for key, text in texts.items()
        }
    except Exception as e:
        logging.error("Error loading model: %s", e)
        return {}


def calculate_similarity(
    tags_emb: Dict[str, List[float]], stereotypes_emb: Dict[str, List[float]]
) -> pd.DataFrame:
    """
    Calculate cosine similarity between the two sets of embeddings.
        Parameters:
    - tags_emb (Dict[str, List[float]]): A dictionary where the keys are tag identifiers and the values are the embeddings of the tags.
    - stereotypes_emb (Dict[str, List[float]]): A dictionary where the keys are stereotype identifiers and the values are the embeddings of the stereotypes.

    Returns:
    - pd.DataFrame: A DataFrame containing the cosine similarity scores between tags and stereotypes. The rows are indexed by tag identifiers, and the columns are labeled with stereotype identifiers.

    """
    tags_keys, tags_values = zip(*tags_emb.items())
    stereotypes_keys, stereotypes_values = zip(*stereotypes_emb.items())
    sim_matrix = cosine_similarity(tags_values, stereotypes_values)
    return pd.DataFrame(sim_matrix, index=tags_keys, columns=stereotypes_keys)


def plot_heatmap(df: pd.DataFrame, file_name: str, model_name: str):
    ensure_directory_exists("plots")
    plt.figure(figsize=(10, 8))
    sns.heatmap(df, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Cosine Similarity between Videos and Stereotypes")
    plt.xlabel("Stereotypes")
    plt.ylabel("Videos")
    plt.savefig(f"plots/{file_name}_{model_name}")
    plt.show()


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
    ensure_directory_exists("plots")
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
    nx.draw_networkx_edges(G, pos, edge_color=weights, edge_cmap=plt.cm.Blues, width=2)
    plt.title("Network Graph of Cosine Similarity between Tags and Stereotypes")
    plt.savefig(f"plots/{file_name}_{model_name}")
    plt.show()
