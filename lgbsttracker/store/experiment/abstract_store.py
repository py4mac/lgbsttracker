from abc import ABCMeta, abstractmethod
from typing import List

from lgbsttracker.entities import ExperimentCreate
from lgbsttracker.store.experiment.dbmodels.experiment import Experiment


class AbstractStore:
    """
    Abstract class for Experiment.
    This class defines the API interface for front ends to connect with various types of stores.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        """
        Empty constructor for now. This is deliberately not marked as abstract, else every
        derived class would be forced to create one.
        """

    @abstractmethod
    def open(self):
        """
        Open Store
        """

    @abstractmethod
    def close(self):
        """
        Close Store
        """

    @abstractmethod
    async def create_experiment(self, entity: ExperimentCreate) -> Experiment:
        """

        :param A :py:class:`lgbsttracker.entity.ExperimentCreate` object.

        :return: A :py:class:`lgbsttracker.entity.Experiment` object.
        """

    @abstractmethod
    async def get_experiment_by_uuid(self, uuid: str) -> List[Experiment]:
        """

        :param id: Experiment Id

        :return: A list of :py:class:`lgbsttracker.entity.Experiment` objects.
        """
