"""
A collection of functions to clean the data.
"""

from collections import Counter
from itertools import combinations
from typing import List, Set

import pandas as pd

# TODO refactor to class
# TODO consider using argparse
# TODO replace space with underscore in tags


def extract_tags(categories: str) -> List[str]:
    """
    Extracts tags from a string of categories.

    Parameters
    ----------
        categories : str
            string of categories from which to extract tags

    Returns
    -------
        list
            a list of tags
    """
    return categories.replace("['", "").replace("']", "").replace("'", "").split(", ")


def remove_tag(tag_list: List[str], tag_to_remove: str = "HD Porn") -> List[str]:
    """
    Removes a specific tag from a list of tags.

    Parameters
    ----------
        tag_list : list
            list of tags from which to remove the tag
        tag_to_remove : str
            tag to remove

    Returns
    -------
        list
            a list of tags without the removed tag
    """
    return [tag for tag in tag_list if tag != tag_to_remove]


def flatten_tags(tags: List[List[str]]) -> pd.DataFrame:
    """
    Flattens a list of lists into a single list and creates a DataFrame.

    Parameters
    ----------
        tags : list
            list of lists to be flattened

    Returns
    -------
        DataFrame
            a DataFrame with a single column named "tag" containing the flattened list
    """
    flat_list = [tag for tag_list in tags for tag in tag_list]
    df_flat_tag = pd.DataFrame(flat_list, columns=["tag"])
    return df_flat_tag


def get_tag_counts(df_flat_tag: pd.DataFrame) -> pd.DataFrame:
    """
    Gets the counts of each tag from a DataFrame.

    Parameters
    ----------
        df_flat_tag : DataFrame
            DataFrame with a single column named "tag" containing the tags

    Returns
    -------
        DataFrame
            a DataFrame sorted by the counts of each tag in descending order with their counts
    """
    return (
        df_flat_tag.groupby("tag")
        .size()
        .reset_index(name="counts")  # type: ignore
        .sort_values("counts", ascending=False)
        .reset_index(drop=True)
    )


def get_popular_tags(df: pd.DataFrame, quantile: float = 0.75) -> Set[str]:
    """
    Gets the popular tags from a DataFrame based on quantile.

    Parameters
    ----------
        df : DataFrame
            DataFrame with a single column named "tag" containing the tags

    Returns
    -------
        DataFrame
            a DataFrame sorted by the counts of each tag in descending order
    """
    tag_counts = get_tag_counts(df)
    # todo add float here
    min_appearance = tag_counts.counts.quantile(quantile)
    return set(tag_counts[tag_counts.counts >= min_appearance]["tag"])


def filter_popular_tags(tag_list: List[str], popular_tags_set: Set[str]) -> List[str]:
    """
    Filters a list of tags based on a set of popular tags.

    Parameters
    ----------
        tag_list : list
            list of tags to be filtered
        popular_tags_set : set
            set of popular tags

    Returns
    -------
        list
            a list containing only the tags that are in the set of popular tags
    """
    return [tag for tag in tag_list if tag in popular_tags_set]


def get_tag_combinations(tags: List[List[str]], ntags: int = 2) -> Counter:
    """
    Gets the tag combinations from a list of lists of tags.

    Parameters
    ----------
        tags : list
            list of lists of tags
        ntags : int
            number of tags to combine

    Returns
    -------
        Counter
            a Counter object with the tag combinations and their counts
    """
    return Counter(
        combo for tag_list in tags for combo in combinations(tag_list, ntags)
    )


def get_specific_tag_combinations(tags: Counter, selected_tags: List[str]) -> Counter:
    """
    Returns a Counter object with combinations that include any of the selected tags.

    Args:
        tags (Counter): A Counter object where keys are tuples representing combinations of tags,
                        and values are the counts of each combination.
        selected_tags (List[str]): A list of tags to be selected. Note that the selected tags are not paired.

    Returns:
        Counter: A Counter object with keys as combinations that include any of the selected tags,
                 and values as the counts of each combination.
    """
    return Counter(
        dict(
            item
            for item in tags.items()
            if any(tag in item[0] for tag in selected_tags)
        )
    )


if __name__ == "__main__":
    # Read the data
    dat = pd.read_csv("data/porn-with-dates-2022.csv")

    # Extract tags
    dat["tags"] = dat["categories"].apply(extract_tags)

    # Remove unwanted tag
    dat["tags"] = dat["tags"].apply(remove_tag)

    # Flatten tags into a DataFrame
    dat_flat_tag = flatten_tags(dat["tags"])  # type: ignore

    # Get popular tags
    popular_tags = get_popular_tags(dat_flat_tag)

    # Filter tags based on popular tags
    dat["popular_tags"] = dat["tags"].apply(
        lambda tag_list: filter_popular_tags(tag_list, popular_tags)
    )

    # Filter DataFrame to include only rows where 'popular_tags' is not empty
    dat_popular_tags = dat.loc[
        dat["popular_tags"].apply(lambda tag_list: tag_list != [])
    ]
    dat_popular_tags.to_csv("data/dat.csv", index=False)
    print(dat_popular_tags.head())

    # combination of popular tags
    combo = get_tag_combinations(dat_popular_tags["popular_tags"], ntags=3)
