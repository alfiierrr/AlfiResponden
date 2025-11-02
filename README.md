# Auto Responden - Pengisi Formulir Google Otomatis

Skrip ini memungkinkan Anda untuk mengisi formulir Google secara otomatis menggunakan Selenium dan Python, dengan data yang berasal dari file CSV. Script ini dapat dijalankan secara lokal atau menggunakan GitHub Actions dengan kemampuan kontrol dari ponsel.

## Fitur Utama

- **Unduhan ChromeDriver Otomatis**: Skrip secara otomatis mengunduh dan mengatur ChromeDriver yang sesuai dengan versi Google Chrome Anda.
- **Tanpa Login**: Menggunakan mode incognito dan pengaturan khusus untuk menghindari permintaan login.
- **Pengisian Otomatis**: Mengisi formulir berdasarkan data dari file CSV.
- **Mencegah Duplikasi**: Menggunakan file progress.json untuk melacak jawaban yang sudah dikirim.
- **Kompatibel GitHub Actions**: Dapat dijalankan secara terjadwal menggunakan GitHub Actions.
- **Kontrol dari Ponsel**: Dapat dikontrol (mulai/berhenti) dari ponsel melalui GitHub API atau antarmuka web sederhana.
- **Lanjutkan dari Tempat Terakhir**: Script akan melanjutkan dari baris terakhir yang diproses setelah dihentikan.

## Persyaratan

### Untuk Penggunaan Lokal:
- Python (versi 3.8 atau lebih baru)
- Google Chrome Browser
- Koneksi Internet (untuk mengunduh ChromeDriver secara otomatis)

### Untuk Penggunaan dengan GitHub Actions:
- Akun GitHub (gratis)
- Repository GitHub untuk script
- Git terinstal di komputer lokal

## Instalasi

### Instalasi Git (Jika Belum Terinstal)
Sebelum melakukan setup Git, pastikan Git sudah terinstal:
1. Lihat file [INSTALL_GIT.md](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/INSTALL_GIT.md) untuk instruksi instalasi Git
2. Verifikasi instalasi dengan menjalankan:
   ```bash
   git --version
   ```

### Untuk Penggunaan Lokal:
1.  Pastikan Python sudah terinstal di komputer Anda.
2.  Buka terminal/command prompt.
3.  Navigasi ke direktori proyek ini.
4.  Instal dependensi Python yang diperlukan:
    ```bash
    pip install pandas selenium webdriver-manager
    ```
   
   Catatan: Dengan penambahan `webdriver-manager`, Anda tidak perlu lagi mengunduh ChromeDriver secara manual.

### Untuk Penggunaan dengan GitHub Actions:
1.  **Setup Git Repository** (Menggunakan file batch):
    *   Jalankan `setup_git.bat` untuk inisialisasi repository
    *   Buat repository "AlfiResponden" di GitHub
    *   Jalankan `push_to_github.bat` untuk upload ke GitHub

2.  **Konfigurasi Permission GitHub Actions**:
    *   Pergi ke Settings > Actions > General di repository Anda
    *   Di bagian "Workflow permissions", pilih "Read and write permissions"
    *   Centang "Allow GitHub Actions to create and approve pull requests"
    *   Lihat file [README-GITHUB-ACTIONS.md](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/README-GITHUB-ACTIONS.md) untuk detail lebih lanjut

3.  Workflow akan berjalan secara otomatis setiap 15 menit

## Penggunaan

### Untuk Penggunaan Lokal:
1.  **Konfigurasi Skrip (`autoFillForm.py`)**:
    *   Buka file `autoFillForm.py`.
    *   **`FORM_URL`**: Ganti dengan URL formulir Google Anda yang sebenarnya.
    *   Catatan: Anda tidak perlu lagi mengatur `CHROME_DRIVER_PATH` karena sekarang ditangani secara otomatis.

2.  **Siapkan File CSV**:
    *   Pastikan file CSV Anda memiliki format yang sesuai dengan struktur formulir Anda.
    *   File CSV harus berada di direktori yang sama dengan `autoFillForm.py`.

3.  **Jalankan Skrip**:
    ```bash
    python autoFillForm.py
    ```

### Untuk Penggunaan dengan GitHub Actions:
1.  **Setup Git Repository** (Menggunakan file batch):
    *   Jalankan `setup_git.bat` untuk inisialisasi repository
    *   Buat repository "AlfiResponden" di GitHub
    *   Jalankan `push_to_github.bat` untuk upload ke GitHub

2.  **Konfigurasi Secret FORM_URL**:
    *   Pergi ke Settings > Secrets and variables > Actions di repository Anda
    *   Klik "New repository secret"
    *   Tambahkan:
        - Name: [FORM_URL](file://c:\Users\ASUS\OneDrive\Desktop\Auto%20Responden\autoFillForm.py#L28-L28)
        - Value: URL Google Form Anda yang sebenarnya

3.  **Konfigurasi Permission GitHub Actions**:
    *   Pergi ke Settings > Actions > General di repository Anda
    *   Di bagian "Workflow permissions", pilih "Read and write permissions"
    *   Centang "Allow GitHub Actions to create and approve pull requests"

4.  Workflow akan berjalan otomatis setiap 15 menit
5.  Untuk menjalankan manual:
    *   Pergi ke tab "Actions" di repository Anda
    *   Pilih workflow "Auto Form Filler"
    *   Klik "Run workflow" > "Run workflow"

## Kontrol dari Ponsel

Script dapat dikontrol dari ponsel menggunakan dua metode:

### Metode 1: Antarmuka Web (Disarankan)
1. Buka file `mobile_controller.html` di browser ponsel Anda
2. Masukkan:
   - Personal Access Token GitHub Anda
   - Username GitHub Anda (alfiierrr)
   - Nama repository (AlfiResponden)
3. Gunakan tombol "Mulai Script" dan "Hentikan Script"

### Metode 2: GitHub API
1.  **Mulai Script**: Kirim perintah untuk memulai eksekusi
2.  **Hentikan Script**: Kirim perintah untuk menghentikan eksekusi
3.  **Lanjutkan dari Tempat Terakhir**: Script akan melanjutkan dari baris terakhir yang diproses

Lihat file [README-CONTROL.md](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/README-CONTROL.md) untuk instruksi lengkap tentang cara mengontrol script dari ponsel.

## Cara Kerja

### Tanpa Login
Skrip menggunakan mode incognito dan pengaturan khusus untuk menghindari permintaan login:
- `--incognito`: Menjalankan browser dalam mode privat
- `--disable-infobars`: Menyembunyikan notifikasi otomatisasi
- `--disable-notifications`: Menonaktifkan notifikasi browser
- `--disable-save-password-bubble`: Mencegah popup penyimpanan password
- `--disable-blink-features=AutomationControlled`: Menyembunyikan deteksi otomatisasi
- `--disable-storage`: Menonaktifkan penyimpanan data
- `--disable-geolocation`: Menonaktifkan lokasi

### Pengisian Otomatis
1. Skrip membaca data dari file CSV
2. Untuk setiap baris data, skrip membuka formulir dalam browser baru
3. Mengisi semua field berdasarkan data dari CSV
4. Mengirim formulir
5. Mengklik "Kirim jawaban lain" untuk melanjutkan ke data berikutnya

### Mencegah Duplikasi
1. Skrip menggunakan file `progress.json` untuk melacak jawaban yang sudah dikirim
2. Setiap jawaban yang berhasil dikirim akan disimpan progressnya
3. File `progress.json` akan diperbarui setiap kali ada jawaban yang berhasil dikirim

### Kontrol dari Ponsel
1. File `control.json` digunakan untuk mengontrol status script (berjalan/berhenti)
2. Perintah dari ponsel akan memperbarui file `control.json`
3. Script akan memeriksa status kontrol setiap iterasi

## Troubleshooting

### Linter Errors di IDE
Jika Anda melihat pesan kesalahan seperti "Import could not be resolved" di IDE Anda, ini adalah false positive. Pastikan Anda telah menjalankan perintah instalasi:
```bash
pip install pandas selenium webdriver-manager
```

Verifikasi instalasi dengan:
```bash
pip list
```

### Masalah ChromeDriver
Jika Anda mengalami masalah dengan ChromeDriver:
1. Pastikan koneksi internet Anda aktif
2. Periksa apakah antivirus Anda memblokir unduhan
3. Coba hapus cache webdriver-manager:
   - Windows: Hapus folder `%USERPROFILE%\.wdm`
   - Linux/Mac: Hapus folder `~/.wdm`

### Masalah Form Google
Jika form tidak terisi dengan benar:
1. Periksa kembali struktur form Anda
2. Sesuaikan XPath jika diperlukan
3. Pastikan Anda tidak melanggar kebijakan penggunaan Google Forms

### Masalah Git
Jika mengalami masalah dengan Git:
1. Lihat file [INSTALL_GIT.md](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/INSTALL_GIT.md) untuk instruksi instalasi
2. Pastikan Git sudah terinstal dan dapat diakses dari command line
3. Restart terminal setelah instalasi Git

### Masalah GitHub Actions
Jika mengalami masalah dengan GitHub Actions:
1. Lihat file [README-GITHUB-ACTIONS.md](file:///C:/Users/ASUS/OneDrive/Desktop/Auto%20Responden/README-GITHUB-ACTIONS.md) untuk troubleshooting
2. Pastikan permission GitHub Actions sudah dikonfigurasi dengan benar
3. Periksa apakah [FORM_URL](file://c:\Users\ASUS\OneDrive\Desktop\Auto%20Responden\autoFillForm.py#L28-L28) sudah dikonfigurasi di Secrets

## Keamanan

**PENTING**: Jangan pernah membagikan kredensial pribadi Anda (email, password) dalam kode. Skrip ini dirancang untuk bekerja tanpa memerlukan login.

## Catatan Penting

- Skrip ini akan membuka browser Google Chrome dan mengisi formulir secara otomatis.
- Pastikan `FORM_URL` telah dikonfigurasi dengan benar.
- Skrip menyertakan pengaturan untuk menghindari deteksi otomatis oleh Google Forms.
- Gunakan skrip ini secara bertanggung jawab dan sesuai dengan kebijakan penggunaan Google Forms.
- Untuk penggunaan dengan GitHub Actions, pastikan repository Anda memiliki kuota build yang cukup.
- Script akan melanjutkan dari baris terakhir yang diproses setelah dihentikan, mencegah duplikasi data.