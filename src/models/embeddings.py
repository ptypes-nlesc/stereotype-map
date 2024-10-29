"""
Determine the similarity between video tags and predefined stereotypes by leveraging word embeddings
"""

import json
import logging
import re
from typing import Dict, List

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def download_nltk_data():
    """Download necessary NLTK data if not already present."""
    nltk_data = ["stopwords", "punkt"]
    for data in nltk_data:
        try:
            nltk.data.find(f"tokenizers/{data}")
        except LookupError:
            nltk.download(data)


def preprocess(text: str) -> str:
    """
    Tokenize and clean the input text by removing stopwords and non-alphabetic tokens.

    Parameters:
    - text (str): The input text to be preprocessed.

    Returns:
    - str: The preprocessed text, with stopwords and non-alphabetic tokens removed.
    """
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text.lower())
    return " ".join(
        [word for word in tokens if word.isalpha() and word not in stop_words]
    )


def clean_tokenize_and_stem(text):
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    # Remove punctuation, numbers, and convert to lowercase
    text = re.sub(r"[^\w\s]", "", text.lower())  # Remove punctuation
    text = re.sub(r"\d+", "", text)  # Remove numbers
    words = [stemmer.stem(word) for word in text.split() if word not in stop_words]
    return words


def load_and_preprocess_data(file_path: str) -> Dict[str, str]:
    """Load and preprocess data from a JSON file.

    Parameters:
    - file_path (str): The path to the JSON file to be loaded and processed.

    Returns:
    - Dict[str, str]: A dictionary containing the original keys from the JSON
    file and their associated preprocessed text values.
    If the file is not found, an empty dictionary is returned.

    Raises:
    - FileNotFoundError: If the specified file does not exist, a logging error
    is recorded, and an empty dictionary is returned.
    """
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            data = json.load(file)
        return {key: preprocess(text) for key, text in data.items()}
    except FileNotFoundError:
        logging.error("File %s not found.", file_path)
        return {}


def generate_embeddings(
    texts: Dict[str, str], model_name: str
) -> Dict[str, List[float]]:
    """Generate embeddings for a dictionary of texts."""
    try:
        model = SentenceTransformer(model_name)
        return {
            key: model.encode(text, show_progress_bar=False).tolist()
            for key, text in texts.items()
        }
    except Exception as e:
        logging.error("Error loading model: %s", e)
        return {}


def calculate_similarity(
    tags_emb: Dict[str, List[float]], stereotypes_emb: Dict[str, List[float]]
) -> pd.DataFrame:
    """
    Calculate cosine similarity between the two sets of embeddings.
        Parameters:
    - tags_emb (Dict[str, List[float]]): A dictionary where the keys are tag identifiers and the values are the embeddings of the tags.
    - stereotypes_emb (Dict[str, List[float]]): A dictionary where the keys are stereotype identifiers and the values are the embeddings of the stereotypes.

    Returns:
    - pd.DataFrame: A DataFrame containing the cosine similarity scores between tags and stereotypes. The rows are indexed by tag identifiers, and the columns are labeled with stereotype identifiers.

    """
    tags_keys, tags_values = zip(*tags_emb.items())
    stereotypes_keys, stereotypes_values = zip(*stereotypes_emb.items())
    sim_matrix = cosine_similarity(tags_values, stereotypes_values)
    return pd.DataFrame(sim_matrix, index=tags_keys, columns=stereotypes_keys)
