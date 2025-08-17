#!/usr/bin/env python3
"""
محول وحدات قياس الأراضي
الإصدار: 1.0
"""
import sqlite3
import os
from datetime import datetime

class LandUnitsConverter:
    """فئة لتحويل وحدات قياس الأراضي بين الأنظمة المختلفة"""
    
    def __init__(self, db_path='database/land_units.db'):
        """
        تهيئة المحول مع تحديد مسار قاعدة البيانات
        
        المعلمات:
        db_path -- مسار قاعدة البيانات (افتراضي: 'database/land_units.db')
        """
        self.db_path = db_path
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"قاعدة البيانات غير موجودة: {db_path}")
    
    def get_unit_data(self, unit_id, region=None):
        """
        الحصول على بيانات الوحدة مع مراعاة الاختلافات المحلية
        
        المعلمات:
        unit_id -- معرف الوحدة
        region -- المنطقة (اختياري)
        
        تُرجع:
        قاموس يحتوي على معلومات الوحدة
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # محاولة الحصول على القيمة المحلية أولاً إذا تم تحديد منطقة
        if region:
            cursor.execute("""
                SELECT m2_value FROM unit_variations 
                WHERE unit_id = ? AND region = ?
            """, (unit_id, region))
            result = cursor.fetchone()
            if result:
                m2_value = result[0]
                conn.close()
                return {'m2_value': m2_value, 'region': region, 'source': 'local'}
        
        # إذا لم تكن هناك قيمة محلية، نستخدم القيمة العامة
        cursor.execute("""
            SELECT m2_value, display_name, country, region 
            FROM units 
            WHERE unit_id = ?
        """, (unit_id,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise ValueError(f"الوحدة غير معروفة: {unit_id}")
        
        return {
            'm2_value': result[0],
            'display_name': result[1],
            'country': result[2],
            'region': result[3],
            'source': 'standard'
        }
    
    def convert(self, value, from_unit, to_unit, region=None):
        """
        تحويل قيمة من وحدة إلى أخرى
        
        المعلمات:
        value -- القيمة المراد تحويلها
        from_unit -- وحدة القياس الأصلية
        to_unit -- وحدة القياس الهدف
        region -- المنطقة (اختياري للاختلافات المحلية)
        
        تُرجع:
        قاموس يحتوي على نتيجة التحويل وتفاصيله
        """
        from_data = self.get_unit_data(from_unit, region)
        to_data = self.get_unit_data(to_unit, region)
        
        conversion_factor = from_data['m2_value'] / to_data['m2_value']
        converted_value = value * conversion_factor
        
        return {
            'input': {
                'value': value,
                'unit': from_unit,
                'display_name': from_data['display_name'],
                'region': region
            },
            'output': {
                'value': converted_value,
                'unit': to_unit,
                'display_name': to_data['display_name']
            },
            'conversion_factor': conversion_factor,
            'region': region,
            'timestamp': datetime.now().isoformat(),
            'metadata': {
                'from_source': from_data['source'],
                'to_source': to_data['source']
            }
        }
    
    def get_supported_units(self, country=None):
        """
        الحصول على قائمة جميع الوحدات المدعومة
        
        المعلمات:
        country -- الفلترة حسب الدولة (اختياري)
        
        تُرجع:
        قائمة بالوحدات المدعومة
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if country:
            cursor.execute("""
                SELECT unit_id, display_name, country, region, usage_type 
                FROM units 
                WHERE country = ?
            """, (country,))
        else:
            cursor.execute("""
                SELECT unit_id, display_name, country, region, usage_type 
                FROM units
            """)
        
        units = cursor.fetchall()
        conn.close()
        
        return [{
            'id': u[0],
            'name': u[1],
            'country': u[2],
            'region': u[3],
            'usage_type': u[4]
        } for u in units]

# مثال استخدام
if __name__ == "__main__":
    print("="*50)
    print("مرحباً بكم في محول وحدات قياس الأراضي")
    print("="*50)
    
    try:
        # تحديد مسار قاعدة البيانات الصحيح
        DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database', 'land_units.db')
        converter = LandUnitsConverter(DB_PATH)
        
        # مثال 1: تحويل 10 لبنة صنعاني إلى فدان
        result = converter.convert(10, 'lbna_sanaani', 'faddan')
        print(f"\n10 لبنة صنعاني = {result['output']['value']:.4f} فدان")
        print(f"عامل التحويل: {result['conversion_factor']:.6f}")
        
        # مثال 2: تحويل 1 معاد تهامي إلى لبنة ذماري
        result = converter.convert(1, 'maad_tihami', 'lbna_dhamari')
        print(f"\n1 معاد تهامي = {result['output']['value']:.4f} لبنة ذماري")
        print(f"عامل التحويل: {result['conversion_factor']:.6f}")
        
        # مثال 3: تحويل مع اختلاف محلي
        result = converter.convert(5, 'lbna_sanaani', 'qasba_ashari_taiz', region='صنعاء الريفية')
        print(f"\n5 لبنة صنعاني (في صنعاء الريفية) = {result['output']['value']:.4f} قصبة عشاري تعزي")
        print(f"عامل التحويل: {result['conversion_factor']:.6f}")
        
        # عرض جميع الوحدات المدعومة
        print("\nجميع الوحدات المدعومة (أول 5 وحدات):")
        for unit in converter.get_supported_units()[:5]:
            print(f"- {unit['name']} ({unit['id']}) - {unit['country']} - {unit['usage_type']}")
            
    except Exception as e:
        print(f"حدث خطأ: {str(e)}")
        print("\nلحل المشكلة، تأكد من:")
        print("1. وجود ملف قاعدة البيانات في المسار الصحيح")
        print("2. تشغيل السكربت من المجلد الصحيح")
        print("3. إنشاء قاعدة البيانات باستخدام ملف land_units_schema.sql")