import unittest

from lgbsttracker.entities.experiment import ExperimentCreate


class TestExperimentEntity(unittest.TestCase):
    def _check(self, experiment, experiment_uuid):
        self.assertIsInstance(experiment, ExperimentCreate)
        self.assertEqual(experiment.experiment_uuid, experiment_uuid)

    def test_creation_and_hydration(self):
        experiment_uuid = "experiment1"
        s1 = ExperimentCreate(experiment_uuid=experiment_uuid)
        self._check(s1, experiment_uuid)
