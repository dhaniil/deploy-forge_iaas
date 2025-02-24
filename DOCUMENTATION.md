# 📚 Dokumentasi Deploy Forge

Aplikasi untuk mendeploy framework web ke server remote melalui SSH dengan mudah.

## 🛠 Prasyarat Sistem
- Python 3.8+
- Streamlit
- SSH Server dengan:
  - User dengan akses sudo
  - Port SSH terbuka (default: 22)
  - Node.js (untuk framework JavaScript)
  - PHP 7.4+ dan Composer (untuk Laravel)

## 📥 Instalasi
1. Clone repositori:
```bash
git clone https://github.com/username/deploy-forge.git
cd deploy-forge
```

2. Buat virtual environment:
```bash
python -m venv venv
```

3. Aktifkan virtual environment:
```bash
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## ⚙ Konfigurasi
Tambahkan environment variable di file `.env`:
```env
SSH_DEFAULT_PORT=22
NODE_VERSION=18.x
COMPOSER_VERSION=2.5
```

## 🚀 Panduan Penggunaan
1. Jalankan aplikasi:
```bash
streamlit run main.py
```

2. **Langkah 1 - Koneksi SSH**:
   - Masukkan alamat IP/hostname server
   - Username dan password SSH
   - Port SSH (default: 22)

3. **Langkah 2 - Pilih Framework**:
   - Pilih framework dari dropdown
   - Masukkan nama proyek
   - Tekan tombol "Deploy"

4. **Proses Deployment**:
   - Aplikasi akan otomatis:
     1. Menginstall dependensi
     2. Membuat direktori proyek
     3. Menjalankan server development

## 🖥 Framework yang Didukung
| Framework | Versi | Port Default |
|-----------|-------|--------------|
| Next.js   | 13.4+ | 3000         |
| Node.js   | 18.x+ | 8080         |
| Laravel   | 10.x+ | 8000         |

## 🚨 Troubleshooting
**Error: "Composer could not find composer.json"**
```bash
# Solusi:
# 1. Pastikan direktori proyek belum ada
# 2. Pastikan path deployment benar
# 3. Jalankan command manual:
ssh user@hostname "mkdir -p /path/to/project && cd /path/to/project && composer init"
```

**Error Koneksi SSH Gagal**
- Periksa kembali kredensial SSH
- Pastikan port SSH terbuka
- Coba koneksi manual dengan:
```bash
ssh username@hostname -p port
