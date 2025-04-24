import os
import pandas as pd
import spacy
from collections import Counter
from tqdm import tqdm

# Initialize spaCy model once
nlp = spacy.load("en_core_web_sm")

def process_in_batches(text_series, batch_size=1000):
    results = []
    for doc in tqdm(nlp.pipe(text_series, batch_size=batch_size, disable=["ner"]), total=len(text_series), desc="spaCy parsing"):
        results.append([(token.text, token.pos_, token.dep_) for token in doc])
    return results

def extract_adj_noun_pairs(parsed_rows):
    for row in parsed_rows:
        for (word, tag, dep), (next_word, next_tag, next_dep) in zip(row, row[1:]):
            if tag == "ADJ" and next_tag == "NOUN":
                yield (word.lower(), next_word.lower())

def load_or_process_pos(df, cache_path="pos_title_with_deps.pkl"):
    if os.path.exists(cache_path):
        print("Loading cached POS data...")
        df["pos_title_with_deps"] = pd.read_pickle(cache_path)["pos_title_with_deps"]
    else:
        print("Processing titles with spaCy...")
        valid_rows = df[df["title_words"].apply(lambda x: isinstance(x, list))]
        sentences = valid_rows["title_words"].apply(lambda x: " ".join(x))
        processed_results = process_in_batches(sentences)
        df.loc[valid_rows.index, "pos_title_with_deps"] = pd.Series(processed_results, index=valid_rows.index)
        df[["pos_title_with_deps"]].to_pickle(cache_path)
    return df

def compute_and_save_pairs(df, output_csv="adjective_noun_pairs.csv"):
    valid_rows_with_deps = df[df["pos_title_with_deps"].apply(lambda x: isinstance(x, list))]
    adj_noun_pairs = extract_adj_noun_pairs(valid_rows_with_deps["pos_title_with_deps"])
    pair_counts = Counter(adj_noun_pairs)
    pair_df = pd.DataFrame(pair_counts.items(), columns=["Pair", "Count"]).sort_values(by="Count", ascending=False)
    pair_df.to_csv(output_csv, index=False)
    print(f"Saved {len(pair_df)} adjective–noun pairs to {output_csv}")
    return pair_df

# Entrypoint
def run_pipeline(input_df, cache_path="pos_title_with_deps.pkl", output_csv="adjective_noun_pairs.csv"):
    df = input_df.copy()
    df = load_or_process_pos(df, cache_path)
    return compute_and_save_pairs(df, output_csv)
