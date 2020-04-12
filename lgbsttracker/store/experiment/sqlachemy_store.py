import logging
from typing import List

from sqlalchemy.orm import Session

from lgbsttracker.entities.experiment import ExperimentCreate, ExperimentUpdate
from lgbsttracker.store.db.sql_background import run_async
from lgbsttracker.store.db.sql_crud_base import CRUDBase
from lgbsttracker.store.db.sql_database import db, schema, transactional_session
from lgbsttracker.store.experiment.abstract_store import AbstractStore
from lgbsttracker.store.experiment.dbmodels.experiment import Experiment

_logger = logging.getLogger()


class CRUDExperiment(CRUDBase[Experiment, ExperimentCreate, ExperimentUpdate]):
    async def get_by_uuid(self, db_session: Session, *, uuid: str) -> List[Experiment]:
        def _get_by_uuid(db_session: Session, uuid: str):
            ret = db_session.query(Experiment).filter(Experiment.experiment_uuid == uuid).all()
            # Hard trick here as the session could expire here.
            db_obj = [
                Experiment(
                    id=e.id, experiment_uuid=e.experiment_uuid, ts=e.ts, action=e.action, vision_sensor=e.vision_sensor, speed=e.speed, state=e.state,
                )
                for e in ret
            ]
            return db_obj

        return await run_async(_get_by_uuid, db_session, uuid)

    async def create(self, db_session: Session, *, obj_in: ExperimentCreate) -> Experiment:
        def _create(db_session: Session, obj_in: ExperimentCreate):
            db_obj = Experiment(experiment_uuid=obj_in.experiment_uuid)
            db_session.add(db_obj)
            db_session.commit()
            db_session.refresh(db_obj)
            return Experiment(
                id=db_obj.id,
                experiment_uuid=db_obj.experiment_uuid,
                ts=db_obj.ts,
                action=db_obj.action,
                vision_sensor=db_obj.vision_sensor,
                speed=db_obj.speed,
                state=db_obj.state,
            )

        return await run_async(_create, db_session, obj_in)


experiment = CRUDExperiment(Experiment)


class SqlAlchemyStore(AbstractStore):
    def __init__(self, db_uri):
        super(SqlAlchemyStore, self).__init__()
        self.db_uri = db_uri

    def open(self):
        db.initialize(self.db_uri)
        # Check if the table exist
        if not db.engine.dialect.has_table(db.engine, Experiment.__tablename__, schema):
            _logger.info("Creating 'experiment' database")
            Experiment.__table__.create(bind=db.engine)

    def close(self):
        db.cleanup()

    async def create_experiment(self, entity: ExperimentCreate) -> Experiment:
        async with transactional_session() as session:
            _experiment = await experiment.create(session, obj_in=entity)
            return _experiment

    async def get_experiment_by_uuid(self, uuid: str) -> List[Experiment]:
        async with transactional_session() as session:
            _experiments = await experiment.get_by_uuid(session, uuid=uuid)
            return _experiments
