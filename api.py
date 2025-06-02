from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import utils

app = FastAPI(title="Skincare Recommendation API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class RecommendationFinalRequest(BaseModel):
    query: str
    answers: str

class RAGRequest(BaseModel):
    results: Dict[str, Any]
    user_question: str
    
    class Config:
        schema_extra = {
            "example": {
                "results": {
                    "documents": [
                        ["Context document 1 content...", "Context document 2 content..."]
                    ]
                },
                "user_question": "What are the key points?"
            }
        }

class ProductsRequest(BaseModel):
    query: str
    # Note: In a real application, you'd want to handle the catalog_collection properly
    # This is a simplified version

@app.post("/api/intent")
async def get_intent(request: QueryRequest):
    """
    Classifies a user query as either 'Recommendation' or 'Non-Recommendation'.
    """
    try:
        intent = utils.findIntent(request.query)
        return {"intent": intent.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recommendation/questions")
async def get_recommendation_questions(request: QueryRequest):
    """
    Generates follow-up questions for recommendation queries.
    """
    try:
        questions = utils.recommQuestion(request.query)
        return {"questions": questions.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recommendation/final")
async def get_final_recommendation(request: RecommendationFinalRequest):
    """
    Creates a structured query based on user's initial query and follow-up answers.
    """
    try:
        result = utils.recommFinalQuery(request.query, request.answers)
        return {"recommendation": result.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rag")
async def get_rag_response(request: RAGRequest):
    """
    Answers questions using provided context through RAG (Retrieval-Augmented Generation).
    
    Request body should contain:
    - results: Dict containing 'documents' key with a list of context strings
    - user_question: The question to be answered based on the provided context
    """
    try:
        # Input validation
        if not request.results or 'documents' not in request.results:
            raise HTTPException(
                status_code=400,
                detail="Invalid input: 'results' must contain 'documents' key with a list of context strings"
            )
            
        if not request.user_question or not request.user_question.strip():
            raise HTTPException(
                status_code=400,
                detail="Invalid input: 'user_question' cannot be empty"
            )
            
        # Validate documents format
        if not isinstance(request.results['documents'], list) or not all(isinstance(doc, str) for doc in request.results['documents']):
            raise HTTPException(
                status_code=400,
                detail="Invalid format: 'documents' must be a list of strings"
            )
        
        # Call the RAG function
        response = utils.RAG(request.results, request.user_question)
        
        if not response or not response.strip():
            return {
                "response": "No relevant information found in the provided context.",
                "status": "success",
                "debug": {
                    "context_count": len(request.results['documents']),
                    "question_length": len(request.user_question)
                }
            }
            
        return {
            "response": response.strip(),
            "status": "success",
            "debug": {
                "response_length": len(response),
                "context_count": len(request.results['documents'])
            }
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
        
    except Exception as e:
        # Log the full error for debugging
        import traceback
        error_details = {
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }
        raise HTTPException(
            status_code=500,
            detail={
                "message": "An error occurred while processing your request",
                "error": str(e),
                "type": type(e).__name__
            }
        )

@app.post("/api/products")
async def get_products(request: ProductsRequest):
    """
    Retrieves and sorts products based on a query.
    Note: This is a simplified version. In a real application, you'd need to handle the catalog_collection properly.
    """
    try:
        # In a real application, you'd want to properly initialize and pass the catalog_collection
        # For now, we'll return a not implemented response
        raise HTTPException(status_code=501, detail="Product search functionality not fully implemented")
        # products = utils.getProducts(request.query, catalog_collection)
        # return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
