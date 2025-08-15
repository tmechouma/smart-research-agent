# Smart Research Agent

An AI-powered research assistant that:
1. Searches the web for relevant information
2. Processes results using Mistral 7B LLM
3. Provides sourced answers to user questions

## Features
- Web search integration (SerpAPI)
- Local LLM processing via Ollama
- Vector database caching with ChromaDB
- Streamlit frontend
- FastAPI backend

## Setup

1. Clone the repository
2. Install requirements for both frontend and backend
3. Set up Ollama with Mistral 7B
4. Configure SerpAPI key in research.py
5. Run the FastAPI backend: `uvicorn main:app --reload`
6. Run the Streamlit frontend: `streamlit run app.py`

## Configuration
- Set environment variables in `.env` file:
  - SERPAPI_KEY=your_api_key
  - HOST=0.0.0.0
  - PORT=8000
