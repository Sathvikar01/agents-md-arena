def transpose(matrix: list[list]) -> list[list]:
    if not matrix:
        return []
    rows = len(matrix)
    cols = len(matrix[0])
    return [[matrix[r][c] for r in range(rows)] for c in range(cols)]
