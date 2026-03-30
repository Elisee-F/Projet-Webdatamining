import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ==================== Louvre Configuration (English) ====================
# Target URLs: Wikipedia Louvre-related pages (permanently valid)
TARGET_URLS = [
    "https://en.wikipedia.org/wiki/Louvre",                      # Louvre overview
    "https://en.wikipedia.org/wiki/Mona_Lisa",                   # Mona Lisa
    "https://en.wikipedia.org/wiki/Venus_de_Milo",               # Venus de Milo
    "https://en.wikipedia.org/wiki/Winged_Victory_of_Samothrace",# Winged Victory of Samothrace
    "https://en.wikipedia.org/wiki/Louvre_Museum#Collections"    # Louvre Collections (100% valid)
]
RAW_DATA_DIR = "../data/raw"
LOG_DIR = "../logs"

# Crawler configuration (anti-blocking)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://en.wikipedia.org/"
}
DELAY = 2  # 2-second delay between requests to avoid anti-crawling

# ==================== Directory Initialization ====================
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ==================== Logging Function ====================
def log_error(message):
    """Record error logs to file"""
    log_path = os.path.join(LOG_DIR, "crawler_errors.log")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

# ==================== Core Crawling Functions ====================
def crawl_static_page(url):
    """Crawl static web pages (most Wikipedia pages are static)"""
    try:
        time.sleep(DELAY)
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()  # Raise HTTP errors (4xx/5xx)
        response.encoding = response.apparent_encoding
        return response.text
    except Exception as e:
        error_msg = f"Static crawl failed for {url}: {str(e)}"
        print(error_msg)
        log_error(error_msg)
        return None

def crawl_dynamic_page(url):
    """Crawl dynamically loaded pages (fallback option)"""
    try:
        # Configure Chrome in headless mode
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        driver.get(url)
        time.sleep(3)  # Wait for dynamic content loading
        html = driver.page_source
        driver.quit()
        return html
    except Exception as e:
        error_msg = f"Dynamic crawl failed for {url}: {str(e)}"
        print(error_msg)
        log_error(error_msg)
        return None

def save_raw_html(html_content, url, index):
    """Save raw HTML content to file"""
    # Generate safe filename
    safe_filename = f"louvre_page_{index}.html"
    file_path = os.path.join(RAW_DATA_DIR, safe_filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Saved: {file_path}")

# ==================== Main Program ====================
if __name__ == "__main__":
    print("🚀 Starting Louvre English website data crawling...")
    success_count = 0
    
    for idx, url in enumerate(tqdm(TARGET_URLS, desc="Crawling Progress")):
        # Try static crawl first, fallback to dynamic if failed
        html = crawl_static_page(url)
        if not html:
            html = crawl_dynamic_page(url)
        
        if html:
            save_raw_html(html, url, idx+1)
            success_count += 1
    
    print(f"\n📊 Crawling completed! Success: {success_count}/{len(TARGET_URLS)} pages")
    print(f"📁 Raw data saved to: {os.path.abspath(RAW_DATA_DIR)}")
