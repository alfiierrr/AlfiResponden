# Instalasi Git

Sebelum Anda dapat menjalankan script push ke GitHub, Anda perlu menginstal Git terlebih dahulu.

## Langkah-langkah Instalasi Git

### 1. Download Git
1. Buka browser dan kunjungi situs resmi Git: https://git-scm.com/downloads
2. Klik tombol "Windows" untuk mendownload Git untuk Windows
3. Tunggu proses download selesai

### 2. Instal Git
1. Klik dua kali file installer yang telah didownload
2. Ikuti instruksi instalasi:
   - Klik "Next" pada layar selamat datang
   - Pilih lokasi instalasi (biarkan default)
   - Pilih komponen (biarkan default)
   - Pilih editor teks default (biarkan default - Vim, atau pilih editor lain)
   - Sesuaikan PATH environment (pilih "Git from the command line and also from 3rd-party software")
   - Pilih pustaka koneksi HTTPS (biarkan default - OpenSSL)
   - Konfigurasi line ending (biarkan default - "Checkout Windows-style, commit Unix-style line endings")
   - Pilih terminal emulator (biarkan default - MinTTY)
   - Konfigurasi opsi tambahan (biarkan default)
   - Klik "Install" untuk memulai instalasi
   - Tunggu proses instalasi selesai
   - Klik "Finish"

### 3. Verifikasi Instalasi
1. Buka Command Prompt atau PowerShell
2. Ketik perintah berikut dan tekan Enter:
   ```bash
   git --version
   ```
3. Jika instalasi berhasil, Anda akan melihat versi Git yang terinstal

### 4. Konfigurasi Git
1. Buka Command Prompt atau PowerShell
2. Konfigurasi username dan email:
   ```bash
   git config --global user.name "Nama Anda"
   git config --global user.email "email@anda.com"
   ```

### 5. Restart Terminal
Setelah instalasi selesai, restart Command Prompt atau PowerShell untuk memastikan perubahan PATH diterapkan.

## Setelah Instalasi Selesai

Setelah Git terinstal, Anda dapat menjalankan kembali script setup:

1. Jalankan `setup_git.bat`
2. Buat repository "AlfiResponden" di GitHub
3. Jalankan `push_to_github.bat`

## Troubleshooting

### Error: "'git' is not recognized"
Jika masih muncul error setelah instalasi:
1. Restart komputer Anda
2. Pastikan Anda membuka Command Prompt atau PowerShell baru
3. Periksa apakah PATH sistem sudah mencakup direktori instalasi Git

### Masalah Autentikasi
GitHub sekarang memerlukan Personal Access Token (PAT) daripada password:
1. Buat PAT di GitHub: Settings > Developer settings > Personal access tokens
2. Gunakan token sebagai password saat diminta