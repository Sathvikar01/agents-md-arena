from impl import transpose


def test_square():
    assert transpose([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]


def test_rectangular_tall_to_wide():
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]


def test_rectangular_wide_to_tall():
    assert transpose([[1, 4], [2, 5], [3, 6]]) == [[1, 2, 3], [4, 5, 6]]


def test_single_row():
    assert transpose([[1, 2, 3]]) == [[1], [2], [3]]


def test_single_column():
    assert transpose([[1], [2], [3]]) == [[1, 2, 3]]


def test_empty_matrix():
    assert transpose([]) == []


def test_row_of_zero_length():
    assert transpose([[]]) == []


def test_double_transpose_identity():
    m = [[1, 2, 3], [4, 5, 6]]
    assert transpose(transpose(m)) == m
