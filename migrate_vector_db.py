import sqlite3
from src.config import VECTOR_DB_PATH

conn = sqlite3.connect(VECTOR_DB_PATH)
cur = conn.cursor()

# Add file_name column if it doesn't exist
try:
    cur.execute("ALTER TABLE documents ADD COLUMN file_name TEXT")
    print("✅ Added file_name column.")
except Exception as e:
    print("ℹ️ Could not add column (maybe it already exists?):", e)

conn.commit()
conn.close()
