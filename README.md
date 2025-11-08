# 🦟 Dashboard DBD Indonesia - Business Intelligence

Dashboard interaktif berbasis web untuk analisis dan monitoring kasus Demam Berdarah Dengue (DBD) di Indonesia menggunakan Python Streamlit dan AI Claude Sonnet 4.0.

## 🌟 Fitur Utama

### 📊 Visualisasi Data Interaktif
- **Tabel Summary**: Ringkasan data per provinsi dan tahun
- **Grafik Bar Trend**: Visualisasi trend kasus DBD per tahun untuk setiap provinsi
- **Heatmap**: Peta panas distribusi kasus per kabupaten/kota
- **Pie Chart**: Distribusi proporsi kasus per provinsi
- **Line Chart**: Trend nasional kasus DBD

### 🔍 Filter Data Dinamis
- Filter berdasarkan **Tahun**
- Filter berdasarkan **Provinsi**
- Filter berdasarkan **Kabupaten/Kota**
- Multi-select dengan update real-time

### 🤖 Business Intelligence dengan AI
- **AI-Generated Insights**: Analisis mendalam menggunakan Claude Sonnet 4.0
- **Trend Analysis**: Analisis tren nasional dan per provinsi
- **Hotspot Detection**: Identifikasi area dengan kasus tertinggi
- **Rekomendasi Mitigasi**: Saran tindakan berdasarkan data
- **Prediksi & Peringatan**: Early warning system

### 💾 Export & Download
- Export data terfilter ke **CSV**
- Export summary data ke **CSV**
- Export visualisasi ke **PNG**
- Export AI insights ke **TXT**

### 📁 Upload Data Custom
- Upload file CSV dengan format standar
- Validasi otomatis struktur data
- Support multiple file formats

## 🚀 Instalasi & Setup

### Prerequisites
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Langkah Instalasi

1. **Clone atau download repository ini**
```bash
git clone <repository-url>
cd dashboard-dbd
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup API Key Claude (Opsional - untuk fitur AI Insights)**

   a. Dapatkan API Key dari [Anthropic Console](https://console.anthropic.com/)
   
   b. Buat file `.env` di root directory:
   ```bash
   cp .env.example .env
   ```
   
   c. Edit file `.env` dan masukkan API key Anda:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
   ```

4. **Jalankan aplikasi**
```bash
streamlit run dashboard.py
```

5. **Akses dashboard**
   
   Browser akan otomatis membuka aplikasi di `http://localhost:8501`

## 📋 Format Data CSV

Dashboard ini menggunakan format CSV dengan kolom berikut:

| Kolom | Deskripsi | Tipe Data | Contoh |
|-------|-----------|-----------|--------|
| `kode_provinsi` | Kode unik provinsi | Integer | 11 |
| `nama_provinsi` | Nama provinsi | String | Aceh |
| `kode_kabupaten_kota` | Kode unik kabupaten/kota | Integer | 1101 |
| `nama_kabupaten_kota` | Nama kabupaten/kota | String | Kab. Simeulue |
| `jumlah_kasus` | Jumlah kasus DBD | Integer | 45 |
| `satuan` | Satuan pengukuran | String | Kasus |
| `tahun` | Tahun data | Integer | 2023 |

### Contoh Data CSV

```csv
kode_provinsi,nama_provinsi,kode_kabupaten_kota,nama_kabupaten_kota,jumlah_kasus,satuan,tahun
11,Aceh,1101,Kab. Simeulue,45,Kasus,2020
11,Aceh,1171,Kota Banda Aceh,234,Kasus,2020
31,DKI Jakarta,3171,Kota Jakarta Pusat,789,Kasus,2020
```

File sample data tersedia di `data_dbd_sample.csv`

## 🎯 Cara Penggunaan

### 1. Upload Data
- Klik tombol "Browse files" di sidebar
- Pilih file CSV dengan format yang sesuai
- Atau gunakan data sample yang sudah disediakan

### 2. Filter Data
- Gunakan filter di sidebar untuk menyaring data:
  - **Tahun**: Pilih tahun yang ingin dianalisis
  - **Provinsi**: Pilih provinsi tertentu
  - **Kabupaten/Kota**: Pilih kabupaten/kota spesifik

### 3. Eksplorasi Dashboard

#### Tab "Overview & Summary"
- Lihat metrics utama (Total Kasus, Rata-rata, dll)
- Cek tabel summary per provinsi dan tahun
- Identifikasi Top 10 Provinsi dan Kabupaten/Kota
- Explore detail data lengkap

#### Tab "Visualisasi & Analisis"
- Analisis trend kasus per tahun dengan grafik bar
- Pilih provinsi spesifik untuk perbandingan
- Lihat trend nasional dengan line chart
- Explore heatmap distribusi kasus
- Analisis proporsi kasus per provinsi

#### Tab "AI Insights & Rekomendasi"
- Masukkan Anthropic API Key
- Klik "Generate AI Insights"
- Dapatkan analisis mendalam dari Claude AI:
  - Insight tren nasional
  - Insight regional
  - Rekomendasi mitigasi konkret
  - Prediksi dan peringatan
- Lihat analisis statistik otomatis

#### Tab "Export Data"
- Download data terfilter dalam format CSV
- Download summary data
- Download top provinsi/kabupaten
- Generate dan download visualisasi (PNG)
- Export AI insights (TXT)

## 🛠️ Teknologi yang Digunakan

### Core Framework
- **Streamlit 1.28.0**: Web framework untuk dashboard interaktif
- **Python 3.8+**: Bahasa pemrograman utama

### Data Processing
- **Pandas 2.1.0**: Manipulasi dan analisis data
- **NumPy 1.24.3**: Komputasi numerik

### Visualisasi
- **Plotly 5.17.0**: Visualisasi interaktif (chart, heatmap)
- **Matplotlib 3.8.0**: Visualisasi plotting
- **Seaborn 0.13.0**: Visualisasi statistik

### AI & Machine Learning
- **Anthropic SDK 0.7.0**: Integrasi dengan Claude AI (Sonnet 4.0)
- **Claude Sonnet 4.0**: Model AI untuk analisis dan rekomendasi

### Utilities
- **python-dotenv 1.0.0**: Manajemen environment variables
- **openpyxl 3.1.2**: Export data ke Excel (opsional)

## 📊 Contoh Analisis & Insight

### Analisis yang Dapat Dilakukan:

1. **Trend Analysis**
   - Identifikasi peningkatan/penurunan kasus per tahun
   - Deteksi pola musiman
   - Perbandingan antar provinsi

2. **Hotspot Identification**
   - Area dengan kasus tertinggi
   - Wilayah yang memerlukan intervensi prioritas
   - Peta penyebaran geografis

3. **Predictive Insights** (via AI)
   - Prediksi tren ke depan
   - Area berisiko tinggi
   - Faktor risiko potensial

4. **Rekomendasi Mitigasi**
   - Program fogging prioritas
   - Kampanye edukasi targeted
   - Alokasi resource kesehatan

## 🤖 Integrasi Claude AI

Dashboard ini menggunakan **Claude Sonnet 4.0** untuk menghasilkan insight mendalam:

### Capabilities:
- Analisis tren kompleks
- Identifikasi pola tersembunyi
- Rekomendasi berbasis data
- Kontekstualisasi dengan situasi kesehatan Indonesia

### Contoh Prompt yang Digunakan:
```python
prompt = f"""
Analisis data DBD Indonesia berikut dan berikan insight mendalam:

Data Summary:
- Total Kasus: {total_kasus} kasus
- Periode: {tahun_data}
- Top 5 Provinsi: {provinsi_tertinggi}
- Trend Tahunan: {trend_tahunan}

Berikan analisis dalam format:
1. INSIGHT TREN NASIONAL
2. INSIGHT REGIONAL
3. REKOMENDASI MITIGASI
4. PREDIKSI & PERINGATAN
"""
```

### Setup API Key:
1. Daftar di [Anthropic Console](https://console.anthropic.com/)
2. Buat API key baru
3. Tambahkan ke file `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
   ```
4. Atau input langsung di dashboard

## 📁 Struktur Project

```
dashboard-dbd/
├── dashboard.py              # Aplikasi Streamlit utama
├── requirements.txt          # Dependencies Python
├── data_dbd_sample.csv      # Contoh data DBD
├── .env.example             # Template environment variables
├── .env                     # Environment variables (create this)
└── README.md                # Dokumentasi (file ini)
```

## 🔒 Keamanan & Privacy

- API Key disimpan di environment variables (`.env`)
- File `.env` tidak di-commit ke repository
- Data CSV hanya diproses lokal di memory
- Tidak ada data yang dikirim ke server eksternal (kecuali Claude API untuk insights)

## 🐛 Troubleshooting

### Error: "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### Error: "API Key invalid"
- Pastikan API key Claude sudah benar
- Cek di [Anthropic Console](https://console.anthropic.com/)
- Pastikan sudah setup `.env` file dengan benar

### Error: "CSV format tidak valid"
- Pastikan CSV memiliki semua kolom yang diperlukan
- Cek delimiter (harus menggunakan koma)
- Pastikan encoding UTF-8

### Visualisasi tidak muncul
```bash
pip install plotly --upgrade
pip install kaleido  # Untuk export PNG
```

## 📈 Pengembangan Lanjutan

Fitur yang dapat ditambahkan:

- [ ] Integrasi dengan database real-time
- [ ] Forecasting dengan ML models
- [ ] Notifikasi email untuk alerts
- [ ] Dashboard mobile responsive
- [ ] Multi-language support
- [ ] Export to PDF reports
- [ ] Real-time data streaming
- [ ] Geospatial mapping dengan folium
- [ ] Integrasi dengan API Kemenkes

## 🤝 Kontribusi

Kontribusi sangat welcome! Silakan:
1. Fork repository
2. Buat branch fitur baru
3. Commit perubahan
4. Push ke branch
5. Buat Pull Request

## 📝 Lisensi

Project ini dibuat untuk tujuan edukasi dan analisis kesehatan masyarakat.

## 📧 Kontak & Support

Jika ada pertanyaan atau butuh bantuan:
- Buka issue di repository
- Email: [email-anda]
- Dokumentasi: [link-docs]

## 🙏 Acknowledgments

- Data DBD: Kementerian Kesehatan RI
- AI Model: Anthropic Claude Sonnet 4.0
- Framework: Streamlit Community
- Visualisasi: Plotly Team

---

**Dashboard DBD Indonesia** - Membantu menganalisis dan memitigasi penyebaran Demam Berdarah Dengue di Indonesia 🇮🇩

Dibuat dengan ❤️ menggunakan Python & Streamlit

