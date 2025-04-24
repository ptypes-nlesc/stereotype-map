import pandas as pd
from typing import Set
from scipy.stats import chi2_contingency


# --- Configuration ---

# Manually curated categories (expandable)
APPEARANCE_ADJECTIVES: Set[str] = {
    "hot", "sexy", "cute", "beautiful", "blonde", "busty", "naughty", "attractive", "pretty", "gorgeous"
}

ROLE_ACTION_ADJECTIVES: Set[str] = {
    "dominant", "submissive", "experienced", "aggressive", "first", "young", "mature", "amateur", "professional"
}

FEMALE_NOUNS: Set[str] = {"girl", "woman", "wife", "mom", "lady", "female"}
MALE_NOUNS: Set[str] = {"boy", "man", "husband", "dad", "guy", "male"}


# --- Core Functions ---

def classify_adjective(adj: str) -> str:
    """Label adjectives by semantic category."""
    if adj in APPEARANCE_ADJECTIVES:
        return "appearance"
    elif adj in ROLE_ACTION_ADJECTIVES:
        return "role_or_action"
    return "other"


def label_adjectives(pair_df: pd.DataFrame) -> pd.DataFrame:
    """Add columns for adjective, noun, and category."""
    df = pair_df.copy()
    df["adjective"] = df["Pair"].apply(lambda x: x[0])
    df["noun"] = df["Pair"].apply(lambda x: x[1])
    df["adj_category"] = df["adjective"].apply(classify_adjective)
    return df


def compute_proportions(df: pd.DataFrame, group_nouns: Set[str]) -> pd.Series:
    """Compute percentage distribution of adjective categories within a noun group."""
    subset = df[df["noun"].isin(group_nouns)]
    category_counts = subset.groupby("adj_category")["Count"].sum()
    total = category_counts.sum()
    return (category_counts / total).fillna(0).sort_values(ascending=False)


def run_chi_squared_test(df: pd.DataFrame) -> float:
    """Run a chi-squared test comparing appearance adjective use in female vs. male noun groups."""
    female = df[df["noun"].isin(FEMALE_NOUNS)]
    male = df[df["noun"].isin(MALE_NOUNS)]

    a_f = female[female["adj_category"] == "appearance"]["Count"].sum()
    o_f = female[female["adj_category"] != "appearance"]["Count"].sum()
    a_m = male[male["adj_category"] == "appearance"]["Count"].sum()
    o_m = male[male["adj_category"] != "appearance"]["Count"].sum()

    contingency = [[a_f, o_f], [a_m, o_m]]
    chi2, p, _, _ = chi2_contingency(contingency)
    return chi2, p


def analyze_qualitative_adjectives(pair_df: pd.DataFrame, show_stats: bool = True):
    """High-level function to run full qualitative adjective analysis."""
    labeled_df = label_adjectives(pair_df)

    female_props = compute_proportions(labeled_df, FEMALE_NOUNS)
    male_props = compute_proportions(labeled_df, MALE_NOUNS)

    print("\n🧠 Adjective Category Proportions for Female Nouns:")
    print(female_props.to_string())

    print("\n🧠 Adjective Category Proportions for Male Nouns:")
    print(male_props.to_string())

    if show_stats:
        chi2, p = run_chi_squared_test(labeled_df)
        print(f"\n📊 Chi-squared Test for Appearance Bias:\nχ² = {chi2:.2f}, p = {p:.4f} {'(significant)' if p < 0.05 else ''}")

    return labeled_df, female_props, male_props
