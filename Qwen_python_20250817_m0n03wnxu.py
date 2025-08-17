#!/usr/bin/env python3
"""
سكربت التحقق من صحة بيانات قاعدة وحدات قياس الأراضي
الإصدار: 1.0
"""
import sqlite3
import sys
import os

def verify_database(db_path='database/land_units.db'):
    """
    التحقق من صحة قاعدة البيانات
    
    المعلمات:
    db_path -- مسار قاعدة البيانات
    
    تُرجع:
    صحيح إذا كانت قاعدة البيانات سليمة، خطأ إذا لم تكن
    """
    print(f"🔍 جارٍ التحقق من قاعدة البيانات: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"❌ خطأ: ملف قاعدة البيانات غير موجود في المسار: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # التحقق من وجود الجداول
        tables = ['units', 'unit_equivalents', 'unit_references', 'unit_variations']
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not cursor.fetchone():
                print(f"❌ خطأ: الجدول '{table}' غير موجود في قاعدة البيانات")
                return False
            print(f"✅ تم العثور على الجدول: {table}")
        
        # التحقق من وجود وحدات
        cursor.execute("SELECT COUNT(*) FROM units")
        total_units = cursor.fetchone()[0]
        if total_units < 10:
            print(f"❌ خطأ: عدد الوحدات أقل من المتوقع ({total_units})")
            return False
        print(f"✅ وجد {total_units} وحدة مدعومة")
        
        # التحقق من وجود تحويلات
        cursor.execute("SELECT COUNT(*) FROM unit_equivalents")
        conversions = cursor.fetchone()[0]
        if conversions < 10:
            print(f"❌ خطأ: عدد التحويلات أقل من المتوقع ({conversions})")
            return False
        print(f"✅ وجد {conversions} تحويلة بين الوحدات")
        
        print("\n✅ جميع الفحوصات ناجحة: قاعدة البيانات سليمة وجاهزة للاستخدام")
        return True
        
    except sqlite3.Error as e:
        print(f"❌ خطأ في قاعدة البيانات: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # تحديد مسار قاعدة البيانات تلقائياً
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'database', 'land_units.db')
    
    print(f"جارٍ التحقق من قاعدة البيانات في: {db_path}")
    
    if verify_database(db_path):
        print("\nلإنشاء قاعدة البيانات من الصفر، يمكنك استخدام:")
        print(f"  sqlite3 {db_path} < database/land_units_schema.sql")
        sys.exit(0)
    else:
        print("\nلإنشاء قاعدة البيانات:")
        print(f"  1. تأكد من وجود ملف database/land_units_schema.sql")
        print(f"  2. نفّذ الأمر التالي:")
        print(f"     sqlite3 {db_path} < database/land_units_schema.sql")
        sys.exit(1)