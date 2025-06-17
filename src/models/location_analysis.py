import os
import pandas as pd
from collections import Counter, defaultdict
from tqdm import tqdm
import spacy

# Load spaCy model once
nlp = spacy.load("en_core_web_sm")


def extract_prep_phrase_locations(doc, place_vocab=None):
    """Extract place nouns from prepositional object constructions."""
    locations = []
    for token in doc:
        if token.dep_ == "pobj" and token.head.dep_ == "prep":
            if token.pos_ == "NOUN":
                loc = token.text.lower()
                if place_vocab is None or loc in place_vocab:
                    locations.append(loc)
    return locations


def add_locations_from_titles(df, title_col="title", place_vocab=None,
                               cache_path="data/processed/locations.pkl"):
    """Parse titles and extract location nouns, with caching."""
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)

    if os.path.exists(cache_path):
        print(f"Loading cached location data from {cache_path}")
        locations = pd.read_pickle(cache_path)
        df["locations"] = locations
        return df

    print("Extracting locations from titles using spaCy...")
    locations = []
    for doc in tqdm(nlp.pipe(df[title_col].fillna(""), batch_size=1000),
                    total=len(df), desc="spaCy parsing (locations)"):
        locations.append(extract_prep_phrase_locations(doc, place_vocab))

    df = df.copy()
    df["locations"] = locations
    df[["locations"]].to_pickle(cache_path)
    print(f"Saved location data to {cache_path}")
    return df


def location_identity_cooccurrence(
    df, pos_col="pos_title_with_deps",
    female_terms=None, male_terms=None, racialized_terms=None,
    include_neutral=True
):
    cooccurrence = defaultdict(Counter)

    # Map tokens to identity groups
    term_groups = {}
    if female_terms:
        term_groups.update({t.lower(): "female" for t in female_terms})
    if male_terms:
        term_groups.update({t.lower(): "male" for t in male_terms})
    if racialized_terms:
        term_groups.update({t.lower(): "racialized" for t in racialized_terms})

    for _, row in df.dropna(subset=[pos_col, "locations"]).iterrows():
        if not isinstance(row["locations"], list):
            continue

        locations = row["locations"]
        tokens = [t[0].lower() for t in row[pos_col] if isinstance(t, tuple)]
        matched = set(t for t in tokens if t in term_groups)

        if matched:
            for token in matched:
                group = term_groups[token]
                for loc in locations:
                    cooccurrence[group][loc] += 1
        elif include_neutral:
            for loc in locations:
                cooccurrence["neutral"][loc] += 1

    return pd.DataFrame(cooccurrence).fillna(0).astype(int).T



def normalize_and_sort(df):
    """Row-normalize and sort index alphabetically."""
    return df.div(df.sum(axis=1), axis=0).sort_index()



