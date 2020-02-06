import logging
import os

import sqlalchemy
import sqlalchemy_utils

_logger = logging.getLogger(__name__)


def _create_sqlalchemy_engine(db_uri):
    return sqlalchemy.create_engine(db_uri)


def _get_package_dir():
    """Returns directory containing python package."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(current_dir, os.pardir, os.pardir))


def _get_alembic_config(db_url, alembic_dir=None):
    """
    Constructs an alembic Config object referencing the specified database and migration script
    directory.

    :param db_url Database URL, like sqlite:///<absolute-path-to-local-db-file>. See
    https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls for a full list of valid
    database URLs.
    :param alembic_dir Path to migration script directory. Uses canonical migration script
    directory under mlflow/alembic if unspecified. TODO: remove this argument in MLflow 1.1, as
    it's only used to run special migrations for pre-1.0 users to remove duplicate constraint
    names.
    """
    from alembic.config import Config

    final_alembic_dir = (
        os.path.join(_get_package_dir(), "store", "db_migrations") if alembic_dir is None else alembic_dir
    )
    config = Config(os.path.join(final_alembic_dir, "alembic.ini"))
    config.set_main_option("script_location", final_alembic_dir)
    config.set_main_option("sqlalchemy.url", db_url)
    return config


def upgrade_sql_db(url):
    """
    Upgrade Model DB and create DataBase if not exists

    :param url Database URL
    """
    # alembic adds significant import time, so we import it lazily
    from alembic import command

    engine = _create_sqlalchemy_engine(url)
    if not sqlalchemy_utils.database_exists(engine.url):
        sqlalchemy_utils.create_database(engine.url)
    _logger.info("Updating database tables at %s", url)
    config = _get_alembic_config(url)
    command.upgrade(config, "heads")
