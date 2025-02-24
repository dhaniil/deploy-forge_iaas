# 🚀 Deploy Forge IAAS

Aplikasi berbasis Streamlit untuk deploy framework web ke server melalui SSH secara otomatis.

![Deploy Forge Screenshot](https://via.placeholder.com/800x500.png?text=Deploy+Forge+Screenshot)

## 📋 Prasyarat
- Python 3.8+
- Git
- Akses SSH ke server target
- Streamlit

## ⚡ Instalasi Cepat
1. Clone repositori:
```bash
git clone https://github.com/username/deploy-forge_iaas.git
cd deploy-forge_iaas
```

2. Setup environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/MacOS
pip install -r requirements.txt
```

3. Jalankan aplikasi:
```bash
streamlit run main.py
```

## ⚙️ Konfigurasi
Buat file `.env` di root folder:
```env
# Contoh konfigurasi
SSH_DEFAULT_PORT=22
DEPLOYMENT_PATH=/var/www
```

## 🛠 Penggunaan
1. Masukkan kredensial SSH server
2. Pilih framework yang ingin di-deploy
3. Masukkan nama proyek
4. Tekan tombol "Deploy"

## 🆘 Dukungan
Untuk masalah teknis, buka [issue](https://github.com/username/deploy-forge_iaas/issues) baru di GitHub.