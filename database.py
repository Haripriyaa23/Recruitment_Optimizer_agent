import sqlite3
import json
import ast

DB_NAME = "candidates.db"

def create_tables():
    """Creates tables for job descriptions and candidate CVs if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Table for Job Descriptions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_descriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            vector BLOB
        )
    """)

    # Table for Candidate CVs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cvs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            skills TEXT,
            education TEXT,
            projects TEXT,
            experience TEXT,
            certifications TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Tables created (or verified) successfully.")

def store_job_description(title, description, vector):
    """Stores job description and its vector representation in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO job_descriptions (title, description, vector)
        VALUES (?, ?, ?)
    """, (title, description, vector))

    conn.commit()
    conn.close()
    print("✅ Job description stored successfully.")

def store_cv(candidate_data):
    """Stores extracted CV data in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Convert complex fields to JSON strings
    candidate_data["skills"] = json.dumps(candidate_data.get("skills", []))
    candidate_data["education"] = json.dumps(candidate_data.get("education", {}))
    candidate_data["projects"] = json.dumps(candidate_data.get("projects", []))
    candidate_data["experience"] = json.dumps(candidate_data.get("experience", []))
    candidate_data["certifications"] = json.dumps(candidate_data.get("certifications", []))

    cursor.execute("""
        INSERT INTO cvs (name, email, phone, skills, education, projects, experience, certifications)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate_data["name"],
        candidate_data["email"],
        candidate_data["phone"],
        candidate_data["skills"],
        candidate_data["education"],
        candidate_data["projects"],
        candidate_data["experience"],
        candidate_data["certifications"]
    ))

    conn.commit()
    conn.close()
    print("✅ Resume data stored successfully in the database!")

def get_latest_cv_entry():
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, phone, skills, education, projects, certifications FROM cvs ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        name, email, phone, skills, education, projects, certifications = row
        return {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": ast.literal_eval(skills),
            "education": education,
            "projects": projects,
            "certifications": ast.literal_eval(certifications)
        }
    return None
