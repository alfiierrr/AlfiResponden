# Setup Git untuk AlfiResponden Repository

Panduan langkah demi langkah untuk mengatur repository "AlfiResponden" menggunakan Git.

## Prasyarat

1. Git sudah terinstal di komputer Anda
2. Akun GitHub sudah dibuat
3. Terminal/command prompt bisa diakses

## Langkah-langkah Setup

### 1. Inisialisasi Git Repository

Buka terminal/command prompt dan navigasi ke direktori proyek:
```bash
cd "C:\Users\ASUS\OneDrive\Desktop\Auto Responden"
```

Inisialisasi git repository:
```bash
git init
```

### 2. Tambahkan File ke Staging Area

Tambahkan semua file ke staging area:
```bash
git add .
```

### 3. Commit File

Buat commit pertama:
```bash
git commit -m "Initial commit for AlfiResponden"
```

### 4. Buat Repository di GitHub

1. Login ke akun GitHub Anda
2. Klik tombol "New" atau "+" di pojok kanan atas, lalu pilih "New repository"
3. Isi form pembuatan repository:
   - **Repository name**: AlfiResponden
   - **Description**: (Opsional) Auto form filler for Google Forms
   - **Public/Private**: Pilih sesuai preferensi Anda
   - **Initialize this repository with a README**: Jangan dicentang
4. Klik "Create repository"

### 5. Hubungkan Local Repository dengan Remote Repository

Setelah repository dibuat di GitHub, Anda akan melihat halaman dengan instruksi. Ikuti instruksi "…or push an existing repository from the command line":

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/AlfiResponden.git
```

**Catatan**: Ganti `YOUR_USERNAME` dengan username GitHub Anda.

### 6. Push ke GitHub

Push local repository ke GitHub:
```bash
git push -u origin main
```

Jika diminta, masukkan username dan password/token GitHub Anda.

### 7. Verifikasi Setup

1. Buka repository Anda di GitHub: `https://github.com/YOUR_USERNAME/AlfiResponden`
2. Pastikan semua file sudah terupload
3. Periksa struktur direktori:
   - File utama: `autoFillForm.py`, `Dampak Pamasarannnn.csv`, `control.json`, `progress.json`
   - Direktori: `.github/workflows/` dengan file `auto-form-filler.yml`
   - File dokumentasi: `README.md`, `README-GITHUB-ACTIONS.md`, `README-CONTROL.md`

## Troubleshooting

### Error: "fatal: remote origin already exists"
Jika Anda sudah pernah menambahkan remote origin sebelumnya:
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/AlfiResponden.git
```

### Error: "Authentication failed"
GitHub sekarang memerlukan Personal Access Token (PAT) daripada password:
1. Buat PAT di GitHub: Settings > Developer settings > Personal access tokens
2. Gunakan token sebagai password saat diminta

### Error: "Permission denied (publickey)"
Jika menggunakan SSH:
1. Pastikan SSH key sudah diatur
2. Atau gunakan HTTPS URL sebagai gantinya

## Langkah Selanjutnya

Setelah setup selesai:
1. Buat Personal Access Token untuk kontrol dari ponsel
2. Konfigurasikan FORM_URL secret di GitHub (jika diperlukan)
3. Jalankan workflow pertama kali dari tab Actions di GitHub
4. Mulai kontrol dari ponsel menggunakan API GitHub

## Catatan Penting

- Repository akan berjalan secara otomatis setiap 15 menit
- Script dapat dikontrol dari ponsel menggunakan Personal Access Token
- File `progress.json` akan menyimpan baris terakhir yang diproses
- File `control.json` akan menyimpan status script (running/stopped)