import importlib

import pandas as pd

import clean
import embeddings
import helpers

importlib.reload(helpers)

# load data
dat = pd.read_csv("data/dat.csv")

dat["popular_tags_formatted"] = dat["popular_tags"].apply(clean.extract_tags)
# prepare tags
helpers.df_to_json(
    df=dat,
    key_col_index=0,
    value_col_index=-1,
    filename="video-tags.json"
)


embeddings.download_nltk_data()
# load stereotypes
stereotypes = embeddings.load_and_preprocess_data("stereotypes.json")
tags = embeddings.load_and_preprocess_data("output.json")

stereotypes_emb = embeddings.generate_embeddings(stereotypes)
tags_emb = embeddings.generate_embeddings(tags)
sim_df = embeddings.calculate_similarity(tags_emb, stereotypes_emb)
embeddings.plot_heatmap(sim_df)
embeddings.create_network_graph(tags, stereotypes, sim_df)
