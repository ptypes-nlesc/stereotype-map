from collections import Counter

from src.data.clean import get_specific_tag_combinations


def test_get_specific_tag_combinations():
    tags = {("a", "b"): 3, ("a", "c"): 1, ("b", "c"): 1, ("a", "d"): 1, ("b", "d"): 1}
    selected_tags = ["d"]
    expected_output = {("a", "d"): 1, ("b", "d"): 1}
    assert get_specific_tag_combinations(tags, selected_tags) == expected_output
