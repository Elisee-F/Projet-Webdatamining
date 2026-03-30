import os
import spacy
import pandas as pd
from tqdm import tqdm
from collections import Counter

# ==================== Louvre Entity Configuration (English) ====================
CLEANED_DATA_DIR = "../data/cleaned"
ENTITY_OUTPUT_DIR = "../data/entities"
LOG_DIR = "../logs"

# Load spaCy English entity recognition model (lightweight version for beginners)
nlp = spacy.load("en_core_web_sm")

# Core entity types for Louvre project (filter irrelevant entities)
TARGET_ENTITY_TYPES = [
    "PERSON",     # Artists/People (e.g., Leonardo da Vinci)
    "ORG",        # Organizations (e.g., Louvre Museum)
    "GPE",        # Geopolitical entities (e.g., Paris, Italy)
    "WORK_OF_ART",# Artworks (e.g., Mona Lisa)
    "DATE",       # Dates/Time periods (e.g., 1503-1519)
    "OBJECT"      # Objects (e.g., sculpture, painting)
]

# ==================== Directory Initialization ====================
os.makedirs(ENTITY_OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ==================== Core Entity Extraction Functions ====================
def extract_louvre_entities(text, file_name):
    """Extract Louvre-related entities and filter irrelevant types"""
    doc = nlp(text)
    entities = []
    
    for ent in doc.ents:
        # Keep only target entity types
        if ent.label_ in TARGET_ENTITY_TYPES:
            # Standardize entity text (title case)
            entity_text = ent.text.strip().title()
            entities.append({
                "source_file": file_name,
                "entity": entity_text,
                "entity_type": ent.label_,
                "start_position": ent.start_char,
                "end_position": ent.end_char,
                "context": text[max(0, ent.start_char-50):min(len(text), ent.end_char+50)]  # Entity context
            })
    return entities

def save_entities(entities):
    """Save entities to Excel and CSV (for partner's use)"""
    df = pd.DataFrame(entities)
    # Remove duplicates: keep only one entry per (source_file, entity)
    df = df.drop_duplicates(subset=["source_file", "entity"])
    
    # Save to Excel (main file)
    excel_path = os.path.join(ENTITY_OUTPUT_DIR, "louvre_entities.xlsx")
    df.to_excel(excel_path, index=False, engine="openpyxl")
    
    # Save to CSV (backup)
    csv_path = os.path.join(ENTITY_OUTPUT_DIR, "louvre_entities.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")
    
    # Generate entity statistics report
    stats = df["entity_type"].value_counts()
    print("\n📈 Louvre Entity Statistics:")
    print(stats)
    
    # Save top 20 most frequent entities
    top_entities = Counter(df["entity"]).most_common(20)
    top_df = pd.DataFrame(top_entities, columns=["entity", "count"])
    top_df_path = os.path.join(ENTITY_OUTPUT_DIR, "top_20_entities.csv")
    top_df.to_csv(top_df_path, index=False, encoding="utf-8")
    print(f"\n🏆 Top 20 frequent entities saved to: {top_df_path}")
    
    return excel_path

# ==================== Main Program ====================
if __name__ == "__main__":
    print("🔍 Starting Louvre English entity extraction...")
    text_files = [f for f in os.listdir(CLEANED_DATA_DIR) if f.endswith(".txt")]
    all_entities = []

    for file_name in tqdm(text_files, desc="Extraction Progress"):
        file_path = os.path.join(CLEANED_DATA_DIR, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        # Extract entities
        entities = extract_louvre_entities(text, file_name)
        all_entities.extend(entities)

    if all_entities:
        output_path = save_entities(all_entities)
        print(f"\n✅ Entity extraction completed! Full entity list saved to: {output_path}")
    else:
        print("\n❌ No entities extracted! Please check:")
        print("  1. Are cleaned text files empty?")
        print("  2. Is spaCy model installed correctly? (python3 -m spacy download en_core_web_sm)")
        print("  3. Is the text in English?")
