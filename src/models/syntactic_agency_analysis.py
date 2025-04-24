import pandas as pd
from collections import Counter, defaultdict

# Define gendered nouns (expand as needed)
FEMALE_TERMS = {"girl", "woman", "wife", "mom", "her", "she"}
MALE_TERMS = {"boy", "man", "husband", "dad", "him", "he"}

AGENCY_ROLES = {"nsubj", "nsubjpass", "dobj"}

def extract_grammatical_roles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Count how often gendered terms appear in subject/object positions.
    """
    counts = defaultdict(Counter)  # e.g., counts["female"]["nsubj"] = 123

    for parsed in df["pos_title_with_deps"].dropna():
        for token, tag, dep in parsed:
            token_lower = token.lower()
            if dep in AGENCY_ROLES:
                if token_lower in FEMALE_TERMS:
                    counts["female"][dep] += 1
                elif token_lower in MALE_TERMS:
                    counts["male"][dep] += 1

    # Convert to DataFrame
    result = pd.DataFrame(counts).fillna(0).astype(int)
    result["total"] = result.sum(axis=1)
    result["female_ratio"] = result["female"] / result["total"]
    result["male_ratio"] = result["male"] / result["total"]
    return result
