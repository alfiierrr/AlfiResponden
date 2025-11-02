@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Push Repository ke GitHub
echo ========================================
echo.

REM Minta username GitHub
set /p github_username="Masukkan username GitHub Anda: "

if "%github_username%"=="" (
    echo Error: Username GitHub tidak boleh kosong
    pause
    exit /b 1
)

echo.
echo Setting up remote repository...
"C:\Program Files\Git\bin\git.exe" branch -M main
"C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/%github_username%/AlfiResponden.git

echo.
echo Pushing to GitHub...
"C:\Program Files\Git\bin\git.exe" push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo Error: Gagal push ke GitHub. Mungkin Anda perlu:
    echo 1. Menggunakan Personal Access Token sebagai password
    echo 2. Memeriksa koneksi internet
    echo 3. Memastikan repository "AlfiResponden" sudah dibuat di GitHub
    pause
    exit /b %errorlevel%
)

echo.
echo ========================================
echo Repository berhasil diupload ke GitHub!
echo URL: https://github.com/%github_username%/AlfiResponden
echo ========================================
echo.

echo Setup selesai! Sekarang Anda dapat:
echo 1. Membuat Personal Access Token untuk kontrol dari ponsel
echo 2. Mengatur FORM_URL secret di Settings ^> Secrets and variables ^> Actions
echo 3. Menjalankan workflow dari tab Actions di GitHub
pause