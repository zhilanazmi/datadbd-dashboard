import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Dashboard Admin DBD", 
    page_icon="🦟", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS (Disalin dari Dashboard Utama) ---
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
    
    /* Header (Untuk Tampilan Internal) */
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
    
    /* Metric Cards (jika digunakan) */
    .stMetric {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    /* Buttons di Main Area */
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
    
    /* Tombol sekunder (misal Hapus) */
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
    
    /* === Sidebar Styling === */
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
    
    /* Tombol di Sidebar (cth: Logout) */
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        font-size: 0.9375rem !important; /* Ukuran font konsisten */
        padding: 0.625rem 1.5rem !important;
        border-radius: 8px !important;
        width: 100%; /* Tombol logout full-width */
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.15) !important;
    }
    
    /* Info boxes di sidebar (jika ada) */
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
    </style>
""", unsafe_allow_html=True)


# --- Path ke File ---
DATA_FILE_PATH = "data_dbd.csv"
LOG_FILE_PATH = "admin_log.csv" 

# --- Definisi Pengguna (Admin) ---
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

# --- Fungsi Helper untuk LOG ---

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

# --- Fungsi Helper untuk DATA ---

@st.cache_data
def load_data(filepath):
    """Memuat data dari CSV."""
    if not os.path.exists(filepath):
        st.error(f"File data {filepath} tidak ditemukan!")
        st.info("Pastikan Anda sudah membuat file `data_dbd.csv` di folder yang sama.")
        return pd.DataFrame(columns=[
            'id', 'kode_provinsi', 'nama_provinsi', 'kode_kabupaten_kota', 
            'nama_kabupaten_kota', 'jumlah_kasus', 'satuan', 'tahun'
        ])
    
    try:
        df = pd.read_csv(filepath)
        if 'kode_kabupaten_kota' in df.columns:
            df['kode_kabupaten_kota'] = df['kode_kabupaten_kota'].astype(str)
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return pd.DataFrame()

def save_data(df, filepath):
    """Menyimpan DataFrame kembali ke CSV."""
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

def check_login(username, password):
    """Memeriksa kredensial pengguna dan mencatat log jika berhasil."""
    user = ADMIN_USERS.get(username)
    if user and user["password"] == password:
        init_log_file(LOG_FILE_PATH)
        write_log(username, "LOGIN", f"Admin '{username}' berhasil login.")
        return True, user["role"], user["region_code"]
    return False, None, None

# --- Logika Login ---

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.region_code = None

if not st.session_state.logged_in:
    
    # --- HALAMAN LOGIN (SESUAI PERMINTAAN: TIDAK DIUBAH) ---
    # Catatan: Font dan warna background mungkin berubah karena CSS global,
    # tapi struktur Python tetap standar.
    
    st.title("🔒 Login Admin Dashboard DBD")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

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
else:
    # --- Halaman Aplikasi Utama (Setelah Login) ---
    
    init_log_file(LOG_FILE_PATH)

    # Sidebar (Kini menggunakan style dari CSS)
    with st.sidebar:
        # Menggunakan style header sidebar dari dashboard
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.2);'>
            <h2 style='color: white; margin: 0; font-size: 1.25rem; font-weight: 600;'>👨‍💼 Profil Admin</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.write(f"**Username:** {st.session_state.username}")
        st.write(f"**Role:** {st.session_state.role.capitalize()}")
        if st.session_state.role == "daerah":
            st.write(f"**Wilayah:** {st.session_state.region_code}")
        
        st.markdown("<br>", unsafe_allow_html=True) # Spasi
        
        # Tombol logout otomatis ter-styling oleh CSS
        if st.button("Logout", use_container_width=True):
            write_log(st.session_state.username, "LOGOUT", f"Admin '{st.session_state.username}' logout.")
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.username = None
            st.session_state.region_code = None
            st.cache_data.clear()
            st.rerun()

    # Konten Utama (Kini menggunakan style dari CSS)
    
    # Mengganti st.title dengan header kustom
    st.markdown('<h1 class="main-header">📊 Dashboard Admin Kasus DBD Jawa Barat</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Manajemen Data Kasus Demam Berdarah Dengue</p>', unsafe_allow_html=True)

    df_full = load_data(DATA_FILE_PATH)
    
    if df_full.empty:
        st.warning("Data kosong atau gagal dimuat. Cek file `data_dbd.csv`.")
    else:
        # Filter data berdasarkan role
        if st.session_state.role == "master":
            st.header("Semua Data (Master Admin)") # Menggunakan st.header
            df_display = df_full.copy()
        else: # role == "daerah"
            region_code = st.session_state.region_code
            nama_daerah_series = df_full[df_full['kode_kabupaten_kota'] == region_code]['nama_kabupaten_kota']
            nama_daerah = nama_daerah_series.iloc[0] if not nama_daerah_series.empty else f"Kode {region_code}"
            
            st.header(f"Data untuk Wilayah: {nama_daerah}") # Menggunakan st.header
            
            df_display = df_full[df_full['kode_kabupaten_kota'] == region_code].copy()
            
            if df_display.empty:
                st.warning("Belum ada data untuk wilayah Anda.")

        # --- Fitur CRUD ---
        st.header("Kelola Data (CRUD)")

        if not df_display.empty:
            df_display.insert(0, "pilih_hapus", False)

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
        
        # st.info otomatis ter-styling
        st.info("Untuk Edit/Tambah: Ubah langsung tabel di bawah dan klik 'Simpan Perubahan'.\n\nUntuk Hapus: Centang baris dan klik 'Hapus Baris Terpilih'.")
        
        # st.data_editor otomatis ter-styling
        edited_df = st.data_editor(
            df_display,
            num_rows="dynamic",
            column_config=config,
            key="data_editor",
            use_container_width=True,
            height=400 
        )

        # --- Tombol Aksi (Otomatis ter-styling) ---
        
        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Simpan Perubahan (Edit/Tambah)", use_container_width=True, type="primary"):
                username = st.session_state.username
                
                edited_changes = st.session_state.data_editor.get("edited_rows", {})
                added_changes = st.session_state.data_editor.get("added_rows", [])

                try:
                    for row_index, changes in edited_changes.items():
                        original_row = df_display.iloc[row_index]
                        details = f"Memperbarui baris (id: {original_row.get('id', 'N/A')}, wilayah: {original_row.get('nama_kabupaten_kota', 'N/A')}). Perubahan: {changes}"
                        write_log(username, "UPDATE", details)

                    for new_row in added_changes:
                        nama_wilayah = new_row.get('nama_kabupaten_kota', 'N/A')
                        if nama_wilayah == 'N/A' and st.session_state.role == 'daerah':
                            code = st.session_state.region_code
                            nama_daerah_list = df_full[df_full['kode_kabupaten_kota'] == code]['nama_kabupaten_kota'].unique()
                            if len(nama_daerah_list) > 0:
                                nama_wilayah = nama_daerah_list[0]
                        
                        log_data = new_row.copy()
                        log_data['nama_kabupaten_kota'] = nama_wilayah
                        details = f"Membuat baris baru (wilayah: {nama_wilayah}). Data: {log_data}"
                        write_log(username, "CREATE", details)

                    if st.session_state.role == "master":
                        final_df_to_save = edited_df
                    else:
                        other_regions_data = df_full[df_full['kode_kabupaten_kota'] != st.session_state.region_code]
                        final_df_to_save = pd.concat([other_regions_data, edited_df], ignore_index=True)

                    save_data(final_df_to_save, DATA_FILE_PATH)
                    st.success("Perubahan berhasil disimpan!")
                    st.cache_data.clear() 
                    st.rerun()

                except Exception as e:
                    st.error(f"Terjadi kesalahan saat menyimpan: {e}")

        with col2:
            if st.button("🗑️ Hapus Baris Terpilih", use_container_width=True):
                username = st.session_state.username
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
    
    # --- Tampilan Log (Hanya Master Admin) ---
    if st.session_state.role == "master":
        st.markdown("---")
        st.header("📜 Log Aktivitas Admin") # Menggunakan st.header
        
        if st.button("🔄 Muat Ulang Log"):
            st.cache_data.clear()
            st.rerun()
            
        log_df = load_logs(LOG_FILE_PATH)
        
        if log_df.empty:
            st.info("Belum ada aktivitas yang tercatat.")
        else:
            # st.dataframe otomatis ter-styling
            st.dataframe(
                log_df.sort_values(by="timestamp", ascending=False),
                use_container_width=True,
                height=300
            )
            
    # Footer kustom (Sesuai Dashboard)
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0; color: #64748b;'>
        <p>Panel Admin Dashboard DBD</p>
        <p style='font-size: 0.875rem; margin-top: 0.5rem;'>© 2025</p>
    </div>
    """, unsafe_allow_html=True)