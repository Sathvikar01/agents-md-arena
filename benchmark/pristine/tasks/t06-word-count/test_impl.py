from impl import top_words


def test_case_insensitive():
    assert top_words("The cat THE dog the", 3) == [("the", 3), ("cat", 1), ("dog", 1)]


def test_tie_broken_alphabetically():
    assert top_words("b a b a c", 3) == [("a", 2), ("b", 2), ("c", 1)]


def test_all_ties():
    assert top_words("delta alpha charlie bravo", 2) == [
        ("alpha", 1),
        ("bravo", 1),
    ]


def test_k_larger_than_unique():
    assert top_words("one two", 10) == [("one", 1), ("two", 1)]


def test_k_zero():
    assert top_words("hello world", 0) == []


def test_punctuation_split():
    assert top_words("end. Start, end! START?", 2)[0] == ("end", 2)


def test_apostrophes_kept():
    assert top_words("don't stop don't", 2)[0] == ("don't", 2)


def test_empty_text():
    assert top_words("", 5) == []


def test_digits_in_words():
    r = top_words("v2 v2 v10 v10", 2)
    assert dict(r)["v2"] == 2 and dict(r)["v10"] == 2
