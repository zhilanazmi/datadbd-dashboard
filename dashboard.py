"""
Dashboard Interaktif DBD Indonesia
Menggunakan Streamlit dan Google Gemini AI untuk Business Intelligence
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai
import os
from dotenv import load_dotenv
import io
import base64

# Load environment variables
load_dotenv()

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard DBD Indonesia",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clean dan Rapi
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main Container */
    .main {
        background: #f5f7fa;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header */
    .main-header {
        font-size: 2.5rem;
        color: #1e293b;
        text-align: center;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Metric Cards */
    .stMetric {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    .stMetric label {
        color: #64748b !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #1e293b !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
    }
    
    /* Tabs */
    .stTabs {
        margin-top: 1rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8fafc;
        border-radius: 10px;
        padding: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        font-size: 0.9375rem;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e2e8f0;
    }
    
    .stTabs [aria-selected="true"] {
        background: #667eea !important;
        color: white !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: #667eea;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.625rem 1.5rem;
        font-weight: 600;
        font-size: 0.9375rem;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #5568d3;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Info Boxes */
    .stInfo {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stSuccess {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stWarning {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stError {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #1e293b !important;
    }
    
    /* Semua teks di sidebar harus putih dan readable */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span:not([class*="baseweb"]):not([class*="st"]),
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] strong,
    [data-testid="stSidebar"] small {
        color: white !important;
    }
    
    /* Markdown content di sidebar */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] div,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h4 {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stFileUploader label,
    [data-testid="stSidebar"] .stMetric label {
        color: white !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        font-size: 0.875rem !important;
        padding: 0.5rem 0.75rem !important;
        border-radius: 6px !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.15) !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background: rgba(59, 130, 246, 0.3) !important;
        border: 1px solid rgba(59, 130, 246, 0.5) !important;
        color: white !important;
        border-radius: 6px !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div:hover,
    [data-testid="stSidebar"] .stMultiSelect > div > div:hover {
        background: rgba(59, 130, 246, 0.4) !important;
        border-color: rgba(59, 130, 246, 0.6) !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div:focus,
    [data-testid="stSidebar"] .stMultiSelect > div > div:focus {
        background: rgba(59, 130, 246, 0.4) !important;
        border-color: rgba(59, 130, 246, 0.7) !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div > div,
    [data-testid="stSidebar"] .stMultiSelect > div > div > div {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background: rgba(59, 130, 246, 0.3) !important;
        border: 1px solid rgba(59, 130, 246, 0.5) !important;
        color: white !important;
        border-radius: 6px !important;
    }
    
    [data-testid="stSidebar"] .stTextInput > div > div > input:focus {
        background: rgba(59, 130, 246, 0.4) !important;
        border-color: rgba(59, 130, 246, 0.7) !important;
    }
    
    [data-testid="stSidebar"] .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.6) !important;
    }
    
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
        background: rgba(59, 130, 246, 0.4) !important;
        color: white !important;
        border: 1px solid rgba(59, 130, 246, 0.6) !important;
    }
    
    [data-testid="stSidebar"] .stFileUploader {
        background: rgba(255,255,255,0.05) !important;
        border: 2px dashed rgba(255,255,255,0.3) !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stSidebar"] .stFileUploader [data-testid="stMarkdownContainer"] {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stInfo,
    [data-testid="stSidebar"] .stSuccess,
    [data-testid="stSidebar"] .stWarning,
    [data-testid="stSidebar"] .stError {
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stInfo *,
    [data-testid="stSidebar"] .stSuccess *,
    [data-testid="stSidebar"] .stWarning *,
    [data-testid="stSidebar"] .stError * {
        color: white !important;
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar {
        width: 6px;
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.2);
        border-radius: 3px;
    }
    
    /* Search Highlight */
    .highlight {
        background: linear-gradient(135deg, #fff9c4 0%, #fff59d 100%);
        padding: 0.1rem 0.3rem;
        border-radius: 4px;
        font-weight: 600;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s ease;
        border-top: 4px solid #667eea;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Action Buttons Group */
    .button-group {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin: 1rem 0;
    }
    
    /* Filter Tags */
    .filter-tag {
        display: inline-block;
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.25rem;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Responsive Design Enhanced */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .subtitle {
            font-size: 1rem;
        }
        
        .stats-grid {
            grid-template-columns: 1fr;
        }
        
        .button-group {
            flex-direction: column;
        }
        
        .button-group button {
            width: 100%;
        }
    }
    
    /* Print Styles */
    @media print {
        .stSidebar,
        .stButton,
        .stDownloadButton {
            display: none !important;
        }
    }
    
    /* Dark Mode Support (Future) */
    @media (prefers-color-scheme: dark) {
        /* Can be implemented later */
    }
    </style>
""", unsafe_allow_html=True)

# Fungsi untuk load data
@st.cache_data
def load_data(file_path):
    """Load data dari file CSV"""
    try:
        df = pd.read_csv(file_path)
        # Validasi kolom yang diperlukan
        required_columns = ['kode_provinsi', 'nama_provinsi', 'kode_kabupaten_kota', 
                          'nama_kabupaten_kota', 'jumlah_kasus', 'satuan', 'tahun']
        
        if not all(col in df.columns for col in required_columns):
            st.error(f"File CSV harus memiliki kolom: {', '.join(required_columns)}")
            return None
        
        # Konversi tipe data
        df['jumlah_kasus'] = pd.to_numeric(df['jumlah_kasus'], errors='coerce')
        df['tahun'] = pd.to_numeric(df['tahun'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error saat membaca file: {str(e)}")
        return None

# Fungsi untuk analisis data
def analyze_data(df):
    """Analisis statistik dasar dari data"""
    analysis = {
        'total_kasus': df['jumlah_kasus'].sum(),
        'rata_rata_kasus': df['jumlah_kasus'].mean(),
        'provinsi_count': df['nama_provinsi'].nunique(),
        'kabkot_count': df['nama_kabupaten_kota'].nunique(),
        'tahun_range': (df['tahun'].min(), df['tahun'].max())
    }
    return analysis

# Fungsi untuk mendapatkan insight dari Gemini AI dengan 4 Analytics
def get_ai_insights(df, api_key):
    """Generate AI insights menggunakan Google Gemini dengan 4 jenis analytics"""
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Analisis data yang lebih mendalam
        tahun_list = sorted(df['tahun'].unique())
        
        # Trend analysis
        trend_tahunan = df.groupby('tahun')['jumlah_kasus'].sum().to_dict()
        if len(tahun_list) > 1:
            kasus_awal = trend_tahunan[tahun_list[0]]
            kasus_akhir = trend_tahunan[tahun_list[-1]]
            growth_rate = ((kasus_akhir - kasus_awal) / kasus_awal * 100) if kasus_awal > 0 else 0
        else:
            growth_rate = 0
        
        # Provincial analysis
        provinsi_stats = df.groupby('nama_provinsi')['jumlah_kasus'].agg(['sum', 'mean', 'std']).round(2)
        top_5_provinsi = provinsi_stats.nlargest(5, 'sum')['sum'].to_dict()
        
        # Kabupaten/Kota analysis
        kabkot_stats = df.groupby(['nama_provinsi', 'nama_kabupaten_kota'])['jumlah_kasus'].sum()
        top_5_kabkot = kabkot_stats.nlargest(5).to_dict()
        
        # Year-over-year growth by province
        provinsi_growth = {}
        for prov in df['nama_provinsi'].unique():
            prov_data = df[df['nama_provinsi'] == prov].groupby('tahun')['jumlah_kasus'].sum()
            if len(prov_data) > 1:
                growth = ((prov_data.iloc[-1] - prov_data.iloc[0]) / prov_data.iloc[0] * 100) if prov_data.iloc[0] > 0 else 0
                provinsi_growth[prov] = round(growth, 2)
        
        # Variability analysis
        std_dev_nasional = df.groupby('tahun')['jumlah_kasus'].sum().std()
        
        # Siapkan data summary lengkap
        summary_data = {
            'total_kasus': int(df['jumlah_kasus'].sum()),
            'periode': f"{tahun_list[0]} - {tahun_list[-1]}",
            'jumlah_tahun': len(tahun_list),
            'growth_rate_nasional': round(growth_rate, 2),
            'rata_rata_kasus_per_tahun': round(df.groupby('tahun')['jumlah_kasus'].sum().mean(), 2),
            'std_dev_nasional': round(std_dev_nasional, 2),
            'trend_tahunan': trend_tahunan,
            'top_5_provinsi': top_5_provinsi,
            'top_5_kabkot': {f"{k[0]} - {k[1]}": int(v) for k, v in top_5_kabkot.items()},
            'provinsi_growth': provinsi_growth,
            'jumlah_provinsi': df['nama_provinsi'].nunique(),
            'jumlah_kabkot': df['nama_kabupaten_kota'].nunique()
        }
        
        prompt = f"""
Sebagai ahli epidemiologi dan data scientist, lakukan analisis komprehensif terhadap data DBD Indonesia berikut:

═══════════════════════════════════════════════════════════════════════════════
DATA SUMMARY
═══════════════════════════════════════════════════════════════════════════════
📊 STATISTIK DASAR:
- Total Kasus: {summary_data['total_kasus']:,} kasus
- Periode: {summary_data['periode']}
- Jumlah Provinsi: {summary_data['jumlah_provinsi']} provinsi
- Jumlah Kabupaten/Kota: {summary_data['jumlah_kabkot']} kab/kota
- Growth Rate Nasional: {summary_data['growth_rate_nasional']}%
- Rata-rata Kasus per Tahun: {summary_data['rata_rata_kasus_per_tahun']:,}
- Standar Deviasi: {summary_data['std_dev_nasional']:,.0f}

📈 TREND TAHUNAN:
{summary_data['trend_tahunan']}

🏆 TOP 5 PROVINSI (Total Kasus):
{summary_data['top_5_provinsi']}

🎯 TOP 5 KABUPATEN/KOTA:
{summary_data['top_5_kabkot']}

📊 GROWTH RATE PER PROVINSI (%):
{summary_data['provinsi_growth']}

═══════════════════════════════════════════════════════════════════════════════

Berikan analisis dalam 4 JENIS ANALYTICS berikut dalam Bahasa Indonesia:

═══════════════════════════════════════════════════════════════════════════════
## 📊 1. DESCRIPTIVE ANALYTICS - "APA YANG TERJADI?"
═══════════════════════════════════════════════════════════════════════════════

Jelaskan kondisi SAAT INI berdasarkan data:

### A. Situasi Nasional
- Bagaimana kondisi kasus DBD di Indonesia saat ini?
- Berapa total kasus dan distribusinya?
- Apa tren umum yang terlihat?

### B. Distribusi Regional
- Provinsi mana yang paling terdampak?
- Kabupaten/kota mana yang menjadi hotspot?
- Bagaimana pola geografis penyebarannya?

### C. Pola Temporal
- Bagaimana perkembangan kasus dari tahun ke tahun?
- Apakah ada peningkatan atau penurunan?
- Berapa persentase perubahannya?

### D. Key Metrics
- Berikan 5-7 poin statistik penting yang harus diketahui

═══════════════════════════════════════════════════════════════════════════════
## 🔍 2. DIAGNOSTIC ANALYTICS - "MENGAPA INI TERJADI?"
═══════════════════════════════════════════════════════════════════════════════

Analisis PENYEBAB dan FAKTOR di balik kondisi saat ini:

### A. Root Cause Analysis
- Mengapa provinsi/kabupaten tertentu memiliki kasus tinggi?
- Faktor apa yang berkontribusi terhadap peningkatan/penurunan?

### B. Faktor Risiko Potensial
- **Faktor Geografis**: Iklim, curah hujan, suhu, ketinggian
- **Faktor Demografis**: Kepadatan penduduk, urbanisasi
- **Faktor Lingkungan**: Sanitasi, pengelolaan sampah, genangan air
- **Faktor Sosial-Ekonomi**: Akses kesehatan, pendidikan, ekonomi
- **Faktor Program**: Efektivitas program fogging, 3M Plus, surveilans

### C. Correlation & Patterns
- Apakah ada korelasi antara pertumbuhan kasus dengan wilayah tertentu?
- Pola apa yang terlihat dari data historis?

### D. Gap Analysis
- Apa yang kurang dari program mitigasi saat ini?
- Mengapa beberapa wilayah berhasil menurunkan kasus sementara yang lain tidak?

═══════════════════════════════════════════════════════════════════════════════
## 🔮 3. PREDICTIVE ANALYTICS - "APA YANG AKAN TERJADI?"
═══════════════════════════════════════════════════════════════════════════════

Prediksi MASA DEPAN berdasarkan trend dan pola data:

### A. Proyeksi Trend
- Bagaimana prediksi kasus untuk tahun-tahun mendatang jika trend berlanjut?
- Wilayah mana yang berpotensi mengalami outbreak?

### B. Early Warning Indicators
- Provinsi/kabupaten mana yang perlu DIWASPADAI?
- Indikator apa yang menunjukkan risiko peningkatan?
- Kapan periode kritis yang perlu diantisipasi?

### C. Scenario Analysis
- **Best Case Scenario**: Jika intervensi berhasil
- **Worst Case Scenario**: Jika tidak ada tindakan
- **Most Likely Scenario**: Proyeksi realistis

### D. Risk Assessment
- Klasifikasi wilayah berdasarkan level risiko (High/Medium/Low)
- Area yang memerlukan perhatian URGENT
- Potensi hotspot baru yang mungkin muncul

═══════════════════════════════════════════════════════════════════════════════
## 💡 4. PRESCRIPTIVE ANALYTICS - "APA YANG HARUS DILAKUKAN?"
═══════════════════════════════════════════════════════════════════════════════

REKOMENDASI KONKRET dan ACTIONABLE berdasarkan analisis:

### A. IMMEDIATE ACTIONS (0-3 Bulan) 🚨
Tindakan SEGERA yang harus dilakukan:
1. [Action 1 dengan target wilayah spesifik]
2. [Action 2 dengan resource requirement]
3. [Action 3 dengan KPI yang jelas]
... (3-5 rekomendasi)

### B. SHORT-TERM STRATEGIES (3-12 Bulan) 📋
Program jangka pendek:
1. [Program 1 dengan timeline]
2. [Program 2 dengan budget estimation]
3. [Program 3 dengan expected impact]
... (3-5 strategi)

### C. LONG-TERM STRATEGIES (1-3 Tahun) 🎯
Strategi jangka panjang:
1. [Strategi sistemik 1]
2. [Perubahan kebijakan 2]
3. [Infrastruktur improvement 3]
... (3-5 strategi)

### D. PRIORITAS INTERVENSI PER WILAYAH
- **Prioritas Tinggi**: [List provinsi/kabkot] - Tindakan: [...]
- **Prioritas Menengah**: [List provinsi/kabkot] - Tindakan: [...]
- **Prioritas Monitoring**: [List provinsi/kabkot] - Tindakan: [...]

### E. RESOURCE ALLOCATION
- Anggaran yang diperlukan
- Alokasi tenaga kesehatan
- Distribusi logistik (obat, fogging, dll)

### F. KEY PERFORMANCE INDICATORS (KPI)
- Target penurunan kasus (%)
- Timeline pencapaian
- Metrics untuk monitoring

### G. STAKEHOLDER ACTIONS
- **Kemenkes**: [Tindakan spesifik]
- **Dinkes Provinsi**: [Tindakan spesifik]
- **Puskesmas**: [Tindakan spesifik]
- **Masyarakat**: [Tindakan spesifik]

═══════════════════════════════════════════════════════════════════════════════

PENTING: 
- Gunakan data KONKRET dari summary di atas
- Berikan ANGKA dan PERSENTASE spesifik
- Sebutkan NAMA PROVINSI/KABUPATEN spesifik
- Buat rekomendasi yang ACTIONABLE dan MEASURABLE
- Prioritaskan berdasarkan URGENCY dan IMPACT
- Gunakan Bahasa Indonesia yang JELAS dan PROFESIONAL
"""
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"Error saat menghasilkan AI insights: {str(e)}\n\nPastikan API Key Gemini sudah diset dengan benar."

# Fungsi untuk membuat grafik trend
def create_trend_chart(df, selected_provinces=None):
    """Membuat grafik trend kasus DBD per tahun"""
    if selected_provinces:
        df_filtered = df[df['nama_provinsi'].isin(selected_provinces)]
    else:
        df_filtered = df
    
    trend_data = df_filtered.groupby(['tahun', 'nama_provinsi'])['jumlah_kasus'].sum().reset_index()
    
    fig = px.bar(
        trend_data,
        x='tahun',
        y='jumlah_kasus',
        color='nama_provinsi',
        title='Trend Kasus DBD per Tahun per Provinsi',
        labels={'jumlah_kasus': 'Jumlah Kasus', 'tahun': 'Tahun', 'nama_provinsi': 'Provinsi'},
        barmode='group',
        height=500
    )
    
    fig.update_layout(
        xaxis=dict(tickmode='linear'),
        hovermode='x unified',
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
    )
    
    return fig

# Fungsi untuk membuat heatmap
def create_heatmap(df, selected_province=None):
    """Membuat heatmap kasus DBD per kabupaten/kota"""
    if selected_province:
        df_filtered = df[df['nama_provinsi'] == selected_province]
    else:
        # Ambil top 10 kabupaten/kota dengan kasus tertinggi
        top_kabkot = df.groupby('nama_kabupaten_kota')['jumlah_kasus'].sum().nlargest(15).index
        df_filtered = df[df['nama_kabupaten_kota'].isin(top_kabkot)]
    
    # Pivot data untuk heatmap
    heatmap_data = df_filtered.pivot_table(
        values='jumlah_kasus',
        index='nama_kabupaten_kota',
        columns='tahun',
        aggfunc='sum',
        fill_value=0
    )
    
    fig = px.imshow(
        heatmap_data,
        labels=dict(x="Tahun", y="Kabupaten/Kota", color="Jumlah Kasus"),
        title=f"Heatmap Kasus DBD per Kabupaten/Kota{' - ' + selected_province if selected_province else ' (Top 15)'}",
        aspect="auto",
        color_continuous_scale="Reds",
        height=600
    )
    
    fig.update_xaxes(side="bottom")
    
    return fig

# Fungsi untuk export data
def export_to_csv(df):
    """Export dataframe ke CSV"""
    return df.to_csv(index=False).encode('utf-8')

def export_figure_to_png(fig):
    """Export plotly figure ke PNG"""
    img_bytes = fig.to_image(format="png", width=1200, height=800)
    return img_bytes

# Main App
def main():
    # Header - Clean dan sederhana
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem; padding: 2rem 0;'>
        <h1 class="main-header">🦟 Dashboard DBD Indonesia</h1>
        <p class="subtitle">Business Intelligence untuk Analisis Demam Berdarah Dengue</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Header
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.2);'>
        <h2 style='color: white; margin: 0; font-size: 1.25rem; font-weight: 600;'>Kontrol Panel</h2>
        <p style='color: rgba(255,255,255,0.7); font-size: 0.875rem; margin: 0.5rem 0 0 0;'>Upload & Filter Data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload Section
    st.sidebar.markdown("### 📁 Upload Data", unsafe_allow_html=True)
    
    # File upload dengan styling
    uploaded_file = st.sidebar.file_uploader(
        "Pilih file CSV",
        type=['csv'],
        help="Format: kode_provinsi, nama_provinsi, kode_kabupaten_kota, nama_kabupaten_kota, jumlah_kasus, satuan, tahun",
        label_visibility="collapsed"
    )
    
    # Load data
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        st.sidebar.success("✅ File berhasil diupload")
    else:
        if os.path.exists('data_dbd_sample.csv'):
            df = load_data('data_dbd_sample.csv')
            st.sidebar.info("📊 Menggunakan data sample")
        else:
            st.sidebar.warning("⚠️ Upload file CSV untuk memulai")
            st.stop()
    
    if df is None or df.empty:
        st.sidebar.error("❌ Data tidak valid")
        st.stop()
    
    # Filter Section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Filter Data", unsafe_allow_html=True)
    
    # Filter Tahun
    years = sorted(df['tahun'].unique())
    st.sidebar.markdown("**📅 Tahun**")
    selected_years = st.sidebar.multiselect(
        "Pilih Tahun",
        options=years,
        default=years,
        label_visibility="collapsed"
    )
    
    if len(years) > 1:
        col_yr1, col_yr2 = st.sidebar.columns(2)
        with col_yr1:
            if st.sidebar.button("📊 Semua", use_container_width=True, key="all_years_btn"):
                selected_years = years
                st.rerun()
        with col_yr2:
            if st.sidebar.button("📈 Terbaru", use_container_width=True, key="latest_year_btn"):
                selected_years = [years[-1]]
                st.rerun()
    
    # Filter Provinsi
    provinces = sorted(df['nama_provinsi'].unique())
    st.sidebar.markdown("**🗺️ Provinsi**")
    selected_provinces = st.sidebar.multiselect(
        "Pilih Provinsi",
        options=provinces,
        default=provinces,
        label_visibility="collapsed"
    )
    
    if len(provinces) > 1:
        col_pr1, col_pr2 = st.sidebar.columns(2)
        with col_pr1:
            if st.sidebar.button("🌏 Semua", use_container_width=True, key="all_provinces_btn"):
                selected_provinces = provinces
                st.rerun()
        with col_pr2:
            top_3_prov = df.groupby('nama_provinsi')['jumlah_kasus'].sum().nlargest(3).index.tolist()
            if st.sidebar.button("🔥 Top 3", use_container_width=True, key="top_provinces_btn"):
                selected_provinces = top_3_prov
                st.rerun()
    
    # Apply filters
    df_filtered = df[
        (df['tahun'].isin(selected_years)) &
        (df['nama_provinsi'].isin(selected_provinces))
    ]
    
    # Filter Kabupaten/Kota
    if selected_provinces:
        kabkot_options = sorted(df_filtered['nama_kabupaten_kota'].unique())
        st.sidebar.markdown("**🏙️ Kabupaten/Kota**")
        selected_kabkot = st.sidebar.multiselect(
            "Pilih Kabupaten/Kota",
            options=kabkot_options,
            default=kabkot_options,
            label_visibility="collapsed"
        )
        df_filtered = df_filtered[df_filtered['nama_kabupaten_kota'].isin(selected_kabkot)]
        
        if len(kabkot_options) > 1:
            col_kb1, col_kb2 = st.sidebar.columns(2)
            with col_kb1:
                if st.sidebar.button("📍 Semua", use_container_width=True, key="all_kabkot_btn"):
                    selected_kabkot = kabkot_options
                    st.rerun()
            with col_kb2:
                top_5_kabkot = df_filtered.groupby('nama_kabupaten_kota')['jumlah_kasus'].sum().nlargest(5).index.tolist()
                if st.sidebar.button("🔥 Top 5", use_container_width=True, key="top_kabkot_btn"):
                    selected_kabkot = top_5_kabkot
                    st.rerun()
    
    # Data Summary
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Ringkasan", unsafe_allow_html=True)
    total_records = len(df_filtered)
    total_kasus = df_filtered['jumlah_kasus'].sum()
    total_provinsi = df_filtered['nama_provinsi'].nunique()
    total_kabkot = df_filtered['nama_kabupaten_kota'].nunique()
    
    st.sidebar.metric("Records", f"{total_records:,}")
    st.sidebar.metric("Total Kasus", f"{total_kasus:,}")
    st.sidebar.metric("Provinsi", total_provinsi)
    st.sidebar.metric("Kab/Kota", total_kabkot)
    
    # Main content
    if not df_filtered.empty:
        # Tab navigation
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Overview & Summary",
            "📈 Visualisasi & Analisis",
            "🤖 AI Insights & Rekomendasi",
            "💾 Export Data"
        ])
        
        # TAB 1: Overview & Summary
        with tab1:
            st.header("📊 Overview Data DBD")
            
            # Metrics
            analysis = analyze_data(df_filtered)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Kasus", f"{int(analysis['total_kasus']):,}")
            with col2:
                st.metric("Rata-rata Kasus", f"{analysis['rata_rata_kasus']:.1f}")
            with col3:
                st.metric("Jumlah Provinsi", analysis['provinsi_count'])
            with col4:
                st.metric("Jumlah Kab/Kota", analysis['kabkot_count'])
            
            st.markdown("---")
            
            # Tabel Summary
            st.subheader("📋 Tabel Summary Data")
            summary_df = df_filtered.groupby(['nama_provinsi', 'tahun']).agg({
                'jumlah_kasus': ['sum', 'mean', 'count'],
                'nama_kabupaten_kota': 'nunique'
            }).round(2)
            
            summary_df.columns = ['Total Kasus', 'Rata-rata Kasus', 'Jumlah Record', 'Jumlah Kab/Kota']
            summary_df = summary_df.reset_index()
            
            st.dataframe(summary_df, use_container_width=True, height=400)
            
            st.markdown("---")
            
            # Top 10 Wilayah
            st.subheader("🏆 Ranking Wilayah")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Top 10 Provinsi**")
                top_provinces = df_filtered.groupby('nama_provinsi')['jumlah_kasus'].sum().nlargest(10).reset_index()
                top_provinces.columns = ['Provinsi', 'Total Kasus']
                # Add ranking
                top_provinces.insert(0, 'Rank', range(1, len(top_provinces) + 1))
                st.dataframe(top_provinces, use_container_width=True, hide_index=True)
            
            with col2:
                st.write("**Top 10 Kabupaten/Kota**")
                top_kabkot = df_filtered.groupby('nama_kabupaten_kota')['jumlah_kasus'].sum().nlargest(10).reset_index()
                top_kabkot.columns = ['Kabupaten/Kota', 'Total Kasus']
                top_kabkot.insert(0, 'Rank', range(1, len(top_kabkot) + 1))
                st.dataframe(top_kabkot, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Detail data table
            st.subheader("📄 Data Detail")
            st.dataframe(
                df_filtered,
                use_container_width=True,
                height=400,
                column_config={
                    "jumlah_kasus": st.column_config.NumberColumn(
                        "Jumlah Kasus",
                        format="%d"
                    ),
                    "tahun": st.column_config.NumberColumn(
                        "Tahun",
                        format="%d"
                    )
                }
            )
        
        # TAB 2: Visualisasi & Analisis
        with tab2:
            st.header("📈 Visualisasi Data DBD")
            
            # Trend Chart
            st.subheader("📊 Trend Kasus DBD per Tahun")
            trend_provinces = st.multiselect(
                "Pilih provinsi (kosongkan untuk semua)",
                options=sorted(df_filtered['nama_provinsi'].unique()),
                default=None,
                key='trend_provinces'
            )
            trend_fig = create_trend_chart(df_filtered, trend_provinces if trend_provinces else None)
            st.plotly_chart(trend_fig, use_container_width=True)
            
            st.markdown("---")
            
            # Trend Nasional
            st.subheader("📈 Trend Nasional")
            national_trend = df_filtered.groupby('tahun')['jumlah_kasus'].sum().reset_index()
            fig_national = px.line(
                national_trend,
                x='tahun',
                y='jumlah_kasus',
                title='Trend Kasus DBD Nasional',
                labels={'jumlah_kasus': 'Total Kasus', 'tahun': 'Tahun'},
                markers=True
            )
            fig_national.update_traces(line_color='#667eea', line_width=3)
            st.plotly_chart(fig_national, use_container_width=True)
            
            st.markdown("---")
            
            # Heatmap
            st.subheader("🔥 Heatmap Kasus DBD")
            heatmap_province = st.selectbox(
                "Pilih Provinsi",
                options=['Semua (Top 15)'] + sorted(df_filtered['nama_provinsi'].unique()),
                index=0,
                key='heatmap_province'
            )
            heatmap_prov = None if heatmap_province == 'Semua (Top 15)' else heatmap_province
            heatmap_fig = create_heatmap(df_filtered, heatmap_prov)
            st.plotly_chart(heatmap_fig, use_container_width=True)
            
            # Distribusi kasus per provinsi - Pie Chart
            st.markdown("---")
            st.subheader("🥧 Distribusi Kasus per Provinsi")
            
            province_dist = df_filtered.groupby('nama_provinsi')['jumlah_kasus'].sum().reset_index()
            fig_pie = px.pie(
                province_dist,
                values='jumlah_kasus',
                names='nama_provinsi',
                title='Proporsi Kasus DBD per Provinsi'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # TAB 3: AI Insights & Rekomendasi
        with tab3:
            st.header("🤖 AI-Powered Analytics Dashboard")
            
            st.info("""
            **Powered by Google Gemini 1.5 Pro** - AI akan menganalisis data dan memberikan:
            - 📊 **Descriptive Analytics**: Kondisi saat ini
            - 🔍 **Diagnostic Analytics**: Penyebab masalah
            - 🔮 **Predictive Analytics**: Prediksi masa depan
            - 💡 **Prescriptive Analytics**: Rekomendasi actionable
            """)
            
            st.markdown("---")
            
            # Input API Key
            api_key = st.text_input(
                "🔑 Google Gemini API Key",
                type="password",
                help="Dapatkan API key dari https://aistudio.google.com/app/apikey",
                value=os.getenv('GEMINI_API_KEY', '')
            )
            
            # Data Summary
            st.subheader("📊 Data yang Akan Dianalisis")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Records", f"{len(df_filtered):,}")
            with col2:
                st.metric("Provinsi", df_filtered['nama_provinsi'].nunique())
            with col3:
                st.metric("Kab/Kota", df_filtered['nama_kabupaten_kota'].nunique())
            with col4:
                st.metric("Periode", f"{df_filtered['tahun'].min()}-{df_filtered['tahun'].max()}")
            with col5:
                st.metric("Total Kasus", f"{df_filtered['jumlah_kasus'].sum():,.0f}")
            
            st.markdown("---")
            
            # Generate Button
            generate_btn = st.button(
                "🚀 Generate 4 Analytics Insights", 
                type="primary", 
                use_container_width=True
            )
            
            # Reset Button
            if st.button("🔄 Reset", use_container_width=True):
                if 'ai_insights' in st.session_state:
                    del st.session_state['ai_insights']
                st.success("✅ Insights berhasil di-reset!")
                st.rerun()
            
            if generate_btn:
                if not api_key:
                    st.error("""
                    ❌ **API Key Belum Diisi!**
                    
                    Silakan masukkan Google Gemini API Key terlebih dahulu.
                    
                    **Cara mendapatkan API Key:**
                    1. Kunjungi: https://aistudio.google.com/app/apikey
                    2. Login dengan Google account
                    3. Klik "Create API Key"
                    4. Copy dan paste di field di atas
                    """)
                else:
                    # Progress indicator
                    progress_placeholder = st.empty()
                    progress_placeholder.markdown("""
                    <div style='text-align: center; padding: 2rem;'>
                        <div class="loading-spinner" style='margin: 0 auto 1rem;'></div>
                        <p style='color: #667eea; font-weight: 600; font-size: 1.1rem;'>
                            🧠 Gemini AI sedang menganalisis data Anda...
                        </p>
                        <p style='color: #666; font-size: 0.9rem; margin-top: 0.5rem;'>
                            Ini mungkin memakan waktu 30-60 detik
                        </p>
                        <div class="progress-indicator">
                            <div class="progress-dot active"></div>
                            <div class="progress-dot"></div>
                            <div class="progress-dot"></div>
                            <div class="progress-dot"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    try:
                        insights = get_ai_insights(df_filtered, api_key)
                        
                        progress_placeholder.empty()
                        
                        # Success message dengan animasi
                        st.markdown("""
                        <div style='background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); 
                                    padding: 1.5rem; border-radius: 15px; 
                                    border-left: 5px solid #4CAF50; 
                                    margin-bottom: 2rem; 
                                    box-shadow: 0 5px 15px rgba(76, 175, 80, 0.2);'>
                            <div style='display: flex; align-items: center; gap: 1rem;'>
                                <div class="success-check">✓</div>
                                <div>
                                    <h4 style='margin: 0; color: #2e7d32;'>✅ Analisis Selesai!</h4>
                                    <p style='margin: 0.5rem 0 0 0; color: #388e3c;'>
                                        Scroll ke bawah untuk melihat hasil lengkap 4 Analytics
                                    </p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                        st.markdown("## 🎯 AI-Generated Analytics Insights")
                        st.markdown("""
                        <div style='background: rgba(102, 126, 234, 0.05); padding: 1rem; border-radius: 10px; margin-bottom: 1.5rem;'>
                            <p style='margin: 0; color: #666; font-size: 0.9rem;'>
                                💡 <strong>Tips:</strong> Baca semua 4 jenis analytics secara berurutan untuk pemahaman lengkap. 
                                Focus pada <strong>Prescriptive Analytics</strong> untuk action plan yang bisa langsung diimplementasikan.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(insights)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Save insights to session state
                        st.session_state['ai_insights'] = insights
                        
                        # Auto scroll to results
                        st.markdown("""
                        <script>
                            setTimeout(function() {
                                window.scrollTo({ top: document.querySelector('.insight-box').offsetTop - 100, behavior: 'smooth' });
                            }, 500);
                        </script>
                        """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        progress_placeholder.empty()
                        st.error(f"""
                        ❌ **Error saat generate insights:**
                        
                        {str(e)}
                        
                        **Troubleshooting:**
                        1. Pastikan API Key valid dan aktif
                        2. Cek koneksi internet
                        3. Cek quota API di Google AI Studio
                        4. Coba lagi dalam beberapa saat
                        """)
            
            # Display saved insights if available
            if 'ai_insights' in st.session_state:
                st.markdown("---")
                st.markdown("### 📌 Analytics Results (Tersimpan)")
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown(st.session_state['ai_insights'])
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Manual insights based on data
            st.markdown("---")
            st.markdown("### 📊 Analisis Statistik Otomatis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**📈 Trend Tahunan**")
                yearly_trend = df_filtered.groupby('tahun')['jumlah_kasus'].sum()
                if len(yearly_trend) > 1:
                    pct_change = ((yearly_trend.iloc[-1] - yearly_trend.iloc[0]) / yearly_trend.iloc[0] * 100)
                    trend_direction = "meningkat" if pct_change > 0 else "menurun"
                    st.write(f"- Kasus DBD {trend_direction} sebesar **{abs(pct_change):.1f}%** dari tahun {yearly_trend.index[0]} ke {yearly_trend.index[-1]}")
                    st.write(f"- Total kasus tahun {yearly_trend.index[-1]}: **{yearly_trend.iloc[-1]:,.0f} kasus**")
            
            with col2:
                st.write("**🎯 Area Prioritas**")
                top_3_provinces = df_filtered.groupby('nama_provinsi')['jumlah_kasus'].sum().nlargest(3)
                st.write("**Top 3 Provinsi yang Memerlukan Perhatian:**")
                for i, (prov, kasus) in enumerate(top_3_provinces.items(), 1):
                    st.write(f"{i}. {prov}: **{kasus:,.0f} kasus**")
            
            st.markdown("---")
            
            # Rekomendasi umum
            st.write("**💊 Rekomendasi Mitigasi Umum**")
            st.markdown("""
            1. **Fokus Intervensi**: Prioritaskan wilayah dengan kasus tertinggi untuk program fogging dan 3M Plus
            2. **Surveilans Ketat**: Tingkatkan monitoring di area dengan tren peningkatan signifikan
            3. **Edukasi Masyarakat**: Kampanye pencegahan DBD terutama menjelang musim hujan
            4. **Koordinasi Lintas Sektor**: Libatkan puskesmas, kelurahan, dan masyarakat
            5. **Early Warning System**: Implementasi sistem deteksi dini berbasis data
            """)
        
        # TAB 4: Export Data
        with tab4:
            st.header("💾 Export Data & Visualisasi")
            st.markdown("Download data dan visualisasi dalam berbagai format")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Export Data")
                
                # Export filtered data
                csv_data = export_to_csv(df_filtered)
                st.download_button(
                    label="⬇️ Download Data Terfilter (CSV)",
                    data=csv_data,
                    file_name=f"data_dbd_filtered_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # Export summary data
                summary_csv = export_to_csv(summary_df)
                st.download_button(
                    label="⬇️ Download Summary Data (CSV)",
                    data=summary_csv,
                    file_name=f"summary_dbd_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # Export top provinces
                top_prov_csv = export_to_csv(top_provinces)
                st.download_button(
                    label="⬇️ Download Top Provinsi (CSV)",
                    data=top_prov_csv,
                    file_name=f"top_provinsi_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                st.subheader("📈 Export Visualisasi")
                
                st.info("💡 Klik tombol di bawah untuk generate dan download grafik dalam format PNG")
                
                if st.button("📊 Generate Trend Chart PNG", use_container_width=True):
                    with st.spinner("Generating..."):
                        try:
                            trend_fig = create_trend_chart(df_filtered)
                            img_bytes = export_figure_to_png(trend_fig)
                            st.download_button(
                                label="⬇️ Download Trend Chart",
                                data=img_bytes,
                                file_name=f"trend_chart_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.png",
                                mime="image/png",
                                use_container_width=True
                            )
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                
                if st.button("🔥 Generate Heatmap PNG", use_container_width=True):
                    with st.spinner("Generating..."):
                        try:
                            heatmap_fig = create_heatmap(df_filtered)
                            img_bytes = export_figure_to_png(heatmap_fig)
                            st.download_button(
                                label="⬇️ Download Heatmap",
                                data=img_bytes,
                                file_name=f"heatmap_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.png",
                                mime="image/png",
                                use_container_width=True
                            )
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            
            # Export insights
            if 'ai_insights' in st.session_state:
                st.markdown("---")
                st.subheader("🤖 Export AI Insights")
                
                insights_text = st.session_state['ai_insights']
                st.download_button(
                    label="⬇️ Download AI Insights (TXT)",
                    data=insights_text,
                    file_name=f"ai_insights_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    else:
        # Empty state dengan design yang menarik
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📭</div>
            <h2 style='color: #333; margin-bottom: 1rem;'>Tidak Ada Data</h2>
            <p style='color: #666; font-size: 1.1rem; margin-bottom: 2rem;'>
                Tidak ada data yang sesuai dengan filter yang dipilih
            </p>
            <div style='display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;'>
                <div style='background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); max-width: 300px;'>
                    <h4 style='margin-top: 0; color: #667eea;'>💡 Saran:</h4>
                    <ul style='text-align: left; color: #666;'>
                        <li>Pilih tahun yang berbeda</li>
                        <li>Pilih provinsi lain</li>
                        <li>Hapus beberapa filter</li>
                        <li>Upload data baru</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0; color: #64748b;'>
        <p>Powered by <strong>Streamlit</strong> & <strong>Google Gemini AI</strong></p>
        <p style='font-size: 0.875rem; margin-top: 0.5rem;'>© 2025 Dashboard DBD Indonesia</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

