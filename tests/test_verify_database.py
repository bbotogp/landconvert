import sqlite3
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verify_data import verify_database


def _create_tables(cur):
    cur.execute("CREATE TABLE units (unit_id TEXT PRIMARY KEY, m2_value REAL)")
    cur.execute("CREATE TABLE unit_equivalents (id INTEGER)")
    cur.execute("CREATE TABLE unit_references (id INTEGER)")
    cur.execute("CREATE TABLE unit_variations (id INTEGER)")


def test_verify_database_valid(tmp_path):
    db_file = tmp_path / "db.sqlite"
    with sqlite3.connect(db_file) as con:
        cur = con.cursor()
        _create_tables(cur)
        for i in range(5):
            cur.execute("INSERT INTO units VALUES (?, ?)", (f"u{i}", float(i + 1)))
        for i in range(3):
            cur.execute("INSERT INTO unit_equivalents VALUES (?)", (i,))
        con.commit()
    verify_database(str(db_file))


def test_verify_database_invalid_counts(tmp_path):
    db_file = tmp_path / "db.sqlite"
    with sqlite3.connect(db_file) as con:
        cur = con.cursor()
        _create_tables(cur)
        cur.execute("INSERT INTO units VALUES ('u1', 1.0)")
        con.commit()
    with pytest.raises(AssertionError, match="عدد الوحدات"):
        verify_database(str(db_file))

