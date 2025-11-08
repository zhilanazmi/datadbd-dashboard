"""
Utility Functions untuk Integrasi dengan Claude AI (Sonnet 4.0)
Untuk Business Intelligence dan Analisis Data DBD
"""

import pandas as pd
from anthropic import Anthropic
import json
from typing import Dict, List, Optional, Tuple
import os
from datetime import datetime


class ClaudeDBDAnalyzer:
    """
    Class untuk analisis data DBD menggunakan Claude AI
    """
    
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        """
        Inisialisasi analyzer dengan API key
        
        Args:
            api_key: Anthropic API key
            model: Model Claude yang digunakan
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.conversation_history = []
    
    def prepare_data_summary(self, df: pd.DataFrame) -> Dict:
        """
        Prepare data summary untuk analisis AI
        
        Args:
            df: DataFrame dengan data DBD
            
        Returns:
            Dictionary berisi summary data
        """
        # Basic statistics
        total_kasus = int(df['jumlah_kasus'].sum())
        rata_rata = float(df['jumlah_kasus'].mean())
        
        # Temporal analysis
        tahun_list = sorted(df['tahun'].unique().tolist())
        trend_tahunan = df.groupby('tahun')['jumlah_kasus'].sum().to_dict()
        trend_tahunan = {int(k): int(v) for k, v in trend_tahunan.items()}
        
        # Geographic analysis
        top_provinsi = df.groupby('nama_provinsi')['jumlah_kasus'].sum().nlargest(10).to_dict()
        top_provinsi = {k: int(v) for k, v in top_provinsi.items()}
        
        top_kabkot = df.groupby(['nama_provinsi', 'nama_kabupaten_kota'])['jumlah_kasus'].sum().nlargest(10)
        top_kabkot_dict = {f"{k[0]} - {k[1]}": int(v) for k, v in top_kabkot.items()}
        
        # Growth rate analysis
        if len(tahun_list) > 1:
            tahun_awal = tahun_list[0]
            tahun_akhir = tahun_list[-1]
            kasus_awal = trend_tahunan[tahun_awal]
            kasus_akhir = trend_tahunan[tahun_akhir]
            growth_rate = ((kasus_akhir - kasus_awal) / kasus_awal * 100) if kasus_awal > 0 else 0
        else:
            growth_rate = 0
        
        # Province-level growth
        provinsi_growth = {}
        for prov in df['nama_provinsi'].unique():
            prov_data = df[df['nama_provinsi'] == prov].groupby('tahun')['jumlah_kasus'].sum()
            if len(prov_data) > 1:
                pct_change = ((prov_data.iloc[-1] - prov_data.iloc[0]) / prov_data.iloc[0] * 100) if prov_data.iloc[0] > 0 else 0
                provinsi_growth[prov] = float(pct_change)
        
        # Top growing provinces
        top_growing = dict(sorted(provinsi_growth.items(), key=lambda x: x[1], reverse=True)[:5])
        
        summary = {
            'statistik_dasar': {
                'total_kasus': total_kasus,
                'rata_rata_kasus': round(rata_rata, 2),
                'jumlah_provinsi': df['nama_provinsi'].nunique(),
                'jumlah_kabkot': df['nama_kabupaten_kota'].nunique(),
                'periode': f"{tahun_list[0]} - {tahun_list[-1]}",
                'growth_rate_nasional': round(growth_rate, 2)
            },
            'trend_tahunan': trend_tahunan,
            'top_10_provinsi': top_provinsi,
            'top_10_kabupaten_kota': top_kabkot_dict,
            'provinsi_pertumbuhan_tertinggi': top_growing
        }
        
        return summary
    
    def generate_comprehensive_insights(
        self,
        df: pd.DataFrame,
        focus_areas: Optional[List[str]] = None
    ) -> str:
        """
        Generate comprehensive insights dari data DBD
        
        Args:
            df: DataFrame dengan data DBD
            focus_areas: Area fokus analisis (opsional)
            
        Returns:
            String berisi insights dari Claude AI
        """
        summary = self.prepare_data_summary(df)
        
        focus_text = ""
        if focus_areas:
            focus_text = f"\n\nBerikan perhatian khusus pada aspek: {', '.join(focus_areas)}"
        
        prompt = f"""
Sebagai ahli epidemiologi dan data scientist, analisis data Demam Berdarah Dengue (DBD) Indonesia berikut:

DATA SUMMARY:
{json.dumps(summary, indent=2, ensure_ascii=False)}

{focus_text}

Berikan analisis mendalam dalam format berikut:

## 1. EXECUTIVE SUMMARY
Ringkasan singkat situasi DBD di Indonesia berdasarkan data.

## 2. ANALISIS TREN NASIONAL
- Pola perkembangan kasus dari tahun ke tahun
- Identifikasi periode kritis (peningkatan signifikan)
- Perbandingan growth rate dengan standar epidemiologi

## 3. ANALISIS REGIONAL
- Provinsi dengan kasus tertinggi dan alasannya
- Hotspot area yang memerlukan perhatian khusus
- Pola geografis penyebaran
- Perbandingan antar wilayah

## 4. ANALISIS PERTUMBUHAN
- Provinsi dengan pertumbuhan kasus tertinggi
- Identifikasi wilayah dengan tren menurun (best practices)
- Faktor-faktor yang mungkin mempengaruhi

## 5. REKOMENDASI MITIGASI PRIORITAS
Berikan 7-10 rekomendasi konkret dan actionable:
- Berdasarkan data aktual
- Spesifik untuk wilayah tertentu jika perlu
- Dapat diimplementasikan oleh Dinas Kesehatan
- Prioritas dari yang paling urgent

## 6. EARLY WARNING & PREDIKSI
- Wilayah yang perlu diwaspadai
- Indikator potensi outbreak
- Rekomendasi surveillance

## 7. KEY INSIGHTS
Poin-poin penting yang harus diketahui stakeholder.

Gunakan data konkret, berikan angka spesifik, dan pastikan rekomendasi praktis dan implementable.
"""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            insights = message.content[0].text
            
            # Save to history
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'comprehensive_insights',
                'prompt': prompt,
                'response': insights
            })
            
            return insights
        
        except Exception as e:
            return f"Error saat generate insights: {str(e)}"
    
    def generate_mitigation_recommendations(
        self,
        df: pd.DataFrame,
        target_province: Optional[str] = None
    ) -> str:
        """
        Generate rekomendasi mitigasi spesifik
        
        Args:
            df: DataFrame dengan data DBD
            target_province: Provinsi target (None untuk nasional)
            
        Returns:
            String berisi rekomendasi
        """
        if target_province:
            df_filtered = df[df['nama_provinsi'] == target_province]
            scope = f"provinsi {target_province}"
        else:
            df_filtered = df
            scope = "nasional"
        
        summary = self.prepare_data_summary(df_filtered)
        
        prompt = f"""
Sebagai konsultan kesehatan masyarakat, buatkan rekomendasi mitigasi DBD untuk {scope}.

DATA:
{json.dumps(summary, indent=2, ensure_ascii=False)}

Buatkan rekomendasi dalam format berikut:

## REKOMENDASI MITIGASI DBD - {scope.upper()}

### 1. INTERVENSI JANGKA PENDEK (1-3 bulan)
- Tindakan segera yang perlu dilakukan
- Program yang dapat dimulai dengan cepat
- Target area prioritas

### 2. PROGRAM JANGKA MENENGAH (3-12 bulan)
- Program berkelanjutan
- Kampanye edukasi
- Pemberdayaan masyarakat

### 3. STRATEGI JANGKA PANJANG (1-3 tahun)
- Perubahan sistemik
- Infrastruktur kesehatan
- Kebijakan preventif

### 4. ALOKASI SUMBER DAYA
- Prioritas anggaran
- Distribusi tenaga kesehatan
- Kebutuhan logistik

### 5. KEY PERFORMANCE INDICATORS (KPI)
- Metrik untuk mengukur keberhasilan
- Target yang realistis
- Timeline pencapaian

### 6. STAKEHOLDER & KOORDINASI
- Pihak-pihak yang perlu dilibatkan
- Mekanisme koordinasi
- Pembagian tanggung jawab

Berikan rekomendasi yang spesifik, terukur, achievable, relevant, dan time-bound (SMART).
"""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=3072,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            recommendations = message.content[0].text
            
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'mitigation_recommendations',
                'scope': scope,
                'response': recommendations
            })
            
            return recommendations
        
        except Exception as e:
            return f"Error saat generate rekomendasi: {str(e)}"
    
    def analyze_specific_area(
        self,
        df: pd.DataFrame,
        province: str,
        kabkot: Optional[str] = None
    ) -> str:
        """
        Analisis mendalam untuk wilayah spesifik
        
        Args:
            df: DataFrame dengan data DBD
            province: Nama provinsi
            kabkot: Nama kabupaten/kota (opsional)
            
        Returns:
            String berisi analisis
        """
        if kabkot:
            df_area = df[
                (df['nama_provinsi'] == province) &
                (df['nama_kabupaten_kota'] == kabkot)
            ]
            area_name = f"{kabkot}, {province}"
        else:
            df_area = df[df['nama_provinsi'] == province]
            area_name = province
        
        if df_area.empty:
            return f"Data tidak ditemukan untuk {area_name}"
        
        # Analisis area
        trend = df_area.groupby('tahun')['jumlah_kasus'].sum().to_dict()
        total = df_area['jumlah_kasus'].sum()
        rata_rata = df_area['jumlah_kasus'].mean()
        
        # Perbandingan dengan nasional
        df_nasional = df.groupby('tahun')['jumlah_kasus'].sum()
        df_area_by_year = df_area.groupby('tahun')['jumlah_kasus'].sum()
        
        kontribusi = {}
        for year in df_area_by_year.index:
            if year in df_nasional.index:
                pct = (df_area_by_year[year] / df_nasional[year] * 100)
                kontribusi[int(year)] = round(float(pct), 2)
        
        prompt = f"""
Analisis mendalam kasus DBD di {area_name}:

DATA WILAYAH:
- Total Kasus: {int(total)}
- Rata-rata Kasus per Periode: {round(rata_rata, 2)}
- Trend Tahunan: {trend}
- Kontribusi terhadap Kasus Nasional: {kontribusi}

Berikan analisis:

## PROFIL WILAYAH
Karakteristik dan situasi DBD di {area_name}

## ANALISIS TREND
- Pola perkembangan kasus
- Periode kritis
- Perbandingan dengan wilayah lain

## FAKTOR RISIKO POTENSIAL
- Faktor geografis
- Faktor demografis
- Faktor lingkungan
- Faktor sosial-ekonomi

## ROOT CAUSE ANALYSIS
Mengapa wilayah ini memiliki kasus dengan pola seperti ini?

## REKOMENDASI SPESIFIK
5-7 rekomendasi khusus untuk {area_name}

## BEST PRACTICES
Pembelajaran yang bisa diambil atau diterapkan

Berikan analisis yang kontekstual dan actionable.
"""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2560,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            analysis = message.content[0].text
            
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'area_analysis',
                'area': area_name,
                'response': analysis
            })
            
            return analysis
        
        except Exception as e:
            return f"Error saat analisis: {str(e)}"
    
    def compare_time_periods(
        self,
        df: pd.DataFrame,
        year1: int,
        year2: int
    ) -> str:
        """
        Bandingkan dua periode waktu
        
        Args:
            df: DataFrame dengan data DBD
            year1: Tahun pertama
            year2: Tahun kedua
            
        Returns:
            String berisi perbandingan
        """
        df_year1 = df[df['tahun'] == year1]
        df_year2 = df[df['tahun'] == year2]
        
        data_comparison = {
            'tahun_1': {
                'tahun': year1,
                'total_kasus': int(df_year1['jumlah_kasus'].sum()),
                'top_5_provinsi': df_year1.groupby('nama_provinsi')['jumlah_kasus'].sum().nlargest(5).to_dict()
            },
            'tahun_2': {
                'tahun': year2,
                'total_kasus': int(df_year2['jumlah_kasus'].sum()),
                'top_5_provinsi': df_year2.groupby('nama_provinsi')['jumlah_kasus'].sum().nlargest(5).to_dict()
            }
        }
        
        # Calculate changes
        pct_change = ((data_comparison['tahun_2']['total_kasus'] - 
                      data_comparison['tahun_1']['total_kasus']) / 
                     data_comparison['tahun_1']['total_kasus'] * 100)
        
        prompt = f"""
Bandingkan situasi DBD Indonesia antara tahun {year1} dan {year2}:

DATA PERBANDINGAN:
{json.dumps(data_comparison, indent=2, ensure_ascii=False)}

Perubahan Total Kasus: {pct_change:.2f}%

Berikan analisis perbandingan:

## PERUBAHAN NASIONAL
- Tren umum (naik/turun)
- Magnitude perubahan
- Signifikansi perubahan

## PERUBAHAN REGIONAL
- Provinsi dengan peningkatan terbesar
- Provinsi dengan penurunan terbesar
- Pergeseran hotspot

## ANALISIS FAKTOR
Kemungkinan faktor yang mempengaruhi perubahan:
- Program intervensi yang mungkin berhasil/gagal
- Faktor eksternal (cuaca, kebijakan, dll)
- Perubahan surveillance

## LESSONS LEARNED
- Apa yang berhasil?
- Apa yang perlu diperbaiki?
- Best practices yang teridentifikasi

## PROYEKSI & REKOMENDASI
Berdasarkan perbandingan ini, apa yang harus dilakukan ke depan?

Berikan insight yang data-driven dan actionable.
"""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2560,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            comparison = message.content[0].text
            
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'time_comparison',
                'years': f"{year1} vs {year2}",
                'response': comparison
            })
            
            return comparison
        
        except Exception as e:
            return f"Error saat perbandingan: {str(e)}"
    
    def generate_executive_report(
        self,
        df: pd.DataFrame,
        target_audience: str = "Direktur Jenderal Pencegahan dan Pengendalian Penyakit"
    ) -> str:
        """
        Generate executive report untuk stakeholder
        
        Args:
            df: DataFrame dengan data DBD
            target_audience: Target pembaca report
            
        Returns:
            String berisi executive report
        """
        summary = self.prepare_data_summary(df)
        
        prompt = f"""
Buatkan Executive Report untuk {target_audience} tentang situasi DBD Indonesia.

DATA:
{json.dumps(summary, indent=2, ensure_ascii=False)}

Format Report:

# EXECUTIVE REPORT: SITUASI DBD INDONESIA
**Untuk: {target_audience}**
**Tanggal: {datetime.now().strftime('%d %B %Y')}**

---

## EXECUTIVE SUMMARY
Ringkasan 2-3 paragraf untuk decision maker yang sibuk.

## HIGHLIGHTS
- 3-5 poin paling penting yang harus diketahui
- Gunakan bullet points yang impactful

## SITUASI TERKINI
### Gambaran Nasional
- Status kasus saat ini
- Perbandingan dengan periode sebelumnya

### Area Kritis
- Wilayah yang memerlukan perhatian urgent
- Level of concern (High/Medium/Low)

## TREN & PROYEKSI
- Kemana arah perkembangan kasus?
- Potensi risiko di masa depan

## REKOMENDASI STRATEGIS
### Tindakan Immediate (0-1 bulan)
1. ...
2. ...
3. ...

### Tindakan Strategic (1-6 bulan)
1. ...
2. ...
3. ...

## KEBUTUHAN SUMBER DAYA
- Budget requirement
- Human resources
- Infrastructure

## RISK ASSESSMENT
- Potential risks
- Mitigation strategies

## KESIMPULAN
Key takeaways untuk decision making.

---

Buat report yang concise, data-driven, dan actionable. Hindari jargon teknis yang tidak perlu.
"""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=3584,
                temperature=0.5,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            report = message.content[0].text
            
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'executive_report',
                'audience': target_audience,
                'response': report
            })
            
            return report
        
        except Exception as e:
            return f"Error saat generate report: {str(e)}"
    
    def save_conversation_history(self, file_path: str = "ai_analysis_history.json"):
        """
        Simpan conversation history ke file
        
        Args:
            file_path: Path file untuk menyimpan history
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
            print(f"Conversation history saved to {file_path}")
        except Exception as e:
            print(f"Error saving history: {str(e)}")


# Contoh penggunaan
if __name__ == "__main__":
    # Setup
    api_key = os.getenv('ANTHROPIC_API_KEY', 'your-api-key-here')
    
    if api_key == 'your-api-key-here':
        print("⚠️  Set ANTHROPIC_API_KEY di environment variable atau ganti 'your-api-key-here'")
        print("    Contoh: export ANTHROPIC_API_KEY='sk-ant-...'")
        exit(1)
    
    # Load data
    print("Loading data...")
    from utils_parsing import DBDDataParser
    
    parser = DBDDataParser("data_dbd_sample.csv")
    df = parser.load_csv()
    df_clean = parser.clean_data()
    
    # Inisialisasi AI analyzer
    print("\nInisialisasi Claude AI Analyzer...")
    analyzer = ClaudeDBDAnalyzer(api_key=api_key)
    
    # Contoh 1: Comprehensive Insights
    print("\n" + "=" * 70)
    print("CONTOH 1: COMPREHENSIVE INSIGHTS")
    print("=" * 70)
    
    insights = analyzer.generate_comprehensive_insights(
        df_clean,
        focus_areas=['Tren Peningkatan', 'Hotspot Area']
    )
    print(insights)
    
    # Contoh 2: Mitigation Recommendations
    print("\n" + "=" * 70)
    print("CONTOH 2: REKOMENDASI MITIGASI")
    print("=" * 70)
    
    recommendations = analyzer.generate_mitigation_recommendations(df_clean)
    print(recommendations)
    
    # Contoh 3: Area-specific Analysis
    print("\n" + "=" * 70)
    print("CONTOH 3: ANALISIS WILAYAH SPESIFIK")
    print("=" * 70)
    
    area_analysis = analyzer.analyze_specific_area(
        df_clean,
        province='DKI Jakarta'
    )
    print(area_analysis)
    
    # Contoh 4: Time Period Comparison
    print("\n" + "=" * 70)
    print("CONTOH 4: PERBANDINGAN PERIODE")
    print("=" * 70)
    
    comparison = analyzer.compare_time_periods(df_clean, 2020, 2023)
    print(comparison)
    
    # Contoh 5: Executive Report
    print("\n" + "=" * 70)
    print("CONTOH 5: EXECUTIVE REPORT")
    print("=" * 70)
    
    exec_report = analyzer.generate_executive_report(df_clean)
    print(exec_report)
    
    # Save history
    print("\n" + "=" * 70)
    print("Menyimpan conversation history...")
    analyzer.save_conversation_history()
    print("✓ History tersimpan")
    
    print("\n" + "=" * 70)
    print("SEMUA CONTOH SELESAI!")
    print("=" * 70)

