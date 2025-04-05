import pickle
import faiss
import numpy as np
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from database import get_latest_cv_entry  # 🔥 This will pull structured fields from the DB

# Load environment variables (if any)
load_dotenv()

# Path to store CV FAISS index
CV_FAISS_INDEX_PATH = "cv_faiss_index"

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def combine_cv_fields(cv_data):
    """Combine important CV fields into a single string for embedding."""
    return f"""
    Name: {cv_data['name']}
    Email: {cv_data['email']}
    Phone: {cv_data['phone']}
    Skills: {', '.join(cv_data['skills'])}
    Education: {cv_data['education']}
    Projects: {cv_data['projects']}
    Certifications: {', '.join(cv_data['certifications'])}
    """


def embed_and_store_cv(cv_data):
    combined_text = combine_cv_fields(cv_data)
    print("📦 Embedding the combined CV text...")

    embedding = embedding_model.embed_documents([combined_text])
    embedding = np.array(embedding).astype('float32')

    index = faiss.IndexFlatL2(len(embedding[0]))
    index.add(embedding)
    faiss.write_index(index, CV_FAISS_INDEX_PATH)

    # Store metadata
    with open("cv_metadata.pkl", "wb") as f:
        pickle.dump({"cv_text": combined_text}, f)

    print("✅ CV embedding stored successfully!")


# Entry point
if __name__ == "__main__":
    print("🔍 Fetching latest CV from DB...")
    cv_data = get_latest_cv_entry()  # You implement this 👇

    if cv_data:
        embed_and_store_cv(cv_data)
    else:
        print("❌ No CV data found in the database.")
