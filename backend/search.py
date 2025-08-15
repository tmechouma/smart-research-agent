import ollama
from sentence_transformers import SentenceTransformer
import chromadb
from bs4 import BeautifulSoup
import requests

# Initialize ChromaDB client with telemetry disabled
chroma_client = chromadb.Client(settings=chromadb.config.Settings(anonymized_telemetry=False))

# --- Initialization --- #
# Text embedding model (runs locally)
encoder = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight model

# Vector database setup
collection = chroma_client.create_collection("research_cache")  # Stores past queries/results

def web_search(query: str, max_results: int = 3):
  """
  Perform a web search using SerpAPI
  Args:
      query: Search query string
      max_results: Maximum number of results to return
  Returns:
      List of dictionaries containing title and URL for each result
  """
  try:
    api_key = "239a39a6a9e0e93a03e1e54jgd5fkdfdg557e2e46eae91f84a"  # Replace with actual key
    params = {
        "q": query,
        "engine": "google",
        "api_key": api_key,
        "num": max_results
    }
    response = requests.get("https://serpapi.com/search.json", params=params)
    
    if response.status_code == 200:
      data = response.json()
      return [{"title": r["title"], "url": r["link"]} for r in data.get("organic_results", [])]
    else:
      print(f"Error {response.status_code}: {response.text}")
      return []    
  except Exception as e:
    print("ERROR in web_search():", str(e))  # Log error
    return []      

def process_query(query: str, max_results: int = 3):
  """
  Process a research query by:
  1. Performing web search
  2. Generating answer using Mistral LLM
  3. Returning answer with sources
  
  Args:
      query: The research question
      max_results: Number of sources to include
      
  Returns:
      Dictionary with 'answer' and 'sources' keys
  """
  try:
    # 1. Web search via API
    web_results = web_search(query, max_results)
    
    # Save results to file for debugging (optional)
    with open("search_results.txt", 'w', encoding='utf-8') as file:
        file.write(str(web_results))
        
    # 2. Generate answer with Mistral
    prompt = f"""
    Question: {query}
    Context: {[r['title'] + ' (' + r['url'] + ')' for r in web_results]}
    Answer in French citing sources when possible. Example: "According to [Source](url)..."
    Answer:
    """
    response = ollama.generate(
        model='mistral',
        prompt=prompt,
        stream=False
    )
    
    return {
        "answer": response['response'],
        "sources": web_results
    }
  except Exception as e:
    return {
        "answer": f"Error: {str(e)}",
        "sources": []
    }
