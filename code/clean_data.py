import os
import trafilatura
from tqdm import tqdm
import hashlib
import re

# ==================== Configuration ====================
RAW_DATA_DIR = "../data/raw"
CLEANED_DATA_DIR = "../data/cleaned"
LOG_DIR = "../logs"
MIN_TEXT_LENGTH = 150  # Minimum text length to filter invalid content

# ==================== Directory Initialization ====================
os.makedirs(CLEANED_DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ==================== Text Cleaning Utilities ====================
def remove_extra_whitespace(text):
    """Remove extra whitespace and line breaks"""
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    text = re.sub(r'^\s+|\s+$', '', text)  # Remove leading/trailing spaces
    return text

def get_text_hash(text):
    """Calculate text hash for deduplication"""
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def clean_louvre_html(html_file_path):
    """Clean Louvre HTML files and extract plain text (compatible with all trafilatura versions)"""
    try:
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Extract text WITHOUT language parameter (compatible with old trafilatura versions)
        cleaned_text = trafilatura.extract(
            html_content,
            include_comments=False, # Exclude comments
            include_tables=True,    # Keep artwork information tables
            include_images=False,   # Exclude image descriptions
            deduplicate=True,       # Remove duplicate paragraphs
            only_with_metadata=True # Keep only content with metadata
        )
        
        if cleaned_text:
            # Additional cleaning for Louvre-specific noise (English text optimization)
            cleaned_text = remove_extra_whitespace(cleaned_text)
            # Filter short/invalid text (ensure meaningful English content)
            if len(cleaned_text) >= MIN_TEXT_LENGTH:
                return cleaned_text
        return None
    except Exception as e:
        print(f"❌ Failed to clean {html_file_path}: {str(e)}")
        return None

def save_cleaned_text(text, index):
    """Save cleaned plain text to file"""
    filename = f"louvre_cleaned_{index}.txt"
    file_path = os.path.join(CLEANED_DATA_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    return file_path

# ==================== Main Program ====================
if __name__ == "__main__":
    print("🧹 Starting Louvre text data cleaning...")
    html_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith(".html")]
    hash_set = set()  # Store text hashes for deduplication
    cleaned_count = 0

    for idx, file_name in enumerate(tqdm(html_files, desc="Cleaning Progress")):
        file_path = os.path.join(RAW_DATA_DIR, file_name)
        clean_text = clean_louvre_html(file_path)
        
        if clean_text:
            text_hash = get_text_hash(clean_text)
            if text_hash not in hash_set:
                hash_set.add(text_hash)
                save_cleaned_text(clean_text, idx+1)
                cleaned_count += 1

    print(f"\n📊 Cleaning completed! Generated {cleaned_count} clean text files")
    print(f"📁 Cleaned data saved to: {os.path.abspath(CLEANED_DATA_DIR)}")