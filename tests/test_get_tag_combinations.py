from src.data.clean import get_tag_combinations


def test_get_tag_combination():
    tags = [["a", "b", "c"], ["a", "b", "d"], ["a", "b"]]
    expected_output = {
        ("a", "b"): 3,
        ("a", "c"): 1,
        ("b", "c"): 1,
        ("a", "d"): 1,
        ("b", "d"): 1,
    }
    assert get_tag_combinations(tags) == expected_output
