# 🔑 Setup Google Gemini API Key

Panduan lengkap untuk mendapatkan dan setup API Key Google Gemini.

---

## 📝 Langkah-Langkah

### 1. Dapatkan API Key dari Google AI Studio

1. **Buka Google AI Studio**
   - Kunjungi: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

2. **Login dengan Google Account**
   - Gunakan akun Google Anda
   - Jika belum punya, buat akun baru

3. **Create API Key**
   - Klik tombol **"Create API Key"**
   - Pilih Google Cloud project (atau buat baru)
   - API key akan otomatis generated

4. **Copy API Key**
   - Klik **"Copy"** untuk menyalin API key
   - Format: `AIzaSy...` (sekitar 39 karakter)

---

## ⚙️ Cara Setup di Dashboard

### Opsi 1: File .env (Recommended)

1. **Buat file `.env`** di root folder project:
   ```bash
   # Windows
   echo GEMINI_API_KEY=your_api_key_here > .env
   
   # Linux/macOS
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

2. **Edit file `.env`** dan ganti dengan API key Anda:
   ```
   GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

3. **Jalankan dashboard** - API key akan otomatis terbaca

### Opsi 2: Input Manual di Dashboard

1. Jalankan dashboard: `streamlit run dashboard.py`
2. Buka tab **"AI Insights & Rekomendasi"**
3. Masukkan API key di field **"Masukkan Google Gemini API Key"**
4. Klik **"Generate AI Insights"**

---

## 🆓 Free Tier & Quota

### Google Gemini API - Free Tier

| Feature | Free Tier Limit |
|---------|----------------|
| **Requests per minute (RPM)** | 15 RPM |
| **Requests per day (RPD)** | 1,500 RPD |
| **Tokens per minute** | 1 million TPM |
| **Cost** | **FREE** |

### Model: Gemini 1.5 Pro

- **Context window**: 2 juta tokens
- **Output tokens**: Hingga 8,192 tokens
- **Multimodal**: Support text, images, video, audio
- **Languages**: 100+ bahasa termasuk Indonesia

---

## 🔒 Keamanan API Key

### ✅ DO's

1. **Simpan di `.env`** - Jangan hardcode di code
2. **Add `.env` ke `.gitignore`** - Jangan commit ke repository
3. **Gunakan environment variables** untuk production
4. **Regenerate key** jika tercuri atau terkompromis

### ❌ DON'Ts

1. ❌ **Jangan commit ke GitHub/GitLab**
2. ❌ **Jangan share di public forum**
3. ❌ **Jangan hardcode di source code**
4. ❌ **Jangan simpan di screenshot atau dokumentasi public**

---

## 🚨 Troubleshooting

### Error: "API key not valid"

**Solusi:**
- Cek API key sudah benar (tidak ada spasi/enter extra)
- Pastikan API key aktif di Google AI Studio
- Regenerate API key jika perlu

### Error: "Quota exceeded"

**Solusi:**
- Tunggu 1 menit (RPM limit)
- Cek quota harian (1,500 requests/day)
- Upgrade ke paid tier jika perlu lebih

### Error: "Permission denied"

**Solusi:**
- Enable Gemini API di Google Cloud Console
- Pastikan billing account aktif (untuk paid tier)
- Cek project permission

### API tidak terbaca dari .env

**Solusi:**
```bash
# Pastikan format benar
cat .env  # Linux/macOS
type .env  # Windows

# Restart dashboard
streamlit run dashboard.py
```

---

## 💰 Upgrade ke Paid Tier (Opsional)

Jika butuh quota lebih tinggi:

1. **Buka Google Cloud Console**
   - [https://console.cloud.google.com/](https://console.cloud.google.com/)

2. **Enable Billing**
   - Setup billing account
   - Link ke project Anda

3. **Pay-as-you-go Pricing**
   - Gemini 1.5 Pro: ~$7 per 1M tokens
   - Gemini 1.5 Flash: ~$0.35 per 1M tokens

---

## 📊 Monitoring Usage

### Cek Quota Usage

1. Buka [Google AI Studio](https://aistudio.google.com/)
2. Klik menu **"Quota"**
3. Lihat usage statistics:
   - Requests per day
   - Tokens used
   - Remaining quota

### Tips Hemat Quota

1. **Filter data** sebelum generate insights (lebih fokus)
2. **Save results** untuk menghindari regenerate yang sama
3. **Gunakan untuk analisis penting** saja
4. **Batch analysis** untuk multiple provinsi sekaligus

---

## 🔄 Regenerate API Key

Jika API key terkompromis atau perlu ganti:

1. Buka [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Klik ikon **trash/delete** pada key yang lama
3. Klik **"Create API Key"** untuk buat yang baru
4. Update `.env` file dengan key baru
5. Restart dashboard

---

## ✅ Verifikasi Setup

Test API key Anda:

```python
import google.generativeai as genai

# Setup API key
genai.configure(api_key="AIzaSy...")

# Test connection
model = genai.GenerativeModel('gemini-1.5-pro')
response = model.generate_content("Hello, test connection!")
print(response.text)
```

Atau jalankan:
```bash
python test_dashboard.py
```

---

## 📞 Bantuan Lebih Lanjut

### Dokumentasi Official

- **Google AI Studio**: [https://aistudio.google.com/](https://aistudio.google.com/)
- **Gemini API Docs**: [https://ai.google.dev/docs](https://ai.google.dev/docs)
- **Python SDK**: [https://ai.google.dev/tutorials/python_quickstart](https://ai.google.dev/tutorials/python_quickstart)

### Community Support

- **Google AI Forum**: [https://discuss.ai.google.dev/](https://discuss.ai.google.dev/)
- **Stack Overflow**: Tag `google-gemini`
- **GitHub Issues**: Report bugs di repo

---

## 🎯 Checklist Setup

- [ ] Buat akun Google (jika belum)
- [ ] Akses Google AI Studio
- [ ] Generate API key
- [ ] Copy API key
- [ ] Buat file `.env`
- [ ] Paste API key ke `.env`
- [ ] Test dengan `python test_dashboard.py`
- [ ] Run dashboard `streamlit run dashboard.py`
- [ ] Generate AI insights di dashboard
- [ ] ✅ Setup selesai!

---

**Selamat! API Key Gemini Anda sudah siap digunakan! 🚀**

*Last updated: November 2025*

