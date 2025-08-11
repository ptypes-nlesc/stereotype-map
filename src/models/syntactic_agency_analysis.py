import pandas as pd
import numpy as np
from collections import Counter, defaultdict

# --- Role Definitions ---
SUBJECT_ROLES = {"nsubj"}            # Active subject (agent)
PASSIVE_SUBJECT_ROLES = {"nsubjpass"}  # Passive subject (patient)
OBJECT_ROLES = {"dobj", "obj"}       # Direct objects (patients in active voice)

# --- Role Frequency Analysis ---
def extract_grammatical_roles(df: pd.DataFrame, FEMALE_NOUNS: set, MALE_NOUNS: set) -> pd.DataFrame:
    """
    Separates counts of gendered tokens by syntactic role: subject, passive subject, and direct object.
    
    Parameters:
        df: DataFrame with 'pos_title_with_deps' column (list of (token, pos, dep) tuples)
        FEMALE_NOUNS, MALE_NOUNS: sets of gendered terms in lowercase
    
    Returns:
        DataFrame: counts of male/female tokens per role with totals and ratios
    """
    counts = defaultdict(Counter)

    # Iterate over parsed dependency tuples
    for parsed in df["pos_title_with_deps"].dropna():
        for token, pos, dep in parsed:
            dep = dep.lower()
            dep = "dobj" if dep == "obj" else dep  # normalize 'obj' to 'dobj'
            token_lower = token.lower()

            role = None
            if dep in SUBJECT_ROLES:
                role = "subject"
            elif dep in PASSIVE_SUBJECT_ROLES:
                role = "passive_subject"
            elif dep in OBJECT_ROLES:
                role = "direct_object"
            
            if role:
                if token_lower in FEMALE_NOUNS:
                    counts[role]["female"] += 1
                elif token_lower in MALE_NOUNS:
                    counts[role]["male"] += 1

    # Convert to DataFrame
    result = pd.DataFrame(counts).fillna(0).astype(int)

    # Ensure roles exist even if empty
    for role in ["subject", "passive_subject", "direct_object"]:
        if role not in result.columns:
            result[role] = 0

    # Compute totals and ratios safely
    for role in result.columns:
        total = result[role].sum()
        result.loc["total", role] = total
        result.loc["female_ratio", role] = (
            result[role]["female"] / total if total > 0 else 0
        )
        result.loc["male_ratio", role] = (
            result[role]["male"] / total if total > 0 else 0
        )

    return result

# --- Title Extraction by Dependency ---
def extract_titles_by_dependency(df, gender_terms, dependency="dobj", max_examples=10, random_state=None):
    """
    Extract random titles where a gendered token appears with a specific syntactic dependency.
    """
    matches = []
    for title, tokens in df[["title", "pos_title_with_deps"]].dropna().itertuples(index=False):
        for word, pos, dep in tokens:
            dep = dep.lower()
            dep = "dobj" if dep == "obj" else dep  # normalize obj → dobj
            if dep == dependency and word.lower() in gender_terms:
                matches.append({
                    "title": title,
                    "matched_token": word,
                    "dependency": dep
                })
                break  # only one match per title
    
    if not matches:
        return pd.DataFrame(columns=["title", "matched_token", "dependency"])
    
    matches_df = pd.DataFrame(matches)
    return matches_df.sample(n=min(max_examples, len(matches_df)), random_state=random_state).reset_index(drop=True)

# --- Random Examples by Role ---
def extract_examples_by_role(df, FEMALE_NOUNS, MALE_NOUNS, max_examples=5, random_state=None):
    """
    Extract random example titles for subjects, passive subjects, and direct objects.
    
    Returns:
        dict: Nested dict of DataFrames with female/male examples for each role.
    """
    roles = {
        "subject": "nsubj",
        "passive_subject": "nsubjpass",
        "direct_object": "dobj"
    }
    
    examples = {}
    for role_name, dep in roles.items():
        examples[role_name] = {
            "female": extract_titles_by_dependency(df, FEMALE_NOUNS, dependency=dep, max_examples=max_examples, random_state=random_state),
            "male": extract_titles_by_dependency(df, MALE_NOUNS, dependency=dep, max_examples=max_examples, random_state=random_state)
        }
    return examples
