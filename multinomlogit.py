import embeddings

embeddings.download_nltk_data()
stereotypes = embeddings.load_and_preprocess_data("stereotypes.json")
tags = embeddings.load_and_preprocess_data("tags.json")
stereotypes_emb = embeddings.generate_embeddings(stereotypes)
tags_emb = embeddings.generate_embeddings(tags)
sim_df = embeddings.calculate_similarity(tags_emb, stereotypes_emb)
embeddings.plot_heatmap(sim_df)
embeddings.create_network_graph(tags, stereotypes, sim_df)
