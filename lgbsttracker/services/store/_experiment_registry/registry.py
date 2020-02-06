from lgbsttracker.services.store.registry import StoreRegistry


class ExperimentStoreRegistry(StoreRegistry):
    """Scheme-based registry for experiment store implementations
    """

    def __init__(self):
        super(ExperimentStoreRegistry, self).__init__("lgbsttracker.experiment_store")

    def get_store(self, experiment_uri=None):
        """Get a store from the registry based on the scheme of experiment_uri

        :param uri: The store URI. If None, it will be inferred from the environment. This URI
                          is used to select which store implementation to instantiate and
                          is passed to the constructor of the implementation.

        :return: An instance of `lgbsttracker.services.store.experiment.AbstractStore` that fulfills the store URI
                 requirements.
        """
        from lgbsttracker.services.store._experiment_registry import utils

        experiment_uri = experiment_uri if experiment_uri is not None else utils.get_experiment_uri()
        builder = self.get_store_builder(experiment_uri)
        return builder(experiment_uri=experiment_uri)
