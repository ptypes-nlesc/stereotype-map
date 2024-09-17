import json

import pandas as pd


def df_to_json(df, key_col_index, value_col_index, filename):
    """
    Convert specified columns of a DataFrame to a JSON file.

    This function takes a DataFrame and two column indices, converts the specified columns
    to a dictionary where one column's values are used as keys and the other column's values
    are used as values, and then saves this dictionary to a JSON file.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    key_col_index (int): The index of the column to be used as keys in the JSON.
    value_col_index (int): The index of the column to be used as values in the JSON.
    filename (str): The name of the file to save the JSON data.

    Returns:
    str: A message indicating that the data has been saved to the specified file.
    """
    # Ensure the column indices are within the DataFrame's bounds
    if key_col_index >= len(df.columns) or value_col_index >= len(df.columns):
        return "Column index out of bounds."

    # Convert the DataFrame slice to a dictionary with the specified columns as keys and values
    result_dict = {
        row[key_col_index]: row[value_col_index] for index, row in df.iterrows()
    }
    # Save the dictionary to a JSON file
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(result_dict, file, ensure_ascii=False, indent=4)

    return f"Data saved to {filename}"


if __name__ == "__main__":
    # Example usage
    df = pd.DataFrame(
        {"col1": ["key1", "key2", "key3"], "col2": ["val1, val2", "val2, val3", "val3"]}
    )
    json_output = df_to_json(df, 0, 1, "test.json")
