# محول وحدات قياس الأراضي (Demo)
- أنشئ قاعدة البيانات:
```
sqlite3 database/land_units.db < database/land_units_schema.sql
```
- تحقق:
```
python src/verify_data.py
```
- شغل الويب:
```
python web/app.py
```
