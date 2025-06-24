import pandas as pd
from typing import Set, List, Dict
from scipy.stats import chi2_contingency

def classify_adjective(adj: str, adj_set_1: Set[str], adj_set_2: Set[str], label_1: str, label_2: str) -> str:
    if adj in adj_set_1:
        return label_1
    elif adj in adj_set_2:
        return label_2
    return "other"

def label_adjectives(
    pair_df: pd.DataFrame,
    adj_set_1: Set[str],
    adj_set_2: Set[str],
    label_1: str,
    label_2: str
) -> pd.DataFrame:
    df = pair_df.copy()
    if "Pair" in df.columns:
        df["adjective"] = df["Pair"].apply(lambda x: x[0])
        df["noun"] = df["Pair"].apply(lambda x: x[1])
    df["adj_category"] = df["adjective"].apply(lambda x: classify_adjective(x, adj_set_1, adj_set_2, label_1, label_2))
    return df

def compute_proportions(df: pd.DataFrame, group_nouns: Set[str]) -> pd.Series:
    subset = df[df["noun"].isin(group_nouns)]
    category_counts = subset.groupby("adj_category")["Count"].sum()
    total = category_counts.sum()
    return (category_counts / total).fillna(0).sort_values(ascending=False)

def run_chi_squared_test(
    df: pd.DataFrame,
    group1_nouns: Set[str],
    group2_nouns: Set[str],
    label_1: str,
    label_2: str
) -> float:
    group1 = df[df["noun"].isin(group1_nouns)]
    group2 = df[df["noun"].isin(group2_nouns)]

    c1_g1 = group1[group1["adj_category"] == label_1]["Count"].sum()
    c2_g1 = group1[group1["adj_category"] == label_2]["Count"].sum()
    o_g1 = group1[(group1["adj_category"] != label_1) & (group1["adj_category"] != label_2)]["Count"].sum()

    c1_g2 = group2[group2["adj_category"] == label_1]["Count"].sum()
    c2_g2 = group2[group2["adj_category"] == label_2]["Count"].sum()
    o_g2 = group2[(group2["adj_category"] != label_1) & (group2["adj_category"] != label_2)]["Count"].sum()

    contingency = [
        [c1_g1, c2_g1, o_g1],
        [c1_g2, c2_g2, o_g2]
    ]
    chi2, p, _, _ = chi2_contingency(contingency)
    return chi2, p

def analyze_adj_noun_categories(
    pair_df: pd.DataFrame,
    adj_set_1: Set[str],
    adj_set_2: Set[str],
    label_1: str,
    label_2: str,
    group1_nouns: Set[str],
    group2_nouns: Set[str],
    group1_label: str = "Group 1",
    group2_label: str = "Group 2",
    show_stats: bool = True
):
    labeled_df = label_adjectives(pair_df, adj_set_1, adj_set_2, label_1, label_2)

    group1_props = compute_proportions(labeled_df, group1_nouns)
    group2_props = compute_proportions(labeled_df, group2_nouns)

    print(f"\n🔎 {label_1}/{label_2} Adjective Proportions for {group1_label}:")
    print(group1_props.to_string())

    print(f"\n🔎 {label_1}/{label_2} Adjective Proportions for {group2_label}:")
    print(group2_props.to_string())

    if show_stats:
        chi2, p = run_chi_squared_test(labeled_df, group1_nouns, group2_nouns, label_1, label_2)
        print(f"\n📊 Chi-squared Test for {label_1}/{label_2} Adjective Bias:\nχ² = {chi2:.2f}, p = {p:.4f} {'(significant)' if p < 0.05 else ''}")

    return labeled_df, group1_props, group2_props