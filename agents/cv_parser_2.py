from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import json
import re

from database import create_tables, store_cv

# ✅ Set Tesseract path (update if installed elsewhere)
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# ✅ Initialize DeepSeek LLM from Ollama
llm = ChatOllama(
    model="deepseek-r1:1.5b",
    base_url="http://localhost:11434",
    temperature=0,
)

def extract_text_from_pdf(pdf_path):
    """Converts PDF pages to text using OCR"""
    images = convert_from_path(pdf_path)
    full_text = ""
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        full_text += f"\n--- Page {i+1} ---\n{text}"
    print(full_text)
    return full_text

def clean_llm_output(output):
    """Extract valid JSON from LLM response using regex and clean line breaks in string values"""
    try:
        # 🧽 Remove <think>...</think> section
        output = re.sub(r"<think>.*?</think>", "", output, flags=re.DOTALL)

        # 🎯 Extract only the JSON object
        json_match = re.search(r"\{.*\}", output, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object found in LLM output.")

        json_text = json_match.group(0)

        # 🧹 Fix invalid control characters (like newlines inside strings)
        json_text = re.sub(r'\n+', ' ', json_text)  # Replace all newlines with space
        json_text = re.sub(r'\s{2,}', ' ', json_text)  # Clean up double/triple spaces

        return json.loads(json_text)
    except Exception as e:
        print("⚠️ Error parsing LLM output:", e)
        print("Raw LLM output:\n", output)
        return {}

def extract_fields_with_llm(resume_text):
    """Uses DeepSeek to extract structured resume data from plain text"""
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system",
            """
            You are a resume parser. Extract the following details from the resume text:
            - name
            - email
            - phone
            - skills (as list) - it should include all the programming languages listed in the resume
            - education (with degree, institution, and year)
            - projects (list of {{title, description}})
            - certifications (as list) - include certifications only if present in the resume text
            
            - Do not use "..." or placeholder values like "more bullet points"
            - Only output valid JSON — no comments, no extra text

            Return them ONLY in this JSON format:
            Return them ONLY in this JSON format (no newlines inside string values).
            Return all JSON fields as single-line strings. Do not use raw line breaks inside values.
            {{
              "name": "...",
              "email": "...",
              "phone": "...",
              "skills": ["...", "..."],
              "education": {{
                "type": "...",
                "institution": "...",
                "year": "..."
              }},
              "projects": [
                {{
                  "title": "...",
                  "description": "..."
                }}
              ],
              "certifications": ["...", "..."]
            }}

            Resume text:
            {resume_text}
            """)
        ]
    ).partial(resume_text=resume_text)

    formatted_prompt = prompt_template.format_messages(resume_text=resume_text)
    res = llm.invoke(formatted_prompt)
    llm_output = res.content if hasattr(res, "content") else res

    print("\n🧠 Extracted Response:\n", llm_output)

    return clean_llm_output(llm_output)

# 🏁 Main Logic
if __name__ == "__main__":
    create_tables()

    resume_path = r"C:/Users/Hi/Recruitment-optimizer-agent/Hari Priyaa Resume (1).pdf"
    resume_text = extract_text_from_pdf(resume_path)

    candidate_data = extract_fields_with_llm(resume_text)

    if candidate_data:
        store_cv(candidate_data)
        print("✅ Resume data stored successfully!")
    else:
        print("❌ Failed to extract or store resume data.")

def process_resume(resume_path):
    resume_text = extract_text_from_pdf(resume_path)
    candidate_data = extract_fields_with_llm(resume_text)
    if candidate_data:
        store_cv(candidate_data)
        return "✅ Resume parsed and stored!"
    else:
        return "❌ Failed to extract/store resume."
