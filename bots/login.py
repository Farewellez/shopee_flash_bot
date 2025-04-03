import os
import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import random


def save_cookies(account_name):
    driver = None
    try:
        # Path absolut ke chromedriver (fix untuk Windows)
        chromedriver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'myenv', 'Scripts', 'chromedriver.exe'))
        print(f"ChromeDriver path: {chromedriver_path}")  # Debugging
        
        # Setup Chrome options
        chrome_options = Options()
        
        # Anti-detection settings
        chrome_options.add_argument("--disable-gpu")  # Mencegah error WebGL
        chrome_options.add_argument("--disable-software-rasterizer")  # Perbaiki rendering GPU
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")
        chrome_options.add_argument("--disable-gpu")  # Jika di Windows
        chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging
        chrome_options.add_argument("user-data-dir=C:\\Users\\ZAFARELL\\AppData\\Local\\Google\\Chrome\\User Data")


        # Inisialisasi Service
        service = Service(executable_path=chromedriver_path)
        
        # Inisialisasi Driver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Buka halaman Shopee dengan timeout
        driver.set_page_load_timeout(30)
        driver.get("https://shopee.co.id")
        time.sleep(random.uniform(2, 5))  # Delay acak lebih natural
        # Cek apakah CAPTCHA muncul
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'CAPTCHA') or contains(text(),'Verifikasi') or contains(@class,'captcha')]"))
            )
            print("⚠️ CAPTCHA terdeteksi, silakan selesaikan manual.")
            input("Tekan Enter setelah CAPTCHA selesai...")
        except:
            print("✅ Tidak ada CAPTCHA, lanjut login.")

        input("Tekan Enter setelah login berhasil...")
        # Menjalankan JavaScript untuk menyembunyikan otomatisasi
        # Menyembunyikan navigator.webdriver untuk menghindari deteksi
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        
        print(f"\n🛒 Silakan login untuk akun: {account_name}")
        print("1. Buka browser yang muncul")
        print("2. Login MANUAL dengan akun Shopee/Google")
        print("3. Pastikan sudah masuk beranda Shopee")
        print("4. Kembali ke terminal ini dan tekan Enter")
        
        input("Tekan Enter setelah login berhasil...")
        
        # Tunggu dan simpan cookies
        time.sleep(5)
        cookies_dir = Path("cookies")
        cookies_dir.mkdir(exist_ok=True)
        pickle.dump(driver.get_cookies(), open(cookies_dir / f"{account_name}.pkl", "wb"))
        print(f"✅ Cookies tersimpan di: {cookies_dir}/{account_name}.pkl")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if driver is not None:
            driver.save_screenshot(f"error_{account_name}.png")
    finally:
        if driver is not None:
            driver.quit()

if __name__ == "__main__":
    accounts = ["ahmadzafarell", "stellediot", "violet306"]
    
    print("🚀 Memulai proses penyimpanan cookies Shopee")
    print("⚠️ Pastikan:")
    print("- Chrome versi terbaru terinstall")
    print("- Tidak ada session Shopee yang aktif di browser biasa")
    
    for acc in accounts:
        print(f"\n{'='*50}")
        print(f"Memproses akun: {acc}")
        save_cookies(acc)
    
    print("\n✅ Proses selesai. Periksa folder 'cookies'")