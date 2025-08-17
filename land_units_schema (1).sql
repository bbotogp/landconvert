-- ملف: land_units_schema.sql
-- وصف: هيكل قاعدة بيانات وحدات قياس الأراضي - إصدار مختصر للتجريب
-- يمكن استبداله بالنسخة الكاملة التي شاركتَها سابقًا

CREATE TABLE IF NOT EXISTS units (
    unit_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    country TEXT NOT NULL,
    region TEXT,
    category TEXT NOT NULL,
    unit_family TEXT NOT NULL,
    usage_type TEXT NOT NULL,
    m2_value REAL NOT NULL,
    m2_value_range_min REAL,
    m2_value_range_max REAL,
    historical_origin TEXT,
    standardization_date INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS unit_equivalents (
    from_unit_id TEXT NOT NULL,
    to_unit_id TEXT NOT NULL,
    conversion_factor REAL NOT NULL,
    notes TEXT,
    PRIMARY KEY (from_unit_id, to_unit_id),
    FOREIGN KEY (from_unit_id) REFERENCES units(unit_id),
    FOREIGN KEY (to_unit_id) REFERENCES units(unit_id)
);

CREATE TABLE IF NOT EXISTS unit_references (
    unit_id TEXT NOT NULL,
    reference_type TEXT NOT NULL, -- 'law','historical','academic'
    reference_value TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS unit_variations (
    unit_id TEXT NOT NULL,
    region TEXT NOT NULL,
    m2_value REAL NOT NULL,
    description TEXT
);

-- أمثلة بيانات أساسية (قابلة للتوسعة)
INSERT INTO units (unit_id, display_name, country, region, category, unit_family, usage_type, m2_value, m2_value_range_min, m2_value_range_max, historical_origin, standardization_date, notes)
VALUES
('lbna_sanaani', 'اللبنة الصنعاني', 'YE', 'صنعاء', 'مساحة', 'لبنة', 'سكني', 44.44, 44.00, 44.88, 'مربع ضلع ~6.66م', 1970, 'قيمة مرجعية شائعة'),
('qasba_ashari_taiz', 'القصبة العشاري التعزي', 'YE', 'تعز', 'مساحة', 'قصبة', 'زراعي', 20.25, 20.0, 20.5, 'مرجعية محلية', 1970, 'تعز'),
('maad_tihami', 'المعاد التهامي', 'YE', 'الساحل الغربي', 'مساحة', 'معاد', 'زراعي', 4355.12, 4300, 4400, '≈ 98 لبنة صنعاني', 1970, 'مزارع كبيرة'),
('faddan', 'الفدان', 'EG', 'مصر والسودان', 'مساحة', 'فدان', 'زراعي', 4200.83, 4200, 4201, 'تقليدي', 1899, 'النظام المصري'),
('dunam_shami', 'الدونم الشامي', 'SY', 'بلاد الشام', 'مساحة', 'دونم', 'زراعي/سكني', 1000.00, 990, 1010, 'عثماني', 1920, 'سوريا/لبنان/فلسطين/الأردن'),
('m2', 'المتر المربع', 'GLOBAL', 'عالمي', 'مساحة', 'متر', 'عام', 1.0, 1.0, 1.0, 'متري', 1795, 'الوحدة الأساسية');

INSERT INTO unit_equivalents (from_unit_id, to_unit_id, conversion_factor, notes) VALUES
('lbna_sanaani','m2',44.44,'قيمة مرجعية'),
('lbna_sanaani','qasba_ashari_taiz', 44.44/20.25, 'حساب مباشر'),
('maad_tihami','lbna_sanaani', 98.0, 'تعريف تقليدي'),
('maad_tihami','faddan', 4355.12/4200.83, 'حساب مباشر'),
('faddan','dunam_shami', 4200.83/1000.0, 'حساب مباشر');

INSERT INTO unit_variations (unit_id, region, m2_value, description) VALUES
('lbna_sanaani','صنعاء الحضرية',44.44,'قياسي'),
('lbna_sanaani','صنعاء الريفية',43.50,'اختلاف محلي'),
('maad_tihami','الحديدة',4355.12,'قياسي');
