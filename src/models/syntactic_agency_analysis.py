import pandas as pd
from collections import Counter, defaultdict

# --- Gendered Terms and Dependencies ---

FEMALE_TERMS = {"girl", "woman", "wife", "mom", "her", "she"}
MALE_TERMS = {"boy", "man", "husband", "dad", "him", "he"}
AGENCY_ROLES = {"nsubj", "nsubjpass", "dobj"}


# --- Role Frequency Analysis ---

def extract_grammatical_roles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Count how often gendered terms appear in subject/object positions.
    Returns a DataFrame with absolute counts and gender ratios.
    """
    counts = defaultdict(Counter)

    for parsed in df["pos_title_with_deps"].dropna():
        for token, tag, dep in parsed:
            token_lower = token.lower()
            if dep in AGENCY_ROLES:
                if token_lower in FEMALE_TERMS:
                    counts["female"][dep] += 1
                elif token_lower in MALE_TERMS:
                    counts["male"][dep] += 1

    result = pd.DataFrame(counts).fillna(0).astype(int)
    result["total"] = result.sum(axis=1)
    result["female_ratio"] = result["female"] / result["total"]
    result["male_ratio"] = result["male"] / result["total"]
    return result


# --- Qualitative Example Extraction ---

def extract_titles_by_dependency(df, gender_terms, dependency="dobj", max_examples=10):
    """
    Extracts example titles where a gendered token appears with a specific syntactic dependency.
    
    Parameters:
        df (pd.DataFrame): DataFrame with 'title' and 'pos_title_with_deps'
        gender_terms (set): e.g., FEMALE_TERMS
        dependency (str): "dobj", "nsubj", or "nsubjpass"
        max_examples (int): number of examples to extract
    
    Returns:
        pd.DataFrame: matched titles and dependency info
    """
    results = []
    for i, (title, tokens) in df[["title", "pos_title_with_deps"]].dropna().iterrows():
        for word, pos, dep in tokens:
            if dep == dependency and word.lower() in gender_terms:
                results.append({
                    "title": title,
                    "matched_token": word,
                    "dependency": dep
                })
                break  # One match per title
        if len(results) >= max_examples:
            break
    return pd.DataFrame(results)
