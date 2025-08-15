from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import logging
import os
import research  # Custom research processing module
import uvicorn

# Setup logging
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Smart Research Agent API",
    description="API for conducting AI-powered research",
    version="1.0.0"
)

# Data Models
class Query(BaseModel):
  text: str
  max_results: int = Field(
      default=3, 
      gt=0, 
      le=10, 
      description="Number of sources to return (1-10)"
  )

class ResearchResponse(BaseModel):
  query: str
  sources: list[dict[str, str]]
  answer: str

# API Endpoints
@app.get("/", summary="Health check")
async def root():
  """Check if API is running"""
  return {"message": "Smart Research Agent API is running"}
    
@app.post("/research", response_model=ResearchResponse)
async def conduct_research(query: Query):
  """
  Process a research query and return:
  - Generated answer
  - List of sources with titles and URLs
  
  Args:
      query: The research question and parameters
      
  Returns:
      ResearchResponse containing answer and sources
  """
  try:
    logger.info(f"Processing query: {query.text}")
    result = research.process_query(
        query.text,
        max_results=query.max_results
    )
    return ResearchResponse(
        query=query.text,
        sources=result["sources"],
        answer=result["answer"]
    )
  except Exception as e:
    logger.error(f"Research failed: {str(e)}")
    raise HTTPException(
        status_code=500,
        detail=f"Research failed: {str(e)}"
    )

if __name__ == "__main__":
  uvicorn.run(
      app,
      host=os.getenv("HOST", "0.0.0.0"),
      port=int(os.getenv("PORT", "8000")),
      log_level="info"
  )