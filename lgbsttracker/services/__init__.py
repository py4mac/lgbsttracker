import logging

from lgbsttracker.entities import Experiment, ExperimentCreate
from lgbsttracker.services.store._experiment_registry.service import ExperimentService

# TODO: rework using logger
_logger = logging.getLogger(__name__)

_experiment_service = None


def _get_experiment_service(uri=None):
    from lgbsttracker.services.store._experiment_registry import utils

    global _experiment_service
    if _experiment_service is None:
        experiment_uri = uri or utils.get_experiment_uri()
        _experiment_service = ExperimentService(experiment_uri)
        _experiment_service.open()
    return _experiment_service


async def create_experiment(entity: ExperimentCreate) -> Experiment:
    return await _get_experiment_service().create_experiment(entity)


async def get_experiment_by_uuid(uuid: str) -> Experiment:
    return await _get_experiment_service().get_experiment_by_uuid(uuid)
