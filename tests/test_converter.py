import sqlite3
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from converter import LandUnitsConverter


def _setup_db(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("CREATE TABLE units (unit_id TEXT PRIMARY KEY, m2_value REAL)")
    cur.executemany(
        "INSERT INTO units (unit_id, m2_value) VALUES (?, ?)",
        [("u1", 1.0), ("u2", 10.0)],
    )
    con.commit()
    con.close()


def test_convert_basic(tmp_path):
    db_file = tmp_path / "db.sqlite"
    _setup_db(db_file)
    conv = LandUnitsConverter(str(db_file))
    result = conv.convert(2, "u1", "u2")
    assert result["conversion_factor"] == pytest.approx(0.1)
    assert result["result"] == pytest.approx(0.2)
