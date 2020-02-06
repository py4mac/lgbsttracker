import asynctest

from lgbsttracker.store.experiment.abstract_store import AbstractStore


class AbstractStoreTestImpl(AbstractStore):
    def open(self):
        raise NotImplementedError(self)

    def close(self):
        raise NotImplementedError(self)

    async def create_experiment(self, entity):
        raise NotImplementedError(self)

    async def get_experiment_by_name(self, name):
        raise NotImplementedError(self)


class TestAbstractStoreTestCase:
    @asynctest.patch("lgbsttracker.store.experiment.abstract_store.AbstractStore.create_experiment")
    async def test_create_experiment(self, create_experiment):
        experiment = "test"
        create_experiment.return_value = experiment
        store = AbstractStore()
        ret = await store.create_experiment(None)
        assert ret == experiment
