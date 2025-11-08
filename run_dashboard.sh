#!/bin/bash

echo "===================================="
echo "  Dashboard DBD Indonesia"
echo "  Starting Streamlit Application"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Aktivasi virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment tidak ditemukan."
    echo "Membuat virtual environment baru..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo ""
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "Starting dashboard..."
echo ""
echo "Dashboard akan terbuka di browser secara otomatis."
echo "Tekan Ctrl+C untuk menghentikan aplikasi."
echo ""

streamlit run dashboard.py

