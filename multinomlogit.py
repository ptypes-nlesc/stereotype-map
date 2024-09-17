import helpers
import embeddings
import pandas as pd

# load data
dat = pd.read_csv("data/dat.csv")

# prepare tags
helpers.df_to_json_string(dat.head(20), 0, -1)

embeddings.download_nltk_data()
# load stereotypes
stereotypes = embeddings.load_and_preprocess_data("stereotypes.json")
tags = embeddings.load_and_preprocess_data("video-tags.json")

stereotypes_emb = embeddings.generate_embeddings(stereotypes)
tags_emb = embeddings.generate_embeddings(tags)
sim_df = embeddings.calculate_similarity(tags_emb, stereotypes_emb)
embeddings.plot_heatmap(sim_df)
embeddings.create_network_graph(tags, stereotypes, sim_df)
