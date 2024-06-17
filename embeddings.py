"""
Link each stereotype to a list of tags and show their similarity via word embeddings
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


# load data
with open("data/stereotypes.json", "r") as file:
    stereotypes = json.load(file)

stereotypes = [preprocess(stype) for stype in stereotypes]

with open("data/tags.json", "r") as file:
    tags = json.load(file)

tags = [preprocess(tag) for tag in tags]

# word embeddings
# pre-trained BERT
# Other options are Word2Vec (skip-gram), GloVe, FastText, etc.

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

# another way to calculate cosine similarity
similarities = 1 - cdist(tag_emb, stereotype_emb, metric="cosine")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# temporary tags and stereotypes
s = ["1", "2", "3", "4", "5", "6", "7"]
t = ["a", "b", "c", "d", "e", "f", "g", "h"]

# Convert similarities to a DataFrame for better visualization
similarity_df = pd.DataFrame(similarities, index=t, columns=s)

# Plot the heatmap of similarities
plt.figure(figsize=(10, 8))
sns.heatmap(similarity_df, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Cosine Similarity between Tags and Stereotypes")
plt.xlabel("Stereotypes")
plt.ylabel("Tags")
plt.show()

