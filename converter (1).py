#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""محول وحدات قياس الأراضي (SQLite)
الإصدار: 1.0 (Demo)
"""
import sqlite3
from datetime import datetime
from typing import Optional, Dict

class LandUnitsConverter:
    def __init__(self, db_path: str='database/land_units.db'):
        self.db_path = db_path

    def _fetch_m2(self, unit_id: str, region: Optional[str]=None) -> float:
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        m2 = None
        if region:
            cur.execute("""SELECT m2_value FROM unit_variations
                           WHERE unit_id=? AND region=?""", (unit_id, region))
            row = cur.fetchone()
            if row: m2 = float(row[0])
        if m2 is None:
            cur.execute("SELECT m2_value FROM units WHERE unit_id=?", (unit_id,))
            row = cur.fetchone()
            if not row:
                con.close()
                raise ValueError(f"الوحدة غير موجودة: {unit_id}")
            m2 = float(row[0])
        con.close()
        return m2

    def convert(self, value: float, from_unit: str, to_unit: str, region: Optional[str]=None) -> Dict:
        from_m2 = self._fetch_m2(from_unit, region)
        to_m2   = self._fetch_m2(to_unit, region)
        factor = from_m2 / to_m2
        return {
            "input_value": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
            "region": region,
            "conversion_factor": factor,
            "result": value * factor,
            "timestamp": datetime.now().isoformat()
        }

    def list_units(self, country: Optional[str]=None):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        if country:
            cur.execute("SELECT unit_id, display_name, country, region FROM units WHERE country=?", (country,))
        else:
            cur.execute("SELECT unit_id, display_name, country, region FROM units")
        rows = cur.fetchall()
        con.close()
        return [{"unit_id":r[0],"display_name":r[1],"country":r[2],"region":r[3]} for r in rows]

if __name__ == "__main__":
    c = LandUnitsConverter()
    print(c.convert(10,'lbna_sanaani','faddan'))
