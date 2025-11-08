# 🚀 Quick Start Guide - Dashboard DBD Indonesia

Panduan cepat untuk memulai menggunakan Dashboard DBD Indonesia.

## 📋 Prerequisites

- **Python 3.8+** terinstall di komputer
- **pip** (Python package manager)
- **Web browser** (Chrome, Firefox, Edge, atau Safari)
- **Anthropic API Key** (opsional, untuk fitur AI insights)

## ⚡ Instalasi Cepat

### Windows

1. **Download atau clone project ini**

2. **Buka Command Prompt atau PowerShell** di folder project

3. **Double-click file `run_dashboard.bat`**
   
   ATAU jalankan di terminal:
   ```cmd
   run_dashboard.bat
   ```

4. **Dashboard akan otomatis terbuka di browser** 🎉

### Linux / macOS

1. **Download atau clone project ini**

2. **Buka Terminal** di folder project

3. **Jalankan script:**
   ```bash
   chmod +x run_dashboard.sh
   ./run_dashboard.sh
   ```

4. **Dashboard akan otomatis terbuka di browser** 🎉

## 🛠️ Instalasi Manual (Jika Script Tidak Bekerja)

### Step 1: Buat Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Setup API Key (Opsional)

Jika ingin menggunakan fitur AI Insights:

1. Dapatkan API Key dari [https://console.anthropic.com/](https://console.anthropic.com/)

2. Buat file `.env` di root folder:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
   ```

   ATAU masukkan langsung di dashboard saat menggunakan fitur AI.

### Step 4: Jalankan Dashboard

```bash
streamlit run dashboard.py
```

Dashboard akan terbuka otomatis di browser pada `http://localhost:8501`

## 📁 Menggunakan Data

### Opsi 1: Gunakan Sample Data (Default)

Dashboard sudah include file `data_dbd_sample.csv` yang akan otomatis dimuat.

### Opsi 2: Upload Data Sendiri

1. Buka dashboard
2. Klik **"Browse files"** di sidebar kiri
3. Pilih file CSV Anda
4. Dashboard akan otomatis memproses dan menampilkan data

### Format CSV yang Diperlukan

File CSV harus memiliki kolom berikut:

```
kode_provinsi,nama_provinsi,kode_kabupaten_kota,nama_kabupaten_kota,jumlah_kasus,satuan,tahun
11,Aceh,1101,Kab. Simeulue,45,Kasus,2020
31,DKI Jakarta,3171,Kota Jakarta Pusat,789,Kasus,2023
...
```

## 🎯 Fitur-Fitur Utama

### 1️⃣ Tab "Overview & Summary"
- Lihat metrics utama (total kasus, rata-rata, dll)
- Tabel summary data
- Top 10 provinsi dan kabupaten/kota
- Data detail lengkap

### 2️⃣ Tab "Visualisasi & Analisis"
- **Grafik Bar:** Trend kasus per tahun per provinsi
- **Line Chart:** Trend nasional
- **Heatmap:** Distribusi kasus per kabupaten/kota
- **Pie Chart:** Proporsi kasus per provinsi

### 3️⃣ Tab "AI Insights & Rekomendasi"
- Input API Key Claude
- Generate AI insights otomatis
- Analisis tren mendalam
- Rekomendasi mitigasi
- Prediksi dan early warning

### 4️⃣ Tab "Export Data"
- Download data terfilter (CSV)
- Download summary data (CSV)
- Download visualisasi (PNG)
- Export AI insights (TXT)

## 🔍 Filter Data

Gunakan sidebar untuk filter data:
- **Tahun:** Pilih tahun yang ingin dianalisis
- **Provinsi:** Filter berdasarkan provinsi
- **Kabupaten/Kota:** Filter berdasarkan kabupaten/kota

Filter akan update semua visualisasi secara real-time!

## 🤖 Menggunakan AI Insights

1. Buka tab **"AI Insights & Rekomendasi"**

2. **Input API Key:**
   - Dapatkan dari [Anthropic Console](https://console.anthropic.com/)
   - Paste di field "Masukkan Anthropic API Key"
   
   ATAU setup di file `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
   ```

3. **Klik "Generate AI Insights"**

4. **Tunggu beberapa detik** - Claude AI akan menganalisis data

5. **Lihat hasil:**
   - Insight tren nasional
   - Analisis regional
   - Rekomendasi mitigasi
   - Prediksi & peringatan
   - Analisis statistik otomatis

## 💡 Tips & Trik

### Performance

- **Filter data** untuk visualisasi lebih cepat
- **Pilih provinsi spesifik** untuk analisis detail
- **Export hasil** untuk sharing dengan team

### Best Practices

1. **Mulai dengan Overview** untuk pahami data keseluruhan
2. **Gunakan Filter** untuk fokus pada area tertentu
3. **Generate AI Insights** untuk mendapat rekomendasi
4. **Export hasil** untuk dokumentasi dan presentasi

### Troubleshooting

**Dashboard tidak terbuka?**
- Pastikan Python sudah terinstall: `python --version`
- Cek port 8501 tidak digunakan aplikasi lain
- Coba jalankan manual: `streamlit run dashboard.py`

**Module not found?**
- Pastikan virtual environment aktif
- Install ulang dependencies: `pip install -r requirements.txt --upgrade`

**CSV tidak terbaca?**
- Cek format CSV sesuai dengan requirement
- Pastikan encoding UTF-8
- Cek delimiter menggunakan koma (`,`)

**AI Insights error?**
- Cek API Key sudah benar
- Pastikan koneksi internet stabil
- Cek quota API di Anthropic Console

## 📚 File Utility Tambahan

Project ini include utility scripts yang bisa digunakan terpisah:

### `utils_parsing.py`
Parsing dan validasi data CSV:
```python
from utils_parsing import DBDDataParser

parser = DBDDataParser("data_dbd_sample.csv")
df = parser.load_csv()
df_clean = parser.clean_data()
stats = parser.get_summary_statistics()
```

### `utils_visualization.py`
Membuat visualisasi custom:
```python
from utils_visualization import DBDVisualizer

viz = DBDVisualizer(df)
fig = viz.create_bar_trend()
fig.show()
```

### `utils_ai_integration.py`
Integrasi Claude AI:
```python
from utils_ai_integration import ClaudeDBDAnalyzer

analyzer = ClaudeDBDAnalyzer(api_key="your-key")
insights = analyzer.generate_comprehensive_insights(df)
print(insights)
```

## 🆘 Bantuan Lebih Lanjut

- **Dokumentasi lengkap:** Baca `README.md`
- **Contoh kode:** Lihat file `utils_*.py`
- **Sample data:** Check `data_dbd_sample.csv`

## 🎓 Tutorial Video (Coming Soon)

1. Setup & Instalasi
2. Upload Data & Filter
3. Analisis Visualisasi
4. AI Insights & Rekomendasi
5. Export & Sharing

---

## ✅ Checklist Mulai Menggunakan

- [ ] Python 3.8+ terinstall
- [ ] Download/clone project
- [ ] Install dependencies
- [ ] (Opsional) Setup API Key Claude
- [ ] Jalankan dashboard
- [ ] Upload data atau gunakan sample
- [ ] Explore semua tab
- [ ] Generate AI insights
- [ ] Export hasil analisis

---

**Selamat menggunakan Dashboard DBD Indonesia!** 🇮🇩

Jika ada pertanyaan atau masalah, silakan buka issue di repository atau hubungi tim support.

**Happy Analyzing! 📊🦟**

