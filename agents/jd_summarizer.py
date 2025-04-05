from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

from tools import extract_text_from_pdf

load_dotenv()

llm = ChatOllama(
    model="deepseek-r1:1.5b",
    base_url="http://localhost:11434",
    temperature=0,
)

def summarize_jd(pdf_path):
    jd_text = extract_text_from_pdf(pdf_path)
    jd_details_extracter_prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """ Summarize the key elements from the Job Description.
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
    ).partial(jd_text = jd_text)

    formatted_prompt = jd_details_extracter_prompt_template.format_messages()
    res = llm.invoke(formatted_prompt)
    return res.content


print("hello")
res = summarize_jd("C:/Users/Hi/Recruitment-optimizer-agent/JEO - JD - Lumina Datamatics.pdf")
print(res)
print("hi")



