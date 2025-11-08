"""
Utility Functions untuk Visualisasi Data DBD
Menggunakan Plotly, Matplotlib, dan Seaborn
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional, Tuple
import warnings

warnings.filterwarnings('ignore')

# Set style untuk matplotlib
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class DBDVisualizer:
    """
    Class untuk membuat berbagai visualisasi data DBD
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Inisialisasi visualizer dengan dataframe
        
        Args:
            df: DataFrame dengan data DBD
        """
        self.df = df
        self.color_palette = px.colors.qualitative.Set3
    
    # ========== PLOTLY VISUALIZATIONS ==========
    
    def create_bar_trend(
        self,
        provinces: Optional[List[str]] = None,
        title: str = "Trend Kasus DBD per Tahun"
    ) -> go.Figure:
        """
        Membuat bar chart trend kasus per tahun
        
        Args:
            provinces: List nama provinsi (None untuk semua)
            title: Judul grafik
            
        Returns:
            Plotly Figure object
        """
        if provinces:
            df_filtered = self.df[self.df['nama_provinsi'].isin(provinces)]
        else:
            df_filtered = self.df
        
        trend_data = df_filtered.groupby(['tahun', 'nama_provinsi'])['jumlah_kasus'].sum().reset_index()
        
        fig = px.bar(
            trend_data,
            x='tahun',
            y='jumlah_kasus',
            color='nama_provinsi',
            title=title,
            labels={
                'jumlah_kasus': 'Jumlah Kasus',
                'tahun': 'Tahun',
                'nama_provinsi': 'Provinsi'
            },
            barmode='group',
            height=600
        )
        
        fig.update_layout(
            xaxis=dict(tickmode='linear', dtick=1),
            hovermode='x unified',
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            ),
            font=dict(size=12)
        )
        
        return fig
    
    def create_line_trend(
        self,
        groupby: str = 'nama_provinsi',
        title: str = "Trend Line Kasus DBD"
    ) -> go.Figure:
        """
        Membuat line chart trend kasus
        
        Args:
            groupby: Kolom untuk grouping
            title: Judul grafik
            
        Returns:
            Plotly Figure object
        """
        trend_data = self.df.groupby(['tahun', groupby])['jumlah_kasus'].sum().reset_index()
        
        fig = px.line(
            trend_data,
            x='tahun',
            y='jumlah_kasus',
            color=groupby,
            title=title,
            labels={
                'jumlah_kasus': 'Jumlah Kasus',
                'tahun': 'Tahun'
            },
            markers=True,
            height=600
        )
        
        fig.update_traces(line=dict(width=3))
        fig.update_layout(
            xaxis=dict(tickmode='linear', dtick=1),
            hovermode='x unified',
            font=dict(size=12)
        )
        
        return fig
    
    def create_heatmap(
        self,
        province: Optional[str] = None,
        top_n: int = 15,
        title: str = "Heatmap Kasus DBD"
    ) -> go.Figure:
        """
        Membuat heatmap kasus per kabupaten/kota per tahun
        
        Args:
            province: Nama provinsi (None untuk top N kabupaten)
            top_n: Jumlah kabupaten teratas jika province=None
            title: Judul grafik
            
        Returns:
            Plotly Figure object
        """
        if province:
            df_filtered = self.df[self.df['nama_provinsi'] == province]
            title = f"{title} - {province}"
        else:
            top_kabkot = self.df.groupby('nama_kabupaten_kota')['jumlah_kasus'].sum().nlargest(top_n).index
            df_filtered = self.df[self.df['nama_kabupaten_kota'].isin(top_kabkot)]
            title = f"{title} (Top {top_n})"
        
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
            title=title,
            aspect="auto",
            color_continuous_scale="Reds",
            height=max(600, len(heatmap_data) * 30)
        )
        
        fig.update_xaxes(side="bottom")
        fig.update_layout(font=dict(size=11))
        
        return fig
    
    def create_pie_chart(
        self,
        groupby: str = 'nama_provinsi',
        title: str = "Distribusi Kasus DBD",
        top_n: int = 10
    ) -> go.Figure:
        """
        Membuat pie chart distribusi kasus
        
        Args:
            groupby: Kolom untuk grouping
            title: Judul grafik
            top_n: Jumlah kategori teratas
            
        Returns:
            Plotly Figure object
        """
        dist_data = self.df.groupby(groupby)['jumlah_kasus'].sum().nlargest(top_n).reset_index()
        
        fig = px.pie(
            dist_data,
            values='jumlah_kasus',
            names=groupby,
            title=f"{title} (Top {top_n})",
            height=600
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Kasus: %{value:,.0f}<br>Persentase: %{percent}<extra></extra>'
        )
        
        return fig
    
    def create_box_plot(
        self,
        groupby: str = 'nama_provinsi',
        title: str = "Distribusi Kasus DBD"
    ) -> go.Figure:
        """
        Membuat box plot untuk melihat distribusi dan outlier
        
        Args:
            groupby: Kolom untuk grouping
            title: Judul grafik
            
        Returns:
            Plotly Figure object
        """
        fig = px.box(
            self.df,
            x=groupby,
            y='jumlah_kasus',
            title=title,
            labels={'jumlah_kasus': 'Jumlah Kasus'},
            height=600
        )
        
        fig.update_xaxes(tickangle=-45)
        fig.update_layout(showlegend=False)
        
        return fig
    
    def create_treemap(
        self,
        title: str = "Treemap Kasus DBD"
    ) -> go.Figure:
        """
        Membuat treemap hierarki provinsi-kabupaten
        
        Args:
            title: Judul grafik
            
        Returns:
            Plotly Figure object
        """
        treemap_data = self.df.groupby(
            ['nama_provinsi', 'nama_kabupaten_kota']
        )['jumlah_kasus'].sum().reset_index()
        
        fig = px.treemap(
            treemap_data,
            path=['nama_provinsi', 'nama_kabupaten_kota'],
            values='jumlah_kasus',
            title=title,
            height=700
        )
        
        fig.update_traces(
            textinfo="label+value+percent parent",
            hovertemplate='<b>%{label}</b><br>Kasus: %{value:,.0f}<br>%{percentParent}<extra></extra>'
        )
        
        return fig
    
    def create_comparison_chart(
        self,
        years: List[int],
        title: str = "Perbandingan Kasus Antar Tahun"
    ) -> go.Figure:
        """
        Membuat chart perbandingan antar tahun
        
        Args:
            years: List tahun yang ingin dibandingkan
            title: Judul grafik
            
        Returns:
            Plotly Figure object
        """
        df_filtered = self.df[self.df['tahun'].isin(years)]
        comparison_data = df_filtered.groupby(
            ['nama_provinsi', 'tahun']
        )['jumlah_kasus'].sum().reset_index()
        
        fig = go.Figure()
        
        for year in years:
            year_data = comparison_data[comparison_data['tahun'] == year]
            fig.add_trace(go.Bar(
                name=str(year),
                x=year_data['nama_provinsi'],
                y=year_data['jumlah_kasus'],
                text=year_data['jumlah_kasus'],
                textposition='outside'
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Provinsi",
            yaxis_title="Jumlah Kasus",
            barmode='group',
            height=600,
            xaxis_tickangle=-45
        )
        
        return fig
    
    # ========== MATPLOTLIB/SEABORN VISUALIZATIONS ==========
    
    def create_matplotlib_trend(
        self,
        figsize: Tuple[int, int] = (14, 8),
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Membuat trend chart dengan matplotlib
        
        Args:
            figsize: Ukuran figure
            save_path: Path untuk menyimpan gambar
            
        Returns:
            Matplotlib Figure object
        """
        trend_data = self.df.groupby(['tahun', 'nama_provinsi'])['jumlah_kasus'].sum().reset_index()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        for province in trend_data['nama_provinsi'].unique():
            prov_data = trend_data[trend_data['nama_provinsi'] == province]
            ax.plot(
                prov_data['tahun'],
                prov_data['jumlah_kasus'],
                marker='o',
                linewidth=2,
                label=province
            )
        
        ax.set_xlabel('Tahun', fontsize=12, fontweight='bold')
        ax.set_ylabel('Jumlah Kasus', fontsize=12, fontweight='bold')
        ax.set_title('Trend Kasus DBD per Tahun per Provinsi', fontsize=14, fontweight='bold')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_seaborn_heatmap(
        self,
        province: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 10),
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Membuat heatmap dengan seaborn
        
        Args:
            province: Nama provinsi
            figsize: Ukuran figure
            save_path: Path untuk menyimpan gambar
            
        Returns:
            Matplotlib Figure object
        """
        if province:
            df_filtered = self.df[self.df['nama_provinsi'] == province]
        else:
            top_kabkot = self.df.groupby('nama_kabupaten_kota')['jumlah_kasus'].sum().nlargest(15).index
            df_filtered = self.df[self.df['nama_kabupaten_kota'].isin(top_kabkot)]
        
        heatmap_data = df_filtered.pivot_table(
            values='jumlah_kasus',
            index='nama_kabupaten_kota',
            columns='tahun',
            aggfunc='sum',
            fill_value=0
        )
        
        fig, ax = plt.subplots(figsize=figsize)
        
        sns.heatmap(
            heatmap_data,
            annot=True,
            fmt='.0f',
            cmap='Reds',
            linewidths=0.5,
            cbar_kws={'label': 'Jumlah Kasus'},
            ax=ax
        )
        
        title = f"Heatmap Kasus DBD - {province}" if province else "Heatmap Kasus DBD (Top 15)"
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Tahun', fontsize=12, fontweight='bold')
        ax.set_ylabel('Kabupaten/Kota', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_correlation_matrix(
        self,
        figsize: Tuple[int, int] = (10, 8),
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Membuat correlation matrix
        
        Args:
            figsize: Ukuran figure
            save_path: Path untuk menyimpan gambar
            
        Returns:
            Matplotlib Figure object
        """
        # Pivot data untuk correlation
        pivot_data = self.df.pivot_table(
            values='jumlah_kasus',
            index='nama_provinsi',
            columns='tahun',
            aggfunc='sum'
        )
        
        # Hitung correlation
        corr_matrix = pivot_data.corr()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        sns.heatmap(
            corr_matrix,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={'label': 'Correlation'},
            ax=ax
        )
        
        ax.set_title('Correlation Matrix Kasus DBD Antar Tahun', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def create_dashboard_summary(
        self,
        year: int,
        figsize: Tuple[int, int] = (16, 12),
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Membuat dashboard summary dengan multiple plots
        
        Args:
            year: Tahun untuk analisis
            figsize: Ukuran figure
            save_path: Path untuk menyimpan gambar
            
        Returns:
            Matplotlib Figure object
        """
        df_year = self.df[self.df['tahun'] == year]
        
        fig = plt.figure(figsize=figsize)
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # Plot 1: Top 10 Provinsi
        ax1 = fig.add_subplot(gs[0, 0])
        top_provinces = df_year.groupby('nama_provinsi')['jumlah_kasus'].sum().nlargest(10)
        top_provinces.plot(kind='barh', ax=ax1, color='steelblue')
        ax1.set_title(f'Top 10 Provinsi - {year}', fontweight='bold')
        ax1.set_xlabel('Jumlah Kasus')
        
        # Plot 2: Distribusi kasus
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.hist(df_year['jumlah_kasus'], bins=30, color='coral', edgecolor='black')
        ax2.set_title(f'Distribusi Kasus - {year}', fontweight='bold')
        ax2.set_xlabel('Jumlah Kasus')
        ax2.set_ylabel('Frekuensi')
        
        # Plot 3: Top 10 Kabupaten/Kota
        ax3 = fig.add_subplot(gs[1, :])
        top_kabkot = df_year.groupby('nama_kabupaten_kota')['jumlah_kasus'].sum().nlargest(10)
        top_kabkot.plot(kind='bar', ax=ax3, color='lightgreen', edgecolor='black')
        ax3.set_title(f'Top 10 Kabupaten/Kota - {year}', fontweight='bold')
        ax3.set_xlabel('Kabupaten/Kota')
        ax3.set_ylabel('Jumlah Kasus')
        ax3.tick_params(axis='x', rotation=45)
        
        # Plot 4: Pie chart provinsi
        ax4 = fig.add_subplot(gs[2, :])
        province_dist = df_year.groupby('nama_provinsi')['jumlah_kasus'].sum().nlargest(8)
        ax4.pie(
            province_dist.values,
            labels=province_dist.index,
            autopct='%1.1f%%',
            startangle=90
        )
        ax4.set_title(f'Distribusi Kasus per Provinsi (Top 8) - {year}', fontweight='bold')
        
        fig.suptitle(f'Dashboard Summary DBD Indonesia - {year}', fontsize=16, fontweight='bold', y=0.995)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig


# Contoh penggunaan
if __name__ == "__main__":
    # Load sample data
    import sys
    sys.path.append('.')
    from utils_parsing import DBDDataParser
    
    parser = DBDDataParser("data_dbd_sample.csv")
    df = parser.load_csv()
    df_clean = parser.clean_data()
    
    # Inisialisasi visualizer
    viz = DBDVisualizer(df_clean)
    
    print("=" * 50)
    print("CONTOH VISUALISASI")
    print("=" * 50)
    
    # Contoh 1: Bar trend dengan Plotly
    print("\n1. Membuat bar trend chart...")
    fig1 = viz.create_bar_trend(title="Trend Kasus DBD per Tahun per Provinsi")
    # fig1.show()  # Uncomment untuk menampilkan
    print("✓ Bar trend chart created")
    
    # Contoh 2: Line trend
    print("\n2. Membuat line trend chart...")
    fig2 = viz.create_line_trend(title="Trend Line Kasus DBD per Provinsi")
    print("✓ Line trend chart created")
    
    # Contoh 3: Heatmap
    print("\n3. Membuat heatmap...")
    fig3 = viz.create_heatmap(top_n=10, title="Heatmap Top 10 Kabupaten/Kota")
    print("✓ Heatmap created")
    
    # Contoh 4: Pie chart
    print("\n4. Membuat pie chart...")
    fig4 = viz.create_pie_chart(top_n=8)
    print("✓ Pie chart created")
    
    # Contoh 5: Treemap
    print("\n5. Membuat treemap...")
    fig5 = viz.create_treemap()
    print("✓ Treemap created")
    
    # Contoh 6: Matplotlib trend
    print("\n6. Membuat matplotlib trend...")
    fig6 = viz.create_matplotlib_trend(save_path="trend_matplotlib.png")
    print("✓ Matplotlib trend saved to trend_matplotlib.png")
    plt.close(fig6)
    
    # Contoh 7: Seaborn heatmap
    print("\n7. Membuat seaborn heatmap...")
    fig7 = viz.create_seaborn_heatmap(save_path="heatmap_seaborn.png")
    print("✓ Seaborn heatmap saved to heatmap_seaborn.png")
    plt.close(fig7)
    
    # Contoh 8: Dashboard summary
    print("\n8. Membuat dashboard summary...")
    fig8 = viz.create_dashboard_summary(year=2023, save_path="dashboard_summary_2023.png")
    print("✓ Dashboard summary saved to dashboard_summary_2023.png")
    plt.close(fig8)
    
    print("\n" + "=" * 50)
    print("SEMUA VISUALISASI BERHASIL DIBUAT!")
    print("=" * 50)

