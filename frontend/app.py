import streamlit as st
import requests

# --- UI Configuration --- #
st.set_page_config(
    page_title="Smart Research Agent",
    layout="wide"  # Better use of screen space
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Report box styling */
    .report { 
        padding: 20px; 
        border-radius: 10px; 
        background: #9fb8d1; 
        color: #5b5e61; 
        margin-bottom: 15px;
    }
    
    /* Source listing styling */
    .source { 
        font-size: 0.9em; 
        color: #666; 
        border-left: 3px solid #ddd; 
        padding-left: 10px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Header Section --- #
st.title("🔍 Smart Research Agent By Toufik Mechouma")
st.write("Ask your question and get a sourced answer")

# --- Main Form --- #
with st.form("research_form"):  
  query = st.text_input(
      "Your question",
      placeholder="Example: Who invented the World Wide Web?"
  )
  submitted = st.form_submit_button("Search")

# --- Results Handling --- #
if submitted and query:
  with st.spinner("🔎 Searching..."):
    try:
      # Call our FastAPI endpoint
      response = requests.post(
          "http://localhost:8000/research",
          json={"text": query, "max_results": 3}
      ).json()
      print("API Response:", response)  # Debug
      
      # --- Display Results --- #
      # 1. Main Answer
      st.markdown(f"### 📝 Answer")
      st.markdown(
          f'<div class="report">{response["answer"]}</div>',
          unsafe_allow_html=True
      )
      
      # 2. Sources
      st.markdown("### 📚 Sources")
      for i, source in enumerate(response["sources"]):
        print(i,':',source)
        st.markdown(f"""
        <div class="source">
            {i+1}. <a href="{source['url']}" target="_blank">{source['title']}</a>
        </div>
        """, unsafe_allow_html=True)
            
    except Exception as e:
      st.error(f"Error during research: {str(e)}")

# --- Sidebar --- #
with st.sidebar:
  st.markdown("## About")
  st.info("""
  **Technologies used:**
  - Mistral 7B (local LLM via Ollama)
  - ChromaDB (vector database)
  - Web scraping (Google Search)
  """)
