-- ملف: land_units_schema.sql
-- وصف: هيكل قاعدة بيانات وحدات قياس الأراضي
-- الإصدار: 1.0

-- إنشاء الجداول الأساسية
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
    reference_type TEXT NOT NULL,
    reference_value TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (unit_id) REFERENCES units(unit_id)
);

CREATE TABLE IF NOT EXISTS unit_variations (
    unit_id TEXT NOT NULL,
    region TEXT NOT NULL,
    m2_value REAL NOT NULL,
    description TEXT,
    FOREIGN KEY (unit_id) REFERENCES units(unit_id)
);

-- إدخال البيانات الأساسية (اليمن)
INSERT OR REPLACE INTO units (unit_id, display_name, country, region, category, unit_family, usage_type, m2_value, m2_value_range_min, m2_value_range_max, historical_origin, standardization_date, notes)
VALUES 
('lbna_sanaani', 'اللبنة الصنعاني', 'YE', 'صنعاء', 'مساحة', 'لبنة', 'سكني', 44.44, 44.00, 44.88, 'مصدرها قياس مربع طول ضلعه 6.66 متر (جذر 44.44)', 1970, 'تستخدم في قياس الأراضي السكنية في صنعاء'),
('lbna_dhamari', 'اللبنة الذماري', 'YE', 'ذمار', 'مساحة', 'لبنة', 'سكني', 114.49, 113.00, 116.00, 'مصدرها مربع طول ضلعه 10.70 متر', 1970, 'تستخدم في قياس الأراضي السكنية في ذمار'),
('qasba_ashari_taiz', 'القصبة العشاري التعزي', 'YE', 'تعز', 'مساحة', 'قصبة', 'زراعي', 20.25, 20.00, 20.50, 'مصدرها 10 × 2.025 متر', 1970, 'تستخدم في قياس الأراضي الزراعية في تعز'),
('qasba_ithnay_ashr_taiz', 'القصبة الاثنا عشري الهدوي التعزي', 'YE', 'تعز', 'مساحة', 'قصبة', 'زراعي', 29.16, 28.50, 29.80, 'مصدرها 12 × 2.43 متر', 1970, 'تستخدم في قياس الأراضي الزراعية في تعز'),
('maad_tihami', 'المعاد التهامي', 'YE', 'الساحل الغربي', 'مساحة', 'معاد', 'زراعي', 4355.12, 4300.00, 4400.00, '98 لبنة صنعاني', 1970, 'يستخدم في قياس المزارع الكبيرة في المناطق الساحلية'),

-- إدخال البيانات الأساسية (مصر والسودان)
('faddan', 'الفدان', 'EG', 'مصر والسودان', 'مساحة', 'فدان', 'زراعي', 4200.83, 4200.00, 4201.00, 'نظام فلقي يعود للعصور الفرعونية', 1899, 'وحدة قياس أراضي زراعية رئيسية في مصر والسودان'),
('qirat', 'القيراط', 'EG', 'مصر والسودان', 'مساحة', 'قيراط', 'زراعي', 175.09, 175.00, 175.10, '1/24 فدان', 1899, 'وحدة فرعية للفدان'),
('sahm', 'السهم', 'EG', 'مصر والسودان', 'مساحة', 'سهم', 'زراعي', 7.29, 7.28, 7.30, '1/24 قيراط', 1899, 'أصغر وحدة في النظام الزراعي المصري'),

-- إدخال البيانات الأساسية (بلاد الشام)
('dunam_shami', 'الدونم الشامي', 'SY', 'بلاد الشام', 'مساحة', 'دونم', 'زراعي/سكني', 1000.00, 990.00, 1010.00, 'نظام عثماني تقليدي', 1920, 'وحدة قياس رئيسية في سوريا ولبنان وفلسطين والأردن'),

-- إدخال البيانات الأساسية (العراق)
('dunam_iraqi', 'الدونم العراقي', 'IQ', 'العراق', 'مساحة', 'دونم', 'زراعي', 2500.00, 2450.00, 2550.00, 'نظام عثماني مع تعديلات عراقية', 1958, 'وحدة قياس رئيسية في العراق'),

-- إدخال البيانات الأساسية (الوحدات الدولية)
('m2', 'المتر المربع', 'GLOBAL', 'عالمي', 'مساحة', 'متر', 'عام', 1.00, 1.00, 1.00, 'نظام متري دولي', 1795, 'الوحدة الأساسية لقياس المساحة'),
('hectare', 'الهكتار', 'GLOBAL', 'عالمي', 'مساحة', 'هكتار', 'عام', 10000.00, 10000.00, 10000.00, 'نظام متري دولي', 1795, '100 × 100 متر'),
('acre', 'الآكر', 'GLOBAL', 'عالمي', 'مساحة', 'آكر', 'عام', 4046.86, 4046.86, 4046.86, 'نظام إمبراطوري بريطاني', 1878, 'وحدة شائعة في الولايات المتحدة وبريطانيا');

-- إدخال التحويلات الأساسية
INSERT OR REPLACE INTO unit_equivalents (from_unit_id, to_unit_id, conversion_factor, notes)
VALUES
-- تحويلات اللبنة الصنعاني
('lbna_sanaani', 'm2', 44.44, 'القيمة الأساسية'),
('lbna_sanaani', 'qasba_ashari_taiz', 2.194, '44.44 / 20.25'),
('lbna_sanaani', 'faddan', 0.01057, '44.44 / 4200.83'),
('lbna_sanaani', 'dunam_shami', 0.04444, '44.44 / 1000'),

-- تحويلات المعاد التهامي
('maad_tihami', 'lbna_sanaani', 98.00, 'القيمة المعرفة'),
('maad_tihami', 'faddan', 1.036, '4355.12 / 4200.83'),
('maad_tihami', 'dunam_shami', 4.355, '4355.12 / 1000'),

-- تحويلات الفدان
('faddan', 'qirat', 24.00, 'النظام المصري'),
('faddan', 'dunam_shami', 4.20, '4200.83 / 1000'),
('faddan', 'hectare', 0.42, '4200.83 / 10000'),

-- تحويلات القيراط
('qirat', 'sahm', 24.00, 'النظام المصري'),
('qirat', 'm2', 175.09, 'القيمة الأساسية'),

-- تحويلات الدونم الشامي
('dunam_shami', 'm2', 1000.00, 'القيمة الأساسية'),
('dunam_shami', 'hectare', 0.10, '1000 / 10000'),
('dunam_shami', 'faddan', 0.238, '1000 / 4200.83'),

-- تحويلات الدونم العراقي
('dunam_iraqi', 'm2', 2500.00, 'القيمة الأساسية'),
('dunam_iraqi', 'dunam_shami', 2.50, '2500 / 1000'),
('dunam_iraqi', 'faddan', 0.595, '2500 / 4200.83');

-- إدخال المراجع القانونية
INSERT OR REPLACE INTO unit_references (unit_id, reference_type, reference_value, description)
VALUES
-- مراجع اللبنة الصنعاني
('lbna_sanaani', 'law', 'المرسوم الجمهوري رقم 12 لسنة 1970', 'المرسوم الجمهوري رقم 12 لسنة 1970 (الفصل الثالث: وحدات القياس)'),
('lbna_sanaani', 'academic', 'المجلة الزراعية العربية 1985', 'دراسة وحدات القياس في اليمن - المجلة الزراعية العربية 1985'),

-- مراجع الفدان
('faddan', 'law', 'القانون المصري رقم 50 لسنة 1899', 'قانون تنظيم القياسات الزراعية في مصر 1899'),
('faddan', 'academic', 'الموسوعة الزراعية المصرية', 'الفصل الثالث: وحدات القياس الزراعية'),

-- مراجع الدونم الشامي
('dunam_shami', 'law', 'مرسوم الانتداب البريطاني 1920', 'مرسوم تنظيم الأراضي في بلاد الشام 1920');

-- إدخال الاختلافات المحلية
INSERT OR REPLACE INTO unit_variations (unit_id, region, m2_value, description)
VALUES
-- اختلافات اللبنة الصنعاني
('lbna_sanaani', 'صنعاء الحضرية', 44.44, 'القيمة القياسية في المناطق الحضرية'),
('lbna_sanaani', 'صنعاء الريفية', 43.50, 'تختلف بنسبة 2% في المناطق الريفية'),

-- اختلافات المعاد التهامي
('maad_tihami', 'الحديدة', 4355.12, 'القيمة القياسية في الحديدة'),
('maad_tihami', 'تعز الساحلية', 4300.00, 'تختلف في المناطق الساحلية لتعز');