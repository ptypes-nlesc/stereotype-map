import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

import src.data.clean as clean

df = pd.read_csv("data/porn-with-dates-2022.csv")
df["tags"] = df["categories"].apply(clean.extract_tags)
df["tags"] = df["tags"].apply(clean.remove_tag)
df_flat_tag = clean.flatten_tags(df["tags"])
tags_counts = clean.get_tag_counts(df_flat_tag)
tags_counts_dict = tags_counts.set_index("tag")["counts"].to_dict()

# Create the word cloud
wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(tags_counts_dict)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig("plots/tag_cloud.png")
