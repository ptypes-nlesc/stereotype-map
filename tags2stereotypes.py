"""
Link each stereotype to a list of tags and show their similarity
Steps:
1. text preprocessing;
2. embedding generation for stereotypes and tags using pre-trained embeddings,
3. similarity calculation using cosine similarity,
4. visualization?
"""

import json
import string

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("stopwords")
nltk.download("punkt")


# text tokenization
def preprocess(text):
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    return " ".join(tokens)


with open("data/stereotypes.json", "r") as file:
    stereotypes = json.load(file)

stereotypes = [preprocess(stype) for stype in stereotypes]

with open("data/tags.json", "r") as file:
    tags = json.load(file)

tags = [preprocess(tag) for tag in tags]

# word embeddings
# pre-trained BERT or Word2Vec/GloVe??

from sentence_transformers import SentenceTransformer

# Load pre-trained model
model = SentenceTransformer("bert-base-nli-mean-tokens")

# Generate embeddings
stereotype_emb = model.encode(stereotypes)
tag_emb = model.encode(tags)

# Calculate cosine similarity

from sklearn.metrics.pairwise import cosine_similarity

# Compute similarities
sim = cosine_similarity(stereotype_emb, tag_emb)
from scipy.spatial.distance import cdist

similarities = 1 - cdist(tag_embeddings, stereotype_embeddings, metric="cosine")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# temporary tags and stereotypes
s = ["a", "b", "c", "d", "e", "f", "g"]
t = ["a", "b", "c", "d", "e", "f", "g"]

# Convert similarities to a DataFrame for better visualization
similarity_df = pd.DataFrame(similarities, index=t, columns=s)

# Plot the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(similarity_df, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Cosine Similarity between Tags and Stereotypes")
plt.xlabel("Stereotypes")
plt.ylabel("Tags")
plt.show()

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
