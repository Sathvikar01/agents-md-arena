from impl import flatten


def test_shallow():
    assert flatten([1, 2, 3]) == [1, 2, 3]


def test_one_level():
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]


def test_deep():
    assert flatten([1, [2, [3, [4, [5]]]]]) == [1, 2, 3, 4, 5]


def test_empty():
    assert flatten([]) == []
    assert flatten([[[]]]) == []


def test_strings_are_leaves():
    assert flatten(["ab", ["cd", "ef"]]) == ["ab", "cd", "ef"]


def test_tuples_are_leaves():
    assert flatten([(1, 2), [3], (4,)]) == [(1, 2), 3, (4,)]


def test_mixed_types():
    assert flatten([None, [True], [1.5, ["x"]]]) == [None, True, 1.5, "x"]
