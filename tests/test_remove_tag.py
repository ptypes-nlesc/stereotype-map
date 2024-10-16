from src.data.clean import remove_tag


def test_remove_tag():
    tag_list = ["tag1", "tag2", "HD Porn", "tag3"]
    tag_to_remove = "HD Porn"
    expected_output = ["tag1", "tag2", "tag3"]
    assert remove_tag(tag_list, tag_to_remove) == expected_output

