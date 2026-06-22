from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from uuid import UUID
from sqlalchemy.orm import Session
from typing import List
from database.models import DataChunk
from database.config import get_db
from backend.middleware.auth import get_current_user

router = APIRouter(prefix="/data_ingestion", tags=["Data Ingestion"])

class DataChunkBase(BaseModel):
    sheet_name: str
    row_range: str
    chunk_text: str

class DataChunkCreate(DataChunkBase):
    uploaded_file_id: UUID
    user_id: UUID
    session_id: UUID

class DataChunkResponse(DataChunkBase):
    id: UUID
    embedding: List[float]
    created_at: str

@router.get("/", response_model=List[DataChunkResponse])
async def list_data_chunks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    data_chunks = db.query(DataChunk).filter(DataChunk.user_id == user.id).all()
    return data_chunks

@router.get("/{chunk_id}", response_model=DataChunkResponse)
async def get_data_chunk(chunk_id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)):
    data_chunk = db.query(DataChunk).filter(DataChunk.id == chunk_id, DataChunk.user_id == user.id).first()
    if not data_chunk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data chunk not found")
    return data_chunk

@router.post("/", response_model=DataChunkResponse)
async def create_data_chunk(data: DataChunkCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_chunk = DataChunk(**data.dict(), user_id=user.id)
    db.add(new_chunk)
    db.commit()
    db.refresh(new_chunk)
    return new_chunk

@router.put("/{chunk_id}", response_model=DataChunkResponse)
async def update_data_chunk(chunk_id: UUID, data: DataChunkBase, db: Session = Depends(get_db), user=Depends(get_current_user)):
    data_chunk = db.query(DataChunk).filter(DataChunk.id == chunk_id, DataChunk.user_id == user.id).first()
    if not data_chunk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data chunk not found")
    for key, value in data.dict().items():
        setattr(data_chunk, key, value)
    db.commit()
    db.refresh(data_chunk)
    return data_chunk

@router.delete("/{chunk_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_data_chunk(chunk_id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)):
    data_chunk = db.query(DataChunk).filter(DataChunk.id == chunk_id, DataChunk.user_id == user.id).first()
    if not data_chunk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data chunk not found")
    db.delete(data_chunk)
    db.commit()