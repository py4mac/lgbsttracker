import click

import lgbsttracker.store.db.utils


@click.group("db")
def commands():
    """
    Commands for managing databases.
    """


@commands.command()
@click.argument("url", required=False)
def upgrade_db(url):
    """
    Upgrade database to the latest supported version.

    :param url of database
    """
    from lgbsttracker.services.store._experiment_registry import utils

    url = url if url is not None else utils.get_experiment_uri()
    lgbsttracker.store.db.utils.upgrade_sql_db(url)
