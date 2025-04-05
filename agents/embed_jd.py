import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings
from database import store_job_description


def embed_job_description(text):
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # You define how to split title & description from text
    parts = text.strip().split("\n", 1)  # first line = title, rest = desc
    title = parts[0]
    description = parts[1] if len(parts) > 1 else ""

    vector = embedding_model.embed_query(description)
    vector_bytes = np.array(vector, dtype=np.float32).tobytes()
    store_job_description(title, description, vector_bytes)
    return {"title": title, "vector": vector_bytes}

