def flatten(nested: list) -> list:
    """Flatten an arbitrarily deep nested list into a flat list.

    Only lists are containers; everything else (str, tuple, etc.) is a leaf.
    """
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result
