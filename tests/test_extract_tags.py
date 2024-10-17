from src.data.clean import extract_tags


def test_extract_tags():
    categories = "['tag1', 'tag2', 'tag3']"
    expected_output = ["tag1", "tag2", "tag3"]
    assert extract_tags(categories) == expected_output
