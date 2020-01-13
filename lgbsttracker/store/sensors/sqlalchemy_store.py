import logging
import sqlalchemy

import lgbsttracker
from lgbsttracker.store.db.base_sql_model import Base
from lgbsttracker.entities import LightSensor
from lgbsttracker.exceptions import LgbsttrackerException
from lgbsttracker.protos.common_pb2 import INVALID_PARAMETER_VALUE, RESOURCE_ALREADY_EXISTS, INVALID_STATE, RESOURCE_DOES_NOT_EXIST, INTERNAL_ERROR
from lgbsttracker.store.sensors.abstract_store import AbstractStore
from lgbsttracker.store.sensors.dbmodels.sqlalchemy_models import SqlLightSensor
from lgbsttracker.store.db.utils import create_sqlalchemy_engine
from lgbsttracker.utils.uri import extract_host_name_from_uri

_logger = logging.getLogger(__name__)


def now():
    import datetime

    return datetime.datetime.now()


class SqlAlchemyStore(AbstractStore):
    """
    SqlAlchemy Storage
    """

    def __init__(self, db_uri):
        super(SqlAlchemyStore, self).__init__()
        self.db_uri = db_uri
        self.engine = create_sqlalchemy_engine(db_uri)
        Base.metadata.create_all(self.engine)
        # Verify that all model registry tables exist.
        SqlAlchemyStore._verify_registry_tables_exist(self.engine)
        Base.metadata.bind = self.engine
        SessionMaker = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.ManagedSessionMaker = lgbsttracker.store.db.utils._get_managed_session_maker(SessionMaker)

    @staticmethod
    def _verify_registry_tables_exist(engine):
        # Verify that all tables have been created.
        inspected_tables = set(sqlalchemy.inspect(engine).get_table_names())
        expected_tables = [SqlLightSensor.__tablename__]
        if any([table not in inspected_tables for table in expected_tables]):
            lgbsttracker.store.db.utils._initialize_tables(engine)

    def _save_to_db(self, session, objs):
        """
        Store in db
        """
        if type(objs) is list:
            session.add_all(objs)
        else:
            # single object
            session.add(objs)

    def create_light_sensor(self, name):
        with self.ManagedSessionMaker() as session:
            try:
                creation_time = now()
                service = SqlLightSensor(name=name, creation_time=creation_time, last_updated_time=None)
                self._save_to_db(session, service)
                session.flush()
                return service.to_entity()
            except sqlalchemy.exc.IntegrityError as e:
                raise LgbsttrackerException("Something wrongs happens while creating light sensor. " "Error: {}".format(str(e)), INTERNAL_ERROR)
