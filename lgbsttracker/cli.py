import click

from lgbsttracker.server import _run_server


@click.command()
def run():
    _run_server()


if __name__ == '__main__':
    run()
