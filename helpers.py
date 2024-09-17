import pandas as pd
import json

def df_to_json_string(df, key_col_index, value_col_index):
    """
    Convert specified columns of a DataFrame to a JSON string.

    This function takes a DataFrame and two column indices, converts the specified columns
    to a dictionary where one column's values are used as keys and the other column's values
    are used as comma-separated string values. The resulting dictionary is then converted to a JSON string.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    key_col_index (int): The index of the column to be used as keys in the JSON.
    value_col_index (int): The index of the column to be used as values in the JSON.

    Returns:
    str: A JSON string representing the DataFrame.

    Example:
    >>> df = pd.DataFrame({
    >>>     'col1': ['Video1', 'Video2'],
    >>>     'col2': [['Tag1', 'Tag2', 'Tag3'], ['Tag3', 'Tag4']]
    >>> })
    >>> df_to_json_string(df, 0, 1)
    '{"Video1": "Tag1, Tag2, Tag3", "Video2": "Tag3, Tag4"}'
    """
    # Ensure the column indices are within the DataFrame's bounds
    if key_col_index >= len(df.columns) or value_col_index >= len(df.columns):
        return "Column index out of bounds."

    # Create a dictionary with the specified columns as keys and comma-separated string values
    result_dict = {
        row[key_col_index]: ', '.join(row[value_col_index]) for index, row in df.iterrows()
    }

    # Convert the dictionary to a JSON string
    json_str = json.dumps(result_dict, ensure_ascii=False, indent=4)

    return json_str

if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "col1": ["Video1", "Video2"],
            "col2": [["Tag1", "Tag2", "Tag3"], ["Tag3", "Tag4"]]
        }
    )
    json_output = df_to_json_string(df, 0, 1)
    print(json_output)