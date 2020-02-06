import click

import lgbsttracker.db
from lgbsttracker import __version__


@click.group()
@click.version_option(__version__)
def cli():
    pass


cli.add_command(lgbsttracker.db.commands)

if __name__ == "__main__":
    cli()
