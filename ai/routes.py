from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from database.config import get_db
from backend.services.auth import get_current_user
from ai.ingest import ingest_document
from ai.rag import answer_question

router = APIRouter(prefix="/api/ai", tags=["AI"])

class IngestRequest(BaseModel):
    session_id: str
    user_id: str

class QueryRequest(BaseModel):
    query: str
    session_id: str
    user_id: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@router.post("/ingest", response_model=dict)
async def ingest(file: UploadFile = File(...), request: IngestRequest = Depends(), db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        # Save the uploaded file temporarily
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Call the ingest_document function
        result = ingest_document(file_path, request.session_id, request.user_id)

        # Clean up the temporary file
        import os
        os.remove(file_path)

        return {"status": "success", "ingested_chunks": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during ingestion: {str(e)}")

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        # Call the answer_question function
        result = answer_question(request.query, request.session_id, request.user_id)

        # Extract the answer and sources
        answer = result['answer']
        sources = result['sources']

        return QueryResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during query: {str(e)}")