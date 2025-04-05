from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 🔍 Load your model (you can switch to deepseek-embedding later)
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')  # lightweight & fast


def compute_embedding(text):
    return model.encode([text], convert_to_tensor=True)


def calculate_match_score(jd_text, resume_text):
    jd_embedding = compute_embedding(jd_text)
    resume_embedding = compute_embedding(resume_text)

    similarity = cosine_similarity(jd_embedding, resume_embedding)[0][0]
    score_percentage = round(similarity * 100, 2)

    return score_percentage
