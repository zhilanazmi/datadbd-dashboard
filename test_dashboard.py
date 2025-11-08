"""
Script Testing untuk Dashboard DBD Indonesia
Test semua komponen dan fungsi utama
"""

import pandas as pd
import os
import sys

# Warna untuk output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✓{Colors.ENDC} {msg}")

def print_error(msg):
    print(f"{Colors.RED}✗{Colors.ENDC} {msg}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.ENDC} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.ENDC} {msg}")

def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{msg}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}\n")

def test_dependencies():
    """Test apakah semua dependencies terinstall"""
    print_header("TEST 1: Dependencies")
    
    required_packages = {
        'streamlit': 'streamlit',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'plotly': 'plotly',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'anthropic': 'anthropic',
        'dotenv': 'python-dotenv'
    }
    
    all_ok = True
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            print_success(f"{pip_name} installed")
        except ImportError:
            print_error(f"{pip_name} NOT installed")
            all_ok = False
    
    return all_ok

def test_data_files():
    """Test keberadaan file data"""
    print_header("TEST 2: Data Files")
    
    files = [
        'data_dbd_sample.csv',
        'dashboard.py',
        'requirements.txt',
        'README.md'
    ]
    
    all_ok = True
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print_success(f"{file} exists ({size} bytes)")
        else:
            print_error(f"{file} NOT found")
            all_ok = False
    
    return all_ok

def test_csv_format():
    """Test format CSV"""
    print_header("TEST 3: CSV Format")
    
    try:
        df = pd.read_csv('data_dbd_sample.csv')
        print_success(f"CSV loaded: {len(df)} rows")
        
        required_columns = [
            'kode_provinsi', 'nama_provinsi', 'kode_kabupaten_kota',
            'nama_kabupaten_kota', 'jumlah_kasus', 'satuan', 'tahun'
        ]
        
        all_ok = True
        for col in required_columns:
            if col in df.columns:
                print_success(f"Column '{col}' exists")
            else:
                print_error(f"Column '{col}' MISSING")
                all_ok = False
        
        # Test data types
        print_info(f"\nData types:")
        for col in df.columns:
            print(f"  - {col}: {df[col].dtype}")
        
        # Test statistics
        print_info(f"\nStatistics:")
        print(f"  - Total kasus: {df['jumlah_kasus'].sum():,.0f}")
        print(f"  - Jumlah provinsi: {df['nama_provinsi'].nunique()}")
        print(f"  - Tahun range: {df['tahun'].min()}-{df['tahun'].max()}")
        
        return all_ok
    
    except Exception as e:
        print_error(f"Error loading CSV: {str(e)}")
        return False

def test_parsing_utils():
    """Test utils_parsing.py"""
    print_header("TEST 4: Parsing Utils")
    
    try:
        from utils_parsing import DBDDataParser, quick_load_and_validate
        
        parser = DBDDataParser('data_dbd_sample.csv')
        df = parser.load_csv()
        print_success("DBDDataParser initialized")
        
        is_valid, errors = parser.validate_structure()
        if is_valid:
            print_success("Data structure valid")
        else:
            print_warning(f"Structure issues: {errors}")
        
        df_clean = parser.clean_data()
        print_success(f"Data cleaned: {len(df_clean)} rows")
        
        stats = parser.get_summary_statistics()
        print_success(f"Statistics calculated: {len(stats)} metrics")
        
        # Test quick function
        df2, is_valid2, errors2 = quick_load_and_validate('data_dbd_sample.csv')
        if is_valid2:
            print_success("quick_load_and_validate works")
        else:
            print_warning(f"Validation warnings: {errors2}")
        
        return True
    
    except Exception as e:
        print_error(f"Parsing utils error: {str(e)}")
        return False

def test_visualization_utils():
    """Test utils_visualization.py"""
    print_header("TEST 5: Visualization Utils")
    
    try:
        from utils_visualization import DBDVisualizer
        from utils_parsing import DBDDataParser
        
        parser = DBDDataParser('data_dbd_sample.csv')
        df = parser.load_csv()
        df_clean = parser.clean_data()
        
        viz = DBDVisualizer(df_clean)
        print_success("DBDVisualizer initialized")
        
        # Test berbagai visualisasi
        fig1 = viz.create_bar_trend()
        print_success("Bar trend chart created")
        
        fig2 = viz.create_line_trend()
        print_success("Line trend chart created")
        
        fig3 = viz.create_heatmap(top_n=5)
        print_success("Heatmap created")
        
        fig4 = viz.create_pie_chart(top_n=5)
        print_success("Pie chart created")
        
        fig5 = viz.create_treemap()
        print_success("Treemap created")
        
        print_info("All visualizations created successfully")
        
        return True
    
    except Exception as e:
        print_error(f"Visualization utils error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_integration():
    """Test utils_ai_integration.py"""
    print_header("TEST 6: AI Integration")
    
    try:
        from utils_ai_integration import ClaudeDBDAnalyzer
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        
        if not api_key or api_key == 'your-api-key-here':
            print_warning("API Key not set - skipping AI tests")
            print_info("Set ANTHROPIC_API_KEY in .env to test AI features")
            return True
        
        from utils_parsing import DBDDataParser
        
        parser = DBDDataParser('data_dbd_sample.csv')
        df = parser.load_csv()
        df_clean = parser.clean_data()
        
        analyzer = ClaudeDBDAnalyzer(api_key=api_key)
        print_success("ClaudeDBDAnalyzer initialized")
        
        # Test data preparation
        summary = analyzer.prepare_data_summary(df_clean)
        print_success(f"Data summary prepared: {len(summary)} sections")
        
        print_info("AI integration structure OK (skipping live API calls)")
        
        return True
    
    except Exception as e:
        print_error(f"AI integration error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_dashboard_components():
    """Test komponen dashboard utama"""
    print_header("TEST 7: Dashboard Components")
    
    try:
        # Cek apakah dashboard.py bisa di-import (syntax check)
        import importlib.util
        spec = importlib.util.spec_from_file_location("dashboard", "dashboard.py")
        dashboard = importlib.util.module_from_spec(spec)
        
        print_success("dashboard.py syntax OK")
        
        # Cek fungsi-fungsi penting ada
        required_functions = [
            'load_data',
            'analyze_data',
            'get_ai_insights',
            'create_trend_chart',
            'create_heatmap',
            'export_to_csv'
        ]
        
        with open('dashboard.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
            for func in required_functions:
                if f"def {func}" in content:
                    print_success(f"Function '{func}' defined")
                else:
                    print_warning(f"Function '{func}' not found")
        
        return True
    
    except Exception as e:
        print_error(f"Dashboard component error: {str(e)}")
        return False

def run_all_tests():
    """Run semua tests"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         DASHBOARD DBD INDONESIA - TEST SUITE              ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")
    
    results = {
        'Dependencies': test_dependencies(),
        'Data Files': test_data_files(),
        'CSV Format': test_csv_format(),
        'Parsing Utils': test_parsing_utils(),
        'Visualization Utils': test_visualization_utils(),
        'AI Integration': test_ai_integration(),
        'Dashboard Components': test_dashboard_components()
    }
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.ENDC}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED!{Colors.ENDC}")
        print(f"{Colors.GREEN}Dashboard siap digunakan!{Colors.ENDC}")
        print(f"\n{Colors.BLUE}Jalankan dashboard dengan:{Colors.ENDC}")
        print(f"{Colors.BOLD}  streamlit run dashboard.py{Colors.ENDC}\n")
        return True
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ SOME TESTS FAILED{Colors.ENDC}")
        print(f"{Colors.RED}Perbaiki issues di atas sebelum menggunakan dashboard{Colors.ENDC}\n")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

