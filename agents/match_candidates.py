import sqlite3
import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import json

DB_NAME = "candidates.db"
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_all_candidate_embeddings(cursor):
    cursor.execute("SELECT id, name, skills, education, projects, experience, certifications FROM cvs")
    rows = cursor.fetchall()
    candidates = []

    for row in rows:
        candidate_id, name, skills, education, projects, experience, certifications = row
        combined_text = f"{skills} {education} {projects} {experience} {certifications}"
        candidates.append((candidate_id, name, combined_text))

    return candidates

def match_candidates_to_jd():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 🧾 Show available JDs
    cursor.execute("SELECT id, title FROM job_descriptions")
    jd_list = cursor.fetchall()

    if not jd_list:
        print("🚨 No job descriptions found in the database.")
        return

    print("📄 Available Job Descriptions:")
    for row in jd_list:
        print(f"{row[0]}. {row[1]}")

    try:
        selected_id = int(input("🎯 Enter the ID of the JD to match candidates for: "))
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
        return

    # 🔍 Fetch selected JD
    cursor.execute("SELECT title, description, vector FROM job_descriptions WHERE id = ?", (selected_id,))
    row = cursor.fetchone()

    if not row:
        print("❌ JD not found.")
        return

    jd_title, jd_description, jd_vector_blob = row
    jd_vector = np.frombuffer(jd_vector_blob, dtype=np.float32)

    print(f"✅ Matching candidates for: {jd_title}")
    print("📦 Comparing against stored CVs...")

    candidates = get_all_candidate_embeddings(cursor)
    results = []

    for candidate_id, name, text in candidates:
        candidate_vector = embedding_model.embed_query(text)
        similarity = cosine_similarity([jd_vector], [candidate_vector])[0][0]
        results.append((name, similarity))

    results.sort(key=lambda x: x[1], reverse=True)

    print("\n🎯 Top Matching Candidates:")
    for name, score in results:
        print(f"🧑 {name}: Match Score = {score:.4f}")

    conn.close()

if __name__ == "__main__":
    match_candidates_to_jd()
