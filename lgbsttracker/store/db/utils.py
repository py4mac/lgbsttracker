import logging
import sqlalchemy
from contextlib import contextmanager

from lgbsttracker.store.sensors.dbmodels.initial_models import Base as InitialBase
from lgbsttracker.exceptions import LgbsttrackerException
from lgbsttracker.protos.common_pb2 import INTERNAL_ERROR

_logger = logging.getLogger(__name__)


def create_sqlalchemy_engine(db_uri):
    return sqlalchemy.create_engine(db_uri)


def _get_managed_session_maker(SessionMaker):
    """
    Creates a factory for producing exception-safe SQLAlchemy sessions that are made available
    using a context manager. Any session produced by this factory is automatically committed
    if no exceptions are encountered within its associated context. If an exception is
    encountered, the session is rolled back. Finally, any session produced by this factory is
    automatically closed when the session's associated context is exited.
    """

    @contextmanager
    def make_managed_session():
        """Provide a transactional scope around a series of operations."""
        session = SessionMaker()
        try:
            yield session
            session.commit()
        except LgbsttrackerException:
            session.rollback()
            raise
        except Exception as e:
            session.rollback()
            raise LgbsttrackerException(message=e, error_code=INTERNAL_ERROR)
        finally:
            session.close()

    return make_managed_session


def _initialize_tables(engine):
    _logger.info("Creating initial database tables...")
    InitialBase.metadata.create_all(engine)
