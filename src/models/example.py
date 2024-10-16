"""
Use the embeddings module to determine the similarity between video tags and predefined stereotypes for a given video
"""

import embeddings as emb

# Constants for file paths
STEREOTYPES_JSON_PATH = "stereotypes.json"
TAGS_JSON_PATH = "tags.json"
MODEL_NAME = "distilroberta-base-paraphrase-v1"

# TODO try different models
# e.g. "bert-base-nli-mean-tokens"

emb.download_nltk_data()
stereotypes = emb.load_and_preprocess_data(STEREOTYPES_JSON_PATH)
tags = emb.load_and_preprocess_data(TAGS_JSON_PATH)
stereotypes_emb = emb.generate_embeddings(texts=stereotypes, model_name=MODEL_NAME)
tags_emb = emb.generate_embeddings(texts=tags, model_name=MODEL_NAME)
df = emb.calculate_similarity(tags_emb, stereotypes_emb)
emb.plot_heatmap(df, "heatmap", model_name=MODEL_NAME)
emb.create_network_graph(tags, stereotypes, df, "network_graph", model_name=MODEL_NAME)
