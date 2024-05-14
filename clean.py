"""
A collection of functions to clean the data.
"""

import pandas as pd

# TODO refactor to class
# TODO add type hints
# TODO replace space with underscore in tags


def extract_tags(categories):
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


def remove_tag(tag_list, tag_to_remove="HD Porn"):
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


def flatten_tags(tags):
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


def get_popular_tags(df_flat_tag, quantile=0.75):
    """
    Gets the popular tags from a DataFrame based on quantile.

    Parameters
    ----------
        df_flat_tag : DataFrame
            DataFrame with a single column named "tag" containing the tags

    Returns
    -------
        DataFrame
            a DataFrame sorted by the counts of each tag in descending order
    """
    popular_tags = (
        df_flat_tag.groupby("tag")
        .size()
        .reset_index(name="counts")  # type: ignore
        .sort_values("counts", ascending=False)
        .reset_index(drop=True)
    )
    min_appearance = popular_tags.counts.quantile(quantile)
    return set(popular_tags[popular_tags.counts >= min_appearance]["tag"])


def filter_popular_tags(tag_list, popular_tags_set):
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


if __name__ == "__main__":
    # Read the data
    df = pd.read_csv("data/porn-with-dates-2022.csv")

    # Extract tags
    df["tags"] = df["categories"].apply(extract_tags)

    # Remove unwanted tag
    df["tags"] = df["tags"].apply(remove_tag)

    # Flatten tags into a DataFrame
    df_flat_tag = flatten_tags(df["tags"])

    # Get popular tags
    popular_tags = get_popular_tags(df_flat_tag)

    # Filter tags based on popular tags
    df["popular_tags"] = df["tags"].apply(
        lambda tag_list: filter_popular_tags(tag_list, popular_tags)
    )

    # Filter DataFrame to include only rows where 'popular_tags' is not empty
    df_popular_tags = df.loc[df["popular_tags"].apply(lambda tag_list: tag_list != [])]

    print(df_popular_tags.head())
