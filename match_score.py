from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

# ✅ Load model from local path if available
model_path = './local_model'

if os.path.exists(model_path):
    print(f"✅ Loading model from local path: {model_path}")
    model = SentenceTransformer(model_path)
else:
    print("🌐 Local model not found. Falling back to online model...")
    model = SentenceTransformer('paraphrase-MiniLM-L3-v2')


def compute_embedding(text):
    return model.encode([text], convert_to_numpy=True)


def calculate_match_score(jd_text, resume_text):
    jd_embedding = compute_embedding(jd_text)
    resume_embedding = compute_embedding(resume_text)

    similarity = cosine_similarity(jd_embedding, resume_embedding)[0][0]
    score_percentage = round(similarity * 100, 2)

    return score_percentage
