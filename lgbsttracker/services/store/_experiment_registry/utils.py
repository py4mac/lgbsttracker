from __future__ import print_function

from lgbsttracker.errors import ErrorCodes
from lgbsttracker.exceptions import GenericException
from lgbsttracker.services.store._experiment_registry.registry import ExperimentStoreRegistry
from lgbsttracker.utils import env

_EXPERIMENT_URI_ENV_VAR = "EXPERIMENT_STORAGE_URI"

_experiment_uri = None


def is_experiment_uri_set():
    """Returns True if the experiment URI has been set, False otherwise."""
    if _experiment_uri or env.get_env(_EXPERIMENT_URI_ENV_VAR):
        return True
    return False


def set_experiment_uri(uri):
    """
    Set the Experiment URI storage.
    :param uri: Input parameter string
    """
    global _experiment_uri
    _experiment_uri = uri


def get_experiment_uri():
    """
    Get the Experiment URI storage.

    :return: The Experiment URI.
    """
    global _experiment_uri
    if _experiment_uri is not None:
        return _experiment_uri
    elif env.get_env(_EXPERIMENT_URI_ENV_VAR) is not None:
        return env.get_env(_EXPERIMENT_URI_ENV_VAR)
    else:
        raise GenericException("Storage Experiment URI store is not set", error=ErrorCodes.INTERNAL_ERROR)


def _get_sqlalchemy_store(experiment_uri):
    from lgbsttracker.store.experiment.sqlachemy_store import SqlAlchemyStore

    return SqlAlchemyStore(db_uri=experiment_uri)


_experiment_store_registry = ExperimentStoreRegistry()
_experiment_store_registry.register("sqlite", _get_sqlalchemy_store)
_experiment_store_registry.register("postgresql", _get_sqlalchemy_store)

_experiment_store_registry.register_entrypoints()


def _get_store(experiment_uri=None):
    return _experiment_store_registry.get_store(experiment_uri)
