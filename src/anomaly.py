"""Day 7: SQL-based anomaly detection.

Flags (a) duplicate invoice numbers and (b) tax-rate outliers over the
`data/invoices.db` SQLite table, via SQL/statistics — not LLM judgment.
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def check_duplicates(conn: sqlite3.Connection) -> list[dict]:
    # TODO(day7): SELECT invoice_number, COUNT(*) ... GROUP BY ... HAVING COUNT(*) > 1
    raise NotImplementedError


def check_tax_outliers(conn: sqlite3.Connection) -> list[dict]:
    # TODO(day7): compute tax-rate distribution (tax/total) and flag
    # statistical outliers (e.g. > N std devs from the mean).
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser(description="Run anomaly checks over the invoices DB")
    parser.add_argument("db_path", type=Path, default=Path("data/invoices.db"), nargs="?")
    args = parser.parse_args()
    raise NotImplementedError


if __name__ == "__main__":
    main()
