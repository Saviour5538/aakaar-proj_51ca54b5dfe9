from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID
from database.models import User
from database.config import get_db
from backend.middleware.auth import get_current_user

# Router
router = APIRouter(prefix="/users", tags=["Users"])

# Pydantic schemas
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

# Routes
@router.get("/", response_model=list[UserResponse])
async def list_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = db.query(User).all()
    return [UserResponse(id=user.id, email=user.email, created_at=user.created_at) for user in users]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse(id=user.id, email=user.email, created_at=user.created_at)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: UUID, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user_update.email:
        user.email = user_update.email
    if user_update.password:
        user.password_hash = pwd_context.hash(user_update.password)
    
    db.commit()
    db.refresh(user)
    return UserResponse(id=user.id, email=user.email, created_at=user.created_at)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(user)
    db.commit()
    return None