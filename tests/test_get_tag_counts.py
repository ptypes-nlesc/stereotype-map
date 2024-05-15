import pandas as pd
from clean import get_tag_counts

def test_get_tag_counts():
    df_flat_tag = pd.DataFrame({'tag': ['tag1', 'tag2', 'tag1', 'tag3', 'tag2', 'tag2']})
    expected_output = pd.DataFrame({'tag': ['tag2', 'tag1', 'tag3'], 'counts': [3, 2, 1]})
    pd.testing.assert_frame_equal(get_tag_counts(df_flat_tag), expected_output, check_like=True)