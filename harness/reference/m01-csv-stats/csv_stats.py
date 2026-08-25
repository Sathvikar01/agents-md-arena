import io
from csv import DictReader


def parse_csv(text: str) -> list[dict]:
    rows = []
    reader = DictReader(io.StringIO(text))
    for row in reader:
        rows.append(row)
    return rows


def column_stats(rows: list[dict], column: str) -> dict:
    values = [float(r[column]) for r in rows if str(r[column]).strip() != ""]
    if not values:
        raise ValueError("no numeric values")
    return {
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values),
    }
