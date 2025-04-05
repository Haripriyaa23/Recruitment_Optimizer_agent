from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from database import create_tables
from agents.embed_jd import embed_job_description
from agents.cv_parser_2 import process_resume  # A wrapper for full PDF parsing flow


import sqlite3

# Sanity check right after table creation
conn = sqlite3.connect("candidates.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("🗂 Tables present in DB:", tables)
conn.close()

# 👷 Step 1: Set up DB
create_tables()

# 🧩 Step 2: Define graph state
# We'll use a dictionary to pass state around
def start(state):
    print("🚀 LangGraph workflow starting...")
    return state

# 📌 Node: Embedding Job Description
embed_jd_node = RunnableLambda(lambda state: {
    **state,
    "jd_result": embed_job_description()
})

# 📄 Node: Parsing Resume
parse_cv_node = RunnableLambda(lambda state: {
    **state,
    "cv_result": process_resume()
})

# 🧠 Step 3: Build LangGraph with nodes
graph = StateGraph(dict)

graph.add_node("start", start)
graph.add_node("embed_jd", embed_jd_node)
graph.add_node("parse_cv", parse_cv_node)

# 🔀 Transitions
graph.set_entry_point("start")
graph.add_edge("start", "embed_jd")
graph.add_edge("embed_jd", "parse_cv")
graph.add_edge("parse_cv", END)

# 🏁 Step 4: Compile and run
app = graph.compile()
final_state = app.invoke({})

print("🎉 Done! Final state:")
print(final_state)

from match_score import calculate_match_score

jd_text = final_state.get("jd_result", "")
resume_text = final_state.get("cv_result", "")

if jd_text and resume_text:
    score = calculate_match_score(jd_text, resume_text)
    print(f"🔥 Match Score: {score}%")
else:
    print("⚠️ Could not calculate score. Missing JD or Resume content.")

