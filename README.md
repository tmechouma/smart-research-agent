# Smart Research Agent

An AI-powered research assistant that:
1. Searches the web for relevant information
2. Processes results using Mistral 7B LLM
3. Provides sourced answers to user questions

![Demo Screenshot](https://github.com/tmechouma/smart-research-agent/blob/main/snapsh.png) 

## Features
- Web search integration (SerpAPI)
- Local LLM processing via Ollama
- Vector database caching with ChromaDB
- Streamlit frontend
- FastAPI backend

## Setup

1. Clone the repository
2. Install requirements for both frontend and backend
3. Set up Ollama with Mistral 7B  (type in terminal after installing Ollama :  `Ollama pull Mistral` )
4. Get and Configure SerpAPI key in research.py
5. In terminal Run 1: `Ollama serve`  
6. Run 2 : the FastAPI backend: `python main.py`
7. Run 3 : the Streamlit frontend: `streamlit run app.py`

## Configuration
  - Set environment variables in `.env` file:
  - SERPAPI_KEY=your_api_key
  - HOST=0.0.0.0
  - PORT=8000
