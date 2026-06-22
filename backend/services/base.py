from typing import Type, TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from database.config import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDService(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, obj_in: dict) -> ModelType:
        try:
            db_obj = self.model(**obj_in)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating {self.model.__name__}: {str(e)}")

    def read(self, db: Session, id: uuid.UUID) -> Optional[ModelType]:
        try:
            return db.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Error reading {self.model.__name__}: {str(e)}")

    def update(self, db: Session, id: uuid.UUID, obj_in: dict) -> Optional[ModelType]:
        try:
            db_obj = db.query(self.model).filter(self.model.id == id).first()
            if not db_obj:
                raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
            for key, value in obj_in.items():
                setattr(db_obj, key, value)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating {self.model.__name__}: {str(e)}")

    def delete(self, db: Session, id: uuid.UUID) -> bool:
        try:
            db_obj = db.query(self.model).filter(self.model.id == id).first()
            if not db_obj:
                raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
            db.delete(db_obj)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error deleting {self.model.__name__}: {str(e)}")