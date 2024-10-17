# Project: luchoh.com refactoring
# File: backend/app/crud/base.py

"""Base CRUD (Create, Read, Update, Delete) operations for database models."""

from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

ModelT = TypeVar("ModelT")
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)


class CRUDBase(Generic[ModelT, CreateSchemaT, UpdateSchemaT]):
    """
    Base class for CRUD operations on a SQLAlchemy model.
    """

    def __init__(self, model: Type[ModelT]):
        """
        Initialize the CRUD object with a SQLAlchemy model.
        """
        self.model = model

    def get(self, db: Session, id_: int) -> ModelT:
        """
        Retrieve a single record by ID.
        """
        return db.query(self.model).filter(self.model.id == id_).first()

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> list[ModelT]:
        """
        Retrieve multiple records with pagination.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CreateSchemaT) -> ModelT:
        """
        Create a new record.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, db_obj: ModelT, obj_in: UpdateSchemaT
    ) -> ModelT:
        """
        Update an existing record.
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id_: int) -> ModelT:
        """
        Delete a record by ID.
        """
        obj = db.query(self.model).get(id_)
        db.delete(obj)
        db.commit()
        return obj
