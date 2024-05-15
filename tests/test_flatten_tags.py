import pandas as pd
from clean import flatten_tags

def test_flatten_tags():
    tags = [['tag1', 'tag2'], ['tag3', 'tag4'], ['tag5']]
    expected_output = pd.DataFrame({'tag': ['tag1', 'tag2', 'tag3', 'tag4', 'tag5']})
    assert flatten_tags(tags).equals(expected_output)