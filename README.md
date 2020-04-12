<H1>lgbsttracker</H1>
<p align="center">
<img src="https://img.shields.io/github/last-commit/py4mac/lgbsttracker.svg">
<a href="https://github.com/py4mac/" target="_blank">
    <img src="https://github.com/py4mac/lgbsttracker/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/py4mac/lgbsttracker" target="_blank">
    <img src="https://codecov.io/gh/py4mac/lgbsttracker/branch/master/graph/badge.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/lgbsttracker" target="_blank">
    <img src="https://badge.fury.io/py/lgbsttracker.svg" alt="Package version">
</a>
</p>

---

**Trello Plan**: <a href="https://trello.com/b/lGICXLqL/lgbsttracker" target="_blank">https://trello.com/b/lGICXLqL/lgbsttracker</a>

**Documentation**: <a href="https://py4mac.github.io/lgbsttracker" target="_blank">https://py4mac.github.io/lgbsttracker</a>

**Source Code**: <a href="https://github.com/py4mac/lgbsttracker" target="_blank">https://github.com/py4mac/lgbsttracker</a>

---

## Requirements

Python 3.6+

## Installation

```bash
pip install lgbsttracker==0.0.3
```

## Example

### Use it with async def

```Python
from lbgsttracker import create_experiment
from lbgsttracker.entities import ExperimentCreate
...
await create_experiment(ExperimentCreate(experiment_uuid="experiment1"))
experiment = await get_experiment_by_uuid("experiment1")
_logger.info(f"Freshly created experiment: {experiment}")
```

## Environment variables

| Variable Name                    | Description                   | Default value                                         |
| -------------------------------- | ----------------------------- | ----------------------------------------------------- |
| EXPERIMENT_STORAGE_URI           | DB Experiment Storage URI     | Mandatory: to be set by the user before using library |
| SQL_DB_THREAD_POOL_EXECUTOR_SIZE | Thread pool size              | 100                                                   |
| MIN_CONNECTION_POOL_SIZE         | Minimum pool size connection  | 10                                                    |
| MAX_CONNECTION_POOL_SIZE         | Maxiumum pool size connection | 20                                                    |
| CONNECTION_POOL_RECYCLE_TIME     | Pool connection recycle time  | 30                                                    |

## Credits

- https://github.com/mlflow/mlflow/
- https://github.com/undera/pylgbst
- https://github.com/tiangolo/fastapi
- https://github.com/aalhour/cookiecutter-aiohttp-sqlalchemy/

## License

This project is licensed under the terms of the MIT license.
