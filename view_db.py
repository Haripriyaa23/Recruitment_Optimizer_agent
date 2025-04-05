import sqlite3

# Use the correct path to the database
DB_PATH = "agents/candidates.db"  # Ensure this matches the actual location

def fetch_candidates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()
    conn.close()
    return candidates

# Fetch and print candidates
candidates = fetch_candidates()
print("Candidates:", candidates)
