import warnings
from abc import ABCMeta, abstractmethod

import entrypoints

from lgbsttracker.errors import ErrorCodes
from lgbsttracker.exceptions import GenericException
from lgbsttracker.utils.uri import get_uri_scheme


class UnsupporteRegistryStoreURIException(GenericException):
    """Exception thrown when building a registry store with an unsupported URI"""

    def __init__(self, unsupported_uri, supported_uri_schemes):
        message = "Unsupported URI '{}' for registry store. Supported schemes are: {}".format(
            unsupported_uri, supported_uri_schemes
        )
        super(UnsupporteRegistryStoreURIException, self).__init__(
            message, error_code=ErrorCodes.INVALID_PARAMETER_VALUE
        )
        self.supported_uri_schemes = supported_uri_schemes


class StoreRegistry:
    """
    Abstract class defining a scheme-based registry for store implementations.

    This class allows the registration of a function or class to provide an
    implementation for a given scheme of `store_uri` through the `register`
    methods. Implementations declared though the entrypoints can be automatically
    registered through the `register_entrypoints` method.

    When instantiating a store through the `get_store` method, the scheme of
    the store URI provided (or inferred from environment) will be used to
    select which implementation to instantiate, which will be called with same
    arguments passed to the `get_store` method.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, group_name):
        self._registry = {}
        self.group_name = group_name

    def register(self, scheme, store_builder):
        self._registry[scheme] = store_builder

    def register_entrypoints(self):
        """Register stores provided by other packages"""
        for entrypoint in entrypoints.get_group_all(self.group_name):
            self.register(entrypoint.name, entrypoint.load())
            try:
                self.register(entrypoint.name, entrypoint.load())
            except (AttributeError, ImportError) as exc:
                warnings.warn(
                    'Failure attempting to register store for scheme "{}": {}'.format(entrypoint.name, str(exc)),
                    stacklevel=2,
                )

    def get_store_builder(self, uri):
        """Get a store from the registry based on the scheme of store_uri

        :param uri: The store URI. If None, it will be inferred from the environment. This
                          URI is used to select which store implementation to instantiate
                          and is passed to the constructor of the implementation.
        :return: A function that returns an instance of
                 ``lgbsttracker.store.experiment.AbstractStore`` that fulfills the store
                  URI requirements.
        """
        scheme = get_uri_scheme(uri)
        try:
            store_builder = self._registry[scheme]
        except KeyError:
            raise UnsupporteRegistryStoreURIException(
                unsupported_uri=uri, supported_uri_schemes=list(self._registry.keys())
            )
        return store_builder
