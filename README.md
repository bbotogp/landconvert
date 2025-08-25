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

## Flutter Demo
يوجد مثال مبسط للمشروع باستخدام Flutter داخل مجلد `flutter_app`.
لتشغيله بعد تثبيت Flutter:
```
cd flutter_app
flutter run
```
