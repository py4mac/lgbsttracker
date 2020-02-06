"""
Internal package providing a Python CRUD interface.
"""
from typing import List

from lgbsttracker.entities import Experiment, ExperimentCreate
from lgbsttracker.services.store._experiment_registry import utils


class ExperimentService(object):
    """
    Experiment Service.
    """

    def __init__(self, experiment_uri: str) -> None:
        """
        :param experiment_uri: Address of local or remote experiment db.
        """
        self.experiment_uri = experiment_uri
        self.store = utils._get_store(self.experiment_uri)

    def open(self) -> None:
        """
        Open DB
        """
        self.store.open()

    def close(self) -> None:
        """
        Close DB
        """
        self.store.close()

    async def create_experiment(self, entity: ExperimentCreate,) -> Experiment:
        """
        Create experiment entity.

        :param entity: :py:class:`lgbsttracker.entities.ExperimentCreate` entity

        :return: None
        """
        return await self.store.create_experiment(entity)

    async def get_experiment_by_uuid(self, uuid: str) -> List[Experiment]:
        """
        Get Experiment entry by name.
        :param uuid: Experiment UUID.

        :return: A list :py:class:`lgbsttracker.entities.Experiment` entities
        """
        return await self.store.get_experiment_by_uuid(uuid)
