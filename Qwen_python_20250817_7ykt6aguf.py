import os
import sqlite3

# إنشاء الهيكل
os.makedirs('land_units_converter/database', exist_ok=True)
os.makedirs('land_units_converter/src', exist_ok=True)
os.makedirs('land_units_converter/web/templates', exist_ok=True)

# إنشاء الملفات
with open('land_units_converter/database/land_units_schema.sql', 'w', encoding='utf-8') as f:
    f.write("""-- محتوى ملف land_units_schema.sql من هذا الرد""")

with open('land_units_converter/src/converter.py', 'w', encoding='utf-8') as f:
    f.write("""-- محتوى ملف converter.py من هذا الرد""")

# ... (كرر لجميع الملفات)

# إنشاء قاعدة البيانات
conn = sqlite3.connect('land_units_converter/database/land_units.db')
with open('land_units_converter/database/land_units_schema.sql', 'r', encoding='utf-8') as f:
    conn.executescript(f.read())
conn.close()

print("✅ تم إنشاء المشروع بنجاح!")
print("لإنشاء ملف RAR:")
print("  - Windows: انقر بزر الماوس الأيمن → Add to archive")
print("  - Mac/Linux: rar a -m5 land_units_converter.rar land_units_converter")