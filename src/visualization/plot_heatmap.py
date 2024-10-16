import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import src.utils.helpers as helpers


def plot_heatmap(df: pd.DataFrame, file_name: str, model_name: str):
    """
    Plot a heatmap of the cosine similarity scores and save it to a file.

    Parameters:
    - df (pd.DataFrame): A DataFrame containing the cosine similarity scores between tags and stereotypes.
    - file_name (str): The name of the file to save the heatmap plot.
    - model_name (str): The name of the model used to generate the embeddings, included in the file name.

    The function generates a heatmap where the rows represent video tags and the columns represent stereotypes.
    The heatmap is saved in the 'plots' directory with the specified file name and model name.
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(df, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Cosine Similarity between Videos and Stereotypes")
    plt.xlabel("Stereotypes")
    plt.ylabel("Videos")
    plt.savefig(f"{file_name}_{model_name}.png")
    plt.show()
