from abc import abstractmethod, ABCMeta


class AbstractStore:
    """
    Abstract class for Backend.
    This class defines the API interface for front ends to connect with various types of backends.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        """
        Empty constructor for now. This is deliberately not marked as abstract, else every
        derived class would be forced to create one.
        """
        pass

    @abstractmethod
    def create_light_sensor(self, name):
        """

        :param id_company: Company Identifier

        :return: A :py:class:`lgbsttracker.entities.LightSensor` object.
        """
        pass
