@echo off
echo ========================================
echo Setup Git Repository untuk AlfiResponden
echo ========================================
echo.

REM Navigasi ke direktori proyek
cd /d "C:\Users\ASUS\OneDrive\Desktop\Auto Responden"

echo [1/6] Inisialisasi Git repository...
"C:\Program Files\Git\bin\git.exe" init
if %errorlevel% neq 0 (
    echo Error: Gagal menginisialisasi Git repository
    pause
    exit /b %errorlevel%
)

echo [2/6] Konfigurasi identitas Git...
echo Masukkan informasi identitas Anda untuk Git:
set /p git_name="Nama Anda: "
set /p git_email="Email Anda: "

"C:\Program Files\Git\bin\git.exe" config --local user.name "%git_name%"
if %errorlevel% neq 0 (
    echo Error: Gagal mengatur nama pengguna
    pause
    exit /b %errorlevel%
)

"C:\Program Files\Git\bin\git.exe" config --local user.email "%git_email%"
if %errorlevel% neq 0 (
    echo Error: Gagal mengatur email pengguna
    pause
    exit /b %errorlevel%
)

echo [3/6] Menambahkan file ke staging area...
"C:\Program Files\Git\bin\git.exe" add .
if %errorlevel% neq 0 (
    echo Error: Gagal menambahkan file ke staging area
    pause
    exit /b %errorlevel%
)

echo [4/6] Membuat commit...
"C:\Program Files\Git\bin\git.exe" commit -m "Initial commit for AlfiResponden"
if %errorlevel% neq 0 (
    echo Error: Gagal membuat commit
    pause
    exit /b %errorlevel%
)

echo.
echo ========================================
echo Langkah selanjutnya:
echo 1. Buat repository "AlfiResponden" di GitHub
echo 2. Jalankan perintah berikut setelah membuat repository:
echo    "C:\Program Files\Git\bin\git.exe" branch -M main
echo    "C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/YOUR_USERNAME/AlfiResponden.git
echo    "C:\Program Files\Git\bin\git.exe" push -u origin main
echo ========================================
echo.

echo Setup awal selesai! 
echo Sekarang buat repository di GitHub dan jalankan perintah di atas.
pause