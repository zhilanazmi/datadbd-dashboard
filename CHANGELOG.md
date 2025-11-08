# 📝 Changelog - Dashboard DBD Indonesia

Semua perubahan penting pada project ini akan didokumentasikan di file ini.

---

## [v1.1.0] - 2025-11-08

### 🔄 Changed - Migrasi ke Google Gemini AI

**Breaking Changes:**
- Mengganti AI provider dari **Anthropic Claude** ke **Google Gemini**
- API Key sekarang menggunakan **GEMINI_API_KEY** (bukan ANTHROPIC_API_KEY)

### ✨ Added

- Support untuk **Google Gemini 1.5 Pro**
- Free tier dengan generous quota (15 RPM, 1,500 RPD)
- Dokumentasi lengkap setup Gemini API (`SETUP_GEMINI_API.md`)
- Guide troubleshooting untuk Gemini API

### 🔧 Updated Files

#### Core Files
- `dashboard.py`
  - Import `google.generativeai` instead of `anthropic`
  - Update `get_ai_insights()` function untuk Gemini
  - Update UI text dan help messages
  - Update footer credit

- `utils_ai_integration.py`
  - Rename class: `ClaudeDBDAnalyzer` → `GeminiDBDAnalyzer`
  - Update all API calls ke Gemini format
  - Simplify API calls (tidak perlu messages array)
  - Update model name ke `gemini-1.5-pro`

#### Dependencies
- `requirements.txt`
  - Remove: `anthropic==0.7.0`
  - Add: `google-generativeai==0.3.2`

#### Testing
- `test_dashboard.py`
  - Update dependency test untuk `google.generativeai`
  - Update class name references
  - Update environment variable ke `GEMINI_API_KEY`

#### Documentation
- New: `SETUP_GEMINI_API.md` - Complete guide setup Gemini
- New: `CHANGELOG.md` - This file

### 🎯 Migration Guide

Jika Anda sudah menggunakan versi sebelumnya dengan Claude:

#### 1. Update Dependencies
```bash
pip install -r requirements.txt --upgrade
```

#### 2. Get Gemini API Key
- Visit: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
- Generate API key
- Format: `AIzaSy...`

#### 3. Update .env File
```bash
# OLD (Claude)
ANTHROPIC_API_KEY=sk-ant-...

# NEW (Gemini)
GEMINI_API_KEY=AIzaSy...
```

#### 4. Update Code (jika menggunakan utils_ai_integration.py)
```python
# OLD
from utils_ai_integration import ClaudeDBDAnalyzer
analyzer = ClaudeDBDAnalyzer(api_key=api_key)

# NEW
from utils_ai_integration import GeminiDBDAnalyzer
analyzer = GeminiDBDAnalyzer(api_key=api_key)
```

### ✅ Benefits of Gemini

| Aspect | Claude Sonnet 4.0 | Gemini 1.5 Pro |
|--------|------------------|----------------|
| **Cost (Free Tier)** | ❌ No free tier | ✅ 1,500 requests/day FREE |
| **Context Window** | 200K tokens | 2M tokens (10x larger!) |
| **Output Tokens** | 4,096 | 8,192 |
| **Speed** | Fast | Very Fast |
| **Languages** | 100+ | 100+ |
| **API Simplicity** | Complex | Simple |

### 🐛 Known Issues

- None at this time

### 📚 Documentation Updates Needed

- [ ] Update README.md dengan Gemini references
- [ ] Update TUTORIAL_LENGKAP.md
- [ ] Update QUICK_START_ID.md
- [x] Create SETUP_GEMINI_API.md
- [x] Create CHANGELOG.md

---

## [v1.0.0] - 2025-11-08

### 🎉 Initial Release

#### Features
- ✅ Dashboard interaktif dengan Streamlit
- ✅ 4 tab utama: Overview, Visualisasi, AI Insights, Export
- ✅ Filter dinamis (tahun, provinsi, kabupaten/kota)
- ✅ Multiple visualizations (bar, line, heatmap, pie)
- ✅ AI insights dengan Claude Sonnet 4.0
- ✅ Export data (CSV, PNG, TXT)
- ✅ Sample data DBD Indonesia
- ✅ Comprehensive documentation

#### Modules
- `dashboard.py` - Main Streamlit app
- `utils_parsing.py` - CSV parsing & validation
- `utils_visualization.py` - Chart generation
- `utils_ai_integration.py` - Claude AI integration
- `test_dashboard.py` - Test suite

#### Documentation
- README.md - Full documentation
- QUICK_START_ID.md - Quick start guide
- TUTORIAL_LENGKAP.md - Complete tutorial

#### Scripts
- `run_dashboard.bat` - Windows launcher
- `run_dashboard.sh` - Linux/macOS launcher

---

## 🔮 Future Roadmap

### v1.2.0 (Planned)
- [ ] Database integration (PostgreSQL/MySQL)
- [ ] Real-time data sync
- [ ] User authentication
- [ ] Role-based access control
- [ ] API endpoints (REST API)
- [ ] Automated email reports
- [ ] Mobile responsive design

### v1.3.0 (Planned)
- [ ] Geospatial mapping (Folium/Leaflet)
- [ ] ML forecasting models
- [ ] Anomaly detection
- [ ] Custom alert system
- [ ] Multi-language support
- [ ] PDF report generation

### v2.0.0 (Future)
- [ ] Microservices architecture
- [ ] Docker containerization
- [ ] Kubernetes deployment
- [ ] Advanced analytics dashboard
- [ ] Integration with Kemenkes API
- [ ] Blockchain for data integrity

---

## 📋 Version Numbering

Format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, minor improvements

---

## 🤝 Contributing

Jika Anda ingin contribute:
1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

## 📞 Support

- **Issues**: Open issue di GitHub
- **Questions**: Discussion section
- **Email**: [contact]

---

*Dashboard DBD Indonesia - Monitoring Demam Berdarah Dengue di Indonesia* 🇮🇩


