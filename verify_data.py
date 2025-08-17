#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3, sys

def verify_database(db_path='database/land_units.db'):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    # check tables
    for t in ['units','unit_equivalents','unit_references','unit_variations']:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (t,))
        assert cur.fetchone(), f"❌ الجدول مفقود: {t}"
    # minimum counts
    cur.execute("SELECT COUNT(*) FROM units"); assert cur.fetchone()[0] >= 5, "❌ عدد الوحدات أقل من المتوقع"
    cur.execute("SELECT COUNT(*) FROM unit_equivalents"); assert cur.fetchone()[0] >= 3, "❌ التحويلات قليلة"
    print("✅ قاعدة البيانات تبدو سليمة.")
    con.close()

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv)>1 else 'database/land_units.db'
    verify_database(path)
