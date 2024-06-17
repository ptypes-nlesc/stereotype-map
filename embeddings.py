"""
Link each stereotype to a list of tags and show their similarity via word embeddings
Steps:
1. text preprocessing;
2. embedding generation for stereotypes and tags using pre-trained embeddings,
3. similarity calculation using cosine similarity,
4. visualization?
"""

import json

import matplotlib.pyplot as plt
import nltk
import pandas as pd
import seaborn as sns
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("stopwords")
nltk.download("punkt")


# text tokenization
def preprocess(text):
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    return " ".join(tokens)


# load data
with open("stereotypes.json", "r") as file:
    stereotypes = json.load(file)

stereotypes_v = [preprocess(stype) for stype in stereotypes.values()]

with open("tags.json", "r") as file:
    tags = json.load(file)

tags_v = [preprocess(tag) for tag in tags.values()]

# word embeddings
# pre-trained BERT
# Other options are Word2Vec (skip-gram), GloVe, FastText, etc.

# Load pre-trained model
model = SentenceTransformer("bert-base-nli-mean-tokens")

# Generate embeddings
stereotypes_emb = model.encode(stereotypes_v)
tags_emb = model.encode(tags_v)

# Calculate cosine similarity
# Compute similarities
sim = cosine_similarity(tags_emb, stereotypes_emb)

# Convert similarities to a DataFrame for better visualization
sim_df = pd.DataFrame(sim, index=tags.keys(), columns=stereotypes.keys())

# Plot the heatmap of similarities
plt.figure(figsize=(10, 8))
sns.heatmap(sim_df, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Cosine Similarity between Videos and Stereotypes")
plt.xlabel("Stereotypes")
plt.ylabel("Videos")
plt.savefig("plots/video_sterotype_heatmap.png")
plt.show()
