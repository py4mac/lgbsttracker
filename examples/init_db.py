import logging
import asyncio

from lgbsttracker import create_experiment, get_experiment_by_uuid
from lgbsttracker.entities import ExperimentCreate

_logger = logging.getLogger("lgbsttracker.examples.init_db")


def init_experiment():

    _logger.info("[Init-Experiment] creating new rows in table: `experiment`")

    async def create_new_experiment():
        await create_experiment(ExperimentCreate(experiment_uuid="experiment1"))
        experiment = await get_experiment_by_uuid("experiment1")
        _logger.info(f"Freshly created experiment: {experiment}")

    asyncio.get_event_loop().run_until_complete(create_new_experiment())

    _logger.info("[Init-Experiment] done...")


if __name__ == "__main__":
    init_experiment()
