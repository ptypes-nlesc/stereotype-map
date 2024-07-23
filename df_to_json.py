import json

import pandas as pd


def df_to_json(df, key_col_index, value_col_index, filename):
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
