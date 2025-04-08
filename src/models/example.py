"""
Use the embeddings module to determine the similarity between video tags and predefined stereotypes for a given video
"""

import src.models.embeddings as emb
import src.visualization.create_network_graph as create_network_graph
import src.visualization.plot_heatmap as plot_heatmap

STEREOTYPES_JSON_PATH = "src/models/stereotypes.json"
TAGS_JSON_PATH = "src/models/tags.json"
MODEL_NAME = "distilroberta-base-paraphrase-v1"

emb.download_nltk_data()
stereotypes = emb.load_and_preprocess_data(STEREOTYPES_JSON_PATH)
tags = emb.load_and_preprocess_data(TAGS_JSON_PATH)
stereotypes_emb = emb.generate_embeddings(texts=stereotypes, model_name=MODEL_NAME)
tags_emb = emb.generate_embeddings(texts=tags, model_name=MODEL_NAME)
df = emb.calculate_similarity(tags_emb, stereotypes_emb)
plot_heatmap.plot_heatmap(df, "heatmap", model_name=MODEL_NAME)
create_network_graph.create_network_graph(
    tags, stereotypes, df, "network_graph", model_name=MODEL_NAME
)
