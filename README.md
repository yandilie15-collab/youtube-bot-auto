# YouTube Bot - Upload Video Otomatis

Bot otomatis untuk membuat dan upload video YouTube setiap hari.

## 📋 Persiapan

### 1. API Keys (Pilih salah satu atau keduanya)

**A. Groq API (Gratis & Cepat) - RECOMMENDED**
- Buka: https://console.groq.com
- Sign up dengan email
- Buat API Key
- Copy key (format: `gsk_xxxxx`)

**B. OpenAI API (Berbayar)**
- Buka: https://platform.openai.com/api-keys
- Buat API Key
- Copy key (format: `sk_xxxxx`)

### 2. Google Cloud Setup

1. Buka: https://console.cloud.google.com
2. Buat Project baru: "YouTube Bot"
3. Enable **YouTube Data API v3**
4. Buat OAuth 2.0 Credentials:
   - Type: Desktop Application
   - Download JSON file
   - Rename jadi `client_secrets.json`
   - Taruh di folder project ini

### 3. Setup File

1. Copy file `client_secrets.json` ke folder project
2. Buat file `.env` (copy dari `.env.example`):
```bash
cp .env.example .env
```

3. Edit `.env` dan isi API keys Anda:
```
GROQ_API_KEY=gsk_your_actual_key_here
OPENAI_API_KEY=sk_your_actual_key_here  # Optional
UPLOAD_SCHEDULE=daily
UPLOAD_TIME=18:00
LANGUAGE=id
```

## 🚀 Cara Menjalankan

### Dengan Docker (Recommended)

```bash
# Build dan jalankan
docker-compose -f docker-compose-chatgpt.yml up -d

# Lihat logs
docker-compose -f docker-compose-chatgpt.yml logs -f

# Stop bot
docker-compose -f docker-compose-chatgpt.yml down
```

### Tanpa Docker

```bash
# Install dependencies
pip install -r requirements_chatgpt.txt

# Jalankan bot
python bot_chatgpt.py
```

## ⚙️ Konfigurasi

Edit file `.env` untuk mengubah pengaturan:

- `UPLOAD_SCHEDULE`: `daily` (default)
- `UPLOAD_TIME`: Jam upload (format 24 jam, contoh: `18:00`)
- `LANGUAGE`: `id` untuk Bahasa Indonesia

## 📝 Cara Kerja

1. Bot berjalan sesuai jadwal (default: setiap hari jam 18:00)
2. Pilih topik random dari list yang tersedia
3. Generate script menggunakan AI (Groq/OpenAI)
4. Buat video dengan teks overlay
5. Upload ke YouTube secara otomatis
6. Simpan record di database

## 🔐 Authentication YouTube (Pertama Kali)

Saat pertama kali upload:
1. Browser akan terbuka otomatis
2. Login dengan akun YouTube Anda
3. Klik "Allow" untuk memberikan akses
4. Token akan disimpan di `token.pickle`
5. Upload berikutnya otomatis tanpa login lagi

## 🐛 Troubleshooting

**Error: No API keys found**
- Pastikan `.env` sudah dibuat dan diisi dengan benar
- Minimal harus ada `GROQ_API_KEY` atau `OPENAI_API_KEY`

**Error: client_secrets.json not found**
- Download file OAuth dari Google Cloud Console
- Rename jadi `client_secrets.json`
- Taruh di folder yang sama dengan bot

**Upload gagal**
- Cek koneksi internet
- Pastikan sudah authentication dengan YouTube
- Lihat logs untuk detail error

## 📊 Database

Bot menyimpan data di `topics.db` (SQLite):
- History video yang sudah dibuat
- Status upload
- YouTube video IDs

## 🎯 Topik Video

Bot memilih random dari 10 topik:
1. Fakta Menarik Tentang Hewan
2. Tips Kesehatan Harian
3. Sejarah Dunia yang Jarang Diketahui
4. Teknologi Terbaru
5. Motivasi Hidup
6. Tips Produktivitas
7. Fenomena Alam yang Menakjubkan
8. Kisah Inspiratif
9. Tips Keuangan Pribadi
10. Psikologi Manusia

Untuk menambah topik, edit `TOPICS` di `config_chatgpt.py`.

## ⚠️ Catatan Penting

- **JANGAN** share API keys Anda ke siapapun
- **JANGAN** commit file `.env` atau `client_secrets.json` ke Git
- Bot akan upload setiap hari sesuai jadwal
- Pastikan PC/server Anda menyala saat jadwal upload
- YouTube API quota: 10,000 units/hari (cukup untuk puluhan upload)

## 📞 Support

Jika ada masalah, cek:
1. Logs: `docker-compose logs -f`
2. Database: `topics.db`
3. API quotas di Google Cloud Console

## 🎉 Selamat!

Bot Anda siap! Video pertama akan diupload sesuai jadwal di `UPLOAD_TIME`.

Untuk test langsung tanpa tunggu jadwal, uncomment baris ini di `bot_chatgpt.py`:
```python
# create_and_upload_video()  # Hapus # di depan
```
