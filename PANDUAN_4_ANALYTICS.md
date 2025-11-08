# 🧠 Panduan 4 Jenis Analytics - Dashboard DBD Indonesia

Dashboard ini menggunakan **4 jenis analytics** untuk memberikan insight komprehensif dari data DBD yang Anda upload.

---

## 📚 Apa itu 4 Jenis Analytics?

Analytics adalah proses analisis data untuk mendapatkan insight yang dapat digunakan untuk pengambilan keputusan. Ada 4 level analytics yang semakin kompleks:

```
Descriptive → Diagnostic → Predictive → Prescriptive
   (Apa?)    (Mengapa?)    (Akan?)      (Lakukan?)
```

---

## 📊 1. DESCRIPTIVE ANALYTICS
### "Apa yang Terjadi?"

**Tujuan**: Memahami kondisi SAAT INI berdasarkan data historis

**Pertanyaan yang Dijawab**:
- Berapa total kasus DBD di Indonesia?
- Provinsi mana yang paling terdampak?
- Bagaimana distribusi kasus per wilayah?
- Apa tren umum yang terlihat dari data?

**Output Dashboard**:
```
A. Situasi Nasional
   - Total kasus: 45,234 kasus
   - Periode: 2020-2023
   - Growth rate: +15.3%

B. Distribusi Regional
   - Top 3 Provinsi:
     1. DKI Jakarta: 12,456 kasus
     2. Jawa Barat: 10,234 kasus
     3. Jawa Timur: 8,901 kasus

C. Pola Temporal
   - 2020: 10,500 kasus
   - 2021: 11,200 kasus (+6.7%)
   - 2022: 11,800 kasus (+5.4%)
   - 2023: 12,734 kasus (+7.9%)

D. Key Metrics
   - Rata-rata kasus per tahun: 11,308
   - Standar deviasi: 856
   - Jumlah hotspot: 15 kabupaten/kota
```

**Metode Analisis**:
- Sum, average, count
- Distribusi data
- Trend historis
- Visualisasi (chart, grafik)

**Value untuk User**:
✅ Memahami kondisi saat ini
✅ Baseline untuk perbandingan
✅ Identifikasi area kritis

---

## 🔍 2. DIAGNOSTIC ANALYTICS
### "Mengapa Ini Terjadi?"

**Tujuan**: Memahami PENYEBAB dan FAKTOR di balik kondisi saat ini

**Pertanyaan yang Dijawab**:
- Mengapa DKI Jakarta memiliki kasus tertinggi?
- Faktor apa yang menyebabkan peningkatan kasus?
- Mengapa beberapa wilayah berhasil menurunkan kasus?
- Apa gap dalam program mitigasi saat ini?

**Output Dashboard**:
```
A. Root Cause Analysis
   - DKI Jakarta tinggi karena:
     * Kepadatan penduduk sangat tinggi
     * Genangan air di musim hujan
     * Mobilitas penduduk tinggi

B. Faktor Risiko Potensial
   Faktor Geografis:
   - Curah hujan tinggi di Jakarta, Bogor
   - Suhu optimal untuk nyamuk (25-30°C)
   
   Faktor Demografis:
   - Kepadatan >10,000/km² korelasi +75%
   - Area urban lebih tinggi vs rural
   
   Faktor Lingkungan:
   - Sanitasi kurang di 45% wilayah
   - Pengelolaan sampah buruk
   
   Faktor Program:
   - Coverage fogging hanya 60%
   - Edukasi masyarakat kurang efektif

C. Correlation & Patterns
   - Korelasi kepadatan vs kasus: r=0.78
   - Pola musiman: puncak di Jan-Mar

D. Gap Analysis
   - Program fogging tidak merata
   - Surveilans tidak real-time
   - Koordinasi antar stakeholder lemah
```

**Metode Analisis**:
- Correlation analysis
- Root cause analysis
- Comparative analysis
- Pattern recognition
- Statistical testing

**Value untuk User**:
✅ Memahami akar masalah
✅ Identifikasi faktor risiko
✅ Dasar untuk intervensi targeted

---

## 🔮 3. PREDICTIVE ANALYTICS
### "Apa yang Akan Terjadi?"

**Tujuan**: Memprediksi MASA DEPAN berdasarkan trend dan pattern

**Pertanyaan yang Dijawab**:
- Berapa proyeksi kasus tahun depan?
- Wilayah mana yang berisiko outbreak?
- Kapan periode kritis akan terjadi?
- Bagaimana berbagai skenario ke depan?

**Output Dashboard**:
```
A. Proyeksi Trend
   - Proyeksi 2024: 13,500-14,200 kasus (+6-11%)
   - Potensi outbreak di 5 provinsi
   - Peak season: Januari-Maret 2024

B. Early Warning Indicators
   Wilayah yang Perlu Diwaspadai:
   - HIGH RISK: Jakarta, Bekasi, Tangerang
   - MEDIUM RISK: Bandung, Surabaya, Semarang
   
   Indikator Risiko:
   - Growth rate >10% per tahun
   - Trend meningkat 3 tahun berturut-turut
   - Kepadatan >8,000/km²

C. Scenario Analysis
   Best Case: -15% (dengan intervensi maksimal)
   Most Likely: +7% (business as usual)
   Worst Case: +25% (tanpa tindakan)

D. Risk Assessment
   Prioritas Tinggi (12 kabupaten/kota):
   - Jakarta Timur, Jakarta Utara
   - Bekasi Kota, Tangerang Selatan
   - Bandung Kota, dll
   
   Prioritas Menengah (18 kabupaten/kota)
   Monitoring (35 kabupaten/kota)
```

**Metode Analisis**:
- Trend analysis
- Time series forecasting
- Machine learning models
- Scenario modeling
- Risk scoring

**Value untuk User**:
✅ Antisipasi masalah sebelum terjadi
✅ Alokasi resource proaktif
✅ Early warning system

---

## 💡 4. PRESCRIPTIVE ANALYTICS
### "Apa yang Harus Dilakukan?"

**Tujuan**: Memberikan REKOMENDASI KONKRET dan ACTIONABLE

**Pertanyaan yang Dijawab**:
- Tindakan apa yang harus segera dilakukan?
- Bagaimana prioritas intervensi?
- Resource apa yang diperlukan?
- Siapa yang harus melakukan apa?

**Output Dashboard**:
```
A. IMMEDIATE ACTIONS (0-3 Bulan) 🚨
   1. FOGGING MASSAL di 12 wilayah prioritas tinggi
      Target: Jakarta Timur, Utara, Bekasi
      Resource: 50 tim fogging, 500L insektisida
      Budget: Rp 2.5M
      KPI: Turunkan kasus 30% dalam 3 bulan

   2. SURVEILANS KETAT di 18 wilayah prioritas menengah
      Target: Daily monitoring kasus baru
      Resource: 36 petugas surveilans
      Budget: Rp 1.8M
      KPI: Deteksi outbreak dalam 24 jam

   3. KAMPANYE EDUKASI darurat
      Target: 5 juta rumah tangga di area HIGH RISK
      Channel: TV, radio, social media, door-to-door
      Budget: Rp 3.5M
      KPI: Awareness 80%, adoption 3M Plus 60%

B. SHORT-TERM STRATEGIES (3-12 Bulan) 📋
   1. Program JUMANTIK berbasis komunitas
      Timeline: 6 bulan
      Target: 100 kelurahan
      Budget: Rp 5M
      Impact: -25% larva index

   2. Integrasi SISTEM SURVEILANS digital
      Timeline: 8 bulan
      Deliverable: Dashboard real-time
      Budget: Rp 8M
      Impact: Response time <24 jam

   3. TRAINING petugas kesehatan
      Timeline: 12 bulan
      Peserta: 500 petugas
      Budget: Rp 3M
      Impact: Quality surveilans +40%

C. LONG-TERM STRATEGIES (1-3 Tahun) 🎯
   1. Infrastruktur pengelolaan AIR & SAMPAH
      Timeline: 2 tahun
      Scope: 50 kelurahan prioritas
      Budget: Rp 50M
      Impact: -40% breeding sites

   2. Kebijakan WAJIB 3M Plus di perumahan
      Timeline: 18 bulan
      Enforcement: Sanksi administratif
      Budget: Rp 2M
      Impact: Compliance 75%

   3. Research & Development vaksin DBD lokal
      Timeline: 3 tahun
      Partner: Universitas, BPOM
      Budget: Rp 100M
      Impact: Vaksinasi 50% populasi

D. PRIORITAS INTERVENSI PER WILAYAH
   HIGH PRIORITY (12 kabupaten/kota):
   - Jakarta Timur: Fogging 2x/bulan + edukasi
   - Bekasi: Surveilans harian + jumantik
   - Bandung: Program 3M Plus + infrastruktur
   
   MEDIUM PRIORITY (18 kabupaten/kota):
   - Monitoring mingguan
   - Edukasi berkelanjutan
   - Fogging area terdampak
   
   MONITORING (35 kabupaten/kota):
   - Surveilans rutin
   - Maintain program existing

E. RESOURCE ALLOCATION
   Total Budget Needed: Rp 175M untuk 1 tahun
   
   Breakdown:
   - Fogging & insektisida: 35% (Rp 61M)
   - Edukasi & kampanye: 20% (Rp 35M)
   - Surveilans & sistem: 25% (Rp 44M)
   - Infrastruktur: 15% (Rp 26M)
   - Training: 5% (Rp 9M)
   
   Human Resources:
   - 200 petugas fogging
   - 100 surveyor
   - 50 health educator
   - 20 data analyst

F. KEY PERFORMANCE INDICATORS (KPI)
   Short-term (3 bulan):
   - ↓ 30% kasus di area HIGH PRIORITY
   - 80% awareness masyarakat
   - Response time <24 jam
   
   Medium-term (12 bulan):
   - ↓ 40% kasus nasional
   - 90% coverage fogging
   - 75% compliance 3M Plus
   
   Long-term (3 tahun):
   - ↓ 60% kasus nasional
   - Zero outbreak
   - Eliminasi DBD di 20 kabupaten

G. STAKEHOLDER ACTIONS
   KEMENKES:
   - Alokasi budget nasional
   - Koordinasi lintas provinsi
   - Monitoring & evaluasi nasional
   - Procurement insektisida massal
   
   DINKES PROVINSI:
   - Implementasi program di lapangan
   - Koordinasi dengan kab/kota
   - Reporting & surveilans
   - Training petugas
   
   PUSKESMAS:
   - Fogging rutin
   - Surveilans harian
   - Edukasi door-to-door
   - Case management
   
   MASYARAKAT:
   - Praktek 3M Plus
   - Laporkan kasus segera
   - Partisipasi jumantik
   - Jaga kebersihan lingkungan
```

**Metode Analisis**:
- Optimization algorithms
- Cost-benefit analysis
- Resource allocation modeling
- Simulation
- Decision trees

**Value untuk User**:
✅ Action plan yang jelas
✅ Prioritas berdasarkan impact & urgency
✅ Resource planning
✅ Clear accountability

---

## 🎯 Bagaimana 4 Analytics Bekerja Bersama?

### Siklus Decision Making:

```
1. DESCRIPTIVE
   └─> "Total kasus naik 15.3%, Jakarta tertinggi"
        │
2. DIAGNOSTIC
   └─> "Karena kepadatan tinggi + sanitasi buruk + fogging tidak merata"
        │
3. PREDICTIVE
   └─> "Jika tidak ada tindakan, proyeksi naik 25% tahun depan"
        │
4. PRESCRIPTIVE
   └─> "Lakukan fogging massal, perbaiki sanitasi, edukasi masyarakat"
        │
        └─> IMPLEMENTASI → Monitor → Kembali ke DESCRIPTIVE
```

### Contoh Kasus Nyata:

**Skenario**: Kabupaten X memiliki kasus DBD meningkat drastis

1. **Descriptive**: 
   - Kasus naik dari 150 (2022) → 350 (2023) = +133%
   - Hotspot: 5 kelurahan di pusat kota

2. **Diagnostic**: 
   - Penyebab: Program fogging hanya 40% coverage
   - Faktor: Banyak rumah kosong, genangan air, sampah menumpuk
   - Gap: Tidak ada koordinasi RT/RW

3. **Predictive**: 
   - Proyeksi 2024: 600-700 kasus jika tidak ada tindakan
   - Risk: Outbreak di 10 kelurahan lainnya
   - Timeline: Peak di Feb-Mar 2024

4. **Prescriptive**:
   - **Immediate**: Fogging massal 5 kelurahan dalam 2 minggu
   - **Short-term**: Training 50 kader jumantik dalam 3 bulan
   - **Long-term**: Perbaikan drainase dalam 1 tahun
   - **Budget**: Rp 500M
   - **Target**: Turunkan kasus 50% dalam 6 bulan

---

## 🚀 Cara Menggunakan di Dashboard

### Step-by-Step:

1. **Upload Data CSV**
   - Pastikan data punya kolom lengkap
   - Minimal 2 tahun data untuk trend analysis

2. **Filter Data (Optional)**
   - Fokus ke provinsi/wilayah tertentu
   - Pilih periode spesifik

3. **Input API Key Gemini**
   - Get from: https://aistudio.google.com/app/apikey

4. **Klik "Generate 4 Analytics Insights"**
   - Tunggu 30-60 detik
   - AI akan analisis data Anda

5. **Review Results**
   - Baca semua 4 jenis analytics
   - Focus pada Prescriptive untuk action items

6. **Take Action**
   - Implementasikan rekomendasi
   - Monitor progress
   - Upload data baru untuk re-analyze

---

## 💡 Tips untuk Hasil Terbaik

### 1. Data Quality
✅ **DO**:
- Data lengkap minimal 2-3 tahun
- Konsisten naming provinsi/kabupaten
- No missing values di kolom penting

❌ **DON'T**:
- Data cuma 1 tahun (trend tidak jelas)
- Banyak missing values
- Format tidak konsisten

### 2. Filtering Strategy
✅ **DO**:
- Filter untuk analisis spesifik wilayah
- Compare multiple periods
- Focus on problem areas

❌ **DON'T**:
- Filter terlalu sedikit data
- Mixed unrelated regions

### 3. Interpretation
✅ **DO**:
- Baca semua 4 analytics secara utuh
- Cross-reference dengan data lain
- Validate dengan domain knowledge

❌ **DON'T**:
- Hanya baca Prescriptive saja
- Skip context dari Descriptive/Diagnostic
- Implement tanpa validasi

---

## 📊 Metrics untuk Evaluasi

### KPI Dashboard Analytics:

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Accuracy Descriptive | >95% | - | - |
| Root Cause Identified | >3 | - | - |
| Prediction Confidence | >70% | - | - |
| Actionable Recommendations | >10 | - | - |
| Implementation Rate | >60% | - | - |

---

## 🆘 FAQ

### Q: Berapa lama generate insights?
**A**: 30-60 detik tergantung ukuran data. Data lebih besar butuh waktu lebih lama.

### Q: Apakah bisa untuk data selain DBD?
**A**: Ya! Format CSV yang sama bisa digunakan untuk penyakit lain, cukup sesuaikan kolom.

### Q: Akurasi prediksi berapa persen?
**A**: Tergantung kualitas dan jumlah data. Data 3+ tahun bisa capai 70-80% akurasi.

### Q: Bisakah customize prompt AI?
**A**: Saat ini tidak via UI, tapi bisa edit di code (dashboard.py function get_ai_insights).

### Q: Hasil berbeda setiap generate?
**A**: Sedikit berbeda karena nature AI, tapi insight utama konsisten.

---

## 📚 Resources Tambahan

- **Tutorial Video**: [Coming Soon]
- **Case Study**: [Coming Soon]
- **API Documentation**: https://ai.google.dev/docs
- **Support**: Open issue di repository

---

**Dashboard DBD Indonesia | 4 Analytics Powered by Google Gemini AI** 🇮🇩

*Transforming Data into Actionable Insights*

