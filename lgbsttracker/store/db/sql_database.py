"""
Database module.
Defines types, functions and primitives for the initialization, disposition and management of
  database connections and their sessions.
"""
from typing import Callable

from sqlalchemy import create_engine as _sa_create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session as SQLAlchemySession, scoped_session, sessionmaker
from sqlalchemy.schema import MetaData

from lgbsttracker.exceptions import DatabaseNotInitialized
from lgbsttracker.store.db.sql_background import run_async
from lgbsttracker.store.db.sql_base import CustomBase
from lgbsttracker.utils import env

__all__ = [
    "transactional_session",
    "DatabaseManager",
    "db",
]

schema = env.get_env("SCHEMA", "public")
min_connection_pool_size = env.get_env("MIN_CONNECTION_POOL_SIZE", 10)
max_connection_pool_size = env.get_env("MAX_CONNECTION_POOL_SIZE", 20)
connection_pool_recycle_time = env.get_env("CONNECTION_POOL_RECYCLE_TIME", 30)


###
# Context Manager for Transactional Session Management
#
class transactional_session:
    """
    Context manager which provides transactional session management.
    Supports the sync/async context manager protocols.
    """

    def __init__(self, expire_on_commit: bool = True):
        """
        Initializer.
        :param bool expire_on_commit: If True, will make a session the expires all objects in memory after commit;
            otherwise, will make objects in memory accessible even after session.commit() is called.
        """
        if db.Session is None or db.OnCommitExpiringSession is None:
            raise DatabaseNotInitialized(message="The global database.db singleton is not initialized!")

        self._session = None
        self._expire_on_commit = expire_on_commit

    ###
    # Synchronous context manager protocol
    #
    def __enter__(self) -> SQLAlchemySession:
        if self._expire_on_commit is True:
            self._session = db.OnCommitExpiringSession()
        else:
            self._session = db.Session()

        return self._session  # type: ignore

    def __exit__(self, exc_type, exc, tb):
        try:
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            _logger.error(e)
            raise e
        finally:
            self._session.close()

    ###
    # Asynchronous context manager protocol
    #
    async def __aenter__(self) -> SQLAlchemySession:
        if self._expire_on_commit is True:
            self._session = db.OnCommitExpiringSession()
        else:
            self._session = db.Session()

        return self._session  # type: ignore

    async def __aexit__(self, exc_type, exc, tb):
        try:
            await run_async(self._session.commit)
        except Exception as e:
            await run_async(self._session.rollback)
            _logger.error(e)
            raise e
        finally:
            self._session.close()


###
# Database Manager
#
class DatabaseManager:
    """
    Configuration class for DB that encapsulates engine and configured class for creating scoped session instances.
    """

    def __init__(self):
        ###
        # Private database engine and metadata attributes.
        #
        self._engine = None
        self._metadata = MetaData(schema=schema)

        ###
        # Session Factory classes, later initialized in self.initialize() method.
        #
        # The self.Session corresponds to a session factory that doesn't expire ORM instances from memory
        #   after getting committed.
        #
        # The self.OnCommitExpiringSession corresponds to a session factory that expires ORM instances from
        #   memory after getting committed.
        #
        self.Session = None
        self.OnCommitExpiringSession = None

        ###
        # Declarative Base Model class.
        #
        self.BaseModel = declarative_base(cls=CustomBase, metadata=MetaData(schema=schema))

    @property
    def engine(self) -> Engine:
        return self._engine

    @classmethod
    def create_database_engine(cls, db_uri: str) -> Engine:
        """
        Creates a new SQLAlchemy database engine (sqlalchemy.engine.base.Engine) and returns it.
        :return: a working SQLAlchemy database engine
        """
        ###
        # Database configuration options
        #
        # # Database connection pool settings
        min_pool_size = min_connection_pool_size
        max_pool_size = max_connection_pool_size

        if max_pool_size < min_pool_size:
            raise ValueError("Max Pool Size cannot be lower than Min Pool Size!")

        max_pool_overflow = max_pool_size - min_pool_size
        pool_recycle_time = connection_pool_recycle_time

        return _sa_create_engine(
            db_uri,
            encoding="utf-8",
            pool_size=min_pool_size,
            max_overflow=max_pool_overflow,
            pool_recycle=pool_recycle_time,
        )

    def initialize(self, db_uri: str, db_engine: Engine = None, scope_function: Callable = None):
        """
        Configure class for creating scoped sessions.
        :param db_engine: DB connection engine.
        :param scope_function: a function for scoping database connections.
        """
        # Set or initialize the database engine
        if db_engine is None:
            self._engine = self.create_database_engine(db_uri)
        else:
            self._engine = db_engine

        # Create the session factory classes
        self.Session = scoped_session(sessionmaker(bind=self._engine, expire_on_commit=False), scopefunc=scope_function)

        self.OnCommitExpiringSession = scoped_session(
            sessionmaker(bind=self._engine, expire_on_commit=True), scopefunc=scope_function
        )

    def cleanup(self):
        """
        Cleans up the database connection pool.
        """
        if self._engine is not None:
            self._engine.dispose()


###
# Database Extension
#
db = DatabaseManager()
