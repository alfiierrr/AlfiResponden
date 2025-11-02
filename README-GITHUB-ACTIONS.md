# Deploy ke GitHub Actions

Panduan ini menjelaskan cara mendeploy dan menjalankan script autoFillForm.py menggunakan GitHub Actions.

## Prasyarat

1. Akun GitHub (gratis)
2. Repository GitHub untuk script
3. Git terinstal di komputer lokal
4. File CSV dengan data yang akan diisi ke Google Form

## Setup Awal

### 1. Setup Git Repository
Jika Anda belum memiliki repository Git:
1. Jalankan `setup_git.bat` untuk inisialisasi repository lokal
2. Buat repository baru di GitHub dengan nama `AlfiResponden`
3. Jalankan `push_to_github.bat` untuk upload ke GitHub

### 2. Konfigurasi Secret FORM_URL
1. Buka repository Anda di GitHub
2. Pergi ke Settings > Secrets and variables > Actions
3. Klik "New repository secret"
4. Tambahkan:
   - Name: [FORM_URL](file://c:\Users\ASUS\OneDrive\Desktop\Auto%20Responden\autoFillForm.py#L28-L28)
   - Value: URL Google Form Anda yang sebenarnya

### 3. Aktifkan GitHub Actions
1. Pergi ke tab "Actions" di repository Anda
2. Klik tombol untuk mengaktifkan workflow jika diminta
3. Workflow akan berjalan secara otomatis setiap 15 menit

## Konfigurasi Permission untuk GitHub Actions

Untuk memastikan GitHub Actions dapat berjalan dengan benar, pastikan repository memiliki permission yang tepat:

1. Repository settings > Actions > General
2. Di bagian "Workflow permissions", pilih:
   - "Read and write permissions"
   - Centang "Allow GitHub Actions to create and approve pull requests"

Ini diperlukan agar GitHub Actions bot dapat melakukan commit dan push perubahan ke repository, seperti update file [progress.json](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/progress.json) dan [control.json](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/control.json).

## Cara Kerja

Script akan berjalan secara terjadwal setiap 15 menit menggunakan cron job. Anda juga dapat menjalankan secara manual:

1. Pergi ke tab "Actions" di repository Anda
2. Pilih workflow "Auto Form Filler"
3. Klik "Run workflow" > "Run workflow"

## Monitoring

### Melihat Status Eksekusi
1. Pergi ke tab "Actions" di repository Anda
2. Lihat workflow "Auto Form Filler"
3. Klik pada eksekusi terbaru untuk melihat detail log

### Melihat Progress
1. Buka file [progress.json](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/progress.json) di repository
2. Lihat nilai `last_index` untuk mengetahui baris data terakhir yang diproses

### Melihat Status Kontrol
1. Buka file [control.json](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/control.json) di repository
2. Lihat nilai `status`:
   - `"running"`: Script akan berjalan
   - `"stopped"`: Script akan berhenti

## Troubleshooting

### Error: Permission denied to github-actions[bot]
Jika Anda melihat error ini:
```
remote: Permission to alfiierrr/AlfiResponden.git denied to github-actions[bot].
fatal: unable to access 'https://github.com/alfiierrr/AlfiResponden/': The requested URL returned error: 403
```

Solusi:
1. Pergi ke Settings > Actions > General di repository Anda
2. Di bagian "Workflow permissions", pilih "Read and write permissions"
3. Centang "Allow GitHub Actions to create and approve pull requests"

### Error: Process completed with exit code 128
Ini biasanya terkait dengan masalah permission atau autentikasi. Ikuti langkah di atas untuk mengatasi masalah permission.

### Script Tidak Berjalan
1. Pastikan workflow sudah diaktifkan
2. Periksa apakah ada error di tab "Actions"
3. Pastikan [FORM_URL](file://c:\Users\ASUS\OneDrive\Desktop\Auto%20Responden\autoFillForm.py#L28-L28) sudah dikonfigurasi di Secrets
4. Periksa file [control.json](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/control.json) untuk memastikan statusnya "running"
