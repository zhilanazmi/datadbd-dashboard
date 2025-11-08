# 📚 Tutorial Lengkap Dashboard DBD Indonesia

Panduan komprehensif untuk memaksimalkan penggunaan Dashboard DBD Indonesia.

---

## 📖 Daftar Isi

1. [Pengenalan](#pengenalan)
2. [Arsitektur Dashboard](#arsitektur-dashboard)
3. [Tutorial Step-by-Step](#tutorial-step-by-step)
4. [Contoh Use Cases](#contoh-use-cases)
5. [Advanced Features](#advanced-features)
6. [Best Practices](#best-practices)
7. [FAQ](#faq)

---

## 🎯 Pengenalan

Dashboard DBD Indonesia adalah aplikasi Business Intelligence berbasis web yang dirancang untuk:

- **Monitoring:** Memantau perkembangan kasus DBD secara real-time
- **Analisis:** Mengidentifikasi tren dan pola penyebaran
- **Prediksi:** Early warning system untuk outbreak
- **Rekomendasi:** AI-powered recommendations untuk mitigasi
- **Reporting:** Export data dan visualisasi untuk stakeholder

### Target Pengguna

1. **Dinas Kesehatan:** Monitoring dan decision making
2. **Puskesmas:** Surveillance dan reporting
3. **Researcher:** Analisis epidemiologi
4. **Policy Maker:** Perencanaan program kesehatan

---

## 🏗️ Arsitektur Dashboard

### Komponen Utama

```
Dashboard DBD Indonesia
│
├── Frontend (Streamlit)
│   ├── Overview & Summary
│   ├── Visualisasi & Analisis
│   ├── AI Insights & Rekomendasi
│   └── Export Data
│
├── Data Processing (Pandas)
│   ├── CSV Parser
│   ├── Data Validator
│   ├── Data Cleaner
│   └── Aggregator
│
├── Visualization (Plotly, Matplotlib, Seaborn)
│   ├── Bar Charts
│   ├── Line Charts
│   ├── Heatmaps
│   ├── Pie Charts
│   └── Treemaps
│
└── AI Integration (Claude Sonnet 4.0)
    ├── Trend Analysis
    ├── Regional Insights
    ├── Mitigation Recommendations
    └── Executive Reports
```

### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|----------|
| Frontend | Streamlit | Interactive web interface |
| Data Processing | Pandas, NumPy | Data manipulation |
| Visualization | Plotly, Matplotlib, Seaborn | Charts & graphs |
| AI Engine | Claude Sonnet 4.0 | Business intelligence |
| Language | Python 3.8+ | Core programming |

---

## 📝 Tutorial Step-by-Step

### Tutorial 1: First Time Setup

#### Langkah 1: Persiapan Environment

```bash
# Clone repository
git clone <repo-url>
cd dashboard-dbd

# Buat virtual environment
python -m venv venv

# Aktivasi (Windows)
venv\Scripts\activate

# Aktivasi (Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Langkah 2: Setup API Key (Optional)

```bash
# Buat file .env
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" > .env

# Atau copy dari template
cp .env.example .env
# Edit .env dan masukkan API key
```

#### Langkah 3: Jalankan Dashboard

```bash
streamlit run dashboard.py
```

Dashboard akan terbuka di `http://localhost:8501`

### Tutorial 2: Upload dan Validasi Data

#### Langkah 1: Prepare Data CSV

Buat atau siapkan file CSV dengan format:

```csv
kode_provinsi,nama_provinsi,kode_kabupaten_kota,nama_kabupaten_kota,jumlah_kasus,satuan,tahun
11,Aceh,1101,Kab. Simeulue,45,Kasus,2020
11,Aceh,1101,Kab. Simeulue,52,Kasus,2021
31,DKI Jakarta,3171,Kota Jakarta Pusat,789,Kasus,2020
```

**Validasi Checklist:**
- ✅ Semua kolom ada
- ✅ Tidak ada header duplikat
- ✅ Encoding UTF-8
- ✅ Delimiter koma (`,`)
- ✅ Nilai numerik tidak mengandung karakter non-numerik
- ✅ Tidak ada baris kosong

#### Langkah 2: Upload di Dashboard

1. Buka dashboard
2. Lihat sidebar kiri
3. Klik **"Browse files"** di section "📁 Upload Data"
4. Pilih file CSV Anda
5. Dashboard akan otomatis validasi dan load data

#### Langkah 3: Verifikasi Data

Cek di tab "Overview & Summary":
- Total records sesuai?
- Total kasus make sense?
- Provinsi dan kabupaten/kota terbaca dengan benar?

### Tutorial 3: Eksplorasi Data dengan Filter

#### Scenario: Analisis Provinsi Tertentu

**Goal:** Analisis kasus DBD di DKI Jakarta tahun 2023

**Steps:**
1. Sidebar → Filter **Tahun** → Pilih **2023**
2. Sidebar → Filter **Provinsi** → Pilih **DKI Jakarta**
3. Lihat metrics update secara real-time
4. Explore semua visualisasi di tab "Visualisasi & Analisis"

#### Scenario: Perbandingan Multi-Provinsi

**Goal:** Bandingkan DKI Jakarta, Jawa Barat, Jawa Timur

**Steps:**
1. Filter **Provinsi** → Select ketiga provinsi
2. Pilih semua tahun yang tersedia
3. Tab "Visualisasi & Analisis" → Grafik bar akan menampilkan perbandingan
4. Gunakan heatmap untuk lihat detail per kabupaten/kota

#### Scenario: Analisis Temporal

**Goal:** Lihat trend dari 2020-2023

**Steps:**
1. Filter **Tahun** → Select 2020, 2021, 2022, 2023
2. Pilih semua provinsi atau spesifik
3. Tab "Visualisasi & Analisis" → Lihat trend line nasional
4. Perhatikan pola peningkatan/penurunan

### Tutorial 4: Generate AI Insights

#### Scenario: Insight Nasional

**Steps:**
1. Pastikan API Key sudah disetup
2. Buka tab **"AI Insights & Rekomendasi"**
3. Input API Key (jika belum di `.env`)
4. **Jangan apply filter** (biarkan semua data selected)
5. Klik **"Generate AI Insights"**
6. Tunggu 10-30 detik
7. Baca hasil analisis komprehensif

**Insight yang Didapat:**
- Trend nasional
- Hotspot provinsi
- Rekomendasi mitigasi
- Area yang perlu diwaspadai

#### Scenario: Insight Regional

**Steps:**
1. Filter hanya **1 provinsi** (misal: Jawa Tengah)
2. Select semua tahun
3. Generate AI Insights
4. Claude akan fokus analisis ke provinsi tersebut

**Hasil lebih spesifik:**
- Analisis detail provinsi
- Kabupaten/kota hotspot
- Rekomendasi spesifik lokasi
- Best practices wilayah

#### Scenario: Insight Temporal

**Steps:**
1. Filter **2 tahun** spesifik (misal: 2020 vs 2023)
2. Pilih provinsi yang ingin dibandingkan
3. Generate insights
4. Claude akan analisis perubahan

**Insight perbandingan:**
- Perubahan signifikan
- Faktor yang mempengaruhi
- Lessons learned
- Proyeksi ke depan

### Tutorial 5: Export dan Reporting

#### Export Data Terfilter

**Use Case:** Share data ke team

**Steps:**
1. Apply filter sesuai kebutuhan
2. Tab **"Export Data"**
3. Klik **"Download Data Terfilter (CSV)"**
4. File akan terdownload dengan timestamp
5. Buka di Excel atau Google Sheets

#### Export Visualisasi

**Use Case:** Presentasi ke stakeholder

**Steps:**
1. Setup visualisasi di tab "Visualisasi & Analisis"
2. Tab "Export Data"
3. Klik **"Generate Trend Chart PNG"** atau **"Generate Heatmap PNG"**
4. Tunggu processing
5. Klik **"Download"** yang muncul
6. Gunakan untuk PowerPoint atau laporan

#### Export AI Insights

**Use Case:** Dokumentasi analisis

**Steps:**
1. Generate AI insights terlebih dahulu
2. Tab "Export Data"
3. Scroll ke "Export AI Insights"
4. Klik **"Download AI Insights (TXT)"**
5. Gunakan untuk laporan atau dokumentasi

---

## 🎓 Contoh Use Cases

### Use Case 1: Monthly Monitoring oleh Dinkes

**Persona:** Kepala Dinas Kesehatan Provinsi

**Workflow:**
1. Setiap bulan, upload data terbaru
2. Filter provinsi nya
3. Compare dengan bulan sebelumnya
4. Generate AI insights untuk rekomendasi
5. Export data dan visualisasi untuk laporan bulanan
6. Present ke Gubernur/Walikota

**Output:**
- Dashboard overview
- Trend chart
- Top 10 kabupaten/kota
- AI recommendations
- Executive summary

### Use Case 2: Research Analysis

**Persona:** Researcher Epidemiologi

**Workflow:**
1. Upload dataset multi-tahun
2. No filter → analisis keseluruhan
3. Explore semua visualisasi
4. Generate comprehensive AI insights
5. Export semua data untuk analisis lanjutan di Python/R
6. Gunakan heatmap untuk identifikasi cluster

**Output:**
- Clean dataset
- Visualization library
- Statistical insights
- Hypothesis untuk penelitian

### Use Case 3: Outbreak Response

**Persona:** Tim Response Kemenkes

**Workflow:**
1. Upload data real-time
2. Filter area dengan kasus meningkat
3. Identify hotspot via heatmap
4. Generate AI insights untuk affected area
5. Get specific mitigation recommendations
6. Export untuk koordinasi dengan daerah

**Output:**
- Hotspot identification
- Risk assessment
- Immediate action recommendations
- Resource allocation suggestions

### Use Case 4: Policy Planning

**Persona:** Policy Maker Kemenkes

**Workflow:**
1. Upload historical data 5 tahun
2. Analyze trend nasional
3. Compare antar provinsi
4. Generate executive report via AI
5. Identify best practices dari provinsi dengan trend menurun
6. Formulate national policy

**Output:**
- Multi-year trend analysis
- Regional comparison
- Best practices identification
- Policy recommendations

---

## 🚀 Advanced Features

### 1. Programmatic Access

Gunakan utility functions untuk analisis custom:

```python
# Import utilities
from utils_parsing import DBDDataParser
from utils_visualization import DBDVisualizer
from utils_ai_integration import ClaudeDBDAnalyzer

# Parse data
parser = DBDDataParser("my_data.csv")
df = parser.load_csv()
df_clean = parser.clean_data()

# Get statistics
stats = parser.get_summary_statistics()
print(stats)

# Create custom visualization
viz = DBDVisualizer(df_clean)
fig = viz.create_treemap()
fig.show()

# AI analysis
analyzer = ClaudeDBDAnalyzer(api_key="your-key")
insights = analyzer.generate_comprehensive_insights(df_clean)
print(insights)
```

### 2. Batch Processing

Process multiple files:

```python
import glob
from utils_parsing import quick_load_and_validate

files = glob.glob("data/*.csv")
all_data = []

for file in files:
    df, is_valid, errors = quick_load_and_validate(file)
    if is_valid:
        all_data.append(df)
        print(f"✓ {file}")
    else:
        print(f"✗ {file}: {errors}")

# Combine all data
import pandas as pd
combined_df = pd.concat(all_data, ignore_index=True)
```

### 3. Custom AI Prompts

Customize AI analysis:

```python
analyzer = ClaudeDBDAnalyzer(api_key="your-key")

# Area-specific analysis
analysis = analyzer.analyze_specific_area(
    df,
    province="Jawa Barat",
    kabkot="Kota Bandung"
)

# Time comparison
comparison = analyzer.compare_time_periods(df, 2020, 2023)

# Executive report
report = analyzer.generate_executive_report(
    df,
    target_audience="Menteri Kesehatan"
)
```

### 4. Integration dengan Systems Lain

Dashboard bisa diintegrasikan dengan:

- **Database:** MySQL, PostgreSQL
- **API:** REST API untuk real-time data
- **Cloud Storage:** AWS S3, Google Cloud Storage
- **Notification:** Email, Slack, Telegram
- **Scheduling:** Cron jobs untuk automated reports

---

## 💡 Best Practices

### Data Quality

1. **Validasi sebelum upload:** Cek format dan completeness
2. **Konsistensi naming:** Gunakan nama yang consistent untuk provinsi/kabupaten
3. **Regular update:** Upload data terbaru secara berkala
4. **Backup data:** Simpan backup sebelum modify

### Performance Optimization

1. **Filter data:** Gunakan filter untuk dataset besar
2. **Selective visualization:** Pilih provinsi spesifik untuk grafik
3. **Export hasil:** Simpan visualisasi yang sering digunakan
4. **Clear cache:** Restart dashboard jika performance menurun

### AI Usage

1. **Specific questions:** Gunakan filter untuk analisis spesifik
2. **Iterative analysis:** Generate insights multiple times dengan filter berbeda
3. **Save results:** Export dan dokumentasikan insights
4. **Validate recommendations:** Cross-check dengan domain knowledge

### Security

1. **API Key:** Jangan commit API key ke repository
2. **Sensitive data:** Jangan upload data confidential ke public
3. **Access control:** Limit access ke dashboard jika production
4. **Regular update:** Update dependencies untuk security patches

---

## ❓ FAQ

### General

**Q: Apakah dashboard ini gratis?**
A: Ya, dashboard ini open source. Namun API Claude memerlukan subscription.

**Q: Bisa digunakan offline?**
A: Bisa, kecuali fitur AI Insights yang memerlukan internet.

**Q: Support format data lain selain CSV?**
A: Saat ini hanya CSV. Untuk Excel, convert dulu ke CSV.

### Technical

**Q: Kenapa loading lama?**
A: Dataset besar atau banyak visualisasi. Gunakan filter untuk optimasi.

**Q: AI Insights error?**
A: Cek API key, internet connection, dan quota API.

**Q: Visualisasi tidak muncul?**
A: Update Plotly: `pip install plotly --upgrade`

### Data

**Q: Format tanggal bagaimana?**
A: Saat ini hanya support kolom tahun (integer).

**Q: Bisa multi-tahun dalam 1 file?**
A: Ya, sangat direkomendasikan untuk analisis trend.

**Q: Data kosong untuk beberapa kabupaten?**
A: Pastikan semua kabupaten ada di dataset atau filter sesuai kebutuhan.

---

## 📞 Support & Resources

### Dokumentasi
- **README.md:** Dokumentasi lengkap
- **QUICK_START_ID.md:** Quick start guide
- **TUTORIAL_LENGKAP.md:** Tutorial ini

### Code Examples
- **utils_parsing.py:** Contoh parsing data
- **utils_visualization.py:** Contoh visualisasi
- **utils_ai_integration.py:** Contoh AI integration

### External Resources
- [Streamlit Docs](https://docs.streamlit.io)
- [Plotly Python](https://plotly.com/python/)
- [Anthropic Claude API](https://docs.anthropic.com)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## 🎯 Kesimpulan

Dashboard DBD Indonesia adalah tool powerful untuk:
- ✅ Monitoring real-time
- ✅ Analisis mendalam
- ✅ AI-powered insights
- ✅ Professional reporting

**Next Steps:**
1. Mulai dengan quick start guide
2. Upload data pertama
3. Explore semua fitur
4. Generate AI insights
5. Share dengan team

**Happy Analyzing! 🚀**

---

*Versi: 1.0.0 | Update: November 2025*

