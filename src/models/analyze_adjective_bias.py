import pandas as pd
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
import os
import spacy

from src.data.lexicons import female_roles, female_nouns, male_nouns, male_roles, racialized_nouns

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define controlled sets of nouns
GENDERED_NOUNS = female_nouns | male_nouns
RACIALIZED_NOUNS = racialized_nouns

plot_output_path = "plots"
os.makedirs(plot_output_path, exist_ok=True)

# Cache for adjective POS lookups
_ADJ_CACHE = {}

# Optional: list of known noisy or malformed adjectives to exclude
STOP_ADJECTIVES = {"unknown", "random", "misc", "various", "alic", "coffe"}

def is_true_adjective(word):
    """Check if a word is a true adjective using spaCy POS tagging with caching."""
    if word in _ADJ_CACHE:
        return _ADJ_CACHE[word]
    doc = nlp(word)
    is_adj = any(tok.pos_ == "ADJ" for tok in doc)
    _ADJ_CACHE[word] = is_adj
    return is_adj

def prepare_pair_df(pair_df):
    """Split adjective–noun tuples and expand into new columns."""
    pair_df = pair_df.copy()
    pair_df["adjective"] = pair_df["Pair"].apply(lambda x: x[0].lower())
    pair_df["noun"] = pair_df["Pair"].apply(lambda x: x[1].lower())
    pair_df = pair_df[pair_df["adjective"].str.isalpha()]  # filter noisy tokens
    pair_df = pair_df[~pair_df["adjective"].isin(STOP_ADJECTIVES)]  # remove known noise
    pair_df = pair_df[pair_df["adjective"].apply(is_true_adjective)]  # retain only real adjectives
    return pair_df

def compute_bias_scores(pair_df, noun_set, min_total=5, min_group=3):
    """Compute normalized adjective usage bias scores against a noun group."""
    group_pairs = pair_df[pair_df["noun"].isin(noun_set)]
    group_adj_freq = group_pairs.groupby("adjective")["Count"].sum()
    group_adj_freq = group_adj_freq[group_adj_freq >= min_group]  # filter rare group terms
    total_adj_freq = pair_df.groupby("adjective")["Count"].sum()
    valid_adjs = total_adj_freq[total_adj_freq >= min_total].index
    bias_score = (group_adj_freq / total_adj_freq).fillna(0)
    return bias_score.loc[valid_adjs.intersection(group_adj_freq.index)].sort_values(ascending=False)

def get_top_bias_adjectives(pair_df, noun_set, top_n=10, min_total=5, min_group=3):
    """Return top biased adjectives with frequency context."""
    bias = compute_bias_scores(pair_df, noun_set, min_total, min_group)
    freq = pair_df.groupby("adjective")["Count"].sum()
    result = pd.DataFrame({"bias": bias, "frequency": freq})
    return result.sort_values(by="bias", ascending=False).head(top_n)

def plot_heatmap(pair_df, noun_subset, top_n=20, min_count=5):
    """Plot a heatmap of adjective–noun frequency counts for selected nouns."""
    subset = pair_df[pair_df["noun"].isin(noun_subset)]
    subset = subset[subset["Count"] >= min_count]
    pivot = subset.pivot_table(index="adjective", columns="noun", values="Count", fill_value=0)
    top_adjs = pivot.sum(axis=1).sort_values(ascending=False).head(top_n).index
    pivot = pivot.loc[top_adjs]

    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot, cmap="YlGnBu", linewidths=0.5, annot=True, fmt=".0f")
    plt.xlabel("Noun")
    plt.ylabel("Adjective")
    plt.tight_layout()

    for ext in ["png", "eps"]:
        fname = f"heatmap-adj-noun-pairs-counts.{ext}"
        plt.savefig(os.path.join(plot_output_path, fname), bbox_inches="tight", dpi=300)
    plt.show()

def analyze_adjective_bias(pair_df, show_heatmap=True, min_total=5, min_group=3):
    """Main analysis function with bias scoring and optional visualization."""
    pair_df = prepare_pair_df(pair_df)

    gender_bias = compute_bias_scores(pair_df, GENDERED_NOUNS, min_total, min_group)
    print("\nTop adjectives by proportion used with gendered nouns:")
    print(gender_bias.head(10))

    race_bias = compute_bias_scores(pair_df, RACIALIZED_NOUNS, min_total, min_group)
    print("\nTop adjectives by proportion used with racialized nouns:")
    print(race_bias.head(10))

    if show_heatmap:
      plot_heatmap(pair_df, GENDERED_NOUNS | RACIALIZED_NOUNS, min_count=min_total)

    return {
        "gender_bias": gender_bias,
        "race_bias": race_bias,
        "pair_df": pair_df
    }
