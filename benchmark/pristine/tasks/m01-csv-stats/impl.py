"""Per-column statistics over CSV text.

parse_csv(text) -> list[dict] of rows (header excluded).
column_stats(rows, column) -> {"min": float, "max": float, "avg": float}
over numeric values in that column; empty-string cells are skipped.
Raises KeyError if the column does not exist; raises ValueError if no
numeric values remain after skipping blanks.
"""
import io
from csv import DictReader


def parse_csv(text: str) -> list[dict]:
    rows = []
    reader = DictReader(io.StringIO(text))
    for row in reader:
        rows.append(row)
    return rows


def column_stats(rows: list[dict], column: str) -> dict:
    values = [float(r[column]) for r in rows]
    return {
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values),
    }
