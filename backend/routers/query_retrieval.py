from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from uuid import UUID
from sqlalchemy.orm import Session
from typing import List
from database.models import QueryHistory
from database.config import get_db
from backend.middleware.auth import get_current_user

router = APIRouter(prefix="/query_retrieval", tags=["Query Retrieval"])

class QueryHistoryBase(BaseModel):
    question: str
    answer: str
    sources: dict

class QueryHistoryCreate(QueryHistoryBase):
    session_id: UUID

class QueryHistoryResponse(QueryHistoryBase):
    id: UUID
    created_at: str

@router.get("/", response_model=List[QueryHistoryResponse])
async def list_query_histories(db: Session = Depends(get_db), user=Depends(get_current_user)):
    query_histories = db.query(QueryHistory).filter(QueryHistory.user_id == user.id).all()
    return query_histories

@router.get("/{query_id}", response_model=QueryHistoryResponse)
async def get_query_history(query_id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query_history = db.query(QueryHistory).filter(QueryHistory.id == query_id, QueryHistory.user_id == user.id).first()
    if not query_history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Query history not found")
    return query_history

@router.post("/", response_model=QueryHistoryResponse)
async def create_query_history(data: QueryHistoryCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_query = QueryHistory(**data.dict(), user_id=user.id)
    db.add(new_query)
    db.commit()
    db.refresh(new_query)
    return new_query

@router.put("/{query_id}", response_model=QueryHistoryResponse)
async def update_query_history(query_id: UUID, data: QueryHistoryBase, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query_history = db.query(QueryHistory).filter(QueryHistory.id == query_id, QueryHistory.user_id == user.id).first()
    if not query_history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Query history not found")
    for key, value in data.dict().items():
        setattr(query_history, key, value)
    db.commit()
    db.refresh(query_history)
    return query_history

@router.delete("/{query_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_query_history(query_id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)):
    query_history = db.query(QueryHistory).filter(QueryHistory.id == query_id, QueryHistory.user_id == user.id).first()
    if not query_history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Query history not found")
    db.delete(query_history)
    db.commit()