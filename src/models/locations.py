import os
import pandas as pd
from collections import Counter, defaultdict
from tqdm import tqdm
import spacy

# Load spaCy model once
nlp = spacy.load("en_core_web_sm")

# --- Configuration ---

PLACE_NOUNS = {
    "kitchen", "bathroom", "school", "hotel", "car", "office", "beach", "classroom",
    "park", "gym", "public", "bedroom", "club", "bus", "library", "shower"
}

GENDERED_TERMS = {"girl", "woman", "wife", "mom", "her", "she", "boy", "man", "husband", "dad", "him", "he"}
RACIALIZED_TERMS = {"black", "white", "asian", "latina", "indian", "ebony", "blonde"}
PERSON_TERMS = GENDERED_TERMS | RACIALIZED_TERMS


def extract_prep_phrase_locations(doc, place_vocab=None):
    locations = []
    for token in doc:
        if token.dep_ == "pobj" and token.head.dep_ == "prep":
            if token.pos_ == "NOUN":
                loc = token.text.lower()
                if place_vocab is None or loc in place_vocab:
                    locations.append(loc)
    return locations



def add_locations_from_titles(df, title_col="title", place_vocab=PLACE_NOUNS,
                               cache_path="data/processed/locations.pkl"):
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)

    if os.path.exists(cache_path):
        print(f"🔄 Loading cached location data from {cache_path}")
        locations = pd.read_pickle(cache_path)
        df["locations"] = locations
        return df

    print("⚙️ Extracting locations from titles using spaCy...")
    locations = []
    for doc in tqdm(nlp.pipe(df[title_col].fillna(""), batch_size=1000),
                    total=len(df), desc="spaCy parsing (locations)"):
        locations.append(extract_prep_phrase_locations(doc, place_vocab))

    df = df.copy()
    df["locations"] = locations
    df[["locations"]].to_pickle(cache_path)
    print(f"Saved location data to {cache_path}")
    return df


def location_person_cooccurrence(df, pos_col="pos_title_with_deps", person_terms=PERSON_TERMS):
    cooccurrence = defaultdict(Counter)

    for _, row in df.dropna(subset=[pos_col, "locations"]).iterrows():
        if not isinstance(row["locations"], list):
            continue
        locations = row["locations"]
        tokens = [t[0].lower() for t in row[pos_col] if isinstance(t, tuple)]
        people = set(tokens).intersection(person_terms)
        for person in people:
            for loc in locations:
                cooccurrence[person][loc] += 1

    return pd.DataFrame(cooccurrence).fillna(0).astype(int).T  # locations x people


# --- Optional: Normalize and sort ---

def normalize_and_sort(df):
    return df.div(df.sum(axis=1), axis=0).sort_index()
