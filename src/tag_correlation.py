"""
This scipt calculates correlation between the most popular tags
It then plots the correlation matrix as a heatmap.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import src.data.clean as clean

# if __name__ == "__main__":
df = pd.read_csv("data/porn-with-dates-2022.csv")

# Create 'tags' column from categories
df["tags"] = df["categories"].apply(clean.extract_tags)

# Remove a specific tag from the "tags" column
df["tags"] = df["tags"].apply(clean.remove_tag, tag_to_remove="HD Porn")

# confirm it is a list
# df.tags.apply(lambda tag_list: isinstance(tag_list, list))

# flatten out tags
df_flat_tag = clean.flatten_tags(df.tags)

# number of unique hashtags
df_flat_tag["tag"].unique().size
# 108 unique tags

# count the number of each hashtag
popular_tags_set = clean.get_popular_tags(df_flat_tag)

# make a new column with only the popular tags
df["popular_tags"] = df.tags.apply(
    lambda tag_list: clean.filter_popular_tags(tag_list, popular_tags_set)
)

# drop rows without popular tag
df_popular_tags = df.loc[df.popular_tags.apply(lambda tag_list: tag_list != [])]

df_tags_vector = df_popular_tags.loc[:, ["popular_tags"]]

for tag in popular_tags_set:
    # make columns to encode presence of hashtags
    df_tags_vector["{}".format(tag)] = df_tags_vector.popular_tags.apply(
        lambda tag_list: int(tag in tag_list)
    )

# create a matrix of tags
tag_matrix = df_tags_vector.drop("popular_tags", axis=1)

# calculate the correlation matrix
correlations = tag_matrix.corr()

# plot the correlation matrix
plt.figure(figsize=(10, 10))
sns.heatmap(
    correlations,
    cmap="RdBu",
    vmin=-0.5,
    vmax=0.5,
    square=True,
    cbar_kws={"label": "correlation"},
)
plt.savefig("plots/tag_correlation.png")
