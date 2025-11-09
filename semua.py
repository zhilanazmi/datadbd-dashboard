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
from datetime import datetime

# --- Konfigurasi Halaman (Diambil dari Dashboard) ---
st.set_page_config(
    # --- MODIFIKASI ---: Judul diubah
    page_title="Dashboard DBD Jawa Barat",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Path File Global ---
DATA_FILE_PATH = "data_dbd.csv"
LOG_FILE_PATH = "admin_log.csv"

# --- Definisi Pengguna (Gabungan) ---
KODE_KABUPATEN_KOTA = [
    "3201", "3202", "3203", "3204", "3205", "3206", "3207", "3208", 
    "3209", "3210", "3211", "3212", "3213", "3214", "3215", "3216", 
    "3217", "3271", "3272", "3273", "3274", "3275", "3276", "3277", 
    "3278", "3279"
]

ADMIN_USERS = {
    "masteradmin": {
        "password": "admin123",
        "role": "master",
        "region_code": None
    }
}
for code in KODE_KABUPATEN_KOTA:
    username = f"admin{code}"
    ADMIN_USERS[username] = {
        "password": "admin123",
        "role": "daerah",
        "region_code": code
    }


# --- CUSTOM CSS (Global untuk kedua halaman) ---
st.markdown("""
    <style>
    /* ... Semua CSS Anda sebelumnya ... */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main Container */
    .main {
        background: #f5f7fa; /* Aturan dasar Anda */
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header */
    .main-header {
        font-size: 2.5rem;
        color: #1e293b; /* Aturan dasar Anda */
        text-align: center;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        text-align: center;
        color: #64748b; /* Aturan dasar Anda */
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
        color: #4b5563; /* <-- PERBAIKAN: Menambahkan warna default */
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
    
    /* Tombol sekunder (misal Hapus di Admin) */
    .stButton > button:not([kind="primary"]) {
        background: white;
        color: #4b5563;
        border: 1px solid #d1d5db;
    }
    
    .stButton > button:not([kind="primary"]):hover {
        background: #f9fafb;
        border-color: #b0b8c1;
        box-shadow: none;
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
    
    /* Dataframe & Data Editor */
    .stDataFrame, .stDataEditor {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #1e293b !important;
    }
    
    /* ... semua aturan sidebar Anda lainnya (tetap sama) ... */
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
    [data-testid="stSidebar"] .stFileUploader label {
        color: white !important;
        font-weight: 500;
    }
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        font-size: 0.875rem !important;
        padding: 0.5rem 0.75rem !important;
        border-radius: 6px !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        padding: 0.625rem 1.5rem !important;
        font-size: 0.9375rem !important;
        font-weight: 600 !important;
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
    
    /* --- AWAL PERBAIKAN: PAKSA LIGHT MODE --- */
    /* Ini adalah aturan baru yang "melawan" [data-theme="dark"] milik Streamlit */

    [data-theme="dark"] .main {
        background: #f5f7fa !important;
    }
    
    [data-theme="dark"] .main-header {
        color: #1e293b !important;
    }
    
    [data-theme="dark"] .subtitle {
        color: #64748b !important;
    }
    
    /* Paksa semua teks markdown di area .main */
    [data-theme="dark"] .main [data-testid="stMarkdownContainer"] p,
    [data-theme="dark"] .main [data-testid="stMarkdownContainer"] li,
    [data-theme="dark"] .main [data-testid="stMarkdownContainer"] h1,
    [data-theme="dark"] .main [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] {
        color: #1e293b !important;
    }

    /* Paksa teks di dalam tabel (DataFrame) */
    [data-theme="dark"] .stDataFrame {
        color: #1e293b !important;
    }
    [data-theme="dark"] .stDataFrame [data-testid="stDataGridColHeader"] div {
        color: #1e293b !important;
    }
    [data-theme="dark"] .stDataFrame [data-testid="stDataGridCell"] {
         color: #1e293b !important;
    }

    /* Paksa warna latar belakang dan teks di data editor */
    [data-theme="dark"] .stDataEditor {
        background: #ffffff !important;
        color: #1e293b !important;
    }
    [data-theme="dark"] .stDataEditor [data-testid="stDataGridCell"] {
         color: #1e293b !important;
    }
    [data-theme="dark"] .stDataEditor [data-testid="stDataGridColHeader"] div {
        color: #1e293b !important;
    }
    
    /* --- TAMBAHAN PERBAIKAN UNTUK TABS --- */
    [data-theme="dark"] .stTabs [data-baseweb="tab-list"] {
        background: #f8fafc !important;
    }
    [data-theme="dark"] .stTabs [data-baseweb="tab"]:not([aria-selected="true"]) {
        color: #4b5563 !important; 
    }
    [data-theme="dark"] .stTabs [data-baseweb="tab"]:not([aria-selected="true"]):hover {
        background: #e2e8f0 !important;
        color: #1e293b !important;
    }
    /* --- AKHIR PERBAIKAN --- */
    
    </style>
""", unsafe_allow_html=True)


# --- FUNGSI HELPER (Log & Auth) ---

def init_log_file(filepath):
    """Membuat file log jika belum ada."""
    if not os.path.exists(filepath):
        try:
            log_df = pd.DataFrame(columns=["timestamp", "username", "action", "details"])
            log_df.to_csv(filepath, index=False)
        except Exception as e:
            st.error(f"Gagal membuat file log: {e}")

def write_log(username, action, details):
    """Menulis satu baris log ke file CSV."""
    try:
        new_log_entry = pd.DataFrame({
            "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "username": [username],
            "action": [action],
            "details": [details]
        })
        new_log_entry.to_csv(LOG_FILE_PATH, mode='a', header=False, index=False)
    except Exception as e:
        print(f"Error writing log: {e}")

@st.cache_data
def load_logs(filepath):
    """Memuat semua log dari file CSV."""
    if not os.path.exists(filepath):
        return pd.DataFrame(columns=["timestamp", "username", "action", "details"])
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        st.error(f"Gagal memuat log: {e}")
        return pd.DataFrame(columns=["timestamp", "username", "action", "details"])

def check_login(username, password):
    """Memeriksa kredensial pengguna dan mencatat log jika berhasil."""
    user = ADMIN_USERS.get(username)
    if user and user["password"] == password:
        init_log_file(LOG_FILE_PATH)
        # Semua login yang berhasil melalui fungsi ini adalah Admin
        write_log(username, "LOGIN", f"Admin '{username}' berhasil login.")
        return True, user["role"], user["region_code"]
    return False, None, None

def perform_logout():
    """Membersihkan session state untuk logout."""
    write_log(st.session_state.username, "LOGOUT", f"Pengguna '{st.session_state.username}' logout.")
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.region_code = None
    st.cache_data.clear()
    st.rerun()


# --- FUNGSI HELPER (Data & CRUD) ---

@st.cache_data
def load_data(file_path):
    """
    Load data dari file CSV (dari skrip dashboard, lebih robust).
    Fungsi ini sekarang digunakan oleh Admin dan Dashboard.
    """
    if not os.path.exists(file_path):
        st.error(f"File data {file_path} tidak ditemukan!")
        st.info("Pastikan Anda sudah membuat file `data_dbd.csv` di folder yang sama.")
        # Kembalikan DataFrame kosong dengan kolom yang diharapkan
        return pd.DataFrame(columns=[
            'id', 'kode_provinsi', 'nama_provinsi', 'kode_kabupaten_kota', 
            'nama_kabupaten_kota', 'jumlah_kasus', 'satuan', 'tahun'
        ])
        
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
        if 'kode_kabupaten_kota' in df.columns:
            df['kode_kabupaten_kota'] = df['kode_kabupaten_kota'].astype(str)
        
        return df
    except Exception as e:
        st.error(f"Error saat membaca file data: {str(e)}")
        return None

def save_data(df, filepath):
    """Menyimpan DataFrame kembali ke CSV (dari skrip admin)."""
    try:
        if "pilih_hapus" in df.columns:
            df_to_save = df.drop(columns=["pilih_hapus"])
        else:
            df_to_save = df
            
        df_to_save.to_csv(filepath, index=False)
        return True
    except Exception as e:
        st.error(f"Gagal menyimpan data: {e}")
        return False


# --- FUNGSI HELPER (Dashboard Visuals & AI) ---
# ... (Semua fungsi helper dashboard: analyze_data, get_ai_insights, create_trend_chart, dll. tetap sama) ...
def analyze_data(df):
    """Analisis statistik dasar dari data (dari skrip dashboard)."""
    analysis = {
        'total_kasus': df['jumlah_kasus'].sum(),
        'rata_rata_kasus': df['jumlah_kasus'].mean(),
        'provinsi_count': df['nama_provinsi'].nunique(), # Ini akan jadi 1
        'kabkot_count': df['nama_kabupaten_kota'].nunique(), # Ini yang utama
        'tahun_range': (df['tahun'].min(), df['tahun'].max())
    }
    return analysis

# --- MODIFIKASI ---: Fungsi AI disesuaikan untuk level Kab/Kota
def get_ai_insights(df, api_key):
    """Generate AI insights menggunakan Google Gemini (dari skrip dashboard)."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash') # Menggunakan 1.5 Flash
        
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
        
        # Kabupaten/Kota analysis (sebelumnya provinsi)
        kabkot_stats = df.groupby('nama_kabupaten_kota')['jumlah_kasus'].agg(['sum', 'mean', 'std']).round(2)
        top_5_kabkot = kabkot_stats.nlargest(5, 'sum')['sum'].to_dict()
        
        # Year-over-year growth by kab/kota (sebelumnya provinsi)
        kabkot_growth = {}
        for kabkot in df['nama_kabupaten_kota'].unique():
            kabkot_data = df[df['nama_kabupaten_kota'] == kabkot].groupby('tahun')['jumlah_kasus'].sum()
            if len(kabkot_data) > 1:
                growth = ((kabkot_data.iloc[-1] - kabkot_data.iloc[0]) / kabkot_data.iloc[0] * 100) if kabkot_data.iloc[0] > 0 else 0
                kabkot_growth[kabkot] = round(growth, 2)
        
        # Variability analysis
        std_dev_nasional = df.groupby('tahun')['jumlah_kasus'].sum().std()
        
        # Siapkan data summary lengkap
        summary_data = {
            'total_kasus': int(df['jumlah_kasus'].sum()),
            'periode': f"{tahun_list[0]} - {tahun_list[-1]}",
            'jumlah_tahun': len(tahun_list),
            'growth_rate_provinsi': round(growth_rate, 2), # Ganti nama jadi growth_rate_provinsi (Jawa Barat)
            'rata_rata_kasus_per_tahun': round(df.groupby('tahun')['jumlah_kasus'].sum().mean(), 2),
            'std_dev_provinsi': round(std_dev_nasional, 2),
            'trend_tahunan': trend_tahunan,
            'top_5_kabkot': top_5_kabkot,
            'kabkot_growth': kabkot_growth,
            'jumlah_kabkot': df['nama_kabupaten_kota'].nunique()
        }
        
        # Prompt (disalin langsung)
        prompt = f"""
Sebagai ahli epidemiologi dan data scientist, lakukan analisis komprehensif terhadap data DBD Jawa Barat berikut:
[... Prompt lengkap Anda disisipkan di sini ...]
═══════════════════════════════════════════════════════════════════════════════
DATA SUMMARY (PROVINSI JAWA BARAT)
═══════════════════════════════════════════════════════════════════════════════
📊 STATISTIK DASAR:
- Total Kasus: {summary_data['total_kasus']:,} kasus
- Periode: {summary_data['periode']}
- Jumlah Kabupaten/Kota: {summary_data['jumlah_kabkot']} kab/kota
- Growth Rate Jawa Barat: {summary_data['growth_rate_provinsi']}%
- Rata-rata Kasus per Tahun: {summary_data['rata_rata_kasus_per_tahun']:,}
- Standar Deviasi: {summary_data['std_dev_provinsi']:,.0f}

📈 TREND TAHUNAN (JAWA BARAT):
{summary_data['trend_tahunan']}

🏆 TOP 5 KABUPATEN/KOTA (Total Kasus):
{summary_data['top_5_kabkot']}

📊 GROWTH RATE PER KABUPATEN/KOTA (%):
{summary_data['kabkot_growth']}
═══════════════════════════════════════════════════════════════════════════════
Berikan analisis dalam 4 JENIS ANALYTICS berikut dalam Bahasa Indonesia:
[... Sisa prompt lengkap Anda (Descriptive, Diagnostic, Predictive, Prescriptive) ...]
PENTING: 
- Gunakan data KONKRET dari summary di atas
- Berikan ANGKA dan PERSENTASE spesifik
- Sebutkan NAMA KABUPATEN/KOTA spesifik
- Buat rekomendasi yang ACTIONABLE dan MEASURABLE
- Prioritaskan berdasarkan URGENCY dan IMPACT
- Gunakan Bahasa Indonesia yang JELAS dan PROFESIONAL
"""
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"Error saat menghasilkan AI insights: {str(e)}\n\nPastikan API Key Gemini sudah diset dengan benar."

# --- MODIFIKASI ---: Fungsi diubah untuk level Kab/Kota
def create_trend_chart(df, selected_kabkots=None):
    """Membuat grafik trend kasus DBD per tahun per kab/kota."""
    if selected_kabkots:
        df_filtered = df[df['nama_kabupaten_kota'].isin(selected_kabkots)]
    else:
        df_filtered = df
    
    trend_data = df_filtered.groupby(['tahun', 'nama_kabupaten_kota'])['jumlah_kasus'].sum().reset_index()
    
    fig = px.bar(
        trend_data,
        x='tahun',
        y='jumlah_kasus',
        color='nama_kabupaten_kota', # Diubah dari nama_provinsi
        title='Trend Kasus DBD per Tahun per Kabupaten/Kota',
        labels={'jumlah_kasus': 'Jumlah Kasus', 'tahun': 'Tahun', 'nama_kabupaten_kota': 'Kabupaten/Kota'}, # Diubah
        barmode='group',
        height=500
    )
    
    fig.update_layout(
        xaxis=dict(tickmode='linear'),
        # hovermode 'x unified' diubah menjadi 'closest'
        hovermode='closest', 
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
     )
    
    return fig

# --- MODIFIKASI ---: Fungsi disederhanakan, filter provinsi tidak perlu lagi
def create_heatmap(df):
    """Membuat heatmap kasus DBD per kabupaten/kota."""
    
    # Ambil top 15 kabupaten/kota dengan kasus tertinggi dari data yang sudah difilter
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
        title="Heatmap Kasus DBD per Kabupaten/Kota (Top 15)", # Judul diubah
        aspect="auto",
        color_continuous_scale="Reds",
        height=600
    )
    
    fig.update_xaxes(side="bottom")
    
    return fig

def export_to_csv(df):
    """Export dataframe ke CSV (dari skrip dashboard)."""
    return df.to_csv(index=False).encode('utf-8')

def export_figure_to_png(fig):
    """Export plotly figure ke PNG (dari skrip dashboard)."""
    img_bytes = fig.to_image(format="png", width=1200, height=800)
    return img_bytes


# --- FUNGSI RENDER HALAMAN ---

def render_dashboard():
    """
    Render seluruh halaman Dashboard Interaktif (dari dashboard.py).
    """
    
    # --- MODIFIKASI ---: Judul diubah
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem; padding: 2rem 0;'>
        <h1 class="main-header">🦟 Dashboard DBD Jawa Barat</h1>
        <p class="subtitle">Business Intelligence untuk Analisis Demam Berdarah Dengue</p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- Sidebar Dashboard ---
    
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.2);'>
        <h2 style='color: white; margin: 0; font-size: 1.25rem; font-weight: 600;'>Kontrol Panel</h2>
        <p style='color: rgba(255,255,255,0.7); font-size: 0.875rem; margin: 0.5rem 0 0 0;'>Filter Data</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("### 📁 Sumber Data", unsafe_allow_html=True)
    
    df = load_data(DATA_FILE_PATH)
    
    if df is None or df.empty:
        st.sidebar.error("❌ Data tidak ditemukan atau kosong.")
        st.error("Gagal memuat data. Silakan hubungi admin.")
        st.stop()
    else:
        st.sidebar.info(f"Menggunakan data terpusat:\n`{DATA_FILE_PATH}`")
        st.sidebar.success("✅ Data berhasil dimuat")
    
    # --- Filter Section (dari dashboard.py) ---
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
    
    # --- MODIFIKASI ---: Filter Provinsi diubah menjadi Kab/Kota
    kabkots = sorted(df['nama_kabupaten_kota'].unique())
    st.sidebar.markdown("**🗺️ Kabupaten/Kota**")
    selected_kabkots = st.sidebar.multiselect(
        "Pilih Kabupaten/Kota",
        options=kabkots,
        default=kabkots,
        label_visibility="collapsed"
    )
    
    if len(kabkots) > 1:
        col_pr1, col_pr2 = st.sidebar.columns(2)
        with col_pr1:
            if st.sidebar.button("🌏 Semua", use_container_width=True, key="all_kabkots_btn"):
                selected_kabkots = kabkots
                st.rerun()
        with col_pr2:
            top_3_kabkot = df.groupby('nama_kabupaten_kota')['jumlah_kasus'].sum().nlargest(3).index.tolist()
            if st.sidebar.button("🔥 Top 3", use_container_width=True, key="top_kabkots_btn"):
                selected_kabkots = top_3_kabkot
                st.rerun()
    
    # Apply filters
    df_filtered = df[
        (df['tahun'].isin(selected_years)) &
        (df['nama_kabupaten_kota'].isin(selected_kabkots)) # Diubah dari nama_provinsi
    ]
    
    # --- MODIFIKASI ---: Filter Kab/Kota sekunder dihapus karena sudah jadi filter primer
    
    # --- MODIFIKASI: Data Summary Sidebar (Ringkasan Filter) dihapus ---
    # Blok yang menampilkan st.sidebar.metric "Records", "Total Kasus", dan "Kab/Kota"
    # telah dihapus dari sini.

    # --- Tombol Logout di Sidebar Dashboard ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔒 Akun", unsafe_allow_html=True)
    st.sidebar.write(f"Login sebagai: **{st.session_state.username}**")
    if st.sidebar.button("Logout", use_container_width=True, type="secondary", key="dashboard_logout"):
        perform_logout()

    
    # --- Main Content Dashboard ---
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
            # --- MODIFIKASI ---: Metrik disesuaikan
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Kasus", f"{int(analysis['total_kasus']):,}")
            with col2:
                st.metric("Rata-rata Kasus", f"{analysis['rata_rata_kasus']:.1f}")
            with col3:
                st.metric("Jumlah Kab/Kota", analysis['kabkot_count']) # Diubah dari Provinsi
            
            st.markdown("---")
            
            # Tabel Summary
            st.subheader("📋 Tabel Summary Data")
            # --- MODIFIKASI ---: Groupby diubah ke kab/kota
            summary_df = df_filtered.groupby(['nama_kabupaten_kota', 'tahun']).agg({
                'jumlah_kasus': ['sum', 'mean', 'count'],
            }).round(2)
            
            summary_df.columns = ['Total Kasus', 'Rata-rata Kasus', 'Jumlah Record']
            summary_df = summary_df.reset_index()
            
            st.dataframe(summary_df, use_container_width=True, height=400)
            
            st.markdown("---")
            
            # --- MODIFIKASI ---: Ranking Wilayah disederhanakan jadi 1 tabel
            st.subheader("🏆 Ranking Wilayah")
            
            st.write("**Top 10 Kabupaten/Kota**")
            top_kabkots_table = df_filtered.groupby('nama_kabupaten_kota')['jumlah_kasus'].sum().nlargest(10).reset_index()
            top_kabkots_table.columns = ['Kabupaten/Kota', 'Total Kasus']
            top_kabkots_table.insert(0, 'Rank', range(1, len(top_kabkots_table) + 1))
            st.dataframe(top_kabkots_table, use_container_width=True, hide_index=True)
            
        
        # TAB 2: Visualisasi & Analisis
        with tab2:
            st.header("📈 Visualisasi Data DBD")
            
            # --- MODIFIKASI ---: Trend Chart diubah ke level kab/kota
            st.subheader("📊 Trend Kasus DBD per Tahun")
            # Langsung buat chart tanpa filter
            trend_fig = create_trend_chart(df_filtered, None)
            st.plotly_chart(trend_fig, use_container_width=True)

            
            st.markdown("---")
            
            # --- MODIFIKASI ---: Judul Trend diubah
            st.subheader("📈 Trend Total Jawa Barat")
            national_trend = df_filtered.groupby('tahun')['jumlah_kasus'].sum().reset_index()
            fig_national = px.line(
                national_trend,
                x='tahun',
                y='jumlah_kasus',
                title='Trend Kasus DBD Jawa Barat', # Judul diubah
                labels={'jumlah_kasus': 'Total Kasus', 'tahun': 'Tahun'},
                markers=True
            )
            fig_national.update_traces(line_color='#667eea', line_width=3)
            st.plotly_chart(fig_national, use_container_width=True)
            
            st.markdown("---")
            
            # --- MODIFIKASI ---: Heatmap disederhanakan
            st.subheader("🔥 Heatmap Kasus DBD")
            st.info("Heatmap menampilkan 15 kabupaten/kota dengan kasus tertinggi dalam data yang terfilter.")
            heatmap_fig = create_heatmap(df_filtered) # Tidak perlu parameter
            st.plotly_chart(heatmap_fig, use_container_width=True)
            
            # --- MODIFIKASI ---: Pie chart diubah ke level kab/kota
            st.markdown("---")
            st.subheader("🥧 Distribusi Kasus per Kabupaten/Kota")
            
            kabkot_dist = df_filtered.groupby('nama_kabupaten_kota')['jumlah_kasus'].sum().reset_index()
            fig_pie = px.pie(
                kabkot_dist,
                values='jumlah_kasus',
                names='nama_kabupaten_kota', # Diubah dari nama_provinsi
                title='Proporsi Kasus DBD per Kabupaten/Kota' # Judul diubah
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # TAB 3: AI Insights & Rekomendasi
        with tab3:
            st.header("🤖 AI-Powered Analytics Dashboard")
            
            st.info("""
            **Powered by Google Gemini 1.5 Flash** - AI akan menganalisis data dan memberikan:
            - 📊 **Descriptive Analytics**: Kondisi saat ini
            - 🔍 **Diagnostic Analytics**: Penyebab masalah
            - 🔮 **Predictive Analytics**: Prediksi masa depan
            - 💡 **Prescriptive Analytics**: Rekomendasi actionable
            """)
            
            st.markdown("---")
            
            load_dotenv() # Load .env file
            
            # Get API Key from environment variable
            api_key = os.getenv('GEMINI_API_KEY', '')
            
            if not api_key:
                st.warning("""
                ⚠️ **API Key Gemini belum di-set!**
                
                Silakan set environment variable `GEMINI_API_KEY` terlebih dahulu.
                
                **Cara setup:**
                1. Buat file `.env` di root project
                2. Tambahkan: `GEMINI_API_KEY=your_api_key_here`
                3. Atau set di system environment variable
                
                Dapatkan API Key di: https://aistudio.google.com/app/apikey
                """)
            
            st.subheader("📊 Data yang Akan Dianalisis")
            # --- MODIFIKASI ---: Metrik disesuaikan
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Records", f"{len(df_filtered):,}")
            with col2:
                st.metric("Kab/Kota", df_filtered['nama_kabupaten_kota'].nunique())
            with col3:
                st.metric("Periode", f"{df_filtered['tahun'].min()}-{df_filtered['tahun'].max()}")
            with col4:
                st.metric("Total Kasus", f"{df_filtered['jumlah_kasus'].sum():,.0f}")
            
            st.markdown("---")
            
            generate_btn = st.button(
                "🚀 Generate 4 Analytics Insights", 
                type="primary", 
                use_container_width=True
            )
            
            if st.button("🔄 Reset", use_container_width=True):
                if 'ai_insights' in st.session_state:
                    del st.session_state['ai_insights']
                st.success("✅ Insights berhasil di-reset!")
                st.rerun()
            
            if generate_btn:
                if not api_key:
                    st.error("""
                    ❌ **API Key Belum Diisi!**
                    ... (Error message tidak berubah) ...
                    """)
                else:
                    with st.spinner("🧠 Gemini AI sedang menganalisis data Anda... (Ini mungkin memakan waktu 30-60 detik)"):
                        try:
                            insights = get_ai_insights(df_filtered, api_key)
                            
                            st.success("✅ Analisis Selesai! Scroll ke bawah untuk melihat hasil.")
                            
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
                            
                            st.session_state['ai_insights'] = insights
                            
                        except Exception as e:
                            st.error(f"""
                            ❌ **Error saat generate insights:**
                            ... (Error message tidak berubah) ...
                            {str(e)}
                            """)
            
            if 'ai_insights' in st.session_state:
                st.markdown("---")
                st.markdown("### 📌 Analytics Results (Tersimpan)")
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown(st.session_state['ai_insights'])
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 📊 Analisis Statistik Otomatis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**📈 Trend Tahunan (Jawa Barat)**")
                yearly_trend = df_filtered.groupby('tahun')['jumlah_kasus'].sum()
                if len(yearly_trend) > 1:
                    pct_change = ((yearly_trend.iloc[-1] - yearly_trend.iloc[0]) / yearly_trend.iloc[0] * 100)
                    trend_direction = "meningkat" if pct_change > 0 else "menurun"
                    st.write(f"- Kasus DBD {trend_direction} sebesar **{abs(pct_change):.1f}%** dari tahun {yearly_trend.index[0]} ke {yearly_trend.index[-1]}")
                    st.write(f"- Total kasus tahun {yearly_trend.index[-1]}: **{yearly_trend.iloc[-1]:,.0f} kasus**")
            
            # --- MODIFIKASI ---: Area prioritas diubah ke kab/kota
            with col2:
                st.write("**🎯 Area Prioritas**")
                top_3_kabkots = df_filtered.groupby('nama_kabupaten_kota')['jumlah_kasus'].sum().nlargest(3)
                st.write("**Top 3 Kabupaten/Kota yang Memerlukan Perhatian:**")
                for i, (kabkot, kasus) in enumerate(top_3_kabkots.items(), 1):
                    st.write(f"{i}. {kabkot}: **{kasus:,.0f} kasus**")
            
            st.markdown("---")
            
            st.write("**💊 Rekomendasi Mitigasi Umum**")
            st.markdown("""
            1. **Fokus Intervensi**: Prioritaskan kabupaten/kota dengan kasus tertinggi untuk program fogging dan 3M Plus
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
                
                csv_data = export_to_csv(df_filtered)
                st.download_button(
                    label="⬇️ Download Data Terfilter (CSV)",
                    data=csv_data,
                    file_name=f"data_dbd_filtered_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                summary_csv = export_to_csv(summary_df)
                st.download_button(
                    label="⬇️ Download Summary Data (CSV)",
                    data=summary_csv,
                    file_name=f"summary_dbd_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # --- MODIFIKASI ---: Export top provinsi diubah ke kab/kota
                top_kabkot_csv = export_to_csv(top_kabkots_table)
                st.download_button(
                    label="⬇️ Download Top Kab/Kota (CSV)",
                    data=top_kabkot_csv,
                    file_name=f"top_kabkot_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                st.subheader("📈 Export Visualisasi")
                
                st.info("💡 Klik tombol di bawah untuk generate dan download grafik dalam format PNG")
                
                try:
                    if st.button("📊 Generate Trend Chart PNG", use_container_width=True):
                        with st.spinner("Generating..."):
                            trend_fig_export = create_trend_chart(df_filtered)
                            img_bytes = export_figure_to_png(trend_fig_export)
                            st.download_button(
                                label="⬇️ Download Trend Chart",
                                data=img_bytes,
                                file_name=f"trend_chart_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.png",
                                mime="image/png"
                            )
                    
                    if st.button("🔥 Generate Heatmap PNG", use_container_width=True):
                        with st.spinner("Generating..."):
                            heatmap_fig_export = create_heatmap(df_filtered)
                            img_bytes = export_figure_to_png(heatmap_fig_export)
                            st.download_button(
                                label="⬇️ Download Heatmap",
                                data=img_bytes,
                                file_name=f"heatmap_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.png",
                                mime="image/png"
                            )
                except Exception as e:
                    st.warning(f"Gagal generate PNG. Pastikan library 'kaleido' terinstall. (Error: {e})")
            
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
        st.markdown("""
        <div style='text-align: center; padding: 3rem; background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
            <div style='font-size: 4rem;'>📭</div>
            <h2 style='color: #333; margin-bottom: 1rem;'>Tidak Ada Data</h2>
            <p style='color: #666; font-size: 1.1rem; margin-bottom: 2rem;'>
                Tidak ada data yang sesuai dengan filter yang dipilih
            </p>
            <p style='color: #667eea;'>💡 <strong>Saran:</strong> Coba ubah pilihan filter di sidebar.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0; color: #64748b;'>
        <p>Powered by <strong>Kelompok B6</strong></p>
        <p style='font-size: 0.875rem; margin-top: 0.5rem;'>Dashboard DBD Jawa Barat</p>
    </div>
    """, unsafe_allow_html=True)

def render_admin_panel():
    """
    Render seluruh halaman Admin Panel (dari admin.py).
    (Logika "Simpan" telah diperbaiki untuk menangani 'daerah' admin)
    """
    
    init_log_file(LOG_FILE_PATH)

    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.2);'>
            <h2 style='color: white; margin: 0; font-size: 1.25rem; font-weight: 600;'>👨‍💼 Profil Admin</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.write(f"**Username:** {st.session_state.username}")
        st.write(f"**Role:** {st.session_state.role.capitalize()}")
        if st.session_state.role == "daerah":
            st.write(f"**Wilayah:** {st.session_state.region_code}")
        
        st.markdown("<br>", unsafe_allow_html=True) 
        
        if st.button("Logout", use_container_width=True, type="secondary", key="admin_logout"):
            perform_logout()

    st.markdown('<h1 class="main-header">📊 Dashboard Admin Kasus DBD Jawa Barat</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Manajemen Data Kasus Demam Berdarah Dengue</p>', unsafe_allow_html=True)

    df_full = load_data(DATA_FILE_PATH) 
    
    if df_full is None:
        st.error("Gagal memuat data utama. Panel Admin tidak dapat ditampilkan.")
        st.stop()
        
    if df_full.empty:
        st.warning("Data kosong. Silakan tambahkan data pertama.")
        # Buat df_display kosong agar data_editor tetap bisa render
        df_display = pd.DataFrame(columns=[
            'id', 'kode_provinsi', 'nama_provinsi', 'kode_kabupaten_kota', 
            'nama_kabupaten_kota', 'jumlah_kasus', 'satuan', 'tahun'
        ])
    else:
        if st.session_state.role == "master":
            st.header("Semua Data (Master Admin)")
            df_display = df_full.copy()
        else: # role == "daerah"
            region_code = st.session_state.region_code
            nama_daerah_series = df_full[df_full['kode_kabupaten_kota'] == region_code]['nama_kabupaten_kota']
            nama_daerah = nama_daerah_series.iloc[0] if not nama_daerah_series.empty else f"Kode {region_code}"
            
            st.header(f"Data untuk Wilayah: {nama_daerah}")
            
            df_display = df_full[df_full['kode_kabupaten_kota'] == region_code].copy()
            
            if df_display.empty:
                st.warning("Belum ada data untuk wilayah Anda.")

    st.header("Kelola Data (CRUD)")

    if not df_display.empty:
        df_display.insert(0, "pilih_hapus", False)
    else:
        # Jika df_display kosong, tambahkan kolom 'pilih_hapus'
        df_display["pilih_hapus"] = []

    config = {
        "pilih_hapus": st.column_config.CheckboxColumn(
            "Pilih Hapus", 
            help="Centang untuk menghapus baris. Klik 'Hapus Baris Terpilih' di bawah."
        ),
    }

    if st.session_state.role == "daerah":
        config.update({
            "kode_kabupaten_kota": st.column_config.TextColumn(disabled=True),
            "nama_kabupaten_kota": st.column_config.TextColumn(disabled=True),
            "kode_provinsi": st.column_config.TextColumn(disabled=True),
            "nama_provinsi": st.column_config.TextColumn(disabled=True),
            "satuan": st.column_config.TextColumn(disabled=True),
        })
    
    st.info("Untuk Edit/Tambah: Ubah langsung tabel di bawah dan klik 'Simpan Perubahan'.\n\nUntuk Hapus: Centang baris dan klik 'Hapus Baris Terpilih'.")
    
    edited_df = st.data_editor(
        df_display,
        num_rows="dynamic",
        column_config=config,
        key="data_editor",
        use_container_width=True,
        height=400 
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Simpan Perubahan (Edit/Tambah)", use_container_width=True, type="primary"):
            username = st.session_state.username
            
            # --- START PERBAIKAN ---
            
            # 1. Ambil dataframe terbaru dari data_editor
            df_from_editor = edited_df.copy()
            
            try:
                # 2. Log perubahan (logika ini opsional tapi bagus untuk ada)
                edited_changes = st.session_state.data_editor.get("edited_rows", {})
                added_changes = st.session_state.data_editor.get("added_rows", [])

                for row_index, changes in edited_changes.items():
                    if row_index < len(df_display): # Pastikan index valid
                        original_row = df_display.iloc[row_index]
                        details = f"Memperbarui baris (id: {original_row.get('id', 'N/A')}, wilayah: {original_row.get('nama_kabupaten_kota', 'N/A')}). Perubahan: {changes}"
                        write_log(username, "UPDATE", details)

                for new_row_data in added_changes:
                        details = f"Mencoba membuat baris baru. Data mentah: {new_row_data}"
                        write_log(username, "CREATE_ATTEMPT", details)
                
                # 3. FIX: Isi data yang nonaktif untuk admin daerah
                if st.session_state.role == "daerah":
                    region_code = st.session_state.region_code
                    
                    # Ambil info default dari data yang ada atau hardcode
                    if not df_display.empty:
                        nama_daerah = df_display['nama_kabupaten_kota'].iloc[0]
                        nama_prov = df_display['nama_provinsi'].iloc[0]
                        kode_prov = df_display['kode_provinsi'].iloc[0]
                        satuan_default = df_display['satuan'].iloc[0]
                    elif not df_full.empty:
                        # Jika admin daerah belum punya data, coba cari infonya dari df_full
                        region_info = df_full[df_full['kode_kabupaten_kota'] == region_code]
                        if not region_info.empty:
                            nama_daerah = region_info['nama_kabupaten_kota'].iloc[0]
                            nama_prov = region_info['nama_provinsi'].iloc[0]
                            kode_prov = region_info['kode_provinsi'].iloc[0]
                            satuan_default = region_info['satuan'].iloc[0]
                        else: # Jika kode tidak ada di df_full, pakai default
                            nama_daerah = f"Wilayah {region_code}"
                            nama_prov = "JAWA BARAT"
                            kode_prov = "32"
                            satuan_default = "KASUS"
                    else:
                        # Jika df_full juga kosong (awal), hardcode
                        nama_daerah = f"Wilayah {region_code}"
                        nama_prov = "JAWA BARAT"
                        kode_prov = "32"
                        satuan_default = "KASUS"

                    # Isi nilai NaN/None di kolom nonaktif HANYA untuk baris baru
                    # st.data_editor akan mengisi NaN untuk kolom nonaktif saat baris baru dibuat
                    df_from_editor['kode_kabupaten_kota'] = df_from_editor['kode_kabupaten_kota'].fillna(region_code)
                    df_from_editor['nama_kabupaten_kota'] = df_from_editor['nama_kabupaten_kota'].fillna(nama_daerah)
                    df_from_editor['kode_provinsi'] = df_from_editor['kode_provinsi'].fillna(kode_prov)
                    df_from_editor['nama_provinsi'] = df_from_editor['nama_provinsi'].fillna(nama_prov)
                    df_from_editor['satuan'] = df_from_editor['satuan'].fillna(satuan_default)

                # 4. Gabungkan kembali dengan data wilayah lain
                if st.session_state.role == "master":
                    final_df_to_save = df_from_editor
                else:
                    # Ambil data wilayah lain dari df_full (data SEBELUM diedit)
                    other_regions_data = df_full[df_full['kode_kabupaten_kota'] != st.session_state.region_code]
                    # Gabungkan data wilayah lain + data baru dari editor
                    final_df_to_save = pd.concat([other_regions_data, df_from_editor], ignore_index=True)

                # 5. Simpan ke file
                save_data(final_df_to_save, DATA_FILE_PATH)
                st.success("Perubahan berhasil disimpan!")
                st.cache_data.clear() 
                st.rerun()

            except Exception as e:
                st.error(f"Terjadi kesalahan saat menyimpan: {e}")
                
            # --- END PERBAIKAN ---

    with col2:
        if st.button("🗑️ Hapus Baris Terpilih", use_container_width=True):
            username = st.session_state.username
            
            # Logika Hapus (Sudah Benar)
            rows_to_keep = edited_df[edited_df["pilih_hapus"] == False]
            
            if len(rows_to_keep) == len(edited_df):
                st.warning("Tidak ada baris yang dipilih untuk dihapus.")
            else:
                try:
                    rows_to_delete = edited_df[edited_df["pilih_hapus"] == True]
                    for index, row_data in rows_to_delete.iterrows():
                        details = f"Menghapus baris (id: {row_data.get('id', 'N/A')}, wilayah: {row_data.get('nama_kabupaten_kota', 'N/A')}, tahun: {row_data.get('tahun', 'N/A')})"
                        write_log(username, "DELETE", details)
                    
                    if st.session_state.role == "master":
                        final_df_to_save = rows_to_keep
                    else:
                        other_regions_data = df_full[df_full['kode_kabupaten_kota'] != st.session_state.region_code]
                        final_df_to_save = pd.concat([other_regions_data, rows_to_keep], ignore_index=True)
                    
                    save_data(final_df_to_save, DATA_FILE_PATH)
                    st.success("Baris yang dipilih berhasil dihapus!")
                    st.cache_data.clear() 
                    st.rerun()

                except Exception as e:
                    st.error(f"Terjadi kesalahan saat menghapus: {e}")
    
    # --- START MODIFIKASI (SESUAI PERMINTAAN) ---
    if st.session_state.role == "master":
        st.markdown("---")
        st.header("📜 Log Aktivitas Admin")
        
        if st.button("🔄 Muat Ulang Log"):
            st.cache_data.clear()
            st.rerun()
            
        log_df = load_logs(LOG_FILE_PATH)
        
        if log_df.empty:
            st.info("Belum ada aktivitas yang tercatat.")
        else:
            # Definisikan kategori aksi
            data_actions = ["UPDATE", "CREATE_ATTEMPT", "DELETE"]
            auth_actions = ["LOGIN", "LOGOUT"]
            
            # Filter DataFrame berdasarkan kategori
            data_log_df = log_df[log_df['action'].isin(data_actions)].sort_values(by="timestamp", ascending=False)
            auth_log_df = log_df[log_df['action'].isin(auth_actions)].sort_values(by="timestamp", ascending=False)
            
            # 1. Tampilkan Log Aktivitas Perubahan Data
            st.subheader("1. Log Aktivitas Perubahan Data (CRUD)")
            if data_log_df.empty:
                st.info("Belum ada aktivitas perubahan data (tambah, edit, hapus) yang tercatat.")
            else:
                st.dataframe(
                    data_log_df,
                    use_container_width=True,
                    height=300
                )
            
            st.markdown("<br>", unsafe_allow_html=True) # Memberi jarak
            
            # 2. Tampilkan Log Aktivitas Login Admin
            st.subheader("2. Log Aktivitas Login & Logout")
            if auth_log_df.empty:
                st.info("Belum ada aktivitas login atau logout yang tercatat.")
            else:
                st.dataframe(
                    auth_log_df,
                    use_container_width=True,
                    height=300
                )
    # --- END MODIFIKASI ---
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0; color: #64748b;'>
        <p>Panel Admin Dashboard DBD</p>
        <p style='font-size: 0.875rem; margin-top: 0.5rem;'>© 2025</p>
    </div>
    """, unsafe_allow_html=True)


# --- MAIN APP ROUTER (LOGIKA UTAMA) ---

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.session_state.region_code = None

    if not st.session_state.logged_in:
        
        st.markdown('<h1 class="main-header">🔒 Login Aplikasi Dashboard DBD</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Silakan login sebagai Admin atau masuk sebagai Guest</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            
            # --- MODIFIKASI: Form Admin ---
            st.markdown("### 👨‍💼 Login Admin")
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                login_button = st.form_submit_button(
                    "Login Admin",  # Teks tombol diubah
                    use_container_width=True, 
                    type="primary"
                )

                if login_button:
                    success, role, region_code = check_login(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.role = role
                        st.session_state.username = username
                        st.session_state.region_code = region_code
                        st.cache_data.clear() 
                        st.rerun()
                    else:
                        st.error("Username atau Password salah!")
            
            # --- MODIFIKASI: Pemisah dan Tombol Guest ---
            st.markdown(
                "<p style='text-align: center; margin: 1rem 0; color: #64748b;'>atau</p>", 
                unsafe_allow_html=True
            )
            
            if st.button("Masuk sebagai Guest", use_container_width=True, type="secondary"):
                # Logika untuk login sebagai guest
                init_log_file(LOG_FILE_PATH)
                write_log("guest", "LOGIN", "Pengguna 'guest' berhasil login.")
                
                st.session_state.logged_in = True
                st.session_state.role = "user" # Role "user" tetap dipakai untuk routing ke dashboard
                st.session_state.username = "guest"
                st.session_state.region_code = None
                
                st.cache_data.clear()
                st.rerun()

    else:
        # Bagian ini tetap sama, routing "user" akan menangkap "guest"
        if st.session_state.role == "user":
            render_dashboard()
        elif st.session_state.role in ["master", "daerah"]:
            render_admin_panel()
        else:
            st.error("Peran pengguna tidak dikenali. Silakan logout dan login kembali.")
            if st.button("Logout"):
                perform_logout()

if __name__ == "__main__":
    # Pastikan file .env dimuat jika ada
    load_dotenv() 
    main()