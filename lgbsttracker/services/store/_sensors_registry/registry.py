from lgbsttracker.services.store.registry import StoreRegistry


class SensorStoreRegistry(StoreRegistry):
    """Scheme-based registry for sensors store implementations

    This class allows the registration of a function or class to provide an
    implementation for a given scheme of `store_uri` through the `register`
    methods. Implementations declared though the entrypoints
    `lgbsstracker.sensors_store` group can be automatically registered through the
    `register_entrypoints` method.

    When instantiating a store through the `get_store` method, the scheme of
    the store URI provided (or inferred from environment) will be used to
    select which implementation to instantiate, which will be called with same
    arguments passed to the `get_store` method.
    """

    def __init__(self):
        super(SensorStoreRegistry, self).__init__("lgbsttracker.sensors_store")

    def get_store(self, sensor_uri=None):
        """Get a store from the registry based on the scheme of store_uri

        :param uri: The store URI. If None, it will be inferred from the environment. This URI
                          is used to select which sensor store implementation to instantiate and
                          is passed to the constructor of the implementation.

        :return: An instance of `services.store.sensors.AbstractStore` that fulfills the store URI
                 requirements.
        """
        from lgbsttracker.services.store._sensors_registry import utils

        sensor_uri = sensor_uri if sensor_uri is not None else utils.get_sensor_uri()
        builder = self.get_store_builder(sensor_uri)
        return builder(sensor_uri=sensor_uri)
