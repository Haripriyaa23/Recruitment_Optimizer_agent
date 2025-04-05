import os
import faiss
import pickle
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from tools import extract_text_from_pdf  # Assuming this extracts text from a PDF
import numpy as np

# Load environment variables (if any)
load_dotenv()

# Initialize the LLM (DeepSeek)
llm = ChatOllama(
    model="deepseek-r1:1.5b",
    base_url="http://localhost:11434",
    temperature=0,
)

# Initialize HuggingFace Embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Path for FAISS index storage
FAISS_INDEX_PATH = "jd_faiss_index"

def summarize_jd(pdf_path):
    """Extract and summarize the Job Description (JD) using an LLM."""
    jd_text = extract_text_from_pdf(pdf_path)

    # Prompt to summarize JD
    jd_prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Summarize the key elements from the Job Description.
                Extract and present the following details in a structured manner:

                1. **Required skills**,
                2. **Experience**,
                3. **Qualifications**,
                4. **Job Responsibilities**.

                Ensure the response is **clear, concise, and formatted in bullet points**.
                Job Description: {jd_text}
                """
            )
        ]
    ).partial(jd_text=jd_text)

    formatted_prompt = jd_prompt_template.format_messages()
    res = llm.invoke(formatted_prompt)
    return res.content, jd_text  # Return both summary and full text


import numpy as np  # make sure this is imported at the top


def store_jd_embeddings(jd_text, jd_summary):
    """Generate embeddings and store them in FAISS."""
    embeddings = embedding_model.embed_documents([jd_text, jd_summary])

    # 💡 Convert list of lists into a NumPy array
    embeddings = np.array(embeddings).astype('float32')

    # Create a FAISS index and add embeddings
    index = faiss.IndexFlatL2(len(embeddings[0]))  # L2 (Euclidean) index
    index.add(embeddings)

    # Save FAISS index
    faiss.write_index(index, FAISS_INDEX_PATH)

    # Store metadata separately
    metadata = {"jd_text": jd_text, "jd_summary": jd_summary}
    with open("jd_metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print("✅ JD Embeddings stored successfully!")

# Run the process
if __name__ == "__main__":
    print("Processing JD...")
    pdf_path = "C:/Users/Hi/Recruitment-optimizer-agent/JEO - JD - Lumina Datamatics.pdf"
    jd_summary, jd_text = summarize_jd(pdf_path)

    print("\n🔹 JD Summary:\n", jd_summary)

    print("\nStoring JD Embeddings in FAISS...")
    store_jd_embeddings(jd_text, jd_summary)

    print("✅ Done!")
