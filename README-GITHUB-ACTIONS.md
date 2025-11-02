# Setup Script dengan GitHub Actions

Panduan ini akan membantu Anda mengatur script pengisian form otomatis menggunakan GitHub Actions dengan kemampuan kontrol dari ponsel.

## Persyaratan

1. Akun GitHub (gratis)
2. Repository GitHub untuk script Anda
3. File CSV dengan data yang akan diisi ke form

## Langkah-langkah Setup

### 1. Membuat Repository di GitHub
1. Login ke akun GitHub Anda
2. Klik "New repository"
3. Beri nama repository (misalnya: auto-form-filler)
4. Pilih "Public" atau "Private" (bebas)
5. Jangan inisialisasi dengan README
6. Klik "Create repository"

### 2. Upload File ke Repository
Upload file-file berikut ke repository Anda:
- [autoFillForm.py](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/autoFillForm.py)
- [Dampak Pamasarannnn.csv](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/Dampak%20Pamasarannnn.csv)
- [.github/workflows/auto-form-filler.yml](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/.github/workflows/auto-form-filler.yml) (sudah dibuat otomatis)
- [control.json](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/control.json)
- [web_controller.py](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/web_controller.py)

### 3. Konfigurasi GitHub Actions
File workflow sudah dibuat di `.github/workflows/auto-form-filler.yml` dengan konfigurasi berikut:

```yaml
name: Auto Form Filler

on:
  schedule:
    # Menjalankan setiap 15 menit untuk simulasi "terus-menerus"
    - cron: '*/15 * * * *'
  workflow_dispatch:  # Memungkinkan menjalankan secara manual dari GitHub UI
  repository_dispatch:
    types: [start-script, stop-script]

jobs:
  fill-form:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pandas selenium webdriver-manager

    - name: Install Chrome
      run: |
        sudo apt-get update
        sudo apt-get install -y wget gnupg
        wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
        echo "deb http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google.list
        sudo apt-get update
        sudo apt-get install -y google-chrome-stable

    - name: Check control file
      id: control
      run: |
        if [ -f "control.json" ]; then
          STATUS=$(jq -r '.status' control.json)
          echo "status=$STATUS" >> $GITHUB_OUTPUT
        else
          echo "status=running" >> $GITHUB_OUTPUT
        fi

    - name: Run autoFillForm script
      if: steps.control.outputs.status != 'stopped'
      env:
        FORM_URL: ${{ secrets.FORM_URL }}
      run: |
        # Jika FORM_URL tidak diset di secrets, gunakan URL default
        if [ -z "$FORM_URL" ]; then
          echo "FORM_URL not set in secrets, using default URL"
        fi
        python autoFillForm.py

    - name: Commit and push progress
      run: |
        git config --global user.name 'github-actions[bot]'
        git config --global user.email 'github-actions[bot]@users.noreply.github.com'
        git add progress.json control.json
        git commit -m "Update progress.json and control.json" || echo "No changes to commit"
        git push
```

### 4. Konfigurasi URL Form (Opsional)
Jika Anda ingin menggunakan URL form yang berbeda dari yang sudah dikodekan:

1. Di repository GitHub Anda, pergi ke Settings > Secrets and variables > Actions
2. Klik "New repository secret"
3. Buat secret dengan nama `FORM_URL` dan nilai URL form Google Anda

### 5. Menjalankan Workflow
Ada beberapa cara untuk menjalankan workflow:

1. **Otomatis**: Workflow akan berjalan setiap 15 menit sesuai jadwal
2. **Manual**: 
   - Pergi ke tab "Actions" di repository Anda
   - Pilih workflow "Auto Form Filler"
   - Klik "Run workflow" > "Run workflow"

## Kontrol dari Ponsel

Script dapat dikontrol dari ponsel menggunakan GitHub API. Lihat file [README-CONTROL.md](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/README-CONTROL.md) untuk instruksi lengkap.

### Fitur Kontrol:
1. **Mulai Script**: Mengirim perintah untuk memulai eksekusi
2. **Hentikan Script**: Mengirim perintah untuk menghentikan eksekusi
3. **Cek Status**: Melihat status saat ini (berjalan/berhenti)
4. **Lanjutkan dari Tempat Terakhir**: Script akan melanjutkan dari baris terakhir yang diproses

## Cara Kerja

1. GitHub Actions akan menjalankan script setiap 15 menit
2. Script membaca data dari [Dampak Pamasarannnn.csv](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/Dampak%20Pamasarannnn.csv)
3. Script menggunakan file [progress.json](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/progress.json) untuk melacak jawaban yang sudah dikirim
4. File kontrol [control.json](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/control.json) digunakan untuk mengontrol status script
5. Setiap jawaban yang berhasil dikirim akan disimpan progressnya
6. File [progress.json](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/progress.json) dan [control.json](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/control.json) akan di-commit kembali ke repository

## Monitoring

### Melihat Log
1. Pergi ke tab "Actions" di repository Anda
2. Klik pada workflow run yang ingin dilihat
3. Lihat log di setiap langkah

### Melihat File Log
File `form_filler.log` akan berisi log aktivitas script. Untuk melihatnya:
1. Clone repository ke komputer lokal
2. Buka file `form_filler.log`

## Batasan GitHub Actions

1. **Waktu Eksekusi**: Maksimal 6 jam per job
2. **Kuota**: 2000 menit/build per bulan untuk akun gratis
3. **Runtime**: Tidak bisa berjalan 24/7 terus menerus (tetapi dijadwalkan setiap 15 menit)
4. **Jaringan**: Mungkin ada batasan akses jaringan

## Tips

1. **Optimalkan Data CSV**: Pastikan file CSV tidak terlalu besar karena ada batasan waktu eksekusi
2. **Jadwal**: Sesuaikan jadwal cron sesuai kebutuhan Anda
3. **Monitoring**: Periksa log secara berkala untuk memastikan script berjalan dengan baik
4. **Backup**: Simpan salinan file CSV dan progress.json di tempat lain

## Troubleshooting

### Error: "Form not found" atau "Element not found"
- Pastikan XPath di script sesuai dengan form Anda
- Periksa apakah form masih tersedia dan tidak berubah strukturnya

### Error: "CSV file not found"
- Pastikan nama file CSV adalah `Dampak Pamasarannnn.csv` (dengan double 'n')
- Pastikan file CSV diupload ke repository

### Error: "ChromeDriver not found"
- Biasanya ini ditangani oleh webdriver-manager
- Jika terjadi error, coba restart workflow

## Keamanan

1. **Private Repository**: Gunakan repository private jika data sensitif
2. **Secrets**: Gunakan GitHub Secrets untuk menyimpan informasi sensitif
3. **Permissions**: Batasi akses ke repository hanya untuk pengguna yang diperlukan
4. **Token Management**: Jaga kerahasiaan Personal Access Token dan jangan bagikan

## Bantuan Tambahan

Jika mengalami masalah:
1. Periksa log di tab Actions
2. Pastikan semua dependensi terinstal dengan benar
3. Verifikasi file CSV ada dan dapat diakses
4. Pastikan URL form valid dan dapat diakses
5. Periksa file `control.json` untuk status kontrol