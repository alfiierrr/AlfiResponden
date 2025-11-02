import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import os
import json
import logging
from datetime import datetime
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('form_filler.log'),
        logging.StreamHandler()
    ]
)

# --- KONFIGURASI PENTING ---
# Ganti dengan URL Google Form Anda
FORM_URL = os.environ.get('FORM_URL', 'https://forms.gle/wqeJBMLVcmrghjyv5')  # Ganti dengan URL Google Form Anda yang sebenarnya
# Ganti dengan nama file CSV Anda
CSV_FILE = 'Dampak_Pamasarannnn.csv'  # Menggunakan file CSV yang sebenarnya

# Gunakan path absolut untuk file CSV untuk menghindari masalah dengan OneDrive
CSV_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), CSV_FILE)

# File untuk menyimpan progress
PROGRESS_FILE = 'progress.json'
CONTROL_FILE = 'control.json'

# Waktu tunggu (detik) untuk browser memuat elemen
WAIT_TIME = random.randint(10, 17)
# Waktu tunggu (detik) antar pengiriman untuk menghindari deteksi bot
DELAY_BETWEEN_SUBMISSIONS = random.randint(49, 273)

# --- CUSTOM XPATH CONFIGURATION ---
# Tempat untuk menaruh path setelah inspect pada Google Form Anda
# Anda bisa mengganti nilai di bawah ini dengan XPath yang Anda dapatkan dari inspect element

# HALAMAN PEMBUKAAN (Welcome Page)
OPENING_PAGE_XPATHS = {
    'berikutnya': '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span',  # XPath untuk tombol "Berikutnya" di halaman pembukaan
}

# HALAMAN 1: Pilihan Wajib/Spesifik
PAGE1_XPATHS = {
    'nama': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input',  # XPath untuk field Nama
    'jenis_kelamin_pria': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div/span/div/div[1]/label/div',  # XPath untuk Pilihan Pria
    'jenis_kelamin_wanita': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div/span/div/div[2]/label/div',  # XPath untuk Pilihan Wanita
    'usia': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div/span/div',  # XPath untuk pertanyaan Usia (semua opsi)
    'pendidikan': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div/span/div',  # XPath untuk pertanyaan Pendidikan (semua opsi)
    'pernah_membeli': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div/span/div/div[1]/label/div',  # XPath untuk Pilihan 'Sudah'
    'belum_membeli': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div/span/div/div[2]/label/div',  # XPath untuk Pilihan 'Belum'
}

# HALAMAN 2: Pilihan Acak 3-4-5 (Pertanyaan Q1-Q5)
PAGE2_XPATHS = {
    'q1': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/span',  # XPath untuk pertanyaan 1
    'q2': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/span',  # XPath untuk pertanyaan 2
    'q3': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div',  # XPath untuk pertanyaan 3
    'q4': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div',  # XPath untuk pertanyaan 4
    'q5': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div',  # XPath untuk pertanyaan 5
}

# HALAMAN 3: Pilihan Acak 3-4-5 (Pertanyaan Q6-Q10)
PAGE3_XPATHS = {
    'q6': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/span',  # XPath untuk pertanyaan 6
    'q7': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/span',  # XPath untuk pertanyaan 7
    'q8': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/span',  # XPath untuk pertanyaan 8
    'q9': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/span',  # XPath untuk pertanyaan 9
    'q10': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/span',  # XPath untuk pertanyaan 10
}

# HALAMAN 4: Pilihan Acak 3-4-5 (Pertanyaan Q11-Q15)
PAGE4_XPATHS = {
    'q11': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/span',   # XPath untuk pertanyaan 11
    'q12': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/span',  # XPath untuk pertanyaan 12
    'q13': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/span',  # XPath untuk pertanyaan 13
    'q14': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/span',  # XPath untuk pertanyaan 14
    'q15': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/span',  # XPath untuk pertanyaan 15
}

# XPath untuk tombol navigasi
NAVIGATION_XPATHS = {
    'berikutnya': '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span',
    'kirim': '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span',
    'kirim_lain': '/html/body/div[1]/div[2]/div[1]/div/div[4]/a'
}

# XPath khusus untuk navigasi setelah setiap halaman
PAGE_TRANSITIONS = {
    'after_page_1': '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span',      # Setelah halaman pertama
    'after_page_2': '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span',      # Setelah halaman kedua
    'after_page_3': '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span',      # Setelah halaman ketiga
    'after_page_4': '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span',      # Setelah halaman keempat
    'halaman_penutup_kirim': '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span',  # Di halaman penutup - tombol kirim
    'kirim_jawaban_lain': '/html/body/div[1]/div[2]/div[1]/div/div[4]/a'  # Setelah kirim - lanjut ke halaman selanjutnya
}

def select_radio_option(driver, xpath, choice_index):
    """Memilih opsi radio button berdasarkan XPath dan index pilihan."""
    try:
        # Wait for the container element to be present
        container = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        
        # Scroll the container into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
        time.sleep(1)
        
        # Print debug information
        print(f"Mencoba memilih opsi {choice_index} untuk pertanyaan dengan xpath: {xpath}")
        
        # Try to find radio buttons by role='radio' (this approach has been working)
        radio_buttons = container.find_elements(By.XPATH, ".//div[@role='radio']")
        print(f"Ditemukan {len(radio_buttons)} radio button dengan role='radio'")
        if len(radio_buttons) >= choice_index:
            # Make sure the element is clickable
            WebDriverWait(driver, WAIT_TIME).until(
                EC.element_to_be_clickable(radio_buttons[choice_index - 1])
            )
            driver.execute_script("arguments[0].click();", radio_buttons[choice_index - 1])
            print(f"Berhasil mengklik radio button index {choice_index} dengan role='radio'")
            return
            
        # If the above method fails, raise an exception
        raise Exception(f"Could not select option {choice_index} for xpath {xpath} - tidak ditemukan radio button yang cukup")
        
    except Exception as e:
        print(f"Error memilih opsi: {e}")
        raise e

def click_next_or_submit(driver, xpath):
    """Mengklik tombol berdasarkan XPath."""
    try:
        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        # Scroll element into view
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)  # Give time for scroll
        element.click()
        time.sleep(2) # Tunggu transisi halaman
    except Exception as e:
        print(f"Error mengklik tombol: {e}")
        # Coba cara alternatif
        try:
            element = WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            driver.execute_script("arguments[0].click();", element)
            time.sleep(2)
        except Exception as e2:
            print(f"Gagal mengklik tombol dengan cara alternatif: {e2}")

def get_choice_from_csv_value(value):
    """Mengubah nilai CSV menjadi index pilihan (1-5)"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def save_progress(index):
    """Simpan index baris terakhir yang diproses"""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({'last_index': index}, f)

def load_progress():
    """Muat index baris terakhir yang diproses"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            data = json.load(f)
            return data.get('last_index', 0)
    return 0

def reset_progress():
    """Reset file progress"""
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)

def load_control():
    """Muat status kontrol dari file"""
    if os.path.exists(CONTROL_FILE):
        try:
            with open(CONTROL_FILE, 'r') as f:
                data = json.load(f)
                return data.get('status', 'running')
        except:
            return 'running'
    return 'running'

def save_control(status):
    """Simpan status kontrol ke file"""
    control_data = {
        'status': status,
        'last_updated': datetime.now().isoformat()
    }
    with open(CONTROL_FILE, 'w') as f:
        json.dump(control_data, f)

def isi_form_otomatis(headless=True):
    logging.info("Memulai proses pengisian form otomatis")
    
    # Periksa status kontrol
    control_status = load_control()
    if control_status == 'stopped':
        logging.info("Script dihentikan berdasarkan kontrol file")
        return
    
    # 1. Inisialisasi WebDriver dengan ChromeDriver path
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--disable-storage")
    chrome_options.add_argument("--disable-geolocation")
    
    # Tambahkan headless mode jika diperlukan untuk cloud server
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
    
    # Setup ChromeDriver service dengan webdriver-manager
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logging.info("ChromeDriver berhasil diinisialisasi dengan webdriver-manager.")
    except Exception as e:
        logging.error(f"Error saat menginisialisasi ChromeDriver: {e}")
        return

    # 2. Baca Data dari CSV
    try:
        # Gunakan path absolut untuk file CSV
        data = pd.read_csv(CSV_FILE_PATH)
        if data.empty:
            logging.error("Error: File CSV kosong.")
            driver.quit()
            return
        logging.info(f"Total {len(data)} baris data ditemukan di CSV.")
    except FileNotFoundError:
        logging.error(f"Error: File CSV '{CSV_FILE}' tidak ditemukan. Pastikan ada di folder yang sama.")
        logging.error(f"Path file yang dicari: {CSV_FILE_PATH}")
        driver.quit()
        return
    except Exception as e:
        logging.error(f"Error saat membaca file CSV: {e}")
        driver.quit()
        return

    # Load progress
    start_index = load_progress()
    logging.info(f"Melanjutkan dari baris ke-{start_index}")
    
    # 3. Lakukan Looping untuk Setiap Baris Data
    for index, row in data.iterrows():
        # Periksa status kontrol setiap iterasi
        control_status = load_control()
        if control_status == 'stopped':
            logging.info("Script dihentikan berdasarkan kontrol file")
            break
            
        if index < start_index:
            continue  # Lewati baris yang sudah diproses
            
        # Extract data with simple error handling
        nama = ''
        jenis_kelamin = ''
        usia = ''
        pendidikan = ''
        pernah_membeli = 'Sudah'
        
        # Simple data extraction
        try:
            nama = str(row['Nama']) if 'Nama' in row and pd.notna(row['Nama']) else ''
            jenis_kelamin = str(row['Jenis Kelamin']) if 'Jenis Kelamin' in row and pd.notna(row['Jenis Kelamin']) else ''
            usia = str(row['Usia']) if 'Usia' in row and pd.notna(row['Usia']) else ''
            pendidikan = str(row['Pendidikan Terakhir']) if 'Pendidikan Terakhir' in row and pd.notna(row['Pendidikan Terakhir']) else ''
            pernah_membeli = str(row['Pernah Membeli Produk Hush Puppies']) if 'Pernah Membeli Produk Hush Puppies' in row and pd.notna(row['Pernah Membeli Produk Hush Puppies']) else 'Sudah'
        except:
            pass
        
        # Simple index conversion
        try:
            index_display = int(index) + 1
        except:
            index_display = 1
        
        logging.info(f"\n--- Memproses data ke-{index_display}: {nama} ({jenis_kelamin}) ---")
        
        try:
            # 3.1. Buka Form
            driver.get(FORM_URL)
            time.sleep(2) 

            # =======================================================
            # HALAMAN PEMBUKAAN (Welcome Page)
            # =======================================================
            # Tambahkan path untuk tombol "Berikutnya" di halaman pembukaan jika ada
            # Jika tidak ada halaman pembukaan, bagian ini bisa dilewati
            try:
                # Menggunakan XPath dari konfigurasi untuk tombol "Berikutnya" di halaman pembukaan
                WebDriverWait(driver, WAIT_TIME).until(
                    EC.element_to_be_clickable((By.XPATH, OPENING_PAGE_XPATHS['berikutnya']))
                ).click()
                logging.info("Halaman pembukaan dilewati.")
                time.sleep(2)
            except:
                # Jika tidak ada halaman pembukaan, lanjutkan ke halaman berikutnya
                logging.info("Tidak ada halaman pembukaan atau tombol 'Berikutnya' tidak ditemukan.")
                pass

            # =======================================================
            # HALAMAN 1: Pilihan Wajib/Spesifik (Asumsi 5 Pertanyaan)
            # =======================================================
            
            # P1: Nama (Opsional - Input Teks di urutan ke-1)
            nama_field = WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.XPATH, PAGE1_XPATHS['nama']))
            )
            nama_field.send_keys(nama)
            logging.info("P1: Nama diisi.")
            
            # P2: Jenis Kelamin (2 Pilihan, pilih salah satu - urutan ke-2)
            # Karena di CSV ada 'Pria' atau 'Wanita', kita tentukan indexnya:
            if jenis_kelamin.lower() == 'pria':
                WebDriverWait(driver, WAIT_TIME).until(
                    EC.element_to_be_clickable((By.XPATH, PAGE1_XPATHS['jenis_kelamin_pria']))
                ).click()
            else:
                WebDriverWait(driver, WAIT_TIME).until(
                    EC.element_to_be_clickable((By.XPATH, PAGE1_XPATHS['jenis_kelamin_wanita']))
                ).click()
            logging.info(f"P2: Jenis Kelamin ({jenis_kelamin}) dipilih.")

            # P3: Usia (4 Pilihan, pilih salah satu - urutan ke-3)
            # Pilih acak dari index 1 hingga 4 jika tidak ada di CSV
            if usia:
                # Map usia dari CSV ke pilihan
                if usia == "< 18 tahun":
                    choice_index = 1
                elif usia == "18 tahun - 25 tahun":
                    choice_index = 2
                elif usia == "26 tahun - 35 tahun":
                    choice_index = 3
                elif usia == "> 35 tahun":
                    choice_index = 4
                else:
                    choice_index = random.choice([1, 2, 3, 4])
                
                select_radio_option(driver, PAGE1_XPATHS['usia'], choice_index)
                logging.info(f"P3: Usia ({usia}) dipilih dengan index {choice_index}.")
            else:
                usia_choice_index = random.choice([1, 2, 3, 4])
                select_radio_option(driver, PAGE1_XPATHS['usia'], usia_choice_index)
                logging.info(f"P3: Usia dipilih acak index {usia_choice_index}.")

            # P4: Pendidikan Terakhir (6 Pilihan, pilih sesuai CSV)
            if pendidikan:
                # Map pendidikan dari CSV ke pilihan
                pendidikan_map = {
                    "< SMA": 1,
                    "SMA / SMK": 2,
                    "D3": 3,
                    "S1": 4,
                    "S2": 5,
                    "S3": 6
                }
                
                # Coba cari mapping, jika tidak ada gunakan acak
                choice_index = pendidikan_map.get(pendidikan, random.choice([2, 3, 4]))
                select_radio_option(driver, PAGE1_XPATHS['pendidikan'], choice_index)
                logging.info(f"P4: Pendidikan ({pendidikan}) dipilih dengan index {choice_index}.")
            else:
                pendidikan_choice_index = random.choice([2, 3, 4])
                select_radio_option(driver, PAGE1_XPATHS['pendidikan'], pendidikan_choice_index)
                logging.info(f"P4: Pendidikan dipilih acak index {pendidikan_choice_index}.")

            # P5: Sudah Pernah Membeli (Pilih sesuai CSV)
            if pernah_membeli.lower() == 'sudah':
                WebDriverWait(driver, WAIT_TIME).until(
                    EC.element_to_be_clickable((By.XPATH, PAGE1_XPATHS['pernah_membeli']))
                ).click()
                logging.info("P5: 'Sudah' dipilih.")
            else:
                WebDriverWait(driver, WAIT_TIME).until(
                    EC.element_to_be_clickable((By.XPATH, PAGE1_XPATHS['belum_membeli']))
                ).click()
                logging.info("P5: 'Belum' dipilih.")
            
            # Klik Tombol Berikutnya setelah halaman pertama
            click_next_or_submit(driver, PAGE_TRANSITIONS['after_page_1'])
            logging.info("Pindah ke halaman kedua.")

            # =======================================================
            # HALAMAN 2: Pilihan dari CSV (Pertanyaan Q1-Q5)
            # =======================================================
            
            # Pertanyaan 1 hingga 5 di halaman ini
            q_columns = [
                "Saya sering melihat promosi Hush Puppies di media sosial seperti Instagram atau TikTok.",
                "Tampilan visual konten promosi Hush Puppies menarik untuk dilihat.",
                "Saya pernah menyukai konten Hush Puppies.",
                "Informasi dalam konten promosi Hush Puppies di media sosial mudah dipahami.",
                "Saya mengikuti akun media sosial resmi Hush Puppies."
            ]
            
            for i, col_name in enumerate(q_columns, 1):
                # Simple choice selection
                choice = random.choice([3, 4, 5])  # Default random choice
                try:
                    if col_name in row and pd.notna(row[col_name]):
                        temp_choice = get_choice_from_csv_value(row[col_name])
                        if temp_choice and 1 <= temp_choice <= 5:
                            choice = temp_choice
                except:
                    pass
                
                select_radio_option(driver, PAGE2_XPATHS[f'q{i}'], choice)
                logging.info(f"H2-Q{i}: Pilihan index {choice}.")
            
            # Klik Tombol Berikutnya setelah halaman kedua
            click_next_or_submit(driver, PAGE_TRANSITIONS['after_page_2'])
            logging.info("Pindah ke halaman ketiga.")

            # =======================================================
            # HALAMAN 3: Pilihan dari CSV (Pertanyaan Q6-Q10)
            # =======================================================
            
            # Pertanyaan 6 hingga 10 di halaman ini
            q_columns = [
                "Saya dapat mengenali logo maupun simbol Hush Puppies dengan mudah.",
                "Saat membutuhkan produk fashion, saya teringat pada Hush Puppies.",
                "Saya merasa cukup akrab dengan brand Hush Puppies.",
                "Saya sering melihat atau mendengar nama Hush Puppies di media sosial.",
                "Saya bisa membedakan produk Hush Puppies dari merek lain."
            ]
            
            for i, col_name in enumerate(q_columns, 1):
                q_num = i + 5  # Q6-Q10
                # Simple choice selection
                choice = random.choice([3, 4, 5])  # Default random choice
                try:
                    if col_name in row and pd.notna(row[col_name]):
                        temp_choice = get_choice_from_csv_value(row[col_name])
                        if temp_choice and 1 <= temp_choice <= 5:
                            choice = temp_choice
                except:
                    pass
                
                select_radio_option(driver, PAGE3_XPATHS[f'q{q_num}'], choice)
                logging.info(f"H3-Q{q_num}: Pilihan index {choice}.")
            
            # Klik Tombol Berikutnya setelah halaman ketiga
            click_next_or_submit(driver, PAGE_TRANSITIONS['after_page_3'])
            logging.info("Pindah ke halaman keempat.")

            # =======================================================
            # HALAMAN 4: Pilihan dari CSV (Pertanyaan Q11-Q15)
            # =======================================================
            
            # Pertanyaan 11 hingga 15 di halaman ini
            q_columns = [
                "Promosi di media sosial mendorong saya membeli produk Hush Puppies.",
                "Saya mencari informasi lebih lanjut tentang Hush Puppies sebelum membeli.",
                "Saya membandingkan Hush Puppies dengan merek lain sebelum membeli.",
                "Saya puas dengan keputusan saya membeli produk Hush Puppies.",
                "Saya berencana untuk membeli produk Hush Puppies lagi di masa depan."
            ]
            
            for i, col_name in enumerate(q_columns, 1):
                q_num = i + 10  # Q11-Q15
                # Simple choice selection
                choice = random.choice([3, 4, 5])  # Default random choice
                try:
                    if col_name in row and pd.notna(row[col_name]):
                        temp_choice = get_choice_from_csv_value(row[col_name])
                        if temp_choice and 1 <= temp_choice <= 5:
                            choice = temp_choice
                except:
                    pass
                
                select_radio_option(driver, PAGE4_XPATHS[f'q{q_num}'], choice)
                logging.info(f"H4-Q{q_num}: Pilihan index {choice}.")
            
            # Klik Tombol Berikutnya setelah halaman keempat
            click_next_or_submit(driver, PAGE_TRANSITIONS['after_page_4'])
            logging.info("Pindah ke halaman penutup.")

            # Langsung ke halaman penutup - klik tombol Kirim
            click_next_or_submit(driver, PAGE_TRANSITIONS['halaman_penutup_kirim'])
            logging.info("Mengirim formulir.")
        
            logging.info(f"Data {nama} berhasil dikirim.")
            save_progress(index)  # Simpan progress setelah berhasil
            
            # =======================================================
            # HALAMAN PENUTUP: Konfirmasi (Kirim Jawaban Lain)
            # =======================================================
            try:
                WebDriverWait(driver, WAIT_TIME).until(
                    EC.element_to_be_clickable((By.XPATH, PAGE_TRANSITIONS['kirim_jawaban_lain']))
                ).click()
                logging.info("Mengklik 'Kirim jawaban lain' untuk loop berikutnya.")
            except:
                logging.info("Tombol 'Kirim jawaban lain' tidak ditemukan. Mungkin sudah di halaman awal.")
                pass
        
            time.sleep(DELAY_BETWEEN_SUBMISSIONS) # Tunggu sebelum memulai form baru

        except Exception as e:
            logging.error(f"Gagal mengirim data {nama}. Error: {e}")
            # Cetak trace lengkap untuk debugging
            # import traceback
            # logging.error(traceback.format_exc()) 

    # 4. Tutup Browser
    driver.quit()
    logging.info("\n------------------------------------")
    logging.info("Otomatisasi pengisian formulir selesai.")
    logging.info("------------------------------------")

if __name__ == "__main__":
    # Secara default menjalankan dengan mode headless untuk kompatibilitas GitHub Actions
    isi_form_otomatis(headless=True)