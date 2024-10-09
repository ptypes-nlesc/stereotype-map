import importlib
import pickle

import matplotlib.pyplot as plt
import pandas as pd

import clean
import embeddings
import helpers

importlib.reload(helpers)

# load data
dat = pd.read_csv("data/dat.csv")

STEREOTYPES_JSON_PATH = "stereotypes.json"
TAGS_JSON_PATH = "video-tags.json"

# subset for now
dat = dat.head(10)

dat["popular_tags_formatted"] = dat["popular_tags"].apply(clean.extract_tags)
# prepare tags
helpers.df_to_json(
    df=dat, key_col_index=0, value_col_index=-1, filename="video-tags.json"
)

embeddings.download_nltk_data()
# load stereotypes
stereotypes = embeddings.load_and_preprocess_data(STEREOTYPES_JSON_PATH)
tags = embeddings.load_and_preprocess_data(TAGS_JSON_PATH)

stereotypes_emb = embeddings.generate_embeddings(stereotypes)
# TODO run for all and save results, long processing time
tags_emb = embeddings.generate_embeddings(tags)

# save tag embeddings
with open("tags_emb.pkl", "wb") as file:
    pickle.dump(tags_emb, file)

# # Load tags_emb from a file
# with open("tags_emb.pkl", "rb") as file:
#     tags_emb = pickle.load(file)

sim_df = embeddings.calculate_similarity(tags_emb, stereotypes_emb)

# plot for a subset only to improve readability
embeddings.plot_heatmap(sim_df)
embeddings.create_network_graph(tags, stereotypes, sim_df)

# TODO visualise sim df
# extract top 3 stereotypes for each video
# create df with extra column 'stereotype1', 'stereotype2', etc
