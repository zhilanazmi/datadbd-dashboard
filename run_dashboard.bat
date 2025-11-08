@echo off
echo ====================================
echo   Dashboard DBD Indonesia
echo   Starting Streamlit Application
echo ====================================
echo.

REM Check if virtual environment exists
if exist venv (
    echo Aktivasi virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment tidak ditemukan.
    echo Membuat virtual environment baru...
    python -m venv venv
    call venv\Scripts\activate.bat
    
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting dashboard...
echo.
echo Dashboard akan terbuka di browser secara otomatis.
echo Tekan Ctrl+C untuk menghentikan aplikasi.
echo.

streamlit run dashboard.py

pause

