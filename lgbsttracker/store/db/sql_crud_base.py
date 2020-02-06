from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from lgbsttracker.store.db.sql_background import run_async
from lgbsttracker.store.db.sql_database import db

ModelType = TypeVar("ModelType", bound=db.BaseModel)  # type: ignore
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db_session: Session, id: int) -> Optional[ModelType]:
        return await run_async(db_session.query(self.model).filter(self.model.id == id).first)  # type: ignore

    async def get_multi(self, db_session: Session, *, skip=0, limit=100) -> List[ModelType]:
        return await run_async(db_session.query(self.model).offset(skip).limit(limit).all)

    async def create(self, db_session: Session, *, obj_in: CreateSchemaType) -> ModelType:
        def _create(db_session, obj_in):
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            db_session.add(db_obj)
            db_session.commit()
            db_session.refresh(db_obj)
            return db_obj

        return await run_async(_create, db_session, obj_in)

    async def update(self, db_session: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        def _update(db_session, db_obj, obj_in):
            obj_data = jsonable_encoder(db_obj)
            update_data = obj_in.dict(skip_defaults=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db_session.add(db_obj)
            db_session.commit()
            db_session.refresh(db_obj)
            return db_obj

        return await run_async(_update, db_session, db_obj, obj_in)

    async def remove(self, db_session: Session, *, id: int) -> ModelType:
        def _remove(db_session, model, id):
            obj = db_session.query(model).get(id)
            db_session.delete(obj)
            db_session.commit()
            return obj

        return await run_async(_remove, db_session, self.model, id)
