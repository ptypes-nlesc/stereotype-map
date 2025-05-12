import pandas as pd
from collections import defaultdict
from src.data.lexicons import female_roles, female_nouns, male_nouns, male_roles, racialized_nouns

import seaborn as sns
import matplotlib.pyplot as plt
import os


# Define controlled sets of nouns
GENDERED_NOUNS = female_nouns | male_nouns
RACIALIZED_NOUNS = racialized_nouns


plot_output_path = "plots"

def prepare_pair_df(pair_df):
    """Split adjective–noun tuples and expand into new columns."""
    pair_df = pair_df.copy()
    pair_df["adjective"] = pair_df["Pair"].apply(lambda x: x[0])
    pair_df["noun"] = pair_df["Pair"].apply(lambda x: x[1])
    return pair_df


def compute_bias_scores(pair_df, noun_set):
    """Compute normalized adjective usage bias scores against a noun group."""
    group_pairs = pair_df[pair_df["noun"].isin(noun_set)]
    group_adj_freq = group_pairs.groupby("adjective")["Count"].sum()
    total_adj_freq = pair_df.groupby("adjective")["Count"].sum()
    bias_score = (group_adj_freq / total_adj_freq).fillna(0)
    return bias_score.sort_values(ascending=False)


def plot_heatmap(pair_df, noun_subset, top_n=20, title="Adjective–Noun Heatmap"):
    """Plot a heatmap of adjective–noun frequency counts for selected nouns."""
    subset = pair_df[pair_df["noun"].isin(noun_subset)]
    pivot = subset.pivot_table(index="adjective", columns="noun", values="Count", fill_value=0)
    top_adjs = pivot.sum(axis=1).sort_values(ascending=False).head(top_n).index
    pivot = pivot.loc[top_adjs]

    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot, cmap="YlGnBu", linewidths=0.5, annot=True,  fmt=".0f")
    plt.title(title)
    plt.xlabel("Noun")
    plt.ylabel("Adjective")
    plt.tight_layout()
    plt.savefig(os.path.join(plot_output_path, "heatmap-adj-noun-pairs-counts.eps"), bbox_inches="tight")
    plt.savefig(os.path.join(plot_output_path, "heatmap-adj-noun-pairs-counts.png"), bbox_inches="tight")
    plt.show()


def analyze_adjective_bias(pair_df, show_heatmap=True):
    """Main analysis function."""
    pair_df = prepare_pair_df(pair_df)

    print("🔍 Computing gender-related adjective bias...")
    gender_bias = compute_bias_scores(pair_df, GENDERED_NOUNS)
    print("\nTop adjectives by proportion used with gendered nouns:")
    print(gender_bias.head(10))

    print("\n🔍 Computing race-related adjective bias...")
    race_bias = compute_bias_scores(pair_df, RACIALIZED_NOUNS)
    print("\nTop adjectives by proportion used with racialized nouns:")
    print(race_bias.head(10))

    if show_heatmap:
        print("\n📊 Generating heatmap for top adjective–noun combinations...")
        plot_heatmap(pair_df, GENDERED_NOUNS | RACIALIZED_NOUNS)

    return gender_bias, race_bias
