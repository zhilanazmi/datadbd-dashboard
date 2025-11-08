"""
Utility Functions untuk Parsing dan Validasi Data CSV DBD
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DBDDataParser:
    """
    Class untuk parsing dan validasi data DBD dari CSV
    """
    
    REQUIRED_COLUMNS = [
        'kode_provinsi',
        'nama_provinsi',
        'kode_kabupaten_kota',
        'nama_kabupaten_kota',
        'jumlah_kasus',
        'satuan',
        'tahun'
    ]
    
    def __init__(self, file_path: str):
        """
        Inisialisasi parser dengan file path
        
        Args:
            file_path: Path ke file CSV
        """
        self.file_path = file_path
        self.df = None
        self.validation_errors = []
    
    def load_csv(self, encoding: str = 'utf-8', delimiter: str = ',') -> pd.DataFrame:
        """
        Load data dari CSV file
        
        Args:
            encoding: Encoding file (default: utf-8)
            delimiter: Delimiter CSV (default: ,)
            
        Returns:
            DataFrame pandas
        """
        try:
            self.df = pd.read_csv(
                self.file_path,
                encoding=encoding,
                delimiter=delimiter
            )
            logger.info(f"Berhasil load {len(self.df)} baris data dari {self.file_path}")
            return self.df
        
        except FileNotFoundError:
            logger.error(f"File tidak ditemukan: {self.file_path}")
            raise
        
        except Exception as e:
            logger.error(f"Error saat membaca CSV: {str(e)}")
            raise
    
    def validate_structure(self) -> Tuple[bool, List[str]]:
        """
        Validasi struktur data CSV
        
        Returns:
            Tuple (is_valid, error_messages)
        """
        if self.df is None:
            return False, ["Data belum di-load"]
        
        errors = []
        
        # Cek kolom yang diperlukan
        missing_columns = set(self.REQUIRED_COLUMNS) - set(self.df.columns)
        if missing_columns:
            errors.append(f"Kolom berikut tidak ditemukan: {', '.join(missing_columns)}")
        
        # Cek data kosong
        if self.df.empty:
            errors.append("Data kosong")
        
        # Cek duplikat
        duplicate_count = self.df.duplicated().sum()
        if duplicate_count > 0:
            errors.append(f"Ditemukan {duplicate_count} baris duplikat")
        
        self.validation_errors = errors
        return len(errors) == 0, errors
    
    def validate_data_types(self) -> Tuple[bool, List[str]]:
        """
        Validasi tipe data kolom
        
        Returns:
            Tuple (is_valid, error_messages)
        """
        if self.df is None:
            return False, ["Data belum di-load"]
        
        errors = []
        
        # Validasi kode_provinsi (harus numerik)
        if not pd.api.types.is_numeric_dtype(self.df['kode_provinsi']):
            errors.append("kode_provinsi harus bertipe numerik")
        
        # Validasi jumlah_kasus (harus numerik)
        if not pd.api.types.is_numeric_dtype(self.df['jumlah_kasus']):
            try:
                self.df['jumlah_kasus'] = pd.to_numeric(self.df['jumlah_kasus'], errors='coerce')
            except:
                errors.append("jumlah_kasus harus bertipe numerik")
        
        # Validasi tahun (harus numerik dan dalam range wajar)
        if not pd.api.types.is_numeric_dtype(self.df['tahun']):
            try:
                self.df['tahun'] = pd.to_numeric(self.df['tahun'], errors='coerce')
            except:
                errors.append("tahun harus bertipe numerik")
        else:
            if self.df['tahun'].max() > 2100 or self.df['tahun'].min() < 2000:
                errors.append("tahun harus dalam range 2000-2100")
        
        # Cek nilai null pada kolom penting
        null_counts = self.df[self.REQUIRED_COLUMNS].isnull().sum()
        for col, count in null_counts[null_counts > 0].items():
            errors.append(f"Kolom {col} memiliki {count} nilai null")
        
        return len(errors) == 0, errors
    
    def validate_business_rules(self) -> Tuple[bool, List[str]]:
        """
        Validasi business rules
        
        Returns:
            Tuple (is_valid, warnings)
        """
        if self.df is None:
            return False, ["Data belum di-load"]
        
        warnings = []
        
        # Cek jumlah kasus negatif
        negative_cases = (self.df['jumlah_kasus'] < 0).sum()
        if negative_cases > 0:
            warnings.append(f"Ditemukan {negative_cases} baris dengan jumlah kasus negatif")
        
        # Cek jumlah kasus sangat tinggi (outlier)
        threshold = self.df['jumlah_kasus'].quantile(0.99)
        high_cases = (self.df['jumlah_kasus'] > threshold * 2).sum()
        if high_cases > 0:
            warnings.append(f"Ditemukan {high_cases} baris dengan jumlah kasus sangat tinggi (outlier)")
        
        # Cek satuan konsistensi
        unique_satuan = self.df['satuan'].unique()
        if len(unique_satuan) > 1:
            warnings.append(f"Ditemukan variasi satuan: {', '.join(unique_satuan)}")
        
        return len(warnings) == 0, warnings
    
    def clean_data(self) -> pd.DataFrame:
        """
        Membersihkan data dari anomali
        
        Returns:
            DataFrame yang sudah dibersihkan
        """
        if self.df is None:
            raise ValueError("Data belum di-load")
        
        df_clean = self.df.copy()
        
        # Hapus duplikat
        df_clean = df_clean.drop_duplicates()
        
        # Hapus baris dengan null di kolom penting
        df_clean = df_clean.dropna(subset=self.REQUIRED_COLUMNS)
        
        # Konversi tipe data
        df_clean['jumlah_kasus'] = pd.to_numeric(df_clean['jumlah_kasus'], errors='coerce')
        df_clean['tahun'] = pd.to_numeric(df_clean['tahun'], errors='coerce')
        df_clean['kode_provinsi'] = pd.to_numeric(df_clean['kode_provinsi'], errors='coerce')
        df_clean['kode_kabupaten_kota'] = pd.to_numeric(df_clean['kode_kabupaten_kota'], errors='coerce')
        
        # Hapus baris dengan jumlah kasus negatif
        df_clean = df_clean[df_clean['jumlah_kasus'] >= 0]
        
        # Trim whitespace di kolom string
        string_columns = ['nama_provinsi', 'nama_kabupaten_kota', 'satuan']
        for col in string_columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].str.strip()
        
        logger.info(f"Data dibersihkan: {len(self.df)} -> {len(df_clean)} baris")
        
        self.df = df_clean
        return df_clean
    
    def get_summary_statistics(self) -> Dict:
        """
        Mendapatkan statistik summary data
        
        Returns:
            Dictionary berisi statistik
        """
        if self.df is None:
            raise ValueError("Data belum di-load")
        
        stats = {
            'total_records': len(self.df),
            'total_kasus': self.df['jumlah_kasus'].sum(),
            'rata_rata_kasus': self.df['jumlah_kasus'].mean(),
            'median_kasus': self.df['jumlah_kasus'].median(),
            'min_kasus': self.df['jumlah_kasus'].min(),
            'max_kasus': self.df['jumlah_kasus'].max(),
            'std_dev_kasus': self.df['jumlah_kasus'].std(),
            'jumlah_provinsi': self.df['nama_provinsi'].nunique(),
            'jumlah_kabupaten_kota': self.df['nama_kabupaten_kota'].nunique(),
            'tahun_range': (self.df['tahun'].min(), self.df['tahun'].max()),
            'tahun_count': self.df['tahun'].nunique()
        }
        
        return stats
    
    def get_data_by_year(self, year: int) -> pd.DataFrame:
        """
        Filter data berdasarkan tahun
        
        Args:
            year: Tahun yang diinginkan
            
        Returns:
            DataFrame terfilter
        """
        if self.df is None:
            raise ValueError("Data belum di-load")
        
        return self.df[self.df['tahun'] == year].copy()
    
    def get_data_by_province(self, province_name: str) -> pd.DataFrame:
        """
        Filter data berdasarkan provinsi
        
        Args:
            province_name: Nama provinsi
            
        Returns:
            DataFrame terfilter
        """
        if self.df is None:
            raise ValueError("Data belum di-load")
        
        return self.df[self.df['nama_provinsi'] == province_name].copy()
    
    def aggregate_by_province_year(self) -> pd.DataFrame:
        """
        Agregasi data per provinsi per tahun
        
        Returns:
            DataFrame agregat
        """
        if self.df is None:
            raise ValueError("Data belum di-load")
        
        agg_df = self.df.groupby(['nama_provinsi', 'tahun']).agg({
            'jumlah_kasus': ['sum', 'mean', 'count'],
            'nama_kabupaten_kota': 'nunique'
        }).reset_index()
        
        agg_df.columns = [
            'provinsi',
            'tahun',
            'total_kasus',
            'rata_rata_kasus',
            'jumlah_record',
            'jumlah_kabkot'
        ]
        
        return agg_df


# Fungsi-fungsi utility standalone
def quick_load_and_validate(file_path: str) -> Tuple[Optional[pd.DataFrame], bool, List[str]]:
    """
    Quick function untuk load dan validasi data
    
    Args:
        file_path: Path ke file CSV
        
    Returns:
        Tuple (dataframe, is_valid, error_messages)
    """
    try:
        parser = DBDDataParser(file_path)
        df = parser.load_csv()
        
        is_valid_structure, structure_errors = parser.validate_structure()
        is_valid_types, type_errors = parser.validate_data_types()
        is_valid_business, business_warnings = parser.validate_business_rules()
        
        all_errors = structure_errors + type_errors + business_warnings
        is_valid = is_valid_structure and is_valid_types
        
        if is_valid:
            df_clean = parser.clean_data()
            return df_clean, True, []
        else:
            return df, False, all_errors
    
    except Exception as e:
        return None, False, [str(e)]


def convert_to_long_format(df: pd.DataFrame) -> pd.DataFrame:
    """
    Konversi data ke long format untuk analisis time series
    
    Args:
        df: DataFrame input
        
    Returns:
        DataFrame dalam long format
    """
    return df.melt(
        id_vars=['kode_provinsi', 'nama_provinsi', 'kode_kabupaten_kota', 'nama_kabupaten_kota'],
        value_vars=['jumlah_kasus'],
        var_name='metric',
        value_name='value'
    )


def calculate_growth_rate(df: pd.DataFrame, groupby_cols: List[str]) -> pd.DataFrame:
    """
    Hitung growth rate year-over-year
    
    Args:
        df: DataFrame input
        groupby_cols: Kolom untuk grouping
        
    Returns:
        DataFrame dengan kolom growth_rate
    """
    df_sorted = df.sort_values(groupby_cols + ['tahun'])
    
    df_sorted['growth_rate'] = df_sorted.groupby(groupby_cols)['jumlah_kasus'].pct_change() * 100
    
    return df_sorted


# Contoh penggunaan
if __name__ == "__main__":
    # Contoh 1: Parsing basic
    print("=" * 50)
    print("CONTOH 1: Basic Parsing")
    print("=" * 50)
    
    parser = DBDDataParser("data_dbd_sample.csv")
    df = parser.load_csv()
    
    print(f"\nData loaded: {len(df)} rows")
    print(f"Columns: {list(df.columns)}")
    
    # Contoh 2: Validasi
    print("\n" + "=" * 50)
    print("CONTOH 2: Validasi Data")
    print("=" * 50)
    
    is_valid_structure, structure_errors = parser.validate_structure()
    print(f"\nStruktur valid: {is_valid_structure}")
    if structure_errors:
        print("Errors:", structure_errors)
    
    is_valid_types, type_errors = parser.validate_data_types()
    print(f"Tipe data valid: {is_valid_types}")
    if type_errors:
        print("Errors:", type_errors)
    
    # Contoh 3: Clean data
    print("\n" + "=" * 50)
    print("CONTOH 3: Clean Data")
    print("=" * 50)
    
    df_clean = parser.clean_data()
    print(f"\nData setelah cleaning: {len(df_clean)} rows")
    
    # Contoh 4: Summary statistics
    print("\n" + "=" * 50)
    print("CONTOH 4: Summary Statistics")
    print("=" * 50)
    
    stats = parser.get_summary_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Contoh 5: Filter data
    print("\n" + "=" * 50)
    print("CONTOH 5: Filter Data")
    print("=" * 50)
    
    df_2023 = parser.get_data_by_year(2023)
    print(f"\nData tahun 2023: {len(df_2023)} rows")
    print(f"Total kasus 2023: {df_2023['jumlah_kasus'].sum()}")
    
    # Contoh 6: Agregasi
    print("\n" + "=" * 50)
    print("CONTOH 6: Agregasi")
    print("=" * 50)
    
    agg_df = parser.aggregate_by_province_year()
    print("\nData agregat per provinsi per tahun:")
    print(agg_df.head(10))
    
    # Contoh 7: Quick load
    print("\n" + "=" * 50)
    print("CONTOH 7: Quick Load & Validate")
    print("=" * 50)
    
    df, is_valid, errors = quick_load_and_validate("data_dbd_sample.csv")
    print(f"\nValid: {is_valid}")
    if errors:
        print("Errors:", errors)
    else:
        print(f"Data siap digunakan: {len(df)} rows")

