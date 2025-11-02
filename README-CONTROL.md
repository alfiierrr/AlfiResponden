# Cara Mengontrol Script dari Ponsel

Panduan ini menjelaskan cara mengontrol script pengisian form otomatis dari ponsel Anda menggunakan GitHub API.

## Prasyarat

1. Repository GitHub dengan script yang sudah disetup
2. Personal Access Token dari GitHub
3. Aplikasi REST API Client di ponsel (seperti Postman Mobile, atau browser)

## Membuat Personal Access Token

1. Login ke GitHub di komputer
2. Pergi ke Settings > Developer settings > Personal access tokens > Tokens (classic)
3. Klik "Generate new token" > "Generate new token (classic)"
4. Beri nama token (misalnya: "form-controller")
5. Pilih scope: `repo` (memberikan akses penuh ke repository)
6. Klik "Generate token"
7. **Simpan token dengan aman** - ini adalah satu-satunya kali Anda akan melihatnya

## Endpoint Kontrol

Script dikontrol melalui GitHub Repository Dispatch API:

```
POST https://api.github.com/repos/{username}/{repository}/dispatches
```

Ganti `{username}` dengan username GitHub Anda dan `{repository}` dengan nama repository Anda.

## Payload untuk Setiap Perintah

### Mulai Script
```json
{
  "event_type": "start-script"
}
```

### Hentikan Script
```json
{
  "event_type": "stop-script"
}
```

## Cara Mengirim Perintah dari Ponsel

### Menggunakan Browser

1. Buka browser di ponsel
2. Akses URL:
   ```
   https://api.github.com/repos/{username}/{repository}/dispatches
   ```

3. Tambahkan header:
   - `Authorization: token {YOUR_PERSONAL_ACCESS_TOKEN}`
   - `Accept: application/vnd.github.v3+json`
   - `Content-Type: application/json`

4. Kirim payload JSON sesuai perintah yang diinginkan

### Menggunakan Aplikasi REST Client

Jika menggunakan aplikasi seperti Postman Mobile:

1. Buat request baru
2. Set method ke `POST`
3. Set URL ke:
   ```
   https://api.github.com/repos/{username}/{repository}/dispatches
   ```
4. Tambahkan headers:
   - `Authorization: token {YOUR_PERSONAL_ACCESS_TOKEN}`
   - `Accept: application/vnd.github.v3+json`
   - `Content-Type: application/json`
5. Di body, pilih "raw" dan "JSON", lalu masukkan payload:
   ```json
   {
     "event_type": "start-script"
   }
   ```
6. Klik "Send"

## Mengecek Status Script

Anda dapat mengecek status script dengan melihat file `control.json` di repository Anda:

1. Pergi ke `https://github.com/{username}/{repository}/blob/main/control.json`
2. Lihat nilai `status`:
   - `"running"`: Script akan berjalan
   - `"stopped"`: Script akan berhenti

## Cara Kerja Sistem Kontrol

1. Ketika Anda mengirim perintah melalui API, GitHub akan memicu workflow dengan event `repository_dispatch`
2. Workflow akan membaca file `control.json` untuk menentukan apakah harus menjalankan script
3. Script akan memeriksa status kontrol setiap iterasi dan berhenti jika statusnya "stopped"
4. File `control.json` akan diperbarui dan di-commit ke repository

## Contoh Penggunaan

### Mulai Script
1. Kirim POST request dengan payload:
   ```json
   {
     "event_type": "start-script"
   }
   ```
2. Script akan mulai berjalan pada workflow berikutnya (dalam 15 menit maksimal)

### Hentikan Script
1. Kirim POST request dengan payload:
   ```json
   {
     "event_type": "stop-script"
   }
   ```
2. Script akan berhenti setelah menyelesaikan iterasi saat ini

### Mengecek Status
1. Buka file `control.json` di repository
2. Lihat nilai `status`

## Catatan Penting

1. **Waktu Tunda**: Karena GitHub Actions dijadwalkan setiap 15 menit, mungkin ada penundaan maksimal 15 menit untuk perintah mulai/berhenti
2. **Keamanan**: Jaga kerahasiaan Personal Access Token Anda
3. **Kuota**: GitHub memberikan 2000 menit build per bulan untuk akun gratis
4. **Monitoring**: Periksa tab "Actions" di repository untuk melihat status workflow

## Troubleshooting

### Error: "Bad credentials"
- Pastikan Personal Access Token benar dan belum kedaluwarsa
- Pastikan token memiliki scope `repo`

### Error: "Not Found"
- Pastikan username dan nama repository benar
- Pastikan repository bersifat public atau Anda memiliki akses

### Script Tidak Merespon
- Periksa tab "Actions" untuk melihat status workflow
- Periksa file `form_filler.log` untuk log error
- Pastikan file `control.json` memiliki status yang benar