from anagram_groups import group_anagrams


def test_classic():
    assert group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]) == [
        ["eat", "tea", "ate"],
        ["tan", "nat"],
        ["bat"],
    ]


def test_letter_multiplicity_matters():
    # "aab" is NOT an anagram of "abb" even though both use letters {a, b}
    assert group_anagrams(["aab", "aba", "abb", "bab"]) == [
        ["aab", "aba"],
        ["abb", "bab"],
    ]


def test_empty_input():
    assert group_anagrams([]) == []


def test_single_word():
    assert group_anagrams(["solo"]) == [["solo"]]


def test_empty_string_is_its_own_group():
    assert group_anagrams(["", "a", "", "b"]) == [["", ""], ["a"], ["b"]]


def test_group_order_by_first_occurrence():
    r = group_anagrams(["zz", "ab", "ba"])
    assert r[0] == ["zz"] and r[1] == ["ab", "ba"]


def test_case_sensitive():
    assert group_anagrams(["Ab", "ba"]) == [["Ab"], ["ba"]]
