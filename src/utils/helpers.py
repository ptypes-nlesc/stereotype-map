import hashlib
import json
import re

import pandas as pd


def df_to_json(df, key_col_name, value_col_name, filename="output.json"):
    """
    Convert a DataFrame column to a JSON string and save it to a file.

    This function takes a DataFrame and two column names, converts the specified columns
    to a dictionary where one column's values are used as keys and the other column's values
    are used as comma-separated string values. The resulting dictionary is then converted to a JSON string.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    key_col_name (str): The name of the column to be used as keys in the JSON.
    value_col_name (str): The name of the column to be used as values in the JSON.
    filename (str): The name of the file to save the JSON data.

    Returns:
    None

    Example:
    >>> df = pd.DataFrame({
    >>>     'col1': ['Video1', 'Video2'],
    >>>     'col2': [['Tag1', 'Tag2', 'Tag3'], ['Tag3', 'Tag4']]
    >>> })
    >>> df_to_json(df, 'col1', 'col2', 'output.json')
    """
    # Ensure the specified columns exist in the DataFrame
    if key_col_name not in df.columns or value_col_name not in df.columns:
        return "Column name not found in DataFrame."

    # Create a dictionary with the specified columns as keys and comma-separated string values
    result_dict = {
        row[key_col_name]: ", ".join(row[value_col_name])
        for index, row in df.iterrows()
    }

    # Convert the dictionary to a JSON string
    json_str = json.dumps(result_dict, ensure_ascii=False, indent=4)

    # Save the JSON string to a file
    with open(filename, "w", encoding="utf-8") as file:
        file.write(json_str)


def extract_and_create_unique_id(url: str, length: int = 8) -> str:
    """
    Extracts the identifier from a given URL and creates a unique ID.

    Parameters:
    - url (str): The URL from which to extract the identifier.
    - length (int, optional): The number of characters to return from the unique ID. Default is 8.

    Returns:
    - str: A unique ID derived from the extracted identifier, or None if not found.
    """
    match = re.search(r"viewkey=([a-zA-Z0-9]+)", url)
    if match:
        identifier = match.group(1)  # Get the captured identifier
        # Create a hash of the identifier and return the specified number of characters
        return hashlib.md5(identifier.encode()).hexdigest()[
            :length
        ]  # Use the specified length
    return None  # Return None if no identifier is found


if __name__ == "__main__":
    # Example usage
    df = pd.DataFrame(
        {
            "col1": ['Video1', 'Video2'],
            "col2": [['Tag1', 'Tag2', 'Tag3'], ['Tag3', 'Tag4']],
        }
    )
    df_to_json(df, "col1", "col2", "output.json")
