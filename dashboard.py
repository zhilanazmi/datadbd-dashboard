"""
Dashboard Interaktif DBD Indonesia
Menggunakan Streamlit dan Claude AI untuk Business Intelligence
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from anthropic import Anthropic
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

# Custom CSS untuk styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .recommendation-box {
        background-color: #fff4e6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #ff7f0e;
        margin: 1rem 0;
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

# Fungsi untuk mendapatkan insight dari Claude AI
def get_ai_insights(df, api_key):
    """Generate AI insights menggunakan Claude Sonnet 4.0"""
    try:
        client = Anthropic(api_key=api_key)
        
        # Siapkan data summary untuk analisis
        summary_data = {
            'total_kasus': int(df['jumlah_kasus'].sum()),
            'tahun_data': df['tahun'].unique().tolist(),
            'provinsi_tertinggi': df.groupby('nama_provinsi')['jumlah_kasus'].sum().nlargest(5).to_dict(),
            'trend_tahunan': df.groupby('tahun')['jumlah_kasus'].sum().to_dict(),
            'kabkot_tertinggi': df.groupby(['nama_provinsi', 'nama_kabupaten_kota'])['jumlah_kasus'].sum().nlargest(5).to_dict()
        }
        
        prompt = f"""
Analisis data DBD Indonesia berikut dan berikan insight mendalam:

Data Summary:
- Total Kasus: {summary_data['total_kasus']} kasus
- Periode: {summary_data['tahun_data']}
- Top 5 Provinsi: {summary_data['provinsi_tertinggi']}
- Trend Tahunan: {summary_data['trend_tahunan']}
- Top 5 Kabupaten/Kota: {summary_data['kabkot_tertinggi']}

Berikan analisis dalam format berikut:
1. INSIGHT TREN NASIONAL: Analisis tren kasus DBD secara nasional dari tahun ke tahun
2. INSIGHT REGIONAL: Analisis pola penyebaran berdasarkan provinsi dan kabupaten/kota
3. REKOMENDASI MITIGASI: Berikan 5-7 rekomendasi konkret untuk mitigasi berdasarkan data
4. PREDIKSI & PERINGATAN: Area yang perlu perhatian khusus

Berikan dalam format yang mudah dibaca dan terstruktur dalam Bahasa Indonesia.
"""
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    
    except Exception as e:
        return f"Error saat menghasilkan AI insights: {str(e)}\n\nPastikan API Key Claude sudah diset dengan benar."

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
    # Header
    st.markdown('<h1 class="main-header">🦟 Dashboard DBD Indonesia</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <p style='font-size: 1.2rem; color: #666;'>
            Dashboard Business Intelligence untuk Analisis Data Demam Berdarah Dengue di Indonesia
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - Upload dan Filter
    st.sidebar.header("📁 Upload Data")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload file CSV",
        type=['csv'],
        help="Upload file CSV dengan format kolom yang sesuai"
    )
    
    # Load data
    if uploaded_file is not None:
        df = load_data(uploaded_file)
    else:
        # Load default sample data
        if os.path.exists('data_dbd_sample.csv'):
            df = load_data('data_dbd_sample.csv')
            st.sidebar.info("📊 Menggunakan data sample default")
        else:
            st.warning("⚠️ Silakan upload file CSV untuk memulai analisis")
            st.stop()
    
    if df is None or df.empty:
        st.error("❌ Data tidak valid atau kosong")
        st.stop()
    
    # Sidebar - Filters
    st.sidebar.header("🔍 Filter Data")
    
    # Filter Tahun
    years = sorted(df['tahun'].unique())
    selected_years = st.sidebar.multiselect(
        "Pilih Tahun",
        options=years,
        default=years,
        help="Filter berdasarkan tahun"
    )
    
    # Filter Provinsi
    provinces = sorted(df['nama_provinsi'].unique())
    selected_provinces = st.sidebar.multiselect(
        "Pilih Provinsi",
        options=provinces,
        default=provinces,
        help="Filter berdasarkan provinsi"
    )
    
    # Apply filters
    df_filtered = df[
        (df['tahun'].isin(selected_years)) &
        (df['nama_provinsi'].isin(selected_provinces))
    ]
    
    # Filter Kabupaten/Kota (berdasarkan provinsi yang dipilih)
    if selected_provinces:
        kabkot_options = sorted(df_filtered['nama_kabupaten_kota'].unique())
        selected_kabkot = st.sidebar.multiselect(
            "Pilih Kabupaten/Kota",
            options=kabkot_options,
            default=kabkot_options,
            help="Filter berdasarkan kabupaten/kota"
        )
        
        df_filtered = df_filtered[df_filtered['nama_kabupaten_kota'].isin(selected_kabkot)]
    
    # Display data info
    st.sidebar.markdown("---")
    st.sidebar.metric("Total Records", len(df_filtered))
    st.sidebar.metric("Total Kasus", f"{df_filtered['jumlah_kasus'].sum():,}")
    
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
            col1, col2, col3, col4 = st.columns(4)
            
            analysis = analyze_data(df_filtered)
            
            with col1:
                st.metric(
                    "Total Kasus",
                    f"{analysis['total_kasus']:,.0f}",
                    delta=None
                )
            
            with col2:
                st.metric(
                    "Rata-rata Kasus",
                    f"{analysis['rata_rata_kasus']:,.1f}",
                    delta=None
                )
            
            with col3:
                st.metric(
                    "Jumlah Provinsi",
                    f"{analysis['provinsi_count']}",
                    delta=None
                )
            
            with col4:
                st.metric(
                    "Jumlah Kab/Kota",
                    f"{analysis['kabkot_count']}",
                    delta=None
                )
            
            st.markdown("---")
            
            # Tabel Summary
            st.subheader("📋 Tabel Summary Data")
            
            # Summary per provinsi dan tahun
            summary_df = df_filtered.groupby(['nama_provinsi', 'tahun']).agg({
                'jumlah_kasus': ['sum', 'mean', 'count'],
                'nama_kabupaten_kota': 'nunique'
            }).round(2)
            
            summary_df.columns = ['Total Kasus', 'Rata-rata Kasus', 'Jumlah Record', 'Jumlah Kab/Kota']
            summary_df = summary_df.reset_index()
            
            st.dataframe(
                summary_df,
                use_container_width=True,
                height=400
            )
            
            # Top 10 Wilayah dengan Kasus Tertinggi
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🔝 Top 10 Provinsi (Kasus Tertinggi)")
                top_provinces = df_filtered.groupby('nama_provinsi')['jumlah_kasus'].sum().nlargest(10).reset_index()
                top_provinces.columns = ['Provinsi', 'Total Kasus']
                st.dataframe(top_provinces, use_container_width=True, hide_index=True)
            
            with col2:
                st.subheader("🔝 Top 10 Kabupaten/Kota (Kasus Tertinggi)")
                top_kabkot = df_filtered.groupby('nama_kabupaten_kota')['jumlah_kasus'].sum().nlargest(10).reset_index()
                top_kabkot.columns = ['Kabupaten/Kota', 'Total Kasus']
                st.dataframe(top_kabkot, use_container_width=True, hide_index=True)
            
            # Detail data table
            st.markdown("---")
            st.subheader("📄 Data Detail")
            st.dataframe(df_filtered, use_container_width=True, height=400)
        
        # TAB 2: Visualisasi & Analisis
        with tab2:
            st.header("📈 Visualisasi Data DBD")
            
            # Trend Chart
            st.subheader("📊 Trend Kasus DBD per Tahun")
            
            # Option untuk memilih provinsi spesifik untuk trend
            trend_provinces = st.multiselect(
                "Pilih provinsi untuk ditampilkan di grafik (kosongkan untuk semua)",
                options=sorted(df_filtered['nama_provinsi'].unique()),
                default=None,
                key='trend_provinces'
            )
            
            trend_fig = create_trend_chart(df_filtered, trend_provinces if trend_provinces else None)
            st.plotly_chart(trend_fig, use_container_width=True)
            
            # Insight singkat tentang trend
            st.markdown("---")
            
            # Grafik tambahan - Trend Nasional
            st.subheader("📈 Trend Nasional Kasus DBD")
            national_trend = df_filtered.groupby('tahun')['jumlah_kasus'].sum().reset_index()
            
            fig_national = px.line(
                national_trend,
                x='tahun',
                y='jumlah_kasus',
                title='Trend Kasus DBD Nasional',
                labels={'jumlah_kasus': 'Total Kasus', 'tahun': 'Tahun'},
                markers=True
            )
            fig_national.update_traces(line_color='#1f77b4', line_width=3)
            st.plotly_chart(fig_national, use_container_width=True)
            
            # Heatmap
            st.markdown("---")
            st.subheader("🔥 Heatmap Kasus DBD per Kabupaten/Kota")
            
            heatmap_province = st.selectbox(
                "Pilih Provinsi untuk Heatmap (kosongkan untuk Top 15 Kabupaten/Kota)",
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
            st.header("🤖 AI Insights & Rekomendasi")
            st.markdown("""
            Gunakan kekuatan Claude Sonnet 4.0 untuk mendapatkan insight mendalam dan rekomendasi 
            berdasarkan analisis data DBD.
            """)
            
            # Input API Key
            api_key = st.text_input(
                "🔑 Masukkan Anthropic API Key",
                type="password",
                help="Dapatkan API key dari https://console.anthropic.com/",
                value=os.getenv('ANTHROPIC_API_KEY', '')
            )
            
            if st.button("🚀 Generate AI Insights", type="primary", use_container_width=True):
                if not api_key:
                    st.error("❌ Silakan masukkan API Key terlebih dahulu")
                else:
                    with st.spinner("🤖 Claude AI sedang menganalisis data..."):
                        insights = get_ai_insights(df_filtered, api_key)
                        
                        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                        st.markdown("### 💡 AI-Generated Insights & Recommendations")
                        st.markdown(insights)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Save insights to session state
                        st.session_state['ai_insights'] = insights
            
            # Display saved insights if available
            if 'ai_insights' in st.session_state:
                st.markdown("---")
                st.markdown("### 📌 Insight Tersimpan")
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown(st.session_state['ai_insights'])
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Manual insights based on data
            st.markdown("---")
            st.markdown("### 📊 Analisis Statistik Otomatis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
                st.markdown("#### 📈 Trend Tahunan")
                
                yearly_trend = df_filtered.groupby('tahun')['jumlah_kasus'].sum()
                if len(yearly_trend) > 1:
                    pct_change = ((yearly_trend.iloc[-1] - yearly_trend.iloc[0]) / yearly_trend.iloc[0] * 100)
                    trend_direction = "meningkat" if pct_change > 0 else "menurun"
                    st.write(f"- Kasus DBD {trend_direction} sebesar **{abs(pct_change):.1f}%** dari tahun {yearly_trend.index[0]} ke {yearly_trend.index[-1]}")
                    st.write(f"- Total kasus tahun {yearly_trend.index[-1]}: **{yearly_trend.iloc[-1]:,.0f} kasus**")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
                st.markdown("#### 🎯 Area Prioritas")
                
                top_3_provinces = df_filtered.groupby('nama_provinsi')['jumlah_kasus'].sum().nlargest(3)
                st.write("**Top 3 Provinsi yang Memerlukan Perhatian:**")
                for i, (prov, kasus) in enumerate(top_3_provinces.items(), 1):
                    st.write(f"{i}. {prov}: **{kasus:,.0f} kasus**")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Rekomendasi umum
            st.markdown("---")
            st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
            st.markdown("### 💊 Rekomendasi Mitigasi Umum")
            st.markdown("""
            1. **Fokus Intervensi**: Prioritaskan wilayah dengan kasus tertinggi untuk program fogging dan 3M Plus
            2. **Surveilans Ketat**: Tingkatkan monitoring di area dengan tren peningkatan signifikan
            3. **Edukasi Masyarakat**: Kampanye pencegahan DBD terutama menjelang musim hujan
            4. **Koordinasi Lintas Sektor**: Libatkan puskesmas, kelurahan, dan masyarakat
            5. **Early Warning System**: Implementasi sistem deteksi dini berbasis data
            6. **Manajemen Lingkungan**: Program kebersihan lingkungan berkelanjutan
            7. **Preparedness**: Stok obat dan alat kesehatan yang memadai
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
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
        st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>Dashboard DBD Indonesia | Powered by Streamlit & Claude AI (Sonnet 4.0)</p>
        <p style='font-size: 0.9rem;'>Dibuat untuk analisis dan monitoring kasus Demam Berdarah Dengue di Indonesia</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

