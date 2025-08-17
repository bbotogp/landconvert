#!/usr/bin/env python3
"""
واجهة ويب لمحول وحدات قياس الأراضي
الإصدار: 1.0
"""
from flask import Flask, render_template, request, jsonify
import os
import sys

# إضافة مسار المشروع إلى PYTHONPATH
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from src.converter import LandUnitsConverter

app = Flask(__name__)

# تهيئة محول الوحدات
try:
    DB_PATH = os.path.join(base_dir, 'database', 'land_units.db')
    converter = LandUnitsConverter(DB_PATH)
    print(f"✅ تم تحميل محول الوحدات بنجاح من: {DB_PATH}")
except Exception as e:
    print(f"⚠️ تحذير: فشل تهيئة محول الوحدات: {str(e)}")
    converter = None

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template('index.html')

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    """تحويل وحدات القياس"""
    if not converter:
        return render_template('error.html', message="فشل تحميل محول الوحدات")
    
    if request.method == 'POST':
        try:
            value = float(request.form['value'])
            from_unit = request.form['from_unit']
            to_unit = request.form['to_unit']
            region = request.form.get('region', None)
            
            result = converter.convert(value, from_unit, to_unit, region)
            return render_template('conversion.html', result=result, units=converter.get_supported_units())
            
        except ValueError as e:
            error = f"خطأ في المدخلات: {str(e)}"
            return render_template('conversion.html', error=error, units=converter.get_supported_units())
        except Exception as e:
            error = f"حدث خطأ أثناء التحويل: {str(e)}"
            return render_template('conversion.html', error=error, units=converter.get_supported_units())
    
    # إذا كانت طريقة GET
    units = converter.get_supported_units() if converter else []
    return render_template('convert.html', units=units)

@app.route('/api/convert', methods=['POST'])
def api_convert():
    """واجهة برمجية لتحويل الوحدات"""
    if not converter:
        return jsonify({"error": "فشل تحميل محول الوحدات"}), 500
    
    try:
        data = request.json
        value = float(data['value'])
        from_unit = data['from_unit']
        to_unit = data['to_unit']
        region = data.get('region', None)
        
        result = converter.convert(value, from_unit, to_unit, region)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/units')
def api_units():
    """واجهة برمجية للحصول على الوحدات المدعومة"""
    if not converter:
        return jsonify({"error": "فشل تحميل محول الوحدات"}), 500
    
    country = request.args.get('country', None)
    units = converter.get_supported_units(country)
    return jsonify(units)

if __name__ == '__main__':
    print("\n===== محول وحدات قياس الأراضي =====")
    print("لبدء الخادم:")
    print("  1. تأكد من تثبيت المتطلبات: pip install -r requirements.txt")
    print("  2. تأكد من وجود قاعدة البيانات في database/land_units.db")
    print("  3. افتح المتصفح وانتقل إلى: http://localhost:5000\n")
    
    app.run(debug=True, port=5000)