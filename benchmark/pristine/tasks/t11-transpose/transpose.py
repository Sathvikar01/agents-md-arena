def transpose(matrix: list[list]) -> list[list]:
    """Transpose a rectangular matrix (list of equal-length rows)."""
    if not matrix:
        return []
    rows = len(matrix)
    cols = len(matrix[0])
    return [[matrix[r][c] for c in range(rows)] for r in range(cols)]
