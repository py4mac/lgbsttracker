import click

from lgbsttracker import __version__
from lgbsttracker.server import _get_api_storage_sensors_server, _get_api_doc_server, _run_server


@click.group()
@click.version_option(__version__)
def cli():
    pass


@cli.command()
def serve_api_storage_sensors():
    app = _get_api_storage_sensors_server()
    _run_server(app)


@cli.command()
def serve_api_doc():
    app = _get_api_doc_server()
    _run_server(app)


if __name__ == "__main__":
    cli()
